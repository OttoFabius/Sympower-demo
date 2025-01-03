import streamlit as st
import numpy as np
import pandas as pd
from energy_functions import *  # Import your logic
import plotly.express as px

from datetime import timedelta
from visualisations import show_dayahead_use, show_dayahead_savings, show_mock_savings_history

# Read dayahead prices
prices_df = read_dayahead_prices('dayaheadprices-FI data 2023.xlsx - result.csv')
current_datetime = pd.to_datetime('2023-01-06 08:00:00')
prices_onefulldayahead = convert_df(prices_df, current_datetime)

# Generate mock data for projected energy usage for one day ahead (sine wave)
timestamps = pd.date_range(current_datetime + timedelta(hours=25), periods=24, freq="H")
energy_usage = 1000 + 500 * np.sin((timestamps.hour - 2) * np.pi / 12)  # Sine wave for energy usage

# Tabs for Control Panel and Results
tab1, tab2 = st.tabs(["Operation", "Savings"])

# Control Panel Tab
with tab1:
    st.title("Operational settings")

    # User input for price comparison
    user_price = st.number_input("Enter the energy price (EUR/MWh) for non-electric heating", value=50)

    # Toggle button
    is_boiler_off = st.checkbox("Override: turn all boilers off", value=False)
    status_color = "red" if is_boiler_off else "green"
    st.markdown(
        f'<div style="font-size:16px;">Boiler Status: '
        f'<span style="color:{status_color};">&#9679;</span> {"OVERRIDE: ALL BOILERS TURNED OFF" if is_boiler_off else "System active" }</div>',
        unsafe_allow_html=True,
    )

    # User inputs for E-boiler details
    num_boilers = st.number_input("Number of E-boilers in system:", min_value=1, value=2, step=1)
    boiler_capacity = st.number_input("Capacity per E-boiler (kW):", min_value=0, value=400, step=1)
    st.write(f"Total E-boiler capacity: {num_boilers * boiler_capacity} kW")

    # Summary
    prices_to_show = prices_onefulldayahead[prices_onefulldayahead['Day-ahead Energy Price'] < user_price]
    st.subheader('Summary')
    st.write(f"Your input energy price: {user_price} EUR")
    st.write(f"Number of hours where the boiler(s) will be on: {prices_to_show.shape[0]}")

    show_dayahead_use(prices_onefulldayahead, prices_to_show)


with tab2: # Savings Tab
    ####### Summary stats #########
    st.title("Projected one-day ahead savings")

    # Calculate and display energy savings (MWh)
    total_capacity = num_boilers * boiler_capacity  # Total capacity of all boilers

    # Calculate energy production of E-boilers for each hour (convert to MWh)
    energy_production = [min(total_capacity, usage) / 1000 for usage in energy_usage]
    # Calculate savings for each hour
    hourly_savings = [production * max(0, user_price - price) for production, price in
                      zip(energy_production, prices_onefulldayahead['Day-ahead Energy Price'])]
    # Calculate total savings
    energy_savings = sum(hourly_savings)

    st.write(f"Total energy capacity of the {num_boilers} E-boiler(s): {total_capacity} kW")
    st.write(f"Projected energy savings for the next 24 hours: {energy_savings:.2f} EUR")

    ####### End summary stats #########

    show_dayahead_savings(timestamps, energy_usage, hourly_savings, energy_production)

    show_mock_savings_history(current_datetime, energy_savings)