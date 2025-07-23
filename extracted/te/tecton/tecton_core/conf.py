import contextlib
import json
import logging
import os
import pathlib
import sys
import threading
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union

import boto3

from tecton_core import errors


logging.getLogger("boto3").setLevel(logging.ERROR)
logging.getLogger("botocore").setLevel(logging.ERROR)

_ConfigSettings = Dict[str, Any]

_CONFIG_OVERRIDES: _ConfigSettings = {}


class RepoConfig:
    def __init__(self, config: Optional[_ConfigSettings] = None) -> None:
        self.config = config or {}

    def __getitem__(self, item: str) -> Union[str, bool]:
        return self.config[item]

    def get(self, key: str) -> Union[str, bool]:
        if key.startswith("TECTON_"):
            # yaml-format the key by stripping TECTON_ and making lower-case.
            key = key.lower()[len("TECTON_") :]
        return self.config.get(key)

    def set_all(self, config: _ConfigSettings) -> None:
        self.config = config


REPO_CONFIG = RepoConfig()


class ConfSource(Enum):
    # (Always supported) This key can be overriden in the Python runtime.
    SESSION_OVERRIDE = 1
    # (Always supported) This key can be read from the local environment.
    OS_ENV = 2
    # This key can be written to and read from the tecton config file.
    LOCAL_TECTON_CONFIG = 3
    # This key can be written to and read from the tecton tokens file.
    LOCAL_TECTON_TOKENS = 4
    # Configuration loaded from repo.yaml
    REPO_CONFIG = 5
    # This key can read from the MDS get-configs endpoint. Note that this will not return anything until after the
    # first MDS RPC is made, which is racy because e.g. @sdk_public_method makes asynchronous MDS calls.

    # BLOCKING_REMOTE_MDS_CONFIG is not racy, but can't be used everywhere without causing MDS requests to happen during
    # initialization. We can clean up this whole mess when confs from secret managers are explicit and AWS_REGION is no
    # longer required.
    REMOTE_MDS_CONFIG = 6
    # Like REMOTE_MDS_CONFIG, but blocks until the initial configuration RPC from MDS is complete.
    BLOCKING_REMOTE_MDS_CONFIG = 7
    # This key can read from the Databricks secrets manager.
    DATABRICKS_SECRET = 8
    # This key can read from the AWS secrets manager.
    AWS_SECRET_MANAGER = 9
    # The default value of this key was used. Used for debug printing. Not an "allowable" source.
    DEFAULT = 10
    # A value for this key was not found. Used for debug printing. Not an "allowable" source.
    NOT_FOUND = 11


RUNTIME_ALLOWED_SOURCES = (ConfSource.SESSION_OVERRIDE, ConfSource.OS_ENV)
DEFAULT_ALLOWED_SOURCES = (
    ConfSource.SESSION_OVERRIDE,
    ConfSource.OS_ENV,
    ConfSource.REMOTE_MDS_CONFIG,
    ConfSource.DATABRICKS_SECRET,
    ConfSource.AWS_SECRET_MANAGER,
)


class _Debugger(object):
    @classmethod
    def _debug_enabled(cls) -> bool:
        debug_value = _get_runtime_only("TECTON_DEBUG")
        return debug_value is not None and debug_value.lower() in ("1", "true", "yes")

    @classmethod
    def preamble(cls, key: str) -> None:
        if cls._debug_enabled():
            print(f"Looking up {key}", file=sys.stderr)

    @classmethod
    def print(cls, src: ConfSource, key: str, val: Optional[str] = None, details: Optional[str] = None) -> None:
        if not cls._debug_enabled():
            return

        if src == ConfSource.NOT_FOUND:
            print(f"Unable to find {key}\n", file=sys.stderr)
            return

        details_str = f"({details})" if details else ""
        val_str = val if val is not None else "not found"
        symbol_str = "[x]" if val is not None else "[ ]"
        print(symbol_str, f"{key} in {src.name} -> {val_str}", details_str, file=sys.stderr)


def set(key: str, value: str) -> None:
    _set(key, value)


def unset(key: str) -> None:
    del _CONFIG_OVERRIDES[key]


def _set(key: str, value: str) -> None:
    _CONFIG_OVERRIDES[key] = value


@contextlib.contextmanager
def _temporary_set(key: str, value: str) -> Iterator[None]:
    curr_val = _CONFIG_OVERRIDES.get(key)
    _CONFIG_OVERRIDES[key] = value
    try:
        yield
    finally:
        if curr_val:
            _CONFIG_OVERRIDES[key] = curr_val
        else:
            del _CONFIG_OVERRIDES[key]


def _does_key_have_valid_prefix(key: str) -> bool:
    for prefix in _VALID_KEY_PREFIXES:
        if key.startswith(prefix):
            return True
    return False


