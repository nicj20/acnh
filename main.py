import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import altair as alt
from images import get_data

dt = pd.read_csv("fish.csv", sep=",")

# CLEAN DATA -----------------------------------

dt.drop(columns=['SH Jan', 'SH Feb', 'SH Mar', 'SH Apr', 'SH May', 'SH Jun', 'SH Jul', 'SH Aug', 'SH Sep', 'SH Oct',
                 'SH Nov', 'SH Dec', 'Lighting Type', 'Icon Filename', 'Critterpedia Filename', 'Internal ID',
                 'Unique Entry ID', 'Furniture Filename'], axis=1, inplace=True)
dt.rename(columns={'NH Jan': 'Jan', 'NH Feb': 'Feb', 'NH Mar': 'Mar', 'NH Apr': 'Apr', 'NH May': 'May', 'NH Jun': 'Jun',
                   'NH Jul': 'Jul', 'NH Aug': 'Aug', 'NH Sep': 'Sep', 'NH Oct': 'Oct', 'NH Nov': 'Nov', 'NH Dec': 'Dec',
                   'Where/How': 'where_how', 'Spawn Rates': 'spawn_rate', '#': 'id'},
          inplace=True)
dt = dt.replace('4 AM – 9 PM', '4 AM – 9 PM')
dt = dt.replace('Sea (rainy days)', 'Sea')

# NEW COLUMNS https://www.reddit.com/r/AnimalCrossing/comments/gdl9p3/heres_a_chart_of_the_spawn_rates_of_every_fish/

dt[['low_sr', 'high_sr']] = dt.spawn_rate.str.split('–', n=1, expand=True)

# UNIQUE VALUES --------------------------------

unique_values_places = dt['where_how'].unique()
unique_values_hours = pd.concat([dt['Jan'], dt['Feb'], dt['Mar'], dt['Apr'], dt['May'], dt['Jun'], dt['Jul'],
                                 dt['Aug'], dt['Sep'], dt['Oct'], dt['Nov'], dt['Dec']]).unique()

# POPULAR MONTH ---------------------------------

x_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
            'Nov', 'Dec']
count_months = dt.count()
count_select = count_months[['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
                             'Nov', 'Dec']]

array = np.column_stack((x_months, count_select))
dt_months = pd.DataFrame(count_months, index=x_months, columns=['count'])
dt_months['count'] = dt_months['count'].astype(float)

data_pie = {'Months': x_months,
            'Count': count_select}

dt_months_pie = pd.DataFrame(data_pie)

# POPULAR HOUR ---------------------------------

x_hours = ['All day', '4AM - 9PM', '4PM - 9AM', '9AM - 4PM', '9PM - 4AM']
count_all_day = (dt == 'All day').sum().sum()
count_4am = (dt == '4 AM – 9 PM').sum().sum()
count_4pm = (dt == '4 PM – 9 AM').sum().sum()
count_9am = (dt == '9 AM – 4 PM').sum().sum()
count_9pm = (dt == '9 PM – 4 AM').sum().sum()
y_hours = [count_all_day, count_4am, count_4pm, count_9am, count_9pm]

data_hour = {'Values': y_hours}
df_hour = pd.DataFrame(data_hour, index=x_hours)

# POPULAR PLACE ---------------------------------

x_places = ['Sea', 'River', 'Pier', 'Pond', 'River (clifftop)', 'River (mouth)']
count_sea = (dt == 'Sea').sum().sum()
count_riv = (dt == 'River').sum().sum()
count_pier = (dt == 'Pier').sum().sum()
count_pond = (dt == 'Pond').sum().sum()
count_rc = (dt == 'River (clifftop)').sum().sum()
count_rm = (dt == 'River (mouth)').sum().sum()
y_places = [count_sea, count_riv, count_pier, count_pond, count_rc, count_rm]

data_place = {'Values': y_places}
df_place = pd.DataFrame(data_place, index=x_places)

x_places_less = ['Sea', 'River', 'Pier', 'Pond']
y_places_less = [count_sea, (count_riv + count_rc + count_rm), count_pier, count_pond]
data_place_less = {'Values': y_places_less}
df_place_less = pd.DataFrame(data_place_less, index=x_places_less)

# SPAWN RANGE---------------------------------

min_r = dt['low_sr'].astype(float)
max_r = dt['high_sr'].astype(float)
dt['mean_sr'] = (min_r + max_r) / 2
mean_r = dt['mean_sr']


# FUNCTIONS--------------------------------------

def name_search(name):
    try:
        row_index = int(dt[dt["Name"] == name].index.to_numpy())
        name = dt.at[dt.index[row_index], 'Name']
        place = dt.at[dt.index[row_index], 'where_how']
        text = f'{name.title()} will be around in the {place}'
        return (text)
    except TypeError:
        return "Please type a valid animal"


def name_date(name):
    try:
        row_index = int(dt[dt["Name"] == name].index.to_numpy())
        name = dt.loc[row_index][['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
                                  'Nov', 'Dec']]
        return name
    except TypeError:
        return "Please type a valid animal"


def id_search(id):
    try:
        row_index = int(dt[dt["id"] == id].index.to_numpy())
        name_ = dt.at[dt.index[row_index], 'Name']
        text = f'The fish you are searching for is the {name_.title()}!'
        return [text, name_]
    except TypeError:
        return "Please type a valid ID"


# WEB --------------------------------------------
st.title("Animal Crossing New Horizons Manager (northern)")
st.text("On this web you will be able to manage the fish and bugs you want to catch")

st.header("Search by name where to find them")
out_name = st.text_input(label="Please type the name -> Example = Salmon").lower()
st.write(name_search(out_name))

try:
    st.image(get_data(out_name))
except KeyError:
    st.write('')

st.header("Search the schedules to find the fish")
out_date = st.text_input(label="Please type the name of the fish -> Example = Salmon").lower()
st.write(name_date(out_date))

#---------------------------------------

st.header("Most popular month")
figure = px.bar(dt_months, color='value', color_continuous_scale='greens')
st.plotly_chart(figure)

figure = px.pie(dt_months_pie, values='Count', names='Months', color_discrete_sequence=px.colors.sequential.Emrld)
st.plotly_chart(figure)

# --------------------------------------

st.header("Most popular hour")
figure = px.bar(df_hour, color='value', color_continuous_scale="greens")
st.plotly_chart(figure)

#------------------------------------

st.header("Most popular place")
figure = px.bar(df_place_less, color='value', color_continuous_scale="greens")
st.plotly_chart(figure)

figure = px.bar(df_place, color='value', color_continuous_scale="greens")
st.plotly_chart(figure)

# -----------------------------------

st.header("Range of Spawn")
out_id = st.number_input(label="Please type the ID you want to search ->  Example = 25", step=1)
result = id_search(out_id)
st.write(result[0])

try:
    st.image(get_data(result[1]))
except KeyError:
    st.write('')

name = dt['id'].astype(int)
df_range = {'ID': name,
            'Min': min_r,
            'Max': max_r}
chart_data = pd.DataFrame(df_range)

figure = alt.Chart(chart_data).mark_circle().encode(
    x='ID', y='Min', size='Max', color=alt.Color('Max', scale=alt.
                                                 Scale(scheme='darkgreen')), tooltip=['ID', 'Min', 'Max'])

st.altair_chart(figure, use_container_width=True, theme=None)
