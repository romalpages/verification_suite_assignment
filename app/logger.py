import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture everything

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # INFO Log
    info_handler = logging.FileHandler(os.path.join(LOG_DIR, "info.log"))
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    # ERROR Log
    error_handler = logging.FileHandler(os.path.join(LOG_DIR, "error.log"))
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # WARNING Log
    warning_handler = logging.FileHandler(os.path.join(LOG_DIR, "warning.log"))
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(formatter)

    # DEBUG Log
    debug_handler = logging.FileHandler(os.path.join(LOG_DIR, "debug.log"))
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    # Add handlers to root logger
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(debug_handler)
