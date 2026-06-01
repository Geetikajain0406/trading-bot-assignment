from bot.logging_config import logger
from bot.validators import validate_all_inputs


def place_order(client, symbol, side, order_type, quantity, price=None):
    # validate everything first
    clean_symbol, clean_side, clean_type, clean_qty, clean_price = validate_all_inputs(
        symbol, side, order_type, quantity, price
    )

    # print summary before sending
    print("\n--- Order Request Summary ---")
    print(f"  Symbol     : {clean_symbol}")
    print(f"  Side       : {clean_side}")
    print(f"  Type       : {clean_type}")
    print(f"  Quantity   : {clean_qty}")
    if clean_price:
        label = "Stop Price" if clean_type == "STOP_MARKET" else "Price"
        print(f"  {label:<11}: {clean_price}")
    print("------------------------------\n")

    logger.info(f"Placing {clean_type} {clean_side} order for {clean_qty} {clean_symbol}")

    # figure out which price param to pass
    order_price = None
    stop_price = None

    if clean_type == "LIMIT":
        order_price = clean_price
    elif clean_type == "STOP_MARKET":
        stop_price = clean_price

    try:
        result = client.send_order(
            symbol=clean_symbol,
            side=clean_side,
            order_type=clean_type,
            quantity=clean_qty,
            price=order_price,
            stop_price=stop_price
        )

        logger.info(f"Order placed successfully! Order ID: {result.get('orderId')}")
        return result

    except Exception as e:
        logger.error(f"Failed to place order: {str(e)}")
        raise


def show_order_result(order_data):
    print("\n=== Order Response ===")
    print(f"  Order ID     : {order_data.get('orderId', 'N/A')}")
    print(f"  Symbol       : {order_data.get('symbol', 'N/A')}")
    print(f"  Status       : {order_data.get('status', 'N/A')}")
    print(f"  Side         : {order_data.get('side', 'N/A')}")
    print(f"  Type         : {order_data.get('type', 'N/A')}")
    print(f"  Qty Ordered  : {order_data.get('origQty', 'N/A')}")
    print(f"  Qty Filled   : {order_data.get('executedQty', 'N/A')}")

    avg_price = order_data.get("avgPrice", "0")
    if avg_price and float(avg_price) > 0:
        print(f"  Avg Price    : {avg_price}")

    order_price = order_data.get("price", "0")
    if order_price and float(order_price) > 0:
        print(f"  Limit Price  : {order_price}")

    print("======================\n")
