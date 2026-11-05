"""The one TLS trust decision for every connection this package opens (plan item (l)). Stdlib only.

Why, the tiers and the shared-context rules: DESIGN.md (tls.py).
"""

from __future__ import annotations

import os
import ssl
import threading

from ..safe_warn.safe_warn import warn

#: OpenSSL's pair (tier 1): variable, load keyword, the built-in path's field on
#: ssl.get_default_verify_paths().
_OPENSSL_PAIR: tuple[tuple[str, str, str], ...] = (
    ("SSL_CERT_FILE", "cafile", "openssl_cafile"),
    ("SSL_CERT_DIR", "capath", "openssl_capath"),
)
#: Tier 2, highest first; the first usable one is ADDED to the defaults.
_EXTRA_BUNDLES: tuple[str, ...] = ("REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE")
_ENV_NAMES: tuple[str, ...] = tuple(name for name, _, _ in _OPENSSL_PAIR) + _EXTRA_BUNDLES

_lock = threading.Lock()
#: Env values -> the context built from them, newest last, at most CACHE_SLOTS (None: empty).
#: One entry per process, except the daemon host, where each session's run has its own.
_cached: dict[tuple[str | None, ...], ssl.SSLContext] | None = None
CACHE_SLOTS = 16
#: How long a caller waits for another's build of the same variables before it builds its own.
BUILD_WAIT_S = 30.0
#: Variables whose context a caller is building now; others with the same wait (`ssl_context`).
_building: dict[tuple[str | None, ...], threading.Event] = {}
#: (variable, value) pairs already warned about: a bad path costs ONE line per process.
_warned: set[tuple[str, str]] = set()

#: (variable, value, what is wrong with it), collected while building.
_Problem = tuple[str, str, str]


def _reset_lock_after_fork() -> None:
    # A fork mid-build (a DataLoader worker) would leave the child's lock held forever and its
    # first client hung. The cached context itself is safe to inherit.
    global _lock, _building
    _lock = threading.Lock()
    _building = {}  # its builders are the parent's threads: none runs here


if hasattr(os, "register_at_fork"):  # POSIX only
    os.register_at_fork(after_in_child=_reset_lock_after_fork)


def ssl_context(environ=None) -> ssl.SSLContext:
    """The shared verifying context: pass it as httpx ``verify=`` / urllib ``context=``.
    ``environ``: another process's variables (the Probe service relaying a training process's
    request, plan D10) instead of this one's.

    First usable wins: ``SSL_CERT_FILE``/``SSL_CERT_DIR`` (replace the defaults), else
    ``REQUESTS_CA_BUNDLE``/``CURL_CA_BUNDLE`` ADDED to the OS store plus certifi. Never
    raises; every branch verifies certificates and hostnames. One per set of those variables,
    never mutated (so no ``http2=``; tests/test_tls_trust.py): an edited bundle needs a restart.
    """
    global _cached
    env = os.environ if environ is None else environ
    key = tuple(env.get(name) or None for name in _ENV_NAMES)
    fresh: list[_Problem] = []
    pending: threading.Event | None = None
    # Registered and released in one try: an interrupt anywhere (a SIGINT, an
    # eval harness's alarm) never leaves the variables marked as being built.
    try:
        while True:
            with _lock:
                hit = (_cached or {}).get(key)
                if hit is not None:
                    return hit
                building = _building.get(key)
                if building is None:
                    pending = _building[key] = threading.Event()
                    break
            # Another caller is building these variables: use theirs. A hung one (a stuck mount)
            # costs a waiter BUILD_WAIT_S, then it builds its own; either context is right.
            if not building.wait(BUILD_WAIT_S):
                break
        # Built OUTSIDE the lock: in the daemon host, one run's path on a hung mount must not
        # stall every other run's next client.
        problems: list[_Problem] = []
        context = _build(problems) if environ is None else _build(problems, env)
        with _lock:
            cache = dict(_cached or {})
            cache.pop(key, None)
            cache[key] = context
            while len(cache) > CACHE_SLOTS:
                cache.pop(next(iter(cache)))
            _cached = cache
            for name, value, problem in problems:
                if (name, value) not in _warned:
                    _warned.add((name, value))
                    fresh.append((name, value, problem))
    finally:
        if pending is not None:
            try:
                pending.set()
            finally:
                with _lock:
                    if _building.get(key) is pending:
                        del _building[key]
    # Emitted OUTSIDE the lock: a warnings hook (a logging handler, a harness's
    # showwarning) that builds a client of its own would otherwise deadlock on it.
    for name, value, problem in fresh:
        warn(
            f"probe: {name}={value!r} {problem}; ignoring it for TLS verification. "
            "Restart the process after fixing it: the certificates are read once."
        )
    return context


