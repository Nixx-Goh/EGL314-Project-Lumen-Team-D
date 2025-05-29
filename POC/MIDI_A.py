import tkinter as tk
import mido
import threading
import time
import RPi.GPIO as GPIO
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# LASER RELAY SETUP
lasers = {
    "1": 17,
    "2": 27,
    "3": 22,
    "4": 23
}
for pin in lasers.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # OFF (active LOW relay)

# LIGHT SENSOR SETUP
SENSOR_PINS = {
    "1": 5,   # WIN
    "2": 6,   # LOSE
    "3": 12,  # LOSE
    "4": 16   # LOSE
}
for pin in SENSOR_PINS.values():
    GPIO.setup(pin, GPIO.IN)

# STAGE CONFIG
PAD_TO_STAGE = {
    36: 1,
    37: 2,
    38: 3,
    39: 4  # pad 4 = stage 4
}
STAGE_DURATIONS = {
    1: 30,
    2: 45,
    3: 60,
    4: 75
}
START_BUTTON_PAD = 45  # pad 10
RESTART_BUTTON_PAD = 46  # pad 11

# SERVO SETUP
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x43)
pca.frequency = 50
channels = [5, 7, 9, 11, 13, 15]
servos = [servo.Servo(pca.channels[i]) for i in channels]
servo_angles = [90] * 6  # initialize to center
for s in servos:
    s.angle = 90

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
        self.sensor_triggered = False
        self.sensor_thread = None

    def show_stage(self, stage):
        if not self.timer_running:
            self.current_stage = stage
            self.label.config(text=f"Stage {stage}")

    def start_timer(self):
        if self.current_stage and not self.timer_running:
            duration = STAGE_DURATIONS.get(self.current_stage, 30)
            self.timer_running = True
            self.sensor_triggered = False

            # Turn on laser
            laser_pin = lasers.get(str(self.current_stage))
            if laser_pin:
                GPIO.output(laser_pin, GPIO.LOW)

            self.sensor_thread = threading.Thread(target=self.monitor_sensors)
            self.sensor_thread.start()

            self.run_countdown(duration)

    def run_countdown(self, seconds_left):
        if self.timer_running and not self.sensor_triggered:
            if seconds_left > 0:
                self.label.config(text=f"Stage {self.current_stage}\n{seconds_left} sec")
                self.timer_id = self.root.after(1000, self.run_countdown, seconds_left - 1)
            else:
                self.stop_stage("END")

    def stop_stage(self, result_text="END"):
        self.timer_running = False
        self.sensor_triggered = True

        # Turn off laser
        laser_pin = lasers.get(str(self.current_stage))
        if laser_pin:
            GPIO.output(laser_pin, GPIO.HIGH)

        self.label.config(text=result_text)
        self.root.after(3000, self.reset_display)

    def reset_display(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.label.config(text="Select a stage")
        self.timer_running = False
        self.sensor_triggered = False
        self.current_stage = None

    def monitor_sensors(self):
        sensor_1_lit_time = 0
        other_lit_time = [0, 0, 0]
        last_check = time.time()

        while self.timer_running and not self.sensor_triggered:
            now = time.time()
            elapsed = now - last_check
            last_check = now

            if GPIO.input(SENSOR_PINS["1"]):
                sensor_1_lit_time += elapsed
            else:
                sensor_1_lit_time = 0

            for i, key in enumerate(["2", "3", "4"]):
                if GPIO.input(SENSOR_PINS[key]):
                    other_lit_time[i] += elapsed
                else:
                    other_lit_time[i] = 0

            if sensor_1_lit_time >= 5:
                print("WIN condition met")
                self.root.after(0, self.stop_stage, "WIN")
                break

            if any(t >= 3 for t in other_lit_time):
                print("LOSE condition met")
                self.root.after(0, self.stop_stage, "LOSE")
                break

            time.sleep(0.1)

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

            elif msg.type == 'control_change':
                cc = msg.control
                val = msg.value
                servo_index = cc % len(servos)
                angle = int(val * 180 / 127)
                servos[servo_index].angle = angle
                servo_angles[servo_index] = angle

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = StageDisplayApp(root)

        midi_thread = threading.Thread(target=midi_listener, args=(app,), daemon=True)
        midi_thread.start()

        root.mainloop()
    finally:
        for pin in lasers.values():
            GPIO.output(pin, GPIO.HIGH)
        GPIO.cleanup()
        for s in servos:
            s.angle = None
        print("System shut down.")
