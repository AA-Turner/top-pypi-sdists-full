"""Public-CDN URL helpers for cloud_sync.

Centralises every decision about whether a file is CDN-eligible and how
to mint a public URL for it. Lives at the foundation layer so any
package or host application can use the same primitive.

Architecture (bucket-isolation):
    - Public assets live in their own dedicated S3 bucket whose name
      equals the CDN host (e.g. ``cdn.matrxserver.com``).
    - Private/shared assets stay in the default bucket
      (``matrx-user-files``) with Block Public Access fully ON.
    - Cloudflare CNAMEs the CDN host → the regional path-style S3
      endpoint and preserves the original Host header. S3 uses that
      header to route to the public bucket; no Origin Rule needed.
    - Cache-busting is content-hash based: every CDN URL ends with
      ``?v=<checksum[:8]>`` so a content change → new URL → instant
      cache miss without an explicit purge call.

Configuration:
    Two env vars (or settings) MUST both be set for the CDN to be
    active:
        CDN_PUBLIC_BASE_URL  e.g. "https://cdn.matrxserver.com"
        AWS_S3_PUBLIC_BUCKET e.g. "cdn.matrxserver.com"
    When either is empty/unset, ``public_url_for`` returns ``None`` and
    callers fall back to AWS-signed URLs.

Public API:
    public_bucket_or_raise(ctx)  The public bucket, or a LOUD failure. The ONLY
                                 way to resolve a bucket for a PUBLIC write —
                                 never fall back to the private bucket.
    public_url_for(record)       Build the CDN URL or return None.
    parse_cdn_url(url)           Reverse: pull (host, key) from a CDN URL.
    cdn_base_host()              The configured CDN host (or None).
    public_bucket()              The configured public S3 bucket name.
    is_public_storage_uri(uri)   True iff uri lives in the public bucket.

The boundary normalizer at AI Dream uses ``parse_cdn_url`` (via
``url_resolver.classify_url``) so any CDN URL the FE sends inside an
``MediaRef`` resolves back to a ``cld_files`` row exactly like a share
link or ``/files/{id}/url`` does.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse


def _setting(*names: str) -> str | None:
    """Read the first non-empty value of any of the given setting names.

    Tries upper-case and lower-case forms. Returns ``None`` when nothing
    is configured. Failures (matrx_utils settings not configured at all)
    are swallowed — the CDN feature degrades to OFF rather than raising.

    🚨 That swallow is only safe because OFF is now LOUD where it matters: a
    PUBLIC write goes through ``public_bucket_or_raise`` and fails outright
    instead of quietly using the private bucket. Never add a consumer that
    reads this as "no CDN, use the default bucket" for a public asset.
    """
    try:
        from matrx_utils.conf import settings
    except Exception:
        return None
    for name in names:
        for variant in (name, name.upper(), name.lower()):
            try:
                v = getattr(settings, variant, None)
            except Exception:
                v = None
            if v:
                return str(v).strip() or None
    return None


def _cdn_base_url() -> str | None:
    raw = _setting("CDN_PUBLIC_BASE_URL", "cdn_public_base_url")
    return raw.rstrip("/") if raw else None


def cdn_base_host() -> str | None:
    """The host part of the configured CDN base URL, lowercased.

    Used by ``url_resolver.classify_url`` to recognize CDN URLs as ours.
    """
    base = _cdn_base_url()
    if not base:
        return None
    parsed = urlparse(base)
    return (parsed.hostname or "").lower() or None


def public_bucket() -> str | None:
    """Configured S3 bucket name that holds public assets.

    Returns ``None`` when the CDN feature is OFF — meaning either
    AWS_S3_PUBLIC_BUCKET or CDN_PUBLIC_BASE_URL is unset.
    """
    if not _cdn_base_url():
        return None
    return _setting("AWS_S3_PUBLIC_BUCKET", "aws_s3_public_bucket")


def is_public_storage_uri(storage_uri: str | None) -> bool:
    """True iff the storage_uri's bucket is the configured public bucket."""
    if not storage_uri:
        return False
    pb = public_bucket()
    if not pb:
        return False
    m = re.match(r"^[a-z0-9+\-_]+://([^/]+)/", storage_uri)
    return bool(m) and m.group(1) == pb


def public_key_from_storage_uri(storage_uri: str | None) -> str | None:
    """Pull the S3 key (the bit after ``s3://<bucket>/``) when the URI
    points at the public bucket. Returns None otherwise.
    """
    if not is_public_storage_uri(storage_uri):
        return None
    m = re.match(r"^[a-z0-9+\-_]+://[^/]+/(.+)$", storage_uri or "")
    return m.group(1) if m else None