def _get(key: str) -> Optional[str]:
    """Get the config value for the given key, or return None if not found."""
    _Debugger.preamble(key)

    if key in _VALID_KEYS_TO_ALLOWED_SOURCES:
        allowed_sources = _VALID_KEYS_TO_ALLOWED_SOURCES[key]
    elif _does_key_have_valid_prefix(key):
        allowed_sources = DEFAULT_ALLOWED_SOURCES
    else:
        msg = f"Tried accessing invalid configuration key '{key}'"
        raise errors.TectonInternalError(msg)

    # Session-scoped override.
    if ConfSource.SESSION_OVERRIDE in allowed_sources:
        val = _CONFIG_OVERRIDES.get(key)
        _Debugger.print(ConfSource.SESSION_OVERRIDE, key, val)
        if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
            return val

    # Environment variable.
    if ConfSource.OS_ENV in allowed_sources:
        val = os.environ.get(key)
        _Debugger.print(ConfSource.OS_ENV, key, val)
        if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
            return val

    # ~/.tecton/config
    if ConfSource.LOCAL_TECTON_CONFIG in allowed_sources:
        val = _LOCAL_TECTON_CONFIG.get(key)
        _Debugger.print(ConfSource.LOCAL_TECTON_CONFIG, key, val, details=str(_LOCAL_TECTON_CONFIG_FILE))
        if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
            return val

    # ~/.tecton/config.tokens
    if ConfSource.LOCAL_TECTON_TOKENS in allowed_sources:
        val = _LOCAL_TECTON_TOKENS.get(key)
        _Debugger.print(ConfSource.LOCAL_TECTON_TOKENS, key, val, details=str(_LOCAL_TECTON_TOKENS_FILE))
        if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
            return val

    # repo.yaml in repository. Loaded by CLI.
    if ConfSource.REPO_CONFIG in allowed_sources:
        val = REPO_CONFIG.get(key)
        _Debugger.print(ConfSource.REPO_CONFIG, key, val, details=str(REPO_CONFIG.config))
        if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
            return val

    if ConfSource.BLOCKING_REMOTE_MDS_CONFIG in allowed_sources:
        _force_initialize_mds_config(timeout_seconds=2.0)

    # Config from MDS
    if ConfSource.REMOTE_MDS_CONFIG in allowed_sources or ConfSource.BLOCKING_REMOTE_MDS_CONFIG in allowed_sources:
        with _mds_config_lock:
            val = _remote_mds_configs.get(key)
        _Debugger.print(ConfSource.REMOTE_MDS_CONFIG, key, val)
        if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
            return val

    if _get_runtime_env() == TectonEnv.UNKNOWN:
        # Fallback attempt to set env if user has not set it.
        _set_tecton_runtime_env()

    # NOTE: although originally intended for internal use. Some customers have
    # found this configuration or have required this behavior. Care should be
    # exercised in changing any behavior here to ensure no customer breakages.
    if ConfSource.DATABRICKS_SECRET in allowed_sources and not _get_runtime_only("TECTON_CONF_DISABLE_DBUTILS"):
        # Databricks secrets
        for scope in _get_secret_scopes():
            value = _get_from_db_secrets(key, scope)
            _Debugger.print(ConfSource.DATABRICKS_SECRET, key, value, details=f"{scope}:{key}")
            if value is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
                return value

    # NOTE: although originally intended for internal use. Some customers have
    # found this configuration or have required this behavior. Care should be
    # exercised in changing any behavior here to ensure no customer breakages.
    if ConfSource.AWS_SECRET_MANAGER in allowed_sources and not _get_runtime_only("TECTON_CONF_DISABLE_AWS_SECRETS"):
        # AWS secret manager
        for scope in _get_secret_scopes():
            value = _get_from_secretsmanager(key, scope)
            if value is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
                return value

    if key in _DEFAULTS:
        value = _DEFAULTS[key]()
        _Debugger.print(ConfSource.DEFAULT, key, value)
        return value

    _Debugger.print(ConfSource.NOT_FOUND, key)
    return None


def _get_runtime_only(key: str, use_defaults: bool = True) -> Optional[str]:
    """An alternate _get() that will look up only from runtime sources. Used to avoid infinite loops or network calls

    Args:
        key: The configuration key to look up
        use_defaults: If True, returns default values when no user setting exists.
                     If False, returns None when no user setting exists.
    """
    if key not in _VALID_KEYS_TO_ALLOWED_SOURCES:
        msg = f"_get_runtime_only should only used with valid keys. {key}"
        raise errors.TectonInternalError(msg)

    # Session-scoped override.
    val = _CONFIG_OVERRIDES.get(key)
    if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
        return val

    # Environment variable.
    val = os.environ.get(key)
    if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
        return val

    if use_defaults and key in _DEFAULTS:
        value = _DEFAULTS[key]()
        return value

    return None


