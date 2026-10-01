import cv2

from turret import overlay
from turret.aiming import aim_error
from turret.vision.pose_detector import PoseDetector

WINDOW_NAME = "Water Turret"


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Couldn't connect to camera")

    with PoseDetector() as detector:
        while True:
            success, frame = cap.read()
            if not success:
                break

            detection = detector.detect(frame)

            overlay.draw_crosshair(frame)
            if detection:
                height, width = frame.shape[:2]
                error = aim_error(detection.target, (width, height))
                overlay.draw_detection(frame, detection)
                overlay.draw_aim(frame, detection.target, error)

            cv2.imshow(WINDOW_NAME, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
