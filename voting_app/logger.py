import logging
import logging.handlers
from config import Config

def setup_logger():
    """Setup logging configuration"""
    logger = logging.getLogger('voting_app')
    logger.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Error file handler
    error_handler = logging.FileHandler(Config.ERROR_LOG_FILE)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    # Success file handler
    success_handler = logging.FileHandler(Config.SUCCESS_LOG_FILE)
    success_handler.setLevel(logging.INFO)
    success_handler.setFormatter(formatter)
    logger.addHandler(success_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()
