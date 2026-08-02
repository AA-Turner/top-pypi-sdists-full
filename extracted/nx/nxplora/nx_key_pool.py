import os
import re
import time
import threading
import hashlib
from dataclasses import dataclass, field
from typing import Optional

from nx_obfuscate import ENV

# Keychain service-name allowlist. All names come from the obfuscated ENV
# table today (trusted), but we validate before handing them to the `security`
# subprocess so that if any of these ever become env/user-configurable, a
# hostile value can't inject shell metacharacters or extra arguments.
_KEYCHAIN_NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")


def _safe_keychain_name(name: str) -> bool:
    return bool(name) and bool(_KEYCHAIN_NAME_RE.match(name))


def _kc_read(service: str):
    """Read one pooled secret under account 'nx'. macOS uses the native Keychain
    (`security`); every other platform (Windows / Linux) uses keyring via nx_keystore.
    Name-validated before it touches the OS. Returns the value or None."""
    if not _safe_keychain_name(service):
        return None
    import sys
    if sys.platform != "darwin":
        try:
            from nx_keystore import kr_get
            return kr_get("nx", service)
        except Exception:
            return None
    try:
        import subprocess
        r = subprocess.run(
            ["security", "find-generic-password", "-a", "nx", "-s", service, "-w"],
            capture_output=True, text=True, timeout=3,
        )
        if r.returncode == 0 and (r.stdout or "").strip():
            return r.stdout.strip()
    except Exception:
        pass
    return None


@dataclass
class KeySlot:
    index: int
    key: str
    requests_this_minute: int = 0
    last_reset: float = field(default_factory=time.time)
    failures: int = 0
    locked_until: float = 0.0

    def is_available(self) -> bool:
        now = time.time()
        if now < self.locked_until:
            return False
        if now - self.last_reset > 60:
            self.requests_this_minute = 0
            self.last_reset = now
        return self.requests_this_minute < 50

    def record_use(self):
        self.requests_this_minute += 1
        self.failures = 0

    def record_failure(self):
        self.failures += 1
        if self.failures >= 3:
            self.locked_until = time.time() + 60


class NvidiaKeyPool:
    def __init__(self):
        self._lock = threading.Lock()
        self._slots = self._load_keys()
        self._user_assignments: dict[str, int] = {}

    def _load_keys(self) -> list[KeySlot]:
        keys = []
        # Prefer process env when available.
        for i in range(1, 7):
            key = os.environ.get(f"{ENV['nvidia_key_env']}{i}", "")
            if key:
                keys.append(KeySlot(index=i - 1, key=key))
        if keys:
            return keys

        # Fall back to Keychain without surfacing errors to the CLI.
        for i in range(1, 7):
            svc = f"{ENV['keychain_prefix']}{i}"
            if not _safe_keychain_name(svc):
                continue
            _v = _kc_read(svc)
            if _v:
                keys.append(KeySlot(index=i - 1, key=_v))

        return keys

    def _user_base_slot(self, user_id: str) -> int:
        return int(hashlib.md5(user_id.encode()).hexdigest(), 16) % len(self._slots)

    def get_key(self, user_id: str) -> tuple[str, int]:
        if not self._slots:
            return "", -1
        with self._lock:
            base = self._user_base_slot(user_id)
            for i in range(len(self._slots)):
                slot = self._slots[(base + i) % len(self._slots)]
                if slot.is_available():
                    slot.record_use()
                    return slot.key, slot.index
            # All slots rate-limited. Prefer the least-loaded UNLOCKED slot.
            # Falling back to a locked slot (failures>=3) just amplifies
            # backpressure on whichever key actually failed last.
            now = time.time()
            unlocked = [s for s in self._slots if now >= s.locked_until]
            pool = unlocked if unlocked else self._slots
            slot = min(pool, key=lambda s: s.requests_this_minute)
            slot.record_use()
            return slot.key, slot.index

    def record_failure(self, slot_index: int):
        if slot_index < 0:
            return
        with self._lock:
            self._slots[slot_index].record_failure()

    def all_locked(self) -> bool:
        """True if every slot is either locked or has hit the per-minute cap."""
        if not self._slots:
            return True
        with self._lock:
            return not any(s.is_available() for s in self._slots)

    def iter_slots(self) -> list:
        """Return a lock-held snapshot of (index, key) for slots with a key.
        Pool consumers should use this instead of touching ._slots directly,
        so iteration is always consistent under concurrent mutation."""
        with self._lock:
            return [(s.index, s.key) for s in self._slots if s.key]

    def status(self) -> list[dict]:
        with self._lock:
            return [
                {
                    "slot": s.index + 1,
                    "requests_this_minute": s.requests_this_minute,
                    "failures": s.failures,
                    "locked": time.time() < s.locked_until,
                }
                for s in self._slots
            ]


