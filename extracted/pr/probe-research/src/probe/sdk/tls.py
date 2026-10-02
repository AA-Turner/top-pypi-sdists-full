"""The one TLS trust decision for every connection this package opens.

WHY THIS EXISTS. Before it, the agent trusted two different sets of roots
depending on which HTTP stack a request happened to use:

  - httpx (every SDK write, the CLI, the daemon, the hosted MCP) read
    ``SSL_CERT_FILE`` / ``SSL_CERT_DIR``, else certifi's bundle -- and nothing
    else. Never ``REQUESTS_CA_BUNDLE``, never ``CURL_CA_BUNDLE``, never the OS
    store.
  - urllib (client telemetry, capture checks, the version manifest, transcript
    upload) used the OS store and ignored every one of those variables.

Behind a TLS-re-signing corporate proxy that split is the worst kind of
partial outage: telemetry reaches the server and says the SDK is alive while
every SDK write fails certificate verification, and the one variable the
researcher already set for ``requests`` (``REQUESTS_CA_BUNDLE``) does nothing.

THE RULE (plan item (l)). The first of these that names something usable wins:

  1. ``SSL_CERT_FILE`` / ``SSL_CERT_DIR`` -- OpenSSL's own pair, and they
     REPLACE the defaults, exactly as ``set_default_verify_paths`` (and httpx)
     read them. A half of the pair that is unset keeps OpenSSL's built-in
     location for that half: ``SSL_CERT_FILE`` alone still searches the
     built-in certificate folder, ``SSL_CERT_DIR`` alone the built-in file.
  2. ``REQUESTS_CA_BUNDLE``, else ``CURL_CA_BUNDLE`` -- ADDED to tier 3,
     never instead of it.
  3. the OS default verify paths PLUS certifi's bundle.

Tier 2 deliberately deviates from decision D21 ("an explicit bundle
replaces"). Those two variables are usually set for ANOTHER tool: a bundle
holding one internal root, exported in a shell profile for ``requests``,
would otherwise make every Probe connection fail where the release before
this one connected fine. Adding can only ever make more servers verify, so a
bundle the user set for anything can never cost them Probe. The corporate
proxy case works either way: its root is in the bundle.

A bundle variable may name a file (``cafile``) or a hashed directory
(``capath``), as ``requests`` accepts. A variable naming something missing,
unreadable or holding no certificate is skipped with ONE warning per process;
this never raises. There is deliberately no switch that turns verification
off: a proxy the user trusts is handled by giving its CA, never by trusting
everyone.

STDLIB ONLY (plus certifi when it is importable, which it always is beside
httpx). The journal's enqueue path and the urllib callers must be able to use
this without importing an HTTP client.

ONE CONTEXT PER PROCESS, SHARED by every client. Nothing here may load
certificates into it, change its verify mode or its hostname check after it is
built. The one mutation it does see is httpcore setting the ALPN list on each
new connection; every client in the package is HTTP/1.1-only, so every such
call writes the same ``["http/1.1"]`` -- which is why no httpx client here may
pass ``http2=`` (tests/test_tls_trust.py guards both).

It is rebuilt only when one of the variables above changes. A bundle FILE that
is edited in place is not re-read: after fixing a bundle, restart the process.
"""

from __future__ import annotations

import os
import ssl
import threading

from .safe_warn import warn

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
#: (the env values it was built from, the context). One slot: the variables
#: change at most a handful of times in a process's life.
_cached: tuple[tuple[str | None, ...], ssl.SSLContext] | None = None
#: (variable, value) pairs already warned about, so a bad path costs ONE line
#: per process however many clients get built.
_warned: set[tuple[str, str]] = set()

#: (variable, value, what is wrong with it), collected while building.
_Problem = tuple[str, str, str]


def _reset_lock_after_fork() -> None:
    # A thread building the context at the moment of a fork (a DataLoader
    # worker, say) would leave the child's lock held forever, and the child's
    # first client would hang. The cached context itself is safe to inherit.
    global _lock
    _lock = threading.Lock()


if hasattr(os, "register_at_fork"):  # POSIX only
    os.register_at_fork(after_in_child=_reset_lock_after_fork)


