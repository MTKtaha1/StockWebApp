from datetime import datetime, timedelta, date
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.express as px
import numpy as np
import finnhub
from statsmodels.tsa.arima.model import ARIMA
from plotly import graph_objs as go


from streamlit_option_menu import option_menu

# Setup Finnhub client with your API key
finnhub_client = finnhub.Client(api_key="co8vr39r01qj5gtjfu0gco8vr39r01qj5gtjfu10")
st.sidebar.title("Stocks Web App")
option = st.sidebar.selectbox("Select an Option", ["Home", "Beginner", "Intermediate", "Expert"])

option2 = st.sidebar.selectbox("Stocks Prediction", ["Stocks", "Map"])


def get_session_state():
    if 'section' not in st.session_state:
        st.session_state.section = "Home"
    return st.session_state


def display_expert_section():
    get_session_state()
    st.markdown("### Welcome to the Expert Section!")
    # Add content specific to the expert section here
    st.write("This section contains resources and tools tailored for experts in trading stocks.")

    selected_stock = st.selectbox("Select a stock",
                                  ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NFLX", "NVDA", "INTC", "CSCO"])

    ticker = selected_stock

    # Set default start date to 1 month before today
    default_start_date = datetime.now() - timedelta(days=30)
    start_date = st.date_input("Start Date", value=default_start_date)
    end_date = st.date_input("End Date")

    data = yf.download(ticker, start=start_date, end=end_date)
    fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
    st.plotly_chart(fig)

    pricing, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "Top 10 News"])

    with pricing:
        st.header('Pricing Movements')
        my_data = data
        my_data['% Change'] = my_data['Adj Close'] / data['Adj Close'].shift(1)
        my_data.dropna(inplace=True)
        st.write(my_data)
        annual = my_data['% Change'].mean() * 252 * 100
        st.write('Annual Return is', annual, '%')
        stdev = np.std(my_data['% Change']) * np.sqrt(252)
        st.write('Standard Deviation is ', stdev * 100, '%')
        st.write('Risk Adj. Return is ', annual / (stdev * 100))

    # with data:
    #     st.write('Fundamental')
    #
    # with news:
    #     st.write('News')


def display_intermediate_section():
    st.markdown("### Welcome to the Intermediate Section!")
    # Add content specific to the intermediate section here
    st.write("This section contains resources and tools for users with intermediate experience in trading stocks.")

    # List of stock symbols for intermediate section
    intermediate_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'NFLX', 'DIS', 'V',
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

session_state = get_session_state()

if option == "Home":

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

        # Switch to appropriate section based on answers
        if q1 == "Yes" and q2 >= 8 and q3 == "Expert":
            st.success("Based on your answers, you should refer to the expert section.")
        elif q1 == "Yes" or q2 >= 5:
            st.success("Based on your answers, you should refer to the intermediate section.")
        else:
            st.success("Based on your answers, you should refer to the Beginner section.")


elif option == "Beginner":
    display_beginner_section()

elif option == "Intermediate":
    display_intermediate_section()

elif option == "Expert":
    display_expert_section()



if option2 == "Stocks":
    START = "2015-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    st.title('Stock Forecast App')

    stocks = ('GOOG', 'AAPL', 'MSFT', 'GME')
    selected_stock = st.selectbox('Select dataset for prediction', stocks)

    n_years = st.slider('Years of prediction:', 1, 4)
    period = n_years * 365


    @st.cache_data
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data


    data_load_state = st.text('Loading data...')
    data = load_data(selected_stock)
    data_load_state.text('Loading data... done!')

    st.subheader('Raw data')
    st.write(data.tail())


    # Plot raw data
    def plot_raw_data():
        fig, ax = plt.subplots()
        ax.plot(data['Date'], data['Open'], label='stock_open')
        ax.plot(data['Date'], data['Close'], label='stock_close')
        ax.set_title('Time Series data with Rangeslider')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        st.pyplot(fig)


    plot_raw_data()

    # Forecast with ARIMA
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    model = ARIMA(df_train['y'], order=(5, 1, 0))
    fit_model = model.fit()

    forecast = fit_model.forecast(steps=period)

    future_dates = pd.date_range(start=df_train['ds'].iloc[-1], periods=period + 1)
    forecast.index = future_dates[1:]

    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())

    st.write(f'Forecast plot for {n_years} years')

    # Prepare data for 3D plot
    forecast_df = forecast.reset_index()
    forecast_df.columns = ['Date', 'Forecast']
    forecast_df['Index'] = forecast_df.index

    # Create 3D scatter plot
    fig4 = px.scatter_3d(forecast_df,
                         x="Index",
                         y="Forecast",
                         z="Date")
    fig4.update_scenes(zaxis_autorange="reversed")
    st.plotly_chart(fig4)

if option2 == "Map":
    st.text_input("Enter your")