_pool: Optional[NvidiaKeyPool] = None


def get_pool() -> NvidiaKeyPool:
    global _pool
    if _pool is None:
        try:
            _pool = NvidiaKeyPool()
        except Exception:
            _pool = NvidiaKeyPool.__new__(NvidiaKeyPool)
            _pool._slots = []
            _pool._lock = threading.Lock()
            _pool._user_assignments = {}
    return _pool


# ─── Secondary provider (single-key, no pool) ───────────────────────────────
#
# The secondary provider was promoted to primary as of 0.3.95. Unlike the
# legacy pooled provider's 6-key pool, this one runs on a single account/key,
# so there's no slot rotation. Server-side rate limits handle backpressure;
# we just hand the key over.
#
# Priority order, matches the pooled key loader's discipline:
#   1. process env var (name resolved from the ENV table — secondary provider
#      API-key env var)
#   2. macOS Keychain — service name resolved from the ENV table (secondary
#      provider keychain name); never a string literal here — the obfuscation
#      guard enforces this
#
# Returns the literal key string, or "" on miss. slot_index for routing is -1
# to signal "bypass pool accounting" — the routing layer reads this to skip
# the pool's record_failure() calls.

_deepinfra_key_cache: Optional[str] = None
_deepinfra_key_loaded: bool = False


def get_deepinfra_key() -> str:
    """Resolve the secondary provider single key. Cached after first successful load."""
    global _deepinfra_key_cache, _deepinfra_key_loaded
    if _deepinfra_key_loaded:
        return _deepinfra_key_cache or ""

    env_key = os.environ.get(ENV["fallback_api_key"], "").strip()
    if env_key:
        _deepinfra_key_cache = env_key
        _deepinfra_key_loaded = True
        return env_key

    # Fall back to the secret store (macOS Keychain / else keyring), via _kc_read.
    _v = _kc_read(ENV["deepinfra_keychain"])
    if _v:
        _deepinfra_key_cache = _v
        _deepinfra_key_loaded = True
        return _deepinfra_key_cache

    _deepinfra_key_cache = ""
    _deepinfra_key_loaded = True
    return ""


def reset_deepinfra_key_cache() -> None:
    """Test-only: clear the cache so tests can mutate env / Keychain mid-run."""
    global _deepinfra_key_cache, _deepinfra_key_loaded
    _deepinfra_key_cache = None
    _deepinfra_key_loaded = False


# ─── Primary provider (single-key, no pool) ─────────────────────────────────
#
# The primary provider as of 0.3.96. Single key — the provider handles rate
# limiting server-side; no pool rotation needed.
#
# Priority order:
#   1. process env var (name resolved from the ENV table — primary provider
#      API-key env var)
#   2. macOS Keychain — service name resolved from the ENV table (primary
#      provider keychain name); never a string literal here — obfuscation
#      guard enforces this

_fireworks_key_cache: Optional[str] = None
_fireworks_key_loaded: bool = False


def get_fireworks_key() -> str:
    """Resolve the primary provider single key. Cached after first successful load."""
    global _fireworks_key_cache, _fireworks_key_loaded
    if _fireworks_key_loaded:
        return _fireworks_key_cache or ""

    env_key = os.environ.get(ENV["fireworks_api_key"], "").strip()
    if env_key:
        _fireworks_key_cache = env_key
        _fireworks_key_loaded = True
        return env_key

    _v = _kc_read(ENV["fireworks_keychain"])
    if _v:
        _fireworks_key_cache = _v
        _fireworks_key_loaded = True
        return _fireworks_key_cache

    _fireworks_key_cache = ""
    _fireworks_key_loaded = True
    return ""


def reset_fireworks_key_cache() -> None:
    """Test-only: clear the cache so tests can mutate env / Keychain mid-run."""
    global _fireworks_key_cache, _fireworks_key_loaded
    _fireworks_key_cache = None
    _fireworks_key_loaded = False
