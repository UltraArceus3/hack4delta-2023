import requests
from datetime import datetime, timedelta
import pandas as pd
import os

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# get all files from specified date
def get_data(start_date, end_date):
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
            df.to_csv(f"../data/plane_data/{trace_name}-{file_date}.csv")

# start_date = datetime(2023, 9, 1)
# end_date = datetime(2023, 9, 2)
# create_csvs(start_date, end_date)

def create_dataset(start_date, file_name = "../data/cali-dataset", bounding_box = {"lat": (22, 49), "long": (-129, -64)}, size_limit=-1):
    l = []
    i = 0
    d = {"flight_id": [], "latitude": [], "longitude": [], "departure": [], "arrival": []}
    for file in os.listdir("../data/plane_data"):

        if file.endswith(".csv"):
            
            df = pd.read_csv(f"../data/plane_data/{file}", converters={'trace': eval})
            
            id = df['icao'].iloc[0]
            if len(set(df['icao'])) != 1:
                print("Multiple IDs")
            lat = df['trace'].apply(lambda x: x[1])
            lat_inrange = lat.apply(lambda x: x > bounding_box['lat'][0] and x < bounding_box['lat'][1])
            lon = df['trace'].apply(lambda x: x[2])
            lon_inrange = lon.apply(lambda x: x > bounding_box['long'][0] and x < bounding_box['long'][1])
            
            if sum(lat_inrange) == 0 or sum(lon_inrange) == 0:
                continue
            i += 1
            
            depart = start_date + timedelta(seconds=df.iloc[0]['trace'][0])
            arrival = start_date + timedelta(seconds=df.iloc[-1]['trace'][0])

            d['flight_id'].append(id)
            d['latitude'].append(list(lat))
            d['longitude'].append(list(lon))
            d['departure'].append(depart)
            d['arrival'].append(arrival)
            l.append(d)

            print(f"{i}", end="\r")

        if size_limit > 0 and i >= size_limit:
            break


    df = pd.DataFrame(d)
    df.to_csv(f"{file_name}.tsv", sep = "\t")
            
start_date = datetime(2023, 9, 1, 0, 0, 0)

# Cali Boundaries
bounding_box = {"lat": (32, 42), "long": (-124, -114)}

create_dataset(start_date, file_name="../data/cali-dataset", size_limit=100, bounding_box=bounding_box)