import mido

pad_labels = {
    80: "ON",
    81: "OFF",
    82: "RESET",
    83: "1",
    76: "2",
    77: "3",
    78: "4",
}

# Optional: give friendly names to control numbers
knob_labels = {
    1: "MIRROR 1",  # Pretend control #3 is control #1
    2: "MIRROR 2",
    4: "MIRROR 3",
    5: "MIRROR 4",
    6: "MIRROR 5",
    7: "MIRROR 6"
}

# Remapping table (hardware control → virtual control)
remap_controls = {
    3: 1,  # Treat control 3 as control 1 
    9: 2,
    12: 4,
    13: 5,
    14: 6,
    15: 7
}

def open_mpd218():
    mpd218_name = None
    for name in mido.get_input_names():
        if 'MPD218' in name:
            mpd218_name = name
            break

    if not mpd218_name:
        print("MPD218 not found.")
        return

    with mido.open_input(mpd218_name) as inport:
        print(f"Listening on {mpd218_name}...")
        try:
            for msg in inport:
                if msg.type == 'note_on':
                    label = pad_labels.get(msg.note, f"Unknown Note {msg.note}")
                    # print(f"Pad Pressed: {label}")
                    print(f"PAD: {label}")
                elif msg.type == 'control_change':
                    # Remap control number if needed
                    control = remap_controls.get(msg.control, msg.control)
                    scaled_value = round((msg.value / 127) * 100)
                    label = knob_labels.get(control, f"Knob {control}")
                    print(f"{label}: {scaled_value}%")
        except KeyboardInterrupt:
            print("Stopped.")

if _name_ == "_main_":
    open_mpd218()