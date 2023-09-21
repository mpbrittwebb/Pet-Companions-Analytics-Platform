import numpy as np
import pandas as pd
import streamlit as st

def pre_process(df):
    
    df.drop(axis=1, labels=['Unnamed: 0', 'Unnamed: 3', 'Unnamed: 11', 'Unnamed: 13', 
                            'Unnamed: 16', 'Unnamed: 18', 'Unnamed: 19', 'Unnamed: 20', 
                            'Unnamed: 23', 'Unnamed: 24', 'Unnamed: 26', 'Unnamed: 28'], 
            inplace=True)
    df.dropna(how='all', axis=0, inplace=True)
    df.dropna(how='all', axis=1, inplace=True)
    
    df.rename(columns={'Unnamed: 4':'Dog', 'Unnamed: 7':'Client'}, inplace=True)
    
    df = df[(df['Client']!='Lenny Snyderman')]
    
    df.reset_index(drop=True, inplace=True)
    
    return df

def customer_info(df):
    
    #create dataframe with just customer names and their email addresses
    customers = df[~df['Client'].isna()]
    customers = customers[(customers['Client'].str.contains(',')) & (~customers['Client'].str.contains('\d')) & (customers['Client'].str.contains(pat = '[a-zA-Z]'))][['Client']]
    # create columns 
    customers['Dog'] = ''
    
    #call function to populate 
    customers = match_info_to_name(df, customers)
    customers = customers.drop_duplicates('Client')
    customers.reset_index(drop=True, inplace=True)
    
    return customers

def match_info_to_name(df, customers):
    
    #create list of clients
    names = list(customers['Client'])
    
    #initialize counter variable
    df.reset_index(drop=True, inplace=True)
    for i in range(len(df)):
        
        if not df.loc[i, ['Client']].isnull()['Client']:
                #if string in temp df is the name of a customer
                if df.loc[i, 'Client'] in names:
                    current_client = df.loc[i, 'Client']
        
        elif not df.loc[i, ['Dog']].isnull()['Dog']:    
            #is this the first dog
            if customers[customers['Client']==current_client].reset_index(drop=True)['Dog'].str.len()[0] < 1: #ugly, need to fix
                customers.loc[customers['Client'] == current_client, 'Dog'] = df.loc[i, 'Dog']
            else:
                customers.loc[customers['Client'] == current_client, 'Dog'] = customers.loc[customers['Client'] == current_client, 'Dog'] + ', ' + df.loc[i, 'Dog']
            
        ##WRITE SOMETHING TO REMOVE DECEASED DOGS
    return customers

@st.cache_data
def deceased_pets(file):
    df = pd.read_excel(file)
    df = pre_process(df)
    df = customer_info(df)
    return df