import plotly as px
import pandas as pd
import plotly.graph_objects as go
import os


fig = go.Figure(go.Densitymapbox())




def flightmap():
    fig = go.Figure(go.Scattergeo())
    i = 0
    for file in os.listdir("../data/plane_data"):
        if file.endswith(".csv"):
            i += 1
            print(f"{i}", end="\r")
            df = pd.read_csv(f"../data/plane_data/{file}", converters={'trace': eval})
            fig.add_trace(go.Scattergeo(
                lon = df['trace'].apply(lambda x: x[2] if x[2] > -129 and x[2] < -64 else None),
                lat = df['trace'].apply(lambda x: x[1] if x[1] > 22 and x[1] < 49 else None),
                mode = 'lines',
                line = {'width': 1},
                name = file
            ))

        if i > 100:
            break
    
    fig.update_layout(mapbox = {'style': "stamen-terrain"})
    fig.update_geos(scope = "usa",)
    fig.show()

def heatmap():
    fig = go.Figure(go.Densitymapbox())
    i = 0
    lon = []
    lat = []
    for file in os.listdir("../data/plane_data"):
        if file.endswith(".csv"):
            i += 1
            print(f"{i}", end="\r")
            df = pd.read_csv(f"../data/plane_data/{file}", converters={'trace': eval})

            lon += df['trace'].apply(lambda x: x[2] if x[2] > -129 and x[2] < -64 else None).tolist()
            lat += df['trace'].apply(lambda x: x[1] if x[1] > 22 and x[1] < 49 else None).tolist()

        if i > 1000:
            break

    fig.add_trace(go.Densitymapbox(
        lon = lon,
        lat = lat,
        #mode = 'lines',
        #line = {'width': 1},
        #name = file
    ))

    fig.update_layout(mapbox = {'style': "stamen-terrain"})
    fig.update_geos(scope = "usa",)
    fig.show()

def countymap():
    from urllib.request import urlopen
    import json
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        countiesjson = json.load(response)

    
    counties = pd.read_csv("../data/wildfire_risk_dataset.csv", converters={'STCOFIPS': str})
    ca_counties = counties[counties['STATE'] == 'California']
    fig = go.Figure(go.Choroplethmapbox(geojson=countiesjson,
                    locations=ca_counties['STCOFIPS'], z=ca_counties['WFIR_RISKS'], colorscale="Viridis", zmin=min(counties['WFIR_RISKS']), zmax=100,
                                    marker_opacity=0.5, marker_line_width=0))

    i = 0

    for file in os.listdir("../data/plane_data"):
        if file.endswith(".csv"):
            i += 1
            print(f"{i}", end="\r")
            df = pd.read_csv(f"../data/plane_data/{file}", converters={'trace': eval})
            fig.add_trace(go.Scattermapbox(
                lon = df['trace'].apply(lambda x: x[2] if x[2] > -129 and x[2] < -64 else None),
                lat = df['trace'].apply(lambda x: x[1] if x[1] > 22 and x[1] < 49 else None),
                mode = 'lines',
                fill="toself",
                line = {'width': 5},
                name = file
            ))

        if i > 100:
            break
    
    fig.update_layout(mapbox = {'style': "stamen-terrain"})
    fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
    fig.update_geos(scope = "usa",)
    fig.show()

countymap()

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
#fig.update_layout(
#    mapbox = {'style': "stamen-terrain", 'zoom': 1})

# fig.update_layout(
#     mapbox = {'style': "stamen-terrain", 
#               })

# fig.update_geos(
#     scope = "usa",)
# fig.show()