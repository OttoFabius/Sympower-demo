import streamlit as st
from energy_functions import *  # Import your logic
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

