import requests 
import configparser
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

"""
Application extracts total balance from Starling Bank account, and copies it to
Google Sheets cell. 

Pre-requisites:

1. Create Google Sheet
2. Go to Google Developer Console
3. Create & Select Project
4. Go to APIs and Services and activate Google Sheets API
5. Go to Create Credentials and create Service Account
6. Click Edit button next to new Service Account
7. Go to KEYS, ADD KEY, CREATE NEW KEY and download as JSON
8. Store JSON in this directory 
9. Find client_email in JSON and copy it
10. Go to your Google Sheet and share with this email
11. Create Starling Developer account and create personal access token (bearer)
12. Create file called config.conf in this directory
12. Copy the below, replacing with your starling credentials

[starling_config]
account_id = enter account id here
bearer = enter bearer token here

"""
# Current path of file
cwd = os.path.dirname(os.path.abspath(__file__))

# Config data for Starling
config = configparser.ConfigParser()
config.read(f'{cwd}/config.conf')
account_id = config['starling_config']['account_id']
bearer = config['starling_config']['bearer']

# Config data from Google
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials_google = ServiceAccountCredentials.from_json_keyfile_name(f"{cwd}/google_auth.json", scope)
file = gspread.authorize(credentials_google) 

# Starling API String
balance_endpoint = f'https://api.starlingbank.com/api/v2/accounts/{account_id}/balance'

# Request Data from Starling
headers = {"Authorization": f'Bearer {bearer}'}
r = requests.get(balance_endpoint, headers=headers)

# Store Data as JSON
r_json = r.json()

# Extract the total effective balance
total = r_json['totalEffectiveBalance']['minorUnits']
total = total / 100

# Update Google sheet
sheet = file.open("Finance").sheet1
sheet.update_acell('C3', total)

from datetime import datetime

today = str(datetime.now())
sheet.update_acell('B16', today)

