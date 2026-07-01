#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Bridge log4j2 records emitted by the JVM (e.g. by customer JARs invoked via
:func:`snowflake.snowpark_connect.server.execute_jar`) into Python's
``logging`` module so they surface on stdout / stderr of the host process.

The motivation is the stored-procedure path: when the SCOS server runs inside
a Snowflake Python stored procedure, log4j2 records emitted inside the JPype
JVM are not picked up by Snowflake's event table, but Python ``logging``
records *are*.  Re-exporting JVM log records through Python logging is a
zero-touch fix for the customer JAR.

Wiring summary
--------------
1. A small log4j2 ``AbstractAppender`` lives in ``sas-scala-udf-*.jar``
   (``com.snowflake.sas.scala.log.SnowparkConnectPythonBridgeAppender``) and
   is shipped with the deps wheels, so it is already on the sproc JVM
   classpath.
2. The appender is parametrised with a Java interface
   (``com.snowflake.sas.scala.log.PyLogSink``) whose implementation is
   provided here via JPype's ``@JImplements`` mechanism.
3. :func:`install_python_bridge_appender` instantiates the appender and
   attaches it to the root ``LoggerConfig`` of the embedded JVM.

The embedded JVM is throwaway -- it terminates with the workload -- so the
install path is one-shot: there is no uninstall, the appender simply stops
receiving events when the JVM shuts down. The Python ``sink`` / appender
objects are kept alive in a module-level list so JPype's proxy is not
GC'd while the JVM still holds a pointer.

Logger naming
-------------
Bridged records are emitted under ``snowflake.snowpark_connect.jvm.<java>``
where ``<java>`` is the original log4j category (e.g.
``org.apache.spark.sql.SparkSession``).  The parent
``snowflake.snowpark_connect.jvm`` gets a ``StreamHandler`` installed on
module import so children propagate to a real sink, while the Python
``%(name)s`` field still carries the Java category.

Environment overrides
---------------------
``SNOWPARK_CONNECT_LOG4J_BRIDGE_LEVEL``
    Lowest log4j level forwarded to Python.  Accepts a log4j name
    (``TRACE``/``DEBUG``/``INFO``/``WARN``/``ERROR``/``FATAL``/``OFF``).
    Defaults to ``INFO``.

``SNOWPARK_CONNECT_LOG4J_BRIDGE_DISABLE``
    When set to ``1``, :func:`install_python_bridge_appender` is a no-op
    and returns ``False``. Escape hatch for cases where the bridge needs
    to be turned off without code changes.

``SNOWPARK_CONNECT_LOG4J_BRIDGE_FORCE``
    Honoured by the caller (``server.execute_jar``) -- not by this
    module. When set to ``1`` it bypasses the warehouse / stored
    procedure detection so the bridge is wired in local runs too. Useful
    for reproducing the sproc logging behaviour from the CLI and for
    integration tests.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

import jpype

from snowflake.snowpark_connect.utils.snowpark_connect_logging import (
    ensure_logger_has_handler,
    logger,
)

_ENV_LEVEL = "SNOWPARK_CONNECT_LOG4J_BRIDGE_LEVEL"
_ENV_DISABLE = "SNOWPARK_CONNECT_LOG4J_BRIDGE_DISABLE"

_BRIDGE_APPENDER_CLASS = (
    "com.snowflake.sas.scala.log.SnowparkConnectPythonBridgeAppender"
)
_PY_LOG_SINK_INTERFACE = "com.snowflake.sas.scala.log.PyLogSink"

# Parent namespace under which bridged JVM records are emitted. Children
# preserve the original Java logger name as a suffix so the Python
# ``%(name)s`` field carries the Java category, while propagation guarantees
# the parent's StreamHandler (installed below) actually emits the record.
JVM_LOGGER_PARENT = "snowflake.snowpark_connect.jvm"

# Python's stdlib does not predefine TRACE; register it once on import so the
# sink can forward log4j2 TRACE events without losing fidelity.
_TRACE_LEVEL_NUM = 5
logging.addLevelName(_TRACE_LEVEL_NUM, "TRACE")

# Ensure the parent logger has a StreamHandler at import time. Children get
# their records emitted via propagation, so the customer's Java logger names
# (e.g. ``org.apache.spark.sql.SparkSession``) are preserved while still
# being printed.
ensure_logger_has_handler(JVM_LOGGER_PARENT, logging.INFO, force_level=False)

