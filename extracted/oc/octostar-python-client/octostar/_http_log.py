"""Log a failed SDK response without the request, headers, cookies or tokens."""

import logging

import httpx

logger = logging.getLogger(__name__)

_BODY_LIMIT = 500


def log_error_response(response: httpx.Response) -> None:
    """Warn with method, path, status and a body prefix when the response is an error."""
    if not response.is_error:
        return
    try:
        request = response.request
        method, path = request.method, request.url.path
    except RuntimeError:
        method, path = "?", "?"
    logger.warning(
        "%s %s -> %s: %s",
        method,
        path,
        response.status_code,
        response.text[:_BODY_LIMIT],
    )
