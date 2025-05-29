import tkinter as tk
import mido
import threading

PAD_TO_STAGE = {
    36: 1,  # Pad 1
    37: 2,  # Pad 2
    38: 3,  # Pad 3
}

STAGE_DURATIONS = {
    1: 30,
    2: 45,
    3: 60,
}

START_BUTTON_PAD = 39  # Pad 4
RESTART_BUTTON_PAD = 43  # Pad 8

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
            self.run_countdown(duration)

    def run_countdown(self, seconds_left):
        if seconds_left > 0:
            self.label.config(text=f"Stage {self.current_stage}\n{seconds_left} sec")
            self.timer_id = self.root.after(1000, self.run_countdown, seconds_left - 1)
        else:
            self.label.config(text="END")
            self.timer_id = self.root.after(3000, self.reset_display)
            self.timer_running = False
            self.current_stage = None

    def reset_display(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.label.config(text="Select a stage")
        self.timer_running = False
        self.current_stage = None

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

if __name__ == "__main__":
    root = tk.Tk()
    app = StageDisplayApp(root)

    midi_thread = threading.Thread(target=midi_listener, args=(app,), daemon=True)
    midi_thread.start()

    root.mainloop()
