import streamlit as st
import pandas as pd

# Setup Finnhub client with your API key
finnhub_client = finnhub.Client(api_key="ck32do1r01qp0k7688qgck32do1r01qp0k7688r0")

# Function to fetch and display stock candles data
def display_stock_candles(symbol, start_date, end_date):
    st.subheader("Stock Candles Data")
    # Fetch candles data from Finnhub API
    candles_data = finnhub_client.stock_candles(symbol, 'D', start_date, end_date)
    # Convert to Pandas DataFrame
    df = pd.DataFrame(candles_data)
    # Display DataFrame
    st.dataframe(df)

# Function to fetch and display company profile
def display_company_profile(symbol):
    st.subheader("Company Profile")
    # Fetch company profile data from Finnhub API
    profile_data = finnhub_client.company_profile(symbol=symbol)
    # Display profile data
    st.write(profile_data)

# Sidebar
st.sidebar.title("Stocks Web App")
option = st.sidebar.selectbox("Select an Option", ["Stock Candles", "Company Profile"])

# Main content area
st.title("Stocks Web App")

if option == "Stock Candles":
    st.sidebar.subheader("Select Stock and Dates")
    symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")
    start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
    end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2022-12-31"))
    # Display stock candles data
    display_stock_candles(symbol, int(start_date.timestamp()), int(end_date.timestamp()))

elif option == "Company Profile":
    st.sidebar.subheader("Select Company")
    symbol = st.sidebar.text_input("Enter Company Symbol", value="AAPL")
    # Display company profile
    display_company_profile(symbol)
