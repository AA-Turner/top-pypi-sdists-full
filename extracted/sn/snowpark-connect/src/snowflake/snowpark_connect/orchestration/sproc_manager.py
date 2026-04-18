#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Programmatic API for generating Snowflake stored procedures that wrap
Java/Scala JVM classes via ``public static void main(String[] args)``.

Primary entry point: :func:`create_jvm_sproc`.

Future: ``create_python_sproc()`` will be added here for Python-based
stored procedure generation.
"""

from __future__ import annotations

import glob as glob_mod
import os
import time
from typing import Any

import jpype

from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger


# ---------------------------------------------------------------------------
# JAR resolution (JVM-specific)
# ---------------------------------------------------------------------------
def resolve_jars(raw_patterns: list[str]) -> list[str]:
    """Expand glob patterns and return deduplicated absolute JAR paths.

    Args:
        raw_patterns: Glob patterns or literal paths to JAR files.

    Returns:
        List of resolved absolute JAR file paths.

    Raises:
        FileNotFoundError: If a pattern matches no files or the list is empty.
        ValueError: If two JARs share the same basename (Snowflake requires
            unique filenames in the import directory).
    """
    jar_files: list[str] = []
    for pattern in raw_patterns:
        resolved = glob_mod.glob(pattern)
        if not resolved:
            raise FileNotFoundError(f"No files matched pattern: {pattern}")
        jar_files.extend(os.path.abspath(p) for p in resolved)

    if not jar_files:
        raise FileNotFoundError("No JAR files resolved from the supplied patterns.")

    basenames = [os.path.basename(j) for j in jar_files]
    seen: set[str] = set()
    for bn in basenames:
        if bn in seen:
            raise ValueError(
                f"Duplicate JAR basename '{bn}' -- "
                "Snowflake imports require unique filenames."
            )
        seen.add(bn)

    return jar_files


# ---------------------------------------------------------------------------
# JVM validation
# ---------------------------------------------------------------------------
def _validate_main_method(class_name: str) -> None:
    """Verify that *class_name* has a ``public static void main(String[])``."""
    try:
        cls = jpype.JClass(class_name)
    except Exception as exc:
        raise ValueError(f"Class not found: {class_name}") from exc

    Modifier = jpype.JClass("java.lang.reflect.Modifier")
    for m in cls.class_.getDeclaredMethods():
        if str(m.getName()) != "main":
            continue
        params = list(m.getParameterTypes())
        if (
            len(params) == 1
            and str(params[0].getName()) == "[Ljava.lang.String;"
            and Modifier.isStatic(m.getModifiers())
            and Modifier.isPublic(m.getModifiers())
        ):
            logger.info(f"Validated {class_name}.main(String[]) exists")
            return

    available = sorted({str(m.getName()) for m in cls.class_.getDeclaredMethods()})
    raise ValueError(
        f"Class '{class_name}' does not have a "
        f"'public static void main(String[])' method. "
        f"Available methods: {', '.join(available)}"
    )


# ---------------------------------------------------------------------------
# SQL generation (JVM-specific)
# ---------------------------------------------------------------------------
def _generate_jvm_sproc_sql(
    procedure_name: str,
    class_name: str,
    jar_files: list[str],
    stage_name: str,
    replace: bool,
    snowpark_connect_version: str | None = None,
) -> str:
    """Generate the CREATE PROCEDURE DDL for a JVM main() wrapper."""
    create_keyword = (
        "CREATE OR REPLACE PROCEDURE" if replace else "CREATE PROCEDURE IF NOT EXISTS"
    )

    spc_pkg = (
        f"snowpark-connect=={snowpark_connect_version}"
        if snowpark_connect_version
        else "snowpark-connect"
    )

    jar_basenames = [os.path.basename(j) for j in jar_files]
    imports_list = ", ".join(f"'@{stage_name}/{bn}'" for bn in jar_basenames)

    jar_paths_py = "\n".join(
        f'        os.path.join(import_dir, "{bn}"),' for bn in jar_basenames
    )

    return f"""\
{create_keyword} {procedure_name}(job_args ARRAY)
    RETURNS STRING
    LANGUAGE PYTHON
    RUNTIME_VERSION = '3.11'
    PACKAGES = ('{spc_pkg}', 'openjdk==17.0.14')
    IMPORTS = ({imports_list})
    HANDLER = 'run'
    EXECUTE AS CALLER
