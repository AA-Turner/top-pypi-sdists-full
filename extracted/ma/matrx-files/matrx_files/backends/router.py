"""BackendRouter — URI scheme detection, URL parsing, retry, and dispatch.

Supported URI schemes (native)
------------------------------
    s3://bucket/path/to/file.ext
    server://path/to/file.ext

Supported HTTPS URLs (auto-converted to native, then read via credentials)
---------------------------------------------------------------------------
    S3 virtual-host:  https://bucket.s3.region.amazonaws.com/key[?X-Amz-Signature=...]
    S3 path-style:    https://s3.region.amazonaws.com/bucket/key

Retry policy
------------
    read() and write() automatically retry on transient failures:
        - Up to MAX_RETRIES attempts total (default 3)
        - Exponential backoff: 0.5 s, 1 s, 2 s
        - Retried: network errors, HTTP 429, HTTP 5xx
        - NOT retried: HTTP 403, HTTP 404, ValueError, RuntimeError
          (these are logic / config errors, not transient)

BackendRouter is lazily initialised — backend instances are created on
first use so that import-time costs and misconfigured-but-unused backends
do not cause errors.
"""

from __future__ import annotations

import time
import logging
from dataclasses import replace
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from .base_backend import ObjectInfo, StorageBackend
from .s3_backend import S3Backend
from .server_backend import ServerBackend
from .url_parser import parse_storage_url, is_storage_url

if TYPE_CHECKING:
    from ..ephemeral_objects import EphemeralObjectPolicy

logger = logging.getLogger(__name__)

CLOUD_SCHEMES: frozenset[str] = frozenset({"s3", "server"})

_MAX_RETRIES: int = 3
_RETRY_BACKOFF: tuple[float, ...] = (0.5, 1.0, 2.0)

# Error message fragments that indicate a transient failure worth retrying.
# Permanent errors (403, 404, bad path, not-configured) are never retried.
_TRANSIENT_FRAGMENTS: tuple[str, ...] = (
    "timeout",
    "timed out",
    "connection",
    "network",
    "throttl",
    "rate limit",
    "503",
    "502",
    "500",
    "429",
    "temporarily unavailable",
    "service unavailable",
    "internal server error",
)

_PERMANENT_FRAGMENTS: tuple[str, ...] = (
    "403",
    "404",
    "forbidden",
    "not found",
    "nosuchkey",
    "nosuchbucket",
    "access denied",
    "not configured",
    "invalid",
    "no such",
)


def _is_transient(exc: Exception) -> bool:
    """Return True if *exc* looks like a transient failure worth retrying."""
    msg = str(exc).lower()
    # Permanent errors take priority — never retry these.
    for fragment in _PERMANENT_FRAGMENTS:
        if fragment in msg:
            return False
    for fragment in _TRANSIENT_FRAGMENTS:
        if fragment in msg:
            return True
    # ConnectionError and TimeoutError subclasses are always transient.
    return isinstance(exc, (ConnectionError, TimeoutError, OSError))


def _url_seconds_remaining(url: str) -> float | None:
    """Return seconds until *url* expires, or None if it has no expiry.

    Reads expiry purely from the URL itself — no network call, no secret key.

    S3 presigned URLs: X-Amz-Date + X-Amz-Expires in query params.
    Public/unknown URLs: return None (treat as non-expiring).
    """
    import time
    from urllib.parse import urlparse, parse_qs
    from datetime import datetime, timezone

    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    # S3 presigned URL — X-Amz-Date + X-Amz-Expires
    amz_date = qs.get("X-Amz-Date", [""])[0]
    amz_expires = qs.get("X-Amz-Expires", [""])[0]
    if amz_date and amz_expires:
        try:
            issued = datetime.strptime(amz_date, "%Y%m%dT%H%M%SZ").replace(
                tzinfo=timezone.utc
            )
            expires_at = issued.timestamp() + int(amz_expires)
            return expires_at - time.time()
        except Exception:
            pass

    return None  # no expiry information found


