import requests 
import configparser
import os
import csv

# Current path of file
cwd = os.path.dirname(os.path.abspath(__file__))

# Output folder for CSV statements
target = cwd + "/statements"

# Config data for Starling
config = configparser.ConfigParser()
config_file = f'{cwd}/config.conf'
config.read(config_file)
account_id = config['starling_config']['account_id']
bearer = config['starling_config']['bearer']

# Endpoints
list_periods_endpoint = f"https://api.starlingbank.com/api/v2/accounts/{account_id}/statement/available-periods"
download_endpoint = f'https://api.starlingbank.com/api/v2/accounts/{account_id}/statement/download'

# Download Header Information
headers_download = {"Authorization": f'Bearer {bearer}', 'accept' : 'text/csv'}
headers_list = {"Authorization": f'Bearer {bearer}'}

# Get periods available in account
r_periods = requests.get(list_periods_endpoint, headers=headers_list)
periods = r_periods.json()

# Download statements for each available period in account
for x in periods['periods']:
    year_month = x['period']

    r_download = requests.get(download_endpoint, headers=headers_download, params={'yearMonth' : year_month})
    download = r_download.content.decode("utf-8")
    cr = csv.reader(download.splitlines(), delimiter = ',')
    my_list = list(cr)
    with open(f'{target}/{year_month}.csv', "w", newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(my_list)
