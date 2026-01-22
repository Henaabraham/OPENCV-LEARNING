import cv2
import time
import os

# ---------- SETTINGS ----------
FOLDER_NAME = "Captures"
MIN_MOTION_SIZE = 1500
SAVE_DELAY = 3
THRESH_VALUE = 20
# ----------------------------


def make_folder():
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)


def get_motion_mask(frame_a, frame_b):
    difference = cv2.absdiff(frame_a, frame_b)
    gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, mask = cv2.threshold(blur, THRESH_VALUE, 255, cv2.THRESH_BINARY)
    return mask


def draw_boxes(frame, mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    motion_found = False

    for contour in contours:
        if cv2.contourArea(contour) < MIN_MOTION_SIZE:
            continue

        motion_found = True
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return motion_found


def save_photo(frame):
    filename = f"motion_{int(time.time())}.jpg"
    path = os.path.join(FOLDER_NAME, filename)
    cv2.imwrite(path, frame)
    print("Saved:", path)


def put_dashboard_text(frame, motion_found, motion_count):
    # Status text
    status = "MOTION DETECTED" if motion_found else "NO MOTION"
    cv2.putText(frame, status, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Motion count
    cv2.putText(frame, f"Count: {motion_count}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Show settings on screen
    cv2.putText(frame, f"Threshold: {THRESH_VALUE}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(frame, f"Min Area: {MIN_MOTION_SIZE}", (20, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(frame, f"Cooldown: {SAVE_DELAY}s", (20, 180),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


def main():
    make_folder()

    cam = cv2.VideoCapture(0)

    ok, frame1 = cam.read()
    ok, frame2 = cam.read()

    last_save_time = 0
    motion_count = 0

    while True:
        mask = get_motion_mask(frame1, frame2)

        motion_found = draw_boxes(frame1, mask)

        now = time.time()
        if motion_found and (now - last_save_time) > SAVE_DELAY:
            save_photo(frame1)
            motion_count += 1
            last_save_time = now

        put_dashboard_text(frame1, motion_found, motion_count)

        cv2.imshow("Day 9 CCTV Dashboard | X to Exit", frame1)

        frame1 = frame2
        ok, frame2 = cam.read()

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
