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

TO-DO:
Google Sheets API integration
Swipe authentication state machine implementation
Build the actual keg
Precise measurement testing (aka drinking)