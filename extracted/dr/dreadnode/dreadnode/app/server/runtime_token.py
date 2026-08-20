"""Resolve the runtime auth token from a rotatable source.

The token gating ``/api/*`` historically came solely from
``DREADNODE_RUNTIME_TOKEN`` in the process env, which is fixed for the life of
the process. To support lossless reconnect (the platform hands a browser a new
token and reconnects it to the *same* running sandbox instead of rebuilding
it), the platform rotates the token by writing a new value to a file named by
``DREADNODE_RUNTIME_TOKEN_FILE``.

This source reads that file so a rotation takes effect on the next request with
no restart, keeps the just-retired token valid for a short grace window (so a
client mid-handoff, or one racing a stale read cache, is not spuriously
rejected), and notifies a listener when a token is retired so live connections
authed with it can be dropped.

When no token file is configured it falls back to the env var, preserving the
prior behavior exactly — a deployment that never sets ``*_TOKEN_FILE`` behaves
identically to before this module existed.
"""

import os
import secrets
import threading
import time
import typing as t
from pathlib import Path

from loguru import logger

from dreadnode.app.env import read_env_with_deprecation

__all__ = [
    "RuntimeTokenSource",
    "get_token_source",
    "materialize_runtime_token_file",
    "read_runtime_token",
    "reset_token_source",
]

_TOKEN_FILE_ENV = "DREADNODE_RUNTIME_TOKEN_FILE"  # noqa: S105  (env var name, not a secret)
_GRACE_SECONDS_ENV = "DREADNODE_RUNTIME_TOKEN_GRACE_SECONDS"

# A just-retired token stays valid this long after a rotation. Long enough to
# cover a client's in-flight requests and a stale read cache during handoff;
# short enough that a kicked device loses REST access promptly. WebSocket
# connections are closed immediately on retire regardless of this window.
_DEFAULT_GRACE_SECONDS = 5.0

# The token file is re-read at most this often on the hot auth path. A presented
# token that misses the cache forces an immediate re-read (see ``is_valid``), so
# a freshly-rotated token is honored without waiting out the cache.
_DEFAULT_CACHE_TTL = 1.0


class _TokenUnavailableError(Exception):
    """The token file exists but could not be read. Callers must keep the last
    known token rather than fall back to the (retired) env token."""


def _read_env_token() -> str | None:
    # Deliberately NOT stripped: preserves the legacy semantics where any set
    # env value counts as "auth enabled". Only the file read is stripped (a
    # trailing newline is expected there); stripping the env value here would
    # let a whitespace-only token silently flip auth off (fail open).
    return read_env_with_deprecation("DREADNODE_RUNTIME_TOKEN", "SANDBOX_AUTH_TOKEN")


def read_runtime_token() -> str | None:
    """Resolve the current runtime token from the token file, else the env var.

    The single point that knows *where* the token lives, shared by the server's
    auth middleware and by out-of-process clients (subprocess workers) that call
    back into the runtime. Reading it fresh on each call is what lets a rotation
    reach a long-lived client without restarting it. Returns ``None`` when no
    token is configured (auth disabled).

    The env var is a *pre-materialization* fallback only: it holds the token the
    sandbox was provisioned with, which after a rotation is a RETIRED credential.
    So once the token file exists, a failure to read it must NOT fall back to the
    env — doing so would hand back the old token. Fail closed (``None``) instead.
    """
    path_str = os.environ.get(_TOKEN_FILE_ENV)
    if path_str:
        path = Path(path_str)
        try:
            return path.read_text(encoding="utf-8").strip() or None
        except FileNotFoundError:
            # Not materialized yet — the env token is still the live one.
            return _read_env_token()
        except OSError as exc:
            # The file exists but we can't read it. The env token may be stale
            # (retired by a rotation), so refusing is safer than resurrecting it.
            logger.warning("Failed to read runtime token file {}: {}", path_str, exc)
            return None
    return _read_env_token()