def ssl_context() -> ssl.SSLContext:
    """The shared verifying context: pass it as httpx ``verify=`` / urllib ``context=``.

    Never raises. Every branch verifies certificates and hostnames.
    """
    global _cached
    key = tuple(os.environ.get(name) or None for name in _ENV_NAMES)
    fresh: list[_Problem] = []
    with _lock:
        if _cached is not None and _cached[0] == key:
            return _cached[1]
        problems: list[_Problem] = []
        context = _build(problems)
        _cached = (key, context)
        for name, value, problem in problems:
            if (name, value) not in _warned:
                _warned.add((name, value))
                fresh.append((name, value, problem))
    # Emitted OUTSIDE the lock: a warnings hook (a logging handler, a harness's
    # showwarning) that builds a client of its own would otherwise deadlock on it.
    for name, value, problem in fresh:
        warn(
            f"probe: {name}={value!r} {problem}; ignoring it for TLS verification. "
            "Restart the process after fixing it: the certificates are read once."
        )
    return context


def _build(problems: list[_Problem]) -> ssl.SSLContext:
    try:
        context = _openssl_pair(problems)
        if context is not None:
            return context
        context = _defaults()
        for name in _EXTRA_BUNDLES:
            if _add(context, name, problems):
                break
        return context
    except Exception:  # noqa: BLE001 -- trust setup may never crash a caller
        # Still verifying: an empty store fails closed (every handshake is
        # refused), which is the right failure for a broken OpenSSL, and far
        # better than the silent alternative of not checking at all.
        return ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


def _openssl_pair(problems: list[_Problem]) -> ssl.SSLContext | None:
    """Tier 1, or None when neither variable names anything usable.

    Mirrors ``set_default_verify_paths``: each half comes from its variable
    when set, else from OpenSSL's built-in path for that half. A set-but-broken
    half also takes the built-in path, with a warning.
    """
    defaults = ssl.get_default_verify_paths()
    context: ssl.SSLContext | None = None
    used_a_variable = False
    for name, keyword, builtin_field in _OPENSSL_PAIR:
        value = os.environ.get(name)
        where = _usable(name, value, problems) if value else None
        if where is not None:
            try:
                context = _load(context, where)
                used_a_variable = True
                continue
            except (OSError, ValueError) as exc:  # ssl.SSLError is an OSError
                problems.append((name, value or "", _no_certificate(exc)))
        builtin = getattr(defaults, builtin_field, None)
        if builtin and os.path.exists(builtin):
            try:
                context = _load(context, {keyword: builtin})
            except (OSError, ValueError):
                pass  # the platform's own path is unreadable: nothing to add
    return context if used_a_variable else None


def _add(context: ssl.SSLContext, name: str, problems: list[_Problem]) -> bool:
    """Load ``name``'s bundle into ``context``; True when it held a certificate."""
    value = os.environ.get(name)
    if not value:
        return False  # unset and empty are the same: `requests` treats "" as unset too
    where = _usable(name, value, problems)
    if where is None:
        return False
    try:
        context.load_verify_locations(**where)
        return True
    except (OSError, ValueError) as exc:
        problems.append((name, value, _no_certificate(exc)))
        return False


def _load(context: ssl.SSLContext | None, where: dict[str, str]) -> ssl.SSLContext:
    if context is None:
        return ssl.create_default_context(**where)
    context.load_verify_locations(**where)
    return context


def _usable(name: str, value: str, problems: list[_Problem]) -> dict[str, str] | None:
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


def _no_certificate(exc: BaseException) -> str:
    return f"holds no usable certificate ({type(exc).__name__})"


def _defaults() -> ssl.SSLContext:
    """The OS store plus certifi: every root either stack trusted before, together."""
    context = ssl.create_default_context()  # OS verify paths; Windows' system store too
    if os.environ.get("SSL_CERT_FILE") or os.environ.get("SSL_CERT_DIR"):
        # We only get here with those set when they named nothing usable -- and
        # OpenSSL's default loader reads the SAME variables, silently, in place
        # of its built-in paths. Load the built-in paths by name so a typo'd
        # variable cannot quietly empty the OS store it was meant to extend.
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
