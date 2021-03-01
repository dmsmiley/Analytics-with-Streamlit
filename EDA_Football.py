import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Premier League Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of Premier League player stats
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))

# web scraping of data
@st.cache
def load_data(year):
    url = "https://fbref.com/en/comps/9/Premier-League-Stats" + str(year) + ""