# Binance Futures Testnet Trading Bot

A simple Python CLI tool to place orders on Binance Futures Testnet (USDT-M).

## What it does

- Place MARKET, LIMIT, and STOP_MARKET orders
- Supports BUY and SELL
- Input validation with clear error messages
- Logs everything to a file

## Setup

### 1. Get Testnet API Keys

1. Go to https://testnet.binancefuture.com
2. Sign in or register
3. Click on "API Key" and generate your keys
4. Copy the API key and secret key

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup your .env file

Copy the example file:

```bash
cp .env.example .env
```

Then open `.env` and paste your actual API key and secret:

```
BINANCE_API_KEY=abc123yourkeyhere
BINANCE_SECRET_KEY=xyz789yoursecrethere
```

## How to run

### Market Order (BUY)

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.01
```

### Market Order (SELL)

```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --qty 0.01
```

### Limit Order

Price is required for limit orders:

```bash
python cli.py --symbol ETHUSDT --side BUY --type LIMIT --qty 0.1 --price 3000
```

### Stop Market Order (Bonus feature)

```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --qty 0.01 --price 65000
```

## Sample output

```
--- Order Request Summary ---
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
------------------------------

=== Order Response ===
  Order ID     : 3785234
  Symbol       : BTCUSDT
  Status       : FILLED
  Side         : BUY
  Type         : MARKET
  Qty Ordered  : 0.01
  Qty Filled   : 0.01
  Avg Price    : 67423.50
======================

SUCCESS: Order was placed on Binance Futures Testnet!
```

## Logs

All logs are saved to `logs/bot.log`. Sample logs from test orders are in `logs/` folder.

## Project structure

```
trading_bot/
  bot/
    __init__.py
    client.py         # handles API calls and signing
    orders.py         # order placement + output display
    validators.py     # checks user input before sending
    logging_config.py # sets up file + console logging
  cli.py              # CLI entry point (argparse)
  .env.example        # copy this to .env and add your keys
  requirements.txt
  README.md
  logs/
    market_order.log
    limit_order.log
```

## Assumptions

- Only USDT-M Futures testnet is supported (not COIN-M)
- Leverage and margin settings use whatever default the testnet account has
- For STOP_MARKET, the `--price` flag is used as the stop trigger price
- Network must have access to testnet.binancefuture.com
