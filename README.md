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

## Run

```Shell
python -m turret.main
```

Steer the turret with the arrow keys (or WASD), press `q` to quit.
The Arduino is auto-detected; pass `--port /dev/...` to override.

## Firmware

`firmware/turret_servos` drives the pan/tilt servos. Open it in the Arduino IDE and upload it.

Wiring:

| Servo wire      | Connects to                         |
| --------------- | ----------------------------------- |
| Pan signal      | Arduino pin 9                       |
| Tilt signal     | Arduino pin 10                      |
| Red (+)         | External 5–6 V supply +             |
| Brown/black (−) | External supply − **and** Arduino GND |

Send `<pan>,<tilt>` (e.g. `90,90`) at 115200 baud with a newline.
