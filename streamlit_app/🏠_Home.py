import streamlit as st
import pandas as pd

st.set_page_config(page_title="Application Assignment", layout="wide", page_icon="🦠")
    
st.title("Welcome to the Application Assignment Home Page")

st.write("")

with st.expander("About the Application", key="about_expander"):
    st.write("""This is the home page of the application assignment. Use the navigation menu to explore different sections of the application. 
         This application is designed to visualize COVID-19 infection data across different counties in Hungary. 
         It allows users to upload geospatial infection data and provides interactive visualizations to analyze the spread 
         of the virus over time.""")
    
with st.expander("How to use the Application", key="usage_expander"):
    st.write("To use the application, follow these steps:")
    st.write('1. Navigate to the ``Visualization`` page in the sidebar to upload your geospatial infection data in CSV format or explore the data already uploaded.')
    st.write("2. If you feel like uploading your data, just use a CSV file with the following structure:")
    st.dataframe(pd.read_csv("covid_data_20200419.csv"))

st.write("")

cols = st.columns(2, )
with cols[0]:
    st.image("giphy.gif", caption="Source: https://giphy.com/gifs/motion-graphics-animated-gif-mograph-dVuyBgq2z5gVBkFtDc",width=800)
with cols[1]:
    st.image("Spread_of_the_Covid-19_pandemic_in_Europe.gif", caption="Source: https://commons.wikimedia.org/wiki/File:Spread_of_the_Covid-19_pandemic_in_Europe.gif")