def is_runtime_set(key: str) -> bool:
    """Check if a config was set during runtime (through conf.set or envvar).

    Args:
        key: The configuration key to check

    Returns:
        True if the config was manually set by user, False otherwise.
    """
    if key not in _VALID_KEYS_TO_ALLOWED_SOURCES:
        msg = f"_is_runtime_set should only used with valid keys. {key}"
        raise errors.TectonInternalError(msg)

    if _CONFIG_OVERRIDES.get(key) is not None:
        return True

    if os.environ.get(key) is not None:
        return True

    return False


def get_or_none(key: str) -> Optional[str]:
    return _get(key)


def get_or_raise(key: str) -> str:
    val = _get(key)
    if val is None:
        msg = f"{key} not set"
        raise errors.TectonInternalError(msg)
    return val


def get_bool(key: str) -> bool:
    val = _get(key)
    if val is None:
        return False
    # bit of a hack for if people set a boolean value in a local override
    if isinstance(val, bool):
        return val
    if isinstance(val, int):
        if val in {0, 1}:
            return bool(val)
        else:
            msg = f"{key} should be 0 or 1, not {val}"
            raise ValueError(msg)
    if not isinstance(val, str):
        msg = f"{key} should be an instance of str, not {type(val)}"
        raise ValueError(msg)
    if val.lower() in {"yes", "true", "1"}:
        return True
    if val.lower() in {"no", "false", "0"}:
        return False
    msg = f"{key} should be 'true', 'false', '1', or '0', not {val}"
    raise ValueError(msg)


def get_float_or_none(key: str) -> Optional[float]:
    """Return value and ensure float type. Returns None if None."""
    val = _get(key)
    if val is None:
        return None
    else:
        return float(val)


def _model_cache_directory() -> str:
    base_cache_dir = os.environ.get("XDG_CACHE_HOME", str(pathlib.Path.home() / ".cache"))
    return os.path.join(base_cache_dir, "tecton", "models")


# Internal

_LOCAL_TECTON_CONFIG_FILE = Path(os.environ.get("TECTON_CONFIG_PATH", Path.home() / ".tecton/config"))
_LOCAL_TECTON_TOKENS_FILE = _LOCAL_TECTON_CONFIG_FILE.with_suffix(".tokens")


