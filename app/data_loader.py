import yfinance as yf
import pandas as pd
from typing import List

def download_data(tickers: List[str], start: str, end: str) -> pd.DataFrame:
    data = yf.download(tickers, start=start, end=end)
    if data is None or getattr(data, 'empty', True):
        raise ValueError(f"No data was downloaded for tickers: {tickers} in range {start} to {end}.")
    # Handle MultiIndex columns
    if isinstance(data.columns, pd.MultiIndex):
        # Try 'Adj Close' first
        if ('Adj Close',) in data.columns or ('Adj Close', tickers[0]) in data.columns:
            try:
                adj_close = data['Adj Close']
                if isinstance(adj_close, pd.Series):
                    adj_close = adj_close.to_frame()
                return adj_close.dropna()
            except KeyError:
                pass  # Fallback to 'Close' below
        # Fallback to 'Close'
        if ('Close',) in data.columns or ('Close', tickers[0]) in data.columns:
            close = data['Close']
            if isinstance(close, pd.Series):
                close = close.to_frame()
            return close.dropna()
        print(f"Downloaded columns: {data.columns}")
        raise KeyError("Neither 'Adj Close' nor 'Close' found in downloaded data. Available columns: {}".format(list(data.columns)))
    else:
        # Single index columns
        if 'Adj Close' in data.columns:
            adj_close = data['Adj Close']
            if isinstance(adj_close, pd.Series):
                adj_close = adj_close.to_frame()
            return adj_close.dropna()
        elif 'Close' in data.columns:
            close = data['Close']
            if isinstance(close, pd.Series):
                close = close.to_frame()
            return close.dropna()
        print(f"Downloaded columns: {data.columns}")
        raise KeyError("Neither 'Adj Close' nor 'Close' found in downloaded data. Available columns: {}".format(list(data.columns))) 