"""Shared request/response metadata for logging and error middleware."""

from __future__ import annotations

import re
from typing import Any, Iterator


def _body_size(response) -> int | None:
    if response is None:
        return None
    body = getattr(response, "body", None)
    if body is None:
        body = getattr(response, "content", None)
    if body is None:
        text = getattr(response, "text", None)
        if isinstance(text, str):
            body = text.encode(errors="replace")
    if body is None:
        return None
    return len(body)


def format_response_size_bytes(response) -> str | None:
    """Return comma-formatted body size (e.g. ``117,001``), or ``None``."""
    size = _body_size(response)
    if size is None:
        return None
    return f"{size:,}"


def format_size_from_meta(request) -> str | None:
    """Read a precomputed size from ``request.meta`` (optional integrations)."""
    if request is None:
        return None
    meta = getattr(request, "meta", None) or {}
    stealth = meta.get("stealth") if isinstance(meta.get("stealth"), dict) else {}
    for candidate in (
        meta.get("response_size_bytes"),
        stealth.get("response_size_bytes"),
        stealth.get("response_body_bytes"),
        stealth.get("last_body_byte_len"),
    ):
        if candidate is None or candidate == "":
            continue
        if isinstance(candidate, str) and "," in candidate:
            return candidate
        try:
            return f"{int(candidate):,}"
        except (TypeError, ValueError):
            continue
    return None


def _unwrap_failure(subject):
    """Twisted ``Failure`` or a plain exception."""
    try:
        from twisted.python.failure import Failure
    except ImportError:
        return subject
    if isinstance(subject, Failure):
        return subject.value
    return subject


def _iter_exception_chain(exception) -> Iterator[Any]:
    seen: set[int] = set()
    current = exception
    while current is not None:
        marker = id(current)
        if marker in seen:
            break
        seen.add(marker)
        yield current
        cause = getattr(current, "__cause__", None)
        context = getattr(current, "__context__", None)
        current = cause if cause is not None else context


def _response_has_payload(response) -> bool:
    return _body_size(response) is not None or bool(
        getattr(response, "status", None) or getattr(response, "status_code", None)
    )


def _attached_response(subject) -> Any | None:
    subject = _unwrap_failure(subject)
    try:
        from scrapy.spidermiddlewares.httperror import HttpError
    except ImportError:
        HttpError = ()  # type: ignore[misc, assignment]

    if HttpError and isinstance(subject, HttpError):
        return subject.response

    attached = getattr(subject, "response", None)
    if attached is not None and _response_has_payload(attached):
        return attached
    return None


def response_from_exception(exception, response=None):
    """Return a response-like object from an exception chain, if any."""
    if response is not None and _response_has_payload(response):
        return response

    for subject in _iter_exception_chain(exception):
        attached = _attached_response(subject)
        if attached is not None:
            return attached
    return None


def response_size_bytes_for_request(
    request, exception=None, response=None
) -> str | None:
    """Resolve comma-formatted size for success and failure paths."""
    size = format_response_size_bytes(response_from_exception(exception, response))
    if size is not None:
        return size
    return format_size_from_meta(request)


def status_code_from_exception(exception, response=None) -> int:
    """Best-effort HTTP status for downloader/spider failures."""
    resp = response_from_exception(exception, response)
    if resp is not None:
        status = getattr(resp, "status", None)
        if not status:
            status = getattr(resp, "status_code", None)
        if status:
            return int(status)

    for subject in _iter_exception_chain(exception):
        exc = _unwrap_failure(subject)
        status_match = re.search(r"\[(\d{3})]", str(exc))
        if status_match:
            return int(status_match.group(1))

        if hasattr(exc, "status") and exc.status:
            return int(exc.status)

        name = exc.__class__.__name__
        if "Timeout" in name or "TimedOut" in name:
            return 408

    return 0
