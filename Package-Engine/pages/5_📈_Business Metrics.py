import streamlit as st
import pandas as pd
from datetime import date, timedelta
import plotly.express as px
from pages.package.daycare_report import daycare_reporting
from pages.dashboard.daycare_analytics import visits_analysis


# Page setting
st.set_page_config(layout="wide")

st.title("Business Analytics")
st.header('Purpose:')

st.text('Quickly analyze key business metrics to understand business performance.')

daycare_report_df = None

st.subheader('Step 1: Login to KC')
st.text("1. Login to Kennel Connection using web access")

st.subheader("Step 2: Select the metric to examine")
options = st.selectbox('Pick a metric to examine', ('None', 'Daycare Visits'))

if options == 'Daycare Visits':

    st.subheader("Step 3: Daycare Reporting")
    st.text("1. Navigate to Daycare->Reports->Weekly Report") 
    st.text("2. Select view as 'Excel'." )
    st.text("3. Set Start Date to before date you want to analyze (2 years is recommended)")
    st.text("4. Set End Date to today now")
    st.text("5. Click okay to export the file ")
    st.text("6. Upload 'DaycareWeeklyReport.xls'")

    daycare_report_file = st.file_uploader(" Upload 'DaycareWeeklyReport.xls'")
    if not daycare_report_file == None: 
        st.success(f"successfully uploaded {daycare_report_file.name}!")
        daycare_report_df = daycare_reporting(daycare_report_file)

        unit = st.selectbox('Pick a unit of time', ('None', 'Day', 'Week', 'Month'))
        
        if unit != 'None':
            quantity = st.number_input(f'How many {unit.lower()}s would you like to look back?')
            
            if quantity >=1:
                table = visits_analysis(daycare_report_df, unit, int(quantity))

                fig = px.line(table, x=unit, y="Dogs", title=f'Daycare Visits by {unit}', markers=True)
                st.plotly_chart(fig, use_container_width=True)

                

            


        # fig = px.line(daycare_report_df, x=df[], y="lifeExp", title='Life expectancy in Canada')
        # fig.show()








