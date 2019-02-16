from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime
import pickle


# Checks ID from pre-polled list
def check_ID(card_id):
    with open('ids.txt', 'rb') as filehandle:
        ids_list = pickle.load(filehandle)

    card_id = str(card_id)  # placeholder

    if card_id in ids_list:
        return True
    else:
        return False

# Upon pour, updates google sheet with pour information


def gs_pour(card_id, pour_amount):

    # the following block sets up the spreadsheet API and connects to spreadsheet
    time_now = datetime.now().strftime('%m-%d %H:%M')
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    store = file.Storage('token.json')
    creds = store.get()
    # if no creds, generates them
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    # builds spreadsheet service
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    SPREADSHEET_ID = '1hopTf_z_OzquBngV11XTryX9qX4AiYPi1hsOucpfVbk'
    TOTAL_BEERS_RANGE = 'keg_contents!A2:C'
    keg_update = {
        'majorDimension': 'COLUMNS',
        'values': [
            [card_id],
            [pour_amount],
            [time_now]
        ]
    }
    # put the data into the sheet
    new_beers_resp = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=TOTAL_BEERS_RANGE,
                                                            body=keg_update, valueInputOption='RAW', insertDataOption='OVERWRITE').execute()
    return
