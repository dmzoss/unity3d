import logging
import sys

def setup_logger(name) -> logging.Logger:
    """
    Set up a logger with consistent configuration across all modules.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # Avoid adding handlers multiple times
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    return logger