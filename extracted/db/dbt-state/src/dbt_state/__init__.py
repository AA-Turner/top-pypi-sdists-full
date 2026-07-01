from dbt_state import plugin

try:
    from dbt_state._version import __version__ as __version__
except ImportError:
    __version__: str = "0.0.0"


plugins = [plugin.RunCachePlugin]
