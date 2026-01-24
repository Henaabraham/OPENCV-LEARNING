import cv2
import time
import os

save_folder = "Captures"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

last_saved_time = 0
motion_count = 0

while True:
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_found = False

    for contour in contours:
        if cv2.contourArea(contour) < 1500:
            continue

        motion_found = True
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Text status
    status_text = "MOTION DETECTED" if motion_found else "NO MOTION"
    cv2.putText(frame1, status_text, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Save + count with cooldown
    if motion_found and (time.time() - last_saved_time) > 3:
        motion_count += 1
        filename = f"motion_{int(time.time())}.jpg"
        filepath = os.path.join(save_folder, filename)
        cv2.imwrite(filepath, frame1)
        print("Saved:", filepath)
        last_saved_time = time.time()

    # Show count
    cv2.putText(frame1, f"Count: {motion_count}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Day 6 CCTV Counter | X to Exit", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()

    key = cv2.waitKey(1) & 0xFF
    if key == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
