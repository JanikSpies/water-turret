import time
from dataclasses import dataclass
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_tasks
from mediapipe.tasks.python import vision

DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parents[2] / "models" / "pose_landmarker_lite.task"
)
NOSE = 0

Point = tuple[int, int]


@dataclass
class Detection:
    points: list[Point]
    target: Point


class PoseDetector:
    """Finds one person in a BGR frame and returns their landmarks in pixels."""

    def __init__(self, model_path: Path = DEFAULT_MODEL_PATH):
        options = vision.PoseLandmarkerOptions(
            base_options=mp_tasks.BaseOptions(
                model_asset_path=str(model_path),
                delegate=mp_tasks.BaseOptions.Delegate.CPU,
            ),
            running_mode=vision.RunningMode.VIDEO,
            num_poses=1,
        )
        self._landmarker = vision.PoseLandmarker.create_from_options(options)
        self._start_time = time.monotonic()

    def detect(self, frame) -> Detection | None:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp_ms = int((time.monotonic() - self._start_time) * 1000)
        result = self._landmarker.detect_for_video(mp_image, timestamp_ms)

        if not result.pose_landmarks:
            return None

        height, width = frame.shape[:2]
        points = [
            (int(landmark.x * width), int(landmark.y * height))
            for landmark in result.pose_landmarks[0]
        ]
        return Detection(points=points, target=points[NOSE])

    def close(self):
        self._landmarker.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
