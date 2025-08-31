import requests
import streamlit as st
import pandas as pd

st.title("SuperKart Sales Prediction")

# Batch Prediction
st.subheader("Online Sales Prediction")

# Input fields for product data
Product_Id = st.text_input("Product ID", max_chars=10, value='FD007')
Product_Weight = st.number_input("Product Weight", min_value=1.0, max_value=50.0, value=12.6)
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.003, max_value=0.5, value=0.05)
Product_MRP = st.number_input("Product MRP", min_value=1.0, max_value=500.0, value=146.0)
Product_Type = st.selectbox("Product Type", ['Frozen Foods', 'Dairy', 'Canned', 'Baking Goods', 'Health and Hygiene', 'Snack Foods', 'Meat', 
                                             'Household', 'Hard Drinks', 'Fruits and Vegetables', 'Breads', 'Soft Drinks', 'Breakfast', 
                                             'Others', 'Starchy Foods', 'Seafood'])
Store_Id = st.selectbox("Store ID", ['OUT004', 'OUT003', 'OUT001', 'OUT002'])
Store_Establishment_Year = st.selectbox("Store Establishment Year", ['2009', '1999', '1987', '1998'])
Store_Type = st.selectbox("Store Type", ['Supermarket Type2', 'Departmental Store', 'Supermarket Type1', 'Food Mart'])
Item_Type = st.selectbox("Item Type", ['Food', 'Non_Consumables', 'Drink'])
Product_Sugar_Content = st.selectbox("Product Sugar Content", ['Low Sugar', 'Regular', 'No Sugar'])
Store_Size = st.selectbox("Store Size", ['Medium', 'High', 'Small'])
Store_Location_City_Type = st.selectbox("Store Location City Type", ['Tier 2', 'Tier 1', 'Tier 3'])

product_data = {
        'Product_Weight': Product_Weight,
        'Product_Allocated_Area': Product_Allocated_Area, 
        'Product_MRP': Product_MRP,
        'Product_Type': Product_Type,
        'Store_Id': Store_Id,
        'Store_Establishment_Year': Store_Establishment_Year,
        'Store_Type': Store_Type,
        'Item_Type': Item_Type,
        'Product_Sugar_Content': Product_Sugar_Content,
        'Store_Size': Store_Size,
        'Store_Location_City_Type': Store_Location_City_Type
    }

if st.button("Predict", type='primary'):    
    response = requests.post("https://subhash33-flask-superkartsales-backend.hf.space/v1/product", json=product_data)    
    
    if response.status_code == 200:
        result = response.json()
        sales_prediction = result["Prediction"]  # Extract only the value
        st.write(f"Based on the information provided, the sales of the product {Product_Id} for the store {Store_Id} is likely going to be \
        {sales_prediction} and the number of products needed will be {int(round(sales_prediction/Product_MRP, 0))}.")
    else:
        st.error("Error in API request")

# Batch Prediction
st.subheader("Batch Prediction")

file = st.file_uploader("Upload CSV file", type=["csv"])
if file is not None:    
    if st.button("Predict for Batch", type='primary'):
        response = requests.post("https://subhash33-flask-superkartsales-backend.hf.space/v1/productbatch", files={"file": file})  
        if response.status_code == 200:
            result = response.json()
            st.header("Batch Prediction Results")
            st.write(result)
        else:
            st.error("Error in API request")
