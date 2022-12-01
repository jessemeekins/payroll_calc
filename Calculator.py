import streamlit as st
import pandas as pd
import datetime as dt
from database_func import *

emp_list = get_all_employees()
transactions = get_transactions()
deta_pay_scale = get_payscale()

today = dt.date.today()

### Defining the Databse of Ranks and Pay
award_= ['130701', '130801']
activity_= [ 'Admin PT','Training', 'Staffing', 'USAR Backfill']
#### Streamlit App LAyout and web functionality code below ####
cost_centers = get_cost_centers()

with st.container():
    COL1,COL2 = st.columns((2))
    with COL1:
        st.header('MFD Telestaff Payroll Calculator')
        st.markdown('_presented by..._')
        st.markdown('##### The MFD TeleStaff Team')

    with COL2:
        st.image('assets/mfd_logo copy.png', width=250)
        pass

with st.sidebar:
    st.subheader("Search for Employee")
    employee_id = st.selectbox('Search Employee', sorted([emp["EMPLOYEE_ID"] for emp in emp_list], reverse=False))
    employee_information = get_employee(employee_id)

if 'payout' not in st.session_state:
    st.session_state.payout = 0.00

def update_payout(total_pay):
    st.session_state.payout += total_pay
st.subheader('Personnel Expense Logging')
col1, col2, col3, col4 = st.columns(4)

grant_number = col1.selectbox('Award Year', key='grant', options=[key for key in cost_centers])
award_number = col2.selectbox('Project Number', key='project', options=[value for value in cost_centers[grant_number]])
project_number = col3.selectbox('Funding Number', key='award', options=award_)
activity = col4.selectbox('Activity', key='activity', options=activity_)
                
col1, col2 = st.columns(2)
start_date = col1.date_input('Start Date', key='start_date')
end_date = col2.date_input('End Date', key='end_date')

rank = employee_information["RANK"]

hours_works = st.number_input('Hours Worked (Decimal Value)',
    step=25e-2,
    format="%.2f")

if activity == 'Admin PT':
    working_rank = 'Lieutenant'
    selected_pay_rate = '8 Hour Rate'
    overtime_type = 'Straight Time'
    long_inc = 0.0000
    job_inc = 0.0000
    college_inc = 0.0000
    hazard_inc = 0.0000

else:
    if employee_information["RANK"] == '':
        working_rank = st.selectbox('Working Rank',[rank["RANK"] for rank in deta_pay_scale])
    else:
        working_rank = employee_information["RANK"]
    selected_pay_rate = col1.selectbox('Hourly Pay Rate', ['24 Hour Rate', '8 Hour Rate'])
    # Defining the pay selector and option "Time and A Half" or "Straight Time"
    overtime_type = col2.selectbox('Type of Pay', ['Time and a Half', 'Straight Time'])
    # Text input box for mannually entering floats
    col1, col2, col3, col4 = st.columns(4)

    if employee_information["LONG_INC"] == 0.0000 or 0:
        long_inc = col1.number_input(
            'Longevity Incentive.',
            min_value=0.0000,
            max_value=1.9999,
            step=1e-4,
            format="%.4f")
    else:
        long_inc = employee_information["LONG_INC"]

    # Text input box for mannually entering floats
    if employee_information["JOB_INC"] == 0.0000 or 0:
        job_inc = col2.number_input(
            'Insert Job Incentive Pay',
            min_value=0.0000,
            max_value=1.9999,
            step=1e-4,
            format="%.4f")
    else:
        job_inc = employee_information["JOB_INC"]

    if employee_information["COLL_INC"] == 0.0000 or 0:
        # Text input box for mannually entering floats
        college_inc = col3.number_input(
            'Insert College Incentive',
            min_value=0.0000,
            max_value=7.500,
            step=1e-4,
            format="%.4f")
    else:
        college_inc = employee_information["COLL_INC"]

    if employee_information["HAZ_INC"] == 0.0000 or 0:
        hazard_inc = col4.number_input(
            'Hazard Incentive', 
            min_value=0.0000,
            max_value=7.500,
            step=1e-4,
            format="%.4f")
    else:
        hazard_inc = employee_information["HAZ_INC"]
        
if employee_information["NAME"] == '':
    name = st.text_input('Name (optional)', key='name_option')
else:
    name = employee_information["NAME"]

notes = st.text_input('Additional Notes (max 50)', max_chars=50)

selected_pay_rate, hourly = determine_hourly_rate(overtime_type, working_rank, selected_pay_rate)

long = multiply(long_inc,hours_works,selected_pay_rate)
job = multiply(job_inc,hours_works,selected_pay_rate)
coll = multiply(college_inc,hours_works,selected_pay_rate)
haz = multiply(hazard_inc,hours_works,selected_pay_rate)
incent = round(long+job+coll+haz, 2)

calc_pay = multiply(hours_works,hourly)
total_pay = round(incent + calc_pay, 2)

payperiod = get_pay_period(start_date)

# "run" varoable create to trigger sessio.state.key
run = st.button('Calculate/Add to Data Base', on_click=update_payout, args=[total_pay], key='person_expense')
if run:
    create_transaction(ADDED=str(today), GRANT_NUMBER=grant_number, PAY_PERIOD=payperiod, PROJECT_NUMBER=project_number, ACTIVITY=activity, EMPLOYEE_ID=employee_id, NAME=name, RANK=rank, HOURS_WORK=hours_works, DATE_WORKED=str(start_date), TOTAL_PAY=total_pay, NOTES=notes, AWARD_NUMBER=award_number)
    # Passing above values to a new data frame
    new_df = pd.DataFrame({
            'Employee ID': employee_id, 
            'Rank': rank, 
            'Hourly Pay': hourly,
            'Pay Type': selected_pay_rate,
            'Hours Worked': hours_works, 
            'Start Date': start_date,
            "End Date": end_date,
            'All Incentives': incent,
            'Pay w/o Incent': calc_pay, 
            'Total Pay': total_pay
            }, index=[0])
    # concartinating the new information to a new dataframe, passing it to the session_state.key
    st.session_state.dataframe = pd.concat([st.session_state.dataframe, new_df], ignore_index=True)

col1, col2, col3 = st.columns(3)

col1.metric('Working Rank', value=f'{working_rank}')
col2.metric('Hourly Rate', value=f'${hourly}')
col3.metric('Hours', value=hours_works)
col1.metric('Total Incentive Pay', value=f'${incent}')
col2.metric('Pay w/o Incentives', value=f'${calc_pay}')
col3.metric(f' Total Pay', value=f'${total_pay}')

if 'data' not in st.session_state:
    st.session_state.data = transactions

# Initalize "key" for session state
if "dataframe" not in st.session_state:
    st.session_state.dataframe = pd.DataFrame(columns=[
            'Employee ID',
            'Rank', 
            'Hourly Pay', 
            'Pay Type',
            'Hours Worked', 
            'Start Date',
            "End Date",
            'All Incentives',
            'Pay w/o Incent', 
            'Total Pay'
    ], index=[0])
    
# Calling on new session_state.key variable to display on the screen 
#st.session_state.dataframe

with st.container():
    col1, col2, col3 = st.columns(3)

    col3.metric(f'Session Running Total', value=f'${round(st.session_state.payout, 2)}')

df = st.session_state.dataframe 
df = df.to_csv()

with st.container():
    col1, buff, col3 = st.columns(3)
    col1.download_button(
        label='Save Session', 
        data=df, 
        file_name='session.csv',
        mime='text/csv')
    col3.button('Clear Session', on_click=st.session_state.clear)
