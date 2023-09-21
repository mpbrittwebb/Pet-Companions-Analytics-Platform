import streamlit as st
import pandas as pd
from datetime import date, timedelta
from pages.package.daycare_report import daycare_reporting
from pages.consult_schedule.consult_scheduling import bookings
from pages.consult_schedule.boarding_report import boarding

daycare_report_df = None
consult_scheduling_df = None
boarding_report_file = None

st.title("Consult Scheduling Helper")

st.header('Purpose:')
st.text('This tool is meant to help with scheduling new dogs for the first visit.')
st.text('Specify how soon you would like the new dog to come in and then run the report')
st.text('You will see bookings already made and the average booking count by day of the week')
st.text('from the last month of data.')

st.header('Instructions:')

st.subheader('Step 1: Login to KC')
st.text("1. Login to Kennel Connection using web access")


st.subheader("Step 2: Boarding Reporting")
st.text("1. Navigate to Boarding->Reports->Occupancy->Occupancy") 
st.text("2. Select view as 'Excel'." )
st.text("3. Set Start Date to 2 months ago")
st.text("4. Set End Date to 4 weeks from now")
st.text("5. Click okay to export the file ")
st.text("4. Upload 'BoardingOccupancy.xls'")

boarding_report_file = st.file_uploader(" Upload 'BoardingOccupancy.xls'")
if not boarding_report_file == None: 
    st.success(f"successfully uploaded {boarding_report_file.name}!")
    boarding_report_df = boarding(boarding_report_file)


st.subheader("Step 3: Daycare Reporting")
st.text("1. Navigate to Daycare->Reports->Weekly Report") 
st.text("2. Select view as 'Excel'." )
st.text("3. Set Start Date to 2 months ago")
st.text("4. Set End Date to 4 weeks from now")
st.text("5. Click okay to export the file ")
st.text("4. Upload 'DaycareWeeklyReport.xls'")

daycare_report_file = st.file_uploader(" Upload 'DaycareWeeklyReport.xls'")
if not daycare_report_file == None: 
    st.success(f"successfully uploaded {daycare_report_file.name}!")
    daycare_report_df = daycare_reporting(daycare_report_file)


st.subheader("Step 3: Show Tables")
st.text('1. Specify how many future days you would like to see.')

limit = st.number_input('How many days ahead would you like to look?')
if limit < 1:
    st.warning('Please input a number greater than or equal to 1', icon="⚠️")
else:
    consult_scheduling_df = bookings(daycare_report_df, int(limit), boarding_report_df)

st.text("2. Press 'Run Analysis'")

if st.button('Run Analysis'):
    st.dataframe(consult_scheduling_df)

    st.subheader('Step 4: Download File if wanted')
    st.text('Press Download First Visit')
    csv = consult_scheduling_df.to_csv().encode('utf-8')
    st.download_button(label='Download First Visit', data=csv, 
        file_name=f'first_visit_analysis_{str(date.today())}.csv', mime='text/csv')









    