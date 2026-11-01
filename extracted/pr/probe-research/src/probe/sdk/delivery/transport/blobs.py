"""BlobsMixin: presigned-URL transfer -- PUT bytes, files, parts and open handles; GET and stream downloads."""

from __future__ import annotations

from ...secret_gate import InspectionResult, warn_if_incomplete
import time

import httpx
import functools
from urllib.parse import urlsplit
from .protocols import observer
from ... import errors


def _warn_upload_inspection(response: httpx.Response) -> None:
    if 200 <= response.status_code < 300 and response.headers.get("x-probe-inspection-warning"):
        # A storage endpoint controls its response headers: report fixed text, never echo
        # remote content or credentials.
        warn_if_incomplete(
            InspectionResult(warnings=("server could not fully inspect artifact contents",))
        )


def _iter_file(fh, chunk_size: int, limit: int | None = None):
    """Yield an open binary file in fixed-size chunks (a streaming upload body).

    With ``limit`` the body stops at that many bytes even if the file grew since it was
    measured (a log appended mid-upload), so declared Content-Length and verified bytes
    match. A file that SHRANK sends short and fails cleanly under Content-Length."""
    remaining = limit
    # Inside a `deadline_scope`, checked per chunk: httpx timeouts bound each socket op,
    # so a slow-but-progressing upload would never be cut. An unfinished body was not applied.
    deadline = _request_deadline.get()
    while remaining is None or remaining > 0:
        if deadline is not None and time.monotonic() >= deadline:
            raise errors.DeadlineExceeded("upload: deadline passed mid-body")
        chunk = fh.read(chunk_size if remaining is None else min(chunk_size, remaining))
        if not chunk:
            break
        if remaining is not None:
            remaining -= len(chunk)
        yield chunk


def _blob_label(url: str) -> str:
    """A presigned URL reduced to host + path: the query carries the signature and never
    enters the buffer; a reader needs which store, which object."""
    try:
        parts = urlsplit(url)
        return f"{parts.netloc}{parts.path}"
    except Exception:
        return "<blob>"


def _instrumented(verb: str):
    """Bracket a blob transfer so the ring buffer sees it. These are the SDK's longest
    requests (artifact and weight transfers), the likeliest to stall, yet only `request()`
    was instrumented, leaving the stall detector blind to the traffic that parks a loop."""

    def decorate(fn):
        @functools.wraps(fn)
        def wrapper(self, url, *args, **kwargs):
            started = time.monotonic()
            label = _blob_label(url)
            base = self.settings.base_url
            observer().begin_transport(verb, label, base=base)
            error = None
            try:
                return fn(self, url, *args, **kwargs)
            except BaseException as exc:
                error = repr(exc)
                raise
            finally:
                observer().end_transport()
                observer().record_transport(
                    verb, label, seconds=time.monotonic() - started, error=error, base=base
                )

        return wrapper

    return decorate
from probe.sdk.delivery.transport.deadlines import _request_deadline  # noqa: E402 -- pieces need each other; the front door loads this one first
