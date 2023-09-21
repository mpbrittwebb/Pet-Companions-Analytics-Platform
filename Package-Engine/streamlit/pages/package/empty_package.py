import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
from datetime import timedelta
import streamlit as st

#find how many packages of each type a user has purchased
def find_packages(df):
    
    #Table containing package purchase info
    packages = df[df['Code'].str.contains('daycare')]
    packages = packages[['Client Name', 'Date', 'Code', 'Quantity', 'Each', 'Total']].reset_index(drop=True)
    
    #initialize df to hold all info
    total = packages[['Client Name']].drop_duplicates()
    
    #sum totals
    for name in list(total['Client Name']):
        days_since = datetime.today() - timedelta(days=180)
        total.loc[total['Client Name'] == name, '10 Half Days Packages'] = sum(packages[(packages['Client Name'] == name) & (packages['Date']> days_since) & ((packages['Code'] == '10 half days daycare')|(packages['Code'] == '10 half daycare'))]['Quantity']) 
        total.loc[total['Client Name'] == name, '10 Full Days Packages'] = sum(packages[(packages['Client Name'] == name) & (packages['Date']> days_since) & ((packages['Code'] == '10 day daycare')|(packages['Code'] == '10 days daycare 2 dogs')|(packages['Code'] == '10 full daycare'))]['Quantity']) 
        total.loc[total['Client Name'] == name, '20 Half Days Packages'] = sum(packages[(packages['Client Name'] == name) & (packages['Date']> days_since) & (packages['Code'] == '20 half daycare')]['Quantity'])
        total.loc[total['Client Name'] == name, '20 Full Days Packages'] = sum(packages[(packages['Client Name'] == name) & (packages['Date']> days_since) & (packages['Code'] == '20 full daycare')]['Quantity'])
        total.loc[total['Client Name'] == name, '30 Half Days Packages'] = sum(packages[(packages['Client Name'] == name) & (packages['Date']> days_since) & (packages['Code'] == '30 half daycare')]['Quantity'])
        total.loc[total['Client Name'] == name, '30 Full Days Packages'] = sum(packages[(packages['Client Name'] == name) & (packages['Date']> days_since) & (packages['Code'] == '30 full daycare')]['Quantity'])
        total.loc[total['Client Name'] == name, '40 Half Days Packages'] = sum(packages[(packages['Client Name'] == name) & (packages['Date']> days_since) & (packages['Code'] == '40 half daycare')]['Quantity'])
        total.loc[total['Client Name'] == name, '40 Full Days Packages'] = sum(packages[(packages['Client Name'] == name) & (packages['Date']> days_since) & (packages['Code'] == '40 full daycare')]['Quantity'])
        total.loc[total['Client Name'] == name, 'Last Purchased Package'] = max(packages[packages['Client Name'] == name]['Date'])
    
        days_since = datetime.today() - timedelta(days=180)
        total.loc[total['Client Name'] == name, 'Sales Volume Last 180 Days'] = sum(df[(df['Date']> days_since)&(df['Client Name'] == name)]['Total'])
        
        total.loc[total['Client Name'] == name, 'Total'] = sum(packages[packages['Client Name'] == name]['Total'])
        
    total.rename(columns={'Client Name':'Client'}, inplace=True)
    return total


def customer_info(df, customers_df):
    customer_names = list(customers_df['Client'])
    
    df['Email'] = ''
    df['Phone'] = ''
    df['Dog'] = ''
    
    names = list(df['Client'])
    
    for name in names:
        if name in customer_names:
            df.loc[df['Client']==name, 'Email'] = customers_df.loc[customers_df['Client'].str.contains(name), 'Email'].reset_index(drop=True)[0]
            df.loc[df['Client']==name, 'Phone'] = customers_df.loc[customers_df['Client'].str.contains(name), 'Phone'].reset_index(drop=True)[0]
            df.loc[df['Client']==name, 'Dog'] = customers_df.loc[customers_df['Client'].str.contains(name), 'Dog'].reset_index(drop=True)[0]
        
    return df[['Client', 'Email', 'Phone', 'Dog', '10 Half Days Packages', '10 Full Days Packages', '20 Half Days Packages', '20 Full Days Packages', '30 Half Days Packages', '30 Full Days Packages', '40 Half Days Packages', '40 Full Days Packages', 'Last Purchased Package', 'Sales Volume Last 180 Days']]


#find people who have purchased a package before but do not have any active ones
@st.cache_data
def empty_packages(sales, remaining_packages, customers_df):
    
    #load people who have bought packages
    packages = find_packages(sales)
    
    #generate list of clients with days left in a package
    remaining_packages_names = list(remaining_packages['Client'])
    
    #find people who have bought packages this year but don't have one right now
    no_packages = packages[~packages[['Client']].isin(remaining_packages_names)]
    
    #drop null rows
    no_packages_names = list(no_packages.dropna(how='all')['Client'])
    
    no_packages = packages[packages['Client'].isin(no_packages_names)]
    
    no_packages = no_packages.sort_values('Total', ascending=False)
    no_packages.reset_index(drop=True, inplace=True)
    
    no_packages = customer_info(no_packages, customers_df)
    
    return no_packages