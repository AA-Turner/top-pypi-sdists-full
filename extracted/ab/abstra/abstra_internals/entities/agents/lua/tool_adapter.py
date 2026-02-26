"""Adapter for converting ToolHandlers into Lua-callable functions.

Defines the ToolAdapter protocol and provides a default implementation
that handles argument conversion before passing to handlers.
"""

from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    Tuple,
    runtime_checkable,
)

from abstra_internals.entities.agents.tools.dispatcher import ToolHandler


@runtime_checkable
class ToolAdapter(Protocol):
    """Protocol for adapting ToolHandlers to runtime-callable functions.

    Swap LuaToolAdapter for a different implementation to change how
    tool arguments are passed or how results are formatted.
    """

    def adapt(self, handler: ToolHandler) -> Callable:
        """Convert a ToolHandler into a callable function for the runtime."""
        ...


class LuaToolAdapter:
    """Default adapter: converts Lua arguments → Python dicts for ToolHandler.execute().

    With abstra-lua, Lua tables are automatically converted to Python dicts
    when passed to Python functions. This adapter handles edge cases and
    logs tool calls.

    When ``log_fn`` is provided, every tool result is automatically written to
    the runtime's output buffer so the agent sees it even without an explicit
    ``print()`` call.
    """

    def __init__(self, log_fn: Optional[Callable[[str], None]] = None) -> None:
        self._call_log: List[Tuple[str, Dict[str, Any], str]] = []
        self._log_fn = log_fn

    @property
    def call_log(self) -> List[Tuple[str, Dict[str, Any], str]]:
        """Log of (handler_name, action_input, result) for debugging."""
        return list(self._call_log)

    def adapt(self, handler: ToolHandler) -> Callable:
        """Wrap a ToolHandler so it can be called from Lua with a table argument."""
        adapter = self

        def wrapper(*args: Any) -> str:
            if len(args) > 1:
                safe_name = handler.name.replace("-", "_")
                result = (
                    f"Error: {safe_name}() takes a single table argument, not {len(args)} arguments. "
                    f"Use: {safe_name}({{key = value}})"
                )
                adapter._call_log.append((handler.name, {}, result))
                if adapter._log_fn and result:
                    adapter._log_fn(result)
                return result
            lua_arg = args[0] if args else None
            action_input = _to_dict(lua_arg)
            try:
                result = handler.execute(action_input)
            except Exception as e:
                result = f"Error: {e}"
            adapter._call_log.append((handler.name, action_input, result))
            if adapter._log_fn and result:
                adapter._log_fn(result)
            return result

        return wrapper


def _to_dict(value: Any) -> Dict[str, Any]:
    """Convert a value to a dict suitable for ToolHandler.execute().

    With abstra-lua, Lua tables are auto-converted to Python dicts/lists.
    This function handles all cases gracefully.
    """
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if isinstance(value, (str, int, float, bool, list)):
        return {}
    return {}


def lua_table_to_dict(lua_table: Any) -> Dict[str, Any]:
    """Convert a Lua table to a Python dict.

    With abstra-lua, tables are auto-converted to Python dicts.
    This function is kept for backward compatibility.
    """
    return _to_dict(lua_table)


def lua_table_to_list(lua_table: Any) -> list:
    """Convert a Lua array table to a Python list."""
    if lua_table is None:
        return []
    if isinstance(lua_table, list):
        return lua_table
    if isinstance(lua_table, dict):
        try:
            items = sorted(lua_table.items(), key=lambda x: int(x[0]))
            return [v for _, v in items]
        except (ValueError, TypeError):
            return list(lua_table.values())
    return []


def _convert_value(value: Any) -> Any:
    """Convert a single value to its Python equivalent.

    With abstra-lua, values are already Python types.
    This function is kept for backward compatibility.
    """
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [_convert_value(item) for item in value]
    if isinstance(value, dict):
        return {k: _convert_value(v) for k, v in value.items()}
    return value
