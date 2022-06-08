import requests 
import configparser
import os
import csv

# Current path of file
cwd = os.path.dirname(os.path.abspath(__file__))

# Output folder for CSV statements
target = cwd + "/statements"
target_pdf = target + "/PDF"
target_csv = target + "/CSV"

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
headers_download_csv = {"Authorization": f'Bearer {bearer}', 'accept' : 'text/csv'}
headers_download_pdf= {"Authorization": f'Bearer {bearer}', 'accept' : 'application/pdf'}
headers_list = {"Authorization": f'Bearer {bearer}'}

# Get periods available in account
r_periods = requests.get(list_periods_endpoint, headers=headers_list)
periods = r_periods.json()

# Download statements for each available period in account
for x in periods['periods']:
    year_month = x['period']

    # Extract statements as CSV
    r_download_csv = requests.get(download_endpoint, headers=headers_download_csv, params={'yearMonth' : year_month})
    download = r_download_csv.content.decode("utf-8")
    cr = csv.reader(download.splitlines(), delimiter = ',')
    my_list = list(cr)
    with open(f'{target_csv}/{year_month}.csv', "w", newline = "") as f:
        writer = csv.writer(f)
        writer.writerows(my_list)

    # Extract statement as PDF
    r_download_pdf = requests.get(download_endpoint, headers=headers_download_pdf, params={'yearMonth' : year_month}, stream = True)
    with open (f'{target_pdf}/{year_month}.pdf', "wb") as f:
        f.write(r_download_pdf.content)