import logging
import os
import json
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = "./logs/process.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5MB
BACKUP_COUNT = 3
LOG_FORMAT = "%(asctime)s - %(levelname)s - [%(name)s] %(message)s"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

class JsonFormatter(logging.Formatter):
    """Custom formatter to output logs in JSON format if needed."""
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def get_logger(name="log_manager", json_logging=False):
    """Creates and returns a configured logger.

    Args:
        name (str): Name of the logger.
        json_logging (bool): Whether to log in JSON format.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger
    logger.setLevel(LOG_LEVEL)
    
    #File Handler with rotation
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setLevel(LOG_LEVEL)
    
    #Srtream Handler with rotation
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(LOG_LEVEL)
    
    # formatter
    formatter = JsonFormatter if json_logging else logging.Formatter(LOG_FORMAT)
    
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger

def log_exception(logger, message, exc_info=True):
    """Helper function to log exceptions with stack traces."""
    logger.error(message, exc_info=exc_info)

logger = get_logger()
