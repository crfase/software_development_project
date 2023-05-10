#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import plotly.express as px


# In[2]:


df = pd.read_csv('vehicles_us.csv')
df.sample(10, random_state = 3)


# In[ ]:





# In[3]:


#creating header with an option to filter the data and the checkbox:
#dataset includes mainly used cars, but there are several new options as well
#let users decide whether they want to see new cars from dealers or not


st.header('Market of used cars')
st.write("""
Filter the data below to see the ads by manufacturer
""")
show_new_cars = st.checkbox('Include new cars from dealers')


# In[4]:


show_new_cars


# In[5]:


if not show_new_cars:
    df = df[df.condition != 'new']


# In[6]:


#creating options for filter from all vehicle types and different years
type_choice = df['type'].unique()
make_type_choice = st.selectbox('Select vehicle type:', type_choice)


# In[7]:


make_type_choice


# In[8]:


#nest let's create a slider for years, so that users can filter cars by years of production
#creating min and max years as limits for sliders
min_year, max_year = int(df['model_year'].min()), int(df['model_year'].max())

year_range = st.slider(
    "Choose years",
    value = (min_year, max_year), min_value = min_year, max_value = max_year)


# In[9]:


year_range


# In[10]:


#creating actual range based on slider that will be used to filter in the dataset
actual_range = list(range(year_range[0], year_range[1]+1))


# In[11]:


#filtering dataset on chosen vehicle type and chosen year range
filtered_type = df[(df.type == make_type_choice) & (df.model_year.isin(list(actual_range)))]

#showing the final table in streamlit
st.table(filtered_type)


# In[12]:


filtered_type


# In[13]:


st.header("Price analysis")
st.write("""
Let's analyze what influences price the most. We will check how distribution of price varies depending on
transmission, cylinders, body type and condition
""")

#will create histograms with the split by paramater of choice: paint color, transmission, type, and condition

#creating list of options to choose from
list_for_hist = ['transmission', 'cylinders', 'type', 'condition']

#creating selectbox
choice_for_hist = st.selectbox('Split for price distribution', list_for_hist)

#plotly histogram, where price is split by the choice mode in the select box
fig1 = px.histogram(df, x = 'price', color = choice_for_hist)

#adding title
fig1.update_layout(title = "<b> Split of price by ()</b>".format(choice_for_hist))

#embedding into streamlit
st.plotly_chart(fig1)


# In[14]:


fig1.show()


# In[19]:


# creating age category of cars, because we want to take it into account when analyzing the price
df['age'] = 2023 - df['model_year']

def age_category(x):
    if x < 5:
        return '<5'
    elif x >= 5 and x < 10:
        return '5-10'
    elif x >= 10 and x < 20:
        return '10-20'
    elif x >= 20:
        return '20+'
    else:
        return 'unknown'
    
df['age_category'] = df['age'].apply(age_category)


# In[20]:


df['age_category']


# In[23]:


st.write("""
Now let's check how price is affected by odometer, number of cylinders, or days listed
""")

#distribution of price depending on odometer, cylinders, days_listed with the split by age category

list_for_scatter = ['odometer', 'cylinders', 'days_listed']
choice_for_scatter = st.selectbox('Price dependency on ', list_for_scatter)
fig2 = px.scatter(df, x = 'price', y = choice_for_scatter, hover_data = ['model_year'])

fig2.update_layout(
title = '<b> Price vs {}<b>'.format(choice_for_scatter))
st.plotly_chart(fig2)


# In[25]:


fig2


# In[ ]:




