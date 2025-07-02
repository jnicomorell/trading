import argparse
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf


def download_data(symbol: str, period: str = '1y') -> pd.DataFrame:
    """Download historical data for the given symbol."""
    data = yf.download(symbol, period=period, progress=False)
    if data.empty:
        raise ValueError(f"No data found for {symbol}")
    return data


def compute_signals(
    data: pd.DataFrame,
    short: int = 20,
    long: int = 50,
    rsi_period: int = 14,
) -> pd.DataFrame:
    """Compute buy/sell signals using moving averages and RSI."""
    data = data.copy()
    data['SMA_SHORT'] = data['Close'].rolling(short).mean()
    data['SMA_LONG'] = data['Close'].rolling(long).mean()

    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(rsi_period).mean()
    avg_loss = loss.rolling(rsi_period).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    data['SIGNAL'] = 0
    buy_cond = (data['SMA_SHORT'] > data['SMA_LONG']) & (data['RSI'] < 30)
    sell_cond = (data['SMA_SHORT'] < data['SMA_LONG']) & (data['RSI'] > 70)
    data.loc[buy_cond, 'SIGNAL'] = 1
    data.loc[sell_cond, 'SIGNAL'] = -1
    return data


def print_latest(data: pd.DataFrame):
    """Print the latest close, RSI and trading signal."""
    latest = data.dropna().iloc[-1]
    date = latest.name.date()
    close = latest['Close']
    short = latest['SMA_SHORT']
    long_ = latest['SMA_LONG']
    rsi = latest['RSI']
    signal = 'BUY' if latest['SIGNAL'] == 1 else 'SELL' if latest['SIGNAL'] == -1 else 'HOLD'
    print(
        f"{date}: Close={close:.2f}, SMA_SHORT={short:.2f}, SMA_LONG={long_:.2f}, RSI={rsi:.2f}, Signal={signal}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Moving average and RSI trading helper"
    )
    parser.add_argument('symbol', help='Ticker symbol, e.g. AAPL')
    parser.add_argument('--period', default='1y', help='History period to download (default 1y)')
    args = parser.parse_args()

    data = download_data(args.symbol, args.period)
    data = compute_signals(data)
    print_latest(data)


if __name__ == '__main__':
    main()
