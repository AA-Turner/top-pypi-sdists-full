import logging
from typing import Any

import aiohttp

from .dap_error import DAPClientError
from .networking import get_content_type

logger = logging.getLogger("dap")


async def read_json_body(response: aiohttp.ClientResponse) -> Any:
    """
    Reads and parses a response body as JSON.

    :param response: The HTTP response whose body to parse.
    :returns: The parsed JSON payload.
    :raises DAPClientError: The response body is not JSON.
    """

    content_type = get_content_type(response.headers.get("Content-Type", ""))
    if content_type == "application/json":
        return await response.json()

    response_text = await response.text()
    if response_text:
        logger.error(
            f"Unexpected response from server (HTTP status {response.status}). "
            f"Unable to parse the HTTP response. \n{response_text}"
        )

    raise DAPClientError(
        f"Unexpected response from server (HTTP status {response.status}). "
        "Unable to parse the HTTP response."
    )
