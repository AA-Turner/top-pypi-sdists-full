"""The managed DuckDB extension baseline: where the pre-installed extensions are, and the settings
applied around them when the kernel's DuckDB is set up."""

import os
import sys
from pathlib import Path
from typing import Optional

# Pre-installed extensions live next to the Python environment that provides duckdb, like the
# pre-installed packages: on SMUS the venv, /sagemaker_packages/.venv -> /sagemaker_packages/duckdb_extensions;
# on an AWS Notebook local kernel the bundled runtime, <app>/dist/python -> <app>/dist/duckdb_extensions.
_DUCKDB_BUNDLE_DIRECTORY_NAME = "duckdb_extensions"
# Extensions loaded eagerly so a missing or mismatched bundle fails at startup, not on the first S3 query.
_DUCKDB_REQUIRED_EXTENSIONS = ("httpfs", "aws")
# Settings user code may still change after the managed configuration is locked.
_DUCKDB_USER_CONFIGS = (
    "threads",
    "memory_limit",
    "temp_directory",
    "max_temp_directory_size",
    "preserve_insertion_order",
    "timezone",
    "default_order",
    "enable_progress_bar",
    "python_scan_all_frames",
    "s3_region",
    # Where unqualified names resolve: what USE sets, and what a SQL cell run in a catalog sets
    # for its duration (duckdbutils); a cell's own USE and SET search_path work as well.
    "search_path",
)


def _duckdb_bundle_directory(duckdb_module) -> Optional[str]:
    """Return the pre-installed extension directory for the loaded duckdb, or None if there is none.

    The folder beside the environment duckdb is installed in: the venv holding it, else the base
    interpreter's prefix. A duckdb the user installed into their own packages (UV_PROJECT_ENVIRONMENT)
    has none: the pre-installed extensions are built for the system duckdb.
    """
    module_file = Path(duckdb_module.__file__).resolve()
    user_environment = os.environ.get("UV_PROJECT_ENVIRONMENT", "").strip()
    for parent in module_file.parents:
        if (parent / "pyvenv.cfg").is_file():
            if user_environment and parent == Path(user_environment).resolve():
                return None
            bundle = parent.parent / _DUCKDB_BUNDLE_DIRECTORY_NAME
            return str(bundle) if bundle.is_dir() else None
    base = Path(sys.base_prefix).resolve()
    if base in module_file.parents:
        bundle = base.parent / _DUCKDB_BUNDLE_DIRECTORY_NAME
        return str(bundle) if bundle.is_dir() else None
    return None


def _apply_baseline(duckdb, extension_directory: str) -> None:
    """Point ``duckdb`` at the bundle (and the user's folder) and load the required extensions.

    Must run before any extension loads.
    """
    # Where user INSTALLs land: next to the user venv, like the user's own packages
    # (UV_PROJECT is the user packages project). DuckDB's default otherwise.
    user_project = os.environ.get("UV_PROJECT", "").strip()
    user_extension_directory = (
        os.path.join(user_project, _DUCKDB_BUNDLE_DIRECTORY_NAME)
        if user_project
        else os.path.join(os.path.expanduser("~"), ".duckdb", "extensions")
    )
    # User dir first: DuckDB installs into the first entry and, when an extension is in both,
    # loads it from the last, so a user install never shadows the bundle.
    duckdb.execute(
        "SET extension_directories = ?", [[user_extension_directory, extension_directory]]
    )
    duckdb.sql("SET autoinstall_known_extensions = false;")
    for extension in _DUCKDB_REQUIRED_EXTENSIONS:
        duckdb.sql(f"LOAD {extension};")


def _lock_configuration(duckdb) -> None:
    """Lock the managed configuration, leaving the settings user code may still change."""
    duckdb.execute("SET allowed_configs = ?", [list(_DUCKDB_USER_CONFIGS)])
    duckdb.sql("SET lock_configuration = true;")
