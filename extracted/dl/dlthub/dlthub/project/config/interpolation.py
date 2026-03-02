import os

from types import SimpleNamespace
from typing import Any, Dict

from dlt.common.utils import map_nested_values_in_place


class SimpleMissingNamespace(SimpleNamespace):
    """A namespace that skips missing attributes"""

    def __getattr__(self, v: Any) -> str:
        return ""


class InterpolateEnvironmentVariables:
    def __init__(self, extra_vars: Dict[str, Any] = None):
        self._vars = _VarMapping(extra_vars or {})

    def interpolate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Two passes so that variables can refer to other variables.
        data = map_nested_values_in_place(self._replace_vars, data)
        return map_nested_values_in_place(self._replace_vars, data)

    def _replace_vars(self, value: Any) -> Any:
        try:
            if isinstance(value, str):
                # Use our custom mapping to perform the interpolation.
                return value.format_map(self._vars)
        except AttributeError:
            pass
        # if not str or there was unknown namespace with . access
        return value


class _VarMapping:
    def __init__(self, extra_vars: Dict[str, Any]):
        self.extra_vars = extra_vars
        self.env_vars = SimpleMissingNamespace(**os.environ)

    def __getitem__(self, key: str) -> Any:
        if key == "env":
            return self.env_vars
        # Return the extra var if available, or empty string otherwise.
        return self.extra_vars.get(key, "{%s}" % key)