# NOTE: For 'FeatureFlags', i.e. Yes/No switches to enable behavior still in development, add a new FeatureFlag object
# at bottom of file, do NOT add it here directly.
_VALID_KEYS_TO_ALLOWED_SOURCES = {
    "API_SERVICE": (*DEFAULT_ALLOWED_SOURCES, ConfSource.LOCAL_TECTON_CONFIG),
    "FEATURE_SERVICE": (*DEFAULT_ALLOWED_SOURCES, ConfSource.LOCAL_TECTON_CONFIG),
    "INGESTION_SERVICE": (
        ConfSource.SESSION_OVERRIDE,
        ConfSource.OS_ENV,
        ConfSource.BLOCKING_REMOTE_MDS_CONFIG,
    ),
    "CLI_CLIENT_ID": (*DEFAULT_ALLOWED_SOURCES, ConfSource.LOCAL_TECTON_CONFIG),
    "TECTON_WORKSPACE": (*DEFAULT_ALLOWED_SOURCES, ConfSource.LOCAL_TECTON_CONFIG),
    "TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE": (
        ConfSource.SESSION_OVERRIDE,
        ConfSource.OS_ENV,
        ConfSource.BLOCKING_REMOTE_MDS_CONFIG,
    ),
    "TECTON_BATCH_COMPUTE_MODE": (
        ConfSource.SESSION_OVERRIDE,
        ConfSource.OS_ENV,
        ConfSource.BLOCKING_REMOTE_MDS_CONFIG,
    ),
    "OAUTH_ACCESS_TOKEN": (*RUNTIME_ALLOWED_SOURCES, ConfSource.LOCAL_TECTON_TOKENS),
    "OAUTH_ACCESS_TOKEN_EXPIRATION": (*RUNTIME_ALLOWED_SOURCES, ConfSource.LOCAL_TECTON_TOKENS),
    "OAUTH_REFRESH_TOKEN": (*RUNTIME_ALLOWED_SOURCES, ConfSource.LOCAL_TECTON_TOKENS),
    # TECTON_CLUSTER_NAME is needed for looking up AWS and Databricks secrets. CLUSTER_REGION is used for looking up AWS
    # secrets. To avoid an infinite loop, these keys cannot be looked up from those sources.
    "TECTON_CLUSTER_NAME": (
        ConfSource.SESSION_OVERRIDE,
        ConfSource.OS_ENV,
        ConfSource.REMOTE_MDS_CONFIG,
    ),
    "CLUSTER_REGION": (
        ConfSource.SESSION_OVERRIDE,
        ConfSource.OS_ENV,
        ConfSource.REMOTE_MDS_CONFIG,
        ConfSource.DATABRICKS_SECRET,
    ),
    # NOTE: TECTON_CONF* are meant for Tecton internal use.
    # TODO(TEC-8744): improve tecton.conf configurations such that end users have more
    # control of where secrets are fetched from.
    "SPARK_REDSHIFT_TEMP_DIR": RUNTIME_ALLOWED_SOURCES,
    "TECTON_CONF_DISABLE_DBUTILS": RUNTIME_ALLOWED_SOURCES,
    "TECTON_CONF_DISABLE_AWS_SECRETS": RUNTIME_ALLOWED_SOURCES,
    "TECTON_DEBUG": RUNTIME_ALLOWED_SOURCES,
    "TECTON_RUNTIME_ENV": RUNTIME_ALLOWED_SOURCES,
    "TECTON_RUNTIME_MODE": RUNTIME_ALLOWED_SOURCES,
    "TECTON_SKIP_OBJECT_VALIDATION": RUNTIME_ALLOWED_SOURCES,
    # TECTON_FORCE_FUNCTION_SERIALIZATION is a parameter used by some users in unit testing. Replacing or making changes
    # to the semantics of this flag will require upgrade/migration guidance. However, this is not a "public/stable"
    # flag, so feel free to make changes as long as there is an upgrade path.
    "TECTON_FORCE_FUNCTION_SERIALIZATION": RUNTIME_ALLOWED_SOURCES,
    "TECTON_REPO_IGNORE_ALL_HIDDEN_DIRS": RUNTIME_ALLOWED_SOURCES,
    "SKIP_OBJECT_VERSION_CHECK": RUNTIME_ALLOWED_SOURCES,
    "USE_BQ_STORAGE_API": RUNTIME_ALLOWED_SOURCES,
    "DUCKDB_DEBUG": RUNTIME_ALLOWED_SOURCES,
    "DUCKDB_BENCHMARK": RUNTIME_ALLOWED_SOURCES,
    "DUCKDB_PERSIST_DB": RUNTIME_ALLOWED_SOURCES,
    "DUCKDB_MEMORY_LIMIT": RUNTIME_ALLOWED_SOURCES,
    "DUCKDB_NTHREADS": RUNTIME_ALLOWED_SOURCES,
    "DUCKDB_EXTENSION_REPO": RUNTIME_ALLOWED_SOURCES,
    "DUCKDB_ALLOW_CACHE_EXTENSION": RUNTIME_ALLOWED_SOURCES,
    "ATHENA_S3_PATH": DEFAULT_ALLOWED_SOURCES,
    "ATHENA_DATABASE": DEFAULT_ALLOWED_SOURCES,
    "ENABLE_TEMPO": DEFAULT_ALLOWED_SOURCES,
    "QUERY_REWRITE_ENABLED": DEFAULT_ALLOWED_SOURCES,
    "AWS_ACCESS_KEY_ID": DEFAULT_ALLOWED_SOURCES,
    "AWS_SECRET_ACCESS_KEY": DEFAULT_ALLOWED_SOURCES,
    "AWS_SESSION_TOKEN": DEFAULT_ALLOWED_SOURCES,
    "HIVE_METASTORE_HOST": DEFAULT_ALLOWED_SOURCES,
    "HIVE_METASTORE_PORT": DEFAULT_ALLOWED_SOURCES,
    "HIVE_METASTORE_USERNAME": DEFAULT_ALLOWED_SOURCES,
    "HIVE_METASTORE_DATABASE": DEFAULT_ALLOWED_SOURCES,
    "HIVE_METASTORE_PASSWORD": DEFAULT_ALLOWED_SOURCES,
    "SPARK_DRIVER_LOCAL_IP": DEFAULT_ALLOWED_SOURCES,
    "METADATA_SERVICE": DEFAULT_ALLOWED_SOURCES,
    "TECTON_API_KEY": DEFAULT_ALLOWED_SOURCES,
    "QUERYTREE_SHORT_SQL_ENABLED": RUNTIME_ALLOWED_SOURCES,
    "QUERYTREE_SHORT_SQL_TYPE": RUNTIME_ALLOWED_SOURCES,
    "REDSHIFT_USER": DEFAULT_ALLOWED_SOURCES,
    "REDSHIFT_PASSWORD": DEFAULT_ALLOWED_SOURCES,
    "SKIP_FEATURE_TIMESTAMP_VALIDATION": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_ACCOUNT_IDENTIFIER": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_DEBUG": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_USER": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_PASSWORD": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_PRIVATE_KEY": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_PRIVATE_KEY_PASSPHRASE": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_WAREHOUSE": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_DATABASE": DEFAULT_ALLOWED_SOURCES,
    "USE_DEPRECATED_ATHENA_RETRIEVAL": RUNTIME_ALLOWED_SOURCES,
    # Instead of the querytree code path, use the old snowflake ghf implementation
    "REDIS_AUTH_TOKEN": DEFAULT_ALLOWED_SOURCES,
    "TECTON_PYTHON_ODFV_OUTPUT_SCHEMA_CHECK_ENABLED": RUNTIME_ALLOWED_SOURCES,
    "USE_LOCAL_OFFLINE_STORE_CREDENTIALS": DEFAULT_ALLOWED_SOURCES,
    "SKIP_REPO_CONFIG_INIT": DEFAULT_ALLOWED_SOURCES,  # Used by itests only
    "DUCKDB_DISK_SPILLING_ENABLED": DEFAULT_ALLOWED_SOURCES,
    "MODEL_CACHE_DIRECTORY": RUNTIME_ALLOWED_SOURCES,
    "DUCKDB_ENABLE_OPTIMIZED_FULL_AGG": DEFAULT_ALLOWED_SOURCES,
    "DUCKDB_OPTIMIZED_FULL_AGG_MAX_EXPLODE": DEFAULT_ALLOWED_SOURCES,
    "ALLOW_NULL_FEATURES": DEFAULT_ALLOWED_SOURCES,
    "DUCKDB_SPINE_SPLIT_COUNT": DEFAULT_ALLOWED_SOURCES,
    "DUCKDB_SPINE_SPLIT_STRATEGY": DEFAULT_ALLOWED_SOURCES,
    "DUCKDB_ENABLE_RANGE_SPLIT": DEFAULT_ALLOWED_SOURCES,
    "DUCKDB_RANGE_SPLIT_COUNT": DEFAULT_ALLOWED_SOURCES,
    "DUCKDB_HTTP_RETRIES": DEFAULT_ALLOWED_SOURCES,
    "DUCKDB_USE_PYARROW_FILESYSTEM": DEFAULT_ALLOWED_SOURCES,
    # Parameter passed to DuckDB.fetch_arrow_reader. It controls the size of pyarrow.RecordBatches produced by DuckDB
    "DUCKDB_BATCH_SIZE": DEFAULT_ALLOWED_SOURCES,
    "PARQUET_MAX_ROWS_PER_FILE": DEFAULT_ALLOWED_SOURCES,
    "PARQUET_MAX_ROWS_PER_GROUP": DEFAULT_ALLOWED_SOURCES,
    # Whether to read the offline store directly into duckdb, otherwise uses Arrow reader
    "DUCKDB_OFFLINE_STORE_READ": RUNTIME_ALLOWED_SOURCES,
    "DUCKDB_FILE_DATA_SOURCE_READ_PARALLEL_FRAGMENTS": RUNTIME_ALLOWED_SOURCES,
    "USE_ARROW_TYPES_IN_PANDAS_TRANSFORMATION": RUNTIME_ALLOWED_SOURCES,
    "DELTA_OFFLINE_STORE_RANGE_PARTITION_ENABLED": RUNTIME_ALLOWED_SOURCES,
    "DELTA_OFFLINE_STORE_RANGE_PARTITION_NUMBER": RUNTIME_ALLOWED_SOURCES,
    # How many samples will be taken to generate partition boundaries
    "DELTA_OFFLINE_STORE_RANGE_SAMPLE_NUMBER": RUNTIME_ALLOWED_SOURCES,
    # Whether to suppress warnings during `tecton test`
    "TECTON_SUPPRESS_TEST_WARNINGS": RUNTIME_ALLOWED_SOURCES,
}

