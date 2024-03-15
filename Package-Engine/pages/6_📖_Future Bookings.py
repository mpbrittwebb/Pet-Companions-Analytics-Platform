import streamlit as st
import pandas as pd
from datetime import date, timedelta
from pages.future_bookings.bookings import process_daycare, process_boarding, combine_data

st.title("Future Bookings")

st.subheader("Upload Uninvoiced booking daycare")

daycare_file = st.file_uploader(" Upload 'Uninvoiced daycare'", type=["xlsx", "xls"])
if not daycare_file == None: 
    st.success(f"successfully uploaded {daycare_file.name}!")
    daycare_df = process_daycare(daycare_file)

boarding_file = st.file_uploader("Upload Uninvoiced booking boarding", type=["xlsx", "xls"])
if not boarding_file == None: 
    st.success(f"successfully uploaded {boarding_file.name}!")
    boarding_df = process_boarding(boarding_file)


if st.button('Run Analysis'):
    
    table = combine_data(daycare_df, boarding_df)
    st.text('Press Download First Visit')
    csv = table.to_csv().encode('utf-8')
    st.download_button(label='Download Data', data=csv, 
        file_name=f'DailyHeadcount_{str(date.today())}.csv', mime='text/csv')