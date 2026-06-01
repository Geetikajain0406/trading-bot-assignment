import argparse
import os
import sys
from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.orders import place_order, show_order_result
from bot.logging_config import logger


def load_credentials():
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    secret_key = os.getenv("BINANCE_SECRET_KEY")

    if not api_key or not secret_key:
        print("ERROR: Please set BINANCE_API_KEY and BINANCE_SECRET_KEY in your .env file")
        logger.error("API credentials not found in environment")
        sys.exit(1)

    return api_key, secret_key


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Simple Binance Futures Testnet Trading Bot",
        epilog="Example: python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.01"
    )

    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair symbol e.g. BTCUSDT, ETHUSDT"
    )

    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL"],
        help="Order side: BUY or SELL"
    )

    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        choices=["MARKET", "LIMIT", "STOP_MARKET"],
        help="Order type: MARKET, LIMIT, or STOP_MARKET"
    )

    parser.add_argument(
        "--qty",
        required=True,
        help="Quantity to trade e.g. 0.01"
    )

    parser.add_argument(
        "--price",
        default=None,
        help="Price for LIMIT orders or stop price for STOP_MARKET (not needed for MARKET)"
    )

    return parser


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    logger.info("Trading bot started")
    logger.info(f"Args received: symbol={args.symbol}, side={args.side}, type={args.order_type}, qty={args.qty}, price={args.price}")

    # load api keys
    api_key, secret_key = load_credentials()

    # create client
    client = BinanceClient(api_key, secret_key)

    # quick connectivity check
    try:
        server_time = client.get_server_time()
        logger.debug(f"Connected to Binance testnet. Server time: {server_time}")
    except Exception as e:
        print(f"Could not connect to Binance testnet: {e}")
        logger.error(f"Connectivity check failed: {e}")
        sys.exit(1)

    # place the order
    try:
        order_result = place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.qty,
            price=args.price
        )

        show_order_result(order_result)
        print("SUCCESS: Order was placed on Binance Futures Testnet!")
        logger.info("Order completed successfully.")

    except ValueError as ve:
        print(f"\nVALIDATION ERROR: {ve}")
        logger.error(f"Validation failed: {ve}")
        sys.exit(1)

    except Exception as e:
        print(f"\nERROR: {e}")
        logger.error(f"Order failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
