#1.Simple PHOTOBOOTH

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

#2.Save the Photos inside a Folder

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

#3.Add a Timestamp

import cv2
import time
import os

save_folder = "Photos"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Show live camera
    cv2.imshow("Photo Booth | Press S to Save | X to Exit", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        # Create readable date & time text
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Put timestamp on the frame (bottom-left)
        cv2.putText(frame, stamp, (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Save with unique name
        filename = f"selfie_{int(time.time())}.jpg"
        filepath = os.path.join(save_folder, filename)

        cv2.imwrite(filepath, frame)
        print("Saved:", filepath)

    if key == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
