import face_recognition
import cv2
import os
import csv
from datetime import datetime

# -------------------------
# Load Known Faces
# -------------------------

known_encodings = []
known_names = []

dataset_path = "dataset"

print("Loading faces...")

for person in os.listdir(dataset_path):

    person_folder = os.path.join(dataset_path, person)

    if not os.path.isdir(person_folder):
        continue

    for image_name in os.listdir(person_folder):

        image_path = os.path.join(person_folder, image_name)

        try:

            image = face_recognition.load_image_file(
                image_path
            )

            encodings = face_recognition.face_encodings(
                image
            )

            if len(encodings) > 0:

                known_encodings.append(
                    encodings[0]
                )

                known_names.append(
                    person
                )

        except Exception as e:

            print(
                f"Error loading {image_path}"
            )
            print(e)

print("Faces Loaded Successfully!")

# -------------------------
# Attendance File
# -------------------------

os.makedirs(
    "logs",
    exist_ok=True
)

attendance_file = "logs/attendance.csv"

if not os.path.exists(attendance_file):

    with open(
        attendance_file,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Name",
            "Login Time",
            "Logout Time"
        ])

# -------------------------
# Logged Users
# -------------------------

logged_in_users = {}

# -------------------------
# Blur Detection
# -------------------------

def is_blurry(frame):

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    score = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    return score < 100

# -------------------------
# Webcam
# -------------------------

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    face_locations = face_recognition.face_locations(
        rgb,
        model="hog"
    )

    face_encodings = face_recognition.face_encodings(
        rgb,
        face_locations
    )

    # -------------------------
    # Blur Status
    # -------------------------

    blur_status = (
        "BLUR"
        if is_blurry(frame)
        else "CLEAR"
    )

    cv2.putText(
        frame,
        f"Blur: {blur_status}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    # -------------------------
    # Face Count
    # -------------------------

    face_count = len(
        face_locations
    )

    cv2.putText(
        frame,
        f"Faces: {face_count}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    # -------------------------
    # Direction Detection
    # -------------------------

    direction = "NO FACE"

    h, w, _ = frame.shape

    for (top, right, bottom, left) in face_locations:

        center_x = (left + right) // 2

        if center_x < w * 0.4:
            direction = "LEFT"

        elif center_x > w * 0.6:
            direction = "RIGHT"

        else:
            direction = "CENTER"

    cv2.putText(
        frame,
        f"Direction: {direction}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # -------------------------
    # Multiple Faces
    # -------------------------

    if face_count > 1:

        cv2.putText(
            frame,
            "ACCESS DENIED",
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        cv2.imshow(
            "Smart Face Authentication",
            frame
        )

        if cv2.waitKey(1) == 27:
            break

        continue

    # -------------------------
    # Face Recognition
    # -------------------------

    for face_encoding, face_location in zip(
        face_encodings,
        face_locations
    ):

        name = "Unknown"

        matches = face_recognition.compare_faces(
            known_encodings,
            face_encoding,
            tolerance=0.5
        )

        if True in matches:

            match_index = matches.index(
                True
            )

            name = known_names[
                match_index
            ]

            if name not in logged_in_users:

                login_time = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                logged_in_users[
                    name
                ] = login_time

                with open(
                    attendance_file,
                    "a",
                    newline=""
                ) as file:

                    writer = csv.writer(
                        file
                    )

                    writer.writerow([
                        name,
                        login_time,
                        ""
                    ])

                print(
                    f"{name} Logged In"
                )

        top, right, bottom, left = face_location

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            2
        )

        status = (
            "SUCCESS"
            if name != "Unknown"
            else "FAILED"
        )

        cv2.putText(
            frame,
            f"Person: {name}",
            (left, top - 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Auth: {status}",
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

    cv2.imshow(
        "Smart Face Authentication System",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

# -------------------------
# Logout Update
# -------------------------

for user in logged_in_users:

    logout_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        attendance_file,
        "r"
    ) as file:

        rows = list(
            csv.reader(file)
        )

    for i in range(
        len(rows) - 1,
        0,
        -1
    ):

        if (
            rows[i][0] == user
            and rows[i][2] == ""
        ):

            rows[i][2] = logout_time
            break

    with open(
        attendance_file,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerows(
            rows
        )

cap.release()
cv2.destroyAllWindows()
