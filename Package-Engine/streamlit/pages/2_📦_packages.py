## Import libraries and functions ##
import streamlit as st
import pandas as pd
from datetime import datetime, date
from pages.package.clean_packages_outstanding import Outstanding_Packages
from pages.package.empty_package import empty_packages
from pages.package.customer_data import Clean_Customer_Data
from pages.package.never_package import no_package_ever
from pages.package.cleaning_deceased_pets import deceased_pets
from pages.package.sales import sales_preprocess
from pages.package.daycare_report import daycare_reporting



## Begin app ##

st.title("Package Engine Program")

st.header('Purpose:')
st.text('This tool is meant to increase the volume of package sales at pet companions. It ')
st.text('identifies three types of customers who might be interested in a package.')
st.text("")
st.text("1. Current package holders. These customers might be interested in renewing a")
st.text('package when it is low.')
st.text('')
st.text('2. Customers with empty packages. They have purchased a package in the last 180')
st.text('days but do not have an active package.')
st.text('')
st.text('3. Frequent customers with no package. They have not purchased a package in the')
st.text('last 180 days but come to Pet Companions frequently.')

st.header('Instructions: ')
st.subheader("Step 1: Login to KC")
st.text("1. Login to kennel connection using web access.")

## Initialize global dataframes ##
packages_left = None
sales_df = None
empty_package_df = None
never_package_df = None
deceased = None
customer_df = None
daycare_report_df = None

st.subheader("Step 2: Deceased Pets")
st.text("1. Navigate to Reports->Lists->Deceased Pets") 
st.text("2. Select view as 'Excel'." )
st.text("3. Click okay to export the file ")
st.text("4. Upload 'DeceasedPets.xls'")

deceased_file = st.file_uploader(" Upload 'DeceasedPets.xls'")
if not deceased_file == None: 
    st.success(f"successfully uploaded {deceased_file.name}!")
    deceased = deceased_pets(deceased_file)


st.subheader("Step 3: Daycare Reporting")
st.text("1. Navigate to Daycare->Reports->Weekly Report") 
st.text("2. Select view as 'Excel'." )
st.text("3. Set Start Date to 4 months before today")
st.text("4. Set End Date to 3 months after today")
st.text("5. Click okay to export the file ")
st.text("4. Upload 'DaycareWeeklyReport.xls'")

daycare_report_file = st.file_uploader(" Upload 'DaycareWeeklyReport.xls'")
if not daycare_report_file == None: 
    st.success(f"successfully uploaded {daycare_report_file.name}!")
    daycare_report_df = daycare_reporting(daycare_report_file)


st.subheader("Step 4: Existing Packages")

st.text("1. Navigate to Daycare->Reports->Daycare Packages Left.") 
st.text("2. Select view as 'Excel'." )
st.text("3. Leave Select Date as todays date.") 
st.text("4. Select Show by Date/ All as 'all'. ")
st.text("5. Click okay to export the file ")
st.text("6. Upload 'DaycarePackageDaysLeft.xlsx")

packages_left_file = st.file_uploader("6. Upload 'DaycarePackageDaysLeft.xlsx")

if packages_left_file is not None:
    st.success(f"successfully uploaded {packages_left_file.name}!")
    packages_left = pd.read_excel(packages_left_file)
    packages_left = Outstanding_Packages(packages_left_file, deceased, daycare_report_df)


st.subheader("Step 5: Customer Data")
st.text("1. Navigate to Reports->Lists->Customer List") 
st.text("2. Select view as 'Excel'." )
st.text("3. Select Print Customers as 'Active") 
st.text("4. Click okay to export the file ")
st.text("5. Upload 'CustomerList.xls'")

customer_file = st.file_uploader(" Upload 'CustomerList.xls'")
if not customer_file == None: 
    st.success(f"successfully uploaded {customer_file.name}!")
    customer_df = Clean_Customer_Data(customer_file)


st.subheader("Step 6: Sales Data")
st.text("1. Navigate to Reports->Revenue->Sales Details For(Excel)") 
st.text("2. Select view as 'Excel'." )
st.text("3. Change Start Date to 01/01/2023.") 
st.text("4. Keep End Date as today. ")
st.text("5. Click okay to export the file ")
st.text("6. Upload 'SalesDetailsExportable.xls'")

sales_file = st.file_uploader(" Upload 'SalesDetailsExportable.xls'")
if not sales_file == None: 
    st.success(f"successfully uploaded {sales_file.name}!")
    sales_df = sales_preprocess(sales_file)

    empty_package_df = empty_packages(sales_df, packages_left, customer_df)
    never_package_df = no_package_ever(sales_df, packages_left, empty_package_df, customer_df)



st.subheader("Step 7: Show Tables")
st.text('1. Please select the tables that you would like to view in the app')

options = st.multiselect('Table Options', ['Outstanding Packages','Empty Packages','Never Packages'])

if options != []:
    st.write('You selected:')
    for option in options:
        st.write(option)

st.text('2. Specify filter details if applicable')

package_limit = 0
if 'Outstanding Packages' in options:
    package_limit = st.number_input("Show packages under this many days left: ")

never_limit = 0
if 'Never Packages' in options:
    never_limit = st.number_input("Show this many top spenders with no package : ")

st.text("3. Press 'Run Analysis'")

if st.button('Run Analysis'):
    if options == []: st.warning('Please select a table', icon="⚠️")

    packages_left_limited = None
    if 'Outstanding Packages' in options:
        st.text('Outstanding Packages Dataframe:')
        packages_left_limited = packages_left[packages_left['Full Days'] + packages_left['Half Days'] < package_limit]
        st.dataframe(packages_left_limited)
    
    if 'Empty Packages' in options:
        st.text('Empty Packages Dataframe:')
        st.dataframe(empty_package_df)
   
    never_package_limit = None
    if 'Never Packages' in options:
        st.text('Never Packages Dataframe:')
        if never_limit >= 1:
            never_package_limit = never_package_df.head(int(never_limit))
            st.dataframe(never_package_limit)
        else: 
            st.warning('Please input a number greater than or equal to 1', icon="⚠️")

    st.text("4. Download files if wanted - you might have to rerun analysis if you want")
    st.text("to download multiple files")
    
    if 'Outstanding Packages' in options:
        csv = packages_left_limited.to_csv().encode('utf-8')
        st.download_button(label='Download Outstanding Packages', data=csv, 
                           file_name=f'outstanding_package_analysis_{str(date.today())}.csv', mime='text/csv')
    

    if 'Empty Packages' in options:
            csv = empty_package_df.to_csv().encode('utf-8')
            st.download_button(label='Download Empty Packages', data=csv, 
                            file_name=f'empty_package_analysis_{str(date.today())}.csv', mime='text/csv')
            
    if 'Never Packages' in options:
            csv = never_package_limit.to_csv().encode('utf-8')
            st.download_button(label='Download Never Packages', data=csv, 
                            file_name=f'never_package_analysis_{str(date.today())}.csv', mime='text/csv')
    