_LEVEL_MAP: dict[str, int] = {
    "FATAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARN": logging.WARNING,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "TRACE": _TRACE_LEVEL_NUM,
}

# Keep installed bridge objects alive so JPype's proxy (and the Python sink it
# wraps) is not garbage-collected while the JVM still holds a reference to it.
# The JVM is throwaway -- the entries are released on process exit.
_ACTIVE_BRIDGES: list[tuple] = []


_LOG4J_CONTEXT_SELECTOR_PROPERTY = (
    "-Dlog4j2.contextSelector="
    "org.apache.logging.log4j.core.selector.BasicContextSelector"
)

_JUL_LOG_MANAGER_PROPERTY = (
    "-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager"
)


def _ensure_basic_context_selector() -> None:
    """Force log4j2 to use ``BasicContextSelector`` for the embedded JVM.

    The default ``ClassLoaderContextSelector`` keys each
    :class:`org.apache.logging.log4j.core.LoggerContext` by the *caller
    class's* classloader. In an embedded JPype JVM that hosts customer JARs
    side-by-side with our own jars, JPype-side and customer-side callers can
    resolve to two distinct LoggerContexts (both happen to be named
    ``Default``), so an appender installed by the Python side never sees
    events emitted from the customer code.

    ``BasicContextSelector`` keeps a single process-wide LoggerContext
    regardless of caller, which is what we want for ``execute_jar``: a
    single shared configuration where the Python bridge appender is
    guaranteed to catch every record.
    """
    java_opts = os.environ.get("JAVA_OPTS", "")
    if "log4j2.contextSelector" in java_opts:
        return
    new_opts = (java_opts + " " + _LOG4J_CONTEXT_SELECTOR_PROPERTY).strip()
    os.environ["JAVA_OPTS"] = new_opts


def _ensure_jul_log_manager() -> None:
    """Replace the JVM's ``java.util.logging.LogManager`` with log4j-jul.

    log4j-jul ships ``org.apache.logging.log4j.jul.LogManager``, a JUL
    ``LogManager`` subclass whose ``Logger`` instances delegate to
    log4j2. Setting the ``java.util.logging.manager`` system property
    *before* the JVM starts (i.e. before any code touches
    ``LogManager.getLogManager()``) makes every JUL record produced by
    the JDK or by customer JARs flow through log4j2, where the existing
    :func:`install_python_bridge_appender` picks it up alongside native
    log4j2 records.

    The property is only meaningful before the JVM boots: once
    ``LogManager`` has been initialised JUL caches the implementation
    class and ignores subsequent changes. We therefore set it via
    ``JAVA_OPTS`` from :func:`add_bridge_jar_to_classpath` (which the
    contract requires the caller to invoke before
    :func:`jpype.startJVM`).

    ``log4j-jul-<ver>.jar`` is bundled in ``includes/jars/`` and added
    to the classpath alongside ``sas-scala-udf`` so the LogManager class
    is loadable.
    """
    java_opts = os.environ.get("JAVA_OPTS", "")
    if "java.util.logging.manager" in java_opts:
        return
    new_opts = (java_opts + " " + _JUL_LOG_MANAGER_PROPERTY).strip()
    os.environ["JAVA_OPTS"] = new_opts


