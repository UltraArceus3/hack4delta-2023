import plotly as px
import pandas as pd
import plotly.graph_objects as go



df = pd.read_json("data/trace_full_000000.json")

lat = df['trace'].apply(lambda x: x[1] if x[1] > 22 and x[1] < 49 else None)
lon = df['trace'].apply(lambda x: x[2] if x[2] > -129 and x[2] < -64 else None)

print(lat)

# fig = go.Figure(go.Scatter(x=lat, y=lon, fill="toself"))
# fig.show()
    
fig = go.Figure(go.Scattermapbox(
    mode = "markers+lines",
    lon = lon,
    lat = lat,
    marker = {'size': 10}),
    line = {'width': 45})

fig.update_layout(
    geo = {'scope': 'usa'},)

fig.show()