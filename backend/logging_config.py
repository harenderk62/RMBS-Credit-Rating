import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Set the log level and log file path
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("LOG_FILE", "app.log")

# configure and return a logger


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logger.setLevel(LOG_LEVEL)

    if logger.handlers:
        return logger

    # logging format: timestamp, log level, logger name, and the message
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",  # Specify the date format
    )

    # StreamHandler to output logs to the console
    stream_handler = logging.StreamHandler()
    # formatter to the stream handler
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # FileHandler to save logs to a file
    file_handler = logging.FileHandler(LOG_FILE)
    # formatter
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
