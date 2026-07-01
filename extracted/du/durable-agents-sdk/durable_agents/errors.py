from __future__ import annotations

from collections.abc import Mapping

import httpx


class DurableApiError(Exception):
    """Normalized Durable API error."""

    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        request_id: str | None = None,
        details: object | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.request_id = request_id
        self.details = details
        self.headers = dict(headers or {})


def error_from_response(response: httpx.Response) -> DurableApiError:
    headers = dict(response.headers)
    fallback_message = f"Durable API request failed with status {response.status_code}"

    try:
        body = response.json()
    except ValueError:
        body = None

    if isinstance(body, dict):
        error = body.get("error")
        if isinstance(error, dict):
            code = error.get("code")
            message = error.get("message")
            if isinstance(code, str) and isinstance(message, str):
                request_id = body.get("request_id")
                return DurableApiError(
                    status_code=response.status_code,
                    code=code,
                    message=message,
                    request_id=request_id if isinstance(request_id, str) else None,
                    details=error.get("details"),
                    headers=headers,
                )

    return DurableApiError(
        status_code=response.status_code,
        code="unauthorized" if response.status_code == 401 else "api_error",
        message=fallback_message,
        request_id=response.headers.get("x-request-id"),
        headers=headers,
    )
