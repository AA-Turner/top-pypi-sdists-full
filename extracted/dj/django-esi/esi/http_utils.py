"""HTTP building blocks shared by the ESI and SSO clients.

This module must not import `esi.models` (directly or via `esi.helpers`),
so that `esi.models` and `esi.managers` can use it without a circular import.
"""
import logging
from datetime import datetime, timedelta, timezone
from string import capwords
from typing import Any

from httpx2 import Limits, Timeout

from esi import app_settings

from . import __title__, __url__, __version__

logger = logging.getLogger(__name__)


def pascal_case_string(string: str) -> str:
    """
    Convert a string to PascalCase by capitalizing the first letter of each word and removing spaces,
    but only if the string contains spaces or hyphens.

    This function checks if the input string contains spaces or hyphens. If so, it replaces hyphens with spaces,
    capitalizes the first letter of each word, removes the spaces, and returns the resulting PascalCase string.
    If the input string does not contain spaces or hyphens, it is returned unchanged.

    Behaviour:
    Any string containing spaces or hyphens will be converted to PascalCase.
    Strings without spaces or hyphens will be returned unchanged.
    This gives you the opportunity to use already formatted strings as needed.

    Examples:
    - "app name" -> "AppName"
    - "app-name" -> "AppName"
    - "appname" -> "appname"
    - "AppName" -> "AppName"
    - "appName" -> "appName"
    - "app_name" -> "app_name"

    :param string: The input string to be converted to PascalCase.
    :type string: str
    :return: The PascalCase formatted string, or the original string if no spaces or hyphens are present.
    :rtype: str
    """

    # Check if the string contains spaces or hyphens
    if any(c in string for c in (" ", "-")):
        # Replace hyphens with spaces, capitalize each word, and remove spaces
        return capwords(string.replace("-", " ")).replace(" ", "")

    # Return the original string if no spaces or hyphens are present
    return string


def build_user_agent(ua_appname: str, ua_version: str, ua_url: str | None = None) -> str:
    """
    AppName/1.2.3 (foo@example.com; +https://gitlab.com/) Django-ESI/1.2.3 (+https://gitlab.com/allianceauth/django-esi)
    Contact Email will be inserted from app_settings.
    Args:
        ua_appname (str): Application Name, PascalCase
        ua_version (str): Application Version, SemVer
        ua_url (str | None): Application URL (Optional)
    Returns:
        str: User-Agent string
    """

    # Enforce PascalCase for `ua_appname` and strip whitespace
    sanitized_ua_appname = pascal_case_string(ua_appname)
    sanitized_appname = pascal_case_string(__title__)

    return (
        f"{sanitized_ua_appname}/{ua_version} "
        f"({app_settings.ESI_USER_CONTACT_EMAIL}{f'; +{ua_url})' if ua_url else ')'} "
        f"{sanitized_appname}/{__version__} (+{__url__})"
    )


def build_django_esi_user_agent() -> str:
    """
    Django-ESI's own User-Agent, for requests not made on behalf of a specific app.
    DjangoEsi/1.2.3 (foo@example.com; +https://gitlab.com/allianceauth/django-esi)
    Returns:
        str: User-Agent string
    """
    return (
        f"{pascal_case_string(__title__)}/{__version__} "
        f"({app_settings.ESI_USER_CONTACT_EMAIL}; +{__url__})"
    )


def build_timeout() -> Timeout:
    return Timeout(
        connect=app_settings.ESI_REQUESTS_CONNECT_TIMEOUT,
        read=app_settings.ESI_REQUESTS_READ_TIMEOUT,
        write=app_settings.ESI_REQUESTS_WRITE_TIMEOUT,
        pool=app_settings.ESI_REQUESTS_POOL_TIMEOUT
    )


def build_limits() -> Limits:
    return Limits(
        max_connections=app_settings.ESI_CONNECTION_POOL_MAX_CONNECTIONS,
        max_keepalive_connections=app_settings.ESI_CONNECTION_POOL_MAX_KEEPALIVE,
        keepalive_expiry=app_settings.ESI_CONNECTION_POOL_KEEPALIVE_EXPIRY
    )


MAX_CACHE_TIME = 60 * 60 * 24  # 24h


def time_to_expiry(expires_header: str) -> int:
    """Calculate cache TTL from Expires header
    Args:
        expires_header (str): The value of the Expires header '%a, %d %b %Y %H:%M:%S %Z'
    Returns:
        int: The cache TTL in seconds
    """
    try:
        expires_dt = datetime.strptime(str(expires_header), '%a, %d %b %Y %H:%M:%S %Z')
        if expires_dt.tzinfo is None:
            expires_dt = expires_dt.replace(tzinfo=timezone.utc)
        return max(int((expires_dt - datetime.now(timezone.utc)).total_seconds()), 0)
    except ValueError:
        return 0


def unpack_cache_control(headers: dict[str, Any]) -> int:
    """Calculate cache TTL from Cache-Control header,
    Falling back to Expires header if no max-age is set
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching#expires_or_max-age

    Args:
        headers (dict): request headers to generate ttl for cache
    Returns:
        int: The cache TTL in seconds up to max cache time.

        The value of the Cache-Control header, 'private, max-age=#####, immutable'
        The value of the date header, '%a, %d %b %Y %H:%M:%S %Z'
    """
    _date = False
    _expires = 0
    if "date" in headers:
        date_format = "%a, %d %b %Y %H:%M:%S %Z"
        try:
            _date = datetime.strptime(headers.get("date"), date_format)
            _date = _date.replace(tzinfo=timezone.utc)
        except ValueError as e:
            logger.warning(f"Error converting date string: {e}")
    if "cache-control" in headers:
        try:
            _header = headers.get("cache-control").split(",")
            _sections = {}
            _expires = 0
            for sec in _header:
                if "=" in sec:
                    _cont = sec.strip().split("=")
                    _sections[_cont[0]] = _cont[1]
            if "max-age" in _sections:
                _max_age = min(MAX_CACHE_TIME, int(_sections.get("max-age", 0)))
                if _date:
                    # Calculate expiry from date of request + max age
                    _expire_date = _date + timedelta(seconds=_max_age)
                    _expire_time: timedelta = _expire_date - datetime.now(timezone.utc)
                    _expires = int(_expire_time.total_seconds())
                else:
                    # Date header failed nbd, so just use max-age as the ttl
                    _expires = _max_age
            elif "no-store" in _sections:
                _expires = 0
            # elif "no-cache": is intentionally missing here.
                # no-cache is mostly delegated off to E-Tags that are handled elsewhere.
                # no-cache endpoints **can have** short HTTP caches 60 seconds, so why not keep
            else:
                # Cache Control exists, but no max-age is defined, fall back to legacy Expires header
                _expires = time_to_expiry(str(headers.get('Expires')))
        except ValueError as e:
            logger.warning(f"Error converting date strings: {e}")
            return 0
        return max(_expires, 0)
    return 0  # please only call this function if cache-control header exists
