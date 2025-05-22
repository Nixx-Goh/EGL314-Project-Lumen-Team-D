# 🔍 Project Introduction
Our project is a **smart mirror maze** that uses **Raspberry Pi** and other elements such as **Laser, Light Sensors, PCA9685 Servo Driver, Servo Motors and MDP218 MIDI Pad** to create a fun and interactive experience. The goal is to make a mirror maze where players have to navigate through the maze by using a laser that will create a laser path and use the MIDI PAD to rotate the servo motor that has a mirror attached  to get the angle for the laser path to bounce off each mirrors from one end of the maze to the center of the maze where the light sensor will be placed. Within the given time limit, players should complete the maze and allow the light sensor at the center to detect the mirror path for 3s to be considered a success.

However, there is a twist! There are light sensors placed along the path as well, where the "walls" are and it should not detect any light for more than 2s, otherwise it is considered a fail. 

There will be a total of 4 stages, with the 1st stage being the easiest and 4th to be the most challenging.

Stage 1 (30s) : Laser placed at the bottom left of the maze and with the use of only 3 mirrors

Stage 2 (45s): Laser placed at the bottom right of the maze 


# 🛠️ What are we using and why

 The **Raspberry Pi** acts as the master, which then connects and controls the other elements:

 * **Laser:** To create a laser path for players to navigate through the maze

 * **Light Sensors:** To detect 