def _with_retry(fn, *args, **kwargs):
    """Call *fn* with retry/backoff on transient errors.

    On a permanent error (403, 404, not-configured, etc.) the exception
    is re-raised immediately without any retry.
    """
    last_exc: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            return fn(*args, **kwargs)
        except (ValueError, RuntimeError) as exc:
            # Config / logic errors — never retry.
            raise
        except Exception as exc:
            if not _is_transient(exc):
                raise
            last_exc = exc
            if attempt < _MAX_RETRIES - 1:
                delay = _RETRY_BACKOFF[min(attempt, len(_RETRY_BACKOFF) - 1)]
                logger.warning(
                    "Transient error on attempt %d/%d (%s). Retrying in %.1fs…",
                    attempt + 1,
                    _MAX_RETRIES,
                    exc,
                    delay,
                )
                time.sleep(delay)
    raise last_exc  # type: ignore[misc]


async def _with_retry_async(fn, *args, **kwargs):
    """Async version of _with_retry — same policy, awaits the coroutine."""
    last_exc: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            return await fn(*args, **kwargs)
        except (ValueError, RuntimeError):
            raise
        except Exception as exc:
            if not _is_transient(exc):
                raise
            last_exc = exc
            if attempt < _MAX_RETRIES - 1:
                import asyncio
                delay = _RETRY_BACKOFF[min(attempt, len(_RETRY_BACKOFF) - 1)]
                logger.warning(
                    "Transient error on attempt %d/%d (%s). Retrying in %.1fs…",
                    attempt + 1,
                    _MAX_RETRIES,
                    exc,
                    delay,
                )
                await asyncio.sleep(delay)
    raise last_exc  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Module-level helpers (kept for backward compat)
# ---------------------------------------------------------------------------

def is_cloud_uri(path: str) -> bool:
    """Return True if *path* is a native cloud URI (s3:// or server://)
    OR an HTTPS URL pointing at a recognized cloud storage provider."""
    if "://" not in path:
        return False
    scheme = path.split("://", 1)[0].lower()
    if scheme in CLOUD_SCHEMES:
        return True
    if scheme in ("http", "https"):
        return is_storage_url(path)
    return False


def parse_uri(uri: str) -> tuple[str, str]:
    """Parse a native cloud URI and return (scheme, path-without-scheme).

    For HTTPS URLs use parse_storage_url() from url_parser instead.

    Examples
    --------
    >>> parse_uri("s3://my-bucket/reports/jan.json")
    ('s3', 'my-bucket/reports/jan.json')
    >>> parse_uri("server://uploads/file.txt")
    ('server', 'uploads/file.txt')
    """
    parsed = urlparse(uri)
    scheme = parsed.scheme.lower()
    if scheme not in CLOUD_SCHEMES:
        raise ValueError(
            f"Unrecognized cloud URI scheme '{scheme}' in '{uri}'. "
            f"Supported schemes: {sorted(CLOUD_SCHEMES)}"
        )
    netloc = parsed.netloc
    path = parsed.path.lstrip("/")
    if netloc and not path:
        # Bucket ROOT. Keep the trailing separator: without it, a bare
        # "bucket" is indistinguishable from "a key prefix inside the default
        # bucket", and S3Backend resolves the ambiguity the wrong way — it
        # listed with Prefix=<bucket-name>, which matches nothing. That made
        # list_files("s3://bucket/") silently return [] forever.
        return scheme, f"{netloc}/"
    full_path = f"{netloc}/{path}" if netloc and path else netloc or path
    return scheme, full_path


