# trading

This project provides a simple script to fetch historical stock prices and evaluate a moving average and RSI strategy.

## Requirements

- Python 3.12
- `pandas`
- `yfinance`

Install dependencies:

```bash
pip install pandas yfinance
```

## Usage

Run `trading.py` with the ticker symbol of interest:

```bash
python trading.py AAPL
```

The script downloads one year of price history and prints the latest closing price, RSI value and a trading signal generated when the short moving average crosses the long one while RSI is oversold or overbought.
