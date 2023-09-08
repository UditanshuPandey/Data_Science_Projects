import json
import pickle
import numpy as np
import math
import streamlit as st

result  = None
__locations = None
__data_columns = None
__model = None

def get_estimated_price(location,sqft,bhk,bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    if loc_index >= 0>= 0:
        x[loc_index] = 1

    price = round(__model.predict([x])[0], 2)
    strp = ' lakhs'

    if math.log10(price) >= 2:
        price = price / 100
        price = round(price, 2)
        strp = " crores"

    return str(price) + strp

def get_location_names():
    return __locations

def load_saved_files():
    print("loading saved files...start")
    global __data_columns
    global __locations

    with open("F:\Data_Science_And_ML\Real_Estate_Price_Prediction\columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    global __model
    if __model is None:
        with open("F:\Data_Science_And_ML\Real_Estate_Price_Prediction\Banglore_home_prices_model.pickle", "rb") as f:
            __model = pickle.load(f)
    print("loading saved files...done")

def main():
    load_saved_files()
    global result
    st.title("Bangalore House Price Predictor")
    html_temp = """
           <div>
           <h2>House Price Prediction ML app</h2>
           </div>
           """
    st.markdown(html_temp, unsafe_allow_html=True)
    total_sqft = st.text_input("Total_sqft")
    bathroom = st.text_input("Number of Bathrooms")
    bhk = st.text_input("BHK")
    location = st.selectbox("Location", get_location_names())

    if st.button("Predict"):
        result = get_estimated_price(location, total_sqft, bathroom, bhk)

    st.success(f"Price = {result}")

if __name__ == "__main__":
    main()