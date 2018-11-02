from __future__ import print_function
from pprint import pprint
import os
import time
import math
import logging
import sys
import json

#commented out not using Raspberry PI
#import RPi.GPIO as GPIO
from flowmeter import *
from google_sheets import *

'''
def GPIO_init()
    GPIO.setmode(GPIO.BCM) # use real GPIO numbering
    GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(26,GPIO.OUT)
'''

swipe = None

# set up the flow meters
fm = FlowMeter('america', ["beer"])

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
#GPIO.add_event_detect(23, GPIO.RISING, callback=doAClick, bouncetime=20) 

# main loop
try:
    while True:
        swipe = raw_input("ID#")
        if isinstance(swipe, basestring):
            card_id = swipe[1:11]
            print(card_id)
            authFlag, id_index = onSwipe(card_id)

        currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
        # Logic control for magnetic swipes

        # If card is authorized (Positive)
        if authFlag:
            # Set the pour flag
            pourFlag = True

            # Allow beer to flow
            # GPIO.output(26,1)

            # wait for pour to finish
            while pourFlag:
                print(fm.currPour)
                # fake pour
                fm.currPour = fm.currPour + 1

                # Set a timer if pour inactive for 10 seconds (False Positive)
                if (fm.currPour > 0.23 and currentTime - fm.lastClick > 10000):
                    print("Timeout")
                    pourFlag = False    # no more beer
                    fm.clearCurrPour()  # clear
                    authFlag = False    # reset authorization
                    swipe = None        # clear the swipe

                # Count ounces poured
                if fm.currPour > 11.5 or (currentTime - fm.lastClick > 20000): # wait for 12 oz of beer
                    pourFlag = False    # no more beer
                    # GPIO.output(26,0) # stop flow
                    # ADD MORE SHIT HERE
                    print("Enjoy your cold beer, brother")
                    gs_pour(card_id, id_index, fm.currPour)
                    fm.clearCurrPour()  # clear
                    authFlag = False    # reset authorization
                    swipe = None        # clear the swipe


        # Card isn't authorized after a swipe (Negative)
        elif authFlag and isinstance(swipe, basestring):
            print("Invalid ID#. What is object?")
            swipe = None #clear the swipe

except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print("Exception occured")
finally:
    pass
    # GPIO.cleanup() # this ensures a clean exit
