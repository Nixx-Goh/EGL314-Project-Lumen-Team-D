from time import sleep
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
from adafruit_motor import servo

# Set up I2C and PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x43)
pca.frequency = 50  # Standard for hobby servos

# Define the channels your servos are connected to
channels = [5, 7, 9, 11, 13, 15]
servos = [servo.Servo(pca.channels[i]) for i in channels]

try:
    while True:
        user_input = input("Enter angle (0 to 180), or 'q' to quit: ")
        if user_input.lower() == 'q':
            print("Exiting program. Centering servos...")
            for s in servos:
                s.angle = 90  # center
            break
        try:
            angle = float(user_input)
            if 0 <= angle <= 180:
                for s in servos:
                    s.angle = angle
                print(f"All servos set to {angle}°")
            else:
                print("Please enter a number between 0 and 180.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")

except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
finally:
    # Optional: turn off PWM signals
    for s in servos:
        s.angle = None
    print("Servos deactivated.")