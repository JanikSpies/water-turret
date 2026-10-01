import time

import serial
from serial.tools import list_ports

BAUD_RATE = 115200
ARDUINO_VENDOR_IDS = {0x2341, 0x2A03}
RESET_DELAY_S = 2.0


def find_arduino_port() -> str | None:
    for port in list_ports.comports():
        if port.vid in ARDUINO_VENDOR_IDS:
            return port.device
    return None


class ServoLink:
    """Sends pan/tilt angles to the Arduino running firmware/turret_servos."""

    def __init__(self, port: str):
        self._serial = serial.Serial(port, BAUD_RATE, timeout=0)
        self._last_sent: tuple[int, int] | None = None
        # The Uno resets when the port opens; give it time to boot.
        time.sleep(RESET_DELAY_S)

    def move(self, pan: float, tilt: float):
        command = (round(pan), round(tilt))
        if command == self._last_sent:
            return
        self._last_sent = command

        # We don't use the "OK" replies, so drop them before they pile up.
        self._serial.reset_input_buffer()
        self._serial.write(f"{command[0]},{command[1]}\n".encode())

    def close(self):
        self._serial.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
