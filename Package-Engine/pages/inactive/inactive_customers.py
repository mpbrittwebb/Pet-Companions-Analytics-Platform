import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


st.cache_data
def find_inactive(sales_df, active):
    clients = sales_df.drop_duplicates('Client Name')[['Client Name']]
    client_names = list(clients['Client Name'])

    for client in client_names:
        last_visit = sales_df.loc[sales_df['Client Name']==client, 'Date'].max().date()
        clients.loc[clients['Client Name']==client, 'Last Visit'] = last_visit
        clients.loc[clients['Client Name']==client, 'Total'] = sum(sales_df.loc[sales_df['Client Name']==client, 'Total'])

        if last_visit <= date.today() - relativedelta(years=2):
            clients.loc[clients['Client Name']==client, 'Visit Category'] = '2+ years'
        elif last_visit <= date.today() - relativedelta(years=1): 
            clients.loc[clients['Client Name']==client, 'Visit Category'] = '1 - 2 years'
        elif last_visit <= date.today() - relativedelta(months=6): 
            clients.loc[clients['Client Name']==client, 'Visit Category'] = '6 - 12 months'
        else:
            clients.loc[clients['Client Name']==client, 'Visit Category'] = 'active'
        
        if len(active[active['Client']==client]) >= 1: 
            clients.loc[clients['Client Name']==client,'Email'] = active.loc[active['Client']==client, 'Email'].reset_index(drop=True)[0]
            clients.loc[clients['Client Name']==client,'Phone'] = active.loc[active['Client']==client, 'Phone'].reset_index(drop=True)[0]
            clients.loc[clients['Client Name']==client,'Dog'] = active.loc[active['Client']==client, 'Dog'].reset_index(drop=True)[0]
            clients.loc[clients['Client Name']==client,'Deceased Pets'] = active.loc[active['Client']==client, 'Deceased Pets'].reset_index(drop=True)[0]


    clients.sort_values('Last Visit', inplace=True)
    clients.reset_index(drop=True, inplace=True)
    clients.rename(columns={'Client Name':'Client'}, inplace=True)
    clients = clients[clients['Visit Category']!='active']
    return clients[['Client', 'Email', 'Phone', 'Dog', 'Deceased Pets', 'Last Visit', 'Visit Category', 'Total']]

st.cache_data
def choose_level(category, inactive_df):

    if category == '2 years':
        inactive_df = inactive_df[inactive_df['Visit Category'] == '2+ years']
    elif category == '1 year':
        inactive_df = inactive_df[inactive_df['Visit Category'] == '1 - 2 years']
    elif category == 'all':
        inactive_df.sort_values(['Visit Category', 'Total'], ascending=False, inplace=True)
        inactive_df.reset_index(drop=True, inplace=True)
        return inactive_df
    else:
        inactive_df = inactive_df[inactive_df['Visit Category'] == '6 - 12 months']
            
    inactive_df = inactive_df.sort_values('Total', ascending=False)
    inactive_df.reset_index(drop=True, inplace=True)
    inactive_df.fillna(' ', inplace=True)
    return inactive_df