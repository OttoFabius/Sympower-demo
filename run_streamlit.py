import streamlit as st
from energy_functions import optimize_energy  # Import your logic

st.title("Energy Optimization Mockup")

# User input
input_value = st.slider("Input Value", min_value=1, max_value=100, value=50)

# Run algorithm and display output
if st.button("Optimize"):
    result = optimize_energy(input_value)
    st.success(f"Optimized Result: {result}")
