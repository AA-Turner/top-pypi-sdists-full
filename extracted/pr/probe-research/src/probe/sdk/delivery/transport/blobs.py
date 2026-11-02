"""BlobsMixin: presigned-URL transfer -- PUT bytes, files, parts and open handles; GET and stream downloads."""

from __future__ import annotations

from collections.abc import Mapping
import functools
import hashlib
import os
import time
from typing import Any
from urllib.parse import urlsplit

import httpx

from probe.sdk.secret_gate import freeze_stream, freeze_upload

from ... import errors
from ...secret_gate import InspectionResult, warn_if_incomplete
from .protocols import observer


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


class BlobsMixin:
    """Part of Transport: its methods run with `self` the Transport; fold_parts() copies them into Transport."""

    @_instrumented("PUT")
    def put_url(
        self,
        url: str,
        data: bytes,
        *,
        content_type: str | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        """Raw PUT of bytes to a presigned URL (artifact upload, fold #16). No
        Authorization header (the URL carries its signature); goes to an absolute URL (R2),
        not the API base; retried on network blips."""
        # No local content scan: the presigned digest pins these bytes, so a scan could only
        # warn; the server inspects every upload and returns its own warning
        # (`_warn_upload_inspection` below).
        data = bytes(data)
        request_headers = dict(headers or {})
        if content_type:
            request_headers.setdefault("Content-Type", content_type)
        attempt = 0
        while True:
            attempt += 1
            attempt_timeout, clamped = self._attempt_timeout(None, f"PUT {_blob_label(url)}")
            try:
                resp = self._client.put(
                    url,
                    content=data,
                    headers=request_headers,
                    **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
                )
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                if self._cut_by_deadline(exc, clamped):
                    raise self._deadline_error(f"PUT {_blob_label(url)}", exc) from exc
                raise errors.TransportError(f"PUT {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                raise _presigned_put_error(resp, url)
            _warn_upload_inspection(resp)
            return

    @freeze_upload
    def put_file(
        self,
        url: str,
        path: str,
        *,
        content_type: str | None = None,
        headers: Mapping[str, str] | None = None,
        chunk_size: int = 1 << 20,
    ) -> None:
        """Stream a local file to a presigned URL without buffering it (weights would OOM the loop); no
        Authorization header. Each attempt re-opens the file and measures Content-Length from it, so a
        retry sends from byte 0 and the length always matches the bytes (R2 refuses chunked, 411)."""
        request_headers = dict(headers or {})
        if content_type:
            request_headers.setdefault("Content-Type", content_type)
        attempt = 0
        while True:
            attempt += 1
            attempt_timeout, clamped = self._attempt_timeout(None, f"PUT {_blob_label(url)}")
            try:
                with open(path, "rb") as fh:
                    request_headers["Content-Length"] = str(os.fstat(fh.fileno()).st_size)
                    resp = self._client.put(
                        url,
                        content=_iter_file(fh, chunk_size),
                        headers=request_headers,
                        **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
                    )
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                if self._cut_by_deadline(exc, clamped):
                    raise self._deadline_error(f"PUT {_blob_label(url)}", exc) from exc
                raise errors.TransportError(f"PUT {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                raise _presigned_put_error(resp, url)
            _warn_upload_inspection(resp)
            return

    @_instrumented("PUT")
    def put_part(
        self,
        url: str,
        path: str,
        *,
        offset: int,
        length: int,
        chunk_size: int = 1 << 20,
    ) -> str | None:
        """PUT bytes ``[offset, offset + length)`` of ``path`` to a presigned multipart PART URL (plan
        (g)); returns the store's ETag. The one byte path with no local credential gate, on purpose: a
        part of an artifact past the 64 MiB inspection limit cannot be redacted without breaking its
        sha256 (DESIGN.md). Streams, re-opening the file every attempt like `put_file`."""
        headers = {"Content-Length": str(length)}
        attempt = 0
        while True:
            attempt += 1
            attempt_timeout, clamped = self._attempt_timeout(None, f"PUT {_blob_label(url)}")
            try:
                with open(path, "rb") as fh:
                    fh.seek(offset)
                    resp = self._client.put(
                        url,
                        content=_iter_file(fh, chunk_size, length),
                        headers=headers,
                        **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
                    )
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                if self._cut_by_deadline(exc, clamped):
                    raise self._deadline_error(f"PUT {_blob_label(url)}", exc) from exc
                raise errors.TransportError(f"PUT {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                # #2075: a 401/403 refuses this part's signed URL, never the login (none is
                # sent): `UploadRefused`, not an auth block.
                raise _presigned_put_error(resp, url)
            return resp.headers.get("etag")

    @_instrumented("PUT")
    @freeze_stream
    def put_fileobj(
        self,
        url: str,
        fh: Any,
        *,
        size: int,
        content_type: str | None = None,
        headers: Mapping[str, str] | None = None,
        chunk_size: int = 1 << 20,
    ) -> None:
        """PUT an already-open, already-verified file handle to a presigned URL. The
        per-file capture path hashes a descriptor before streaming it (bytes sent = bytes
        checked); this sibling of :meth:`put_file` takes that descriptor instead of
        re-opening a path it cannot vouch for. Sends exactly ``size`` bytes, rewinding to
        byte 0 every attempt. No Authorization header."""
        request_headers = dict(headers or {})
        if content_type:
            request_headers.setdefault("Content-Type", content_type)
        request_headers["Content-Length"] = str(size)
        attempt = 0
        while True:
            attempt += 1
            attempt_timeout, clamped = self._attempt_timeout(None, f"PUT {_blob_label(url)}")
            fh.seek(0)
            try:
                resp = self._client.put(
                    url,
                    content=_iter_file(fh, chunk_size, size),
                    headers=request_headers,
                    **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
                )
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                if self._cut_by_deadline(exc, clamped):
                    raise self._deadline_error(f"PUT {_blob_label(url)}", exc) from exc
                raise errors.TransportError(f"PUT {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                raise _presigned_put_error(resp, url)
            _warn_upload_inspection(resp)
            return

    @_instrumented("GET")
    def get_url(self, url: str) -> bytes:
        """Raw GET of a presigned URL (artifact download); returns the bytes. No
        Authorization header (the URL carries its signature)."""
        attempt = 0
        while True:
            attempt += 1
            try:
                resp = self._client.get(url)
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                raise errors.TransportError(f"GET {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                raise _with_retry_after(errors.error_for(resp.status_code, resp.text), resp)
            return resp.content

    @_instrumented("GET")
    def download_to(
        self, url: str, dest: str, *, chunk_size: int = 1 << 20, max_bytes: int | None = None
    ) -> tuple[int, str]:
        """Stream a presigned-URL GET to ``dest``; return ``(size_bytes, sha256_hex)``.
        Sibling of :meth:`get_url` for bytes you do NOT want in memory (model weights): it
        hashes while writing, so a caller verifies against a known ``content_hash`` without
        a second pass. No Authorization header. Idempotent: a blip or retryable status
        restarts from byte 0 (``open`` truncates ``dest``). A partial file remains only when
        retries are exhausted mid-stream; the caller owns cleanup on error."""
        if max_bytes is not None and max_bytes < 0:
            raise ValueError("max_bytes must not be negative")
        attempt = 0
        while True:
            attempt += 1
            try:
                with self._client.stream("GET", url) as resp:
                    if (
                        resp.status_code in _RETRYABLE
                        and attempt <= self.max_retries
                        and self._retry_pause(attempt, resp)
                    ):
                        continue
                    if resp.status_code >= 400:
                        resp.read()  # a streamed response has no .text until read
                        raise _with_retry_after(
                            errors.error_for(resp.status_code, resp.text), resp
                        )
                    hasher = hashlib.sha256()
                    size = 0
                    if max_bytes is not None:
                        declared = resp.headers.get("content-length")
                        if declared is not None and int(declared) > max_bytes:
                            raise ValueError("artifact download exceeds its byte budget")
                    with open(dest, "wb") as fh:
                        for chunk in resp.iter_bytes(chunk_size):
                            if max_bytes is not None and size + len(chunk) > max_bytes:
                                raise ValueError("artifact download exceeds its byte budget")
                            fh.write(chunk)
                            hasher.update(chunk)
                            size += len(chunk)
                return size, hasher.hexdigest()
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                raise errors.TransportError(f"GET {_blob_label(url)}: {exc}") from exc

from probe.sdk.delivery.transport.deadlines import _request_deadline  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.transport.transport import _RETRYABLE  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.transport.failures import _presigned_put_error  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.transport.deadlines import _with_retry_after  # noqa: E402 -- pieces need each other; the front door loads this one first