def _atomic_write(path: Path, content: str) -> None:
    """Write ``content`` to ``path`` so a concurrent reader never sees a partial
    file: write a sibling temp file, then rename it over the target (atomic on
    POSIX). The token file holds a secret, so it's created 0600."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.chmod(0o600)
    tmp.replace(path)  # atomic on POSIX


def materialize_runtime_token_file() -> None:
    """Write the current env token into ``DREADNODE_RUNTIME_TOKEN_FILE`` if that
    path is configured and the file doesn't already hold a token.

    Called once at server startup. The file's *existence* is the signal the
    platform uses to decide a sandbox can be reconnected (its token rotated in
    place) rather than restarted — so a rotation-aware runtime must create it.
    A no-op when the path is unset (local/dev) or already populated.
    """
    path_str = os.environ.get(_TOKEN_FILE_ENV)
    if not path_str:
        return
    path = Path(path_str)
    try:
        if path.exists() and path.read_text(encoding="utf-8").strip():
            return  # already materialized (e.g. by a prior boot or the platform)
    except OSError:
        pass  # unreadable — fall through and try to (re)write it
    token = _read_env_token()
    if not token or not token.strip():
        return  # nothing to materialize (auth disabled)
    try:
        _atomic_write(path, token.strip())
    except OSError as exc:
        logger.warning("Failed to materialize runtime token file {}: {}", path_str, exc)


def _read_grace_seconds() -> float:
    raw = os.environ.get(_GRACE_SECONDS_ENV)
    if raw is None:
        return _DEFAULT_GRACE_SECONDS
    try:
        value = float(raw)
    except ValueError:
        logger.warning(
            "Invalid {}={!r}; using default {}s", _GRACE_SECONDS_ENV, raw, _DEFAULT_GRACE_SECONDS
        )
        return _DEFAULT_GRACE_SECONDS
    return max(0.0, value)


class RuntimeTokenSource:
    """Thread-safe resolver for the current (and briefly, the just-retired) token.

    A single instance is shared process-wide via :func:`get_token_source`. The
    optional ``on_retire`` callback fires with the retired token whenever the
    current token changes (or is removed); it MUST be cheap and non-blocking —
    it runs under the internal lock, so it should only schedule work (e.g.
    ``loop.call_soon_threadsafe``), never perform it inline.
    """

    def __init__(
        self,
        *,
        grace_seconds: float | None = None,
        cache_ttl: float = _DEFAULT_CACHE_TTL,
        clock: t.Callable[[], float] = time.monotonic,
        on_retire: t.Callable[[str], None] | None = None,
    ) -> None:
        self._clock = clock
        self._cache_ttl = cache_ttl
        self._grace_seconds = _read_grace_seconds() if grace_seconds is None else grace_seconds
        self._on_retire = on_retire
        self._lock = threading.RLock()
        self._current: str | None = None
        self._grace: dict[str, float] = {}
        self._last_read: float | None = None
        # True once we've read a real token out of the token file. From then on
        # the env var is a retired relic and must never be fallen back to.
        self._file_backed = False

    def set_on_retire(self, on_retire: "t.Callable[[str], None] | None") -> None:
        """Install (or clear) the retire callback on the live source.

        Lets the server wire WebSocket teardown to token rotation after the
        singleton already exists, without discarding its cache/grace state.
        """
        with self._lock:
            self._on_retire = on_retire

    def _read_token(self) -> str | None:
        """Read the token from its authoritative source.

        Raises :class:`_TokenUnavailableError` when a token file we have previously
        read successfully becomes unreadable. That must NOT fall back to the env
        var: the env holds the token the sandbox was provisioned with, which a
        rotation has since retired. Falling back would make ``_refresh`` see the
        old token as the new current one — re-authorizing a retired credential
        and retiring the live one. Keeping the last known token (fail closed) is
        the only safe answer.
        """
        path_str = os.environ.get(_TOKEN_FILE_ENV)
        if not path_str:
            return _read_env_token()

        path = Path(path_str)
        try:
            value = path.read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            if self._file_backed:
                raise _TokenUnavailableError(f"{path_str} vanished") from None
            # Never materialized — the env token is still the live one.
            return _read_env_token()
        except OSError as exc:
            if self._file_backed:
                raise _TokenUnavailableError(f"{path_str}: {exc}") from exc
            logger.warning("Failed to read runtime token file {}: {}", path_str, exc)
            return _read_env_token()

        if value:
            # From here on the file is authoritative; the env is a stale relic.
            self._file_backed = True
        return value or None

    def _prune(self, now: float) -> None:
        expired = [token for token, expiry in self._grace.items() if expiry <= now]
        for token in expired:
            del self._grace[token]

    def _refresh(self, *, force: bool) -> str | None:
        """Refresh the cached token; return the token to retire on, if any.

        The retire callback is intentionally NOT fired here — it would run under
        the lock. Callers fire it after releasing the lock (see :meth:`enabled`
        / :meth:`is_valid`) to avoid a lock-ordering hazard with the callback's
        own locks.
        """
        now = self._clock()
        cache_fresh = self._last_read is not None and (now - self._last_read) < self._cache_ttl
        if not force and cache_fresh:
            self._prune(now)
            return None
        try:
            raw = self._read_token()
        except _TokenUnavailableError as exc:
            # The token file is unreadable. Keep the last known token — never
            # retire it, and never fall back to the (retired) env token.
            logger.warning("Runtime token file unreadable, keeping current token: {}", exc)
            self._last_read = now
            self._prune(now)
            return None

        self._last_read = now

        retired: str | None = None
        if raw is None and self._current is not None:
            # A real rotation always yields a NEW non-empty token, never None. A
            # None here is almost always a transient empty/partial read racing a
            # non-atomic write (or a vanished file), so keep the current token —
            # failing closed rather than retiring it and opening /api/*. (The
            # platform writer must still write atomically; a partial *non-empty*
            # read can't be distinguished here and is the writer's to prevent.)
            self._prune(now)
            return None
        if raw != self._current:
            retired = self._current
            self._current = raw
            if retired is not None:
                self._grace[retired] = now + self._grace_seconds
        self._prune(now)
        return retired

    def _fire_retire(self, retired: str | None) -> None:
        if retired is None:
            return
        callback = self._on_retire
        if callback is None:
            return
        try:
            callback(retired)
        except Exception:
            logger.exception("runtime token retire callback failed")

    def _matches(self, presented: str) -> bool:
        if self._matches_current(presented):
            return True
        return any(secrets.compare_digest(presented, token) for token in self._grace)

    def enabled(self) -> bool:
        """Whether auth is required (a token is configured from file or env).

        Returns ``False`` only when no token is set anywhere — matching the
        legacy "unset token disables auth" behavior. During a grace window auth
        stays enabled so token *removal* fails closed rather than open.
        """
        with self._lock:
            retired = self._refresh(force=False)
            result = self._current is not None or bool(self._grace)
        self._fire_retire(retired)
        return result

    def is_current(self, presented: str) -> bool:
        """Whether ``presented`` is the *current* token — not merely valid.

        The grace window lets a just-retired token keep REST working through a
        handoff, but a retired credential must not be able to establish a new
        long-lived connection (a WebSocket): the client holding it is the one
        that was just kicked. Connection setup checks currency; REST checks
        validity.

        Unlike :meth:`is_valid`, this always reconciles with the token file
        instead of trusting a fresh cache. A cache *hit* on a token the file has
        since replaced is exactly the dangerous case here: the read cache would
        vouch for a rotated-out token for up to ``cache_ttl``, which is long
        enough for the kicked client to open a socket that then outlives the
        rotation (the retire sweep has already run, or hasn't observed the
        rotation either). Handshakes are rare and the token file is tiny.
        """
        with self._lock:
            retired = self._refresh(force=True)
            matches = self._matches_current(presented)
        self._fire_retire(retired)
        return matches

    def _matches_current(self, presented: str) -> bool:
        return self._current is not None and secrets.compare_digest(presented, self._current)

    def is_valid(self, presented: str) -> bool:
        """Constant-time check of a presented token against current + grace set.

        On a cache miss the file is re-read once before rejecting, so a token the
        platform just wrote is accepted immediately rather than after the cache
        TTL elapses.
        """
        with self._lock:
            retired = self._refresh(force=False)
            if self._matches(presented):
                matches = True
            else:
                retired = self._refresh(force=True) or retired
                matches = self._matches(presented)
        self._fire_retire(retired)
        return matches


# Process-wide singleton. It lives here (rather than on ``ServerState``) so the
# auth middleware can reach it without importing ``app``, which would create an
# ``auth`` <-> ``app`` import cycle.
_source_lock = threading.Lock()
_source: RuntimeTokenSource | None = None


def get_token_source() -> RuntimeTokenSource:
    """Return the process-wide token source, constructing it on first use."""
    global _source  # noqa: PLW0603 - deliberate module-level singleton (see note above)
    with _source_lock:
        if _source is None:
            _source = RuntimeTokenSource()
        return _source


def reset_token_source(**kwargs: t.Any) -> RuntimeTokenSource:
    """Replace the process-wide token source (for tests and reconfiguration)."""
    global _source  # noqa: PLW0603 - deliberate module-level singleton (see note above)
    with _source_lock:
        _source = RuntimeTokenSource(**kwargs)
        return _source
