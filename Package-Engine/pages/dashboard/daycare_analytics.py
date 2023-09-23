import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import streamlit as st


def by_day(df):
    
    days = df.drop_duplicates('Date')[['Date']]
    days['Day of Week'] = ''
    days['Dogs'] = 0
    
    for day in list(days['Date']):
        days.loc[days['Date']==day, 'Dogs'] = len(df[df['Date']==day])
        days.loc[days['Date']==day, 'Day of Week'] = day.strftime('%A')
        
    return days


def daycare_visits_graph(unit, quantity, df):
    
    if unit=='Day':
        df = df[(df['Date']<date.today()) & (df['Date'] > date.today() + timedelta(days=-(quantity+1)))]
        table = df
        table.reset_index(drop=True, inplace=True)
        
    elif unit == 'Week':
        table=pd.DataFrame(columns=['Week', 'Dogs'])
        
        for i in range(quantity):
            end = date.today() + timedelta(-(1+7*i))
            start = date.today() + timedelta(-(8+7*i))
            table.loc[i, 'Week'] = start
            table.loc[i, 'Dogs'] = sum(df[(df['Date']>=start) & (df['Date']<end)]['Dogs'])
            
    elif unit == 'Month':
        table=pd.DataFrame(columns=['Month', 'Dogs'])
        df['Date'] = df['Date'].apply(lambda x: x.strftime('%m-%Y'))
        df.reset_index(drop=True, inplace=True)
        
        for i in range(quantity):
            month = (date.today() - relativedelta(months=i)).strftime('%m-%Y')
            table.loc[i, 'Month'] = month
            table.loc[i, 'Dogs'] = sum(df[df['Date']==month]['Dogs'])
            
    return table

st.cache_data
def visits_analysis(daycare_report, unit, quantity):
    daycare_report = by_day(daycare_report)
    table = daycare_visits_graph(unit, quantity, daycare_report)
    return table
