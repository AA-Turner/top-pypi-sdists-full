import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse, urlunparse

logger = logging.getLogger(__name__)

# Substrings (case-insensitive) that mark a mapping key as holding a secret.
# Values for matching keys are redacted before logging.
_SENSITIVE_KEY_PATTERNS = (
    "secret",
    "password",
    "passwd",
    "token",
    "access_key",
    "accesskey",
    "secret_key",
    "secretkey",
    "refresh",
    "authorization",
    "auth_key",
    "authkey",
    "apikey",
    "api_key",
    "requirepass",
)


def redact_url(value: Any) -> Any:
    """Redact sensitive material from a URL string.

    Strips the query string (which can carry presigned-URL access tokens) and
    any ``user:pass@`` userinfo from the netloc. Non-string / non-URL values are
    returned unchanged so this is safe to apply defensively.
    """
    if not isinstance(value, str) or "://" not in value:
        return value
    try:
        parsed = urlparse(value)
    except (ValueError, TypeError):
        return "<redacted-url>"
    netloc = parsed.netloc
    if "@" in netloc:
        # Drop userinfo (user:pass@), keep host[:port].
        netloc = netloc.rsplit("@", 1)[1]
    # Drop query and fragment (presigned tokens, signatures live here).
    redacted_query = "REDACTED" if parsed.query else ""
    return urlunparse((parsed.scheme, netloc, parsed.path, "", redacted_query, ""))


def _is_sensitive_key(key: Any) -> bool:
    """Return True if a mapping key name looks like it holds a secret."""
    if not isinstance(key, str):
        return False
    lowered = key.lower()
    return any(pat in lowered for pat in _SENSITIVE_KEY_PATTERNS)


def redact_sensitive(obj: Any, _depth: int = 0) -> Any:
    """Recursively redact secrets and URL tokens from a value for safe logging.

    - Values under sensitive-looking keys (secret/password/token/access_key/...)
      are replaced with a boolean-presence marker rather than the value.
    - String values that look like URLs have their query string / userinfo
      stripped via :func:`redact_url`.
    Depth is bounded to avoid pathological nesting.
    """
    if _depth > 6:
        return "<redacted-depth>"
    if isinstance(obj, dict):
        redacted: Dict[Any, Any] = {}
        for key, val in obj.items():
            if _is_sensitive_key(key):
                redacted[key] = f"present={bool(val)}"
            else:
                redacted[key] = redact_sensitive(val, _depth + 1)
        return redacted
    if isinstance(obj, (list, tuple)):
        return type(obj)(redact_sensitive(v, _depth + 1) for v in obj)
    return redact_url(obj)


def create_async_redis_client(
    host: str = "localhost",
    port: int = 6379,
    password: Optional[str] = None,
    username: Optional[str] = None,
    db: int = 0,
    sentinel_hosts: Optional[List[Tuple[str, int]]] = None,
    master_name: Optional[str] = None,
    decode_responses: bool = False,
    socket_keepalive: bool = True,
    socket_timeout: int = 30,
    health_check_interval: int = 30,
    max_connections: Optional[int] = None,
    socket_connect_timeout: Optional[int] = None,
):
    """Create an async Redis client, with Sentinel support if configured.

    Args:
        host: Redis host (used as fallback if Sentinel not configured)
        port: Redis port
        password: Redis password
        username: Redis username (Redis 6.0+ ACL)
        db: Redis database number
        sentinel_hosts: List of (host, port) tuples for Sentinel nodes
        master_name: Sentinel master name
        decode_responses: Whether to decode byte responses
        socket_keepalive: Enable TCP keepalive
        socket_timeout: Socket timeout in seconds
        health_check_interval: Health check interval in seconds
        max_connections: Max pool connections (None = default)
        socket_connect_timeout: Connect timeout (None = use socket_timeout)

    Returns:
        redis.asyncio.Redis client (either direct or via Sentinel)
    """
    import redis.asyncio as aioredis

    if sentinel_hosts and master_name:
        from redis.asyncio.sentinel import Sentinel as AsyncSentinel

        sentinel_kwargs: Dict[str, Any] = {
            "socket_timeout": socket_timeout,
        }
        if password is not None:
            sentinel_kwargs["password"] = password
        sentinel = AsyncSentinel(sentinel_hosts, **sentinel_kwargs)
        master_kwargs: Dict[str, Any] = {
            "db": db,
            "socket_timeout": socket_timeout,
            "decode_responses": decode_responses,
            "retry_on_timeout": True,
            "health_check_interval": health_check_interval,
            "socket_keepalive": socket_keepalive,
        }
        if password is not None:
            master_kwargs["password"] = password
        if username is not None:
            master_kwargs["username"] = username
        client = sentinel.master_for(master_name, **master_kwargs)
        logger.info(
            "Created async Redis Sentinel client (master=%s, sentinels=%d)",
            master_name,
            len(sentinel_hosts),
        )
        return client

    kwargs: Dict[str, Any] = {
        "host": host,
        "port": port,
        "db": db,
        "decode_responses": decode_responses,
        "socket_keepalive": socket_keepalive,
        "socket_timeout": socket_timeout,
        "health_check_interval": health_check_interval,
    }
    if password is not None:
        kwargs["password"] = password
    if username is not None:
        kwargs["username"] = username
    if max_connections is not None:
        kwargs["max_connections"] = max_connections
    if socket_connect_timeout is not None:
        kwargs["socket_connect_timeout"] = socket_connect_timeout

    return aioredis.Redis(**kwargs)


@dataclass
class CameraConfig:
    """Configuration for a camera stream."""

    camera_id: str
    input_topic: str
    output_topic: str
    stream_config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True


@dataclass
class StreamMessage:
    """Raw message from stream."""

    camera_id: str
    message_key: str
    data: Any
    timestamp: datetime
    priority: int = 1
