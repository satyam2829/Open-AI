import json
import os

import openai
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
openai.api_key = st.secrets["OPENAI_SECRET_KEY"]

st.header("Extract Funding and Financial Information")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

instruction = "Identify the following feilds from the below given news article\n\n1. startup name\n2. startup location\n3. founders \n4. funding amount\n5. funding round date\n6. VC Investors\n7. Angel Investors\n8. funding type\n9. Founded Date\n10. Article heading\n11. Article date\n\n"
financial_instruction = "Extract key financial information (revenue, profit/loss, expenses)\n\n"

def get_cleaned_document(url):

    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")
    website_body = soup.find("body")
    input = website_body.get_text()
    return input

url = st.text_input("Enter the URL")

if st.button("SUBMIT"):

    input = get_cleaned_document(url)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. "},
            {"role": "user", "content": instruction + "\n" + input},
            {"role": "user", "content": "format the result as json object."},
            {"role": "user", "content": "feild names should be in lower case combined with under score"},
            {"role": "user", "content": "In case of multiple startups, use startup name as key"}
        ],
    )

    financial_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. "},
            {"role": "user", "content": financial_instruction + "\n" + input},
            {"role": "user", "content": "format the result as table."},
            {"role": "user", "content": "feild names should be in lower case combined with under score"},
            {"role": "user", "content": "In case of financial from multiple year, use year as the key"}
        ],
    )

    response = completion.choices[0].message.content
    financial_response = financial_completion.choices[0].message.content
    st.json(response)
    st.success(financial_response)
