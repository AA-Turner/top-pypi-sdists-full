#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Programmatic API for generating Snowflake stored procedures that wrap
Java/Scala JVM classes via ``public static void main(String[] args)`` or
Python modules executed via ``runpy.run_module``.

Primary entry points:
    :func:`create_jvm_sproc`, :func:`submit_jvm_workload_to_warehouse`
    :func:`create_python_sproc`, :func:`submit_python_workload_to_warehouse`
"""

from __future__ import annotations

import glob as glob_mod
import os
import re
import time
from typing import Any

import jpype

from snowflake.snowpark_connect.utils.identifiers import UNQUOTED_IDENTIFIER_REGEX
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

_VALID_IDENTIFIER_RE = re.compile(rf"\A{UNQUOTED_IDENTIFIER_REGEX}\Z")


def is_valid_snowflake_identifier(name: str) -> bool:
    return bool(_VALID_IDENTIFIER_RE.match(name))


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
    scala_version: str | None = None,
    native_app: bool = False,
) -> str:
    """Generate the CREATE PROCEDURE DDL for a JVM main() wrapper.

    When *scala_version* is ``None`` the emitted handler calls
    ``execute_jar(...)`` without the ``scala_version`` kwarg, keeping it
    wire-compatible with older ``snowpark-connect`` packages whose
    ``execute_jar()`` predates that parameter. When set, the handler
    statically passes ``scala_version="2.12"`` / ``scala_version="2.13"``.

    When *native_app* is True the proc is generated for use inside a Snowflake
    Native App: it uses ``EXECUTE AS OWNER`` (apps disallow ``EXECUTE AS
    CALLER``), references its JARs via **version-stage-relative** ``/``-paths
    (a versioned-schema proc cannot import via a direct stage reference —
    error 093023), and enables ``native_app_mode`` so any Scala UDF closures
    the JAR registers use relative imports too. The app provider is expected to
    bundle the JARs at the version-stage root (e.g. via ``snowflake.yml``
    artifacts); there is no ``CREATE STAGE``/``PUT`` in this mode.
    """
    create_keyword = (
        "CREATE OR REPLACE PROCEDURE" if replace else "CREATE PROCEDURE IF NOT EXISTS"
    )

    spc_pkg = (
        f"snowpark-connect=={snowpark_connect_version}"
        if snowpark_connect_version
        else "snowpark-connect"
    )

    jar_basenames = [os.path.basename(j) for j in jar_files]
    if native_app:
        # Version-stage-relative imports (bundled as app artifacts at the
        # version-stage root). Direct '@stage/...' refs are rejected in a
        # versioned schema (093023).
        imports_list = ", ".join(f"'/{bn}'" for bn in jar_basenames)
    else:
        imports_list = ", ".join(f"'@{stage_name}/{bn}'" for bn in jar_basenames)

    jar_paths_py = "\n".join(
        f'        os.path.join(import_dir, "{bn}"),' for bn in jar_basenames
    )

    scala_kw = f', scala_version="{scala_version}"' if scala_version else ""

    execute_as = "OWNER" if native_app else "CALLER"
    # Native App setup, emitted into the handler before execute_jar():
    #   * skip_session_configuration(True): owner's-rights procs can't run
    #     ALTER SESSION, which SCOS otherwise issues at startup. This is a
    #     released API, so we call it explicitly rather than rely on
    #     execute_jar's in-proc auto-skip (which may not be in the deployed
    #     package yet).
    #   * native_app_mode=true: so any Scala UDF the JAR registers uses relative
    #     version-stage imports. Not a callback config key, so setting it off the
    #     proc thread is safe.
    native_app_setup = (
        "    from snowflake.snowpark_connect import skip_session_configuration\n"
        "    skip_session_configuration(True)\n"
        "    from snowflake.snowpark_connect.config import global_config\n"
        '    global_config.set("snowpark.connect.native_app_mode", "true")\n'
        if native_app
        else ""
    )

    return f"""\
{create_keyword} {procedure_name}(job_args ARRAY, log_level STRING DEFAULT 'INFO')
    RETURNS STRING
    LANGUAGE PYTHON
    RUNTIME_VERSION = '3.11'
    PACKAGES = ('{spc_pkg}', 'openjdk==17.0.14')
    IMPORTS = ({imports_list})
    HANDLER = 'run'
    EXECUTE AS {execute_as}
AS $$
from snowflake.snowpark import Session
import os, threading, time as _time
import logging
from snowflake.snowpark_connect.server import execute_jar

