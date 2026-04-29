import streamlit as st

st.set_page_config(page_title="Application Assignment", layout="wide")
    

st.title("Welcome to the Application Assignment Home Page")
with st.expander("About the Application", key="about_expander"):
    st.write("""This is the home page of the application assignment. Use the navigation menu to explore different sections of the application. 
         This application is designed to visualize COVID-19 infection data across different counties in Hungary. 
         It allows users to upload geospatial infection data and provides interactive visualizations to analyze the spread 
         of the virus over time.""")
    
with st.expander("How to use the Application", key="usage_expander"):
    st.write("To use the application, follow these steps:")
    st.write("1. Navigate to the 'Data Upload' section to upload your geospatial infection data in CSV format.")
    st.write("2. Once the data is uploaded, go to the 'Visualization' section to explore interactive maps and charts that display the infection trends across different counties.")
    st.write("3. Use the filters and options available in the visualization section to customize your analysis and gain insights into the COVID-19 spread.")
