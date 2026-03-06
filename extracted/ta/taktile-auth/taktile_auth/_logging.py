import logging
import typing as t

_logger: logging.Logger

try:
    from aws_lambda_powertools import Logger

    _logger = t.cast(logging.Logger, Logger(service="taktile-auth"))
except ImportError:  # pragma: no cover
    _logger = logging.getLogger("taktile_auth")


def get_logger() -> logging.Logger:
    return _logger
