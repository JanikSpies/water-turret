import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_tasks
from mediapipe.tasks.python import vision


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Couldn't connect to camera")

    base_options = mp_tasks.BaseOptions(
        model_asset_path="models/pose_landmarker_lite.task",
        delegate=mp_tasks.BaseOptions.Delegate.CPU,
    )
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_poses=1,
    )
    detector = vision.PoseLandmarker.create_from_options(options)

    start_time = time.monotonic()

    while True:
        success, frame = cap.read()
        if not success:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp_ms = int((time.monotonic() - start_time) * 1000)
        result = detector.detect_for_video(mp_image, timestamp_ms)

        if result.pose_landmarks:
            nose = result.pose_landmarks[0][0]
            print(f"Nose: x={nose.x:.2f} y={nose.y:.2f}")
        else:
            print("No person")

        cv2.imshow("Test", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    detector.close()


if __name__ == "__main__":
    main()