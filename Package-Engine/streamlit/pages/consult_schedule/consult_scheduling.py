import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta, date
from pages.consult_schedule.boarding_report import boarding

def bookings(daycare_df, future_days, boarders):
    
    past = past_bookings(daycare_df)
    
    daycare_df = daycare_df[(daycare_df['Date']>date.today())&(daycare_df['Date']<=date.today()+timedelta(days=future_days))]
    schedule = pd.DataFrame()
    schedule['Day of the Week'] = ''
    schedule['Date'] = ''
    schedule['Scheduled Daycare'] = ''
    schedule['Avg Daycare Dogs over Last 4 Weeks'] = 0
    schedule['Scheduled Boarders'] = 0
    schedule['Avg Boarding Dogs over Last 4 Weeks'] = 0
    
    for i in range(future_days):
        day = date.today() + timedelta(days=i+1)
        schedule.loc[i, 'Date'] = day
        schedule.loc[i, 'Day of the Week'] = day.strftime('%A')
        schedule.loc[i, 'Scheduled Daycare'] = len(daycare_df[daycare_df['Date']==day])
        schedule.loc[i, 'Avg Daycare Dogs over Last 4 Weeks'] = past.loc[past['Day of Week']==day.strftime('%A'), 'Average Visits'].reset_index(drop=True)[0]
        schedule.loc[i, 'Avg Boarding Dogs over Last 4 Weeks'] = boarders.loc[boarders['Date'] == day, 'Average Boarders'].reset_index(drop=True)[0]
        schedule.loc[i, 'Scheduled Boarders'] = boarders.loc[boarders['Date'] == day, 'Boarders'].reset_index(drop=True)[0]
        
    return schedule[['Day of the Week', 'Date', 'Scheduled Daycare', 'Avg Daycare Dogs over Last 4 Weeks', 'Scheduled Boarders', 'Avg Boarding Dogs over Last 4 Weeks']]
        

def past_bookings(daycare_df):
    daycare_df = daycare_df[(daycare_df['Date']<=date.today())&(daycare_df['Date']>=date.today()+timedelta(days=-27))]

    past = pd.DataFrame()
    past['Day of Week'] = ''
    past['Average Visits'] = 0

    for i in range(8):
        if i == 0: pass
        else:
            day = date.today() + timedelta(days=i) 
            past.loc[i, 'Day of Week'] = day.strftime('%A')
            past.loc[past['Day of Week'] == day.strftime('%A'), 'Average Visits'] = len(daycare_df[daycare_df['Day of Week'] == day.strftime('%A')])/4
    return past