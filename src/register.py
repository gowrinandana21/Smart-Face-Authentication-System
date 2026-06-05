import cv2
import os
import sys

# Get name from Flask
if len(sys.argv) < 2:
    print("Please provide a name")
    sys.exit()

name = sys.argv[1]

folder = f"dataset/{name}"

if not os.path.exists(folder):
    os.makedirs(folder)

cap = cv2.VideoCapture(0)

count = 0

print(f"Registering {name}")
print("Press SPACE to capture image")
print("Press ESC to quit")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    cv2.putText(
        frame,
        f"{name} | Images: {count}/50",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1)

    if key == 32:

        img_path = f"{folder}/img_{count}.jpg"

        cv2.imwrite(
            img_path,
            frame
        )

        print(f"Saved {img_path}")

        count += 1

    if key == 27:
        break

    if count >= 50:
        break

cap.release()
cv2.destroyAllWindows()

print("Registration Complete!")
