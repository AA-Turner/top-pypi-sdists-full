"""Auto-generated stub for module: url_redact."""
from typing import Any

from urllib.parse import urlparse, urlunparse

# Functions
def redact_url(url: Any) -> str: ...
    """
    Return a log-safe form of ``url`` with credentials stripped.
    
        Removes both the ``user:pass@`` userinfo and the ``?...`` query string /
        fragment (which frequently carry presigned tokens), while preserving the
        scheme, host, port and path so the value is still useful for debugging.
    
        Non-URL / non-string inputs and unparseable values are returned as a plain
        ``str`` (with any embedded ``user:pass@`` masked) so callers can use this
        unconditionally.
    """
