"""Runtime detection of the engine's Spark-worker runtime.

What the UDF path needs to know about a connection is two things:

  * the Python **minor** version its Spark workers run (decides sidecar vs local
    build, and which sidecar);
  * the engine's **Spark** version (decides which pyspark the sidecar must use
    for cloudpickle command-format fidelity).

The Spark version is read straight off the engine: ``session.version`` on a
Connect session is a server round trip (``AnalyzePlan`` with ``spark_version``).

The Python version is harder -- it belongs to a process the client never talks
to -- so it is resolved in layers, strongest first, and cached per session:

  0. an explicit override (test seam only);
  1. the cache;
  2. the connection's own metadata, when the engine publishes it;
  3. the engine's runtime conf, where the worker interpreter is often a path
     like ``/usr/bin/python3.13``;
  4. a one-shot WORKER PROBE -- a trivial upstream-built UDF on one row. If it
     runs, the worker matches this client. If it trips the upstream gate, the
     gate's own message names the worker's version. This is authoritative for
     every engine (Glue, EMR Serverless, EMR on EC2/EKS) and self-corrects when
     an engine bumps Python.

Every layer either READS the engine or admits ignorance. A hardcoded
Glue-version-to-Python table used to sit below the probe and was deleted: it was
the only layer that could be confidently wrong, it could not self-correct when an
engine bumped Python, and it answered nothing at all for non-Glue engines. Worse,
consulted with no evidence of a mismatch it could invent one -- routing an engine
whose workers actually match this kernel to a sidecar whose stamp its workers then
reject. Its best case saved a probe; its worst case broke a working engine.

An engine that yields NO signal at all resolves to the client's own version,
which means "matched", which means the untouched upstream local-build path. That
is deliberate, and different from a mismatch we actually OBSERVED but could not
read a version out of: that resolves to :data:`UNKNOWN_PYTHON_VERSION` with
source ``probe-mismatch-unparsed``, reports ``matches_client() is False``, and
makes the UDF path raise with an actionable message. A known-unknown must not
collapse into "fine". Nothing in this module raises; the routing layer does.

``source`` names which layer answered, and is emitted as a metric dimension so
reliance on each one is measurable rather than assumed:

  * ``override``                 -- the test seam;
  * ``connection-metadata``      -- the connection's manager published it;
  * ``server-conf``              -- parsed from a runtime-conf interpreter path;
  * ``probe``                    -- the worker probe answered;
  * ``probe-mismatch-unparsed``  -- a mismatch was seen but no version read;
  * ``client-fallback``          -- no signal at all; assume matched.
"""

from __future__ import annotations

import dataclasses
import itertools
import logging
import os
import re
import weakref
from typing import Any, Dict, List, Optional, Tuple

from sagemaker_studio.utils.udf.registry import client_python_version, normalize_python_version

logger = logging.getLogger("SparkConnect")

# Server runtime-conf keys that may name the WORKER interpreter, most specific
# first.
#
# `spark.pyspark.driver.python` is deliberately NOT here. It names the DRIVER's
# interpreter: Spark declares it in `internal/config` as PYSPARK_DRIVER_PYTHON,
# reads it from `deploy.PythonRunner` (the submit path), and documents it as
# defaulting to `spark.pyspark.python` -- so setting it says nothing about the
# executors, and if it is the only key set the workers use something else
# entirely. The executor interpreter travels separately, as
# `PythonFunction.pythonExec`, to `PythonWorkerFactory`. Under Spark Connect the
# "driver" is the Connect server process, further from the workers still, and
# `worker_util.check_python_version` compares against the WORKER's
# `sys.version_info`. A driver-only signal ranked above the authoritative worker
# probe would let a driver-only configuration silently decide the routing.
SERVER_CONF_PYTHON_KEYS: Tuple[str, ...] = (
    "spark.pyspark.python",
    "spark.executorEnv.PYSPARK_PYTHON",
    "spark.yarn.appMasterEnv.PYSPARK_PYTHON",
)