_VALID_KEY_PREFIXES = ["SECRET_"]

_DEFAULTS = {
    "TECTON_WORKSPACE": (lambda: "prod"),
    "FEATURE_SERVICE": (lambda: _get("API_SERVICE")),
    "ENABLE_TEMPO": (lambda: "false"),
    "QUERY_REWRITE_ENABLED": (lambda: "true"),
    "TECTON_REPO_IGNORE_ALL_HIDDEN_DIRS": (lambda: "true"),
    "QUERYTREE_SHORT_SQL_TYPE": (lambda: "table"),
    "DUCKDB_EXTENSION_REPO": (
        lambda: "http://s3.us-west-2.amazonaws.com/tecton.ai.public/duckdb/tecton-extension/{version}"
    ),
    "TECTON_PYTHON_ODFV_OUTPUT_SCHEMA_CHECK_ENABLED": (lambda: "true"),
    "DUCKDB_DISK_SPILLING_ENABLED": (lambda: "true"),
    "MODEL_CACHE_DIRECTORY": (lambda: _model_cache_directory()),
    "TECTON_SKIP_OBJECT_VALIDATION": (lambda: "false"),
    "ALLOW_NULL_FEATURES": (lambda: "true"),
    "DUCKDB_SPINE_SPLIT_COUNT": (lambda: "5"),
    "DUCKDB_SPINE_SPLIT_STRATEGY": (lambda: "even"),
    "DUCKDB_ENABLE_RANGE_SPLIT": (lambda: "false"),
    "DUCKDB_RANGE_SPLIT_COUNT": (lambda: "5"),
    "DUCKDB_HTTP_RETRIES": (lambda: "10"),
    "DUCKDB_USE_PYARROW_FILESYSTEM": (lambda: "true"),
    "USE_BQ_STORAGE_API": (lambda: "true"),
    "DUCKDB_BATCH_SIZE": (lambda: "10000000"),
    "PARQUET_MAX_ROWS_PER_FILE": (lambda: "8000000"),
    "PARQUET_MAX_ROWS_PER_GROUP": (lambda: "1000000"),
    "DUCKDB_OFFLINE_STORE_READ": (lambda: "true"),
    "DUCKDB_FILE_DATA_SOURCE_READ_PARALLEL_FRAGMENTS": (lambda: "256"),
    "USE_ARROW_TYPES_IN_PANDAS_TRANSFORMATION": (lambda: "false"),
    "DELTA_OFFLINE_STORE_RANGE_PARTITION_ENABLED": (lambda: "false"),
    "DELTA_OFFLINE_STORE_RANGE_PARTITION_NUMBER": (lambda: "100"),
    "DELTA_OFFLINE_STORE_RANGE_SAMPLE_NUMBER": (lambda: "10"),
}

