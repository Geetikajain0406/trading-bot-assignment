import logging
import os


def setup_logger():
    # make logs folder if not there
    if not os.path.exists("logs"):
        os.makedirs("logs")

    my_logger = logging.getLogger("trading_bot")
    my_logger.setLevel(logging.DEBUG)

    # file handler - saves everything to file
    file_handler = logging.FileHandler("logs/bot.log")
    file_handler.setLevel(logging.DEBUG)

    # console handler - shows info and above on screen
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    log_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)

    my_logger.addHandler(file_handler)
    my_logger.addHandler(console_handler)

    return my_logger


logger = setup_logger()
