import cv2
import time

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    cv2.imshow("PhotoBooth | Press 's' to save | x to exit", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        filename = f"photobooth_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        print("Saved:", filename)

    if key == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()