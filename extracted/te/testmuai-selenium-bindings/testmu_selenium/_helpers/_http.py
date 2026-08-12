"""HTTP retry helper for AUTOMIND requests.

Extracted from V2 source. Tenacity-based retry on
transient 5xx; 4xx pass through; fresh httpx.Client per request to avoid
stale connections.
"""
import logging
import time

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

# Transient HTTP status codes that should trigger a retry
# 408: Request Timeout, 429: Too Many Requests, 499: Client Closed Request
# 502: Bad Gateway, 503: Service Unavailable, 504: Gateway Timeout
logging.getLogger("httpx").setLevel(logging.ERROR)  # only surface httpx errors
_log = logging.getLogger(__name__)
TRANSIENT_HTTP_STATUS_CODES = {408, 429, 499, 502, 503, 504}


class TransientHTTPError(Exception):
    """Exception raised for transient HTTP errors that should be retried."""

    def __init__(self, status_code: int, message: str = ""):
        self.status_code = status_code
        self.message = message or f"Transient HTTP error with status code {status_code}"
        super().__init__(self.message)


class KaneAICreditsExhausted(Exception):
    """Raised when an AI call is refused because the organization is out of credits."""

    kaneai_error_code = "INSUFFICIENT_CREDITS"


def _is_transient_http_error(status_code: int) -> bool:
    """Check if the HTTP status code is a transient error that should be retried."""
    return status_code in TRANSIENT_HTTP_STATUS_CODES


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((
        httpx.ConnectError,
        httpx.RemoteProtocolError,
        httpx.ReadError,
        httpx.ConnectTimeout,
        TransientHTTPError,
    )),
    reraise=True,
)
def make_http_request_with_retry(
    method: str,
    url: str,
    headers: dict = None,
    data: str = None,
    json_data: dict = None,
    timeout: int = 120,
    auth: tuple = None,
    silent: bool = False,
) -> httpx.Response:
    """
    Makes HTTP requests using httpx with fresh connections and retry mechanism.
    Uses a fresh connection per request to avoid stale connection issues.

    Retries on:
    - Connection errors (ConnectError, RemoteProtocolError, ReadError, ConnectTimeout)
    - Transient HTTP status codes (408, 429, 499, 502, 503, 504)

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        url: The URL to make the request to
        headers: Optional headers dict
        data: Optional request body as string (for raw data)
        json_data: Optional request body as dict (for JSON data)
        timeout: Request timeout in seconds (default: 120)
        auth: Optional tuple of (username, password) for basic auth
        silent: If True, suppress request/response logging (default: False)

    Returns:
        httpx.Response object
    """
    if not silent:
        _log.info("%s -> %s", method, url)
    start_time = time.time()
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        request_kwargs = {"headers": headers}
        if json_data is not None:
            request_kwargs["json"] = json_data
        elif data is not None:
            # Avoid httpx deprecation warning by sending raw payload via `content`
            if isinstance(data, (str, bytes, bytearray, memoryview)):
                request_kwargs["content"] = data
            else:
                request_kwargs["data"] = data

        if auth is not None:
            request_kwargs["auth"] = auth

        response = client.request(method, url, **request_kwargs)
        elapsed_time = time.time() - start_time
        if not silent:
            _log.info(
                "%s -> %s completed in %.2fs (status: %s)",
                method, url, elapsed_time, response.status_code,
            )
        # Terminal, so it must be raised before the transient-retry check.
        _raise_if_insufficient_credits(response)
        if _is_transient_http_error(response.status_code):
            raise TransientHTTPError(
                response.status_code,
                f"Transient HTTP error: {response.status_code} for {method} {url}",
            )
        return response


def _raise_if_insufficient_credits(response) -> None:
    """Raise if the response is a 403 for exhausted credits.

    No retry can succeed once credits are exhausted, so the run stops here rather
    than continuing to issue calls that will all be refused.
    """
    if response is None or getattr(response, "status_code", None) != 403:
        return
    try:
        body = response.json()
    except Exception:
        return
    if isinstance(body, dict) and body.get("error_code") == "INSUFFICIENT_CREDITS":
        print("[KANEAI][CREDITS] ERROR: Organization KaneAI credits exhausted — AI step blocked. Recharge credits to resume runs.")
        raise KaneAICreditsExhausted(
            body.get("message") or "Organization KaneAI credits exhausted."
        )