def run(session: Session, job_args: list, log_level: str = "INFO") -> str:
    import sys
    import_dir = sys._xoptions["snowflake_import_directory"]
    jars = [
{jar_paths_py}
    ]

    level = (log_level or "INFO").upper()
    os.environ["SNOWPARK_CONNECT_LOG4J_BRIDGE_LEVEL"] = level
    logging.basicConfig(level=level)
    logger = logging.getLogger(__name__)
{native_app_setup}    try:
        execute_jar(
            class_name="{class_name}",
            jars=jars,
            job_args=[str(a) for a in job_args] if job_args else [],
            session=session,
            tcp_port=15002{scala_kw},
        )
    except Exception as ex:
        logger.exception(f"Error executing class: {class_name}")
        raise
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
# Stage / PUT SQL generation (used for --dry-run output)
# ---------------------------------------------------------------------------
def _generate_stage_setup_sql(
    import_files: list[str], stage_name: str, replace: bool
) -> str:
    """Generate the ``CREATE STAGE`` + ``PUT`` SQL block for a sproc.

    Mirrors the runtime steps performed by :func:`create_sproc` so that
    ``--dry-run`` output can be copy-pasted into a Snowflake worksheet.

    Args:
        import_files: Local file paths that would be uploaded.
        stage_name: Target stage name.
        replace: If True, emit ``CREATE OR REPLACE STAGE``; otherwise
            ``CREATE STAGE IF NOT EXISTS``.

    Returns:
        Newline-joined SQL block (no trailing newline).
    """
    if replace:
        stage_stmt = f"CREATE OR REPLACE STAGE {stage_name};"
    else:
        stage_stmt = f"CREATE STAGE IF NOT EXISTS {stage_name};"

    put_stmts = [
        f"PUT file://{os.path.abspath(p)} @{stage_name} "
        f"AUTO_COMPRESS = FALSE OVERWRITE = TRUE;"
        for p in import_files
    ]
    return "\n".join([stage_stmt, *put_stmts])


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
_SUPPORTED_SCALA_VERSIONS = ("2.12", "2.13")


