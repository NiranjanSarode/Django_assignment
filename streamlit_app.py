import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import math

def fetch_sales_data():
    url = 'http://127.0.0.1:8000/api/salesdata/'
    sessionid = st.query_params.get('sessionid', '')
    response = requests.get(url, cookies={'sessionid': sessionid})
    if response.status_code == 200:
        sales_data = response.json()
        return pd.DataFrame(sales_data)
    else:
        st.error("Failed to fetch sales data")
        return pd.DataFrame()

def main():
    st.title("Sales Data Visualization")
    df = fetch_sales_data()

    if not df.empty:
        # Calculate most demanded product
        most_demanded_product = df.groupby('product')['quantity'].sum().idxmax()
        # Calculate most flopped product
        most_flopped_product = df.groupby('product')['quantity'].sum().idxmin()

        # Display most demanded and most flopped products in the sidebar
        st.sidebar.title("Product Insights")
        st.sidebar.header("Bestseller:")
        st.sidebar.write(most_demanded_product)
        st.sidebar.header("Low performer:")
        st.sidebar.write(most_flopped_product)
        
        # Display graphs below the sidebar
        st.subheader("Sales Data Visualization")
        st.write("Sales Data", df)
        st.bar_chart(df.groupby('product')['quantity'].sum())

        if 'product' in df.columns:
            # Calculate total quantity sold per product
            product_quantity = df.groupby('product')['quantity'].sum()
            st.subheader("Product Quantity Distribution")
            fig, ax = plt.subplots()
            ax.pie(product_quantity, labels=product_quantity.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig)

    if not df.empty:
        # Calculate total quantity sold per day
        df['order_date'] = pd.to_datetime(df['order_date']).dt.strftime('%d/%m')
        df = df.groupby('order_date')['quantity'].sum().reset_index()

        # Plot the graph
        st.subheader("Total Quantity Sold Per Day")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df['order_date'], df['quantity'])
        ax.set_xlabel("Date (DD/MM)")
        ax.set_ylabel("Total Quantity")
        ax.set_title("Total Quantity Sold Per Day")
        ax.tick_params(axis='x', rotation=45)
        for i, val in enumerate(df['quantity']):
            ax.text(i, val + 0.1, str(math.ceil(val)), ha='center', va='bottom', rotation=90)
        st.pyplot(fig)

        # product_quantity = df.groupby('product')['quantity'].sum()
        # st.subheader("Product Quantity Distribution")
        # fig, ax = plt.subplots()
        # ax.pie(product_quantity, labels=product_quantity.index, autopct='%1.1f%%', startangle=90)
        # ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        # st.pyplot(fig)
        
    
    else:
        st.error("No sales data found")

if __name__ == "__main__":
    main()
