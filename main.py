from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from models import Cell
from StopWatch import StartTime, StopWatch

# Reading Environmental variables
from os import getenv
from dotenv import load_dotenv
load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The spreadsheet ID
SPREADSHEET_ID = getenv('SPREADSHEET_ID')


def main():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

        # Reruns main with new Token
        main()

    try:

        # Taking user input
        sheet_name = input("Qual o nome da sua página no Orc'ronologia? (É o nome que aparece na barra em baixo):")
        description = input("Descrição: ")

        # Sets the range
        RANGE = f'{sheet_name}!A1:H50'

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        # Checking which range is empty
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
        rows = result.get('values', [])
        for i in range(50):
            if rows[i][0] == '':
                row = i + 1
                break

        # Starts the StopWatch and saves the time
        start = StartTime()
        date = f'{start.month}/{start.day}'
        start_time = f'{start.hour:02d}:{start.minute:02d}'
        end = StopWatch()
        end_time = f'{end.hour:02d}:{end.minute:02d}'

        # Formatting all the information
        row_data = [
            date, 
            f'=CONCATENATE("Semana ", IFERROR(ROUNDDOWN(DATEDIF(Geral!C$5, A{row}, "D") / 7 + 1), 0))', 
            start_time, 
            end_time, 
            '12:00:00 AM', 
            description
        ]

        # Writes on Google Sheets
        cell = Cell(row_data)
        result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=f'{sheet_name}!A{row}',
        valueInputOption="USER_ENTERED", body=cell.body).execute()

    except HttpError as err:
        if err.resp.status in [400, 404]:
            print("\nERRO: Por favor confira se o nome da página foi escrita corretamente\n")
            main()
        else:
            print(err)


if __name__ == '__main__':
    main()