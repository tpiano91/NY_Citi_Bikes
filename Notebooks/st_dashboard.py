import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 

st.set_page_config(page_title = 'NY Citi Bikes (Jersey City) Strategy Dashboard', layout='wide')

st.title("NY Citi Bikes (Jersey City) Strategy Dashboard")

st.markdown("The dashboard will help with the expansion problems in Jersey City")

top20 = pd.read_csv('top_20.csv', index_col = 0)
df_group = pd.read_csv('daily_rides_and_temperature.csv', index_col = 0)

# ########################### DEFINE THE CHARTS ############################


## Bar chart 

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Greens'}))

# Update layout to provide more space for the station names
fig.update_layout(
    title='Top 20 most popular bike stations in Jersey City',
    xaxis_title='Start stations',
    yaxis_title='Sum of trips',
    width=900,  # Adjust the width of the plot
    height=600,  # Adjust the height of the plot
    margin=dict(b=200),  # Increase bottom margin to provide more space for x-axis labels
    xaxis=dict(
        tickangle=-45,  # Rotate x-axis labels for better readability
        automargin=True,  # Automatically adjust margins to fit labels
        tickfont=dict(size=10)  # Adjust font size for x-axis labels
    )
)
st.plotly_chart(fig, use_container_width = True)

## line chart 

# Create subplots with a secondary y-axis
fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add the first trace for daily bike rides
fig_2.add_trace(
    go.Scatter(
        x=df_group['date'], 
        y=df_group['ride_id'], 
        name='Daily bike rides', 
        marker=dict(color='Green')
    ), 
    secondary_y=False
)

# Add the second trace for daily temperature
fig_2.add_trace(
    go.Scatter(
        x=df_group['date'], 
        y=df_group['avgTemp'], 
        name='Daily temperature', 
        marker=dict(color='red')
    ), 
    secondary_y=True
)

# Update layout with titles and dimensions
fig_2.update_layout(
    title='Daily Bike Rides and Temperature in Jersey City', 
    xaxis_title='Date',
    yaxis_title='Daily Bike Rides',
    height=500
)
# Update secondary y-axis title
fig_2.update_yaxes(title_text='Temperature (°C)', secondary_y=True)

st.plotly_chart(fig_2, use_container_width=True)

### Add the map  ###

# Assign the HTML file name to a variable
file_name = "NYC_Citi_Bikes_Map.html"

# Read file and keep in variable 
with open(file_name, 'r') as f:
    html_data = f.read()

## Show in web page 
st.header("Aggregated Bike Trips in Jersey City")
st.components.v1.html(html_data,height = 1000)



