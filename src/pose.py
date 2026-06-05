import cv2
import face_recognition

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)

    h, w, _ = frame.shape

    direction = "NO FACE"

    for (top, right, bottom, left) in face_locations:

        center_x = (left + right) // 2

        if center_x < w * 0.4:
            direction = "LEFT"

        elif center_x > w * 0.6:
            direction = "RIGHT"

        else:
            direction = "CENTER"

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            2
        )

    cv2.putText(
        frame,
        f"Direction: {direction}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "Face Direction Detection",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