def public_url_for(record: dict[str, Any] | None) -> str | None:
    """Build the public CDN URL for a ``cld_files`` row, or return None.

    Returns ``None`` whenever ANY of these is true:
      - CDN_PUBLIC_BASE_URL or AWS_S3_PUBLIC_BUCKET is unset.
      - record is missing or is not published to the web.
      - record's storage_uri is not in the public bucket (i.e. an
        existing pre-CDN public file that hasn't been migrated yet —
        the caller falls back to a signed URL).
      - record is soft-deleted.

    The URL always carries a ``?v=<checksum[:8]>`` cache-buster when a
    checksum is available; that buster invalidates Cloudflare instantly
    on content change without a purge call.
    """
    if not record:
        return None
    if record.get("deleted_at"):
        return None
    if not record.get("published_to_web"):
        return None
    base = _cdn_base_url()
    if not base:
        return None
    key = public_key_from_storage_uri(record.get("storage_uri"))
    if not key:
        return None
    checksum = (record.get("checksum") or "").strip()
    if checksum:
        return f"{base}/{key}?v={checksum[:8]}"
    return f"{base}/{key}"


def parse_cdn_url(url: str) -> dict[str, Any] | None:
    """If ``url`` matches the configured CDN host, return ``{"key": "..."}``.

    The returned key is the client-visible path (the bit AFTER the
    base host), suitable for reconstructing the underlying S3
    ``storage_uri`` as ``s3://<public_bucket>/<key>``. Returns ``None``
    when the CDN is disabled or the URL is not on our CDN host.
    """
    host = cdn_base_host()
    if not host:
        return None
    if not url:
        return None
    parsed = urlparse(url.strip())
    if not parsed.scheme.startswith("http"):
        return None
    url_host = (parsed.hostname or "").lower()
    if url_host != host:
        return None
    key = parsed.path.lstrip("/")
    if not key:
        return None
    return {"kind": "cdn", "is_ours": True, "key": key, "host": host, "bucket": public_bucket()}


__all__ = [
    "cdn_base_host",
    "public_bucket",
    "is_public_storage_uri",
    "public_key_from_storage_uri",
    "public_url_for",
    "parse_cdn_url",
]


class PublicBucketUnconfiguredError(RuntimeError):
    """A PUBLIC write was requested and there is nowhere public to put it.

    Deliberately fatal. See :func:`public_bucket_or_raise`.
    """


def public_bucket_or_raise(context: str) -> str:
    """The public bucket, or a LOUD failure. Never a private-bucket fallback.

    🚨 DO NOT "FIX" THIS BY ADDING `or resolve_s3_bucket()`. That line was here
    for years, framed as a single-bucket-dev convenience, and it is the reason
    this function exists.

    What it did: a caller asked for a PUBLIC file. With the CDN unconfigured,
    `public_bucket()` returned None, so the bytes went into the DEFAULT bucket —
    the private one, with S3 Block Public Access fully ON. The row was still
    written as published to the web. The result is a file the system believes is
    world-readable, whose bytes no anonymous reader can ever reach, and whose
    every URL is therefore a signed one that expires. A podcast cover, a blog
    image, an OG card: all silently broken, days later, with a green run.

    That is not a fallback. A fallback substitutes an equivalent — a second CDN
    serving the same bytes to the same audience. Writing a public asset into a
    private bucket substitutes something that DOES NOT DO THE JOB AT ALL, and
    says nothing. There is no correct silent degradation here: a "public" file
    that cannot be read publicly is a lie, and the only honest options are to
    store it publicly or to refuse.

    So this refuses. Configure `CDN_PUBLIC_BASE_URL` + `AWS_S3_PUBLIC_BUCKET`
    (both, always together — either one alone leaves the feature OFF), or write
    the file unpublished and mean it. Local dev included: a dev whose public
    uploads silently become private is a dev shipping this bug to production.

    Guard: packages/matrx-files/tests/test_public_bucket_no_silent_fallback.py
    Law: common-docs/systems/files/media-durability/FEATURE.md
    """
    bucket = public_bucket()
    if bucket:
        return bucket
    raise PublicBucketUnconfiguredError(
        f"{context}: a PUBLIC file was requested but the public bucket is not "
        "configured (CDN_PUBLIC_BASE_URL and AWS_S3_PUBLIC_BUCKET must BOTH be "
        "set — either one alone leaves the CDN feature off). Refusing to write "
        "it into the private bucket: the row would say published_to_web "
        "while the bytes sit behind Block Public Access, so every URL minted "
        "for it would be a signed one that expires and the page embedding it "
        "would break silently. Configure the public bucket, or persist this "
        "file unpublished."
    )
