import streamlit as st
import pandas as pd
import datetime as dt
import openpyxl

if "key" not in st.session_state:
    st.session_state.key = pd.DataFrame(columns=[
            'Name',
            'Rank', 
            'Hourly Pay', 
            'Pay Type', 
            'Hours Worked', 
            'Longevity Incent', 
            'Job Incent', 
            'College Incent',
            'All Incentives',
            'Pay w/o Incent', 
            'Total Pay'
    ], index=[0])

today = dt.date.today()
### Defining the Databse of Ranks and Pay
data = pd.DataFrame({
    'Rank': ['Deputy Chief','Division Chief', 'Battalion Chief' ,'Lieutenant', 'Driver', 'Firefighter/Paramedic (3 years +)', 'Firefighter/Paramedic (2-3 years)', 'Firefighter/Paramedic (1-2 years)', 'Firefighter/Paramedic-Prob', 'Paramedic Single Role', 'AEMT/Probation', 'EMT/Probation','E.M.T. OOR','Private (+ 3 years)', 'Private II_Lateral', 'Private II (2-years)', 'Private II (1-year)', 'Recruit'],
    '24 Hour Pay': [43.5838, 36.4042, 32.2178, 25.1008, 22.1089, 22.6699, 21.8940, 20.4229, 19.3638, 26.0011, 16.1402, 15.4533, 22.6612, 20.7983, 20.0863, 20.0863, 18.7363, 13.1212],
    '8 Hour Pay':  [61.0174, 50.9659, 45.1049, 35.1411, 30.9525, 31.7379, 30.6516, 28.5920, 27.1093, 26.0011, 22.5963, 21.6346, 31.7256, 29.1176, 28.1209, 28.1209, 26.2309, 18.3696],

})
#### Streamlit App LAyout and web functionality code below ####

with st.container():
    COL1,COL2 = st.columns((2))

    with COL1:
        
        st.header('MFD Telestaff Payroll Calculator')
        st.markdown('_presented by..._')
        st.markdown('##### The MFD TeleStaff Team')

    with COL2:
        st.image('assets/mfd_logo.jpeg', width=250)
        pass

with st.form('form'):

    # Defining from the db the rank
    selected_rank = st.selectbox('Select Rank', data['Rank'])
    # Defining the pay selector and option "24 hours Rate" or "8 hours rate"
    selected_pay_rate = st.selectbox('Hourly Pay Rate', ['24 Hour Pay', '8 Hour Pay'])
    # Defining the pay selector and option "Time and A Half" or "Straight Time"
    overtime_type = st.selectbox('Type of Pay', ['Time and a Half', 'Straight Time'])
    # Text input box for mannually entering floats
    longevity = st.number_input(
        'Longevity Incentive.', 
        min_value=0.0,
        max_value=1.9999,
        step=1e-4,
        format="%.4f")
    # Text input box for mannually entering floats
    job_incentive = st.number_input(
        'Insert Job Incentive Pay', 
        min_value=0.0,
        max_value=1.9999,
        step=1e-4,
        format="%.4f")
    # Text input box for mannually entering floats
    college_inc = st.number_input(
        'Insert College Incentive', 
        min_value=0.0,
        max_value=1.9999,
        step=1e-4,
        format="%.4f")
    # Text inout how many hours they work
    hours_works = st.number_input('Hours Worked (Decimal Value)',
        step=25e-2,
    format="%.2f")



    hourly_pay = data[data['Rank'] == selected_rank]
    hourly_pay = hourly_pay[selected_pay_rate].values
    hourly_pay = hourly_pay[0]

    def determine_time_and_half(overtime_type=overtime_type):
        if overtime_type == 'Time and a Half': 
            overtime_rate = 1.5
        else:
            overtime_rate = 1.0
        return overtime_rate

    hourly_rate = determine_time_and_half()

    def longevity_inc():
        return round(longevity*hours_works*hourly_rate, 2)

    def job_inc():
        return round(job_incentive*hours_works*hourly_rate, 2)

    def coll_inc():
        return round(college_inc*hours_works*hourly_rate, 2)


        


    longevity = longevity_inc()
    job = job_inc()
    coll = coll_inc()

    incent = round(longevity+job+coll, 2)
    calc_pay = round(hours_works*hourly_pay*hourly_rate, 4)

    total_pay = round(incent + calc_pay, 2)

    name = st.text_input('Add ID or Name (optional)')
    '---'
    run = st.form_submit_button('Calculate/Add to Session List')
    '---'
    col1, col2, col3 = st.columns(3)

    col1.metric(' Selected Rank', value=selected_rank)
    col2.metric('Base Pay', value=f'${hourly_pay}')
    col3.metric('Hours', value=hours_works)
    col1.metric('Total Incentive Pay', value=f'${incent}')
    col2.metric('Pay w/o Incentives', value=f'${calc_pay}')
    col3.metric(f' Total Pay', value=f'${total_pay}')

    new_df = pd.DataFrame({
            'Name': name, 
            'Rank': selected_rank, 
            'Hourly Pay': hourly_pay, 
            'Pay Type': hourly_rate, 
            'Hours Worked': hours_works, 
            'Longevity Incent': longevity, 
            'Job Incent': job, 
            'College Incent': coll,
            'All Incentives': incent,
            'Pay w/o Incent': calc_pay, 
            'Total Pay': total_pay
            }, index=[0])

if run:
    st.session_state.key = pd.concat([st.session_state.key, new_df], axis=0)
    st.dataframe(st.session_state.key)

st.write(f"Total Rows: {st.session_state.key.shape[0]}")
'---'

file_name = st.text_input('file Name (optional)') 

def save_download_sessiom():
    df = st.session_state.key
    if file_name == '':
        df.to_excel('session.xlsx')
    else:
        df.to_excel(f'{file_name}.xlsx')

st.button('Save Session', on_click=save_download_sessiom())
