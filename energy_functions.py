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

import pandas as pd
from datetime import datetime, timedelta


def read_dayahead_prices(fname):
    df = pd.read_csv(fname)

    return df


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