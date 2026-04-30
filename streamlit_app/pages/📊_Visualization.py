import streamlit as st
import requests
import geopandas as pdf
import pandas as pd
import streamlit.components.v1 as components
from bokeh.embed import file_html
from bokeh.resources import CDN
import streamlit.components.v1 as components
import holoviews as hv
import holoviews as hv

from InteractiveMap.map_background import prepare_map_data, load_polygon, panel_to_html
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
STREAMLIT_APP_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

st.set_page_config(page_title="Visualization", layout="wide")

st.title("Visualization of COVID-19 Infection Data in Hungary")

st.write(
    "This is the visualization page of the application assignment. "
    "Here you can explore interactive visualizations of the COVID-19 infection data "
    "across different counties in Hungary."
)

data_url = "http://127.0.0.1:8000/api/weekly-data/"
county_url = "http://127.0.0.1:8000/api/counties/" 

counties_response = requests.get(county_url)
counties = counties_response.json()
county_name_to_id = {county["name"]: county["id"] for county in counties}
county_id_to_name = {county["id"]: county["name"] for county in counties}

all_data_request = requests.get(data_url)

if "response" not in st.session_state:
    st.session_state.response = None

with st.expander("Upload your data"):
    with st.form("Upload data to Django"):
        week = st.date_input("Select an infection date:")

        uploaded_file = st.file_uploader(
            "Upload your geospatial infection data",
            type=["csv"]
        )
        
        submit_button = st.form_submit_button("Upload to Django")

        if uploaded_file:
            df=pd.read_csv(uploaded_file)

            county_data = []
            for _, row in df.iterrows():
                county_data.append({
                    "county_id" : county_name_to_id[row["NAME"]],
                    "infections": float(row["Number_of_Infections"])
                })
            
            payload = {
                "date": str(week),
                "county_data": county_data
            }      
            
            if submit_button:
                response = requests.post(data_url, json=payload)
                if response.status_code in [200, 201]:
                    st.success("Uploaded successfully!")
                    st.balloons()
                    st.session_state.response = response
                else:
                    st.error(response.status_code)
                    st.markdown(response.text, unsafe_allow_html=True)

    

if all_data_request.status_code == 200 and all_data_request.json() != []:
    cols = st.columns(2, vertical_alignment="top")
    fetch_response = all_data_request
    st.session_state.fetch_response = fetch_response

    date_list = list(map(lambda x: x['date'], fetch_response.json()))
    
    with cols[0]:
        st.subheader("Data Table")
        if len(date_list)>1:
            selected_date = st.selectbox("Select a week", date_list)
            st.write(f"Week: {selected_date}")
        else:
            st.write(f"Week: {date_list[0]}")
        
        selected_response = requests.get(data_url, params={"date" : selected_date})

        df, edges = prepare_map_data(selected_response)
        shown_df = df.drop(columns=['geometry']).round(2)
        st.dataframe(shown_df)
    
    
    panel = load_polygon(selected_date, df, edges)
    html = panel_to_html(panel)

    #bokeh_fig = hv.render(layout, backend="bokeh")
    #bokeh_fig.background_fill_color = None
    #bokeh_fig.border_fill_color = None
    #bokeh_fig.outline_line_color = None

    with cols[1]:
        st.subheader("Number of weekly new cases per 100 000 people")
        #html = file_html(bokeh_fig, CDN, "Map")
        html = html.replace(
            "<body>",
            "<body style='margin:0; padding:0; overflow:hidden;'>"
        )
        components.html(html, height=700)