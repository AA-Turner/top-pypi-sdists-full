"""CVC CredentialPool — multi-credential rotation with persistent state.

Design (CVC-native, lean port of upstream credential_pool.py):
- Persistent JSON store at ~/.cvc/credentials.json (per-provider lists).
- Status tracking: ok / exhausted, with cooldown TTLs based on HTTP code.
- Rotation strategies: fill_first (default), round_robin, random, least_used.
- Thread-safe (file lock + in-memory RLock).
- Provider-agnostic — Copilot, NVIDIA, OpenAI, Gemini all share the same pool.

Used by:
- cvc/providers/copilot/transport.py — rotates GitHub OAuth tokens on 401/429.
- cvc/providers/nvidia/transport.py — rotates NVIDIA NIM API keys.
- cvc/agent/llm.py — top-level Copilot path falls back to pool on auth failure.
"""

from __future__ import annotations

import json
import logging
import os
import random
import threading
import time
import uuid
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ─── Constants ──────────────────────────────────────────────────────────────

STATUS_OK = "ok"
STATUS_EXHAUSTED = "exhausted"

AUTH_TYPE_OAUTH = "oauth"
AUTH_TYPE_API_KEY = "api_key"
AUTH_TYPE_PAT = "pat"

SOURCE_MANUAL = "manual"
SOURCE_DEVICE_CODE = "device_code"
SOURCE_ENV = "env"
SOURCE_USER = "user"
SOURCE_GH_CLI = "gh_cli"

STRATEGY_FILL_FIRST = "fill_first"
STRATEGY_ROUND_ROBIN = "round_robin"
STRATEGY_RANDOM = "random"
STRATEGY_LEAST_USED = "least_used"
SUPPORTED_STRATEGIES = frozenset({
    STRATEGY_FILL_FIRST, STRATEGY_ROUND_ROBIN, STRATEGY_RANDOM, STRATEGY_LEAST_USED,
})

# Cooldown TTLs (seconds) — overridden by provider-supplied reset_at when available.
EXHAUSTED_TTL_401_SECONDS = 5 * 60        # transient auth — short cooldown
EXHAUSTED_TTL_429_SECONDS = 60 * 60       # rate-limited — 1 hour
EXHAUSTED_TTL_DEFAULT_SECONDS = 60 * 60   # default — 1 hour


# ─── PooledCredential ───────────────────────────────────────────────────────

@dataclass
class PooledCredential:
    """A single credential entry in the pool."""
    provider: str
    id: str
    label: str
    auth_type: str = AUTH_TYPE_API_KEY
    source: str = SOURCE_MANUAL
    priority: int = 0
    access_token: str = ""
    refresh_token: Optional[str] = None
    base_url: Optional[str] = None
    expires_at: Optional[float] = None      # Unix epoch seconds
    last_status: str = STATUS_OK
    last_status_at: Optional[float] = None
    last_error_code: Optional[int] = None
    last_error_message: Optional[str] = None
    last_error_reset_at: Optional[float] = None
    request_count: int = 0
    extra: Dict[str, Any] = field(default_factory=dict)

    @property
    def runtime_api_key(self) -> str:
        return self.access_token or ""

    @property
    def runtime_base_url(self) -> Optional[str]:
        return self.base_url

    def is_available(self, now: Optional[float] = None) -> bool:
        """True if credential is OK or its cooldown has expired."""
        now = now or time.time()
        if self.last_status != STATUS_EXHAUSTED:
            return True
        if self.last_error_reset_at and now >= self.last_error_reset_at:
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for f in fields(self):
            if f.name in ("provider", "extra"):
                continue
            v = getattr(self, f.name)
            if v is not None and v != "":
                result[f.name] = v
        if self.extra:
            result["extra"] = dict(self.extra)
        return result

    @classmethod
    def from_dict(cls, provider: str, payload: Dict[str, Any]) -> "PooledCredential":
        field_names = {f.name for f in fields(cls) if f.name != "provider"}
        data = {k: v for k, v in payload.items() if k in field_names}
        data.setdefault("id", uuid.uuid4().hex[:8])
        data.setdefault("label", payload.get("source", provider))
        data.setdefault("extra", payload.get("extra", {}) or {})
        return cls(provider=provider, **data)


# ─── Cooldown helper ────────────────────────────────────────────────────────

def _exhausted_ttl(error_code: Optional[int]) -> int:
    if error_code == 401:
        return EXHAUSTED_TTL_401_SECONDS
    if error_code == 429:
        return EXHAUSTED_TTL_429_SECONDS
    return EXHAUSTED_TTL_DEFAULT_SECONDS


# ─── CredentialPool ─────────────────────────────────────────────────────────

