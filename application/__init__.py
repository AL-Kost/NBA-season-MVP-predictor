import logging
import os

from .utils import util_functions


def get_conf():
    return util_functions.get_dict_from_yaml("application/configs/conf.yaml")

def get_sidebar():
    return util_functions.get_dict_from_yaml('application/utils/sidebar.yaml')


def get_logger():
    log_level = os.environ.get("LOG_LEVEL", "DEBUG")
    if log_level == "DEBUG":
        level = logging.DEBUG
    elif log_level == "INFO":
        level = logging.INFO
    elif log_level == "WARNING":
        level = logging.WARNING
    elif log_level == "ERROR":
        level = logging.ERROR
    elif log_level == "CRITICAL":
        level = logging.CRITICAL
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    return logger


logger = get_logger()
conf = get_conf()
sidebar = get_sidebar()
