import tkinter as tk
import mido
import threading
import RPi.GPIO as GPIO
from time import sleep

import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# === Servo Setup ===
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x43)
pca.frequency = 50

channels = [5, 7, 9, 11, 13, 15]
servos = [servo.Servo(pca.channels[ch]) for ch in channels]

# === MIDI CC to Servo Map ===
CC_TO_SERVO = {
    22: 0,
    23: 1,
    24: 2,
    25: 3,
    26: 4,
    27: 5,
}

# === Stage + Laser Config ===
PAD_TO_STAGE = {
    36: 1,  # Pad 1
    37: 2,  # Pad 2
    38: 3,  # Pad 3
    39: 4,  # Pad 4 (new)
}

STAGE_DURATIONS = {
    1: 30,
    2: 45,
    3: 60,
    4: 75,  # 1 minute 15 seconds
}

START_BUTTON_PAD = 45  # Pad 10
RESTART_BUTTON_PAD = 46  # Pad 11

# GPIO pins for lasers (active LOW relay)
lasers = {
    "1": 17,
    "2": 27,
    "3": 22,
    "4": 23
}

# === GPIO Setup ===
GPIO.setmode(GPIO.BCM)
for pin in lasers.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # OFF initially (active LOW)


# === GUI + Stage Timer ===
class StageDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stage Display")
        self.root.attributes("-fullscreen", True)

        self.label = tk.Label(self.root, text="Select a stage", font=("Arial", 80))
        self.label.pack(expand=True)

        self.current_stage = None
        self.timer_running = False
        self.timer_id = None

    def show_stage(self, stage):
        if not self.timer_running:
            self.current_stage = stage
            self.label.config(text=f"Stage {stage}")

    def start_timer(self):
        if self.current_stage and not self.timer_running:
            duration = STAGE_DURATIONS.get(self.current_stage, 30)
            self.timer_running = True

            # Turn ON laser (active LOW)
            laser_pin = lasers.get(str(self.current_stage))
            if laser_pin is not None:
                GPIO.output(laser_pin, GPIO.LOW)
                print(f"Laser {self.current_stage} ON")

            self.run_countdown(duration)

    def run_countdown(self, seconds_left):
        if seconds_left > 0:
            self.label.config(text=f"Stage {self.current_stage}\n{seconds_left} sec")
            self.timer_id = self.root.after(1000, self.run_countdown, seconds_left - 1)
        else:
            self.label.config(text="END")
            self.timer_id = self.root.after(3000, self.reset_display)
            self.timer_running = False

            # Turn OFF laser (active LOW)
            laser_pin = lasers.get(str(self.current_stage))
            if laser_pin is not None:
                GPIO.output(laser_pin, GPIO.HIGH)
                print(f"Laser {self.current_stage} OFF")

            self.current_stage = None

    def reset_display(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        # Turn OFF all lasers
        for pin in lasers.values():
            GPIO.output(pin, GPIO.HIGH)

        self.label.config(text="Select a stage")
        self.timer_running = False
        self.current_stage = None


# === MIDI Thread: Pads → Stages ===
def midi_listener(app):
    input_name = None
    for name in mido.get_input_names():
        if "MPD218" in name:
            input_name = name
            break

    if not input_name:
        print("MPD218 not found.")
        return

    with mido.open_input(input_name) as port:
        for msg in port:
            if msg.type == 'note_on' and msg.velocity > 0:
                note = msg.note
                if note in PAD_TO_STAGE:
                    stage = PAD_TO_STAGE[note]
                    print(f"Pad {note} → Stage {stage}")
                    app.root.after(0, app.show_stage, stage)
                elif note == START_BUTTON_PAD:
                    print("Start button pressed")
                    app.root.after(0, app.start_timer)
                elif note == RESTART_BUTTON_PAD:
                    print("Restart button pressed")
                    app.root.after(0, app.reset_display)


# === MIDI Thread: Knobs → Servos ===
def knob_servo_controller():
    input_name = None
    for name in mido.get_input_names():
        if "MPD218" in name:
            input_name = name
            break

    if not input_name:
        print("MPD218 not found.")
        return

    with mido.open_input(input_name) as port:
        for msg in port:
            if msg.type == 'control_change' and msg.control in CC_TO_SERVO:
                servo_index = CC_TO_SERVO[msg.control]
                angle = int((msg.value / 127) * 180)
                servos[servo_index].angle = angle
                print(f"Knob CC {msg.control} → Servo {servo_index + 1} angle {angle}°")


# === MAIN ===
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = StageDisplayApp(root)

        threading.Thread(target=midi_listener, args=(app,), daemon=True).start()
        threading.Thread(target=knob_servo_controller, daemon=True).start()

        root.mainloop()

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        for s in servos:
            s.angle = None
        for pin in lasers.values():
            GPIO.output(pin, GPIO.HIGH)
        GPIO.cleanup()
        print("GPIO and servos deactivated.")
