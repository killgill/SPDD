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

#commented out not using Raspberry PI
#import RPi.GPIO as GPIO
from flowmeter import *

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
authFlag = False    #If card swipe is authorized set to true

# Beer, on Pin 23
#GPIO.add_event_detect(23, GPIO.RISING, callback=doAClick, bouncetime=20) 

# main loop
try:
    while True:

        def onSwipe(card_id):
            SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
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
            ID_NUMBERS_RANGE = 'ids!A2:A' + str(num_ids+1)
            VALUE_RENDER_OPTION = 'UNFORMATTED_VALUE'
            ids_list_response = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=ID_NUMBERS_RANGE, majorDimension='COLUMNS').execute()
            ids_list = ids_list_response['values'][0]
            card_id = str(card_id) # placeholder
            if card_id in ids_list:
                id_index = ids_list.index(card_id)
            BEERS_FOR_CARD = 'ids!C' + str(id_index+2)
            cur_beers_response = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=BEERS_FOR_CARD, valueRenderOption=VALUE_RENDER_OPTION).execute()
            cur_beers = cur_beers_response['values'][0][0]
            new_beers = {'values': [[cur_beers + 1]]}
            new_beers_resp = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=BEERS_FOR_CARD, body=new_beers, valueInputOption='RAW').execute()
            return True

        swipe = raw_input("ID#")
        if isinstance(swipe, basestring):
            card_id = swipe[1:11]
            print(card_id)
            authFlag = onSwipe(card_id)

        # Logic control for magnetic swipes
        while authFlag:
            print(fm.currPour)
            # Allow beer to flow
            # GPIO.output(26,1)

            # fake pour
            fm.currPour = fm.currPour + 1
            if fm.currPour > 12: # wait for 12 oz of beer
                # GPIO.output(26,0) # stop flow
                # ADD MORE SHIT HERE
                fm.clearCurrPour() # clear
                authFlag = False #reset flag

except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print("Exception occured")
finally:
    pass
    # GPIO.cleanup() # this ensures a clean exit
