"""Sandboxed script runtime for agent execution.

Defines the ScriptRuntime protocol and provides a Lua implementation
using abstra-lua. The sandbox is built-in — no os, io, require, load,
debug, etc. Only registered tool functions are available as globals.
"""

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Protocol, runtime_checkable


@runtime_checkable
class ScriptRuntime(Protocol):
    """Protocol for sandboxed script runtimes.

    Swap LupaRuntime for another implementation (e.g. MicroPython, Wasm)
    without changing the executor.
    """

    def register_function(self, name: str, func: Callable) -> None:
        """Make a Python function callable from within the runtime."""
        ...

    def execute(self, code: str) -> str:
        """Execute code and return captured output (print + return value)."""
        ...

    def reset(self) -> None:
        """Reset the runtime state (clear variables, keep registered functions)."""
        ...


class LupaRuntime:
    """Sandboxed Lua runtime using abstra-lua.

    Only registered tool functions and safe built-ins are available.
    All output is captured via a custom print() and returned as a string.
    """

    def __init__(
        self,
        max_instructions: int = 1_000_000,
        working_dir: Optional[Path] = None,
    ) -> None:
        from abstra_lua import LuaSession

        self._lua = LuaSession(max_instructions=max_instructions)
        self._max_instructions = max_instructions
        self._output_lines: List[str] = []
        self._registered_functions: Dict[str, Callable] = {}
        self._working_dir = working_dir or Path.cwd()
        self._setup_globals()

    def _setup_globals(self) -> None:
        """Register custom globals: print override, JSON utils, helpers, guardrails."""
        self._lua.set("print", self._capture_print)
        self._lua.set("json_encode", self._json_encode)
        self._lua.set("json_decode", self._json_decode)
        self._lua.set("array", self._make_array)
        self._lua.set("file", self._make_file)
        self._register_guardrails()

    def _register_guardrails(self) -> None:
        """Register stub functions that return helpful errors for common mistakes.

        When the LLM tries require(), load(), etc., instead of a cryptic
        'attempt to call nil', it gets a clear message pointing to the
        real available functions.
        """
        runtime = self

        def _make_guardrail_fn(blocked_name: str) -> Callable:
            def guard(*_args: Any) -> str:
                tool_names = list(runtime._registered_functions.keys())
                hint = (
                    "You have a real browser and real tools. "
                    "Call them directly as Lua globals.\n"
                    f"Available: {', '.join(tool_names)}\n"
                    'Example: navigate({url = "https://example.com"})'
                )
                raise RuntimeError(f"{blocked_name}() does not exist. {hint}")

            return guard

        for name in ("require", "dofile", "loadfile", "load", "loadstring"):
            self._lua.set(name, _make_guardrail_fn(name))

    def _capture_print(self, *args: Any) -> None:
        """Capture print() calls into output buffer."""
        self._output_lines.append(" ".join(str(a) for a in args))

    def log_output(self, text: str) -> None:
        """Append text to the captured output buffer.

        Public interface for external components (e.g. ToolAdapter) to
        inject output that the agent will see alongside print() calls.
        """
        self._output_lines.append(text)

    def _make_file(self, path: Any) -> str:
        """Resolve a file path relative to the working directory.

        Called from Lua as ``file("relativo/arquivo.xml")``.
        Returns the absolute path string so file references are never lost
        when crossing the Lua → Python boundary.
        """
        p = Path(str(path))
        if p.is_absolute():
            return str(p)
        return str(self._working_dir / p)

    @staticmethod
    def _make_array(*args: Any) -> list:
        """Create a Python list from Lua arguments.

        Called from Lua as ``array()``, ``array("a", "b")``, or
        ``array(lua_table)``.  Returns a real Python ``list`` which the
        tool adapter will preserve as a JSON array.
        """
        if len(args) == 0:
            return []
        if len(args) == 1:
            arg = args[0]
            # Already a list (abstra-lua auto-converts numeric-keyed tables)
            if isinstance(arg, list):
                return arg
            # Dict (abstra-lua auto-converts mixed/string-keyed tables)
            if isinstance(arg, dict):
                try:
                    items = sorted(arg.items(), key=lambda x: int(x[0]))
                    return [v for _, v in items]
                except (ValueError, TypeError):
                    return list(arg.values())
        return list(args)

    @staticmethod
    def _json_encode(value: Any) -> str:
        """Encode a value to JSON string. Exposed to Lua as json_encode()."""
        try:
            return json.dumps(value, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            return f"Error: json_encode failed: {e}"

    @staticmethod
    def _json_decode(text: str) -> Any:
        """Decode a JSON string. Exposed to Lua as json_decode()."""
        try:
            return json.loads(str(text))
        except (json.JSONDecodeError, TypeError) as e:
            return f"Error: json_decode failed: {e}"

    def register_function(self, name: str, func: Callable) -> None:
        """Register a Python function as a Lua global."""
        self._lua.set(name, func)
        self._registered_functions[name] = func

    def execute(self, code: str) -> str:
        """Execute Lua code and return captured output.

        The code is wrapped in a function to support return statements.
        Output = print() lines + return value (if any).
        """
        self._output_lines.clear()

        # Wrap in an immediately-invoked function so `return` works.
        wrapped = f"(function()\n{code}\nend)()"

        try:
            result = self._lua.eval(wrapped)
        except Exception as e:
            error_msg = str(e)
            output = "\n".join(self._output_lines)
            if output:
                return f"{output}\nError: {error_msg}"
            return f"Error: {error_msg}"

        output = "\n".join(self._output_lines)
        if result is not None:
            result_str = str(result)
            if output:
                return f"{output}\n=> {result_str}"
            return f"=> {result_str}"
        return output or "(no output)"

    def reset(self) -> None:
        """Reset runtime: re-create Lua state and re-register functions."""
        from abstra_lua import LuaSession

        self._lua = LuaSession(max_instructions=self._max_instructions)
        self._output_lines.clear()
        self._setup_globals()
        # Re-register all tool functions
        for name, func in self._registered_functions.items():
            self._lua.set(name, func)
