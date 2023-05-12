#!/usr/bin/env python
# coding: utf-8

# # Software Developement Tool Project
# 
# The focus of this project is to provide additional practice with common software engineering tasks.
# 
# Using data provided (`'vehicles_us.csv'`) regarding different vehicles for sale, both new and old, we will look
# at putting together a web app to filter through the data based on a variety of conditions.

# In[6]:


import streamlit as st
import pandas as pd
import plotly.express as px


# In[7]:


df = pd.read_csv('vehicles_us.csv')


# In[8]:


df.info()


# In[13]:


df['model_year'] = df['model_year'].fillna(df.groupby('model')['model_year'].transform('median'))
df['model_year'].unique()


# In[15]:


df['cylinders'] = df['cylinders'].fillna(df.groupby('model')['cylinders'].transform('median'))
df['cylinders'].unique()


# In[18]:


df['odometer'] = df['odometer'].fillna(df.groupby('model_year')['odometer'].transform('median'))
df['odometer'].unique()


# In[21]:


df['paint_color'] = df['paint_color'].fillna('No Info')
df['paint_color'].unique()


# In[22]:


df['is_4wd'] = df['is_4wd'].fillna(0)
df['is_4wd'].unique()


# In[ ]:


#creating header with an option to filter the data and the checkbox:
#let users decide whether they want to see new cars from dealers or not


st.header('Market of used cars')
st.write("""
Filter the data below to see the information by different vehicle types
""")
show_new_cars = st.checkbox('Include new cars from dealers')


# In[ ]:


show_new_cars


# In[ ]:


if not show_new_cars:
    df = df[df.condition != 'new']


# In[ ]:


#creating options for filter from all vehicle types and different years
type_choice = df['type'].unique()
make_type_choice = st.selectbox('Select vehicle type:', type_choice)


# In[ ]:


make_type_choice


# In[ ]:


#next let's create a slider for years, so that users can filter cars by years of production
#creating min and max years as limits for sliders
min_year, max_year = int(df['model_year'].min()), int(df['model_year'].max())

year_range = st.slider(
    "Choose years",
    value = (min_year, max_year), min_value = min_year, max_value = max_year)


# In[ ]:


year_range


# In[ ]:


#creating actual range based on slider that will be used to filter in the dataset
actual_range = list(range(year_range[0], year_range[1]+1))


# In[ ]:


#filtering dataset on chosen vehicle type and chosen year range
filtered_type = df[(df.type == make_type_choice) & (df.model_year.isin(list(actual_range)))]

#showing the final table in streamlit
st.dataframe(filtered_type)


# In[ ]:


filtered_type


# In[ ]:


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


# In[ ]:


fig1.show()


# In[ ]:


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


# In[ ]:


df['age_category']


# In[ ]:


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


# In[ ]:


fig2


# # Conclusion
# 
# After taking care of the missing values within the dataset, we have a code to build a web app to narrow your search by filtering the data by age of the vehicle, and model type. This also allows you to see the way the price is reflected by different factors, including transmission, odometer, number of cylinders and the number of days listed.
