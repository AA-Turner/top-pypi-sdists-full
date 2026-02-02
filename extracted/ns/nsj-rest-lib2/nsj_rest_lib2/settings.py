import logging
import os

ESCOPO_RESTLIB2 = os.environ["ESCOPO_RESTLIB2"]
APP_NAME = os.getenv("APP_NAME", "nsj_rest_lib2")

ENV = os.getenv("ENV", "dev").lower()

if ENV in ("dev", "local"):
    MIN_TIME_SOURCE_REFRESH = 0
else:
    MIN_TIME_SOURCE_REFRESH = int(os.getenv("MIN_TIME_SOURCE_REFRESH", "15"))


def _get_env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "t", "yes", "y", "on")


EDLS_FROM_REDIS = _get_env_bool("EDLS_FROM_REDIS", True)


def get_logger():
    return logging.getLogger(APP_NAME)
