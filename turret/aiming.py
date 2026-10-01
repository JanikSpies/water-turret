from dataclasses import dataclass

from turret.vision.pose_detector import Point

# Keep in sync with the limits in firmware/turret_servos.
PAN_MIN, PAN_MAX = 0, 180
TILT_MIN, TILT_MAX = 45, 135
CENTER = 90


def aim_error(target: Point, frame_size: tuple[int, int]) -> tuple[float, float]:
    width, height = frame_size
    dx = (target[0] - width / 2) / (width / 2)
    dy = (target[1] - height / 2) / (height / 2)
    return dx, dy


@dataclass
class TurretAngles:
    """Servo angles in degrees. Lower pan turns left, lower tilt points up."""

    pan: int = CENTER
    tilt: int = CENTER

    def nudge(self, d_pan: int, d_tilt: int):
        self.pan = max(PAN_MIN, min(PAN_MAX, self.pan + d_pan))
        self.tilt = max(TILT_MIN, min(TILT_MAX, self.tilt + d_tilt))
