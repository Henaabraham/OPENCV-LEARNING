import cv2
import time
import os

# Folder to save video clips
save_folder = "Clips"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

cap = cv2.VideoCapture(0)

# Get camera frame size
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

ret, frame1 = cap.read()
ret, frame2 = cap.read()

last_record_time = 0
record_cooldown = 8  # seconds (avoid recording again and again)
clip_duration = 5    # seconds

while True:
    # 1) Motion mask
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # 2) Find motion contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_found = False

    # 3) Draw motion boxes
    for contour in contours:
        if cv2.contourArea(contour) < 1500:
            continue

        motion_found = True
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 4) If motion found and cooldown passed → start recording
    now = time.time()
    if motion_found and (now - last_record_time) > record_cooldown:
        filename = f"clip_{int(now)}.avi"
        filepath = os.path.join(save_folder, filename)

        # Video writer settings
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")

        out = cv2.VideoWriter(filepath, fourcc, 20.0, (frame_width, frame_height))

        print("Recording started:", filepath)

        start_time = time.time()
        while (time.time() - start_time) < clip_duration:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            cv2.imshow("Day 7 CCTV Recording | X to Exit", frame)

            # allow exit during recording
            if cv2.waitKey(1) & 0xFF == ord('x'):
                break

        out.release()
        last_record_time = time.time()
        print("Recording saved ✅")

    # Show normal camera view
    cv2.imshow("Day 7 CCTV | X to Exit", frame1)

    # update frames
    frame1 = frame2
    ret, frame2 = cap.read()

    key = cv2.waitKey(1) & 0xFF
    if key == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
