"""Small, bounded urllib transport and secret-safe response helpers."""

from __future__ import annotations

import json
import re
import socket
from collections.abc import Iterable, Mapping
from email.utils import parsedate_to_datetime
from time import time
from urllib.error import HTTPError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .base import HttpResponse

_BEARER_PATTERN = re.compile(
    r"(?i)\bBearer[ \t]+[A-Za-z0-9._~+/=-]{4,}"
)
_KEY_ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b(api[_-]?key|token|authorization)"
    r"([\"' \t]*[:=][\"' \t]*)([A-Za-z0-9._~+/=-]{4,})"
)
_OPENAI_STYLE_KEY_PATTERN = re.compile(
    r"\bsk-(?:proj-|or-v1-)?[A-Za-z0-9_-]{8,}"
)
_MAX_ERROR_CHARS = 500


class ResponseTooLargeError(Exception):
    """The transport refused to buffer an oversized response."""


class _NoRedirectHandler(HTTPRedirectHandler):
    """Keep credentials on the one endpoint the caller explicitly selected."""

    def redirect_request(
        self,
        req: Request,
        fp: object,
        code: int,
        msg: str,
        headers: object,
        newurl: str,
    ) -> None:
        del req, fp, code, msg, headers, newurl
        return None


class UrllibTransport:
    """Default zero-dependency HTTP transport."""

    __slots__ = ("_opener",)

    def __init__(self) -> None:
        self._opener = build_opener(_NoRedirectHandler())

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout: float,
        max_response_bytes: int,
    ) -> HttpResponse:
        request = Request(
            url=url,
            data=body,
            headers=dict(headers),
            method=method,
        )
        try:
            response = self._opener.open(request, timeout=timeout)
        except HTTPError as error:
            try:
                response_body = _read_bounded(error, max_response_bytes)
                response_headers = {
                    key.lower(): value for key, value in error.headers.items()
                }
                return HttpResponse(
                    status=error.code,
                    headers=response_headers,
                    body=response_body,
                )
            finally:
                error.close()

        try:
            response_body = _read_bounded(response, max_response_bytes)
            response_headers = {
                key.lower(): value for key, value in response.headers.items()
            }
            return HttpResponse(
                status=response.status,
                headers=response_headers,
                body=response_body,
            )
        finally:
            response.close()


def _read_bounded(response: object, max_response_bytes: int) -> bytes:
    headers = getattr(response, "headers", {})
    content_length = None
    if isinstance(headers, Mapping):
        content_length = headers.get("Content-Length") or headers.get(
            "content-length"
        )
    elif hasattr(headers, "get"):
        content_length = headers.get("Content-Length")
    if content_length is not None:
        try:
            if int(content_length) > max_response_bytes:
                raise ResponseTooLargeError("provider response exceeded the limit")
        except ValueError:
            pass

    read = getattr(response, "read")
    body = read(max_response_bytes + 1)
    if len(body) > max_response_bytes:
        raise ResponseTooLargeError("provider response exceeded the limit")
    return body


def normalize_base_url(base_url: object) -> str:
    """Validate a credential-free HTTP(S) API base URL."""

    if type(base_url) is not str:
        raise TypeError("base_url must be a string")
    if not base_url.strip():
        raise ValueError("base_url must not be empty or whitespace")
    if base_url != base_url.strip():
        raise ValueError("base_url must not have leading or trailing whitespace")
    if any(character.isspace() or ord(character) < 32 for character in base_url):
        raise ValueError("base_url must not contain whitespace or control characters")

    parsed = urlsplit(base_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("base_url must use http or https")
    if not parsed.netloc or parsed.hostname is None:
        raise ValueError("base_url must include a host")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("base_url must not contain credentials")
    try:
        parsed.port
    except ValueError as error:
        raise ValueError("base_url contains an invalid port") from error
    if parsed.query:
        raise ValueError("base_url must not contain a query")
    if parsed.fragment:
        raise ValueError("base_url must not contain a fragment")

    path = parsed.path.rstrip("/")
    return urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))


