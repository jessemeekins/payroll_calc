#%%
import datetime as dt
import streamlit as st
from deta import Deta



deta = Deta(st.secrets['project_key'])
payscale = deta.Base("Payscale")
employees = deta.Base("Employees")
transactions = deta.Base('Transactions')
cost_center = deta.Base('CostCenter')

employee_database_columns = ["EMPLOYEE_ID", "NAME", "RANK", "LONG_INC", "COLL_INC", "JOB_INC", "HAZ_INC"]

def get_payscale():
    try:
        pay = payscale.fetch()
        return pay.items
    except:
        pass
def create_employee(employee_id, name, rank, long_inc=0, coll_inc=0, job_inc=0, haz_inc=0 ):
    employees.put({"EMPLOYEE_ID": employee_id, "NAME": name, "RANK": rank, "LONG_INC": long_inc, "COLL_INC": coll_inc, "JOB_INC": job_inc, "HAZ_INC": haz_inc}, employee_id)
    return True

def insert_employee(**kwargs):
    values = {}
    for k,v in kwargs.items():
        values[k] = v
    employees.insert(values)


def get_employee(employee_id):
    employee = employees.get(employee_id)
    return employee

def get_all_employees():
    e = employees.fetch()
    return e.items

def update_employee(employee_id, **kwargs):
    updates = {}
    for k, v in kwargs.items():
        updates[k] = v
    employees.update(updates, employee_id)

def delete_employee(employee_id):
    employees.delete(employee_id)
    

def create_transaction(**kwargs):
    values = {}
    for k,v in kwargs.items():
        values[k] = v
    transactions.put(values)

def get_transactions():
    try:
        trans = transactions.fetch()
        trans = trans.items
    except:
        trans = None
    return trans

def delete_transaction(trans_id):
    transactions.delete(trans_id)

def get_cost_centers():
    cost = cost_center.fetch()
    d = {}
    items = cost.items
    for i in items:
        grant = i["GRANT"]
        project = i["PROJECT"]
        d[grant] = project
    return d

def determine_hourly_rate(overtime_type, rank, selected_pay_rate):
    overtime_type = {overtime_type: 1.5}
    overtime_type = overtime_type.get('Time and a Half', 1.0)

    hourly_ = get_pay_rate(rank, selected_pay_rate)
    hourly_pay = round(hourly_ * overtime_type, 2)

    return overtime_type, hourly_pay

def get_pay_rate(rank, selected_pay_rate):

    items = get_payscale()
    for i in items:
        if i["RANK"] == rank:
            rank = i[selected_pay_rate]
    return rank
        

def multiply(*args):
    multi = 1
    for arg in args:
        multi *= arg
    return round(multi, 2) 

def get_pay_period(date):
    PP2023 = {
        'PP01': [dt.date(2022,12,17), dt.date(2022,12,30)],
        'PP02': [dt.date(2022,12,31) , dt.date(2023,1,13)],
        'PP03': [dt.date(2023,1,14), dt.date(2023,1,27)],
        'PP04': [dt.date(2023,1,28), dt.date(2023,2,10)],
        'PP05': [dt.date(2023,2,11), dt.date(2023,2,24)],
        'PP06': [dt.date(2023,2,25), dt.date(2023,3,10)],
        'PP07': [dt.date(2023,3,11), dt.date(2023,3,24)],
        'PP08': [dt.date(2023,3,25), dt.date(2023,4,7)],
        'PP09': [dt.date(2023,4,8), dt.date(2023,4,21)],
        'PP10': [dt.date(2023,4,22), dt.date(2023,5,5)],
        'PP11': [dt.date(2023,5,6), dt.date(2023,5,19)],
        'PP12': [dt.date(2023,5,20), dt.date(2023,6,2)],
        'PP13': [dt.date(2023,6,3), dt.date(2023,6,16)],
        'PP14': [dt.date(2023,6,17), dt.date(2023,6,30)],
        'PP15': [dt.date(2023,7,1), dt.date(2023,7,14)],
        'PP16': [dt.date(2023,7,15), dt.date(2023,7,28)],
        'PP17': [dt.date(2023,7,29), dt.date(2023,8,11)],
        'PP18': [dt.date(2023,8,12), dt.date(2023,8,25)],
        'PP29': [dt.date(2023,8,26), dt.date(2023,9,8)],
        'PP20': [dt.date(2023,9,9), dt.date(2023,9,24)],
        'PP21': [dt.date(2023,9,23), dt.date(2023,10,6)],
        'PP22': [dt.date(2023,10,7), dt.date(2023,10,20)],
        'PP23': [dt.date(2023,10,21), dt.date(2023,11,3)],
        'PP24': [dt.date(2023,11,4), dt.date(2023,11,17)],
        'PP25': [dt.date(2023,11,18), dt.date(2023,12,1)],
        'PP26': [dt.date(2023,12,2), dt.date(2023,12,15)]
        }
    for k,v in PP2023.items():
        if date >= v[0] and date  <= v[1]:
            return k