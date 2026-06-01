import time
import hmac
import hashlib
import requests
from bot.logging_config import logger


TESTNET_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = TESTNET_URL
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key
        })

    def make_signature(self, params_string):
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            params_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature

    def get_server_time(self):
        # just checking if connection works
        url = f"{self.base_url}/fapi/v1/time"
        resp = self.session.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def send_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        url = f"{self.base_url}/fapi/v1/order"

        # build the params
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "timestamp": int(time.time() * 1000),
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"  # good till cancelled
        
        if order_type == "STOP_MARKET":
            params["stopPrice"] = stop_price

        # create query string and sign it
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        params["signature"] = self.make_signature(query_string)

        logger.debug(f"Sending order request to: {url}")
        logger.debug(f"Order params: symbol={symbol}, side={side}, type={order_type}, qty={quantity}")

        try:
            response = self.session.post(url, params=params, timeout=15)
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Raw response: {response.text}")

            if response.status_code != 200:
                error_data = response.json()
                error_msg = error_data.get("msg", "Unknown API error")
                error_code = error_data.get("code", "N/A")
                logger.error(f"API Error {error_code}: {error_msg}")
                raise Exception(f"API Error {error_code}: {error_msg}")

            return response.json()

        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Binance testnet. Check your internet!")
            raise Exception("Connection failed. Are you connected to the internet?")

        except requests.exceptions.Timeout:
            logger.error("Request timed out waiting for Binance response")
            raise Exception("Request timed out. Try again.")

        except requests.exceptions.RequestException as e:
            logger.error(f"Some request error happened: {str(e)}")
            raise Exception(f"Request failed: {str(e)}")

    def get_open_orders(self, symbol):
        url = f"{self.base_url}/fapi/v1/openOrders"
        params = {
            "symbol": symbol,
            "timestamp": int(time.time() * 1000)
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        params["signature"] = self.make_signature(query_string)

        logger.debug(f"Fetching open orders for {symbol}")
        resp = self.session.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
