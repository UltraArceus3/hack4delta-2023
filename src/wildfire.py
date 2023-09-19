import sqlite3
import pandas as pd
import plotly.graph_objects as go

# Connect to the SQLite database
conn = sqlite3.connect('../data/wildfire.sqlite')
# Replace 'your_table_name' with the actual table name
query = "SELECT LATITUDE, LONGITUDE, FIRE_SIZE, FIRE_SIZE_CLASS FROM Fires"

# Load data from SQLite into a DataFrame
df = pd.read_sql_query(query, conn)

# Sample a fraction of the data for visual clarity and performance
df_sample = df.sample(frac=0.003)

size_mapping = {'A': 2, 'B': 4, 'C': 6, 'D': 8, 'E': 10, 'F': 12, 'G': 14}
df_sample['dot_size'] = df_sample['FIRE_SIZE_CLASS'].map(size_mapping)


# Plot using Plotly
fig = go.Figure(data=go.Scattergeo(
    lon=df_sample['LONGITUDE'],
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

fig.show()