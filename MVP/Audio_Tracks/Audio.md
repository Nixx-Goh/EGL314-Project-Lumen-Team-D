<h1>
Configurations for reaper with osc
</h1>

<h3>
1. Connecting with the osc using vscode to reaper
</h3>

```
def send_osc(address):
    try:
        IP = "192.168.254.12"
        PORT = 8000
        client = udp_client.SimpleUDPClient(IP, PORT)
        client.send_message(address, float(1))
        print(f"OSC sent: {address}")
    except Exception as e:
        print(f"Failed to send OSC {address}: {e}")
```

<br>
<br>

<h3>
2. Start Button for Asteroid 1
</h3>

```
def on_start(self):
        send_osc("/action/40162")
        send_gma3_command("Off Sequence 4")
        send_gma3_command("Off Sequence 12")
        send_gma3_command("Go+ Sequence 7")
        send_gma3_command("Go+ Sequence 9")
        GPIO.output(LASERS[1], GPIO.LOW)
```
* I used marker 2(40162) as the start button in the midi pad
* When Pressed it will go to this marker number2 which has a light saber sound effect
* This will come on when pressed Asteroid button 1
<br>
<br>

<h3>
3. Win condition for Asteroid 1
</h3>

```
def on_win(self):
        send_osc("/action/40168")
        send_gma3_command("Off Sequence 9")
        send_gma3_command("Go+ Sequence 3")
        send_gma3_command("Go+ Sequence 12")
        send_gma3_command("Go+ Sequence 5")
        send_gma3_command("Go+ Sequence 8")
```
*  I used marker 8(40168) which will come off to the sound effect of "You have clear Stage 1"
<br>
<br>

<h3>
4. Losing
</h3>

```
def on_lose(self):
        send_osc("/action/40164")
        send_gma3_command("Off Sequence 9")
        send_gma3_command("Go+ Sequence 2")
        send_gma3_command("Go+ Sequence 13")
```
*  I used marker 4(40164) which will come off when player does not hit the sensor within the time limit 
<br>
<br>

<h3>
5. Start Button for Asteroid 2
</h3>

```
def on_start(self):
        send_osc("/action/40169")
        send_gma3_command("Off Sequence 4")
        send_gma3_command("Off Sequence 12")
        send_gma3_command("Go+ Sequence 7")
        send_gma3_command("Go+ Sequence 9")
        GPIO.output(LASERS[1], GPIO.LOW)

```
* I used marker 9(40169) as the start button in the midi pad
* When Pressed it will go to this marker number9 which has a light saber sound effect
* This will come on when pressed Asteroid button 2
<br>
<br>

<h3>
6. Win condition for Asteroid 2
</h3>

```
def on_win(self):
        send_osc("/action/40165")
        send_gma3_command("Off Sequence 9")
        send_gma3_command("Go+ Sequence 3")
        send_gma3_command("Go+ Sequence 12")
        send_gma3_command("Go+ Sequence 5")
        send_gma3_command("Go+ Sequence 8")
```
*  I used marker 5(40165) which will come off with a explosion sound effect and commence "You have destroyed the Asteroid"
<br>
<br>


<h1>
Input for the MIDI PAD
</h1>


```
with mido.open_input(input_name) as port:
        for msg in port:
            if msg.type == 'note_on' and msg.velocity > 0:
                note = msg.note
                if note in PAD_TO_STAGE:
                    stage_class = PAD_TO_STAGE[note]
                    app.root.after(0, app.show_stage, stage_class)
                elif note == START_BUTTON_PAD:
                    app.root.after(0, app.start_timer)
                elif note == RESTART_BUTTON_PAD:
                    app.root.after(0, app.reset_display)
                    send_osc("/action/40167")
                elif note == START_PAD:
                    send_osc("/action/40161")
                    send_osc("/action/1007")
                elif note == STOP_PAD:
                    send_osc("/action/1016")
```
*  I used marker 7(40167) for the restart button
*  Marker 1(40161) for the first marker which is the start of my sequence where the biginning audio will start "Welcome to Sector 536"
* I used "1007" to start the Audio and 1016 to stop the Audio
<br>
<br>
<br>
<br>
<br>

<h1> Connecting the OSC</h1>

<h3>1. Control Surface Settings </h3>
<img src="./Audio_image/Control.png">

* This is the page where we do the configuration to connect the osc
* How do we get here
* Below will show you step by step

<br>
<br>
<br>


<h3> 2.Find Preference </h3>
<img src="./Audio_image/Preference.png">

* You will have to look for the option button circled in yellow then head down to the bottom where you can see the blue circle and click on it

<br>
<br>
<br>


<h3> 3.In the Preference tab </h3>
<img src="./Audio_image/OSC.png">

* Search for Control/OSC/web which is the yellow one that i have circled and afterwards press the one circled in blue which is the add button

* Afterwhich you will be in the Control surface settings to set the OSC