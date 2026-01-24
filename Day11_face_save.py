import cv2
import time

# Load face detector model (OpenCV built-in)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw rectangle around face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Face Detector | Press S to Save | X to Exit", frame)

    key = cv2.waitKey(1) & 0xFF

    # Save face image
    if key == ord('s'):
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_img = frame[y:y+h, x:x+w]
            filename = f"face_{int(time.time())}.jpg"
            cv2.imwrite(filename, face_img)
            print("Saved:", filename)
        else:
            print("No face detected!")

    # Exit
    if key == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
