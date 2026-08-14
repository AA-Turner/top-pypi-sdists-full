#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from snowflake import snowpark
from snowflake.snowpark_connect.config import global_config, is_native_app_mode
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.spark_session_cache import get_spark_session_cache


def _is_absolute_stage_path(entry: str) -> bool:
    return entry.startswith("@") or entry.startswith("snow://")


def _rewrite_to_version_stage_relative(entry: str) -> str:
    """Rewrite an absolute stage import to a version-stage-relative path, preserving the
    path *within* the stage (``@stg/a/b/f.jar`` -> ``/a/b/f.jar``) so a nested bundle layout
    survives. Passes ``/...`` and bare names through. A versioned schema only allows IMPORTS
    relative to the version stage root."""
    if entry.startswith("/") or not _is_absolute_stage_path(entry):
        return entry
    if entry.startswith("@"):
        # Drop the stage locator (@stg, @db.schema.stg, @~) up to the first '/'; keep the rest.
        parts = entry.split("/", 1)
        path_within = parts[1] if len(parts) > 1 else parts[0].lstrip("@")
    else:  # snow:// — locator structure varies; fall back to basename
        path_within = entry.rstrip("/").split("/")[-1]
    rewritten = "/" + path_within
    logger.warning(
        "native_app_mode: rewrote absolute import %r to %r; bundle it at that version-stage "
        "path or set snowpark.connect.udf.python.version_stage_imports.",
        entry,
        rewritten,
    )
    return rewritten


def _python_version_stage_imports() -> list[str]:
    """Explicit ``snowpark.connect.udf.python.version_stage_imports`` escape hatch,
    validated ``startswith('/')`` (mirrors ``jvm_udf_utils.build_udxf_imports``)."""
    raw = global_config.get("snowpark.connect.udf.python.version_stage_imports", "")
    entries = (
        [x.strip() for x in raw.strip("[] ").split(",") if x.strip()] if raw else []
    )
    invalid = [e for e in entries if not e.startswith("/")]
    if invalid:
        exception = ValueError(
            f"snowpark.connect.udf.python.version_stage_imports contains invalid paths: {invalid}. "
            "All must be version-stage-relative paths starting with '/'."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
        raise exception
    return entries


def get_python_udxf_import_files(session: snowpark.Session) -> str:
    config_imports = global_config.get(
        "snowpark.connect.udf.python.imports",
        global_config.get("snowpark.connect.udf.imports", ""),
    )
    config_imports = (
        [x.strip() for x in config_imports.strip("[] ").split(",") if x.strip()]
        if config_imports
        else []
    )
    artifacts_store = get_spark_session_cache().artifacts_store
    imports = {
        *artifacts_store.get_python_files(),
        *artifacts_store.get_import_files(),
        *config_imports,
    }

    if not is_native_app_mode():
        return ",".join([file for file in imports if file])

    # Versioned schema rejects absolute-stage IMPORTS (093023): rewrite to version-stage
    # relative, then add the explicit escape-hatch imports.
    by_rewritten: dict[str, set[str]] = {}
    for original in (f for f in imports if f):
        by_rewritten.setdefault(
            _rewrite_to_version_stage_relative(original), set()
        ).add(original)
    for rewritten_path, originals in by_rewritten.items():
        if len(originals) > 1:  # distinct paths, same basename -> collide at the root
            logger.warning(
                "native_app_mode: imports %s all map to %r.",
                sorted(originals),
                rewritten_path,
            )
    result = set(by_rewritten)
    result.update(_python_version_stage_imports())
    return ",".join([file for file in result if file])
