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

swipe = None

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
        print(num_ids)
        print(type(num_ids))
        ID_NUMBERS_RANGE = 'ids!A2:A' + str(num_ids+1)
        VALUE_RENDER_OPTION = 'UNFORMATTED_VALUE'
        ids_list_response = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=ID_NUMBERS_RANGE, majorDimension='COLUMNS').execute()
        pprint(ids_list_response)
        ids_list = ids_list_response['values'][0]
        print(ids_list)
        print(type(ids_list))
        print(type(ids_list[0]))
        card_id = u'3453909285' # placeholder
        print(type(card_id))
        print('guap1')
        if card_id in ids_list:
            id_index = ids_list.index(card_id)
        print(ids_list[0] == card_id)
        print(ids_list[0])
        print(card_id)
        print('guap2')
        BEERS_FOR_CARD = 'ids!C' + str(id_index+2)
        print('guap3')
        cur_beers_response = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=BEERS_FOR_CARD, valueRenderOption=VALUE_RENDER_OPTION).execute()
        print('guap4')
        cur_beers = cur_beers_response['values'][0][0]
        print('guap5')
        new_beers = {'values': [[cur_beers + 1]]}
        print('guap6')
        new_beers_resp = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=BEERS_FOR_CARD, body=new_beers, valueInputOption='RAW').execute()
        print('guap7')
        pprint(new_beers_resp)
        print('guap8')

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
