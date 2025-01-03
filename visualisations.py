import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd


def show_dayahead_use(prices_onefulldayahead, prices_to_show):
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

    return


def show_dayahead_savings(timestamps, energy_usage, hourly_savings, energy_production):
    fig_combined = go.Figure()

    # Add energy usage line
    fig_combined.add_trace(go.Scatter(
        x=timestamps, y=energy_usage / 100,
        mode='lines', name="Total Energy Usage",
        line=dict(color="blue")
    ))

    # Add savings as bars
    fig_combined.add_trace(go.Bar(
        x=timestamps, y=hourly_savings,
        name="Savings (EUR)",
        marker_color="green",
        opacity=0.6
    ))

    # Add projected energy production by E-boilers
    fig_combined.add_trace(go.Scatter(
        x=timestamps, y=[production * 10 for production in energy_production],
        mode='lines', name="Projected Energy Production",
        line=dict(color="orange", dash="dash")
    ))

    fig_combined.update_layout(
        title="Projected Energy Usage, Savings, and E-boiler Production",
        xaxis_title="Time",
        yaxis_title="Energy Usage (x10 kWh) / Savings (x10 EUR)",
        barmode="overlay",
        template="plotly_dark"
    )
    st.plotly_chart(fig_combined)

    return

def show_mock_savings_history(current_date, energy_savings):
    # Display savings so far using mock savings data

    st.title("Savings history")
    # Generate mock data for daily savings (normal distribution)
    num_days = 365
    daily_savings = np.random.normal(
        loc=energy_savings,  # Mean is the calculated daily savings
        scale=0.2 * energy_savings,  # Standard deviation is 20% of the mean
        size=num_days
    )
    daily_savings = np.maximum(daily_savings, 0)  # Ensure no negative savings

    # Calculate cumulative savings
    cumulative_savings = np.cumsum(daily_savings)

    # Create a DataFrame for visualization
    yearly_data = pd.DataFrame({
        'Day': pd.date_range(start="2023-01-01", periods=num_days, freq="D"),
        'Daily Savings': daily_savings,
        'Cumulative Savings': cumulative_savings
    })

    # Calculate total savings for the calendar year so far
    total_savings_year_so_far = cumulative_savings[current_date.dayofyear - 1]

    # Display total savings so far in the calendar year
    st.subheader(f"Total Savings for {current_date.year} So Far")
    st.write(f"Total savings for the calendar year so far: {total_savings_year_so_far:.0f} EUR")


    # User input to select the month
    selected_month = st.selectbox(
        "Select the month to display savings",
        options=pd.date_range("2024-01-01", periods=12, freq="M").strftime("%B"),
        index=current_date.month - 1  # Set default to current month
    )

    # Get the year corresponding to the selected month
    selected_year = current_date.year if selected_month == "January" else current_date.year - 1

    # Filter the data to show only the selected month
    selected_month_index = pd.to_datetime(f"2024-{selected_month}-01").month
    month_data = yearly_data[yearly_data['Day'].dt.month == selected_month_index]

     # If the selected month is the current month, limit the data to the past days
    if selected_month == current_date.strftime("%B"):
        month_data = month_data[month_data['Day'] <= current_date]

    # Calculate total savings for the selected month
    savings_selected_month = month_data['Daily Savings'].sum()


    # Display savings for the selected month
    st.subheader(f"Savings for {selected_month} {selected_year}")
    st.write(f"Savings for {selected_month} {selected_year}: {savings_selected_month:.0f} EUR")

    # Visualization: Daily Savings for selected month
    fig_daily = px.bar(
        month_data, x='Day', y='Daily Savings',
        title=f"Daily Savings for {selected_month} {selected_year}",
        labels={"Daily Savings": "Savings (EUR)", "Day": "Date"},
        template="plotly_dark"
    )
    st.plotly_chart(fig_daily)

    return