def create_jvm_sproc(
    class_name: str,
    jar_files: list[str],
    procedure_name: str | None = None,
    replace: bool = False,
    dry_run: bool = False,
    snowpark_connect_version: str | None = None,
    scala_version: str | None = None,
    native_app: bool = False,
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
        dry_run: Generate SQL but skip upload and execution. Ignored when
            *native_app* is True (that mode never deploys, so it always
            behaves as a dry run -- see *native_app* and Returns).
        snowpark_connect_version: Pin ``snowpark-connect`` to a version.
        scala_version: Optional Scala binary version (``"2.12"`` or
            ``"2.13"``) baked into the generated handler. ``None`` (the
            default) omits the kwarg from the emitted ``execute_jar(...)``
            call entirely, keeping the sproc body wire-compatible with
            older ``snowpark-connect`` releases whose ``execute_jar()``
            does not accept ``scala_version``.
        native_app: Generate a proc for use inside a Snowflake Native App:
            ``EXECUTE AS OWNER``, version-stage-relative ``IMPORTS``, and
            ``native_app_mode`` enabled. In this mode no stage is created and
            nothing is deployed -- only the ``CREATE PROCEDURE`` DDL is
            returned (to paste into the app's ``setup_script.sql``), so
            *dry_run* has no effect.

    Returns:
        In native-app mode: just the ``CREATE PROCEDURE`` DDL (no stage/PUT,
        nothing deployed). Otherwise: the full SQL script -- ``CREATE [OR
        REPLACE] STAGE`` + one ``PUT`` statement per JAR + the ``CREATE
        PROCEDURE`` DDL, joined with blank lines. That full script is what
        ``--dry-run`` prints; in non-dry-run mode the equivalent steps are
        executed via the Snowpark API.

    Raises:
        FileNotFoundError: No JAR files provided.
        ValueError: Class not found, missing ``main(String[])`` method, or
            unsupported *scala_version*.
        RuntimeError: Procedure already exists (when *replace* is False).
    """
    if not jar_files:
        raise FileNotFoundError("At least one JAR file is required.")

    if scala_version is not None and scala_version not in _SUPPORTED_SCALA_VERSIONS:
        raise ValueError(
            f"Unsupported scala_version {scala_version!r}; "
            f"expected one of {list(_SUPPORTED_SCALA_VERSIONS)}."
        )

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
            scala_version=scala_version,
            native_app=native_app,
        )
    finally:
        jpype.shutdownJVM()

    if native_app:
        # Native App: no CREATE STAGE / PUT and no imperative deploy. The app
        # bundles the JARs as version-stage artifacts and installs the proc via
        # its setup script, so we only return the CREATE PROCEDURE DDL (to paste
        # into setup_script.sql). dry_run is implied.
        return create_sql

    stage_setup_sql = _generate_stage_setup_sql(jar_files, stage_name, replace)
    full_sql = f"{stage_setup_sql}\n\n{create_sql}"

    if not dry_run:
        create_sproc(create_sql, jar_files, stage_name, replace)

    return full_sql


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
    log_level: str | None = None,
) -> None:
    """Call a stored procedure by name.

    The procedure is expected to accept a single semi-structured ``ARRAY``
    parameter (the ``job_args``) and return ``STRING`` (always ``""`` for
    void ``main()``).

    The CALL is issued as raw SQL (``CALL X(ARRAY_CONSTRUCT(?, ?, ...))``)
    rather than via ``session.call()``/``session.call_nowait()``.  The
    latter binds Python lists as structured ``ARRAY(VARCHAR)`` in
    Snowpark Python >= 1.50, which does not match the procedure's
    untyped ``ARRAY`` signature.  ``ARRAY_CONSTRUCT`` always yields a
    semi-structured ``ARRAY`` and matches the DDL.

    Args:
        procedure_name: Fully qualified or unqualified procedure name.
        job_args: String arguments forwarded to ``main(String[])``.
        poll_interval: Seconds between ``is_done()`` checks (default 5s).
        timeout: Maximum seconds to wait before raising ``TimeoutError``
            (default 300s / 5 min).
        block: If True (default), poll until completion and return the
            scalar return value of the procedure.  If False, return the
            ``AsyncJob`` immediately.
        session: Optional Snowpark session.
        log_level: Optional log level name (e.g. ``"DEBUG"``, ``"INFO"``,
            ``"WARN"``) forwarded to the procedure as its second argument.
            When ``None``, the CALL omits the argument so the procedure's
            ``DEFAULT 'INFO'`` applies (and pre-existing single-argument
            procedures keep working).

    Returns:
        When *block* is True: the procedure's scalar return value
            (typically ``""`` for void ``main()``).
        When *block* is False: the ``snowflake.snowpark.AsyncJob`` object.

    Raises:
        TimeoutError: If the procedure does not complete within *timeout*.
    """
    session = session or _get_session()

    args = list(job_args or [])
    placeholders = ", ".join(["?"] * len(args))
    if log_level is not None:
        sql = f"CALL {procedure_name}(ARRAY_CONSTRUCT({placeholders}), ?)"
        params = args + [log_level]
    else:
        sql = f"CALL {procedure_name}(ARRAY_CONSTRUCT({placeholders}))"
        params = args
    df = session.sql(sql, params=params) if params else session.sql(sql)
    async_job = df.collect_nowait()
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

    rows = async_job.result()
    if rows and len(rows[0]) > 0:
        return rows[0][0]
    return None


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
    log_level: str | None = None,
    scala_version: str | None = None,
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
        log_level: Optional log level name (``"DEBUG"``, ``"INFO"``, ...)
            forwarded to the procedure at CALL time. ``None`` lets the
            procedure's ``DEFAULT 'INFO'`` apply (keyword-only).
        scala_version: Optional Scala binary version (``"2.12"`` or
            ``"2.13"``) baked into the generated handler (keyword-only).
            Forwarded to :func:`create_jvm_sproc`. ``None`` keeps the
            sproc body wire-compatible with older ``snowpark-connect``
            releases that lack the ``scala_version`` parameter on
            ``execute_jar``.

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
        scala_version=scala_version,
    )

    resolved_name = procedure_name or f"{class_name.rsplit('.', 1)[-1]}_main"

    return call_sproc(
        procedure_name=resolved_name,
        job_args=job_args,
        poll_interval=poll_interval,
        timeout=timeout,
        block=block,
        log_level=log_level,
    )


# ---------------------------------------------------------------------------
# Python file resolution
# ---------------------------------------------------------------------------
def resolve_py_files(raw_patterns: list[str]) -> list[str]:
    """Expand glob patterns and return deduplicated absolute ``.py`` paths.

    Args:
        raw_patterns: Glob patterns or literal paths to ``.py`` files.

    Returns:
        List of resolved absolute Python file paths.

    Raises:
        FileNotFoundError: If a pattern matches no files.
        ValueError: If a resolved file is not a ``.py`` source file or two
            files share the same basename (Snowflake imports require unique
            filenames).
    """
    py_files: list[str] = []
    for pattern in raw_patterns:
        resolved = glob_mod.glob(pattern)
        if not resolved:
            raise FileNotFoundError(f"No files matched pattern: {pattern}")
        py_files.extend(os.path.abspath(p) for p in resolved)

    for p in py_files:
        if not p.endswith(".py"):
            raise ValueError(
                f"Only .py source files are supported in --py-files (got '{p}')."
            )

    basenames = [os.path.basename(p) for p in py_files]
    seen: set[str] = set()
    for bn in basenames:
        if bn in seen:
            raise ValueError(
                f"Duplicate Python file basename '{bn}' -- "
                "Snowflake imports require unique filenames."
            )
        seen.add(bn)

    return py_files


# ---------------------------------------------------------------------------
# requirements.txt parsing (strict)
# ---------------------------------------------------------------------------
# Strict grammar: 'name' or 'name<op>version' where op in {==, >=, <=, >, <}
# Names follow PEP 503 normalised form: letters, digits, '.', '-', '_'.
_REQ_LINE_RE = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)"
    r"(?:\s*(?P<op>==|>=|<=|>|<)\s*(?P<version>[A-Za-z0-9._+!*-]+))?$"
)


def _parse_requirements_file(path: str) -> list[str]:
    """Parse a ``requirements.txt`` file into Snowflake PACKAGES entries.

    Strict mode (per project policy):

    * Blank lines and ``#`` comments are skipped.
    * Each remaining line must match ``name`` or ``name<op>version`` with
      ``op in {==, >=, <=, >, <}``.
    * Pip directives (``-r``, ``-e``, ``--``), URLs / VCS refs, env markers
      (``;``), extras (``pkg[extra]``), and unsupported operators (``~=``,
      ``!=``, multiple specifiers) raise ``ValueError``.

    Args:
        path: Path to a requirements.txt file.

    Returns:
        Plain strings such as ``"numpy"`` or ``"numpy==1.24.0"`` ready to be
        embedded in the PACKAGES clause.

    Raises:
        FileNotFoundError: If *path* does not exist.
        ValueError: On any unsupported line.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"requirements file not found: {path}")

    entries: list[str] = []
    with open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue

            if line.startswith("-") or line.startswith("--"):
                raise ValueError(
                    f"{path}:{lineno}: pip directives (-r/-e/--*) are not "
                    f"supported: {raw.rstrip()!r}"
                )
            if "://" in line:
                raise ValueError(
                    f"{path}:{lineno}: URL / VCS requirements are not "
                    f"supported: {raw.rstrip()!r}"
                )
            if ";" in line:
                raise ValueError(
                    f"{path}:{lineno}: environment markers are not "
                    f"supported: {raw.rstrip()!r}"
                )
            if "[" in line or "]" in line:
                raise ValueError(
                    f"{path}:{lineno}: extras (pkg[extra]) are not "
                    f"supported: {raw.rstrip()!r}"
                )
            if "," in line:
                raise ValueError(
                    f"{path}:{lineno}: multiple version specifiers are not "
                    f"supported: {raw.rstrip()!r}"
                )
            if "~=" in line or "!=" in line:
                raise ValueError(
                    f"{path}:{lineno}: operators '~=' and '!=' are not "
                    f"supported: {raw.rstrip()!r}"
                )

            m = _REQ_LINE_RE.match(line)
            if not m:
                raise ValueError(
                    f"{path}:{lineno}: cannot parse requirement: " f"{raw.rstrip()!r}"
                )

            name = m.group("name")
            op = m.group("op")
            version = m.group("version")
            entries.append(f"{name}{op}{version}" if op else name)

    return entries


# ---------------------------------------------------------------------------
# SQL generation (Python)
# ---------------------------------------------------------------------------
def _generate_python_sproc_sql(
    procedure_name: str,
    main_module: str,
    py_files: list[str],
    main_module_file: str,
    stage_name: str,
    replace: bool,
    extra_packages: list[str] | None = None,
    snowpark_connect_version: str | None = None,
) -> str:
    """Generate the CREATE PROCEDURE DDL for a Python ``runpy`` wrapper.

    The generated handler:

    * Sets ``SPARK_REMOTE`` to ``sc://127.0.0.1:15002``.
    * Starts the SCOS server via ``start_session`` on TCP port 15002.
    * Sets ``sys.argv`` to ``[main_module] + job_args`` and runs the user
      module with ``runpy.run_module(main_module, run_name="__main__")``.

    No ``threading.Event`` / ``finally`` block is emitted; the server's
    lifecycle ends with the procedure invocation.
    """
    create_keyword = (
        "CREATE OR REPLACE PROCEDURE" if replace else "CREATE PROCEDURE IF NOT EXISTS"
    )

    spc_pkg = (
        f"snowpark-connect=={snowpark_connect_version}"
        if snowpark_connect_version
        else "snowpark-connect"
    )

    package_entries = set([spc_pkg] + list(extra_packages or []))
    packages_list = ", ".join(f"'{p}'" for p in package_entries)

    import_basenames = [os.path.basename(main_module_file)] + [
        os.path.basename(p) for p in py_files
    ]
    imports_list = ", ".join(f"'@{stage_name}/{bn}'" for bn in import_basenames)

    return f"""\
{create_keyword} {procedure_name}(job_args ARRAY, log_level STRING DEFAULT 'INFO')
    RETURNS STRING
    LANGUAGE PYTHON
    RUNTIME_VERSION = '3.11'
    PACKAGES = ({packages_list})
    IMPORTS = ({imports_list})
    HANDLER = 'run'
    EXECUTE AS CALLER
AS $$
import os, sys, runpy, logging
from snowflake.snowpark import Session
from snowflake.snowpark_connect.server import start_session

def run(session: Session, job_args: list, log_level: str = "INFO") -> str:
    logging.basicConfig(level=(log_level or "INFO").upper())
    logger = logging.getLogger(__name__)
    main_module = "{main_module}"
    try:
        os.environ["SPARK_REMOTE"] = "sc://127.0.0.1:15002"
        start_session(
            is_daemon=True,
            tcp_port=15002,
            snowpark_session=session,
        )
        sys.argv = [main_module] + [str(arg) for arg in (job_args or [])]
        runpy.run_module(main_module, run_name="__main__")
    except Exception:
        logger.exception(f"Error running module: {main_module}")
        raise
    return ""
$$;"""


# ---------------------------------------------------------------------------
# Top-level orchestrator (Python)
# ---------------------------------------------------------------------------
def create_python_sproc(
    module_file: str,
    py_files: list[str] | None = None,
    requirements_file: str | None = None,
    procedure_name: str | None = None,
    replace: bool = False,
    dry_run: bool = False,
    snowpark_connect_version: str | None = None,
) -> str:
    """Create a Snowflake stored procedure that runs a Python module.

    The target module is executed via ``runpy.run_module(main, run_name="__main__")``
    after the SCOS server has been started inside the procedure.  The
    procedure accepts a single ``ARRAY`` parameter (``job_args``) which is
    forwarded as ``sys.argv[1:]`` of the running module.

    Args:
        module_file: Path to the main ``.py`` module (its top-level code is
            executed as ``__main__``).
        py_files: Additional ``.py`` files to upload to the procedure's
            IMPORTS directory (Snowflake adds the directory to ``sys.path``
            automatically).
        requirements_file: Optional path to a ``requirements.txt`` parsed
            into the PACKAGES clause (see :func:`_parse_requirements_file`).
        procedure_name: Snowflake procedure name.  Defaults to
            ``<module_basename>_main``.
        replace: Use ``CREATE OR REPLACE PROCEDURE``.
        dry_run: Generate SQL but skip upload and execution.
        snowpark_connect_version: Pin ``snowpark-connect`` to a version.

    Returns:
        The full SQL script: ``CREATE [OR REPLACE] STAGE`` + one ``PUT``
        statement per import file + the ``CREATE PROCEDURE`` DDL, joined
        with blank lines.  This is what ``--dry-run`` prints; in non-dry-run
        mode the equivalent steps are executed via the Snowpark API.

    Raises:
        FileNotFoundError: If *module_file* or *requirements_file* does not exist.
        ValueError: If *module_file* is not a ``.py`` file, or any basename
            collides between *module_file* and *py_files*.
        RuntimeError: Procedure already exists (when *replace* is False).
    """
    if not os.path.isfile(module_file):
        raise FileNotFoundError(f"Python module not found: {module_file}")
    if not module_file.endswith(".py"):
        raise ValueError(
            f"module_file must be a .py source file (got '{module_file}')."
        )

    main_abs = os.path.abspath(module_file)
    main_bn = os.path.basename(main_abs)
    main_module = main_bn[: -len(".py")]

    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", main_module):
        raise ValueError(
            f"Main module basename '{main_module}' is not a valid Python "
            "identifier; runpy.run_module requires names matching "
            "[A-Za-z_][A-Za-z0-9_]*."
        )

    py_file_list: list[str] = list(py_files or [])
    for p in py_file_list:
        if os.path.basename(p) == main_bn:
            raise ValueError(
                f"py_files contains a file with the same basename as the main "
                f"module ('{main_bn}'); Snowflake imports require unique filenames."
            )
    seen = {main_bn}
    for p in py_file_list:
        bn = os.path.basename(p)
        if bn in seen:
            raise ValueError(
                f"Duplicate Python file basename '{bn}' -- "
                "Snowflake imports require unique filenames."
            )
        seen.add(bn)

    extra_packages = (
        _parse_requirements_file(requirements_file) if requirements_file else []
    )

    if not procedure_name:
        procedure_name = f"{main_module}_main"

    if not is_valid_snowflake_identifier(procedure_name):
        raise ValueError(f"{procedure_name} is not a valid Snowflake identifier.")

    stage_name = f"{procedure_name}_dependencies"

    create_sql = _generate_python_sproc_sql(
        procedure_name=procedure_name,
        main_module=main_module,
        py_files=py_file_list,
        main_module_file=main_abs,
        stage_name=stage_name,
        replace=replace,
        extra_packages=extra_packages,
        snowpark_connect_version=snowpark_connect_version,
    )

    import_files = [main_abs] + py_file_list
    stage_setup_sql = _generate_stage_setup_sql(import_files, stage_name, replace)
    full_sql = f"{stage_setup_sql}\n\n{create_sql}"

    if not dry_run:
        create_sproc(create_sql, import_files, stage_name, replace)

    return full_sql


# ---------------------------------------------------------------------------
# End-to-end: create + call (Python)
# ---------------------------------------------------------------------------
def submit_python_workload_to_warehouse(
    module_file: str,
    job_args: list[str] | None = None,
    *,
    py_files: list[str] | None = None,
    requirements_file: str | None = None,
    procedure_name: str | None = None,
    replace: bool = False,
    snowpark_connect_version: str | None = None,
    poll_interval: float = 5.0,
    timeout: float = 300.0,
    block: bool = True,
    log_level: str | None = None,
) -> Any:
    """Create a Python stored procedure and immediately call it.

    Convenience wrapper that combines :func:`create_python_sproc` and
    :func:`call_sproc` into a single call.

    Args:
        module_file: Path to the main ``.py`` module.
        job_args: Arguments forwarded as ``sys.argv[1:]`` to the module.
        py_files: Additional ``.py`` files for IMPORTS (keyword-only).
        requirements_file: Optional ``requirements.txt`` (keyword-only).
        procedure_name: Snowflake procedure name (keyword-only).  Defaults
            to ``<module_basename>_main``.
        replace: Use ``CREATE OR REPLACE PROCEDURE`` (keyword-only).
        snowpark_connect_version: Pin ``snowpark-connect`` to a version.
        poll_interval: Seconds between ``is_done()`` checks.
        timeout: Max seconds to wait.
        block: If True (default), poll until completion.  If False, return
            an ``AsyncJob``.
        log_level: Optional log level name (``"DEBUG"``, ``"INFO"``, ...)
            forwarded to the procedure at CALL time. ``None`` lets the
            procedure's ``DEFAULT 'INFO'`` apply.

    Returns:
        When *block* is True: the procedure's return value (always ``""``).
        When *block* is False: a ``snowflake.snowpark.AsyncJob`` object.
    """
    create_python_sproc(
        module_file=module_file,
        py_files=py_files,
        requirements_file=requirements_file,
        procedure_name=procedure_name,
        replace=replace,
        snowpark_connect_version=snowpark_connect_version,
    )

    main_bn = os.path.basename(module_file)
    main_module = main_bn[: -len(".py")] if main_bn.endswith(".py") else main_bn
    resolved_name = procedure_name or f"{main_module}_main"

    return call_sproc(
        procedure_name=resolved_name,
        job_args=job_args,
        poll_interval=poll_interval,
        timeout=timeout,
        block=block,
        log_level=log_level,
    )