_MISMATCH_TOKEN = "PYTHON_VERSION_MISMATCH"
# Spark 4 renders "3.13"; Spark 3.5 renders "(3, 13)". Accept both.
_WORKER_VERSION_RE = re.compile(
    r"worker has different version[:\s]+\(?\s*(\d+)\s*[.,]\s*(\d+)\s*\)?"
)
_PYTHON_PATH_RE = re.compile(r"python(\d+)\.(\d+)$")

_PROBE_COLUMN = "_smus_udf_worker_probe"

# "We saw a mismatch but could not read the worker's version." A KNOWN unknown:
# distinct from every real version and from "no signal at all", because the two
# must not be handled the same way.
UNKNOWN_PYTHON_VERSION = "unknown"
UNKNOWN_SPARK_VERSION = "unknown"

MISMATCHED_UNKNOWN_SOURCE = "probe-mismatch-unparsed"


@dataclasses.dataclass(frozen=True)
class WorkerRuntime:
    """What we know about one connection's Spark-worker runtime."""

    python_version: str
    spark_version: str
    # override|connection-metadata|server-conf|probe|probe-mismatch-unparsed|
    # client-fallback
    source: str
    detail: str

    @property
    def is_mismatched_unknown(self) -> bool:
        """A mismatch was OBSERVED, but its worker version could not be read.

        The probe saw the engine's own ``PYTHON_VERSION_MISMATCH`` and no layer
        could name the worker's version. That is evidence of a mismatch, so it
        must never resolve to "matched" -- see :meth:`matches_client`.
        """
        return self.python_version == UNKNOWN_PYTHON_VERSION

    def matches_client(self) -> bool:
        # A known-unknown must not collapse into "fine". Returning True here
        # would take the local-build path against direct evidence that the
        # worker's Python differs, which is how a mismatch we had already
        # DETECTED would still reach `.show()` as a raw PYTHON_VERSION_MISMATCH.
        if self.is_mismatched_unknown:
            return False
        return self.python_version == client_python_version()


_UNPROBED = object()


class _SessionContext:
    """A weak handle to one connection, plus its manager and cached resolution."""

    __slots__ = ("session_ref", "manager", "override", "runtime", "probe_result", "seq")

    def __init__(self, session: Any, session_manager: Any) -> None:
        self.session_ref = weakref.ref(session)
        # Registration order, read by `resolve_current`. Explicit rather than
        # implied by a mapping's iteration order -- see `_REGISTRATION_SEQ`.
        self.seq = next(_REGISTRATION_SEQ)
        # Strong reference: the manager (e.g. GlueSparkSessionManager) is a small,
        # long-lived object owned by the kernel for the life of the connection --
        # unlike the session, it is not something we want to lose the moment the
        # caller's own reference goes out of scope.
        self.manager = session_manager
        self.override: Optional[str] = None
        self.runtime: Optional[WorkerRuntime] = None
        # The probe is one-shot PER CONNECTION, not per resolution: a runtime with
        # an unknown Spark version is deliberately not cached (see
        # `_resolve_and_maybe_cache`), and without this the re-resolve would run
        # the probe -- a real job on the engine -- again for every UDF.
        self.probe_result: Any = _UNPROBED

    @property
    def session(self) -> Any:
        return self.session_ref()


# Keyed by the CLIENT OBJECT. A Connect DataFrame's plan is built with its client,
# and ``Expression.to_plan`` receives exactly that client -- so this is what lets a
# UDF resolve the runtime of the DataFrame it is applied to, per DataFrame, rather
# than per kernel.
#
# A WeakKeyDictionary rather than a plain dict keyed on ``id(client)``, for three
# reasons:
#
#   * Entries disappear with their client, so NO callback of ours runs during
#     garbage collection. That is the shape that hung a test run for 34 minutes
#     when eviction took a module lock from inside a `weakref.finalize` callback,
#     and that still needed a deferred-eviction queue -- drained from seven call
#     sites -- after the lock was removed.
#   * CPython will not raise "dictionary changed size during iteration" while the
#     mapping is being iterated (see ``weakref._IterationGuard``), which is the
#     window that queue was guarding: a collection provoked by the allocation
#     *inside* ``list(_CONTEXTS.values())``. Measured caveat, since the guard is
#     often described as if it froze the mapping: it does not. Iterating while
#     keys die yields FEWER entries rather than erroring -- 5 of 200 in a
#     deliberate test. That is harmless for every read here, which only ever looks
#     for the newest LIVE context and would skip a dead one anyway, but do not
#     write a caller that needs the count to be stable.
#   * An ``id()`` can be stale-matched; an object cannot. With integer keys a
#     freshly allocated, unrelated client can land on a collected one's address
#     and resolve to that connection's ``WorkerRuntime``.
#
# There are no locks here, deliberately: a notebook kernel runs cells on one
# thread and nothing in this package starts another. What that gives up is that a
# caller who creates their own threads may resolve one connection twice and run
# the one-shot worker probe more than once -- a duplicate 1-row job.
_CONTEXTS: "weakref.WeakKeyDictionary[Any, _SessionContext]" = weakref.WeakKeyDictionary()

