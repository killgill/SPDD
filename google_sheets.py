from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def check_ID(card_id):
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    SPREADSHEET_ID = '1hopTf_z_OzquBngV11XTryX9qX4AiYPi1hsOucpfVbk'
    ID_NUMBERS_RANGE = 'ids!A2:A'
    VALUE_RENDER_OPTION = 'UNFORMATTED_VALUE'

    ids_list_response = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=ID_NUMBERS_RANGE,
                                                            majorDimension='COLUMNS').execute()
    ids_list = ids_list_response['values'][0]
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
    BEERS_FOR_CARD = 'ids!C' + str(id_index + 2)
    VALUE_RENDER_OPTION = 'UNFORMATTED_VALUE'
    cur_beers_response = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=BEERS_FOR_CARD,
                                                        valueRenderOption=VALUE_RENDER_OPTION).execute()

    cur_beers = cur_beers_response['values'][0][0]
    new_beers = {'values': [[cur_beers + 1]]}
    new_beers_resp = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=BEERS_FOR_CARD,
                                                        body=new_beers, valueInputOption='RAW').execute()
    TOTAL_BEERS_RANGE = 'keg_contents!A2:B'
    keg_update = {'majorDimension':'COLUMNS', 'values': [[card_id],[pour_amount]]}
    new_beers_resp = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=TOTAL_BEERS_RANGE,
                                                        body=keg_update, valueInputOption='RAW', insertDataOption='INSERT_ROWS').execute()
    return
