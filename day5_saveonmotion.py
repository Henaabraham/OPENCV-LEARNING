import cv2
import time


def get_motion_mask(frame1, frame2):
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  
    return thresh


def main():
    cap = cv2.VideoCapture(0)

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    last_saved_time = 0  # to avoid saving 100 photos per second

    while True:
        motion_mask = get_motion_mask(frame1, frame2)

        # How much motion is there?
        motion_pixels = cv2.countNonZero(motion_mask)

        # If motion is big enough AND 2 seconds passed since last save
        if motion_pixels > 5000 and (time.time() - last_saved_time) > 2:
            filename = f"motion_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame1)
            print("Saved:", filename)
            last_saved_time = time.time()

        cv2.imshow("Motion Mask", motion_mask)
        cv2.imshow("Camera", frame1)

        frame1 = frame2
        ret, frame2 = cap.read()

        key = cv2.waitKey(1) & 0xFF
        if key == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
