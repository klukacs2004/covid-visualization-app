import streamlit as st
import requests

st.set_page_config(page_title="Visualization", layout="wide")

st.title("Visualization of COVID-19 Infection Data in Hungary")

st.write(
    "This is the visualization page of the application assignment. "
    "Here you can explore interactive visualizations of the COVID-19 infection data "
    "across different counties in Hungary."
)

data_url = "http://127.0.0.1:8000/api/covid-data/"
upload_url = "http://127.0.0.1:8000/api/upload-csv/"

if "response" not in st.session_state:
    st.session_state.response = None


def fetch_covid_data():
    response = requests.get(data_url)
    st.session_state.response = response

    if response.status_code == 200:
        st.success("COVID-19 data fetched successfully!")
    else:
        st.error(f"Failed to fetch COVID-19 data. Status code: {response.status_code}")


cols = st.columns(2)

with cols[0]:
    st.subheader("Fetch data from Django")

    if st.button("Fetch COVID-19 Data"):
        fetch_covid_data()

    if st.session_state.response is not None:
        if st.session_state.response.status_code == 200:
            data = st.session_state.response.json()
            st.write(data)
        else:
            st.error(st.session_state.response.text)


with cols[1]:
    st.subheader("Upload data to Django")

    uploaded_file = st.file_uploader(
        "Upload your geospatial infection data",
        type=["csv"]
    )

    if uploaded_file is not None:
        st.success("File selected successfully!")

        if st.button("Upload to Django"):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            response = requests.post(upload_url, files=files)

            if response.status_code == 200:
                st.success("Uploaded successfully!")
                st.balloons()
            else:
                st.error(response.text)

