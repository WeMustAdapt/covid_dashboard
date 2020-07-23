# Libraries - matplotlib for plotting, pandas for data manipulation and datetime library for supplying classes to manipulate dates and times.
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# Define a function to retrieve data from the API.
@st.cache
def fetch_data():
    df = pd.read_json('http://covidtracking.com/api/v1/us/daily.json')
    df['date'] = pd.to_datetime(df['date'], format = "%Y%m%d") # Convert the 'date' column to datetime objects
    df.set_index('date', inplace = True) # Reindex
    df.sort_index(ascending = True, inplace = True) # Sort the DateFrames by the dates.
    return df

df = fetch_data()

# Create a disctionary of data descriptors and their corresponding columns in the DataFrame constructed from the API. 
options = {"Cumulative Positive Results": 'positive',
           "Daily Positive Tests": 'positiveIncrease',
           "Cumulative Deaths": 'death',
           "Daily Deaths": 'deathIncrease',
           "Current Hospitalizations": 'hospitalizedCurrently',
           "Daily Hospitalizations": 'hospitalizedIncrease',
           "Cumulative Hospitalizations": 'hospitalizedCumulative',
           "Current ICU Patients": 'inIcuCurrently',
           "Cumulative ICU Patients": 'inIcuCumulative',
           "Current Ventilator Patients": 'onVentilatorCurrently',
           "Cumulative Ventilator Patients": 'onVentilatorCumulative',
           "Recovered Patients": 'recovered',
           "Daily Tests Performed": 'totalTestResultsIncrease',
           "Cumulative Tests Performed": 'totalTestResults'}

# Make the dashboard.
# Title
st.title('COVID-19 Dashboard: U.S. Data')

# Reference your data source.
st.subheader('Source: https://covidtracking.com')

# Streamlit comes with many sidebar features.
# For now we will add a date picker feature. We chose an arbitrary start date of 3/1/2020 and end date matching the latest date in the DataFrame
start_date = st.sidebar.date_input("Start Date", value = datetime(2020,3,1)) 
end_date = st.sidebar.date_input("End Date", value = df.index.max())

# Have the user pick which visualizations they want to see. We use a multi-select feature.
charts = st.sidebar.multiselect("Select individual charts to display:", options = list(options.keys()), default = list(options.keys())[0:1])

# In the main window, we now loop through the charts list and plot each one on a single axis. 
for chart in charts: 
    df[options[charts]].loc[start_date:end_date + timedelta(days = 1)].plot(label = chart, figsize = (8, 6)) # selects the column in the DataFrame corresponding to the chosen option, filters out the dates chosen
    plt.xlabel('Date')
    plt.legend(loc = "upper left")
st.pyplot()