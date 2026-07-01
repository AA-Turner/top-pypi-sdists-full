"""Sets up default retry behavior for MAPI requests"""
import logging
from http import HTTPStatus
from typing import Any, Callable, TypeVar, cast

import backoff

from mcli.api.exceptions import MAPIException

logger = logging.getLogger(__name__)

MAX_RETRIES = 10  # pylint: disable=invalid-name
MAX_INTERVAL = 60  # pylint: disable=invalid-name
RETRY_EXCEPTIONS = {
    HTTPStatus.TOO_MANY_REQUESTS,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT,
}  # pylint: disable=invalid-name


def should_giveup(e: Any) -> bool:
    """
    Decides whether to give up retrying a request
    """
    e = cast(MAPIException, e)
    return e.status not in RETRY_EXCEPTIONS


_TCallable = TypeVar('_TCallable', bound=Callable[..., Any])  # pylint: disable=invalid-name


def retry_with_backoff(func: _TCallable) -> _TCallable:
    """
    Decorator that configures a default retry policy for all MAPI requests

    Args:
        func (Callable[..., Any]): The function that should be retried
    """

    return backoff.on_exception(
        backoff.expo,
        MAPIException,
        max_tries=MAX_RETRIES,
        jitter=backoff.random_jitter,
        giveup=should_giveup,
        logger=logger,
        backoff_log_level=logging.DEBUG,
        giveup_log_level=logging.DEBUG,
        max_value=MAX_INTERVAL,
    )(func)