_mds_config_lock = threading.Lock()
_remote_mds_configs: _ConfigSettings = {}

_is_interactive_notebook = None

_is_running_on_databricks_cache = None
_is_running_on_emr_cache = None
TectonEnv = Enum("TectonEnv", "DATABRICKS EMR UNKNOWN")

save_tecton_configs_enabled = False  # only save configs for CLI


def _is_running_on_databricks() -> bool:
    """Whether we're running in Databricks notebook or not."""
    global _is_running_on_databricks_cache
    if _is_running_on_databricks_cache is None:
        main = __import__("__main__")
        filename = os.path.basename(getattr(main, "__file__", ""))
        is_python_shell = filename == "PythonShell.py"
        is_databricks_env = "DBUtils" in main.__dict__
        _is_running_on_databricks_cache = is_python_shell and is_databricks_env
    return _is_running_on_databricks_cache


def _is_running_on_emr() -> bool:
    """Whether we're running in EMR notebook or not."""
    global _is_running_on_emr_cache
    if _is_running_on_emr_cache is None:
        _is_running_on_emr_cache = "EMR_CLUSTER_ID" in os.environ
    return _is_running_on_emr_cache


def _set_tecton_runtime_env():
    key = "TECTON_RUNTIME_ENV"
    if _is_running_on_databricks():
        set(key, "DATABRICKS")
    elif _is_running_on_emr():
        set(key, "EMR")
    else:
        set(key, "UNKNOWN")


def _is_mode_materialization() -> bool:
    runtime_mode = get_or_none("TECTON_RUNTIME_MODE")
    return runtime_mode == "MATERIALIZATION"


def _get_runtime_env() -> TectonEnv:
    # Use _get_runtime_only() and not _get() to avoid an infinite loop.
    runtime_env = _get_runtime_only("TECTON_RUNTIME_ENV")
    if runtime_env == "DATABRICKS":
        return TectonEnv.DATABRICKS
    elif runtime_env == "EMR":
        return TectonEnv.EMR
    else:
        return TectonEnv.UNKNOWN


def _get_dbutils():
    # Returns dbutils import. Only works in Databricks notebook environment
    import IPython

    return IPython.get_ipython().user_ns["dbutils"]


def enable_save_tecton_configs() -> None:
    global save_tecton_configs_enabled
    save_tecton_configs_enabled = True


def _get_keys_with_allowed_source(source: ConfSource) -> List[str]:
    """Returns all the keys that have the allowed ConfSource."""
    return [key for key, allowed_sources in _VALID_KEYS_TO_ALLOWED_SOURCES.items() if source in allowed_sources]


def save_tecton_configs() -> None:
    _save_tecton_config(_LOCAL_TECTON_CONFIG_FILE, _get_keys_with_allowed_source(ConfSource.LOCAL_TECTON_CONFIG))


