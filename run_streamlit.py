import streamlit as st
from energy_functions import *  # Import your logic

st.title("Energy Optimization Mockup")

# User input
input_value = st.slider("Input Value", min_value=1, max_value=100, value=50)
input_value_2 = st.slider("Input Value", min_value=1, max_value=10, value=3)


#read input
prices_df = read_dayahead_prices('dayaheadprices-FI data 2023.xlsx - result.csv')
print(prices_df.head())


# Run algorithm and display output
if st.button("Optimize"):
    result = optimize_energy(input_value)
    st.success(f"Optimized Result: {result}")
