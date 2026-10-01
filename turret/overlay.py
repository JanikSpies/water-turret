import cv2

from turret.vision.pose_detector import Detection

GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (0, 255, 255)


def frame_center(frame) -> tuple[int, int]:
    height, width = frame.shape[:2]
    return width // 2, height // 2


def draw_crosshair(frame, size: int = 20):
    cx, cy = frame_center(frame)
    cv2.line(frame, (cx - size, cy), (cx + size, cy), WHITE, 2)
    cv2.line(frame, (cx, cy - size), (cx, cy + size), WHITE, 2)


def draw_detection(frame, detection: Detection):
    for point in detection.points:
        cv2.circle(frame, point, 4, GREEN, -1)
    cv2.circle(frame, detection.target, 8, RED, -1)


def draw_angles(frame, pan: int, tilt: int):
    cv2.putText(
        frame,
        f"pan={pan} tilt={tilt}",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        WHITE,
        2,
    )


def draw_aim(frame, target, error: tuple[float, float]):
    cv2.line(frame, frame_center(frame), target, YELLOW, 2)
    dx, dy = error
    cv2.putText(
        frame,
        f"dx={dx:+.2f} dy={dy:+.2f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        YELLOW,
        2,
    )
