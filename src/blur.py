import cv2

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    blur_score = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    if blur_score < 100:

        status = "BLUR"

    else:

        status = "CLEAR"

    cv2.putText(
        frame,
        f"Status: {status}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.putText(
        frame,
        f"Score: {int(blur_score)}",
        (20,80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow(
        "Blur Detection",
        frame
    )

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()
