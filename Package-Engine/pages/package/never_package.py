import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import streamlit as st

def customer_info(df, customers_df):
    customer_names = list(customers_df['Client'])
    
    df['Email'] = ''
    df['Phone'] = ''
    df['Dog'] = ''
    
    names = list(df['Client'])
    
    for name in names:
        if name in customer_names:
                                                                                                              #fix for weird bug where names match but says it doesn't contain name
            df.loc[df['Client']==name, 'Email'] = customers_df.loc[(customers_df['Client'].str.contains(name))|(customers_df['Client'] ==name), 'Email'].reset_index(drop=True)[0]
            df.loc[df['Client']==name, 'Phone'] = customers_df.loc[(customers_df['Client'].str.contains(name))|(customers_df['Client'] ==name), 'Phone'].reset_index(drop=True)[0]
            df.loc[df['Client']==name, 'Dog'] = customers_df.loc[(customers_df['Client'].str.contains(name))|(customers_df['Client'] ==name), 'Dog'].reset_index(drop=True)[0]
            
    return df[['Client', 'Email', 'Phone', 'Dog', 'Last Daycare Visit', 'Daycare Visits Last 180 Days', 'Daycare Revenue Last 180 Days']]

@st.cache_data
def no_package_ever(sales_df, remaining_packages, empty_packages, customers_df):
    
    #get list of people who have packages
    clients_with_package = list(remaining_packages['Client'])
    
    #get list of people who have purchased packages and don't currently have one
    clients_with_empty_package = list(empty_packages['Client'])
    
    #all clients with package this year
    all_package = clients_with_empty_package + clients_with_package
    
    #all clients from this year in sales
    never_package = sales_df[~sales_df['Client Name'].isin(all_package)]
    never_package = never_package[(never_package['Code']=='DAYCARE')|(never_package['Code']=='DAYCARE*')]#.isin(['DAYCARE', 'DAYCARE*'])]
    
    #initialize df that will hold info for people who have never bought
    total_never = never_package.drop_duplicates('Client Name')[['Client Name']]
    total_never.rename(columns={'Client Name':'Client'}, inplace=True)
    names = list(total_never['Client'])
    
    since = datetime.today() - timedelta(days=180)
    for name in names:
        total_never.loc[total_never['Client'] == name, 'Daycare Visits Last 180 Days'] = sum(never_package[(never_package['Client Name'] == name) & (never_package['Date']> since)]['Quantity'])
        total_never.loc[total_never['Client'] == name, 'Daycare Revenue Last 180 Days'] = sum(never_package[(never_package['Client Name'] == name) & (never_package['Date']> since)]['Total'])
        total_never.loc[total_never['Client'] == name, 'Last Daycare Visit'] = max(never_package[(never_package['Client Name'] == name)]['Date'])
        
    total_never.sort_values('Daycare Visits Last 180 Days', ascending=False, inplace=True)
    total_never.reset_index(drop=True, inplace=True)
    
    total_never = customer_info(total_never, customers_df)
    return total_never
    
    