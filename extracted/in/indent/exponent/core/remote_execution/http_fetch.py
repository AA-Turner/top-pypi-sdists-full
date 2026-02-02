"""HTTP fetch implementation for remote execution client."""

import logging

import httpx

from exponent.core.remote_execution.cli_rpc_types import (
    HttpRequest,
    HttpResponse,
)

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 30.0
DEFAULT_USER_AGENT = "Indent-HTTP-Client/1.0"


async def fetch_http_content(http_request: HttpRequest) -> HttpResponse:
    """
    Fetch content from an HTTP URL and return the response.

    Args:
        http_request: HttpRequest containing URL, method, headers, and timeout

    Returns:
        HttpResponse with status code, content, and error message if any
    """
    logger.info(f"Fetching {http_request.method} {http_request.url}")

    try:
        # Set up timeout
        timeout = (
            http_request.timeout
            if http_request.timeout is not None
            else DEFAULT_TIMEOUT
        )

        # Set up headers with default User-Agent
        headers = http_request.headers or {}
        if "User-Agent" not in headers:
            headers["User-Agent"] = DEFAULT_USER_AGENT

        # Create HTTP client with timeout
        async with httpx.AsyncClient(timeout=timeout) as client:
            # Make the HTTP request
            response = await client.request(
                method=http_request.method,
                url=http_request.url,
                headers=headers,
            )

            # Get response content as text
            try:
                content = response.text
            except UnicodeDecodeError:
                # If content can't be decoded as text, provide a fallback
                content = f"Binary content ({len(response.content)} bytes)"
                logger.warning(
                    f"Could not decode response content as text for {http_request.url}"
                )

            logger.info(
                f"HTTP {http_request.method} {http_request.url} -> {response.status_code}"
            )

            return HttpResponse(
                status_code=response.status_code,
                content=content,
                error_message=None,
            )

    except httpx.TimeoutException:
        error_msg = f"Request to {http_request.url} timed out after {timeout} seconds"
        return HttpResponse(
            status_code=None,
            content="",
            error_message=error_msg,
        )

    except httpx.RequestError as e:
        error_msg = f"Request error for {http_request.url}: {e!s}"
        return HttpResponse(
            status_code=None,
            content="",
            error_message=error_msg,
        )

    except Exception as e:
        error_msg = f"Unexpected error fetching {http_request.url}: {e!s}"
        return HttpResponse(
            status_code=None,
            content="",
            error_message=error_msg,
        )
