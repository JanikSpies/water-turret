// Moves the pan/tilt servos to angles received over serial.
//
// Protocol: one line per command, "<pan>,<tilt>\n", angles in degrees.
// Example: "90,90" centers both servos. Replies "OK <pan>,<tilt>" or "ERR <line>".

#include <Servo.h>

const long BAUD_RATE = 115200;

const int PAN_PIN = 9;
const int TILT_PIN = 10;

// Tighten these if the servos hit anything at the extremes.
const int PAN_MIN = 0;
const int PAN_MAX = 180;
const int TILT_MIN = 45;
const int TILT_MAX = 135;

const int CENTER = 90;
const int LINE_BUFFER_SIZE = 32;

Servo panServo;
Servo tiltServo;

char lineBuffer[LINE_BUFFER_SIZE];
int lineLength = 0;

void moveTo(int pan, int tilt) {
  pan = constrain(pan, PAN_MIN, PAN_MAX);
  tilt = constrain(tilt, TILT_MIN, TILT_MAX);
  panServo.write(pan);
  tiltServo.write(tilt);

  Serial.print("OK ");
  Serial.print(pan);
  Serial.print(",");
  Serial.println(tilt);
}

void handleLine(char *line) {
  int pan, tilt;
  if (sscanf(line, "%d,%d", &pan, &tilt) == 2) {
    moveTo(pan, tilt);
  } else {
    Serial.print("ERR ");
    Serial.println(line);
  }
}

void setup() {
  Serial.begin(BAUD_RATE);
  panServo.attach(PAN_PIN);
  tiltServo.attach(TILT_PIN);
  moveTo(CENTER, CENTER);
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();

    if (c == '\n' || c == '\r') {
      if (lineLength > 0) {
        lineBuffer[lineLength] = '\0';
        handleLine(lineBuffer);
        lineLength = 0;
      }
    } else if (lineLength < LINE_BUFFER_SIZE - 1) {
      lineBuffer[lineLength++] = c;
    }
  }
}
