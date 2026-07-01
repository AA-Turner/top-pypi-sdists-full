try:
    from dbt_state._version import __version__
except ImportError:
    __version__ = "0.0.0"  # ty: ignore[invalid-assignment]
try:
    from dbt_state.utils import DBT_VERSION

    dbt_version = ".".join(map(str, DBT_VERSION))
except ImportError:
    dbt_version = "0.0.0"
try:
    from sqlglot import __version__ as sqlglot_version
except ImportError:
    sqlglot_version = "0.0.0"
