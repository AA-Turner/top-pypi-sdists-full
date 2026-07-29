"""
Centralized logging configuration for matrice_common.

Applications should call configure_logging() once at startup so that
LOG_LEVEL controls verbosity (e.g. WARNING in production, DEBUG in dev).

This module also hosts the shared secret-redaction helpers used across the
SDK (``redact_url``, ``scrub_sensitive``) and a durable ``logging.Filter``
backstop that scrubs credential-shaped substrings out of every log record.
These live here because this is a dependency-free leaf module (only ``logging``
/ ``os`` / ``re`` / ``urllib``), so ``rpc``/``errors``/stream modules can import
the helpers without creating an import cycle.
"""

import logging
import os
import re
from urllib.parse import urlsplit, urlunsplit

# Parameter/field names that must never have their value logged verbatim.
_SENSITIVE_NAME_RE = re.compile(
    r"(secret|password|passwd|token|access[_-]?key|secret[_-]?key|api[_-]?key|"
    r"authorization|auth[_-]?token|bearer|credential|requirepass)",
    re.IGNORECASE,
)

# Substring patterns scrubbed out of already-formatted log messages as a
# last-resort backstop (H1/H2/H3/L3). Each matches "<label><separator><value>"
# and replaces the value with <redacted> while keeping the label for context.
_LOG_SCRUB_PATTERNS = [
    # Authorization: Bearer <jwt>  /  Bearer <jwt>
    (re.compile(r"(Bearer)\s+[A-Za-z0-9._\-+/=]+", re.IGNORECASE), r"\1 <redacted>"),
    # accessKey=... / secretKey=... / refreshToken=... / access_key: ...  (json or kv)
    (
        re.compile(
            r"([\"']?(?:access[_-]?key|secret[_-]?key|refresh[_-]?token|"
            r"secret[_-]?access[_-]?key|api[_-]?key|password)[\"']?\s*[:=]\s*)"
            r"[\"']?[^\s,;}\"']+[\"']?",
            re.IGNORECASE,
        ),
        r"\1<redacted>",
    ),
    # redis --requirepass <value>
    (re.compile(r"(--requirepass)\s+\S+", re.IGNORECASE), r"\1 <redacted>"),
]


def redact_url(url):
    """Return ``url`` with credentials stripped for safe logging.

    Removes both the ``?...`` query string (presigned-URL signatures live
    there) and any ``user:pass@`` userinfo from the netloc. RTSP/HTTP(S)
    presigned URLs are the primary target. Non-string / unparseable inputs
    are returned coerced to ``str`` unchanged.
    """
    if not url:
        return url
    try:
        parts = urlsplit(str(url))
    except Exception:
        return str(url)
    netloc = parts.netloc
    if "@" in netloc:
        # Drop the "user:pass@" userinfo, keep host[:port].
        netloc = netloc.rsplit("@", 1)[1]
    # Blank out the query (signatures/tokens) and fragment.
    redacted = urlunsplit((parts.scheme, netloc, parts.path, "", ""))
    if parts.query:
        redacted = redacted + "?<redacted>"
    return redacted


def scrub_sensitive(name, value, redacted="<redacted>"):
    """Return ``repr(value)`` unless ``name`` looks sensitive, else ``<redacted>``.

    Used by error-report parameter/context capture so credential-bearing
    locals (access_key, secret_key, token, password, ...) never get serialized
    into logs or the Kafka error_logs topic.
    """
    if name and _SENSITIVE_NAME_RE.search(str(name)):
        return redacted
    return value


def scrub_message(message):
    """Scrub credential-shaped substrings out of an already-formatted string."""
    if not message:
        return message
    text = str(message)
    for pattern, repl in _LOG_SCRUB_PATTERNS:
        text = pattern.sub(repl, text)
    return text


class RedactingFilter(logging.Filter):
    """logging.Filter backstop that scrubs secrets from every log record.

    Applied on the root logger by ``configure_logging`` so that even if a
    caller logs a raw bearer/refresh token, access/secret key, or a redis
    ``--requirepass`` value, the emitted line has the value replaced with
    ``<redacted>``. This is defense-in-depth; call sites should still redact
    at the source.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            if isinstance(record.msg, str):
                # If there are % args, scrub the fully-rendered message and
                # collapse args so we don't re-substitute an unscrubbed value.
                if record.args:
                    record.msg = scrub_message(record.getMessage())
                    record.args = ()
                else:
                    record.msg = scrub_message(record.msg)
        except Exception:
            # Never let logging redaction raise inside the logging path.
            pass
        return True


def configure_logging() -> None:
    """
    Configure the root logger from the LOG_LEVEL environment variable.

    Call once at application startup. If the root logger already has
    handlers, this is a no-op to avoid duplicate configuration.

    Environment
    -----------
    LOG_LEVEL : str, optional
        One of DEBUG, INFO, WARNING, ERROR, CRITICAL. Default is WARNING
        so that debug/info output is silent in production.
    """
    root = logging.getLogger()
    if not root.handlers:
        level_name = os.getenv("LOG_LEVEL", "WARNING").upper()
        level = getattr(logging, level_name, logging.WARNING)
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(name)s %(levelname)s %(message)s",
        )
    # Install the scrubbing filter on the root logger AND every root handler.
    # Handler-level filters are what actually scrub records that propagate up
    # from child loggers, so both are covered here (idempotent).
    _install_redaction_filter(root)
    for handler in root.handlers:
        _install_redaction_filter(handler)


def _install_redaction_filter(target) -> None:
    """Attach a single RedactingFilter to a logger/handler (idempotent)."""
    try:
        if any(isinstance(f, RedactingFilter) for f in getattr(target, "filters", [])):
            return
        target.addFilter(RedactingFilter())
    except Exception:
        pass
