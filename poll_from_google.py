from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pickle
from audio_system import *


class PollGoogle():
    def __init__(self):
        self.SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        self.store = file.Storage('token.json')
        self.creds = self.store.get()
        if not self.creds or self.creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            self.creds = tools.run_flow(flow, store)
        self.service = build('sheets', 'v4', http=self.creds.authorize(Http()))
        self.SPREADSHEET_ID = '1hopTf_z_OzquBngV11XTryX9qX4AiYPi1hsOucpfVbk'
        self.VALUE_RENDER_OPTION = 'UNFORMATTED_VALUE'
        self.audio = AudioSystem()


    def poll(self):
        self.audio.playAudio('polling0')
        self.getIds()
        return


    def getIds(self):
        ID_NUMBERS_RANGE = 'ids!A2:A'
        ids_list_response = self.service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID, range=ID_NUMBERS_RANGE,
                                    majorDimension='COLUMNS').execute()
        ids_list = ids_list_response['values'][0]
        with open('ids.txt', 'wb') as filehandle:  
            pickle.dump(ids_list, filehandle)
        return

pg = PollGoogle()
pg.poll()
