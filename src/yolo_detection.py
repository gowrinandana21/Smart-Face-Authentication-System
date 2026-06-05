from ultralytics import YOLO
import cv2

# Load YOLOv8 Nano Model
model = YOLO("yolov8n.pt")

# Webcam
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Run YOLO Detection
    results = model(frame)

    # Draw detections
    annotated_frame = results[0].plot()

    # Count persons
    person_count = 0

    for box in results[0].boxes:

        cls = int(box.cls[0])

        # COCO class 0 = Person
        if cls == 0:
            person_count += 1

    cv2.putText(
        annotated_frame,
        f"Persons Detected: {person_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "YOLOv8 Person Detection",
        annotated_frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
