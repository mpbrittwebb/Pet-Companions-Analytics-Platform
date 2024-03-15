import pandas as pd
import numpy as np
import streamlit as st

st.cache_data
def process_daycare(file):
    daycare = pd.read_excel(file, header=5)
    daycare = daycare.filter(regex='^(?!Unnamed)')
    daycare.dropna(inplace=True)
    daycare['Date'] = daycare['In Date']
    daycare['Dog'] = daycare['Customer'].apply(lambda x: x.split(':')[1])
    daycare['Customer'] = daycare['Customer'].apply(lambda x: x.split(':')[0])
    daycare = daycare[['Date', 'Customer', 'Dog', 'In Date', 'Out Date']]
    daycare['Daycare'] = 1
    daycare['board_arrive'] = 0
    daycare['board_continue'] = 0
    daycare['board_depart'] = 0

    return daycare

st.cache_data
def process_boarding(file):

    boarding = pd.read_excel(file, header=5)
    boarding = boarding.filter(regex='^(?!Unnamed)')
    boarding.dropna(inplace=True)
    boarding['Date'] = boarding['In Date']
    boarding['Dog'] = boarding['Customer'].apply(lambda x: x.split(':')[1])
    boarding['Customer'] = boarding['Customer'].apply(lambda x: x.split(':')[0])
    boarding = boarding[['Date', 'Customer', 'Dog', 'In Date', 'Out Date']]

    boarding['In Date'] = pd.to_datetime(boarding['In Date'])
    boarding['Out Date'] = pd.to_datetime(boarding['Out Date'])

    # Create a new DataFrame to store the expanded rows
    expanded_rows = []

    # Iterate over each row in the original DataFrame
    for _, row in boarding.iterrows():
        # Generate a date range between 'In Date' and 'Out Date' inclusive
        date_range = pd.date_range(row['In Date'], row['Out Date'], freq='D')
        
        # Create a new row for each date in the range
        for date in date_range:
            new_row = row.copy()
            new_row['Date'] = date
            expanded_rows.append(new_row)
            
    # Create a new DataFrame from the list of expanded rows
    expanded_boarding = pd.DataFrame(expanded_rows)

    # Reset index to get a clean index for the new DataFrame
    expanded_boarding.reset_index(drop=True, inplace=True)

    return expanded_boarding

st.cache_data
def combine_data(daycare, boarding):
    df = pd.concat([daycare, boarding])
    df.sort_values('Date', inplace=True)
    df.fillna(0, inplace=True)
    df['Daycare'] = df['Daycare'].astype(int)

    return df