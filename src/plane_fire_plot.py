import plotly as px
import pandas as pd
import plotly.graph_objects as go
import os
import sqlite3


fig = go.Figure(go.Densitymapbox())


def countymap():
    from urllib.request import urlopen
    import json
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        countiesjson = json.load(response)

    
    counties = pd.read_csv("../data/wildfire_risk_dataset.csv", converters={'STCOFIPS': str})
    ca_counties = counties[counties['STATE'] == 'California']
    
    db_path = '../data/wildfire.sqlite'
    
    conn = sqlite3.connect(db_path)
    # Replace 'your_table_name' with the actual table name
    query = "SELECT LATITUDE, LONGITUDE, FIRE_SIZE, FIRE_SIZE_CLASS FROM Fires"

    # Load data from SQLite into a DataFrame
    df = pd.read_sql_query(query, conn)

    # Sample a fraction of the data for visual clarity and performance
    df_sample = df.sample(frac=0.003)

    size_mapping = {'A': 2, 'B': 4, 'C': 6, 'D': 8, 'E': 10, 'F': 12, 'G': 14}
    df_sample['dot_size'] = df_sample['FIRE_SIZE_CLASS'].map(size_mapping)

    fig = go.Figure(go.Scattergeo(lon=df_sample['LONGITUDE'],
                    lat=df_sample['LATITUDE'],
                    text=df_sample['FIRE_SIZE_CLASS'],  # Display FIRE_SIZE_CLASS on hover
                    mode='markers',
                    hoverinfo='text',  # Ensure only the text is displayed on hover
                    marker=dict(
                        size=df_sample['dot_size'],
                        opacity=0.8,
                        reversescale=True,
                        autocolorscale=False,
                        symbol='circle',
                        line=dict(
                                width=1,
                                color='rgba(102, 102, 102)'
                                ),
                        colorscale='Reds',
                        cmin=0,
                        color=df_sample['FIRE_SIZE'],
                        cmax=df_sample['FIRE_SIZE'].max(),
                        colorbar_title="Fire Size (Acres)"
                    )))


    # Add California Risk Counties
    fig.add_trace(go.Choroplethmapbox(geojson=countiesjson,
                    locations=ca_counties['STCOFIPS'], z=ca_counties['WFIR_RISKS'], colorscale="Viridis", zmin=min(counties['WFIR_RISKS']), zmax=100,
                                    marker_opacity=0.5, marker_line_width=0))

    i = 0

    print("Loading data...")
    #df = pd.read_csv("../data/cali-dataset.tsv", sep = "\t", converters={'latitude': eval, 'longitude': eval})
    print("Loaded data")

    lon = []
    lat = []

    """  for _, row in df.iterrows():
        i += 1
        print(f"{i}", end="\r")
        for o in range(len(row["longitude"])):
            lon.append(row["longitude"][o])
            lat.append(row["latitude"][o])
            if o < len(row["longitude"]) - 1:
                    lon.append(row["longitude"][o + 1])
                    lat.append(row["latitude"][o + 1])
            lon.append(None)
            lat.append(None)

        if i > 1000:
            break  """

    # Add Flight Paths
    fig.add_trace(go.Scattermapbox(
            lon = lon,
            lat = lat,
            mode = 'lines',
            line = {'width': 5, "color": "blue"},
            opacity = 0.1
        ))
    




    
    fig.update_layout(title='US Wildfires from 1992 - 2015',
                  geo=dict(scope='usa',
                        #    center=dict(lat=35, lon=-114.4179),
                           projection_type='albers usa',
                           projection_scale=1,
                           showland=True,
                           landcolor="rgb(250, 250, 250)",
                           subunitcolor="rgb(217, 217, 217)",
                           countrycolor="rgb(217, 217, 217)",
                           countrywidth=0.5,
                           subunitwidth=0.5)
                  )


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