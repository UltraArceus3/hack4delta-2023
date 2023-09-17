import dash
from dash import dcc, html
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

db_path = '/Users/vihaan/Downloads/wildfire.sqlite'

conn = sqlite3.connect(db_path)
query = "SELECT latitude, longitude, FIRE_SIZE, FIRE_SIZE_CLASS FROM Fires"
data1 = pd.read_sql_query(query, conn)

file_path = '/Users/vihaan/Projects/flight_sijm/cali-dataset.tsv'
data2 = pd.read_csv(file_path, sep='\t', converters={'latitude': eval, 'longitude':eval})



filtered_data = data1.loc[~data1['FIRE_SIZE_CLASS'].isin(['A', 'B'])]

# fig = px.scatter_mapbox(filtered_data,
#                         lat='LATITUDE',
#                         lon='LONGITUDE',
#                         size='FIRE_SIZE',
#                         color='FIRE_SIZE_CLASS',
#                         hover_name=None,
#                         mapbox_style="carto-positron",
#                         opacity=0.5,
#                         size_max=15,
#                         zoom=3)

fig = go.Figure()

for _, row in data2.iterrows():
    latitudes = list(row['latitude'])
    longitudes = list(row['longitude'])
    
    fig.add_trace(go.Scattermapbox(
        lat=latitudes,
        lon=longitudes,
        mode='lines',
        line={'width': 1, 'color' : 'red'},
    ))

fig.update_layout(
    height=600, 
    width=800, 
    mapbox_center={"lat": 40, "lon": -100}, 
    mapbox_style="carto-positron"  # Added mapbox_style
)

app.layout = html.Div([
    html.H1('Firefly'),
    dcc.Graph(id='wildfire-map', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)