import logging
import os
from application.utils import util_functions

# Constants
DEFAULT_LOG_LEVEL = "DEBUG"
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

CONF_PATH = "application/configs/conf.yaml"
SIDEBAR_PATH = "application/utils/sidebar.yaml"


def get_config_from_yaml(path: str) -> dict:
    """Retrieve configuration from a given YAML path."""
    return util_functions.get_dict_from_yaml(path)


def get_logger() -> logging.Logger:
    """Create and return a logger with the appropriate level set."""
    log_level = os.environ.get("LOG_LEVEL", DEFAULT_LOG_LEVEL)
    level = LOG_LEVELS.get(log_level, logging.DEBUG)  # default to DEBUG if log_level is not recognized
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    return logger


# Global instances
logger = get_logger()
conf = get_config_from_yaml(CONF_PATH)
sidebar = get_config_from_yaml(SIDEBAR_PATH)
