"""Small shared helpers for safely logging URLs.

RTSP/HTTP source URLs routinely carry credentials — either as ``user:pass@``
userinfo (the norm for RTSP cameras) or as a signed ``?...`` query string (AWS
presigned URLs, SAS tokens). Logging such a URL verbatim leaks those secrets to
centralized log stores. Route every ``source``/``url`` value through
:func:`redact_url` before logging it.
"""

from urllib.parse import urlparse, urlunparse

__all__ = ["redact_url"]


def redact_url(url: object) -> str:
    """Return a log-safe form of ``url`` with credentials stripped.

    Removes both the ``user:pass@`` userinfo and the ``?...`` query string /
    fragment (which frequently carry presigned tokens), while preserving the
    scheme, host, port and path so the value is still useful for debugging.

    Non-URL / non-string inputs and unparseable values are returned as a plain
    ``str`` (with any embedded ``user:pass@`` masked) so callers can use this
    unconditionally.
    """
    if url is None:
        return ""
    text = url if isinstance(url, str) else str(url)
    try:
        parsed = urlparse(text)
    except Exception:
        parsed = None

    if parsed is not None and parsed.scheme and parsed.netloc:
        host = parsed.hostname or ""
        if parsed.port is not None:
            host = f"{host}:{parsed.port}"
        # Mark that userinfo was present but never emit it.
        if parsed.username or parsed.password:
            host = f"***@{host}"
        return urlunparse((parsed.scheme, host, parsed.path, "", "", ""))

    # Fallback for bare strings that still embed userinfo (e.g. "user:pass@host").
    if "@" in text and "//" not in text:
        return "***@" + text.split("@", 1)[1]
    return text
