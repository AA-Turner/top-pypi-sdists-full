import logging
from http import HTTPStatus

import aiohttp
from aiohttp_retry import ExponentialRetry

logger = logging.getLogger("dap")

REQUEST_RETRY_COUNT = 3


class CustomExponentialRetry(ExponentialRetry):
    def __init__(self) -> None:
        super().__init__(
            attempts=REQUEST_RETRY_COUNT,
            methods={"GET", "POST"},
            statuses={HTTPStatus.TOO_MANY_REQUESTS.value},
            retry_all_server_errors=True,
            exceptions={aiohttp.ServerDisconnectedError},
        )

    def get_timeout(self, attempt: int, response: aiohttp.ClientResponse | None = None) -> float:
        if response is not None and response.status == HTTPStatus.TOO_MANY_REQUESTS.value:
            timeout = 30
            retry_after = response.headers.get("Retry-After")
            if retry_after is not None:
                try:
                    timeout = int(retry_after)
                except ValueError:
                    logger.warning(
                        f'Invalid "Retry-After" header value: {retry_after}, using default timeout {timeout} seconds'
                    )

            logger.debug(f'Received error "Too Many Requests", retrying after {timeout} seconds')
            return timeout

        return super().get_timeout(attempt, response)
