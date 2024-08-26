import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image

########################## Initial settings for the dashboard ####################################################


st.set_page_config(page_title = 'NY Citi Bikes Strategy Dashboard (Jersey City)', layout='wide')
st.title("Jersey City Strategy Dashboard")


# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])


########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot_7.csv', index_col = 0)
top20 = pd.read_csv('top_20.csv', index_col = 0)
df_group = pd.read_csv('daily_rides_and_temperature.csv', index_col = 0)

st.markdown("The dashboard will help with the expansion problems in Jersey City")

######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems NY Citi Bikes currently faces in Jersey City.")
    st.markdown("Right now, NY Citi bikes runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("citi_bike.jpg") #source: https://unsplash.com/photos/blue-and-black-bicycle-lot-WdHiBJ1PFmo
    st.image(myImage)


# ########################### DEFINE THE CHARTS ############################


## Dual Axis line chart 

# Create subplots with a secondary y-axis

elif page == 'Weather component and bike usage':

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
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")

## Bar chart 

elif page == 'Most popular stations':

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
    st.markdown("I will add insights about most popular stations here")

### Add the map  ###

elif page == 'Interactive map with aggregated bike trips': 

    st.write("Interactive map showing aggregated bike trips over Jersey City")

    # Assign the HTML file name to a variable
    file_name = "NYC_Citi_Bikes_Map.html"

    # Read file and keep in variable 
    with open(file_name, 'r') as f:
        html_data = f.read()

    ## Show in web page 
    st.header("Aggregated Bike Trips in Jersey City (Top 100 Routes)")
    st.components.v1.html(html_data,height = 1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("Insights.")
    st.markdown("Insights.")

else:
    
    st.header("Conclusions and recommendations")
    bikes = Image.open("recs_page.jpg")  #source: Unsplash
    st.image(bikes)
    st.markdown("### Our analysis has shown that NY Citi Bikes should focus on the following objectives moving forward:")
    st.markdown("- Recommendations")
    st.markdown("- Recommendations")


