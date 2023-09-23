import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def sales_preprocess(file):
    df = pd.read_excel(file)
    df = df[['Unnamed: 0', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 10', 
             'Unnamed: 11', 'Unnamed: 13', 'Unnamed: 17']]
    df.dropna(how='all', axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.iloc[0] = df.iloc[0].fillna(value='Invoice')
    df.rename(columns=df.iloc[0], inplace = True)
    df.drop(index=[0], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df