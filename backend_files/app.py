import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app with a Name
sales_predictor_api = Flask("SuperKart Sales Predictor")

# Load the trained sales prediction model
model = joblib.load("sales_prediction_model_v1_0.joblib")

# Define a route for the home page
@sales_predictor_api.get('/')
def home():
    return "Welcome to the SuperKart Sales Prediction API!"

# Define an endpoint to predict sales for a single product
@sales_predictor_api.post('/v1/product')
def predict_sales():
    # Get JSON data from the request
    product_data = request.get_json()

    # Extract relevant product features from the input data
    sample = {
        'Product_Weight': product_data['Product_Weight'],
        'Product_Allocated_Area': product_data['Product_Allocated_Area'],
        'Product_MRP': product_data['Product_MRP'],
        'Product_Type': product_data['Product_Type'],
        'Store_Id': product_data['Store_Id'],
        'Store_Establishment_Year': product_data['Store_Establishment_Year'],
        'Store_Type': product_data['Store_Type'],
        'Item_Type': product_data['Item_Type'],
        'Product_Sugar_Content': product_data['Product_Sugar_Content'],
        'Store_Size': product_data['Store_Size'],
        'Store_Location_City_Type': product_data['Store_Location_City_Type'],
    }

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make sales prediction using the trained model
    predicted_sales = round(model.predict(input_data).tolist()[0], 2) 

    # Return the prediction as a JSON response
    return jsonify({'Prediction': predicted_sales})

# Define an endpoint to predict sales for a batch of products
@sales_predictor_api.post('/v1/productbatch')
def predict_sales_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)
    input_data['Store_Establishment_Year'] = input_data['Store_Establishment_Year'].astype('object')
    
    # Make predictions for the batch data and convert raw predictions into a readable format
    predicted_sales = [round(x, 2) for x in model.predict(input_data.drop("Product_Id",axis=1)).tolist()]

    prod_id_list = input_data.Product_Id.values.tolist()
    output_dict = dict(zip(prod_id_list, predicted_sales))

    return output_dict

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
