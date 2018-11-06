from __future__ import print_function
from pprint import pprint
import os
import time
import math
import logging
import sys
import json
import random
import serial, string

import RPi.GPIO as GPIO
from flowmeter import *
from google_local import *
from audio_system import *
from barcodeReader import *

def GPIO_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(26,GPIO.OUT)
GPIO_init()

swipe = None

# set up the flow meters
fm = FlowMeter('america', ["beer"])
audio = AudioSystem()
br = BarcodeReader()

swipe = None 

# Beer, on Pin 23.
def doAClick(channel):
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    if fm.enabled == True:
        fm.update(currentTime)


# logic flags for magnetic swipes
authFlag = False    # If card swipe is authorized set to true
pourFlag = False    # Flag to allow pour

# Beer, on Pin 23
GPIO.add_event_detect(23, GPIO.RISING, callback=doAClick, bouncetime=20) 

# main loop
try:
    while True:
        print('waiting for swipe')
        swipe = br.readStripe()
        if isinstance(swipe, basestring):
            print(swipe)
            card_id = swipe[15:25]
            print(card_id)
            audio.playAudio(audio.swipeDetected)
            if (card_id == '1174425248' or card_id == '3453909285'):
                audio.playAudio(audio.master[random.randint(0,1)])
            authFlag, id_index = check_ID(card_id)

        currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
        # Logic control for magnetic swipes

        # If card is authorized (Positive)
        if authFlag:
            # Set the pour flag
            pourFlag = True
            audio.playAudio(audio.readyToPour)
            startTime = time.time()
            print('ready to pour')

            # Allow beer to flow
            GPIO.output(26,1)

            # wait for pour to finish
            while pourFlag:
                
                while fm.currPour < 4 and time.time() - startTime < 45:
                	pass

                # Turn everything off
                pourFlag = False    # no more beer
	            GPIO.output(26,0) # stop flow
	            gs_pour(card_id, id_index, fm.currPour)
	            fm.clearCurrPour()  # clear
                authFlag = False    # reset authorization
                swipe = None        # clear the swipe

                if fm.currPour >= 4:
	                audio.playAudio(audio.enjoy[random.randint(0,1)])
	                print("Enjoy your cold beer, brother")
	                
                elif (time.time() - startTime > 45):
                    audio.playAudio(audio.timeOut)
                    print("Timeout")
                    gs_pour(card_id, id_index, fm.currPour)


        # Card isn't authorized after a swipe (Negative)
        elif ~authFlag and isinstance(swipe, basestring):
            audio.playAudio(audio.whatIsObject[random.randint(0,1)])
            print("Invalid ID#. What is object?")
            swipe = None #clear the swipe

finally:
    GPIO.cleanup() # this ensures a clean exit
