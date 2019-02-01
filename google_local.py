from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pickle


def check_ID(card_id):
    with open('ids.txt', 'rb') as filehandle:  
        ids_list = pickle.load(filehandle)

    card_id = str(card_id)  # placeholder

    if card_id in ids_list:
        id_index = ids_list.index(card_id)
        return (True, id_index)
    else:
        return (False, -1)

def gs_pour(card_id, id_index, pour_amount):

    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    SPREADSHEET_ID = '1hopTf_z_OzquBngV11XTryX9qX4AiYPi1hsOucpfVbk'

    TOTAL_BEERS_RANGE = 'keg_contents!A2:B'
    keg_update = {'majorDimension':'COLUMNS', 'values': [[card_id],[pour_amount]]}
    new_beers_resp = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=TOTAL_BEERS_RANGE,
                                                        body=keg_update, valueInputOption='RAW', insertDataOption='OVERWRITE').execute()
    return
