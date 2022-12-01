import streamlit as st
from database_func import *
import pandas as pd

st.header('Add/Remove Employee')

emp_list = get_all_employees()
deta_pay_scale = get_payscale()

with st.sidebar:
  
    st.subheader("Search for Employee")
    employee_id = st.selectbox('Search Employee', sorted([emp["EMPLOYEE_ID"] for emp in emp_list], reverse=False))
    
    employee_information = get_employee(employee_id)

tab1, tab2 = st.tabs(['Add/Remove/Update', 'Audit Employees'])

with tab1:

    with st.form('Employee Input', clear_on_submit=True):
        
        eid = st.text_input('EID', key='eid')
        name = st.text_input('Name', key='name')
        rank = st.selectbox('Select Rank',[rank["RANK"] for rank in deta_pay_scale])

        long = st.number_input(
            'Longevity Incentive.',
            value=0.0000, 
            min_value=0.0000,
            max_value=1.9999,
            step=1e-4,
            format="%.4f")
        # Text input box for mannually entering floats
        job = st.number_input(
            'Insert Job Incentive Pay',
            value=0.0000, 
            min_value=0.0000,
            max_value=1.9999,
            step=1e-4,
            format="%.4f")
        # Text input box for mannually entering floats
        coll = st.number_input(
            'Insert College Incentive',
            value=0.0000, 
            min_value=0.0000,
            max_value=7.500,
            step=1e-4,
            format="%.4f")
        haz = st.number_input(
            'Hazard Incentive', 
            value=0.0000, 
            min_value=0.0000,
            max_value=7.500,
            step=1e-4,
            format="%.4f")

        col1, col2, col3 = st.columns(3)
        
        inc = {"NAME": name, "RANK": rank, "LONG_INC":long, "JOB_INC":job, "COLL_INC":coll, "HAZ_INC":haz}


        add = col1.form_submit_button('Add')
        if add:
            add_data = {"EMPLOYEE_ID": eid, "NAME": name, "RANK": rank}
            for k, v in inc.items():
                if v != 0:
                    add_data[k] = v
                else:
                    pass
            insert_employee(**add_data)
            st.success('Employee added to database.')

        update = col2.form_submit_button('Update')
        if update:
            update_data = {}
            for k,v in inc.items():
                if v == '' or v == 0 or v == 'AEMT/Probation':
                    pass
                else:
                    update_data[k] = v

            update_employee(eid, **update_data)
            st.success('Employee updated succesfully')

        remove = col3.form_submit_button('Remove')
        if remove:
            delete_employee(eid)
            st.success('Employee deleted')

with tab2:

    df = pd.DataFrame.from_records(emp_list, columns=[
        'EMPLOYEE_ID',
        'NAME',
        'RANK',
        'JOB_INC',
        'LONG_INC',
        'COLL_INC',
        'HAZ_INC'
    ])

    if employee_id == '000000':
        df
    else:    
        filtered_df =  df.query(
            "EMPLOYEE_ID == @ employee_id" 
        )
        filtered_df