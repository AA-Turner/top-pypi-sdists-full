"""THE definition of "is this URL expiring?" — owned by the package that mints them.

A signed URL is a **temporary grant of access to a third party**. It is minted at
the moment of handoff, used immediately, and dies. That is its entire purpose.

It is NOT an identifier, and it must never be how one part of this platform tells
another part which file it means. Internally we pass the ``file_id`` — the same way
we pass a user id rather than carrying a person's whole record around. Anything that
needs bytes or a URL resolves one from the id, fresh, at the moment it needs it.

WHY THIS MODULE EXISTS: this classifier previously existed as three hand-maintained
copies — ``aidream/services/media_durability.py``, the frontend
``lib/media/durability.ts``, and the Postgres ``mtx_is_durable_media_url`` guard —
each carrying a comment saying "keep all three in sync". They drifted. A detector
that knows only SigV4 mistakes a SigV2 URL for a permanent one, skips the re-mint
path, and the media goes dark forever once the signature expires. ``matrx-files``
mints every signed URL in this platform, so ``matrx-files`` owns what one looks
like; the other layers consume this.

Route ALL signed-URL detection through here. Never write another ``X-Amz`` regex.
"""

from __future__ import annotations

import re
from datetime import datetime, UTC
from urllib.parse import parse_qs, urlsplit

# Matches BOTH AWS signing dialects. Deliberately broad: the presence of any of
# these query keys means the URL carries a time-limited signature.
#
#   SigV2 (query-string auth): ?AWSAccessKeyId=…&Signature=…&Expires=<epoch>
#   SigV4 (presigned):         ?X-Amz-Credential=…&X-Amz-Signature=…&X-Amz-Expires=…
_SIGNED_URL_RE = re.compile(
    r"[?&](x-amz-signature|x-amz-credential|x-amz-date|x-amz-expires"
    r"|awsaccesskeyid|signature|expires)=",
    re.IGNORECASE,
)


def is_signed_url(url: str | None) -> bool:
    """True when ``url`` carries a time-limited signature in either AWS dialect.

    An empty/None url is not signed (there is nothing to expire).
    """
    if not url:
        return False
    return _SIGNED_URL_RE.search(url) is not None


def signed_url_expiry_ms(url: str | None) -> int | None:
    """Ms-epoch when ``url``'s signature dies, read out of the URL itself.

    The mint path always knows the TTL and reports it alongside the URL
    (``signed_url_expires_at``); this is the RECOVERY path for a URL that
    reached a wire shape without its expiry — see the invariant enforced in
    ``asset_envelope``. Same ownership argument as ``is_signed_url``: the
    package that mints these URLs owns how to read them, and no other layer
    writes an ``X-Amz`` regex.

    Both AWS dialects:

      SigV4:  ``X-Amz-Date=20260820T101112Z`` + ``X-Amz-Expires=3600``
      SigV2:  ``Expires=<epoch seconds>`` (also CloudFront canned policies)

    ``None`` when the URL is empty, unsigned, or signed by a scheme that does
    not carry its own deadline — a caller that gets ``None`` genuinely cannot
    know when the grant dies and must not invent one.
    """
    if not url:
        return None
    try:
        params = {k.lower(): v for k, v in parse_qs(urlsplit(url).query).items()}
    except ValueError:
        return None

    signed_at = params.get("x-amz-date", [None])[0]
    ttl = params.get("x-amz-expires", [None])[0]
    if signed_at and ttl:
        try:
            start = datetime.strptime(signed_at, "%Y%m%dT%H%M%SZ").replace(tzinfo=UTC)
            return int((start.timestamp() + int(ttl)) * 1000)
        except (ValueError, OverflowError):
            return None

    absolute = params.get("expires", [None])[0]
    if absolute:
        try:
            return int(absolute) * 1000
        except ValueError:
            return None
    return None


def is_durable_media_url(value: str | None) -> bool:
    """True for empty / CDN / public / genuinely-external URLs.

    A durable URL may be stored, persisted into a database column, embedded in a
    public page, or handed to a social crawler. A non-durable value may do none
    of those things — it may only be minted, handed to its consumer, forgotten.

    False for two kinds of value:

    1. An expiring **signed URL** — it dies on a timer.
    2. Anything that is **not a URL at all**, e.g. a bare ``file_id``. A UUID is
       the correct internal handle, but it is meaningless in a column an
       anonymous browser reads, and every alarm we own (the heal pass, the
       Postgres public-URL guard, the frontend violation reporter) keys off this
       function. Calling a UUID "durable" would make a broken public page
       triple-silent: no heal, no guard row, no scream. It is not durable *as a
       URL*; it needs resolving first.
    """
    if not value:
        return True
    if is_signed_url(value):
        return False
    return _looks_like_url(value)


def _looks_like_url(value: str) -> bool:
    """A value usable as a `src`/`href` by something outside this platform."""
    candidate = value.strip().lower()
    return candidate.startswith(("http://", "https://", "data:", "//"))


__all__ = ["is_durable_media_url", "is_signed_url", "signed_url_expiry_ms"]
