from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


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
    num_ids_response = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=ID_NUMBER_RANGE_NAME,
                                                           valueRenderOption=VALUE_RENDER_OPTION).execute()
    num_ids = num_ids_response['values'][0][0]
    ID_NUMBERS_RANGE = 'ids!A2:A' + str(num_ids + 1)
    VALUE_RENDER_OPTION = 'UNFORMATTED_VALUE'
    ids_list_response = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=ID_NUMBERS_RANGE,
                                                            majorDimension='COLUMNS').execute()
    ids_list = ids_list_response['values'][0]
    card_id = str(card_id)  # placeholder
    if card_id in ids_list:
        id_index = ids_list.index(card_id)
        BEERS_FOR_CARD = 'ids!C' + str(id_index + 2)
        cur_beers_response = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=BEERS_FOR_CARD,
                                                             valueRenderOption=VALUE_RENDER_OPTION).execute()
        cur_beers = cur_beers_response['values'][0][0]
        new_beers = {'values': [[cur_beers + 1]]}
        new_beers_resp = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=BEERS_FOR_CARD,
                                                            body=new_beers, valueInputOption='RAW').execute()
        return True
    else:
        return False