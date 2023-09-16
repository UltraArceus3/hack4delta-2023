import plotly as px
import pandas as pd
import plotly.graph_objects as go
import os


fig = go.Figure(go.Scattermapbox())
i = 0



for file in os.listdir("./data/plane_data"):
    
    if file.endswith(".csv"):
        df = pd.read_csv(f"./data/plane_data/{file}", converters={'trace': eval})
        #print(df['trace'])
        #print(list(df['trace']))
        #df.update()
        fig.add_trace(go.Scattermapbox(
            lon = df['trace'].apply(lambda x: x[2]), #if x[2] > -129 and x[2] < -64 else None
            lat = df['trace'].apply(lambda x: x[1]), #if x[1] > 22 and x[1] < 49 else None
            mode = 'markers+lines',
            line = {'width': 1},
            name = file
        ))
        
    i += 1

    print(f"{i}", end = "\r")

    if i > 1000:
        break




# df = pd.read_json("data/trace_full_000000.json")
# lat = df['trace'].apply(lambda x: x[1] if x[1] > 22 and x[1] < 49 else None)
# lon = df['trace'].apply(lambda x: x[2] if x[2] > -129 and x[2] < -64 else None)

#print(lat)

# fig = go.Figure(go.Scatter(x=lat, y=lon, fill="toself"))
# fig.show()
    
""" fig = go.Figure(go.Scattermapbox(
    mode = "markers+lines",
    lon = lon,
    lat = lat,
    marker = {'size': 10}),
    line = {'width': 45})
 """

fig.update_layout(
mapbox = {
    'style': "stamen-terrain",
    'zoom': 1})
# fig.update_layout(
#     geo = {'scope': 'north america'},)

fig.show()