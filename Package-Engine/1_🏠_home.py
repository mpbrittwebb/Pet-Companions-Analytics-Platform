import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Pet Companions Analytics",
    page_icon="🐾",
)

st.title('Pet Companions Internal Analytics Platform')

st.header('Purpose')
st.write('Welcome to the Pet Companions analytics page! This site exists to')
st.write('migrate current analytics from excel to python to make analytics at Pet Companions')
st.write('faster, easier to perform, and deliver more powerful insights.')

st.header('How to use it')
st.write('Select the tool you want to use in the sidebar. Take care to follow the directions in')
st.write('order to prevent errors. These programs might still have errors if there is a change to input')
st.write('file formatting. If you are certain that you have followed directions correctly reach out to')
st.write('Matthew Britt-Webb by phone at 617-852-6690 or over email at mpbrittwebb@u.northwestern.edu')