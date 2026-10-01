from dataclasses import dataclass

from turret.vision.pose_detector import Point

# Keep in sync with the limits in firmware/turret_servos.
PAN_MIN, PAN_MAX = 0, 180
TILT_MIN, TILT_MAX = 45, 135
CENTER = 90

# Field of view of the camera, used to turn an image position into an angle.
# Rough values for a laptop webcam - tune if the turret over- or undershoots.
CAMERA_HFOV_DEG = 60
CAMERA_VFOV_DEG = 40

# How far to move towards the target each frame (0..1). Lower = smoother, slower.
SMOOTHING = 0.3


def aim_error(target: Point, frame_size: tuple[int, int]) -> tuple[float, float]:
    width, height = frame_size
    dx = (target[0] - width / 2) / (width / 2)
    dy = (target[1] - height / 2) / (height / 2)
    return dx, dy


def angles_for_error(error: tuple[float, float]) -> tuple[float, float]:
    """Fixed camera next to the turret: map the target's image position to angles."""
    dx, dy = error
    return CENTER + dx * CAMERA_HFOV_DEG / 2, CENTER + dy * CAMERA_VFOV_DEG / 2


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass
class TurretAngles:
    """Servo angles in degrees. Lower pan turns left, lower tilt points up."""

    pan: float = CENTER
    tilt: float = CENTER

    def nudge(self, d_pan: float, d_tilt: float):
        self._set(self.pan + d_pan, self.tilt + d_tilt)

    def follow(self, pan: float, tilt: float, smoothing: float = SMOOTHING):
        """Move part of the way towards the given angles."""
        self._set(
            self.pan + (pan - self.pan) * smoothing,
            self.tilt + (tilt - self.tilt) * smoothing,
        )

    def _set(self, pan: float, tilt: float):
        self.pan = _clamp(pan, PAN_MIN, PAN_MAX)
        self.tilt = _clamp(tilt, TILT_MIN, TILT_MAX)
