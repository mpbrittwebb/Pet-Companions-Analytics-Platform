import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
import os 
import streamlit as st

def clean_df(df):
    
    df.rename(columns={'Unnamed: 4': 'Dog', 'Unnamed: 7': 'Client', 
                       'Unnamed: 11':'Breed', 'Unnamed: 16': 'Contact', 
                       'Unnamed: 20': 'Dog Gender'}, inplace=True)
    
    df['Client'].replace(' ', np.nan, inplace=True)
    df.dropna(how = 'all', axis=1, inplace=True)
    df.dropna(how='all', axis=0, inplace=True)
    df.drop(columns=['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 1', 
                 'Unnamed: 18', 'Unnamed: 13', 'Unnamed: 21', 
                 'Unnamed: 23', 'Unnamed: 24', 'Unnamed: 27',
                 'Unnamed: 31', 'Unnamed: 32', 'Unnamed: 33', 'Unnamed: 35'], 
        inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df[(df['Client']!='test') & (df['Client']!=', ') & (df['Client']!=', MA  ')]
    
    return df


def customer_clean(df, deceased):
    
    #create dataframe with just customer names and their email addresses
    customers = df[~df['Client'].isna()]
    customers = customers[(customers['Client'].str.contains(',')) & (~customers['Client'].str.contains('\d'))][['Client', 'Contact']]
    customers.rename(columns={'Contact':'Email'}, inplace=True)
    
    # create columns 
    customers['Address'] = ''
    customers['Phone'] = ''
    customers['Dog'] = ''
    customers['Deceased Pets'] = ''
    customers['Breed'] = ''
    customers['Dog Gender'] = ''
    
    #call function to populate 
    customers = match_info_to_name(df, customers, deceased)
    customers.reset_index(drop=True, inplace=True)
    
    return customers
    

def match_info_to_name(df, customers, deceased):
    
    #create list of clients
    names = list(customers['Client'])
    
    #initialize counter variable
    df.reset_index(drop=True, inplace=True)
    for i in range(len(df)):
        
        if not df.loc[i, ['Client']].isnull()['Client']:
            #if string in temp df is the name of a customer
            if df.loc[i, 'Client'] in names:
                current_client = df.loc[i, 'Client']
            
            #if string in the temp df is part of an address
            else:
                customers.loc[customers['Client'] == current_client, 'Address'] = customers.loc[customers['Client'] == current_client, 'Address'] + df.loc[i, 'Client']
                
                #check if there is a phone number in contact info
                if not df.loc[i, ['Contact']].isnull()['Contact']:
                    customers.loc[customers['Client'] == current_client, 'Phone'] = df.loc[i, 'Contact']
        
        elif not df.loc[i, ['Dog']].isnull()['Dog']: 
            
            dog_deceased = False
            if not deceased[deceased['Client']==current_client].empty:
                if df.loc[i, 'Dog'] in deceased.loc[deceased['Client']==current_client, 'Dog'].reset_index(drop=True)[0]:
                    dog_deceased = True
                    customers.loc[customers['Client'] == current_client, 'Deceased Pets'] = df.loc[i, 'Dog']

            if not dog_deceased:
                #is this the first dog
                if customers[customers['Client']==current_client].reset_index(drop=True)['Dog'].str.len()[0] < 1: #ugly, need to fix
                    customers.loc[customers['Client'] == current_client, 'Dog'] = df.loc[i, 'Dog']
                else:
                    customers.loc[customers['Client'] == current_client, 'Dog'] = customers.loc[customers['Client'] == current_client, 'Dog'] + ', ' + df.loc[i, 'Dog']

                if not df.loc[i, ['Breed']].isnull()['Breed']:
                    if customers[customers['Client']==current_client].reset_index(drop=True)['Breed'].str.len()[0] < 1:
                        customers.loc[customers['Client'] == current_client, 'Breed'] = df.loc[i, 'Breed']
                    else:
                        customers.loc[customers['Client'] == current_client, 'Breed'] = customers.loc[customers['Client'] == current_client, 'Breed'] + ', ' + df.loc[i, 'Breed']
                if not df.loc[i, ['Dog Gender']].isnull()['Dog Gender']:
                    if customers[customers['Client']==current_client].reset_index(drop=True)['Dog Gender'].str.len()[0] < 1:
                        customers.loc[customers['Client'] == current_client, 'Dog Gender'] = df.loc[i, 'Dog Gender']
                    else:
                        customers.loc[customers['Client'] == current_client, 'Dog Gender'] = customers.loc[customers['Client'] == current_client, 'Dog Gender'] + ', ' + df.loc[i, 'Dog Gender']
            
    return customers

@st.cache_data
def Clean_Customer_Data(file, deceased):

    df = pd.read_excel(file)
    df = clean_df(df)
    df = customer_clean(df, deceased)
    return df