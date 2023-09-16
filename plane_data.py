import requests
from datetime import datetime, timedelta
import pandas as pd

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# Get all files from this date
start_date = datetime(2023, 9, 1)
end_date = datetime(2023, 9, 2)
for date in daterange(start_date, end_date):
    date_str = date.strftime("%Y/%m/%d")
    print(f"Date {date_str}" + 20 * "-")
    base_url = f"https://samples.adsbexchange.com/traces/{date_str}"
    index_resp = requests.get(base_url + "/index.json").json()

    for i, trace_name in enumerate(index_resp['traces']):
        print(f"Trace #{i + 1}: {trace_name} completed")
        lsb_first_two_chars = trace_name[-2:]
        trace_resp = requests.get(base_url + f"/{lsb_first_two_chars}/trace_full_{trace_name}.json")

        df = pd.DataFrame(trace_resp.json())
        
        file_date = date.strftime("%Y-%m-%d")
        df.to_csv(f"data/plane_data/{trace_name}-{file_date}.csv")



    
        
