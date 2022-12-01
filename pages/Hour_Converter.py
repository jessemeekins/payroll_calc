import streamlit as st

if "twentyfour" not in st.session_state:
    st.session_state.twentyfour = 0

if "eight" not in st.session_state:
    st.session_state.eight = 0

conversion_rates = {
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


st.subheader('Hours Conversion Tool (24/8)')
st.write('...your welcome')

'---'


col1, col2, col3 = st.columns([1,2,2])

with col1:
   years = st.selectbox('Years of Service', options=[i for i in range(1,26)])
   years = conversion_rates.get(years, 0.4509) 
def twentyfour_to_eight():
    st.session_state.eight = round(st.session_state.twentyfour * years, 0)

def eight_to_twentyfour():
    st.session_state.twentyfour = round(st.session_state.eight / years, 0)

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

