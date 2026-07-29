"""Auto-generated stub for module: logging_config."""
from typing import Any

# Functions
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
    ...
def redact_url(url: Any) -> Any:
    """
    Return ``url`` with credentials stripped for safe logging.
    
        Removes both the ``?...`` query string (presigned-URL signatures live
        there) and any ``user:pass@`` userinfo from the netloc. RTSP/HTTP(S)
        presigned URLs are the primary target. Non-string / unparseable inputs
        are returned coerced to ``str`` unchanged.
    """
    ...
def scrub_message(message: Any) -> Any:
    """
    Scrub credential-shaped substrings out of an already-formatted string.
    """
    ...
def scrub_sensitive(name: Any, value: Any, redacted: Any = '<redacted>') -> Any:
    """
    Return ``repr(value)`` unless ``name`` looks sensitive, else ``<redacted>``.
    
        Used by error-report parameter/context capture so credential-bearing
        locals (access_key, secret_key, token, password, ...) never get serialized
        into logs or the Kafka error_logs topic.
    """
    ...

# Classes
class RedactingFilter:
    # logging.Filter backstop that scrubs secrets from every log record.
    #
    #     Applied on the root logger by ``configure_logging`` so that even if a
    #     caller logs a raw bearer/refresh token, access/secret key, or a redis
    #     ``--requirepass`` value, the emitted line has the value replaced with
    #     ``<redacted>``. This is defense-in-depth; call sites should still redact
    #     at the source.

    def filter(self: Any, record: Any.Any) -> bool: ...

