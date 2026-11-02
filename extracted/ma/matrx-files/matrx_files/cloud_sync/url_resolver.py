"""Recognize URLs that AI Dream issued and resolve them to canonical metadata.

Sync-only by design: ``resolve_file_url`` uses the matrx-orm ``_sync``
query twins so it can be called from any context (worker thread, sync
handler) without the cross-loop dispatch problems that brought down an
earlier version; ``resolve_file_url_async`` is the loop-safe twin.

Public API
----------
``classify_url(url)``        cheap structural classification (no DB lookup)
``resolve_file_url(url)``    URL recognition + DB lookup, returns ResolvedFile
``ResolvedFile``             dataclass with canonical mime, file_id, owner, etc.

Recognized URL shapes
---------------------
- ``https://<host>/share/<token>`` and ``/share/<token>/download``
- ``https://<host>/files/<file_id>`` and its sub-paths
- ``https://<host>/files/by-path/<path>``
- ``s3://<bucket>/<key>`` (matched against AI Dream's configured bucket)
- ``https://<bucket>.s3[.<region>].amazonaws.com/<key>``
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

from .db import _models, _row

_UUID_RE = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"

_PATH_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    # Backend byte endpoint + the FE's canonical /s/[token] share page —
    # both carry a platform.share_links token.
    ("share", re.compile(r"^/share/(?P<token>[^/]+)/?$")),
    ("share_download", re.compile(r"^/share/(?P<token>[^/]+)/download/?$")),
    ("share", re.compile(r"^/s/(?P<token>[^/]+)/?$")),
    ("file_id_download", re.compile(rf"^/files/(?P<file_id>{_UUID_RE})/download/?$")),
    ("file_id_url", re.compile(rf"^/files/(?P<file_id>{_UUID_RE})/url/?$")),
    ("file_id_get", re.compile(rf"^/files/(?P<file_id>{_UUID_RE})/?$")),
    ("file_by_path", re.compile(r"^/files/by-path/(?P<path>.+)$")),
]

_OUR_HOST_SUFFIXES = {
    "aimatrx.com",
    "aidream.ai",
    # The server that mints every durable private-file URL
    # (``render_urls.durable_inline_url`` → ``server.app.matrxserver.com``).
    # Missing it classified our OWN ``/files/{id}/download`` URLs as external,
    # so the media funnel fetched them anonymously and got 401 (podcast W8
    # compose, 2026-10-07). ``cdn.matrxserver.com`` is matched earlier by
    # ``parse_cdn_url``; other hosts here only count on a ``/files`` path.
    "matrxserver.com",
    "localhost",
    "127.0.0.1",
}


def _our_hosts() -> set[str]:
    """Static host suffixes plus the host durable file URLs are minted on.

    ``render_urls.files_public_base_url()`` is the ONE base every
    ``/files/{id}/download`` URL is built from; whatever host it names is ours
    by construction, so a deployment on a new domain never mints URLs its own
    resolver calls external.
    """
    hosts = set(_OUR_HOST_SUFFIXES)
    try:
        from .render_urls import files_public_base_url

        base = files_public_base_url()
    except Exception:
        base = None
    if base:
        base_host = urlparse(base).hostname
        if base_host:
            hosts.add(base_host)
    return hosts

_S3_HOST_RE = re.compile(r"^(?P<bucket>[a-z0-9.\-]+)\.s3(?:\.[a-z0-9-]+)?\.amazonaws\.com$")
_S3_VHOST_PATH_RE = re.compile(r"^/(?P<bucket>[a-z0-9.\-]+)/(?P<key>.+)$")


@dataclass
class ResolvedFile:
    """Result of recognizing + DB-resolving a media URL."""

    is_ours: bool = False
    kind: str = "unknown"
    file_id: str | None = None
    owner_id: str | None = None
    file_path: str | None = None
    mime_type: str | None = None
    file_size: int | None = None
    storage_uri: str | None = None
    published_to_web: bool = False
    share_token: str | None = None
    is_share_link: bool = False
    raw_url: str = ""
    error: str | None = None

    def can_get_bytes(self) -> bool:
        return self.is_ours and self.storage_uri is not None


def _our_bucket_set() -> set[str]:
    """Bucket names this deployment treats as ours (for s3:// matching).

    Includes the default bucket (private/shared assets) AND the
    dedicated public bucket when the CDN feature is configured. Lazy +
    best-effort; the resolver still works if we can't read settings.

    Each attribute is read in its own try/except because the matrx-utils
    settings proxy raises NotConfiguredError (not AttributeError) when
    a name isn't set, so a single try/except around the whole loop
    would swallow ALL remaining attrs after the first miss.
    """
    out: set[str] = set()
    try:
        from matrx_utils.conf import settings
    except Exception:
        return out
    for attr in ("AWS_S3_DEFAULT_BUCKET", "AIDREAM_S3_BUCKET", "AWS_S3_PUBLIC_BUCKET"):
        try:
            val = getattr(settings, attr, None)
        except Exception:
            val = None
        if val:
            out.add(str(val))
    return out


def classify_url(url: str) -> dict[str, Any]:
    """Cheap structural classification (no DB lookup). Public for tests."""
    if not url:
        return {"kind": "unknown"}
    url = url.strip()

    if url.startswith("s3://"):
        m = re.match(r"^s3://(?P<bucket>[^/]+)/(?P<key>.+)$", url)
        if m:
            bucket = m.group("bucket")
            return {
                "kind": "s3",
                "bucket": bucket,
                "key": m.group("key"),
                "is_ours": bucket in _our_bucket_set(),
            }
    # CDN host — checked first so cdn.matrxserver.com doesn't fall
    # through to the our-host matcher (it isn't a *.aimatrx.com host).
    from .cdn import parse_cdn_url

    cdn_match = parse_cdn_url(url)
    if cdn_match:
        return cdn_match

    parsed = urlparse(url)
    if not parsed.scheme.startswith("http"):
        return {"kind": "unknown"}

    host = parsed.hostname or ""
    is_our_host = any(host == h or host.endswith("." + h) for h in _our_hosts())

    s3_match = _S3_HOST_RE.match(host)
    if s3_match:
        bucket = s3_match.group("bucket")
        return {
            "kind": "s3",
            "host": host,
            "bucket": bucket,
            "key": parsed.path.lstrip("/"),
            "is_ours": bucket in _our_bucket_set(),
        }
    if "amazonaws.com" in host and parsed.path:
        m = _S3_VHOST_PATH_RE.match(parsed.path)
        if m:
            bucket = m.group("bucket")
            return {
                "kind": "s3",
                "host": host,
                "bucket": bucket,
                "key": m.group("key"),
                "is_ours": bucket in _our_bucket_set(),
            }

    if not is_our_host:
        return {"kind": "external"}

    for label, pattern in _PATH_PATTERNS:
        m = pattern.match(parsed.path)
        if m:
            return {"kind": label, "is_ours": True, **m.groupdict()}

    return {"kind": "external_our_host", "path": parsed.path}


def file_id_from_our_url(url: str | None) -> str | None:
    """Recover the ``cld_files`` id from a URL WE minted, else ``None``.

    THE POINT: a signed URL is a handoff, never an identity — but a producer
    that already handed one out has, structurally, not lost the identity. Every
    URL this platform mints carries the id (the object key is ``{owner}/{file_id}``
    and the ``/files/{id}`` route names it outright), so a consumer holding one of
    our URLs can always get back to the durable handle instead of storing a link
    that dies. This is the ONE recovery — no caller writes its own UUID regex.

    Recognized, via the same ``classify_url`` every other consumer uses:

    - our CDN URL          ``https://cdn.…/{owner}/{file_id}?v=…``
    - our S3 URL           ``https://…s3….amazonaws.com/{owner}/{file_id}``
    - ``s3://…`` URIs on one of our buckets
    - our ``/files/{file_id}`` routes (and ``/download`` / ``/url`` variants)
    - a bare ``file_id`` (the canonical internal handle — passed straight back)

    Returns ``None`` for an external URL, a share link (the token is not an id),
    and any of our shapes whose key does not end in a UUID. ``None`` means "this
    URL does not name a file of ours", NOT "the file does not exist" — it is
    never a reason to drop the URL a caller already has.
    """
    if not url:
        return None
    url = url.strip()
    if re.fullmatch(_UUID_RE, url):
        return url

    info = classify_url(url)
    if not info.get("is_ours"):
        return None

    file_id = info.get("file_id")
    if file_id:
        return str(file_id)

    key = info.get("key")
    if not key:
        return None
    # Object keys are ``{owner_id}/{file_id}[/…]``: BOTH segments are UUIDs, so
    # take the LAST UUID segment, never the first. Reading index 0 hands back
    # the owner's id — a valid-looking UUID that names the wrong row entirely.
    uuids = [seg for seg in str(key).split("/") if re.fullmatch(_UUID_RE, seg)]
    return uuids[-1] if uuids else None


def _populate_from_record(rf: ResolvedFile, record: dict) -> None:
    rf.file_id = record["id"]
    # Accept both the Python concept (owner_id, when the record came through
    # DatabaseClient's read shim) and the canonical files.files column
    # (created_by, when selected directly via the Files model).
    rf.owner_id = record.get("owner_id") or record.get("created_by")
    rf.file_path = record["file_path"]
    rf.mime_type = record.get("mime_type")
    rf.file_size = record.get("size_bytes")
    rf.storage_uri = record.get("storage_uri")
    rf.published_to_web = bool(record.get("published_to_web"))


def resolve_file_url(url: str, db: Any) -> ResolvedFile:
    """Recognize a URL and load the canonical file metadata, sync.

    ``db`` is a ``DatabaseClient`` instance. Pass ``fm.sync_engine.db``
    from a FileManager. Sync-only — uses the ORM ``_sync`` twins, which
    refuse to run inside a live event loop (use the async variant there).
    """
    info = classify_url(url)
    rf = ResolvedFile(raw_url=url, kind=info.get("kind", "unknown"))
    if not info.get("is_ours"):
        return rf

    rf.is_ours = True
    if db is None:
        rf.error = "no_db_client"
        return rf

    try:
        if info["kind"] in ("share", "share_download"):
            rf.share_token = info["token"]
            rf.is_share_link = True
            link = db.get_share_link(rf.share_token)
            if not link or link.get("resource_type") != "file":
                rf.error = "share_link_not_a_file_or_inactive"
                return rf
            rec = db.get_file(link["resource_id"])
            if not rec:
                rf.error = "shared_file_not_found"
                return rf
            _populate_from_record(rf, rec)
            return rf

        if info["kind"] in ("file_id_download", "file_id_url", "file_id_get"):
            rf.file_id = info["file_id"]
            rec = db.get_file(rf.file_id)
            if not rec:
                rf.error = "file_not_found"
                return rf
            _populate_from_record(rf, rec)
            return rf

        if info["kind"] == "file_by_path":
            rf.file_path = info["path"]
            return rf

        if info["kind"] == "s3":
            uri = f"s3://{info['bucket']}/{info['key']}"
            rf.storage_uri = uri
            try:
                mf, _ = _models()
                rec = _row(mf.Files.filter(storage_uri=uri, deleted_at__isnull=True).first_sync())
                if rec:
                    _populate_from_record(rf, rec)
            except Exception:
                pass
            return rf

        if info["kind"] == "cdn":
            # CDN URL: cdn.matrxserver.com/<key>?v=<...> → look up by
            # storage_uri = s3://<public_bucket>/<key>. The public bucket
            # name comes from the CDN config (typically equals the CDN
            # host). The strip-and-lookup shape is identical to the s3://
            # branch; only the URI we look for differs.
            bucket = info.get("bucket")
            if not bucket:
                rf.error = "cdn_public_bucket_unconfigured"
                return rf
            uri = f"s3://{bucket}/{info['key']}"
            rf.storage_uri = uri
            try:
                mf, _ = _models()
                rec = _row(mf.Files.filter(storage_uri=uri, deleted_at__isnull=True).first_sync())
                if rec:
                    _populate_from_record(rf, rec)
                    return rf
            except Exception:
                pass
            rf.error = "cdn_url_not_in_files"
            return rf

    except Exception as e:
        rf.error = f"resolver_error: {type(e).__name__}: {e}"

    return rf


async def resolve_file_url_async(url: str, db: Any) -> ResolvedFile:
    """Async variant of ``resolve_file_url`` — uses the async ORM query
    API. Safe to call from any FastAPI handler / async context with no
    thread-pool dispatch.

    Same return shape as the sync variant.
    """
    info = classify_url(url)
    rf = ResolvedFile(raw_url=url, kind=info.get("kind", "unknown"))
    if not info.get("is_ours"):
        return rf

    rf.is_ours = True
    if db is None:
        rf.error = "no_db_client"
        return rf

    try:
        if info["kind"] in ("share", "share_download"):
            rf.share_token = info["token"]
            rf.is_share_link = True
            link = await db.get_share_link_async(rf.share_token)
            if not link or link.get("resource_type") != "file":
                rf.error = "share_link_not_a_file_or_inactive"
                return rf
            rec = await db.get_file_async(link["resource_id"])
            if not rec:
                rf.error = "shared_file_not_found"
                return rf
            _populate_from_record(rf, rec)
            return rf

        if info["kind"] in ("file_id_download", "file_id_url", "file_id_get"):
            rf.file_id = info["file_id"]
            rec = await db.get_file_async(rf.file_id)
            if not rec:
                rf.error = "file_not_found"
                return rf
            _populate_from_record(rf, rec)
            return rf

        if info["kind"] == "file_by_path":
            rf.file_path = info["path"]
            return rf

        if info["kind"] == "s3":
            uri = f"s3://{info['bucket']}/{info['key']}"
            rf.storage_uri = uri
            try:
                mf, _ = _models()
                rec = _row(await mf.Files.filter(storage_uri=uri, deleted_at__isnull=True).first())
                if rec:
                    _populate_from_record(rf, rec)
            except Exception:
                pass
            return rf

        if info["kind"] == "cdn":
            # See sync variant — same shape.
            bucket = info.get("bucket")
            if not bucket:
                rf.error = "cdn_public_bucket_unconfigured"
                return rf
            uri = f"s3://{bucket}/{info['key']}"
            rf.storage_uri = uri
            try:
                mf, _ = _models()
                rec = _row(await mf.Files.filter(storage_uri=uri, deleted_at__isnull=True).first())
                if rec:
                    _populate_from_record(rf, rec)
                    return rf
            except Exception:
                pass
            rf.error = "cdn_url_not_in_files"
            return rf

    except Exception as e:
        rf.error = f"resolver_error: {type(e).__name__}: {e}"

    return rf


__all__ = ["ResolvedFile", "classify_url", "resolve_file_url", "resolve_file_url_async"]