def endpoint_url(base_url: str, path: str) -> str:
    """Append a relative API path without discarding the configured prefix."""

    return f"{base_url}/{path.lstrip('/')}"


def validate_headers(
    headers: Mapping[str, str] | None,
    *,
    reserved: Iterable[str] = (),
) -> dict[str, str]:
    """Copy custom headers after rejecting injection and reserved names."""

    if headers is None:
        return {}
    if not isinstance(headers, Mapping):
        raise TypeError("headers must be a mapping")
    reserved_lower = {name.lower() for name in reserved}
    copied: dict[str, str] = {}
    for key, value in headers.items():
        if type(key) is not str or type(value) is not str:
            raise TypeError("header names and values must be strings")
        if not key or key.lower() in reserved_lower:
            raise ValueError(f"header {key!r} is reserved or empty")
        if any(character in key for character in "\r\n:"):
            raise ValueError("header names must not contain control characters")
        if any(character in value for character in "\r\n"):
            raise ValueError("header values must not contain newlines")
        copied[key] = value
    return copied


def decode_json_object(body: bytes) -> dict[str, object]:
    """Decode a strict UTF-8 JSON object."""

    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("provider returned non-UTF-8 data") from error
    try:
        decoded = json.loads(
            text,
            parse_constant=lambda value: _reject_json_constant(value),
        )
    except json.JSONDecodeError as error:
        raise ValueError("provider returned invalid JSON") from error
    if type(decoded) is not dict:
        raise ValueError("provider returned a non-object JSON response")
    return decoded


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"non-standard JSON constant {value!r}")


def response_error_detail(
    body: bytes,
    *,
    secrets: Iterable[str] = (),
) -> str:
    """Extract at most one sanitized provider error message."""

    detail = "request failed"
    try:
        decoded = decode_json_object(body)
    except ValueError:
        decoded = {}

    error = decoded.get("error")
    if isinstance(error, Mapping):
        message = error.get("message")
        if type(message) is str and message.strip():
            detail = message
    elif type(error) is str and error.strip():
        detail = error
    else:
        message = decoded.get("message")
        if type(message) is str and message.strip():
            detail = message
    return redact_text(detail, secrets=secrets)


def redact_text(value: str, *, secrets: Iterable[str] = ()) -> str:
    """Redact known and recognizable credentials from diagnostic text."""

    redacted = value
    for secret in secrets:
        if secret:
            redacted = redacted.replace(secret, "<redacted>")
    redacted = _BEARER_PATTERN.sub("Bearer <redacted>", redacted)
    redacted = _KEY_ASSIGNMENT_PATTERN.sub(
        lambda match: f"{match.group(1)}{match.group(2)}<redacted>",
        redacted,
    )
    redacted = _OPENAI_STYLE_KEY_PATTERN.sub("<redacted>", redacted)
    redacted = " ".join(redacted.split())
    if len(redacted) > _MAX_ERROR_CHARS:
        return redacted[: _MAX_ERROR_CHARS - 1] + "…"
    return redacted


def retry_after_seconds(
    headers: Mapping[str, str],
    *,
    maximum: float,
) -> float | None:
    """Parse a bounded Retry-After delta or HTTP date."""

    value = None
    for key, item in headers.items():
        if key.lower() == "retry-after":
            value = item
            break
    if value is None:
        return None
    try:
        seconds = float(value)
    except ValueError:
        try:
            parsed = parsedate_to_datetime(value)
            seconds = parsed.timestamp() - time()
        except (TypeError, ValueError, OverflowError):
            return None
    return min(max(seconds, 0.0), maximum)


def is_timeout_error(error: BaseException) -> bool:
    """Return whether a urllib failure represents a timeout."""

    if isinstance(error, (TimeoutError, socket.timeout)):
        return True
    reason = getattr(error, "reason", None)
    return isinstance(reason, (TimeoutError, socket.timeout))
