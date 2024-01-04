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

# Sidebar for price selection
selected_price = st.sidebar.selectbox('Select a Price:', sorted(df['price'].unique()))

# Sidebar for date selection with reversed order
selected_date = st.sidebar.selectbox('Select a Date:', sorted(df['day'].unique(), reverse=True))

# Filter the DataFrame to find all rows corresponding to the selected price and date
selected_rows = df.query('price == @selected_price and day == @selected_date')

# Display information based on the selected price and date
if not selected_rows.empty:
    st.subheader('Selected House Information')
    for index, row in selected_rows.iterrows():
        st.write(f'Date: {row["day"].strftime("%Y-%m-%d")}')
        st.write(f'Description: {row["description"]}')
        st.write(f'Number of Rooms: {row["rooms"]}')
        st.write(f'Square Meters: {row["m2"]}')
        st.write(f'Bathrooms: {row["bathrooms"]}')
        st.write(f'Price €: {row["price"]}')
        st.write(f'Price R$: {round(row["price"]*eur_to_brl,2)}')
        st.write(f'Link: {row["links"]}')
        st.markdown('---')  # Add a divider line between information for different houses

    # Calcula e exibe o preço médio e desvio padrão com base nos dados da data mais recente
    avg_price_recent_date = df[df['day'] == df['day'].max()]['price'].mean()
    std_dev_price_recent_date = df[df['day'] == df['day'].max()]['price'].std()
    max_price = df[df['day'] == df['day'].max()]['price'].max()
    min_price = df[df['day'] == df['day'].max()]['price'].min()


    st.sidebar.write(f'Average Price €: {avg_price_recent_date:.2f}')
    st.sidebar.write(f'Standard Deviation €: {std_dev_price_recent_date:.2f}')
    st.sidebar.write(f'Max Price €: {max_price:.2f}')
    st.sidebar.write(f'Lower Price €: {min_price:.2f}')



else:
    st.warning('No data found for the selected price.')
