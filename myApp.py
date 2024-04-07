from datetime import datetime, timedelta
import streamlit as st
import finnhub
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.express as px

# Setup Finnhub client with your API key
finnhub_client = finnhub.Client(api_key="co8vr39r01qj5gtjfu0gco8vr39r01qj5gtjfu10")
st.sidebar.title("Stocks Web App")
option = st.sidebar.selectbox("Select an Option", ["Home", "Stocks", "Expert"])

def display_expert_section():
    st.markdown("### Welcome to the Expert Section!")
    # Add content specific to the expert section here
    st.write("This section contains resources and tools tailored for experts in trading stocks.")

    selected_stock = st.selectbox("Select a stock",
                                  ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA", "NFLX", "NVDA", "INTC", "CSCO"])

    ticker = selected_stock
    startdate = st.date_input("Start Date")
    enddate = st.date_input("End Date")

    data = yf.download(ticker, start=startdate, end=enddate)
    fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
    st.plotly_chart(fig)


def display_intermediate_section():
    st.markdown("### Welcome to the Intermediate Section!")
    # Add content specific to the intermediate section here
    st.write("This section contains resources and tools for users with intermediate experience in trading stocks.")

    # List of stock symbols for intermediate section
    intermediate_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'NVDA', 'NFLX', 'DIS', 'V',
                           'PYPL', 'INTC', 'ADBE', 'CMCSA', 'PEP', 'CSCO', 'AVGO', 'COST', 'TXN', 'QCOM']

    st.subheader("Stock Quotes for Intermediate Stocks:")

    # Create a list to store stock quotes
    stock_data = []

    # Fetch and display current price for each stock
    for stock_symbol in intermediate_stocks:
        quote = finnhub_client.quote(stock_symbol)
        stock_data.append({"Stock Symbol": stock_symbol, "Current Price": quote['c']})

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(stock_data)

    # Display the dataframe as a table
    st.table(df)

    # Data Visualization - Bar Chart for stock prices
    st.subheader("Bar Chart: Stock Prices for Intermediate Stocks")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df['Stock Symbol'], df['Current Price'], color='blue')
    ax.set_xlabel('Stock Symbol')
    ax.set_ylabel('Current Price')
    ax.set_title('Stock Prices for Intermediate Stocks')
    plt.xticks(rotation=45)
    st.pyplot(fig)



def plot_stock_price(symbol, start_date, end_date, interval_seconds):
    # Fetch historical price data from Finnhub API
    historical_data = []
    current_date = start_date
    while current_date <= end_date:
        # Fetch quote for each date
        quote = finnhub_client.quote(symbol)
        historical_data.append({"t": current_date.timestamp(), "c": quote['c']})
        current_date += timedelta(days=1)

    # Convert to Pandas DataFrame
    df = pd.DataFrame(historical_data)

    # Set index as date
    df['t'] = pd.to_datetime(df['t'], unit='s')
    df.set_index('t', inplace=True)

    # Resample data based on interval
    df = df.resample(interval_seconds, closed='left').agg({'c': 'last'}).dropna()

    # Create Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['c'], label='Close Price')
    plt.title(f"{symbol} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(plt)


def display_beginner_section():
    st.markdown("### Welcome to the Beginner Section!")
    # Add content specific to the beginner section here
    st.write("This section contains resources and tools for users new to trading stocks.")

    # List of stock symbols for beginner section
    beginner_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'NFLX', 'DIS', 'V']

    st.subheader("Stock Quotes for Beginner Stocks:")

    # Create a list to store stock quotes
    stock_data = []

    # Fetch and display current price for each stock
    for stock_symbol in beginner_stocks:
        quote = finnhub_client.quote(stock_symbol)
        stock_data.append({"Stock Symbol": stock_symbol, "Current Price": quote['c']})

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(stock_data)

    # Display the dataframe as a table
    st.table(df)

# Main content area
st.title("Stocks Web App")

if option == "Home":
    st.sidebar.subheader("Home")

    st.write("Please answer the following questions:")

    # Question 1: Radio Buttons
    q1 = st.radio("1. Do you have prior experience in trading stocks?", ("Yes", "No"))

    # Question 2: Slider
    q2 = st.slider("2. On a scale of 1 to 10, how confident are you in trading stocks?", 1, 10, 5)

    # Question 3: Radio Buttons
    q3_options = ["Beginner", "Intermediate", "Expert"]
    q3 = st.radio("3. What is your level of expertise in trading stocks?", q3_options)

    q4_options = ["1", "2", "3", "4", "5", "More than 5"]
    q4 = st.radio("4. How many stocks have you invested in before?", q4_options)

    # Question 5: Selectbox
    q5_options = ["Technology", "Finance", "Healthcare", "Energy"]
    q5 = st.selectbox("5. Which sector are you most interested in?", q5_options)

    # Button to submit answers
    if st.button("Submit"):
        st.success("Answers submitted successfully!")

        # Switch to appropriate section based on answers
        if q1 == "Yes" and q2 >= 8 and q3 == "Expert":
            display_expert_section()
        elif q1 == "Yes" or q2 >= 5:
            display_intermediate_section()
        else:
            display_beginner_section()

elif option == "Stocks":
    st.sidebar.subheader("Stocks")

    # Here you can add logic to display stocks-related content

elif option == "Expert":
    display_expert_section()
