# 🦠 COVID-19 Visualization App

An interactive web application for visualizing COVID-19 infection data across Hungary, built with **Django (REST API)** and **Streamlit (frontend)**.

Developed as part of the *Data Exploration and Visualization* course at **Eötvös Loránd University (ELTE)**.

---

## ✨ Features

- Interactive map-based visualization of infection data
- Upload custom geospatial datasets (CSV format)
- REST API backend for data handling
- Clean separation between backend (Django) and frontend (Streamlit)

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework  
- **Frontend:** Streamlit  
- **Data handling:** Pandas, GeoPandas  
- **Visualization:** Bokeh / GeoViews  

---

## How to use
 ### 1. Create a virtual environment
 First you need to create an enviroment with the reuirements.txt extensions

 ### 2. Run the application
 You need two terminals

 Terminal 1-Django backend:

 Navigate into the backend directory and start the server:
 ```bash
 cd backend
 python manage.py runserver
 ```
 You should see something like this
 ```bash
 Django version 6.0.4, using settings 'core.settings'
 Starting development server at http://127.0.0.1:8000/
 Quit the server with CTRL-BREAK.

 WARNING: This is a development server. Do not use it in a production setting.
 ```
 Terminal 2 -STreamlit frontend:
 Navigate into the Streamlit app directory and run:
 ```bash
 cd backend
 streamlit run .\🏠_Home.py
 ```
 Expected output:
 ```bash
 You can now view your Streamlit app in your browser.

 Local URL: http://localhost:8501
 Network URL: http://192.168.0.52:8501
 ```
 The application homepage should open automatically in your browser.
 Follow the on-screen instructions to use the app.

## Project strucure
    covid-visualization-app/
    ├── backend/
    │   ├── CovidIntVis/
    │   │   ├── api/
    │   │   │   ├── serializers.py
    │   │   │   ├── urls.py
    │   │   │   └── views.py
    │   │   ├── migrations/
    │   │   ├── models.py
    │   │   └── admin.py
    │   ├── core/
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   └── wsgi.py
    │   ├── db.sqlite3
    │   └── manage.py
    ├── streamlit_app/
    │   ├── pages/
    │   │   └── Visualization.py
    │   ├── Home.py
    │   └── assets/
    └── requirements.txt
 
 ### Notes
 Django models (models.py) define how the data is stored.
 Serializers convert model data into JSON format.
 The API is available at:
    http://127.0.0.1:8000/api/
 The Streamlit app consumes this API and visualizes the data. 
 
 AI was used to learn how Django works and to help me code faster

### 1. Clone the repository

```bash
git clone https://github.com/klukacs2004/covid-visualization-app.git
cd covid-visualization-app