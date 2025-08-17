# Game Lighting Sequences

# By Jun Ting

### System Overview

All lighting sequences except for Sequence 1 are controlled from the **`Main.py`** interface.
The GUI communicates with the **Master Server Raspberry Pi** over the local network using **OSC (Open Sound Control)** messages sent to the GrandMA3 command endpoint.

* Network target for lighting: `GMA_IP = "192.168.254.213"`, `GMA_PORT = 2000`.
* OSC client used in code: `udp_client.SimpleUDPClient(GMA_IP, GMA_PORT)`.
* Lighting commands are sent via `trigger_gma(command)`, which transmits to the GrandMA3 command address: `/gma3/cmd`.
This lets operators fire cues from the GUI without touching the desk: pressing a button sends an OSC command to the Master Pi, which relays it to **GrandMA3**.

### Design Concept

The lighting design adopts a **Galaxy-inspired palette** of **Blue, Pink, and Purple**.

The intention is to create a clean, immersive atmosphere while guiding attention to key stage elements.


## Introduction
- **Sequence 1**: Starry night background lights that consists of Blue & Purple for the introduction.
- **Sequence 2**: Path lights & Red Gobo to lead guests into the Laser Defence Protocol station. 
- **Sequence 3**: Burning Asteriod slowly falling down & explode.
- **Sequence 4**: Alarm lights to make the Asteriod falling down more dramatic & create a Red/Orange starry background after the Asteriod explodes.
- **Sequence 22**: To shine bright white lights onto the station, so that the presenter can be visible. 

## Game Start
- **Sequence 5**: A quick flash of light blue lights to match the Light Saber audio cue.
- **Sequence 6**: Create a big burning Asteriod on the wall.
- **Sequence 7 & 18**: A mix of Pink, Magenta & Purple lights to slightly brighten up the surrounding.
- **Sequence 8 & 19**: 10 ticks of red lights that will light up the wall & ceiling in a clockwise manner to match the 10Sec CountDown audio cue.

## Game Over
- **Sequence 9**: Shine bright red lights in a rhythmic manner to signify Game Over.
  
## Game Win
- **Sequence 10 & 20**: Asteriod on the wall explodes.

## To Team C Transition:
- **Sequence 11**: Emergency like flashing red lights to match the Alarm audio cue.
- **Sequence 21**: Gobo transition to lead the guests to Kinetic Core Recharge.