def _build(problems: list[_Problem], env=None) -> ssl.SSLContext:
    env = os.environ if env is None else env
    try:
        context = _load_openssl_pair(problems, env)
        if context is not None:
            return context
        context = _defaults()
        for name in _EXTRA_BUNDLES:
            if _add(context, name, problems, env):
                break
        return context
    except Exception:  # noqa: BLE001 -- trust setup may never crash a caller
        # Still verifying: an empty store refuses every handshake (fails closed), the right
        # failure for a broken OpenSSL.
        return ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


def _load_openssl_pair(problems: list[_Problem], env=None) -> ssl.SSLContext | None:
    """Tier 1, or None when neither variable names anything usable.

    Mirrors ``set_default_verify_paths``: each half comes from its variable
    when set, else from OpenSSL's built-in path for that half. A set-but-broken
    half also takes the built-in path, with a warning.
    """
    env = os.environ if env is None else env
    defaults = ssl.get_default_verify_paths()
    context: ssl.SSLContext | None = None
    has_used_variable = False
    for name, keyword, builtin_field in _OPENSSL_PAIR:
        value = env.get(name)
        where = _get_usable(name, value, problems) if value else None
        if where is not None:
            try:
                context = _load(context, where)
                has_used_variable = True
                continue
            except (OSError, ValueError) as exc:  # ssl.SSLError is an OSError
                problems.append((name, value or "", _describe_no_certificate(exc)))
        builtin = getattr(defaults, builtin_field, None)
        if builtin and os.path.exists(builtin):
            try:
                context = _load(context, {keyword: builtin})
            except (OSError, ValueError):
                pass  # the platform's own path is unreadable: nothing to add
    return context if has_used_variable else None


def _add(context: ssl.SSLContext, name: str, problems: list[_Problem], env=None) -> bool:
    """Load ``name``'s bundle into ``context``; True when it held a certificate."""
    value = (os.environ if env is None else env).get(name)
    if not value:
        return False  # unset and empty are the same: `requests` treats "" as unset too
    where = _get_usable(name, value, problems)
    if where is None:
        return False
    try:
        context.load_verify_locations(**where)
        return True
    except (OSError, ValueError) as exc:
        problems.append((name, value, _describe_no_certificate(exc)))
        return False


def _load(context: ssl.SSLContext | None, where: dict[str, str]) -> ssl.SSLContext:
    if context is None:
        return ssl.create_default_context(**where)
    context.load_verify_locations(**where)
    return context


def _get_usable(name: str, value: str, problems: list[_Problem]) -> dict[str, str] | None:
    """``{"cafile": ...}`` or ``{"capath": ...}`` for a readable path, else None."""
    if os.path.isdir(value):
        return {"capath": value}
    if os.path.isfile(value) and os.access(value, os.R_OK):
        return {"cafile": value}
    # OpenSSL reads SSL_CERT_DIR as a separator-joined LIST of directories.
    if os.pathsep in value and any(os.path.isdir(p) for p in value.split(os.pathsep) if p):
        return {"capath": value}
    problems.append((name, value, "does not exist or cannot be read"))
    return None


def _describe_no_certificate(exc: BaseException) -> str:
    return f"holds no usable certificate ({type(exc).__name__})"


def _defaults() -> ssl.SSLContext:
    """The OS store plus certifi: every root either stack trusted before, together."""
    context = ssl.create_default_context()  # OS verify paths; Windows' system store too
    if os.environ.get("SSL_CERT_FILE") or os.environ.get("SSL_CERT_DIR"):
        # Set but unusable (else tier 1 won), and OpenSSL's default loader reads them in place of
        # its built-in paths: load those by name so a typo'd variable cannot empty the OS store.
        paths = ssl.get_default_verify_paths()
        for keyword, path in (("cafile", paths.openssl_cafile), ("capath", paths.openssl_capath)):
            if path and os.path.exists(path):
                try:
                    context.load_verify_locations(**{keyword: path})
                except (OSError, ValueError):
                    pass
    try:
        import certifi

        context.load_verify_locations(cafile=certifi.where())
    except Exception:  # noqa: BLE001 -- certifi absent or its bundle unreadable
        pass
    return context
