import streamlit as st
import pandas as pd
import datetime as dt
import time

st.set_page_config(layout='wide')

@st.cache
def get_people_csv():
    print('cache miss...')
    time.sleep(2)
    return pd.read_csv('pages/people.csv')
     
people_df = get_people_csv()

people_df = pd.DataFrame(people_df)

if "twentyfour" not in st.session_state:
    st.session_state.twentyfour = 0

if "eight" not in st.session_state:
    st.session_state.eight = 0

conversion_rates = {
    0: 0.3611,
    1: 0.3611,
    2: 0.3611,
    3: 0.3611,
    4: 0.3611,
    5: 0.3611,
    6: 0.3589,
    7: 0.3571,
    8: 0.3809,
    9: 0.4047,
    10: 0.4,
    11: 0.4222,
    12: 0.4166,
    13: 0.4375,
    14: 0.4583,
    15: 0.4509,
    16: 0.4509,
    17: 0.4705,
    18: 0.4705,
    19: 0.4901,
    20: 0.4901,
    21: 0.5098,
    22: 0.5098,
    23: 0.5294,
    24: 0.5294,
    25: 0.5490
}

st.header('Hours Conversion Tool (24/8)')
st.subheader('...your welcome')
st.write('''
    INSTRUCTIONS: Select 'Yes' or 'No' under 'Use Employee ID' dropdown. If selecting yes, personnels EID will be used to automatically calculate hourly conversion
    rates for personnel detailed 24 hours to 8 hours. 'Years of Service' dropdown will be diabled and be populated with years of service for the selected employee only. This calculation 
    is based on the IAFF 1784 MOU for 2021-2023 accrual schedules for 56 hour and 40 hour employees. Drop down labeled 'Years of Service' will only be populate with the calculated years of service. 
    Years of service is calculated on an employees adjusted hire date ('Special Date') in telestaff MINUS todays date. Example: 10/13/2008 (adjusted hire date) - 12/06/2022 (date of writing this) = 14.

    If selecting 'No', employee ID will have no effect on the conversion rates. Manually change the years of service to calaculate the correct conversion rate in relation to years of service. 24 Hours and 8
    hours work in bi-directional and will automatically be updated upon interaction. 
    
    *This is a tool, this is not an offical statement of benifits owed to an employee. Offical conversion and hours must be approved through payroll. 
''')

'---'

col1, col2, col3, col4 = st.columns([1,2,1,1])

select = col1.selectbox('Use Employee ID', ['No' ,'Yes'])
eid = col2.selectbox('Employee ID Search', options=[person for person in people_df["Employee ID"]])
employee = people_df[people_df['Employee ID'] == eid]

special_date = employee["Special Date"].values[0]
special_date = dt.datetime.strptime(special_date, '%m/%d/%Y').date()

years = dt.datetime.today().year - special_date.year 


col3.metric('Adjusted Hire Date', str(special_date))
col4.metric('Current Years of Service', years)


col1, col2, col3 = st.columns([1,2,2])


with col1:

    if select == 'No':
        years_input = st.selectbox('Years of Service', options=[i for i in range(1,26)])
        years_input = conversion_rates.get(years_input, 0.5490) 
    else:
        years_input = st.selectbox('Years of Service', options=[years])
        years_input = conversion_rates.get(years_input, 0.5409) 

def twentyfour_to_eight():
    st.session_state.eight = round(st.session_state.twentyfour * years_input, 0)

def eight_to_twentyfour():
    st.session_state.twentyfour = round(st.session_state.eight / years_input, 0)

with col2:
    twentyfour_hours = st.number_input(
                        "24 Hours Accrual",
                        key='twentyfour',
                        on_change=twentyfour_to_eight,
                        step=1
                        )

with col3:
    
    
    eight_hours = st.number_input(
                        "8 hours Accrual",
                        key='eight',
                        on_change=eight_to_twentyfour,
                        step=1
                        )


def batching(lst):
    
    
    pass