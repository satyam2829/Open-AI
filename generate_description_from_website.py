import json
import os

import openai
import requests
import streamlit as st
from bs4 import BeautifulSoup

# load_dotenv()
openai.api_key = st.secrets["key"]

st.header("Generate description using Open AI")

focus_area_instruction = "Generate top 5 focus area without its description of the company from below given content and format the result as lists\n\n"
description_instruction = "Generate the summary from below given content in maximum 150 words"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def get_cleaned_document(url):
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")
    website_body = soup.find("body")
    input = website_body.get_text()
    return input

website_url = st.text_input("Enter the website url")

if st.button("SUBMIT"):

    response = dict()
    input = get_cleaned_document(website_url)

    completion_key_focus_area = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": focus_area_instruction + "\n" + input}
        ],
    )

    completion_description = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": description_instruction + "\n" + input}
        ],
    )

    focus_area_response = completion_key_focus_area.choices[0].message.content
    description_response = completion_description.choices[0].message.content
    response["description"] = description_response
    response["focus_areas"] = focus_area_response
    st.json(response)