def _save_tecton_config(path: Path, keys: Iterable[str]) -> None:
    tecton_config = {key: get_or_none(key) for key in keys if get_or_none(key) is not None}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(tecton_config, f, sort_keys=True, indent=2)
        f.write("\n")


def _delete_tecton_config(path: Path) -> None:
    try:
        os.remove(path)
    except Exception:
        pass


# Get key by looking in TECTON_CLUSTER_NAME'd scope and falling back to "tecton"
def _get_secret_scopes() -> List[str]:
    cluster_name = get_or_none("TECTON_CLUSTER_NAME")
    secret_scopes = []
    if cluster_name:
        secret_prefix = cluster_name if cluster_name.startswith("tecton-") else f"tecton-{cluster_name}"
        secret_scopes.append(secret_prefix)
    secret_scopes.append("tecton")
    return secret_scopes


# Initializing boto3 clients is expensive and not thread-safe (thanks boto3)
# The lru_cache decorator ensures the client is initialized only once and in thread-safe way
@lru_cache()
def _get_secretsmanager_client():
    if _is_mode_materialization():
        region_name = None
    else:
        region_name = get_or_none("CLUSTER_REGION")
    return boto3.client("secretsmanager", region_name=region_name)


def _get_from_secretsmanager(key: str, scope: str) -> Optional[str]:
    try:
        # Try to Grab secret from AWS secrets manager
        aws_secret_client = _get_secretsmanager_client()

        secret = aws_secret_client.get_secret_value(SecretId=f"{scope}/{key}")
        value = secret["SecretString"]
        _Debugger.print(ConfSource.AWS_SECRET_MANAGER, key, value, details=f"{scope}/{key}")
        return value
    except Exception as e:
        # If it's not found, just return None and don't give verbose error details. boto3 is garbage so the only way
        # to detect this is by looking at the type name.
        exception_name = type(e).__name__
        if exception_name == "ResourceNotFoundException":
            _Debugger.print(ConfSource.AWS_SECRET_MANAGER, key, details=f"{scope}/{key}")
        else:
            _Debugger.print(
                ConfSource.AWS_SECRET_MANAGER,
                key,
                details=f"Failed to retrieve secret {scope}/{key}: {exception_name}: {e}",
            )
        return None


def _get_from_db_secrets(key: str, scope: str) -> Optional[str]:
    try:
        dbutils = _get_dbutils()
        return dbutils.secrets.get(scope, key)
    except Exception:
        return None


def set_login_configs(
    cli_client_id: str,
    api_service: str,
    feature_service: str,
) -> None:
    (set("CLI_CLIENT_ID", cli_client_id),)
    set("API_SERVICE", api_service)
    set("FEATURE_SERVICE", feature_service)

    if save_tecton_configs_enabled:
        # For notebook environments, don't save the configs and tokens because notebooks
        # attached to the same cluster share a filesystem.
        save_tecton_configs()


def set_okta_tokens(access_token, access_token_expiration, refresh_token=None):
    set("OAUTH_ACCESS_TOKEN", access_token)
    set("OAUTH_ACCESS_TOKEN_EXPIRATION", access_token_expiration)
    if refresh_token:
        set("OAUTH_REFRESH_TOKEN", refresh_token)

    if save_tecton_configs_enabled:
        # For notebook environments, don't save the configs and tokens because notebooks
        # attached to the same cluster share a filesystem.
        save_okta_tokens()


def save_okta_tokens():
    _save_tecton_config(_LOCAL_TECTON_TOKENS_FILE, _get_keys_with_allowed_source(ConfSource.LOCAL_TECTON_TOKENS))


def delete_okta_tokens():
    for key in (
        "OAUTH_ACCESS_TOKEN",
        "OAUTH_REFRESH_TOKEN",
        "OAUTH_ACCESS_TOKEN_EXPIRATION",
    ):
        try:
            unset(key)
        except KeyError:
            pass
    _delete_tecton_config(_LOCAL_TECTON_TOKENS_FILE)


def _read_json_config(file_path: Path) -> _ConfigSettings:
    """If the file exists, reads it and returns parsed JSON. Otherwise returns empty dictionary."""
    if not file_path.exists():
        return {}
    content = file_path.read_text()
    if not content:
        return {}
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError as e:
        raise ValueError(
            f"Unable to decode JSON configuration file {file_path} ({str(e)}). "
            + "To regenerate configuration, delete this file and run `tecton login`."
        )


def validate_api_service_url(url: str) -> None:
    """Validate Tecton API URL.
    Returns nothing for valid URLs or raises an error."""
    if "localhost" in url or "ingress" in url:
        return
    if not url.endswith("/api"):
        msg = f'Tecton API URL ("{url}") should be formatted "https://<deployment>.tecton.ai/api"'
        raise errors.TectonAPIValidationError(msg)


