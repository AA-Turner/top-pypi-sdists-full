import logging
import os

APP_NAME = os.getenv("APP_NAME", "nsj_gcf_utils")


def get_logger():
    return logging.getLogger(APP_NAME)