AS $$
from snowflake.snowpark import Session
import os, threading, time as _time
import jpype

def execute_jar(
    class_name,
    jars,
    job_args=None,
    session=None,
    tcp_port=None,
    jvm_options=None,
):
    # Temporary copy of snowflake.snowpark_connect.server.execute_jar().
    # Will be removed once the Anaconda snowpark-connect package includes it.
    import glob
    stop_event = threading.Event()
    try:
        for jar in jars or []:
            if not glob.glob(jar):
                raise FileNotFoundError(f"JAR not found: {{jar}}")
        for pattern in jars or []:
            for resolved in glob.glob(pattern):
                jpype.addClassPath(os.path.abspath(resolved))

        socket_path = None
        if tcp_port:
            spark_remote_url = f"sc://127.0.0.1:{{tcp_port}}"
        else:
            import tempfile
            socket_dir = tempfile.mkdtemp()
            socket_path = os.path.join(socket_dir, "snowflake_sas_grpc.sock")
            spark_remote_url = f"sc://unix:{{socket_path}}"
        os.environ["SPARK_REMOTE"] = spark_remote_url

        required_flags = [
            "--add-opens=java.base/java.nio=org.apache.arrow.memory.core,ALL-UNNAMED",
            "--add-opens=java.base/jdk.internal.misc=org.apache.arrow.memory.core,ALL-UNNAMED",
            "--add-opens=jdk.unsupported/sun.misc=org.apache.arrow.memory.core,ALL-UNNAMED",
        ]
        existing = os.environ.get("JAVA_OPTS", "").split()
        all_opts = existing + (jvm_options or []) + required_flags
        os.environ["JAVA_OPTS"] = " ".join(dict.fromkeys(all_opts))

        from snowflake.snowpark_connect.server import start_session
        start_session(
            is_daemon=True,
            tcp_port=tcp_port,
            unix_domain_socket=socket_path,
            stop_event=stop_event,
            snowpark_session=session,
        )

        java_args = job_args or []
        java_class = jpype.JClass(class_name)
        java_class.main(java_args)
    finally:
        stop_event.set()
        _time.sleep(1)
        if jpype.isJVMStarted():
            try:
                jpype.shutdownJVM()
            except RuntimeError as e:
                if "main thread" not in str(e):
                    raise

def run(session: Session, job_args: list) -> str:
    import sys
    import_dir = sys._xoptions["snowflake_import_directory"]
    jars = [
{jar_paths_py}
    ]
    execute_jar(
        class_name="{class_name}",
        jars=jars,
        job_args=[str(a) for a in job_args] if job_args else [],
        session=session,
        tcp_port=15002,
    )
    return ""
