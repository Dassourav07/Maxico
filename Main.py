import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore")

# Set up Streamlit page configuration
st.set_page_config(page_title="Mexico City Toy Sales Dashboard", page_icon=":truck:", layout="wide")

# Set the title of the web app
st.title("Mexico Toy Sales Dashboard")

# Adjust the padding of the block container
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

file_path = 'Mexico Toy Sales _ PA _Case Study.xlsx'

if os.path.exists(file_path):
    # Read the Excel file into a Pandas DataFrame
    sales_df = pd.read_excel(file_path, sheet_name='sales')
    stores_df = pd.read_excel(file_path, sheet_name='stores')
    products_df = pd.read_excel(file_path, sheet_name='products')
    inventory_df = pd.read_excel(file_path, sheet_name='inventory')

    # Convert 'Date' column to datetime
    sales_df["Date"] = pd.to_datetime(sales_df["Date"], dayfirst=True)

    # Merge sales data with store data
    df = pd.merge(sales_df, stores_df, on="Store_ID")

    # Define mapping dictionaries for product and store names
    product_name_map = dict(zip(products_df['Product_ID'], products_df['Product_Name']))
    store_name_map = dict(zip(stores_df['Store_ID'], stores_df['Store_Name']))

    # Replace IDs with names
    df['Product_Name'] = df['Product_ID'].map(product_name_map)
    df['Store_Name'] = df['Store_ID'].map(store_name_map)

    # Set up columns for date input in the sidebar
    startDate = st.sidebar.date_input("Start Date", df["Date"].min(), key='start_date')
    endDate = st.sidebar.date_input("End Date", df["Date"].max(), key='end_date')

    # Convert date input to datetime64[ns] for comparison
    startDate = pd.to_datetime(startDate)
    endDate = pd.to_datetime(endDate)

    # Filter dataframe based on selected dates
    df = df[(df["Date"] >= startDate) & (df["Date"] <= endDate)]

    st.sidebar.header("Choose your filter: ")

    # Multiselect for city filtering
    city = st.sidebar.multiselect("Pick the city", df["Store_City"].unique())

    if city:
        df = df[df["Store_City"].isin(city)]

    # Multiselect for product filtering with product names
    product = st.sidebar.multiselect("Pick the product", df["Product_Name"].unique())

    if product:
        df = df[df["Product_Name"].isin(product)]

    # Ensure numeric conversion for financial columns and units
    if products_df['Product_Price'].dtype == 'object':
        products_df['Product_Price'] = products_df['Product_Price'].str.replace('$', '').astype(float)

    if products_df['Product_Cost'].dtype == 'object':
        products_df['Product_Cost'] = products_df['Product_Cost'].str.replace('$', '').astype(float)

    if df['Units'].dtype == 'object':
        df['Units'] = df['Units'].astype(int)

    # Ensure unique Product_ID in inventory_df by aggregating
    inventory_df = inventory_df.groupby('Product_ID').agg({'Stock_On_Hand': 'sum'}).reset_index()

    # Calculate key metrics
    df['Revenue'] = df['Product_ID'].map(products_df.set_index('Product_ID')['Product_Price']) * df['Units']
    df['Profit'] = (df['Product_ID'].map(products_df.set_index('Product_ID')['Product_Price']) - df['Product_ID'].map(products_df.set_index('Product_ID')['Product_Cost'])) * df['Units']
    df['Inventory'] = df['Product_ID'].map(inventory_df.set_index('Product_ID')['Stock_On_Hand']) - df['Units']

    # Calculate Loss only when Product_Cost > Product_Price
    df['Loss'] = 0  # Initialize Loss column
    mask = df['Product_ID'].map(products_df.set_index('Product_ID')['Product_Cost']) > df['Product_ID'].map(products_df.set_index('Product_ID')['Product_Price'])
    df.loc[mask, 'Loss'] = (df['Product_ID'].map(products_df.set_index('Product_ID')['Product_Cost']) - df['Product_ID'].map(products_df.set_index('Product_ID')['Product_Price'])) * df.loc[mask, 'Units']

    # Calculate key metrics after filtering
    total_revenue = df["Revenue"].sum() if not df.empty else 0
    total_profit = df["Profit"].sum() if not df.empty else 0
    total_loss = df["Loss"].sum() if not df.empty else 0
    total_inventory = df["Inventory"].sum() if not df.empty else 0
    
    # Calculate out-of-stock products based on inventory data
    out_of_stock_products_inventory = inventory_df[inventory_df["Stock_On_Hand"] == 0].shape[0]
    total_stock_on_hand = inventory_df['Stock_On_Hand'].sum() if not inventory_df.empty else 0

    # Use Streamlit columns for layout
    col1, col2 = st.columns(2)

    with col1:
        # Display key metrics
        st.subheader("Key Metrics")
        st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
        st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
        st.metric(label="Total Loss", value=f"${total_loss:,.2f}")
        st.metric(label="Total Inventory", value=f"{total_inventory:,}")
        st.metric(label="Out of Stock Products", value=f"{out_of_stock_products_inventory}")
        st.metric(label="Total Stock On Hand", value=f"{total_stock_on_hand:,}")

        # 1. Most profitable store
        profitable_store = df.groupby("Store_Name")["Profit"].sum().idxmax()
        st.write(f"The most profitable store is: {profitable_store}")

        # Graphical representation of profit by store
        fig1 = px.bar(df.groupby("Store_Name")["Profit"].sum().reset_index(), x="Store_Name", y="Profit", title="Profit by Store")
        st.plotly_chart(fig1)

        # 2. Top 5 most profitable products
        top_5_profitable_products = df.groupby("Product_Name")["Profit"].sum().nlargest(5)
        st.write("Top 5 most profitable products:")
        st.write(top_5_profitable_products)

        # Graphical representation of top 5 most profitable products
        fig2 = px.bar(top_5_profitable_products.reset_index(), x="Product_Name", y="Profit", title="Top 5 Most Profitable Products")
        st.plotly_chart(fig2)



    with col2:
        # 3. Most in-demand product (by name)
        most_demand_product_name = df.groupby("Product_Name")["Units"].sum().idxmax()
        st.write(f"The most in-demand product is: {most_demand_product_name}")

        # Graphical representation of demand by product
        fig3 = px.bar(df.groupby("Product_Name")["Units"].sum().reset_index(), x="Product_Name", y="Units", title="Demand by Product")
        st.plotly_chart(fig3)


        # 4. Store showing most potential for investment
        most_potential_store = df.groupby("Store_Name")["Revenue"].sum().idxmax()
        st.write(f"The store showing the most potential for investment is: {most_potential_store}")

        # Graphical representation of revenue by store
        fig4 = px.bar(df.groupby("Store_Name")["Revenue"].sum().reset_index(), x="Store_Name", y="Revenue", title="Revenue by Store")
        st.plotly_chart(fig4)

        # 5. Product showing least promise and should be discontinued
        least_promise_product_name = df.groupby("Product_Name")["Profit"].sum().idxmin()
        st.write(f"The product showing the least promise and should be discontinued is: {least_promise_product_name}")

        # Graphical representation of least profitable products
        fig5 = px.bar(df.groupby("Product_Name")["Profit"].sum().nsmallest(5).reset_index(), x="Product_Name", y="Profit", title="Least Profitable Products")
        st.plotly_chart(fig5)


    # Additional visualizations (example)
    if 'Store_City' in df.columns:
        fig = px.histogram(df, x='Store_City', y='Revenue', title='Revenue by Store City')
        st.plotly_chart(fig)

    # Display the filtered DataFrame at the bottom of the page
    st.subheader("Filtered Sales Data")
    st.dataframe(df)

else:
    st.error(f"File '{file_path}' not found. Please ensure the file is in the correct directory.")

