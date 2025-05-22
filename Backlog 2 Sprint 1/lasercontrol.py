import RPi.GPIO as GPIO

# Define GPIO pins for each laser
lasers = {
    "1": 17,
    "2": 27,
    "3": 22,
    "4": 23
}

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in lasers.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Set all lasers OFF initially (relays inactive)

# Control functions
def turn_on(laser_number):
    GPIO.output(lasers[laser_number], GPIO.LOW)  # Relay active = laser ON
    print(f"Laser {laser_number} turned ON")

def turn_off(laser_number):
    GPIO.output(lasers[laser_number], GPIO.HIGH)  # Relay inactive = laser OFF
    print(f"Laser {laser_number} turned OFF")

# Command loop
try:
    print("Laser Control Console")
    print("Commands: on [1-4], off [1-4], exit")

    while True:
        command = input("Command: ").strip().lower()

        if command == "exit":
            break
        elif command.startswith("on "):
            num = command.split(" ")[1]
            if num in lasers:
                turn_on(num)
            else:
                print("Invalid laser number.")
        elif command.startswith("off "):
            num = command.split(" ")[1]
            if num in lasers:
                turn_off(num)
            else:
                print("Invalid laser number.")
        else:
            print("Invalid command.")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up. Program exited.")