# The fallback for clients CPython cannot weak-reference or hash -- e.g. a type
# with ``__slots__`` and no ``__weakref__``. Keyed on ``id()``, so it is the one
# place the stale-match hazard above still exists, and it has no automatic
# cleanup: an entry lives until ``unregister_session`` or ``clear_cache``.
# Neither is a regression -- such a client could never have carried a
# ``weakref.finalize`` either, so it always depended on explicit cleanup -- and
# no real client lands here: ``SparkConnectClient`` declares no ``__slots__`` and
# keeps identity ``__eq__``/``__hash__`` (verified on pyspark 3.5.6). No callback
# ever touches this mapping, so it carries none of the garbage-collection
# reentrancy the queue existed for.
_UNWEAKREFFABLE: Dict[int, _SessionContext] = {}

# Registration order, so ``resolve_current`` can name the most recent connection
# without depending on either mapping's iteration order. `WeakKeyDictionary` does
# not document one, and ordering *across* the two mappings has none at all.
_REGISTRATION_SEQ = itertools.count()


# -- context registry accessors ------------------------------------------- #
# Every read and write of the two mappings goes through these four, so which
# mapping a client belongs in is decided in exactly one place.
def _context_get(client: Any) -> Optional[_SessionContext]:
    try:
        return _CONTEXTS.get(client)
    except TypeError:
        return _UNWEAKREFFABLE.get(id(client))


def _context_put(client: Any, context: _SessionContext) -> None:
    try:
        _CONTEXTS[client] = context
    except TypeError:
        logger.debug(
            "client %r cannot be weak-referenced; its context relies on "
            "unregister_session() for cleanup",
            type(client),
        )
        _UNWEAKREFFABLE[id(client)] = context


def _context_pop(client: Any) -> None:
    try:
        _CONTEXTS.pop(client, None)
    except TypeError:
        _UNWEAKREFFABLE.pop(id(client), None)


def _contexts_newest_first() -> List[_SessionContext]:
    """Every live context, most recently registered first."""
    contexts = list(_CONTEXTS.values())
    contexts.extend(_UNWEAKREFFABLE.values())
    contexts.sort(key=lambda context: context.seq, reverse=True)
    return contexts


# -- pure parsers -------------------------------------------------------- #
def parse_worker_version(message: str) -> Optional[str]:
    """Extract the worker's Python minor version from a mismatch error message."""
    if not message:
        return None
    match = _WORKER_VERSION_RE.search(message)
    if match is None:
        return None
    return f"{match.group(1)}.{match.group(2)}"


def python_version_from_path(path: str) -> Optional[str]:
    """``/usr/bin/python3.13`` -> ``'3.13'``; unversioned paths -> ``None``."""
    if not path:
        return None
    match = _PYTHON_PATH_RE.search(path.strip())
    if match is None:
        return None
    return f"{match.group(1)}.{match.group(2)}"


