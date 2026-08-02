"""In-memory TTL cache for read-mostly backend config reads.

Several backend GET calls return near-static, scoped config (agent definition,
org default LLM headers, streaming spec, DB connection string, KB details) yet
are re-fetched many times within a single process — once per ``build_agent_args``
(so once per task, plus once per plan-retry and once per sub-agent trigger). This
module provides a tiny, dependency-free TTL cache to coalesce those reads.

Design notes:
- **Lock-free.** ``run_sync`` may execute coroutines in different/new event
  loops (it spins a fresh loop or a worker thread under uvloop), so an
  ``asyncio.Lock`` would be bound to the wrong loop. A rare duplicate fetch on
  a cold key is harmless for 60s config reads, so we skip locking entirely;
  plain dict reads/writes are atomic under the GIL.
- **Scoped keys.** Keys must include a per-tenant scope token
  (``scope_token``) so a multi-tenant process never serves one org's config to
  another. Secrets (api_key) are folded into a short hash, never stored raw.
- **No env vars** for the TTL — module constant per the repo convention.
"""

import hashlib
import time
from collections import OrderedDict
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple
from weakref import WeakKeyDictionary

# Lifetime for cached backend config reads. Short enough that a long-running
# server picks up config changes within a minute; long enough to coalesce the
# repeated reads a single task run makes.
DEFAULT_CONFIG_CACHE_TTL = 60.0


def scope_token(configuration: Any) -> str:
    """Stable per-tenant token from a Configuration (base_url + org + api_key).

    Folds the api_key into a short md5 hash so the secret is never embedded
    verbatim in a cache key. Tolerates missing attributes (returns a token over
    whatever is present)."""
    parts = [
        str(getattr(configuration, "base_url", "") or ""),
        str(getattr(configuration, "organization_id", "") or ""),
        str(getattr(configuration, "api_key", "") or ""),
    ]
    # sha256 (not md5/sha1): only a non-security cache-key digest, but a strong
    # algo keeps CodeQL's weak-sensitive-data-hashing gate green since the api_key
    # is folded in. Truncated — collisions are irrelevant for a cache key.
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:12]


class TTLCache:
    """Minimal async TTL cache. ``get_or_fetch`` returns a cached value while
    fresh, else awaits ``factory`` and stores the result. Exceptions from
    ``factory`` propagate and are NOT cached."""

    def __init__(self, ttl_seconds: float = DEFAULT_CONFIG_CACHE_TTL):
        """Create a cache whose entries expire ``ttl_seconds`` after they are
        written."""
        self._ttl = ttl_seconds
        self._store: Dict[str, Tuple[Any, float]] = {}

    async def get_or_fetch(
        self, key: str, factory: Callable[[], Awaitable[Any]]
    ) -> Any:
        """Return the cached value for ``key`` while fresh; otherwise await
        ``factory()``, store its result with a fresh TTL, and return it.
        Exceptions raised by ``factory`` propagate and are not cached."""
        now = time.monotonic()
        hit = self._store.get(key)
        if hit is not None and hit[1] > now:
            return hit[0]
        value = await factory()
        self._store[key] = (value, time.monotonic() + self._ttl)
        return value

    def invalidate(self, key: Optional[str] = None) -> None:
        """Drop one key, or the whole cache when ``key`` is None."""
        if key is None:
            self._store.clear()
        else:
            self._store.pop(key, None)


# Process-wide cache for backend config reads (60s TTL).
backend_config_cache = TTLCache()


# Cap on distinct tool schemas memoized per process. Bounded so a multi-tenant,
# horizontally-scaled pod that sees many tools keeps flat memory (oldest evicts).
SCHEMA_CACHE_MAXSIZE = 2048

# Staleness backstop. The key is a content fingerprint (schema inputs incl.
# schema_overrides), so a real schema change is a new key and is picked up
# immediately — this TTL only bounds staleness if some output-affecting input were
# ever missed from the fingerprint. 10 min.
SCHEMA_CACHE_TTL_SECONDS = 600

_MISSING = object()


class BoundedCache:
    """Process-wide bounded LRU for pure derived values. The value is a
    deterministic function of the key (a content fingerprint), so a changed input
    is a different key; an optional ``ttl_seconds`` adds a staleness backstop.
    Evicts the least-recently-used entry past ``maxsize``.

    Lock-free like ``TTLCache``: dict ops are atomic under the GIL and a rare
    duplicate build on a cold/expired key is harmless."""

    def __init__(self, maxsize: int, ttl_seconds: Optional[float] = None):
        # key -> (value, expiry_monotonic | None)
        self._store: "OrderedDict[str, Tuple[Any, Optional[float]]]" = OrderedDict()
        self._max = maxsize
        self._ttl = ttl_seconds

    def get_or_build(self, key: str, factory: Callable[[], Any]) -> Any:
        """Return the cached value for ``key`` while fresh; else build it, store
        (with a fresh TTL if configured), and evict the oldest entry past ``maxsize``."""
        now = time.monotonic()
        hit = self._store.get(key, _MISSING)
        if hit is not _MISSING:
            value, expiry = hit
            if expiry is None or expiry > now:
                self._store.move_to_end(key)
                return value
            del self._store[key]  # expired -> rebuild below
        value = factory()
        expiry = None if self._ttl is None else now + self._ttl
        self._store[key] = (value, expiry)
        self._store.move_to_end(key)
        if len(self._store) > self._max:
            self._store.popitem(last=False)
        return value

    def __len__(self) -> int:
        return len(self._store)

    def clear(self) -> None:
        self._store.clear()


# Tool payload-schema class cache, keyed by a content fingerprint of the tool's
# schema inputs (id + parameters + overrides + is_local). The cached value is the
# generated pydantic class — a pure function of those inputs, carrying no
# tenant/config/task state — so a shared entry is safe across tenants by
# construction. See Tool.schema.
tool_schema_cache = BoundedCache(SCHEMA_CACHE_MAXSIZE, ttl_seconds=SCHEMA_CACHE_TTL_SECONDS)

# JSON-schema-per-mode for a given (already-cached) schema class. Keyed weakly by
# the class so entries drop when the class is evicted from tool_schema_cache.
_tool_json_schema_cache: "WeakKeyDictionary[Any, Dict[str, Any]]" = WeakKeyDictionary()


def cached_tool_json_schema(schema_cls: Any, mode: str) -> Dict[str, Any]:
    """Return ``schema_cls.model_json_schema(mode=mode)``, memoized per (class, mode).

    Only safe because ``schema_cls`` is itself a cached, stable object (from
    ``tool_schema_cache``); do not call with freshly-built classes."""
    by_mode = _tool_json_schema_cache.get(schema_cls)
    if by_mode is None:
        by_mode = {}
        _tool_json_schema_cache[schema_cls] = by_mode
    cached = by_mode.get(mode)
    if cached is None:
        cached = schema_cls.model_json_schema(mode=mode)
        by_mode[mode] = cached
    return cached
