from dotenv import load_dotenv
import os
import json
import requests
import streamlit as st


load_dotenv()

api_key = os.getenv("NASA_API_KEY")
api_host = os.getenv("NASA_API_HOST")

url = f'{api_host}?&api_key={api_key}'
response = requests.get(url)

if response.status_code == 200:
    content = response.json()
else:
    with open("content.json") as file:
        content = file.read()
    content = json.loads(content)

st.title('Nasa Image Of the Day')
st.header(content['title'])
st.image(content['hdurl'])
st.write(content['explanation'])
st.header('Geek Info')
st.write(content)


