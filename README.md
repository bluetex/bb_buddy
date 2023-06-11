# bb_buddy
BeatBuddy Buddy Application to push collection info to device.


Features: 
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

Other options
1. bluetex option: syncs the tempo of the current song to the FX rack of my Midas MR18 digital delay
2. can be accessed (with minimal config) from any device on the same network as the one running the app
 * the computer running the app must be the one physically connected to the BB
 * must be running python3