# -- registration -------------------------------------------------------- #
def client_of(session: Any) -> Any:
    """The session's ``SparkConnectClient``, or ``None``.

    Deliberately uses ``object.__getattribute__`` rather than ``getattr``.
    ``LazySparkSession`` implements ``__getattr__`` to create the underlying
    Glue session on first attribute access, so a plain
    ``getattr(session, "_client", None)`` here would make merely INSTALLING the
    routing at kernel start create a Spark session -- expensive, and with the
    failure swallowed at debug level so nobody would see it. It is also
    redundant: ``LazySparkSession._get_spark()`` registers the real session with
    this resolver itself, once it exists.

    ``object.__getattribute__`` consults the instance ``__dict__``, slots and
    type-level descriptors, but does NOT invoke ``__getattr__`` (that hook lives
    on the type's ``tp_getattro`` slot wrapper, which this bypasses). A real
    Connect ``SparkSession`` stores ``_client`` on the instance, so it is found;
    a not-yet-realised ``LazySparkSession`` has no ``_client`` anywhere, so this
    returns ``None`` and the session stays lazy.
    """
    try:
        return object.__getattribute__(session, "_client")
    except AttributeError:
        return None


def register_session(session: Any, session_manager: Any = None) -> None:
    """Associate a live Connect session (and its manager) with its client.

    IDEMPOTENT by design. Two call sites register the same session -- the
    session manager when it creates it, and ``install_udf_interceptor`` when
    the kernel installs the routing factories -- and neither knows about the
    other. A naive re-registration would replace the context and so discard
    both the cached ``WorkerRuntime`` (forcing a needless re-resolve, possibly
    another probe) and any test override set in between. So an existing
    context is kept, and only its missing manager is filled in.

    The context is dropped automatically when the client itself is garbage
    collected, because ``_CONTEXTS`` is keyed on the client object -- so the
    cache is bounded to live clients even if ``unregister_session()`` is never
    called (crash, exception during teardown), with no callback of ours running
    during collection. It also means an ``id()``-reuse hazard is not
    expressible: a new, unrelated client allocated at a collected one's address
    cannot resolve to that connection's stale ``WorkerRuntime``.
    """
    client = client_of(session)
    if client is None:
        logger.debug("session %r has no _client; UDF routing will use the client fallback", session)
        return

    existing = _context_get(client)
    if existing is not None:
        # Adopt a manager if we did not have one yet; never drop the override by
        # replacing the context.
        if session_manager is not None and existing.manager is None:
            existing.manager = session_manager
            # ...but DO drop a resolution reached without it. A manager can
            # answer the connection-metadata layer, which outranks everything
            # below it, and a cached answer would otherwise outlive the arrival
            # of better evidence -- permanently, since the cache is never
            # invalidated. That pins the connection for its whole life: a
            # `mismatched-unknown` keeps raising on every UDF, and a
            # `client-fallback` keeps claiming "matched" and hands the user the
            # raw PYTHON_VERSION_MISMATCH. The probe result is kept, because it
            # is one-shot per connection by design and a manager does not make
            # it stale.
            existing.runtime = None
        return
    _context_put(client, _SessionContext(session, session_manager))


def unregister_session(session: Any) -> None:
    """Forget a session (called when the session is stopped)."""
    client = client_of(session)
    if client is None:
        return
    _context_pop(client)


def set_override(session: Any, python_version: str) -> None:
    """Force the worker Python for one session (test/harness seam only)."""
    client = client_of(session)
    if client is None:
        return
    context = _context_get(client)
    if context is None:
        context = _SessionContext(session, None)
        _context_put(client, context)
    context.override = normalize_python_version(python_version)
    context.runtime = None


def clear_cache() -> None:
    _CONTEXTS.clear()
    _UNWEAKREFFABLE.clear()


def _probe_enabled() -> bool:
    return os.environ.get("SMUS_UDF_WORKER_PROBE", "1").strip().lower() not in (
        "0",
        "false",
        "no",
        "off",
    )


# -- individual layers --------------------------------------------------- #
def _engine_spark_version(session: Any) -> str:
    """The engine's Spark version, read from the server."""
    try:
        version = getattr(session, "version", None)
        if version:
            return str(version)
    except Exception as e:
        logger.debug("could not read the engine Spark version: %s", e)
    return UNKNOWN_SPARK_VERSION


def _from_connection_metadata(manager: Any) -> Optional[str]:
    getter = getattr(manager, "get_connection_python_version", None)
    if not callable(getter):
        return None
    try:
        value = getter()
    except Exception as e:
        logger.debug("connection metadata python version lookup failed: %s", e)
        return None
    if not value:
        return None
    try:
        return normalize_python_version(value)
    except ValueError:
        return None


