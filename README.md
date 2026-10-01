# Water Turret

it goes pew pew in your face


## Local Setup

Install dependencies

```Shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install Google `pose_landmarker_lite`

```
mkdir -p models
curl -L -o models/pose_landmarker_lite.task \
  https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task
```