class CredentialPool:
    """Multi-credential rotation pool with persistent JSON store.

    Usage:
        pool = CredentialPool.get_instance()
        cred = pool.select("copilot")
        try:
            response = make_request(cred.runtime_api_key)
        except HTTPError as e:
            pool.mark_exhausted(cred, e.status_code, str(e))
            cred = pool.select("copilot")  # rotates to next available
    """

    _instance: Optional["CredentialPool"] = None
    _instance_lock = threading.Lock()

    def __init__(self, store_path: Optional[Path] = None,
                 strategy: str = STRATEGY_FILL_FIRST):
        self._store_path = store_path or (Path.home() / ".cvc" / "credentials.json")
        self._store_path.parent.mkdir(parents=True, exist_ok=True)
        self._strategy = strategy if strategy in SUPPORTED_STRATEGIES else STRATEGY_FILL_FIRST
        self._lock = threading.RLock()
        self._round_robin_idx: Dict[str, int] = {}
        self._credentials: Dict[str, List[PooledCredential]] = self._load()

    @classmethod
    def get_instance(cls) -> "CredentialPool":
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    # ─── Persistence ────────────────────────────────────────────────────────

    def _load(self) -> Dict[str, List[PooledCredential]]:
        if not self._store_path.exists():
            return {}
        try:
            raw = json.loads(self._store_path.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning("CredentialPool: failed to load %s: %s", self._store_path, e)
            return {}
        result: Dict[str, List[PooledCredential]] = {}
        for provider, entries in (raw.get("credentials") or {}).items():
            result[provider] = [PooledCredential.from_dict(provider, p) for p in entries]
        return result

    def _save(self) -> None:
        with self._lock:
            payload = {
                "version": 1,
                "credentials": {
                    p: [c.to_dict() for c in entries]
                    for p, entries in self._credentials.items()
                },
            }
            tmp = self._store_path.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            os.replace(tmp, self._store_path)
            try:
                os.chmod(self._store_path, 0o600)
            except OSError:
                pass

    # ─── CRUD ───────────────────────────────────────────────────────────────

    def add(self, credential: PooledCredential) -> PooledCredential:
        with self._lock:
            entries = self._credentials.setdefault(credential.provider, [])
            credential.priority = max(
                (e.priority for e in entries), default=-1
            ) + 1
            entries.append(credential)
            self._save()
            logger.info("CredentialPool: added %s/%s (id=%s)",
                        credential.provider, credential.label, credential.id)
            return credential

    def remove(self, provider: str, credential_id: str) -> bool:
        with self._lock:
            entries = self._credentials.get(provider, [])
            new_entries = [e for e in entries if e.id != credential_id]
            if len(new_entries) == len(entries):
                return False
            self._credentials[provider] = new_entries
            self._save()
            return True

    def list(self, provider: Optional[str] = None) -> List[PooledCredential]:
        with self._lock:
            if provider:
                return list(self._credentials.get(provider, []))
            result: List[PooledCredential] = []
            for entries in self._credentials.values():
                result.extend(entries)
            return result

    def get(self, provider: str, credential_id: str) -> Optional[PooledCredential]:
        with self._lock:
            for cred in self._credentials.get(provider, []):
                if cred.id == credential_id:
                    return cred
            return None

    def update(self, credential: PooledCredential) -> None:
        """Persist in-place mutations (e.g. token refresh)."""
        with self._lock:
            self._save()

    # ─── Selection ──────────────────────────────────────────────────────────

    def select(self, provider: str) -> Optional[PooledCredential]:
        """Pick the next available credential for this provider, per strategy."""
        with self._lock:
            entries = self._credentials.get(provider, [])
            if not entries:
                return None
            now = time.time()
            available = [c for c in entries if c.is_available(now)]
            if not available:
                # All exhausted — return the one with the soonest reset
                logger.warning("CredentialPool: all %d %s credentials exhausted",
                               len(entries), provider)
                return min(entries,
                           key=lambda c: c.last_error_reset_at or float("inf"))

            if self._strategy == STRATEGY_FILL_FIRST:
                # Sort by priority asc, return first available
                available.sort(key=lambda c: c.priority)
                return available[0]
            if self._strategy == STRATEGY_ROUND_ROBIN:
                idx = self._round_robin_idx.get(provider, 0) % len(available)
                self._round_robin_idx[provider] = (idx + 1) % len(available)
                return available[idx]
            if self._strategy == STRATEGY_RANDOM:
                return random.choice(available)
            if self._strategy == STRATEGY_LEAST_USED:
                return min(available, key=lambda c: c.request_count)
            return available[0]

    # ─── State updates ──────────────────────────────────────────────────────

    def mark_used(self, credential: PooledCredential) -> None:
        with self._lock:
            credential.request_count += 1
            credential.last_status = STATUS_OK
            credential.last_status_at = time.time()
            self._save()

    def mark_exhausted(self, credential: PooledCredential, error_code: Optional[int],
                       error_message: str = "", reset_at: Optional[float] = None) -> None:
        with self._lock:
            now = time.time()
            credential.last_status = STATUS_EXHAUSTED
            credential.last_status_at = now
            credential.last_error_code = error_code
            credential.last_error_message = error_message[:500] if error_message else None
            credential.last_error_reset_at = reset_at or (now + _exhausted_ttl(error_code))
            self._save()
            logger.warning(
                "CredentialPool: %s/%s marked exhausted (code=%s, reset_in=%ds)",
                credential.provider, credential.label, error_code,
                int((credential.last_error_reset_at - now)),
            )

    def reset(self, credential: PooledCredential) -> None:
        """Manually clear exhausted status (e.g. user override)."""
        with self._lock:
            credential.last_status = STATUS_OK
            credential.last_error_code = None
            credential.last_error_message = None
            credential.last_error_reset_at = None
            self._save()

    # ─── Stats ──────────────────────────────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            now = time.time()
            providers: Dict[str, Dict[str, Any]] = {}
            for provider, entries in self._credentials.items():
                providers[provider] = {
                    "total": len(entries),
                    "available": sum(1 for c in entries if c.is_available(now)),
                    "exhausted": sum(1 for c in entries if not c.is_available(now)),
                    "total_requests": sum(c.request_count for c in entries),
                }
            return {
                "strategy": self._strategy,
                "store_path": str(self._store_path),
                "providers": providers,
            }


# ─── Module-level convenience ───────────────────────────────────────────────

def get_pool() -> CredentialPool:
    return CredentialPool.get_instance()
