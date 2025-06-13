import tkinter as tk
import mido
import threading
import RPi.GPIO as GPIO
import time
from time import sleep
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
from adafruit_motor import servo

# ==== Servo Setup ====
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x43)
pca.frequency = 50

channels = [5, 7, 9, 11, 13, 15]
servos = [servo.Servo(pca.channels[i]) for i in channels]
servo_angles = [90] * 6  # Start centered

# ==== Laser Setup ====
LASERS = {
    1: 17,
    2: 27,
    3: 22,
    4: 23
}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in LASERS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

# ==== Light Sensors ====
SENSOR_PINS = {
    "win1": 6,
    "win2": 12,
    "lose1": 5,
    "lose2": 16
}

for pin in SENSOR_PINS.values():
    GPIO.setup(pin, GPIO.IN)

PAD_TO_STAGE = {
    36: 1,  # Pad 1
    37: 2   # Pad 2
}

STAGE_DURATIONS = {
    1: 30,
    2: 45
}

START_BUTTON_PAD = 45  # Pad 10
RESTART_BUTTON_PAD = 46  # Pad 11

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
        self.light_thread = None

    def show_stage(self, stage):
        if not self.timer_running:
            self.current_stage = stage
            self.label.config(text=f"Stage {stage}")

    def start_timer(self):
        if self.current_stage and not self.timer_running:
            duration = STAGE_DURATIONS.get(self.current_stage, 30)
            if self.current_stage == 1:
                GPIO.output(LASERS[1], GPIO.LOW)
                GPIO.output(LASERS[2], GPIO.LOW)
            elif self.current_stage == 2:
                GPIO.output(LASERS[3], GPIO.LOW)
                GPIO.output(LASERS[4], GPIO.LOW)
            self.timer_running = True
            self.light_thread = threading.Thread(target=self.monitor_lights, daemon=True)
            self.light_thread.start()
            self.run_countdown(duration)

    def run_countdown(self, seconds_left):
        if seconds_left > 0 and self.timer_running:
            self.label.config(text=f"Stage {self.current_stage}\n{seconds_left} sec")
            self.timer_id = self.root.after(1000, self.run_countdown, seconds_left - 1)
        else:
            self.end_stage("END")

    def end_stage(self, message):
        self.timer_running = False
        self.current_stage = None
        GPIO.output(list(LASERS.values()), GPIO.LOW)
        self.label.config(text=message)
        self.timer_id = self.root.after(3000, self.reset_display)

    def reset_display(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.label.config(text="Select a stage")
        self.timer_running = False
        self.current_stage = None
        for pin in LASERS.values():
            GPIO.output(pin, GPIO.HIGH)

    def monitor_lights(self):
        lit_times = {name: None for name in SENSOR_PINS}
        while self.timer_running:
            current_time = time.time()
            for name, pin in SENSOR_PINS.items():
                if GPIO.input(pin):
                    if lit_times[name] is None:
                        lit_times[name] = current_time
                    else:
                        duration = current_time - lit_times[name]
                        if name.startswith("win") and duration >= 2:
                            self.end_stage("WIN")
                            return
                        elif name.startswith("lose") and duration >= 2:
                            self.end_stage("LOSE")
                            return
                else:
                    lit_times[name] = None
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

                CC_TO_SERVO = {
                    22: 0,
                    23: 1,
                    24: 2,
                    25: 3,
                    26: 4,
                    27: 5
                }

                if cc in CC_TO_SERVO:
                    servo_index = CC_TO_SERVO[cc]
                    angle = int(val * 180 / 127)  # Reduced sensitivity removed, full range restored
                    servos[servo_index].angle = angle

if __name__ == "__main__":
    root = tk.Tk()
    app = StageDisplayApp(root)

    midi_thread = threading.Thread(target=midi_listener, args=(app,), daemon=True)
    midi_thread.start()

    root.mainloop()
