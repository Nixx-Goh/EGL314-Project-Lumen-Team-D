# 🔍 Overview
Project L.U.M.E.N is an experiental/exploratory initiative that invites you to re-awaken the "Temple of Lumen" using modern audio visual technology. The stations, or also known as "Shrines" includes:

1. Beam Circuit
2. Wall Glyphs Silent Sequence
3. Prism Cipher
4. Windle: The 5 Tone Cipher

In this repository, we will be focusing on **Station 1 - Beam Circuit**.

# ℹ️ Introduction to Station 1 - Beam Circuit
In this station, players are tested on not only their observation skills, but also their logical and reaction time as they need to avoid the light sensors placed along the walls that are ostracizing the laser path to reach the final light sensor placed in the center.

 **Raspberry Pi** and other elements such as **Laser, Light Sensors, PCA9685 Servo Driver, MPD218 MIDI Pad and Servo Motors** are used to create a fun and interactive experience.

# 🛠️ Dependencies

 The **Raspberry Pi** acts as the master, which then connects and controls the other elements:

 * **Laser:** To create a laser path for players to navigate through the maze

 * **Light Sensors:** To detect laser path to determine success or failure

 * **PCA9685 Servo Driver:** To support Raspberry Pi to control the servo motor by using I²C 

* **MPD218 MIDI Pad**: To start game, end game, set servo motors to respective stages preset, and rotate respective motors to get desired angle

 * **Servo Motor:** To have mirrors attached and serve laser path to reach destination




