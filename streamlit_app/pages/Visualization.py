import streamlit as st
import requests
import geopandas as pdf
import pandas as pd


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


if "response" not in st.session_state:
    st.session_state.response = None


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
                "infections": int(row["Number_of_Infections"])
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


def fetch_data():
    fetch_response = requests.get(data_url)
    st.session_state.fetch_data = fetch_data

    if fetch_response.status_code == 200:
        data = fetch_response.json()[0]
        df = pd.DataFrame(data['county_data'])
        df_county = pd.json_normalize(df["county"]).drop(columns=["id"])
        df = pd.concat([df.drop(columns=["county"]), df_county],axis=1).drop(columns=["id"])
        st.dataframe(df)
        del(df)
    else:
        st.markdown(fetch_response.text, unsafe_allow_html=True)
    

if st.session_state.response is not None or requests.get(data_url).status_code == 200:
    if st.button("Fetch COVID-19 Data", key="fetch_button"):
        fetch_data()

