# bb_buddy
#### BeatBuddy Buddy Application to push collection info to device.

## Requirements: 
1. BeatBuddy with Midi Cable
2. Audio/Midi interface
3. Python3 (recommended 3.1.12 from the Python.org site)

## Install:
1. Download the zip file under tags/releases
2. Unzip it to your computer
3. cd into your unzipped directory to find the requirements.txt
4. run pip install -r requirements.txt
5. run python ./start.py

this will open a webpage for configuration

## Configuration:
1. on the config page (http://localhost:8000/) you'll be prompted for 3 values. 
  - Midi Interface Input 
  - Midi Interface Output
  - Home Directory of your beatbuddy collection (the folder on your computer will contain Songs, Drumsets etc, if you don't have one of these you'll use BB Manager to save your project locally on your compuer)
2. click the submit and you'll be redirected to http://localhost:5000
  - NOTE: if you don't allow access to ports on your computer, you may need to open both of these ports. It is possible to access the webpage via your computer's IP if you allow access from off your computer to a local webserver. 

## Features: 
1. quick access view list (clickable) of all folders on your current sync to the beatbuddy sd card.  (works off the local pc side of that)
2. search access to the local collection, and if not found searches the online "song match" website
3. songs sent to beatbuddy will always display the genre/song pushed and the tempo (or current approximation)
4. tempo controls are uparrow/downarrow for increase decrease, or type a numeric value 40-300 and enter will send new tempos to the BB
5. play controls:  play, stop, pause, fill, half time, double time, next section, previous section.
6. setlist management: click / search to select a song, "Add to Setlist" will not push the song, but add it to your setlist. 
 * Once a song is selected and pushed from setlist, it will drop off the list.
 * User can remove item from setlist by selecting then clicking remove button
 * Set lists can be exported to a file to save for later.
 * Set lists can be imported from a file
7. drumset select: allows you to push a new drumset to the BB after a song is pushed.
8. Send to BeatBuddy - sends the song from the header display to the BB. 
 * if the song was songmatched from the external site, the tempo is also sent to BB
9. Valid config setup - if the app polls the interface and path listed and finds an invalid config, you'll be pushed to the setup page
 * if a valid config is detected, we move immediately to the control page.