def _from_server_conf(session: Any) -> Optional[Tuple[str, str, Any]]:
    """``(python_version, key, value)`` from the first conf key that names one.

    Returns WHICH key answered, not just the version. Three keys are candidates
    and only one of them wins on any given engine, so a resolution that reports
    merely "server-conf" cannot tell you whether the other two are ever worth
    reading -- which is the question that decides if this list can shrink.
    """
    conf = getattr(session, "conf", None)
    if conf is None:
        return None
    for key in SERVER_CONF_PYTHON_KEYS:
        try:
            value = conf.get(key, None)
            version = python_version_from_path(str(value) if value else "")
        except Exception as e:
            logger.debug("server conf read of %s failed: %s", key, e)
            continue
        if version:
            logger.info("worker python %s detected from server conf %s=%s", version, key, value)
            return version, key, value
    return None


def _from_probe(session: Any) -> Optional[str]:
    """Run one trivial UDF and read the worker's version from the outcome.

    Uses the UPSTREAM factory deliberately, so the probe is stamped with this
    client's Python. Success means the worker matches; the upstream gate's own
    error names the worker version when it does not.

    Returns :data:`UNKNOWN_PYTHON_VERSION` when the probe tripped the engine's
    ``PYTHON_VERSION_MISMATCH`` but the version could not be parsed out of it.
    That is a distinct answer from ``None`` ("no signal"): a mismatch was
    OBSERVED, and the caller must not let a later layer -- or the client
    fallback -- claim the worker matches.
    """
    if not _probe_enabled():
        return None
    try:
        from pyspark.sql.connect.functions import udf as upstream_udf
        from pyspark.sql.types import IntegerType

        probe = upstream_udf(lambda _: 1, returnType=IntegerType())
    except Exception as e:  # pragma: no cover - pyspark is a hard dependency
        logger.debug("cannot build the upstream probe udf: %s", e)
        return None

    try:
        session.range(1).select(probe("id").alias(_PROBE_COLUMN)).collect()
    except Exception as e:
        text = f"{e}"
        worker_version = parse_worker_version(text)
        if worker_version:
            logger.info("worker python %s detected from the probe's mismatch error", worker_version)
            return worker_version
        if _MISMATCH_TOKEN in text:
            logger.warning(
                "worker probe hit %s but the worker version could not be parsed from: %s",
                _MISMATCH_TOKEN,
                text,
            )
            return UNKNOWN_PYTHON_VERSION
        else:
            logger.info("worker probe failed for an unrelated reason (%s); falling through", e)
        return None
    logger.info("worker probe succeeded; the worker matches this client's Python")
    return client_python_version()


# -- public resolution --------------------------------------------------- #
def _resolve_and_maybe_cache(context: _SessionContext) -> WorkerRuntime:
    """Resolve, and memoize the result only if it is worth keeping.

    ``spark_version`` comes from ``session.version``, a live server round trip.
    A single transient failure there yields ``"unknown"``, and memoizing that
    would pin the connection to ``entry.builder("unknown")`` for the rest of its
    life -- a sidecar built against the wrong pyspark, for every later UDF, long
    after ``session.version`` started answering again. So an ``"unknown"`` Spark
    version is returned but not cached: the next call re-resolves.

    """
    runtime = _resolve(context)
    if runtime.spark_version == UNKNOWN_SPARK_VERSION:
        logger.warning(
            "resolved worker runtime with an unknown Spark version (python=%s source=%s); "
            "not caching it, so a transient `session.version` failure does not pin this "
            "connection to a wrong-pyspark sidecar",
            runtime.python_version,
            runtime.source,
        )
        return runtime
    context.runtime = runtime
    return runtime


