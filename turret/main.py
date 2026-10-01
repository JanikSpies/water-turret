import argparse
from contextlib import nullcontext

import cv2

from turret import overlay
from turret.aiming import TurretAngles, aim_error
from turret.controls import QUIT_KEYS, key_to_nudge
from turret.hardware.servo_link import ServoLink, find_arduino_port
from turret.vision.pose_detector import PoseDetector

WINDOW_NAME = "Water Turret"


def parse_args():
    parser = argparse.ArgumentParser(description="Water turret")
    parser.add_argument("--port", help="Arduino serial port (auto-detected if omitted)")
    return parser.parse_args()


def open_servos(port: str | None):
    port = port or find_arduino_port()
    if port is None:
        print("No Arduino found - running without servos")
        return nullcontext()
    print(f"Connecting to Arduino on {port}")
    return ServoLink(port)


def main():
    args = parse_args()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Couldn't connect to camera")

    angles = TurretAngles()

    with PoseDetector() as detector, open_servos(args.port) as servos:
        if servos:
            servos.move(angles.pan, angles.tilt)

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
            overlay.draw_angles(frame, angles.pan, angles.tilt)

            cv2.imshow(WINDOW_NAME, frame)
            key = cv2.waitKeyEx(1)
            if key in QUIT_KEYS:
                break

            nudge = key_to_nudge(key)
            if nudge:
                angles.nudge(*nudge)
                if servos:
                    servos.move(angles.pan, angles.tilt)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
