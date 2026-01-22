import cv2
import time
import os


# ---------- SETTINGS ----------
SAVE_FOLDER = "Captures"
MIN_AREA = 1500
COOLDOWN_SECONDS = 3
THRESHOLD_VALUE = 20
# -----------------------------


def setup_folder(folder_name):
    """Create folder if not exists."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def get_motion_mask(frame1, frame2):
    """Return black & white mask where white = motion."""
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
    return thresh


def draw_motion_boxes(frame, motion_mask):
    """Draw green boxes on moving regions."""
    contours, _ = cv2.findContours(
        motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    motion_found = False

    for contour in contours:
        if cv2.contourArea(contour) < MIN_AREA:
            continue

        motion_found = True
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return motion_found


def save_motion_photo(frame):
    """Save current frame as motion proof image."""
    filename = f"motion_{int(time.time())}.jpg"
    filepath = os.path.join(SAVE_FOLDER, filename)
    cv2.imwrite(filepath, frame)
    print("Saved:", filepath)


def main():
    setup_folder(SAVE_FOLDER)

    cap = cv2.VideoCapture(0)

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    last_saved_time = 0

    while True:
        motion_mask = get_motion_mask(frame1, frame2)

        # draw boxes + check motion
        motion_found = draw_motion_boxes(frame1, motion_mask)

        # save photo when motion found + cooldown passed
        now = time.time()
        if motion_found and (now - last_saved_time) > COOLDOWN_SECONDS:
            save_motion_photo(frame1)
            last_saved_time = now

        cv2.imshow("Day 8 Clean CCTV | X to Exit", frame1)

        # update frames
        frame1 = frame2
        ret, frame2 = cap.read()

        key = cv2.waitKey(1) & 0xFF
        if key == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
