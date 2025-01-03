import streamlit as st
import numpy as np
import pandas as pd
from energy_functions import *  # Import your logic
import plotly.express as px
import plotly.graph_objects as go

# Read dayahead prices
prices_df = read_dayahead_prices('dayaheadprices-FI data 2023.xlsx - result.csv')
current_datetime = pd.to_datetime('2023-01-06 08:00:00')
prices_onefulldayahead = convert_df(prices_df, current_datetime)

# Generate mock data for projected energy usage for one day ahead (sine wave)
timestamps = pd.date_range(current_datetime+timedelta(hours=25), periods=24, freq="H")
energy_usage = 1000 + 500 * np.sin((timestamps.hour - 2) * np.pi / 12)  # Sine wave for energy usage


# Tabs for Control Panel and Results
tab1, tab2 = st.tabs(["Control Panel", "Savings"])

# Control Panel Tab
with tab1:
    st.title("Control Panel")

    # User input for price comparison
    user_price = st.number_input("Enter the energy price (EUR/MWh) for non-electric heating", value=50.0, format="%.2f")

    # Toggle button
    is_boiler_off = st.checkbox("Override: turn all boilers off", value=False)
    status_color = "red" if is_boiler_off else "green"
    st.markdown(
        f'<div style="font-size:16px;">Boiler Status: '
        f'<span style="color:{status_color};">&#9679;</span> {"OVERRIDE: ALL BOILERS TURNED OFF" if is_boiler_off else "System active" }</div>',
        unsafe_allow_html=True,
    )


    # Example boiler; Electro Industries Industrial Electric Boiler:

    # Model: EB-NB-120-480
    # Capacity: 120 kW, 480V 3-phase, 409,560 BTU
    # Price: $16,059.00 (approximately €14,000)
    # Source: BlueRidge Company

    # User inputs for E-boiler details
    num_boilers = st.number_input("Number of E-boilers in system:", min_value=1, value=2, step=1)
    boiler_capacity = st.number_input("Capacity per E-boiler (kW):", min_value=0.0, value=400., step=1.)
    st.write(f"Total E-boiler capacity: {num_boilers*boiler_capacity} kWh ")


    # Summary
    prices_to_show = prices_onefulldayahead[prices_onefulldayahead['Day-ahead Energy Price'] < user_price]
    st.subheader('Summary')
    st.write(f"Your input energy price: {user_price} EUR")
    st.write(f"Number of hours where the boiler(s) will be on: {prices_to_show.shape[0]}")

    # Visualization: Hourly Prices vs User Input
    fig = px.line(prices_onefulldayahead, x='utc_timestamp', y='Day-ahead Energy Price',
                  title='One day ahead boiler use', markers=True)

    # Highlight prices below user input
    fig.add_scatter(
        x=prices_to_show['utc_timestamp'], y=prices_to_show['Day-ahead Energy Price'],
        mode='markers', marker=dict(color='green', size=10, line=dict(width=2, color='green')),
        name="Boiler use"
    )
    fig.update_layout(xaxis_title="Hour", yaxis_title="Price (EUR)", template="plotly_dark")
    st.plotly_chart(fig)


# Results Tab
with tab2:
    st.title("Projected one-day ahead savings")

    # Calculate and display energy savings (MWh)
    total_capacity = num_boilers * boiler_capacity  # Total capacity of all boilers

    # Calculate energy production of E-boilers for each hour (convert to MWh)
    energy_production = [min(total_capacity, usage)/1000 for usage in energy_usage]
    # Calculate savings for each hour
    hourly_savings = [production * max(0, user_price - price) for production, price in zip(energy_production, prices_onefulldayahead['Day-ahead Energy Price'])]
    # Calculate total savings
    energy_savings = sum(hourly_savings)


    # energy_savings = sum(min(total_capacity, usage)/1000 * max(0, user_price - price) for usage, price in zip(energy_usage, prices_onefulldayahead['Day-ahead Energy Price']))
    # energy_savings = total_capacity * len(prices_to_show) * user_price  # Simplified calculation
    st.write(f"Total energy capacity of E-boilers: {total_capacity} kWh")
    st.write(f"Projected energy savings for the day: {energy_savings:.2f} EUR")



    # -------------------------------------------------------------------

    # Create a usage chart
    fig_usage = go.Figure()
    fig_usage.add_trace(go.Scatter(x=timestamps, y=energy_usage, mode='lines', name="Energy Usage"))

    # Add Boiler On/Off status as red dots
    if is_boiler_off==False:
        boiler_times = prices_to_show['utc_timestamp']
        boiler_prices = [1000 + 500 * np.sin((time.hour - 2) * np.pi / 12) for time in boiler_times]
        fig_usage.add_trace(
            go.Scatter(
                x=boiler_times, y=boiler_prices,
                mode='markers',
                marker=dict(color='red', size=8),
                name="Boiler ON"
            )
        )
    elif is_boiler_off:
        st.write("NB: Boilers are turned of with override")


    fig_usage.update_layout(
        title="Projected Energy Usage and Boiler Status",
        xaxis_title="Time",
        yaxis_title="Energy Usage for hour (kWh)",
        template="plotly_dark"
    )
    st.plotly_chart(fig_usage)