def tecton_url() -> str:
    api_service = get_or_none("API_SERVICE")
    if not api_service:
        msg = "Tecton URL not set. Please authenticate to a Tecton instance with tecton.login() "
        raise errors.TectonAPIInaccessibleError(msg)
    validate_api_service_url(api_service)
    url, _, _ = api_service.partition("/api")
    return url


# Config values written to and read from the local .tecton/config file.
_LOCAL_TECTON_CONFIG: _ConfigSettings = {}

# Config values read from the local .tecton/config.tokens file.
_LOCAL_TECTON_TOKENS: _ConfigSettings = {}


def _init_configs():
    if not _is_mode_materialization():
        global _LOCAL_TECTON_CONFIG
        _LOCAL_TECTON_CONFIG = _read_json_config(_LOCAL_TECTON_CONFIG_FILE)

        global _LOCAL_TECTON_TOKENS
        _LOCAL_TECTON_TOKENS = _read_json_config(_LOCAL_TECTON_TOKENS_FILE)


def _init_metadata_server_config(mds_response):
    global _remote_mds_configs
    with _mds_config_lock:
        _remote_mds_configs = dict(mds_response.key_values)


def _force_initialize_mds_config(timeout_seconds: Optional[float] = None) -> None:
    runtime_mode = get_or_none("TECTON_RUNTIME_MODE")
    if runtime_mode in ("MATERIALIZATION", "EVALUATION"):
        return
    from tecton._internals import metadata_service  # noqa: TID251

    with _mds_config_lock:
        if _remote_mds_configs:
            return

    if timeout_seconds is not None:
        thread = threading.Thread(target=metadata_service.instance)
        thread.daemon = True
        thread.start()
        thread.join(timeout_seconds)
    else:
        metadata_service.instance()


def _clear_metadata_server_config():
    global _remote_mds_configs
    with _mds_config_lock:
        _remote_mds_configs = {}


class FeatureFlag:
    def __init__(self, key: str, owner: str, default_enabled: bool, allowed_sources: Optional[tuple] = None) -> None:
        if allowed_sources is None:
            allowed_sources = (
                ConfSource.SESSION_OVERRIDE,
                ConfSource.OS_ENV,
                ConfSource.REPO_CONFIG,
            )

        _VALID_KEYS_TO_ALLOWED_SOURCES[key] = allowed_sources
        _DEFAULTS[key] = lambda: default_enabled
        self.key = key
        self.owner = owner
        self.default_enabled = default_enabled
        self.allowed_sources = allowed_sources

    def enabled(self) -> bool:
        return get_bool(self.key)


IsolateFunctionDeserialization = FeatureFlag(
    key="TECTON_ISOLATE_FUNCTION_DESERIALIZATION", owner="Feature Eng", default_enabled=False
)


TECTON_STRIP_TIMEZONE_FROM_FEATURE_VALUES_FF = FeatureFlag(
    key="TECTON_STRIP_TIMEZONE_FROM_FEATURE_VALUES", owner="Feature Eng", default_enabled=False
)


DUCKDB_ENABLE_SPINE_SPLIT_FF = FeatureFlag(
    key="DUCKDB_ENABLE_SPINE_SPLIT", owner="Batch Compute", default_enabled=False
)


ENABLE_CALCULATION_DEVELOPMENT_FEATURES_FF = FeatureFlag(
    key="ENABLE_CALCULATION_DEVELOPMENT_FEATURES", owner="Devex", default_enabled=False
)


QUERYTREE_ENABLE_PARTITIONED_EXECUTION = FeatureFlag(
    key="QUERYTREE_ENABLE_PARTITIONED_EXECUTION", owner="Batch Compute", default_enabled=False
)

QUERYTREE_VERBOSE = FeatureFlag(key="QUERYTREE_VERBOSE", owner="Batch Data", default_enabled=False)


STREAM_INGEST_V2_ENABLED = FeatureFlag(
    key="STREAM_INGEST_V2_ENABLED",
    owner="Stream Ingest",
    default_enabled=False,
    allowed_sources=(
        ConfSource.SESSION_OVERRIDE,
        ConfSource.OS_ENV,
        ConfSource.REPO_CONFIG,
        ConfSource.BLOCKING_REMOTE_MDS_CONFIG,
    ),
)

TRANSFORM_SERVER_GROUPS_ENABLED = FeatureFlag(
    key="TRANSFORM_SERVER_GROUPS_ENABLED",
    owner="Feature Server",
    default_enabled=False,
    allowed_sources=(
        ConfSource.SESSION_OVERRIDE,
        ConfSource.OS_ENV,
        ConfSource.REPO_CONFIG,
        ConfSource.BLOCKING_REMOTE_MDS_CONFIG,
    ),
)


_init_configs()
