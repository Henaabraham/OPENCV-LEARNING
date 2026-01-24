import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow("My Webcam", frame)
    cv2.imshow("Hena Camera", gray)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
