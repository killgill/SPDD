from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from pprint import pprint
import os
import time
import math
import logging
import sys
import json

##import pygame, sys
##from pygame.locals import *
import RPi.GPIO as GPIO
from flowmeter import *
from adabot import *
##SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
#boardRevision = GPIO.RPI_REVISION
GPIO.setmode(GPIO.BCM) # use real GPIO numbering
GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(24,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26,GPIO.OUT)

# set up the flow meters
fm = FlowMeter('america', ["beer"])

# Beer, on Pin 23.
def doAClick(channel):
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    if fm.enabled == True:
        fm.update(currentTime)


GPIO.add_event_detect(23, GPIO.RISING, callback=doAClick, bouncetime=20) # Beer, on Pin 23

# main loop
try:
    while True:

        SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))
        SPREADSHEET_ID = '1hopTf_z_OzquBngV11XTryX9qX4AiYPi1hsOucpfVbk'
        ID_NUMBER_RANGE_NAME = 'number_of_ids!A1'
        VALUE_RENDER_OPTION = 'UNFORMATTED_VALUE'
        num_ids_response = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=ID_NUMBER_RANGE_NAME, valueRenderOption=VALUE_RENDER_OPTION).execute()
        num_ids = num_ids_response['values'][0][0]
        print(num_ids)
        print(type(num_ids))
        ID_NUMBERS_RANGE = 'ids!A2:C' + str(num_ids+1)
        VALUE_RENDER_OPTION = 'UNFORMATTED_VALUE'
        ids_list = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=ID_NUMBERS_RANGE, valueRenderOption=VALUE_RENDER_OPTION).execute()
        pprint(ids_list)

        '''
        if fm.enabled:
            print(fm.getFormattedThisPour())
            GPIO.output(26,1)
        '''
        '''
        time.sleep(2)
        GPIO.output(26,0)
        time.sleep(2)
        '''

        currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
        # reset flow meter after each pour (2 secs of inactivity)
        if (fm.thisPour <= 0.23 and currentTime - fm.lastClick > 2000):
            fm.thisPour = 0.0
#except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print("Other error or exception occurred!")
finally:  
    GPIO.cleanup() # this ensures a clean exit  