class BackendRouter:
    """Holds one lazily-created instance of each cloud backend and routes
    read/write/delete/append/get_url/list_files/read_url calls to the
    correct one, with automatic retry on transient failures.
    """

    def __init__(self) -> None:
        self._s3: S3Backend | None = None
        self._server: ServerBackend | None = None

    # ------------------------------------------------------------------
    # Lazy backend accessors
    # ------------------------------------------------------------------

    @property
    def s3(self) -> S3Backend:
        if self._s3 is None:
            self._s3 = S3Backend()
        return self._s3

    @property
    def server(self) -> ServerBackend:
        if self._server is None:
            self._server = ServerBackend()
        return self._server

    # ------------------------------------------------------------------
    # Internal dispatch
    # ------------------------------------------------------------------

    def _resolve(self, uri: str) -> tuple[StorageBackend, str]:
        """Return (backend, storage_path) for any URI or HTTPS URL."""
        parsed_scheme = uri.split("://", 1)[0].lower() if "://" in uri else ""

        if parsed_scheme in ("http", "https"):
            result = parse_storage_url(uri)
            scheme: str = result.scheme
            path: str = result.storage_path
        else:
            scheme, path = parse_uri(uri)

        backends: dict[str, StorageBackend] = {
            "s3": self.s3,
            "server": self.server,
        }
        return backends[scheme], path

    # ------------------------------------------------------------------
    # Public routing API — mirrors StorageBackend interface
    # ------------------------------------------------------------------

    def read(self, uri: str) -> bytes:
        """Read bytes from *uri* with automatic retry on transient errors."""
        backend, path = self._resolve(uri)
        return _with_retry(backend.read, path)

    def download_to_path(self, uri: str, local_path: str) -> int:
        """Materialize *uri* to disk using the backend's streaming path."""
        backend, path = self._resolve(uri)
        return _with_retry(backend.download_to_path, path, local_path)

    def write(self, uri: str, content: bytes | str, **kwargs) -> bool:
        """Write *content* to *uri* with automatic retry on transient errors."""
        backend, path = self._resolve(uri)
        return _with_retry(backend.write, path, content, **kwargs)

    def write_ephemeral(
        self,
        uri: str,
        content: bytes | str,
        *,
        policy: EphemeralObjectPolicy,
        content_type: str | None = None,
    ) -> bool:
        """Write row-less scratch with lifecycle classification attached atomically."""
        backend, path = self._resolve(uri)
        return _with_retry(
            backend.write_ephemeral,
            path,
            content,
            policy=policy,
            content_type=content_type,
        )

    def append(self, uri: str, content: bytes | str) -> bool:
        backend, path = self._resolve(uri)
        return _with_retry(backend.append, path, content)

    def delete(self, uri: str) -> bool:
        backend, path = self._resolve(uri)
        return backend.delete(path)

    def get_url(
        self,
        uri: str,
        expires_in: int = 3600,
        *,
        response_content_disposition: str | None = None,
        response_content_type: str | None = None,
    ) -> str:
        backend, path = self._resolve(uri)
        return backend.get_url(
            path,
            expires_in=expires_in,
            response_content_disposition=response_content_disposition,
            response_content_type=response_content_type,
        )

    def get_public_url(self, uri: str) -> str:
        """Return the permanent public URL for a cloud object (bucket must be public)."""
        backend, path = self._resolve(uri)
        return backend.get_public_url(path)

    def list_files(self, uri_prefix: str = "") -> list[str]:
        if not uri_prefix:
            raise ValueError(
                "list_files() requires a URI prefix with a scheme, "
                "e.g. 's3://bucket/folder/' or 'server://folder/'."
            )
        backend, path = self._resolve(uri_prefix)
        raw: list[str] = backend.list_files(path)
        scheme = uri_prefix.split("://", 1)[0].lower()
        return [f"{scheme}://{item}" for item in raw]

    def list_objects(self, uri_prefix: str = "") -> list[ObjectInfo]:
        """list_files() + size/last-modified metadata. ``path`` on each result
        is a full URI (scheme re-attached), directly comparable to a
        ``storage_uri``. See ObjectInfo — deleting off this list REQUIRES an
        age floor."""
        if not uri_prefix:
            raise ValueError(
                "list_objects() requires a URI prefix with a scheme, "
                "e.g. 's3://bucket/folder/'."
            )
        backend, path = self._resolve(uri_prefix)
        scheme = uri_prefix.split("://", 1)[0].lower()
        return [
            replace(o, path=f"{scheme}://{o.path}") for o in backend.list_objects(path)
        ]

    # ------------------------------------------------------------------
    # read_url — the "React sent me a URL" entry point
    # ------------------------------------------------------------------

    def read_url(self, url: str) -> bytes:
        """Read bytes from any URL format that a client might send.

        Unlike read(), this method accepts HTTPS URLs (public, signed,
        presigned) in addition to native cloud URIs. The URL is parsed
        back to a (backend, storage_path) pair and the file is fetched
        using server-side credentials — token expiry, signature
        validity, and URL format are all irrelevant.

        Supported inputs
        ----------------
        - s3://bucket/path/file.ext
        - https://bucket.s3.region.amazonaws.com/key[?X-Amz-Signature=...]
        - https://s3.region.amazonaws.com/bucket/key

        Raises
        ------
        ValueError
            If the URL cannot be recognized as a supported storage URL.
        RuntimeError
            If the relevant backend is not configured (missing credentials).
        """
        return _with_retry(self._read_url_once, url)

    def _read_url_once(self, url: str) -> bytes:
        backend, path = self._resolve(url)
        return backend.read(path)

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------

    def is_configured(self, scheme: str) -> bool:
        """Return True if the backend for *scheme* is ready to use."""
        scheme = scheme.lower()
        if scheme == "s3":
            return self.s3.is_configured()
        if scheme == "server":
            return self.server.is_configured()
        raise ValueError(f"Unknown scheme '{scheme}'.")

    def configured_backends(self) -> list[str]:
        """Return the list of scheme names for all configured backends."""
        result: list[str] = []
        if self.s3.is_configured():
            result.append("s3")
        if self.server.is_configured():
            result.append("server")
        return result

    # ------------------------------------------------------------------
    # Async routing API
    # ------------------------------------------------------------------

    async def read_async(self, uri: str) -> bytes:
        """Non-blocking read. Use in FastAPI routes and all async contexts."""
        backend, path = self._resolve(uri)
        return await _with_retry_async(backend.read_async, path)

    async def download_to_path_async(self, uri: str, local_path: str) -> int:
        """Non-blocking materialization using the backend's streaming path."""
        backend, path = self._resolve(uri)
        return await _with_retry_async(
            backend.download_to_path_async, path, local_path
        )

    async def write_async(self, uri: str, content: bytes | str, **kwargs) -> bool:
        """Non-blocking write."""
        backend, path = self._resolve(uri)
        return await _with_retry_async(backend.write_async, path, content, **kwargs)

    async def write_ephemeral_async(
        self,
        uri: str,
        content: bytes | str,
        *,
        policy: EphemeralObjectPolicy,
        content_type: str | None = None,
    ) -> bool:
        """Non-blocking row-less scratch write with atomic lifecycle tags."""
        backend, path = self._resolve(uri)
        return await _with_retry_async(
            backend.write_ephemeral_async,
            path,
            content,
            policy=policy,
            content_type=content_type,
        )

    async def append_async(self, uri: str, content: bytes | str) -> bool:
        backend, path = self._resolve(uri)
        return await _with_retry_async(backend.append_async, path, content)

    async def delete_async(self, uri: str) -> bool:
        backend, path = self._resolve(uri)
        return await backend.delete_async(path)

    async def copy_async(self, src_uri: str, dst_uri: str) -> bool:
        """Non-blocking server-side copy WITHIN the same backend.

        Used by ``SyncEngine.set_published_to_web_async`` to move objects
        between the public and private buckets without ever
        downloading the bytes. Both URIs must resolve to the same backend
        — cross-backend copies should use read_async + write_async.
        """
        src_backend, src_path = self._resolve(src_uri)
        dst_backend, dst_path = self._resolve(dst_uri)
        if src_backend is not dst_backend:
            raise ValueError(
                f"copy_async: cross-backend copy is not supported "
                f"(src={src_uri!r} dst={dst_uri!r}). "
                "Use read_async + write_async for cross-backend transfers."
            )
        if not hasattr(src_backend, "copy_async"):
            raise NotImplementedError(
                f"Backend {type(src_backend).__name__} does not implement copy_async."
            )
        return await src_backend.copy_async(src_path, dst_path)

    def get_public_url(self, uri: str) -> str:
        """Return the permanent public URL for a cloud object (bucket must be public)."""
        backend, path = self._resolve(uri)
        return backend.get_public_url(path)

    async def get_public_url_async(self, uri: str) -> str:
        """Non-blocking permanent public URL (bucket must be public)."""
        backend, path = self._resolve(uri)
        return await backend.get_public_url_async(path)

    async def get_url_async(
        self,
        uri: str,
        expires_in: int = 3600,
        *,
        response_content_disposition: str | None = None,
        response_content_type: str | None = None,
    ) -> str:
        backend, path = self._resolve(uri)
        return await backend.get_url_async(
            path,
            expires_in=expires_in,
            response_content_disposition=response_content_disposition,
            response_content_type=response_content_type,
        )

    async def list_files_async(self, uri_prefix: str = "") -> list[str]:
        if not uri_prefix:
            raise ValueError(
                "list_files_async() requires a URI prefix with a scheme."
            )
        backend, path = self._resolve(uri_prefix)
        raw: list[str] = await backend.list_files_async(path)
        scheme = uri_prefix.split("://", 1)[0].lower()
        return [f"{scheme}://{item}" for item in raw]

    async def delete_many_async(self, uris: list[str]) -> tuple[int, list[tuple[str, str]]]:
        """Batch-delete many URIs, grouped per backend.

        Returns ``(deleted, [(uri, error), ...])`` where every error carries the
        CALLER'S original URI — a backend speaks backend-relative paths, and the
        router owns the scheme, so it must translate back. A caller matching
        errors against its own URI list (to decide what was actually reclaimed)
        would otherwise silently never match.

        Nothing raises: one bad key, or one failing backend, must not abort a
        bulk reclaim or lose the accounting of what already landed.
        """
        by_backend: dict[int, tuple[StorageBackend, list[str], dict[str, str]]] = {}
        for uri in uris:
            backend, path = self._resolve(uri)
            entry = by_backend.setdefault(id(backend), (backend, [], {}))
            entry[1].append(path)
            entry[2][path] = uri  # backend-relative path -> caller's URI

        deleted = 0
        errors: list[tuple[str, str]] = []
        for backend, paths, originals in by_backend.values():
            try:
                n, errs = await backend.delete_many_async(paths)
            except Exception as e:  # noqa: BLE001 — isolate a failing backend
                errors.extend((originals.get(p, p), str(e)) for p in paths)
                continue
            deleted += n
            errors.extend((originals.get(p, p), msg) for p, msg in errs)
        return deleted, errors

    async def list_objects_async(self, uri_prefix: str = "") -> list[ObjectInfo]:
        """Async version of list_objects()."""
        if not uri_prefix:
            raise ValueError(
                "list_objects_async() requires a URI prefix with a scheme."
            )
        backend, path = self._resolve(uri_prefix)
        scheme = uri_prefix.split("://", 1)[0].lower()
        return [
            replace(o, path=f"{scheme}://{o.path}")
            for o in await backend.list_objects_async(path)
        ]

    async def read_url_async(self, url: str) -> bytes:
        """Non-blocking read from any URL format a client might send."""
        return await _with_retry_async(self._read_url_once_async, url)

    async def _read_url_once_async(self, url: str) -> bytes:
        backend, path = self._resolve(url)
        return await backend.read_async(path)

    # ------------------------------------------------------------------
    # ensure_url — smart URL refresh without unnecessary network calls
    # ------------------------------------------------------------------

    def ensure_url(self, url: str, expires_in: int = 3600) -> str:
        """Return a guaranteed-valid URL for a cloud file.

        Logic (zero network calls when URL is still fresh):
        1. If *url* is a native cloud URI (s3:// or server://) — generate
           a fresh signed URL directly. No expiry check needed.
        2. If *url* is an S3 presigned URL — read X-Amz-Date + X-Amz-Expires
           from the query string. Return the original if still valid.
        3. If *url* is a public (non-expiring) HTTPS URL — return it as-is.
        4. If expired (or unrecognized format) — parse to storage path,
           generate a fresh signed URL via backend credentials, return it.

        Parameters
        ----------
        url:
            Any URL or URI for a cloud file.
        expires_in:
            Expiry for the *new* URL when one needs to be generated (seconds).
        """
        from .url_parser import parse_storage_url
        import time

        # Native URIs have no expiry — generate a fresh signed URL
        parsed_scheme = url.split("://", 1)[0].lower() if "://" in url else ""
        if parsed_scheme in CLOUD_SCHEMES:
            result = parse_storage_url(url)
            backend, path = self._resolve(url)
            return backend.get_url(path, expires_in=expires_in)

        # HTTPS URL — check if it carries expiry information
        remaining = _url_seconds_remaining(url)
        if remaining is None:
            # Public / non-expiring URL — return as-is
            return url
        if remaining > 60:
            # More than 60 s left — safe to use as-is
            return url

        # Expired or about to expire — regenerate via credentials
        result = parse_storage_url(url)
        backend, path = self._resolve(result.to_native_uri())
        return backend.get_url(path, expires_in=expires_in)

    async def ensure_url_async(self, url: str, expires_in: int = 3600) -> str:
        """Async version of ensure_url()."""
        from .url_parser import parse_storage_url

        parsed_scheme = url.split("://", 1)[0].lower() if "://" in url else ""
        if parsed_scheme in CLOUD_SCHEMES:
            backend, path = self._resolve(url)
            return await backend.get_url_async(path, expires_in=expires_in)

        remaining = _url_seconds_remaining(url)
        if remaining is None:
            return url
        if remaining > 60:
            return url

        result = parse_storage_url(url)
        backend, path = self._resolve(result.to_native_uri())
        return await backend.get_url_async(path, expires_in=expires_in)
