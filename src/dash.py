import dash
from dash import html
import plotly.graph_objects as go
import pandas as pd

import json
from urllib.request import urlopen
import sqlite3

# Sample data
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y1': [10, 11, 12, 13, 14],
    'y2': [20, 19, 18, 17, 16]
})

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    dcc.Graph(id='plot1'),
    dcc.Graph(id='plot2')
])

# Define the callback to update the first plot
@app.callback(
    Output('plot1', 'figure'),
    Input('plot2', 'relayoutData')
)
def update_plot1(relayoutData):
    # Replace this with your own plot update logic
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        countiesjson = json.load(response)

    counties = pd.read_csv("../data/wildfire_risk_dataset.csv", converters={'STCOFIPS': str})
    ca_counties = counties[counties['STATE'] == 'California']

    fig = go.Figure(go.Choroplethmapbox(geojson=countiesjson,
                    locations=ca_counties['STCOFIPS'], z=ca_counties['WFIR_RISKS'], colorscale="Viridis", zmin=min(counties['WFIR_RISKS']), zmax=100,
                    marker_opacity=0.5, marker_line_width=0))
    return fig

# Define the callback to update the second plot

def update_plot2(relayoutData):
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
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
