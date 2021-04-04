from datetime import date

import pandas as pd
import yfinance as yf
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns


YEARS_BACK = 10
DEFAULT_COLUMN = "Adj Close"


def read_tickers_from_file(file_name):
    with open(file_name) as f:
        return f.read().split("\n")


def download_stock_data_for_tickers(tickers, column_name, years_back):
    start_date = date.today().replace(year=date.today().year - years_back)
    return yf.download(tickers, start_date)[column_name]


def build_portfolio_weights(stock_data, weights_filename):

    # Calculate expected returns and sample covariance
    if isinstance(stock_data, pd.Series):
        stock_data = stock_data.to_frame()

    mu = expected_returns.mean_historical_return(stock_data)
    S = risk_models.sample_cov(stock_data)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    raw_weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    ef.save_weights_to_file(weights_filename)  # saves to file
    ef.portfolio_performance(verbose=True)
    return cleaned_weights


def build_portfolio_from_ticker_file(ticker_file, column_name=DEFAULT_COLUMN, years_back=YEARS_BACK):
    ticker_group_title = ticker_file.replace(".txt", "")
    tickers = read_tickers_from_file(ticker_file)
    data = download_stock_data_for_tickers(tickers, column_name, years_back)
    return build_portfolio_weights(data, f"weights{YEARS_BACK}-{ticker_group_title}.csv")

def build_dollar_investment_value(weights, ammount):
    portfolio = {}
    for ticker, weight in weights.items():
        portfolio[ticker] = weight * ammount
    return portfolio


if __name__ == "__main__":
    weights = build_portfolio_from_ticker_file("topstocks.txt")

    non_zero_weights = {k:v for k,v in weights.items() if v != 0.0}
    print(build_dollar_investment_value(non_zero_weights, 2_000))