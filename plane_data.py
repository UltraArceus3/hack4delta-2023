import gzip
import shutil
import requests
from datetime import datetime, timedelta


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# Get all files from this date
start_date = datetime(2023, 9, 15)
end_date = datetime(2023, 9, 15)
for date in daterange(start_date, end_date):
    date_str = date.strftime("%Y/%m/%d")
    url = f"https://samples.adsbexchange.com/hires-traces/{date_str}/index.json"
    
    resp = requests.get(url).json()

    for trace in resp['traces']:
                



    # Iterate through all scraped matches in the index file and unzip the files

    with gzip.open(f'file.txt.gz', 'rb') as f_in:
        with open('file.txt', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    

