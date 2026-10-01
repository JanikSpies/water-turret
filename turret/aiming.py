from turret.vision.pose_detector import Point


def aim_error(target: Point, frame_size: tuple[int, int]) -> tuple[float, float]:
    width, height = frame_size
    dx = (target[0] - width / 2) / (width / 2)
    dy = (target[1] - height / 2) / (height / 2)
    return dx, dy
