from __future__ import print_function

import eel
import os
from pathlib import Path

# Reading Environmental variables
from dotenv import load_dotenv
load_dotenv()

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

if os.name == 'nt':
    PATH = Path(f'{os.path.dirname(os.path.realpath(__file__))}\App').as_posix()
else:
    PATH = 'App'

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The spreadsheet ID
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

def connecting_to_api():

    global creds
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

@eel.expose
def AccessGoogleSheet():

    global name
    RANGE = f'{name}!A1:H20'

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        # Checking which range is empty
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
        rows = result.get('values', [])
        print(rows)


    except HttpError as err:
        if err.resp.status in [400, 404]:
            print("\nERRO: Por favor confira se o nome da página foi escrita corretamente\n")
        else:
            print(err)

# Declaring global time variables
hour = min = sec = 0

@eel.expose
def stop():
    global stopwatch
    stopwatch = False

@eel.expose
def StopWatch():

    global stopwatch
    stopwatch = True

    global hour, min, sec

    while stopwatch == True:
        time_elapsed = f"{hour:02d}:{min:02d}:{sec:02d}"
        eel.showTime(time_elapsed)
        eel.sleep(1)
        if(59 > sec >= 0):
            sec = sec + 1
        elif(59 > min >= 0):
            sec = 0
            min = min + 1
        else:
            sec = 0
            min = 0
            hour = hour + 1

@eel.expose
def get_form_input(input):
    global name, description
    name = input[0]
    description = input[1]

if __name__ == "__main__":

    connecting_to_api()

    eel.init(PATH)
    eel.start("index.html", size=(500,350),port=8080)