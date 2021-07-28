import streamlit as st
import numpy as np
import pandas as pd
import requests
import io
   
@st.cache
def get_data():
    url = "https://raw.githubusercontent.com/charliejeynes/guardian_film_reviews/main/data/brads_test.csv" # Make sure the url is the raw version of the file on GitHub
    download = requests.get(url).content
df = get_data()

df = pd.read_csv(io.StringIO(download.decode('utf-8')))

st.title('Guardian Film Review Database')

st.write("The below Table is all of Peter Bradshaw's film reviews since 2000-present")

#df = pd.read_csv('https://raw.githubusercontent.com/charliejeynes/guardian_film_reviews/main/data/brads_test.csv')

df1 = df[['headline', 'webPublicationDate', 'starRating', 'shortUrl', 'bodyText']]

df1 = df1.rename(columns={'headline':'Film name & headline'})

st.write(df1)

user_input = st.text_input("Search for a film")

if user_input:
    st.write(df1[df1['Film name & headline'].str.contains(user_input, case=False)==True])




