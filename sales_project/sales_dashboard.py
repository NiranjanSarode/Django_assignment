import streamlit as st
import pandas as pd
import plotly.express as px
import os
import django

# Set up Django environment (crucial step)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sales_project.settings') # Adjust if your project name is different
django.setup()

# Now you can import your models safely
from sales_app.models import Product, Region, Sale
from sales_app.forms import SaleForm
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO



st.title("Sales Data Management")

tab1, tab2 = st.tabs(["New Sale", "Sales Dashboard"])

with tab1:
    # New Sale Form
    st.header("Create New Sale")

    with st.form("sale_form"):
        date = st.date_input("Date")
        product = st.selectbox("Product", Product.objects.all(), format_func=lambda x: x.name)
        amount = st.number_input("Amount", min_value=0.0)
        region = st.selectbox("Region", Region.objects.all(), format_func=lambda x: x.name)
        receipt_photo = st.file_uploader("Receipt Photo", type=["jpg", "png", "jpeg"])

        submitted = st.form_submit_button("Save Sale")
        if submitted:
            # Convert uploaded file to SimpleUploadedFile
            if receipt_photo:
                bytes_data = receipt_photo.getvalue()
                content_file = SimpleUploadedFile(receipt_photo.name, bytes_data)
            else:
                content_file = None

            # Create form instance with the data and file
            form_data = {
                'date': date,
                'product': product.pk,
                'amount': amount,
                'region': region.pk,
                'receipt_photo': content_file
            }
            form = SaleForm(form_data)

            # Handle form submission
            if form.is_valid():
                form.save()
                st.success("Sale data saved successfully!")
            else:
                st.error("Invalid data. Please check your input.")

# ... other imports ...

with tab2:
    # Sales Data Dashboard
    st.header("Sales Dashboard")
    sales_data = Sale.objects.select_related("product", "region").all() # select_related for region also
    if not sales_data.exists():
        st.warning("No sales data yet. Please add some sales first.")
    else:
        # Convert queryset to list of dictionaries
        sales_list = []
        for sale in sales_data:
            sales_list.append({
                'date': sale.date,
                'product__name': sale.product.name,
                'amount': sale.amount,
                'region__name': sale.region.name
            })
        
        # Create DataFrame from the list of dictionaries
        df = pd.DataFrame(sales_list)

        # Total Sales by Product (Corrected)
        st.subheader("Total Sales by Product")
        product_sales = df.groupby("product__name")["amount"].sum().reset_index()
        fig = px.bar(product_sales, x="product__name", y="amount", title="Total Sales by Product")
        st.plotly_chart(fig)

        # Total Sales by Region
        st.subheader("Total Sales by Region")
        region_sales = df.groupby("region__name")["amount"].sum().reset_index()
        fig = px.pie(region_sales, values='amount', names='region__name', title='Total Sales by Region')
        st.plotly_chart(fig)
