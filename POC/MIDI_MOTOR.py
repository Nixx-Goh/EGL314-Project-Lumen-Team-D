import mido
import busio
import threading
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Servo setup
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x43)
pca.frequency = 50

# Map CC numbers to servo indices
CC_TO_SERVO = {
    22: 0,  # Knob A1 → Servo on channel 5
    23: 1,  # Knob A2 → Servo on channel 7
    24: 2,  # Knob A3 → Servo on channel 9
    25: 3,  # Knob A4 → Servo on channel 11
    26: 4,  # Knob A5 → Servo on channel 13
    27: 5,  # Knob A6 → Servo on channel 15
}

channels = [5, 7, 9, 11, 13, 15]
servos = [servo.Servo(pca.channels[ch]) for ch in channels]

def midi_knob_listener():
    input_name = None
    for name in mido.get_input_names():
        if "MPD218" in name:
            input_name = name
            break

    if not input_name:
        print("MPD218 not found.")
        return

    print("Listening for knob movement...")
    with mido.open_input(input_name) as port:
        for msg in port:
            if msg.type == 'control_change' and msg.control in CC_TO_SERVO:
                servo_index = CC_TO_SERVO[msg.control]
                angle = int((msg.value / 127) * 180)
                servos[servo_index].angle = angle
                print(f"Knob CC {msg.control} → Servo {servo_index+1} angle {angle}°")

try:
    thread = threading.Thread(target=midi_knob_listener, daemon=True)
    thread.start()

    while True:
        pass  # Keep the main program running

except KeyboardInterrupt:
    print("Exiting...")

finally:
    for s in servos:
        s.angle = None
    print("Servos deactivated.")
    