"""Helpers for working with ESI."""

import datetime as dt
import logging
import random
from time import sleep
from typing import Optional

import requests

from django.utils.timezone import now

from app_utils.logging import LoggerAddTag

from . import __title__, __version__
from ._app_settings import (
    APPUTILS_ESI_DAILY_DOWNTIME_END,
    APPUTILS_ESI_DAILY_DOWNTIME_START,
    APPUTILS_ESI_ERROR_LIMIT_THRESHOLD,
)

logger = LoggerAddTag(logging.getLogger(__name__), __title__)


class EsiStatusException(Exception):
    """EsiStatus base exception."""

    def __init__(self, message):
        super().__init__()
        self.message = message


class EsiOffline(EsiStatusException):
    """ESI is offline error."""

    def __init__(self):
        """:meta private:"""
        super().__init__("ESI appears to be offline.")


class EsiDailyDowntime(EsiOffline):
    """ESI is offline due to daily downtime."""

    def __init__(self):
        """:meta private:"""
        super().__init__()
        self.message = "Assuming ESI is offline during it's daily downtime."


class EsiErrorLimitExceeded(EsiStatusException):
    """ESI error limit exceeded error."""

    def __init__(self, retry_in: float = 60) -> None:
        """:meta private:"""
        super().__init__("The ESI error limit has been exceeded.")
        self._retry_in = float(retry_in)

    @property
    def retry_in(self) -> float:
        """Time until next error window in seconds."""
        return self._retry_in


class EsiStatus:
    """Current status of ESI (immutable)."""

    MAX_JITTER = 20

    def __init__(
        self,
        is_online: bool,
        error_limit_remain: Optional[int] = None,
        error_limit_reset: Optional[int] = None,
        is_daily_downtime: bool = False,
    ) -> None:
        self._is_online = bool(is_online)
        self._is_daily_downtime = is_daily_downtime
        if error_limit_remain is None or error_limit_reset is None:
            self._error_limit_remain = None
            self._error_limit_reset = None
        else:
            self._error_limit_remain = int(error_limit_remain)
            self._error_limit_reset = int(error_limit_reset)

    @property
    def is_ok(self) -> bool:
        """True if ESI is online and below error limit, else False."""
        return self.is_online and not self.is_error_limit_exceeded

    @property
    def is_daily_downtime(self) -> bool:
        """True if status was created during daily downtime time frame."""
        return self._is_daily_downtime

    @property
    def is_online(self) -> bool:
        """True if ESI is online, else False."""
        return self._is_online

    @property
    def error_limit_remain(self) -> Optional[int]:
        """Amount of remaining errors in current window."""
        return self._error_limit_remain

    @property
    def error_limit_reset(self) -> Optional[int]:
        """Seconds until current error window resets."""
        return self._error_limit_reset

    @property
    def is_error_limit_exceeded(self) -> bool:
        """True when remain is below the threshold, else False.

        Will also return False if remain/reset are not defined
        """
        return bool(
            self.error_limit_remain
            and self.error_limit_reset
            and self.error_limit_remain <= APPUTILS_ESI_ERROR_LIMIT_THRESHOLD
        )

    def error_limit_reset_w_jitter(self, max_jitter: Optional[int] = None) -> int:
        """Calc seconds to retry in order to reach next error window incl. jitter."""
        if self.error_limit_reset is None:
            return 0
        if not max_jitter or max_jitter < 1:
            max_jitter = self.MAX_JITTER
        return self.error_limit_reset + int(random.uniform(1, max_jitter))

    def raise_for_status(self):
        """Raise an exception if ESI if offline or the error limit is exceeded."""
        if not self.is_online:
            if self.is_daily_downtime:
                raise EsiDailyDowntime()
            raise EsiOffline()
        if self.is_error_limit_exceeded:
            raise EsiErrorLimitExceeded(retry_in=self.error_limit_reset_w_jitter())


def fetch_esi_status(ignore_daily_downtime: bool = False) -> EsiStatus:
    """Determine the current ESI status.

    Args:
        ignore_daily_downtime: When True will always make a request to ESI \
            even during the daily downtime
    """
    is_daily_downtime = _is_daily_downtime()
    if not ignore_daily_downtime and is_daily_downtime:
        return EsiStatus(is_online=False, is_daily_downtime=True)
    try:
        response = _request_esi_status()
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        logger.warning("Network error when trying to call ESI", exc_info=True)
        return EsiStatus(is_online=False, is_daily_downtime=is_daily_downtime)
    if not response.ok:
        is_online = False
    else:
        try:
            is_online = not response.json().get("vip")
        except ValueError:
            is_online = False
    try:
        remain = int(response.headers.get("X-Esi-Error-Limit-Remain"))  # type: ignore
        reset = int(response.headers.get("X-Esi-Error-Limit-Reset"))  # type: ignore
    except TypeError:
        logger.warning("Failed to parse HTTP headers: %s", response.headers)
        return EsiStatus(is_online=is_online, is_daily_downtime=is_daily_downtime)
    logger.debug(
        "ESI status: is_online: %s, error_limit_remain = %s, error_limit_reset = %s",
        is_online,
        remain,
        reset,
    )
    return EsiStatus(
        is_online=is_online,
        error_limit_remain=remain,
        error_limit_reset=reset,
        is_daily_downtime=is_daily_downtime,
    )


def _is_daily_downtime() -> bool:
    """Determine if we currently are in the daily downtime period."""
    downtime_start = _calc_downtime(APPUTILS_ESI_DAILY_DOWNTIME_START)
    downtime_end = _calc_downtime(APPUTILS_ESI_DAILY_DOWNTIME_END)
    return now() >= downtime_start and now() <= downtime_end


def _calc_downtime(hours_float: float) -> dt.datetime:
    hour, minute = _convert_float_hours(hours_float)
    return now().replace(hour=hour, minute=minute)


def _convert_float_hours(hours_float: float) -> tuple:
    """Convert float hours into int hours and int minutes for datetime."""
    hours = int(hours_float)
    minutes = int((hours_float - hours) * 60)
    return hours, minutes


def _request_esi_status() -> requests.Response:
    """Fetch current status from ESI. Retry on common HTTP errors."""
    max_retries = 3
    retry_count = 0
    while True:
        response = requests.get(
            "https://esi.evetech.net/latest/status/",
            timeout=(5, 30),
            headers={"User-Agent": f"{__package__};{__version__}"},
        )
        if response.status_code not in {
            502,  # HTTPBadGateway
            503,  # HTTPServiceUnavailable
            504,  # HTTPGatewayTimeout
        }:
            break

        retry_count += 1
        if retry_count > max_retries:
            break

        logger.warning(
            "HTTP status code %s - Try %s/%s",
            response.status_code,
            retry_count,
            max_retries,
        )

        wait_secs = 0.1 * (random.uniform(2, 4) ** (retry_count - 1))
        sleep(wait_secs)

    return response


def retry_task_if_esi_is_down(self):
    """Retry current celery task if ESI is not online or error threshold is exceeded.

    This function has to be called from inside a celery task!

    Args:
        self: Current celery task from `@shared_task(bind=True)`
    """
    try:
        fetch_esi_status().raise_for_status()
    except EsiOffline as ex:
        countdown = (5 + int(random.uniform(1, 10))) * 60
        logger.warning(
            "ESI appears to be offline. Trying again in %d seconds.", countdown
        )
        raise self.retry(countdown=countdown) from ex
    except EsiErrorLimitExceeded as ex:
        logger.warning(
            "ESI error limit threshold reached. Trying again in %s seconds", ex.retry_in
        )
        raise self.retry(countdown=ex.retry_in) from ex
