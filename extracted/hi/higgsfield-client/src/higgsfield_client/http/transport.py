import asyncio
import logging
import time
from typing import Any

import httpx

from higgsfield_client.exceptions import HiggsfieldClientError
from higgsfield_client.http.error import extract_error_message
from higgsfield_client.http.retry import RetryStrategy

logger = logging.getLogger(__name__)


class HttpTransport:
    def __init__(
        self,
        client: httpx.Client,
        retry_strategy: RetryStrategy,
    ):
        self._client = client
        self._retry_strategy = retry_strategy

    def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        attempt = 0

        while True:
            attempt += 1

            try:
                response = self._client.request(method, url, **kwargs)
                response.raise_for_status()
                return response

            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code

                if not self._retry_strategy.should_retry(attempt, status_code):
                    message = extract_error_message(e.response)
                    raise HiggsfieldClientError(message) from e

                delay = self._retry_strategy.get_delay(attempt)
                logger.debug(
                    f'[{attempt}/{self._retry_strategy.max_retries}] '
                    f'Retrying {method} {url} due to {status_code}; '
                    f'sleeping {delay:.1f}s'
                )
                time.sleep(delay)


class AsyncHttpTransport:
    def __init__(
        self,
        client: httpx.AsyncClient,
        retry_strategy: RetryStrategy,
    ):
        self._client = client
        self._retry_strategy = retry_strategy

    async def request(
        self,
        method: str,
        url: str,
        **kwargs: Any
    ) -> httpx.Response:
        attempt = 0

        while True:
            attempt += 1

            try:
                response = await self._client.request(method, url, **kwargs)
                response.raise_for_status()
                return response

            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code

                if not self._retry_strategy.should_retry(attempt, status_code):
                    message = extract_error_message(e.response)
                    raise HiggsfieldClientError(message) from e

                delay = self._retry_strategy.get_delay(attempt)
                logger.debug(
                    f'[{attempt}/{self._retry_strategy.max_retries}] '
                    f'Retrying {method} {url} due to {status_code}; '
                    f'sleeping {delay:.1f}s'
                )
                await asyncio.sleep(delay)
