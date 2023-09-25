import streamlit as st
import pandas as pd
from pages.inactive.inactive_customers import choose_level, find_inactive
from pages.package.sales import sales_preprocess
from pages.package.cleaning_deceased_pets import deceased_pets
from pages.package.customer_data import Clean_Customer_Data
from datetime import date

sales_df = None
inactive_df = None
deceased = None
customer_df = None
inactive_category_df = None

st.title("Inactive Member Search")

st.header('Purpose:')
st.text('This tool is meant to find once high-frequency members who have')
st.text('since become inactive.')

st.header('Instructions:')

st.subheader('Step 1: Login to KC')
st.text("1. Login to Kennel Connection using web access")

st.subheader("Step 2: Deceased Pets")
st.text("1. Navigate to Reports->Lists->Deceased Pets") 
st.text("2. Select view as 'Excel'." )
st.text("3. Click okay to export the file ")
st.text("4. Upload 'DeceasedPets.xls'")

deceased_file = st.file_uploader(" Upload 'DeceasedPets.xls'")
if not deceased_file == None: 
    st.success(f"successfully uploaded {deceased_file.name}!")
    deceased = deceased_pets(deceased_file)


st.subheader("Step 3: Customer Data")
st.text("1. Navigate to Reports->Lists->Customer List") 
st.text("2. Select view as 'Excel'." )
st.text("3. Select Print Customers as 'Active") 
st.text("4. Click okay to export the file ")
st.text("5. Upload 'CustomerList.xls'")

customer_file = st.file_uploader(" Upload 'CustomerList.xls'")
if not customer_file == None: 
    st.success(f"successfully uploaded {customer_file.name}!")
    customer_df = Clean_Customer_Data(customer_file, deceased)


st.subheader('Step 4: Sales Data')
st.text("1. Navigate to Reports->Revenue->Sales Details For(Excel)") 
st.text("2. Select view as 'Excel'." )
st.text("3. Change Start Date to 3 years ago.") 
st.text("4. Keep End Date as today.")
st.text("5. Click okay to export the file ")
st.text("6. Upload 'SalesDetailsExportable.xls'")

sales_file = st.file_uploader(" Upload 'SalesDetailsExportable.xls'")
if not sales_file == None: 
    st.success(f"successfully uploaded {sales_file.name}!")
    sales_df = sales_preprocess(sales_file)

    st.subheader('Step 3: Select a category of inactive customer')
    st.text('1. Select the category of inactivity you would like to examine.')
    st.text('(this might take a few seconds)')

    category = st.selectbox('Select a category', ('None', '6 - 12 Months', '1 year', '2 years', 'all'))
    if (category != None):
        inactive_df = find_inactive(sales_df, customer_df)
        

    st.subheader('Step 4: Press Run Analysis')
    if st.button('Run Analysis'):
        st.text('Please note that blank rows are the result of missing data.')
        st.text('We do not have a lot of the data of old customers (or at least here).')
        st.text('Deceased pets would only appear for active customers.')
        
        inactive_category_df = choose_level(category, inactive_df)
        st.dataframe(inactive_category_df)

        st.subheader('Step 5: Download Report')
        st.text("Click the button to download this report. Set category to all if you want")
        st.text('a full report.')

        if st.button('Download Report'):
            csv = inactive_category_df.to_csv().encode('utf-8')
            st.download_button(label='Download inactive customers', data=csv, 
                                    file_name=f'inactive_customer_analysis_{str(date.today())}.csv', mime='text/csv')
