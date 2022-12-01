import streamlit as st
from database_func import *
import pandas as pd 
import datetime as dt
today = dt.datetime.today()

st.set_page_config(layout='wide')

df = get_transactions()

df = pd.DataFrame.from_records(df, columns=[
    'key', 
    'PAY_PERIOD',
    'GRANT_NUMBER', 
    'AWARD_NUMBER', 
    'PROJECT_NUMBER',
    'ACTIVITY', 
    'ADDED', 
    'EMPLOYEE_ID', 
    'NAME', 
    'RANK', 
    'HOURS_WORK', 
    'DATE_WORKED', 
    'TOTAL_PAY', 
    'NOTES'
    ])


st.sidebar.header('Filter Information')
pay_period = st.sidebar.multiselect(
    'Select 2023 Pay Period:',
    options=df['PAY_PERIOD'].unique(),
    default=df['PAY_PERIOD'].unique()
)

grant_num = st.sidebar.multiselect(
    'Select Grant Number:',
    options=df['GRANT_NUMBER'].unique(),
    default=df['GRANT_NUMBER'].unique()
)

project_num = st.sidebar.multiselect(
    'Select Project:',
    options=df['PROJECT_NUMBER'].unique(),
    default=df['PROJECT_NUMBER'].unique()
)

award_num = st.sidebar.multiselect(
    'Award Number:',
    options=df['AWARD_NUMBER'].unique(),
    default=df['AWARD_NUMBER'].unique()
)

activity_num = st.sidebar.multiselect(
    'Select Activity:',
    options=df['ACTIVITY'].unique(),
    default=df['ACTIVITY'].unique()
)


st.sidebar.subheader('Remove Record')

with st.sidebar.form('Remove', True):
    tran_id = st.text_input(
        'Transaction Id (required)')
    remove = st.form_submit_button('Remove', )
    if remove:
        delete_transaction(tran_id)
        st.success('Transaction deleted.')

filterd_df = df.query(
    "PAY_PERIOD == @pay_period & GRANT_NUMBER == @grant_num & PROJECT_NUMBER == @project_num & ACTIVITY == @activity_num & AWARD_NUMBER == @award_num"
)

st.dataframe(filterd_df)

csv = filterd_df.to_csv()

st.download_button(
        label='Download Dataframe', 
        data=csv, 
        file_name='session.csv',
        mime='text/csv'
        )

amount = round(filterd_df['TOTAL_PAY'].sum(), 2)
st.metric('Total Amount', f'${amount}')