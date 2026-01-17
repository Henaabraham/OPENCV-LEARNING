import cv2
import time
import os

# Folder name to store photos
save_folder = "Photos"

# Create folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("Photo Booth | Press S to Save | X to Exit", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        filename = f"selfie_{int(time.time())}.jpg"
        filepath = os.path.join(save_folder, filename)

        cv2.imwrite(filepath, frame)
        print("Saved:", filepath)

    if key == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