$$;"""


# ---------------------------------------------------------------------------
# Session management (shared)
# ---------------------------------------------------------------------------
def _get_session():
    """Return a shared Snowpark session, creating one if necessary."""
    from snowflake.snowpark import Session
    from snowflake.snowpark_connect.utils.connection_resolver import (
        resolve_connection_name,
    )

    connection_name = resolve_connection_name()
    return Session.builder.configs({"connection_name": connection_name}).getOrCreate()


# ---------------------------------------------------------------------------
# Create stored procedure (shared across JVM and future Python sprocs)
# ---------------------------------------------------------------------------
def create_sproc(
    create_sql: str,
    import_files: list[str],
    stage_name: str,
    replace: bool,
    session=None,
) -> None:
    """Create a stage, upload import files, and execute the CREATE PROCEDURE DDL.

    When *replace* is True the stage is recreated and all files are uploaded
    unconditionally.  When *replace* is False the stage is created only if it
    does not exist, and each file is skipped if the stage already contains a
    file with the same basename (use ``replace=True`` to force re-upload of
    changed content).

    Args:
        create_sql: The CREATE PROCEDURE DDL to execute.
        import_files: Local file paths to upload to the stage (JARs, .py, etc.).
        stage_name: Name of the Snowflake stage for dependencies.
        replace: If True, recreate stage and overwrite procedure.
        session: Optional Snowpark session. If None, a shared session is
            obtained via ``_get_session()``.

    Raises:
        RuntimeError: If the procedure already exists and *replace* is False.
    """
    session = session or _get_session()
    logger.info(f"Connected to Snowflake: {session.get_current_account()}")

    if replace:
        logger.info(f"Replacing stage {stage_name}...")
        session.sql(f"CREATE OR REPLACE STAGE {stage_name}").collect()
        existing_basenames: set[str] = set()
    else:
        logger.info(f"Creating stage {stage_name} (if not exists)...")
        session.sql(f"CREATE STAGE IF NOT EXISTS {stage_name}").collect()
        listing = session.file.list(f"@{stage_name}")
        existing_basenames = {os.path.basename(r.name) for r in listing}

    for import_file in import_files:
        bn = os.path.basename(import_file)
        if not replace and bn in existing_basenames:
            logger.info(f"Skipping {bn} (already on stage)")
            continue
        logger.info(f"Uploading {bn} to @{stage_name}...")
        session.file.put(
            import_file,
            f"@{stage_name}",
            auto_compress=False,
            overwrite=True,
        )

    logger.info("Executing CREATE PROCEDURE...")
    try:
        session.sql(create_sql).collect()
    except Exception as e:
        err_msg = str(e)
        if not replace and "already exists" in err_msg.lower():
            raise RuntimeError(
                "Procedure already exists. Use replace=True to overwrite it, "
                "or choose a different procedure_name."
            ) from e
        raise

    logger.info("Stored procedure created successfully.")


# ---------------------------------------------------------------------------
# Top-level orchestrator (JVM)
# ---------------------------------------------------------------------------
def create_jvm_sproc(
    class_name: str,
    jar_files: list[str],
    procedure_name: str | None = None,
    replace: bool = False,
    dry_run: bool = False,
    snowpark_connect_version: str | None = None,
) -> str:
    """Create a Snowflake stored procedure that wraps a Java/Scala class.

    The target class must have a ``public static void main(String[] args)``
    method.  The generated procedure accepts a single ``ARRAY`` parameter
    (``job_args``) that is forwarded as ``String[]`` to ``main()``.

    Args:
        class_name: Fully qualified Java/Scala class name.
        jar_files: Resolved absolute paths to JAR files (no globs -- use
            :func:`resolve_jars` first).
        procedure_name: Snowflake procedure name.  Defaults to
            ``<SimpleClassName>_main``.
        replace: Use ``CREATE OR REPLACE PROCEDURE``.
        dry_run: Generate SQL but skip upload and execution.

    Returns:
        The generated CREATE PROCEDURE SQL string.

    Raises:
        FileNotFoundError: No JAR files provided.
        ValueError: Class not found, or missing ``main(String[])`` method.
        RuntimeError: Procedure already exists (when *replace* is False).
    """
    if not jar_files:
        raise FileNotFoundError("At least one JAR file is required.")

    if not procedure_name:
        simple_class = class_name.rsplit(".", 1)[-1]
        procedure_name = f"{simple_class}_main"
    stage_name = f"{procedure_name}_dependencies"

    if jpype.isJVMStarted():
        raise RuntimeError(
            "JVM is already running; cannot start a fresh JVM for validation."
        )

    for jar in jar_files:
        jpype.addClassPath(jar)

    import snowpark_connect_deps_1
    import snowpark_connect_deps_2

    for jar_path in (
        snowpark_connect_deps_1.list_jars() + snowpark_connect_deps_2.list_jars()
    ):
        jpype.addClassPath(str(jar_path))

    jpype.startJVM(convertStrings=True)

    try:
        _validate_main_method(class_name)

        create_sql = _generate_jvm_sproc_sql(
            procedure_name=procedure_name,
            class_name=class_name,
            jar_files=jar_files,
            stage_name=stage_name,
            replace=replace,
            snowpark_connect_version=snowpark_connect_version,
        )
    finally:
        jpype.shutdownJVM()

    if not dry_run:
        create_sproc(create_sql, jar_files, stage_name, replace)

    return create_sql


# ---------------------------------------------------------------------------
# Call a stored procedure
# ---------------------------------------------------------------------------
def call_sproc(
    procedure_name: str,
    job_args: list[str] | None = None,
    poll_interval: float = 5.0,
    timeout: float = 300.0,
    block: bool = True,
    session=None,
) -> None:
    """Call a JVM stored procedure by name.

    The procedure is expected to accept a single ``ARRAY`` parameter
    (the ``job_args``) and return ``STRING`` (always ``""`` for void
    ``main()``).

    When *block* is False, the call is submitted asynchronously via
    ``session.call_nowait()`` and an ``AsyncJob`` is returned for manual
    polling.

    Args:
        procedure_name: Fully qualified or unqualified procedure name.
        job_args: String arguments forwarded to ``main(String[])``.
        poll_interval: Seconds between ``is_done()`` checks (default 5s).
        timeout: Maximum seconds to wait before raising ``TimeoutError``
            (default 300s / 5 min).
        block: If True (default), poll until completion.  If False,
            return the ``AsyncJob`` immediately.
        session: Optional Snowpark session.

    Returns:
        When *block* is True: None (main() is void).
        When *block* is False: the ``snowflake.snowpark.AsyncJob`` object.

    Raises:
        TimeoutError: If the procedure does not complete within *timeout*.
    """
    session = session or _get_session()

    async_job = session.call_nowait(procedure_name, job_args or [])
    logger.info(f"Submitted CALL {procedure_name} (query_id={async_job.query_id})")

    if not block:
        return async_job

    elapsed = 0.0
    while not async_job.is_done():
        if elapsed >= timeout:
            raise TimeoutError(
                f"CALL {procedure_name} did not complete within {timeout}s "
                f"(query_id={async_job.query_id})"
            )
        time.sleep(poll_interval)
        elapsed += poll_interval

    return async_job.result()


# ---------------------------------------------------------------------------
# End-to-end: create + call (JVM)
# ---------------------------------------------------------------------------
def submit_jvm_workload_to_warehouse(
    class_name: str,
    job_args: list[str] | None = None,
    *,
    jar_files: list[str],
    procedure_name: str | None = None,
    replace: bool = False,
    snowpark_connect_version: str | None = None,
    poll_interval: float = 5.0,
    timeout: float = 300.0,
    block: bool = True,
) -> Any:
    """Create a JVM stored procedure and immediately call it.

    Convenience wrapper that combines :func:`create_jvm_sproc` and
    :func:`call_sproc` into a single call.

    Args:
        class_name: Fully qualified Java/Scala class name.
        job_args: String arguments forwarded to ``main(String[])``.
        jar_files: Resolved absolute paths to JAR files (keyword-only).
        procedure_name: Snowflake procedure name (keyword-only).  Defaults
            to ``<SimpleClassName>_main``.
        replace: Use ``CREATE OR REPLACE PROCEDURE`` (keyword-only).
        poll_interval: Seconds between ``is_done()`` checks (keyword-only,
            default 5s).
        timeout: Max seconds to wait (keyword-only, default 300s).
        block: If True (default), poll until completion.  If False, return
            an ``AsyncJob`` (keyword-only).

    Returns:
        When *block* is True: None (main() is void).
        When *block* is False: the ``snowflake.snowpark.AsyncJob`` object.
    """
    create_jvm_sproc(
        class_name=class_name,
        jar_files=jar_files,
        procedure_name=procedure_name,
        replace=replace,
        snowpark_connect_version=snowpark_connect_version,
    )

    resolved_name = procedure_name or f"{class_name.rsplit('.', 1)[-1]}_main"

    return call_sproc(
        procedure_name=resolved_name,
        job_args=job_args,
        poll_interval=poll_interval,
        timeout=timeout,
        block=block,
    )
