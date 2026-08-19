import os

_TRUE_VALUES = frozenset({"true", "1", "t", "y", "yes", "on"})


def _is_state_disabled() -> bool:
    """Return True when dbt-state has been explicitly disabled via environment variables.

    This is evaluated before importing the plugin implementation so that a disabled install
    avoids the (comparatively expensive) ``dbt.*`` imports that ``dbt_state.plugin`` pulls in.
    """
    if "DBT_ENGINE_MANAGE_STATE" in os.environ:
        return os.getenv("DBT_ENGINE_MANAGE_STATE", "").lower() not in _TRUE_VALUES
    disabled_value = os.getenv("RUN_CACHE_DISABLED") or os.getenv("DBT_RUN_CACHE_DISABLED") or ""
    return disabled_value.lower() in _TRUE_VALUES


try:
    from dbt_state._version import __version__ as __version__  # type: ignore[import]
except ImportError:
    __version__: str = "0.0.0"


if _is_state_disabled():
    # Skip importing the plugin implementation entirely. An empty ``plugins`` list means dbt never
    # instantiates the plugin, so none of its ``dbt.*`` dependencies are imported when disabled.
    plugins: list = []

    from dbt_state.events import fire_disabled_event

    fire_disabled_event()
else:
    from dbt_state import plugin

    plugins = [plugin.RunCachePlugin]
