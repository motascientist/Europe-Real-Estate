import streamlit as st
import pandas as pd
import yfinance as yf

# Load the DataFrame from a CSV file
df = pd.read_csv('Processed_data.csv')

# Sort the DataFrame by the most recent date
df['day'] = pd.to_datetime(df['day'])
df = df.sort_values(by=['day', 'price'])
df.dropna(inplace=True)

# Obter a taxa de câmbio do Euro para Real usando o Yahoo Finance
eur_to_brl = yf.download('EURBRL=X')['Close'][-1]

# Streamlit settings
st.set_page_config(page_title='Real Estate App', page_icon=':house:', layout='wide')

# Show the 10 best prices based on m2-€ column within a specified price interval
st.subheader('Top 10 Prices based on m²')

# Manually input the price interval
min_price = st.text_input('Enter Min Price:', df['price'].min())
max_price = st.text_input('Enter Max Price:', df['price'].max())

# Convert input to float
min_price = float(min_price) if min_price else df['price'].min()
max_price = float(max_price) if max_price else df['price'].max()

# Filter data within the specified price interval
filtered_data = df[(df['price'] >= min_price) & (df['price'] <= max_price)]

# Display the top 10 prices based on m2-€
top_10_prices = filtered_data.nsmallest(10, 'm2-€')

for i, row in top_10_prices.iterrows():
    st.write(f'Description: {row["description"]}')
    st.write(f'Number of Rooms: {row["rooms"]}')
    st.write(f'Square Meters: {row["m2"]}')
    st.write(f'Bathrooms: {row["bathrooms"]}')
    st.write(f'Price m² €: {round(row["m2-€"],2)}')
    st.write(f'Price €: {row["price"]}')
    st.write(f'Price R$: {round(row["price"] * eur_to_brl, 2)}')
    st.write(f'Link: {row["links"]}')
    st.markdown('---')  # Add a divider line between information for different houses

if top_10_prices.empty:
    st.warning('No data found for the selected price.')

