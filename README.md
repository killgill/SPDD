# SPDD
Kegerator Code

This Kergerator is a automatic dispensing system meant to dispense 12 oz of 
beer with the swipe of a magnetic card. A swipe of the card reader will 
activate the solenoid on pin 26 setting it high to by flipping a MOSFET
controlled switch. Once the flow sensor has measured 12 oz the solenoid control
signal will be set to 0 stopping the flow of beer.

Magnetic swipe authentication will be handled by the Google Sheets API. We are
using Google Sheets because to make it easier to add and remove registered 
members who have access to the keg. The Raspberry PI will read the card swipe
compare it to a users student identification number and then increment their 
count of beers. Members beer usage (beers in a certain period of time) will 
also be tracked.

### SSH Static IP
192.168.2.169 on spdfast_2.4 and spdfast_5.0

### How to Run Effectively
When sshing, attempt to run the command 'tmux attach'. If there are no windows to attach to, run 'tmux'. Inside the tmux shell, navigate to ''~/Documents/SPDD' and run 'sudo python spdd.py'. You can then detach from the tmux session and the system will persist.

TO-DO:
Google Sheets API integration (DONE)
Swipe authentication state machine implementation (DONE)
Error handling for non-database swipes (DONE)
Google sheets code into seperate file (DONE)
Create a #beers today column and have conditionals for that
Separate google sheet into non-personal drive (Happy Smiles?)
Build the actual keg
Precise measurement testing (aka drinking)
SSH into Raspberry pi
Audio warning system, figure how to play audio files
Cron job to start on reboot

Work Notes:

