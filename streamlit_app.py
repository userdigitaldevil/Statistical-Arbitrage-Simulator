import streamlit as st
import pandas as pd
from app.data_loader import download_data
from app.cointegration import find_cointegrated_pairs
from app.backtest import backtest_pair
import matplotlib.pyplot as plt

st.title("Statistical Arbitrage Simulator")

tickers = st.text_input("Enter tickers (comma separated)", "MSFT,AAPL,GOOG,AMZN,META").split(",")
start = st.date_input("Start date", value=pd.to_datetime("2020-01-01"))
end = st.date_input("End date", value=pd.to_datetime("2023-01-01"))

if st.button("Download Data"):
    data = download_data(tickers, str(start), str(end))
    st.write(data.tail())

    pairs, _, _ = find_cointegrated_pairs(data)
    st.write("Cointegrated pairs:", pairs)

    if pairs:
        S1 = data[pairs[0][0]]
        S2 = data[pairs[0][1]]
        results = backtest_pair(S1, S2)
        st.write("Backtest Results")
        fig, ax = plt.subplots()
        ax.plot(results['cum_returns'])
        ax.set_title("Cumulative Returns")
        st.pyplot(fig) 