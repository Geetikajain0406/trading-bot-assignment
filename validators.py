from bot.logging_config import logger


VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT", "STOP_MARKET"]


def check_symbol(symbol):
    if not symbol or len(symbol) < 3:
        raise ValueError(f"Symbol looks wrong: '{symbol}'. Try something like BTCUSDT")
    return symbol.upper().strip()


def check_side(side):
    side_upper = side.upper().strip()
    if side_upper not in VALID_SIDES:
        raise ValueError(f"Side must be BUY or SELL, you gave: '{side}'")
    return side_upper


def check_order_type(order_type):
    ot = order_type.upper().strip()
    if ot not in VALID_ORDER_TYPES:
        raise ValueError(f"Order type must be one of {VALID_ORDER_TYPES}, got: '{order_type}'")
    return ot


def check_quantity(qty):
    try:
        qty_float = float(qty)
    except (ValueError, TypeError):
        raise ValueError(f"Quantity must be a number, got: '{qty}'")
    
    if qty_float <= 0:
        raise ValueError(f"Quantity must be greater than 0, got: {qty_float}")
    
    return qty_float


def check_price(price):
    try:
        price_float = float(price)
    except (ValueError, TypeError):
        raise ValueError(f"Price must be a number, got: '{price}'")
    
    if price_float <= 0:
        raise ValueError(f"Price must be greater than 0, got: {price_float}")
    
    return price_float


def validate_all_inputs(symbol, side, order_type, quantity, price=None):
    logger.debug("Validating user inputs...")

    clean_symbol = check_symbol(symbol)
    clean_side = check_side(side)
    clean_type = check_order_type(order_type)
    clean_qty = check_quantity(quantity)

    clean_price = None
    if clean_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders!")
        clean_price = check_price(price)
    
    if clean_type == "STOP_MARKET":
        if price is None:
            raise ValueError("Stop price is required for STOP_MARKET orders!")
        clean_price = check_price(price)

    logger.debug("All inputs look good.")
    return clean_symbol, clean_side, clean_type, clean_qty, clean_price
