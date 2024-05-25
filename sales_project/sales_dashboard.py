import streamlit as st
from datetime import datetime
import requests
import pandas as pd
from PIL import Image
import io
import django

# Base URL for the Django backend
BASE_URL = 'http://127.0.0.1:8000/sales_app/'

st.title('Sales Data Management System')

# Add Sales Record Section
st.header('Add Sales Record')
date = st.date_input('Date', value=datetime.now())
product = st.text_input('Product')
sales_amount = st.number_input('Sales Amount', min_value=0.0, format="%.2f")
region = st.text_input('Region')
receipt_photo = st.file_uploader('Upload Receipt Photo', type=['png', 'jpg', 'jpeg'])

if st.button('Add Record'):
    if date and product and sales_amount and region and receipt_photo:
        # Ensure receipt photo has a filename
        receipt_photo_name = receipt_photo.name
        files = {'receipt_photo': (receipt_photo_name, receipt_photo, receipt_photo.type)}
        data = {
            'date': date.strftime('%Y-%m-%d'),
            'product': product,
            'sales_amount': sales_amount,
            'region': region,
        }
        
        # Sending data to Django backend
        response = requests.post(BASE_URL + 'add/', data=data, files=files)

        if response.status_code == 200:
            st.success('Record added successfully!')
        else:
            st.error(f'Failed to add record: {response.json()}')
    else:
        st.error('Please fill in all fields and upload a receipt photo.')

# View and Visualize Sales Data Section
st.header('View and Visualize Sales Data')

if st.button('Load Data'):
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        sales_data = response.json()
        if sales_data:
            df = pd.DataFrame(sales_data)
            st.dataframe(df)
            
            # Visualizations
            st.subheader('Sales Amount by Product')
            sales_by_product = df.groupby('product')['sales_amount'].sum().reset_index()
            st.bar_chart(sales_by_product, x='product', y='sales_amount')

            st.subheader('Sales Amount by Region')
            sales_by_region = df.groupby('region')['sales_amount'].sum().reset_index()
            st.bar_chart(sales_by_region, x='region', y='sales_amount')

            st.subheader('Sales Amount Over Time')
            sales_over_time = df.groupby('date')['sales_amount'].sum().reset_index()
            st.line_chart(sales_over_time, x='date', y='sales_amount')

            # st.subheader('Sales Distribution by Product')
            # st.pie_chart(df['product'].value_counts())
        else:
            st.warning('No sales data available.')
    else:
        st.error('Failed to load data.')

