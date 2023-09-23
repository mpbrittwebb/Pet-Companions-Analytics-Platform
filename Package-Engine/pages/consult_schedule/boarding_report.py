import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import streamlit as st

def preprocess(df):
    
    df.dropna(how='all', axis = 0, inplace=True)
    df.dropna(how='all', axis = 1, inplace=True)
    
    df.rename(columns={'Unnamed: 1': 'Date', 'Unnamed: 7':'Boarders'}, inplace=True)
    df = df[['Date', 'Boarders']].reset_index(drop=True)
    df['Day of the Week'] = ''
    df['Average Boarders'] = 0
    
    for i in range(len(df)):
        if not isinstance(df.loc[i, 'Date'], datetime):
            df.drop(index=[i], inplace=True)
        else:
            df.loc[i, 'Day of the Week'] =  df.loc[i, 'Date'].strftime('%A')
            df.loc[i, 'Date'] = df.loc[i, 'Date'].date()
            
    df.reset_index(drop=True, inplace=True)
    
    df.drop(index=[0], inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    
    return df[['Day of the Week', 'Date', 'Boarders', 'Average Boarders']]


def average(df):
    
    if df[df['Date'] == date.today()+timedelta(days=-27)].empty:
        print('Please set start date to include last month of data')
        
    past = df[(df['Date']<=date.today())&(df['Date']>=date.today()+timedelta(days=-27))]
    
    for i in range(7):
        day = date.today() + timedelta(days=i) 
        df.loc[df['Day of the Week'] == day.strftime('%A'), 'Average Boarders'] = sum(past[past['Day of the Week'] == day.strftime('%A')]['Boarders'])/4
    
    return df

st.cache_data
def boarding(file):
    df = pd.read_excel(file)
    df = preprocess(df)
    df = average(df)
    return df