import os
import datetime

sl_debug = os.environ.get("SL_DEBUG", "false").lower() == "true"


def info(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"{timestamp} [SEALIGHTS] - INFO: {message}")


def error(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"{timestamp} [SEALIGHTS] - ERROR: {message}")


def warn(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"{timestamp} [SEALIGHTS] - WARN: {message}")


def debug(message):
    if not sl_debug:
        return
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"{timestamp} [SEALIGHTS] - DEBUG: {message}")
