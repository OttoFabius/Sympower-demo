"""
● 1MW e-boiler cost ~50k
● A common alternative heat source for greenhouses in Finland is woodchip and it’s
equivalent to paying 50 EUR/MWh of electricity
● Greenhouses electricity contracts are often linked to the day-ahead prices (instead of
paying a fixed fee).
Day-ahead prices in Finland are becoming more and more volatile - in 2024 it was the
● EU country with the most negative power prices (article here)
● Attached to this assignment, you can find a .csv file with the Finnish hourly day-ahead
data for 2023.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def read_dayahead_prices(fname):
    df = pd.read_csv(fname)

    return df


def optimize_energy(input_value):
    # Example logic: minimize cost given constraints
    result = np.sqrt(input_value) * 1  # Replace with your actual logic
    return result

def convert_df(df, current_datetime, hours_from=24, hours_to=48):
    """
    Filters the DataFrame to select rows where the 'utc_timestamp' is between 24 and 48 hours ahead 
    from the current UTC time.
    
    Parameters:
        df (pandas.DataFrame): The DataFrame containing the 'utc_timestamp' column.
        
    Returns:
        pandas.DataFrame: A filtered DataFrame with rows that have 'utc_timestamp' between 24 and 48 hours ahead.
    """
    # Ensure 'utc_timestamp' is a datetime column
    df['utc_timestamp'] = pd.to_datetime(df['utc_timestamp'])

    # Define the time range (24 to 48 hours ahead)
    time_24_hours_ahead = current_datetime + timedelta(hours=hours_from)
    time_48_hours_ahead = current_datetime + timedelta(hours=hours_to)

    # Filter the DataFrame for rows where 'utc_timestamp' is between 24 and 48 hours ahead
    df_filtered = df[(df['utc_timestamp'] >= time_24_hours_ahead) & (df['utc_timestamp'] <= time_48_hours_ahead)]

    return df_filtered

if __name__=="__main__":
    import streamlit as st
    import plotly.express as px


    #read dayahead prices
    prices_df = read_dayahead_prices('dayaheadprices-FI data 2023.xlsx - result.csv')
    current_datetime = pd.to_datetime('2023-01-06 08:00:00')
    prices_onefulldayahead = convert_df(prices_df, current_datetime)  
    print(prices_df.head())
    print(prices_df.shape)

    # User input for price comparison
    user_price = st.number_input("Enter a price to compare with the hourly prices (USD):", min_value=0.0, format="%.2f")

    # Create Plotly figure for visualization
    fig = px.line(prices_onefulldayahead, x='utc_timestamp', y='Day-ahead Energy Price', title='Hourly Electricity Prices vs User Input Price', markers=True)

    # Highlight only the points where the price is lower than the user input price
    prices_to_show = prices_onefulldayahead[prices_onefulldayahead['Day-ahead Energy Price'] < user_price]
    # st.dataframe(prices_to_show)

    # Add scatter plot to highlight prices above the user input
    fig.add_scatter(x=prices_to_show['utc_timestamp'], y=prices_to_show['Day-ahead Energy Price'],
                    mode='markers', marker=dict(color='red', size=10, line=dict(width=2, color='black')),
                    name="Prices Above User Input")

    fig.update_layout(xaxis_title="Hour", yaxis_title="Price (EUR)", template="plotly_dark")

    # Show the plot in Streamlit
    st.plotly_chart(fig)

    # Provide a summary of the comparison
    st.subheader('Comparison Summary')
    st.write(f"Your input price: {user_price} EUR")
    st.write(f"Number of hours where the price is **lower** than your input: {prices_to_show.shape[0]}")



    # st.subheader('Hourly Electricity Prices (USD)')
    # st.dataframe(prices_df)

    # # Plot hourly prices using Plotly
    # current_datetime = pd.to_datetime('2023-01-06 08:00:00')

    # prices_onefulldayahead = convert_df(prices_df, current_datetime)
    # fig = px.line(prices_onefulldayahead, x='utc_timestamp', y='Day-ahead Energy Price', title='Hourly Electricity Prices for 24-48 hours from now)', markers=True)
    # fig.update_layout(xaxis_title="Hour", yaxis_title="Price (USD)", template="plotly_dark")

    # # Show the plot in Streamlit
    # st.plotly_chart(fig)