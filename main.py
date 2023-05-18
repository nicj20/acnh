import pandas as pd
from datetime import date
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

today = date.today()

dt = pd.read_csv("files/fish.csv", sep=",")

#POPULAR MONTH

count_months = dt.count()
count_select = count_months[['january', 'february','march','april','may','june','july','august','september','october','november','december']]
x = ['january', 'february','march','april','may','june','july','august','september','october','november','december']
array = np.column_stack((x, count_select))
dt_months = pd.DataFrame(array, index=(range(1, 13)), columns=['month', 'count'])
#dt.months['count'] = dt_months['count'].astype(float)
#dt_months.loc[0] = count_select
print(dt_months)
print(dt_months.dtypes)

# FUNTIONS

def name_search(name):
    try:
        row_index = int(dt[dt["name"] == name].index.to_numpy())
        name = dt.at[dt.index[row_index], 'name']
        place = dt.at[dt.index[row_index], 'where_how']
        text = f'{name.title()} will be around in the {place}'
        return (text)
    except TypeError:
        return ("Please type a valid animal")


def name_date(name):
    try:
        row_index = int(dt[dt["name"] == name].index.to_numpy())
        name = dt.loc[row_index][['january', 'february','march','april','may','june','july','august','september','october','november','december']]
        return name
    except TypeError:
        return ("Please type a valid animal")

# WEB
st.title("Animal Crossing New Horizons Manager (northern)")
st.text("In this web you will be able to manage the fishes and bugs you want to catch")

st.header("Search by name where to find them")
out_name = st.text_input(label="Please type the name ->").lower()
st.write(name_search(out_name))

st.header("Search the schedules to find the fish")
out_date = st.text_input(label="Please type the name of the fish ->").lower()
st.write(name_date(out_date))
