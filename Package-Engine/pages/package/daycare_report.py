import pandas as pd
import numpy as np
import streamlit as st
from datetime import date

def preprocess1(file):
    
    # read in data
    df = pd.read_excel(file)
    
    #rename column
    df.rename(columns={'Pet Companions, inc.':'Client'}, inplace=True)
    
    #filter for just client column
    df = df[['Client']].dropna().reset_index(drop=True).drop(index=[0]).reset_index(drop=True)
    
    #drop last row
    df = df.drop(index=[len(df)-1])
        #[df['Client']!='Friday, September 15, 2023']
    
    #initialize new rows
    df['Date'] = ''
    df['Day of Week'] = ''
    df['Dog']=''
    
    return df[['Date', 'Day of Week', 'Client', 'Dog']]


def fill_df(df):
    
    #iterate through rows
    for i in range(len(df)):
        
        #if it is string then it is an owner and dog
        if type(df.loc[i, 'Client']) == str:
            df.loc[i, 'Date'] = current_date
            df.loc[i, 'Dog'] = df.loc[i, 'Client'].split(':')[1]
            df.loc[i, 'Client'] = df.loc[i, 'Client'].split(':')[0]
            df.loc[i, 'Day of Week'] = current_date.strftime('%A')
        #it is a datetime format
        else:
            current_date = df.loc[i, 'Client'].date()
            df.drop(index=[i], inplace=True)
            
    df.reset_index(drop=True, inplace=True)
    return df


@st.cache_data
def daycare_reporting(file):
    df = preprocess1(file)
    df = fill_df(df)
    return df