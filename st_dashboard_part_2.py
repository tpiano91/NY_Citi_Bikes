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
  ["Intro page","Weather component and bike usage","Most popular starting stations",
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
    st.markdown("- Weather component and bike usage")
    st.markdown("- Most popular stations")
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
    
    ### First Paragraph of Text
    
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October. Below are more specific initial insights:")
   
    ### Insight 1

    st.markdown("1. There are noticeable points of drops in bike usage. The first in early October; followed by a more signifcant drop in mid-November, and again in mid-December (into the holiday season). ")

    ### Insight 2

    st.markdown("2. There are individual days of particularly low bike-usage that don't seem to correlate with temperature. The two lowest days for bike usage in 2022 are January 29th (a Saturday) and December 25th. Other noticeably low-use days (in relation to their particular time period) are March 12th (Saturday), May 7th (Saturday), September 6th (Tuesday), and October 3rd (Monday). Further research recommended to find reason for these 'isolated dips.'")
    
    ### Insight 3

    st.markdown("3. There are noticeable points of rises in bike usage in mid-February, mid-March and mid-April. Peak usage is reached in May and is sustained until October.")

## Bar chart 

elif page == 'Most popular starting stations':

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Greens'}))

    # Update layout to provide more space for the station names
    fig.update_layout(
        title='Most Frequent Start Stations in Jersey City (Top 20)',
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

    ### Insight 1

    st.markdown("")


### Add the map  ###

elif page == 'Interactive map with aggregated bike trips': 

    st.write("###### Below is an interactive map showing aggregated bike trips over Jersey City. Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")

    # Assign the HTML file name to a variable
    file_name = "NYC_Citi_Bikes_Map.html"

    # Read file and keep in variable 
    with open(file_name, 'r') as f:
        html_data = f.read()

    ## Show in web page 
    st.header("Most Popular Routes in Jersey City (Aggregation/Top 100 Routes)")
    st.components.v1.html(html_data,height = 1000)

    # Insight 1: Three Main Hubs
    st.markdown("#### Three Main Hubs")
    st.markdown("There are three main hubs for bike usage (which are visible by observing the 'route arcs'). 'Hub 1' around in the area of Hoboken Terminal and Yards/Stevens Institute of Technology (parallel to the Meatpacking District in Manhattan); 'Hub 2' south (slightly west of what is labeled Downtown Jersey City); and smaller 'Hub 3' furhter west (near Indian Square). I will focus my insights mostly on Hub 1 and 2. There is also a much smaller Hub 4 in downtown Jersey City, by the water (parallel to Battery City Park in Manhattan).")

    #Insight 2: Hub 1 vs. Hub 2 Trends
    st.markdown("#### Insights: Hub 1")
    st.markdown("The 2nd, 3rd, 4th and 5th most popular starting stations (South Waterfront Walkway at Sinatra & 1st, Hoboken Terminal at River & Hudson, Hoboken Terminal at Hudson St. and Hudson Pl, and City Hall at Washington and 1st) are all in Hub 1, and are all located within the same area of Hub 1. The most popular routes in Hub 1 flow to and from these four centralized stations")
    
    #Insight 3: Hub 2 Insights
    st.markdown("#### Insights: Hub 2")
    st.markdown("The most popular starting station in Jersey City is Grove Street, which appears to be the center of Hub 2. The most popular routes in Hub 2 flow to and from Grove Street.")
    
    #Insight 4: Hub 1 vs. 2 Insights
    st.markdown("#### Insights: Hub 1 vs. Hub 2")
    st.markdown("Hub 1 and Hub 2 both clearly have a 'central area', however Hub 1 has four main stations at its' center, whereas Hub 2 only has one (Grove Street, which is the most popular station of all). ")

    #Insight 5: Bridge Stations Between Hubs 1 and 2
    st.markdown("#### Insights: Popular Stations Between Hubs 1 and 2")
    st.markdown("Newport Pkwy, Hamilton Park, and Newport Path are the 6th-8th most popular starting stations. All three locations are in the same area in between Hubs 1 and 2, suggesting that these three popular stations may be connecting stations in between the two main hubs.")

    

else:
    
    st.header("Conclusions and recommendations")
    bikes = Image.open("recs_page.jpg")  #source: Unsplash
    st.image(bikes)
    st.markdown("### Our analysis has shown that NY Citi Bikes should focus on the following objectives moving forward:")
    st.markdown("- Scale back number of bikes after October. This can be done in phases, according to the three points of drops in bike usage (in early October; followed by a more signifcant drop in mid-November; and again in mid-December). Further statistical analysis recommended to determine how much to scale back in each phase.")
    st.markdown("- Conversely, after the winter, increase the number of bikes in three phases according to the noticeable points of rises in bike usage (mid-February, mid-March and mid-April). Further statistical analysis recommended to determine how to implement the increase of bike as the temperature rises in through the late winter/spring.")
    st.markdown("- In Hub 1, the four most popular 'central stations' are all situated near the waterfront. Additional analysis is required to assess if these four stations can manage being the central stations of this hub; or if these stations should be expanded or if additional stations should be established in the area to alleviate congestion at these four locations. ")
    st.markdown("- In Hub 2, further analysis is recommended to assess whether Grove Street can manage being the central station of this hub, or if the station should be expanded or additional stations introduced in the area to reduce congestion. ")
    st.markdown("- To ensure that bikes are consistently available at the most popular locations, further analysis is necessary to identify specific times of day when these stations predominantly serve as either origin or destination points. During periods when they function primarily as origin stations, it may be important to ensure that an adequate supply of bikes is maintained by replenishing the stock frequently. Conversely, when these stations act as key destinations, efforts should be focused on clearing returned bikes quickly to free up docking space and redistribute them to areas with higher demand for departures. ")

