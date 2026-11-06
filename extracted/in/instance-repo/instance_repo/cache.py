"""cache.py — 线程安全 TTL 缓存（复用 STS 凭据与 oss2 Bucket）。

按 key 缓存 value + 过期 epoch；命中要求 now < expiry - safety。expiry=None 视为不过期。
STS 凭据按 (resource,bucket,prefix)/(acr,host) 缓存、按签发返回的 Expiration 失效；
oss2 Bucket 按 (bucket,prefix,security_token) 缓存以复用底层连接池。
"""
from __future__ import annotations

import hashlib
import threading
import time
from datetime import datetime, timezone
from typing import Any


def parse_expiry(rfc3339: str | None) -> float | None:
    """RFC3339（如 ``2026-08-06T16:32:26Z``）→ epoch 秒；空/不可解析返回 None。

    无时区信息（naive）的字符串按 UTC 解释，避免被本地时区偏移影响过期判断。
    """
    if not rfc3339:
        return None
    s = rfc3339.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


_identity_lock = threading.Lock()


def transport_cache_identity(transport):
    """Opaque per-instance token: no credentials or recyclable object addresses."""
    with _identity_lock:
        token = getattr(transport, "_config_cache_identity", None)
        if token is None:
            token = object()
            try:
                setattr(transport, "_config_cache_identity", token)
            except (AttributeError, TypeError):
                pass  # Immutable adapters safely disable reuse instead of sharing.
        subject = getattr(transport, "token", "")
        digest = hashlib.sha256(subject.encode("utf-8", "surrogatepass")).digest() if isinstance(subject, str) else b""
        return token, digest


class TTLCache:
    """线程安全 TTL 缓存。"""

    def __init__(self, *, safety: float = 60.0, max_entries: int | None = None) -> None:
        self._d: dict[Any, tuple[Any, float | None]] = {}
        self._lock = threading.Lock()
        self._safety = safety
        if max_entries is not None and (isinstance(max_entries, bool)
                                        or not isinstance(max_entries, int)
                                        or max_entries < 1):
            raise ValueError("max_entries must be a positive integer")
        self._max_entries = max_entries

    def get(self, key: Any) -> Any | None:
        with self._lock:
            item = self._d.get(key)
            if item is None:
                return None
            value, exp = item
            if exp is not None and time.time() >= exp - self._safety:
                self._d.pop(key, None)
                return None
            return value

    def put(self, key: Any, value: Any, expiry: float | None) -> None:
        with self._lock:
            if self._max_entries is not None:
                now = time.time()
                for stale, (_, exp) in list(self._d.items()):
                    if exp is not None and now >= exp - self._safety:
                        self._d.pop(stale, None)
                if key not in self._d and len(self._d) >= self._max_entries:
                    self._d.pop(next(iter(self._d)))
            self._d[key] = (value, expiry)

    def clear(self) -> None:
        with self._lock:
            self._d.clear()