def _resolve(context: _SessionContext) -> WorkerRuntime:
    session = context.session
    if session is None:
        return WorkerRuntime(
            client_python_version(),
            UNKNOWN_SPARK_VERSION,
            "client-fallback",
            "the session has been collected",
        )
    spark_version = _engine_spark_version(session)
    manager = context.manager

    if context.override:
        return WorkerRuntime(context.override, spark_version, "override", "set via set_override()")

    version = _from_connection_metadata(manager)
    if version:
        return WorkerRuntime(
            version, spark_version, "connection-metadata", "published by the connection"
        )

    conf_hit = _from_server_conf(session)
    if conf_hit:
        version, conf_key, conf_value = conf_hit
        return WorkerRuntime(version, spark_version, "server-conf", f"{conf_key}={conf_value!r}")

    if context.probe_result is _UNPROBED:
        context.probe_result = _from_probe(session)
    version = context.probe_result
    if version == UNKNOWN_PYTHON_VERSION:
        # A mismatch was OBSERVED but its worker version could not be read, so the
        # honest state is "mismatched, version unknown" -- which raises at build
        # time with an actionable message. Nothing guesses a version here: a
        # Glue-version table used to, and reaching this point essentially requires
        # upstream to have changed its mismatch wording, which ships with a new
        # Spark release -- exactly when such a table is most likely stale. This
        # must not fall through to `client-fallback` and report
        # `matches_client() is True`, which would take the local path against
        # evidence of a mismatch and hand the user the raw
        # PYTHON_VERSION_MISMATCH at `.show()` after all.
        return WorkerRuntime(
            UNKNOWN_PYTHON_VERSION,
            spark_version,
            MISMATCHED_UNKNOWN_SOURCE,
            "the engine reported a Python version mismatch whose worker version could not "
            "be parsed, and no other layer named it",
        )
    if version:
        return WorkerRuntime(version, spark_version, "probe", "one-shot worker probe")

    return WorkerRuntime(
        client_python_version(),
        spark_version,
        "client-fallback",
        "no engine signal; assuming the worker matches this client (local build)",
    )


def _resolve_context(context: _SessionContext) -> WorkerRuntime:
    """Cached resolution for one context."""
    if context.runtime is not None:
        return context.runtime
    return _resolve_and_maybe_cache(context)


def resolve_for_session(session: Any) -> WorkerRuntime:
    """Resolve (and cache) the worker runtime for a session."""
    client = client_of(session)
    context = _context_get(client) if client is not None else None
    if context is None:
        context = _SessionContext(session, None)
        if client is not None:
            _context_put(client, context)
    if context.runtime is not None:
        return context.runtime
    runtime = _resolve_and_maybe_cache(context)
    logger.info(
        "resolved worker runtime: python=%s spark=%s (source=%s: %s)",
        runtime.python_version,
        runtime.spark_version,
        runtime.source,
        runtime.detail,
    )
    return runtime


def resolve_for_client(client: Any) -> WorkerRuntime:
    """Resolve the worker runtime for the session behind a ``SparkConnectClient``.

    This is the per-DataFrame entry point: ``Expression.to_plan`` receives the
    client that is building the plan, which identifies the target connection
    exactly -- even in a notebook holding several sessions at once.
    """
    context = _context_get(client)
    if context is None:
        return WorkerRuntime(
            client_python_version(),
            UNKNOWN_SPARK_VERSION,
            "client-fallback",
            "this client is not registered with the SDK; assuming a matched worker",
        )
    return _resolve_context(context)


def resolve_current() -> Optional[WorkerRuntime]:
    """The worker runtime of the most recently registered LIVE connection.

    Routing itself never uses this: it resolves the client that is building the
    plan (:func:`resolve_for_client`), which is what makes the decision per
    DataFrame. But a UDF *object* has no target DataFrame, so the descriptive
    attributes it carries (see ``routed`` / ``python_ver`` in
    :mod:`sagemaker_studio.utils.udf.routed`) describe the engine that is
    resolvable RIGHT NOW -- the most recent live registration. ``None`` when
    there is none.

    Registers nothing and creates nothing. A session that was never registered
    is simply invisible here -- in particular a still-lazy ``LazySparkSession``,
    which has no ``_client`` to key on, so reading these attributes cannot be
    what creates a Spark session.
    """
    for context in _contexts_newest_first():
        if context.session is None:
            # Its session was collected; it can no longer describe an engine.
            continue
        return _resolve_context(context)
    return None
