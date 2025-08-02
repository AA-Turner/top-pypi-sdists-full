# arpakit

import asyncio
import logging
from datetime import timedelta
from typing import Any

import aiohttp
import requests
from aiohttp_socks import ProxyConnector

from arpakitlib.ar_json_util import transfer_data_to_json_str
from arpakitlib.ar_sleep_util import sync_safe_sleep, async_safe_sleep
from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


def sync_make_http_request(
        *,
        method: str = "GET",
        url: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        max_tries_: int = 9,
        proxy_url_: str | None = None,
        raise_for_status_: bool = False,
        not_raise_for_statuses_: list[int] | None = None,
        timeout_: timedelta | float = timedelta(seconds=15).total_seconds(),
        enable_logging_: bool = False,
        exception_class_: type[Exception] | None = None,
        **kwargs
) -> requests.Response:
    if isinstance(timeout_, float):
        timeout_ = timedelta(seconds=timeout_)
    raise_for_type(timeout_, timedelta)

    tries_counter = 0

    kwargs["method"] = method
    kwargs["url"] = url
    if headers is not None:
        kwargs["headers"] = headers
    if params is not None:
        kwargs["params"] = params
    if proxy_url_:
        kwargs["proxies"] = {
            "http": proxy_url_,
            "https": proxy_url_
        }
    if timeout_ is not None:
        kwargs["timeout"] = timeout_.total_seconds()
    if "allow_redirects" not in kwargs:
        kwargs["allow_redirects"] = True

    if enable_logging_:
        _logger.info(f"try http {method} {url} {params}")

    while True:
        tries_counter += 1
        try:
            response = requests.request(**kwargs)
            if raise_for_status_:
                if not_raise_for_statuses_ and response.status_code in not_raise_for_statuses_:
                    if enable_logging_:
                        _logger.info(f"ignored status {response.status_code} {method} {url} {params}")
                else:
                    try:
                        response.raise_for_status()
                    except requests.HTTPError as raise_for_status_exception:
                        if enable_logging_:
                            try:
                                json_data = response.json()
                                _logger.error(
                                    f"bad status {method} {url} {params}"
                                    f"{transfer_data_to_json_str(data=json_data, beautify=True)}"
                                )
                            except Exception:
                                try:
                                    text = response.text
                                    _logger.error(
                                        f"bad status {method} {url} {params}"
                                        f"{text}"
                                    )
                                except Exception:
                                    pass
                        raise raise_for_status_exception
            if enable_logging_:
                _logger.info(f"good try http {method} {url} {params}")
            return response
        except Exception as exception:
            if enable_logging_:
                _logger.warning(
                    f"{tries_counter}/{max_tries_}, bad try {method} {url} {params}, exception={exception}"
                )
            if tries_counter >= max_tries_:
                if exception_class_ is not None:
                    raise exception_class_(exception)
                else:
                    raise exception
            sync_safe_sleep(timedelta(seconds=0.1).total_seconds())
            continue


async def async_make_http_request(
        *,
        method: str = "GET",
        url: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        max_tries_: int = 9,
        proxy_url_: str | None = None,
        raise_for_status_: bool = False,
        not_raise_for_statuses_: list[int] | None = None,
        timeout_: timedelta | None = timedelta(seconds=15),
        enable_logging_: bool = False,
        exception_class_: type[Exception] | None = None,
        **kwargs
) -> aiohttp.ClientResponse:
    tries_counter = 0

    kwargs["method"] = method
    kwargs["url"] = url
    if headers is not None:
        kwargs["headers"] = headers
    if params is not None:
        kwargs["params"] = params
    if timeout_ is not None:
        kwargs["timeout"] = aiohttp.ClientTimeout(total=timeout_.total_seconds())
    if "allow_redirects" not in kwargs:
        kwargs["allow_redirects"] = True

    proxy_connector: ProxyConnector | None = None
    if proxy_url_:
        proxy_connector = ProxyConnector.from_url(proxy_url_)

    if enable_logging_:
        _logger.info(f"try http {method} {url} {params}")

    while True:
        tries_counter += 1
        try:
            async with aiohttp.ClientSession(connector=proxy_connector) as session:
                async with session.request(**kwargs) as response:
                    if raise_for_status_:
                        if not_raise_for_statuses_ and response.status in not_raise_for_statuses_:
                            if enable_logging_:
                                _logger.info(
                                    f"ignored status {response.status} {method} {url} {params}"
                                )
                        else:
                            try:
                                response.raise_for_status()
                            except aiohttp.ClientResponseError as raise_for_status_exception:
                                if enable_logging_:
                                    try:
                                        json_data = await response.json()
                                        _logger.error(
                                            f"bad status {method} {url} {params}"
                                            f"{transfer_data_to_json_str(data=json_data, beautify=True)}"
                                        )
                                    except Exception:
                                        try:
                                            text = await response.text()
                                            _logger.error(
                                                f"bad status {method} {url} {params}"
                                                f"{text}"
                                            )
                                        except Exception:
                                            pass
                                raise raise_for_status_exception
                    await response.read()
                    if enable_logging_:
                        _logger.info(f"good try {method} {url} {params}")
                    return response
        except Exception as exception:
            if enable_logging_:
                _logger.warning(
                    f"{tries_counter}/{max_tries_}, bad try {method} {url} {params}, exception={exception}"
                )
            if tries_counter >= max_tries_:
                if exception_class_ is not None:
                    raise exception_class_(exception)
                else:
                    raise exception
            await async_safe_sleep(timedelta(seconds=0.1).total_seconds())
            continue


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