def add_bridge_jar_to_classpath(scala_version: str | None = None) -> Path | None:
    """Prepare the JVM for the log4j -> Python bridge appender.

    Must be called *before* :func:`jpype.startJVM`. Performs two pre-JVM
    setup steps:

    1. Adds the ``sas-scala-udf`` jar that ships the bridge appender
       (``com.snowflake.sas.scala.log.SnowparkConnectPythonBridgeAppender``)
       to the JVM classpath. The jar is bundled at
       ``snowflake/snowpark_connect/includes/jars/sas-scala-udf_<scala>-*.jar``
       and is not part of ``snowpark_connect_deps_*``; without this step
       the appender class is not reachable to the running JVM.
    2. Adds the ``log4j-jul`` jar bundled at
       ``snowflake/snowpark_connect/includes/jars/log4j-jul-<ver>.jar``
       so the JUL ``LogManager`` replacement class (set via the
       ``java.util.logging.manager`` system property below) is loadable.
       Routing JUL through log4j2 lets the Python bridge appender pick
       up records from the JDK and from customer code that uses
       ``java.util.logging`` directly.
    3. Appends ``-Dlog4j2.contextSelector=...BasicContextSelector`` to
       ``JAVA_OPTS`` so that all JVM-side log4j2 callers (ours, Spark
       Connect's, the customer JAR's) share a single LoggerContext. See
       :func:`_ensure_basic_context_selector` for the rationale.
    4. Appends
       ``-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager``
       to ``JAVA_OPTS`` so JUL records flow through log4j2. See
       :func:`_ensure_jul_log_manager` for the rationale.

    Args:
        scala_version: Explicit Scala binary version (``"2.12"`` or
            ``"2.13"``) to pick the matching bridge jar. When ``None``
            (default), falls back to
            :func:`snowflake.snowpark_connect.config.get_scala_version`,
            with a final ``"2.12"`` belt-and-suspenders default if that
            ever returns a falsy value.

    Returns the resolved jar path, or ``None`` when the jar cannot be
    found or the JVM has already started.
    """
    if jpype.isJVMStarted():
        logger.warning(
            "Cannot add log4j bridge jar to classpath: JVM has already started"
        )
        return None
    try:
        _ensure_basic_context_selector()
        _ensure_jul_log_manager()

        # Local import to avoid pulling resources_initializer at module load.
        from snowflake.snowpark_connect.resources_initializer import (
            LOG4J_JUL_JAR,
            SAS_SCALA_UDF_JAR_212,
            SAS_SCALA_UDF_JAR_213,
        )

        if scala_version is None:
            from snowflake.snowpark_connect.config import get_scala_version

            scala_version = get_scala_version() or "2.12"
        jar_name = (
            SAS_SCALA_UDF_JAR_213
            if str(scala_version).startswith("2.13")
            else SAS_SCALA_UDF_JAR_212
        )

        includes_jars_dir = Path(__file__).resolve().parent.parent / "includes" / "jars"
        jar_path = includes_jars_dir / jar_name
        if not jar_path.is_file():
            logger.warning(
                "log4j bridge jar not found at %s; the bridge appender will "
                "not be loadable",
                jar_path,
            )
            return None
        jpype.addClassPath(str(jar_path))

        # Best-effort: missing log4j-jul jar must not block install of the
        # log4j2 bridge itself, so we log and continue. Without it, JUL
        # records simply stay invisible to the Python sink (the previous
        # behaviour); native log4j2 records still flow through.
        jul_jar_path = includes_jars_dir / LOG4J_JUL_JAR
        if jul_jar_path.is_file():
            jpype.addClassPath(str(jul_jar_path))
        else:
            logger.warning(
                "log4j-jul jar not found at %s; java.util.logging records "
                "will not be forwarded to the Python bridge",
                jul_jar_path,
            )

        return jar_path
    except Exception:
        logger.warning(
            "Failed to add log4j bridge jar to JVM classpath",
            exc_info=True,
        )
        return None


def _build_sink_class() -> type:
    """Build the ``@JImplements`` class lazily.

    JPype's ``@JImplements`` decorator resolves the target interface at
    decoration time, which requires the JVM to be running.  Building the class
    on demand defers that requirement to ``install_python_bridge_appender``
    callers, who are expected to invoke us after ``start_session()`` has
    started the JVM.
    """

    @jpype.JImplements(_PY_LOG_SINK_INTERFACE)
    class _PyLogSinkImpl:
        @jpype.JOverride
        def accept(
            self,
            level,
            loggerName,
            message,
            throwableText,
            timestampMillis,
            threadName,
        ):
            level_name = str(level) if level is not None else "INFO"
            py_level = _LEVEL_MAP.get(level_name.upper(), logging.INFO)
            java_name = str(loggerName) if loggerName else "root"

            # Optimization: do not format strings text and throwable if Python-side logging is disabled for this level.
            # str() for text and throwable crosses JNI boundary so avoid if not needed. Java side logger could be set to
            # INFO but the Python side logger for catgeory `snowflake.snowpark_connect.jvm` may be set to ERORR. In such
            # cases, we can skip the string str() and avoid the JNI hop.
            target = logging.getLogger(f"{JVM_LOGGER_PARENT}.{java_name}")
            if not target.isEnabledFor(py_level):
                return

            text = str(message) if message is not None else ""
            throwable = str(throwableText) if throwableText else ""
            if throwable:
                # The throwable text already contains a leading marker
                # ("java.lang.RuntimeException: ..."), so concatenation keeps
                # the Python record self-contained and avoids reconstructing a
                # Python ``exc_info`` from a Java ``Throwable``.
                text = f"{text}\n{throwable}" if text else throwable
            try:
                thread_name = str(threadName) if threadName else ""
                target.log(
                    py_level,
                    text,
                    extra={"jvm_thread": thread_name},
                )
            except Exception:
                # Never let a logging failure propagate back into the JVM.
                pass

    return _PyLogSinkImpl


def _resolve_threshold(threshold: str | None) -> str:
    if threshold is None:
        threshold = os.environ.get(_ENV_LEVEL, "INFO")
    threshold = threshold.strip().upper() if threshold else "INFO"
    if threshold not in _LEVEL_MAP and threshold not in ("OFF",):
        logger.warning(
            "Unknown log4j level %r for %s; defaulting to INFO",
            threshold,
            _ENV_LEVEL,
        )
        threshold = "INFO"
    return threshold


def install_python_bridge_appender(
    threshold: str | None = None,
    appender_name: str | None = None,
) -> bool:
    """Attach the Python-bridge appender to the root log4j2 logger.

    Must be called after the JVM has been started (e.g. after
    :func:`snowflake.snowpark_connect.server.start_session`). Relies on
    :func:`add_bridge_jar_to_classpath` having set the
    ``log4j2.contextSelector`` system property *before* the JVM started,
    so there is a single process-wide ``LoggerContext`` to attach to.

    The embedded JVM is throwaway -- there is no uninstall; the appender
    stops receiving events when the JVM shuts down at the end of the
    workload.

    Returns ``True`` on successful install, ``False`` when
    ``SNOWPARK_CONNECT_LOG4J_BRIDGE_DISABLE=1`` is set or when the install
    fails for any reason (a logging shim must never break the customer
    workload).
    """
    if os.environ.get(_ENV_DISABLE, "") == "1":
        logger.info(
            "log4j -> Python bridge appender disabled via %s",
            _ENV_DISABLE,
        )
        return False

    if not jpype.isJVMStarted():
        logger.warning(
            "Cannot install log4j -> Python bridge appender: JVM is not running"
        )
        return False

    try:
        threshold_name = _resolve_threshold(threshold)
        level_cls = jpype.JClass("org.apache.logging.log4j.Level")
        try:
            level = level_cls.valueOf(threshold_name)
        except Exception:
            level = level_cls.INFO

        log_manager = jpype.JClass("org.apache.logging.log4j.LogManager")
        bridge_cls = jpype.JClass(_BRIDGE_APPENDER_CLASS)

        sink_cls = _build_sink_class()
        sink = sink_cls()

        name = appender_name or str(bridge_cls.DEFAULT_NAME)
        appender = bridge_cls.create(name, level, sink)
        appender.start()

        ctx = log_manager.getContext(False)
        cfg = ctx.getConfiguration()
        rcfg = cfg.getRootLogger()
        cfg.addAppender(appender)
        rcfg.addAppender(appender, level, None)

        # log4j2's DefaultConfiguration pins the root level at ERROR, which
        # would filter out everything below ERROR before any appender
        # (including ours) sees it. Widen the root level to the bridge
        # threshold so records at that level actually reach the appender.
        # Never narrow: if the current level is already more permissive,
        # leave it alone.
        original_level = rcfg.getLevel()
        if original_level is not None and original_level.isMoreSpecificThan(level):
            rcfg.setLevel(level)

        ctx.updateLoggers()

        # Hold the JPype proxy and the appender so the JVM-side references
        # remain valid for the lifetime of the embedded JVM.
        _ACTIVE_BRIDGES.append((appender, sink))
        logger.info(
            "Installed log4j -> Python bridge appender '%s' at threshold %s",
            name,
            threshold_name,
        )
        return True
    except Exception:
        logger.warning(
            "Failed to install log4j -> Python bridge appender; "
            "JVM log records will not be forwarded to Python logging",
            exc_info=True,
        )
        return False
