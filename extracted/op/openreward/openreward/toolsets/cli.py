"""Generic sandboxed CLI toolset.

Lifts the historically copy-pasted ``cli_environment.py`` from individual
env repos (ccompiler, sqliterust, gbemurust, Threadneedle, seta, dsbc) into
a single SDK-owned ``Toolset``. Declared on an env via class attribute::

    class MyEnv(Environment):
        toolsets = [CLIToolset]

        def __init__(self, task_spec, secrets):
            super().__init__(task_spec, secrets)
            self.sandbox = or_client.sandbox(self.sandbox_settings)

The env owns ``self.sandbox``; ``CLIToolset.__init__`` picks it up via the
``Toolset`` base contract.

Tool surface (9 tools): ``bash``, ``glob``, ``grep``, ``ls``, ``read``,
``write``, ``edit``, ``multi_edit``, ``todo_write``. Implementation lives
in :mod:`openreward.environments._sandbox_tools`; this file is just the
Pydantic param shapes and ``@tool``-decorated wrappers.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from openreward.environments._sandbox_tools import (
    _bash_impl,
    _edit_impl,
    _glob_impl,
    _grep_impl,
    _ls_impl,
    _multi_edit_impl,
    _read_impl,
    _write_impl,
)
from openreward.environments.environment import tool
from openreward.environments.toolset import Toolset
from openreward.environments.types import TextBlock, ToolOutput


# ── Pydantic parameter models ──

class BashParams(BaseModel, extra="forbid"):
    command: str
    timeout: Optional[float] = 30.0


class GlobParams(BaseModel, extra="forbid"):
    pattern: str
    path: Optional[str] = None


class GrepParams(BaseModel, extra="forbid"):
    pattern: str
    path: Optional[str] = None
    include: Optional[str] = None


class LSParams(BaseModel, extra="forbid"):
    path: str = "."
    ignore: Optional[List[str]] = None


class ReadParams(BaseModel, extra="forbid"):
    file_path: str
    offset: Optional[int] = None
    limit: Optional[int] = None


class WriteParams(BaseModel, extra="forbid"):
    file_path: str
    content: str


class EditParams(BaseModel, extra="forbid"):
    file_path: str
    old_string: str
    new_string: str
    replace_all: bool = False


class MultiEditParams(BaseModel, extra="forbid"):
    file_path: str
    edits: List[Dict[str, Any]]


class TodoWriteParams(BaseModel, extra="forbid"):
    todos: List[Dict[str, Any]]


# ── Toolset ──

class CLIToolset(Toolset):
    """Generic sandboxed CLI toolset (bash + 8 file/grep tools + todo).

    The bound environment must expose ``self.sandbox``. Most envs do this
    via ``self.sandbox = or_client.sandbox(self.sandbox_settings)`` in
    ``__init__``.
    """

    @classmethod
    def name(cls) -> str:
        return "cli"

    def __init__(self, env: Optional[Any] = None, sandbox_attr: str = "sandbox"):
        super().__init__(env, sandbox_attr)
        self.todos: List[Dict[str, Any]] = []

    @tool
    async def bash(self, params: BashParams) -> ToolOutput:
        """Execute a bash command in the sandbox."""
        return await _bash_impl(self.sandbox, params.command)

    @tool
    async def glob(self, params: GlobParams) -> ToolOutput:
        """Find files matching a glob pattern."""
        return await _glob_impl(self.sandbox, params.pattern, params.path)

    @tool
    async def grep(self, params: GrepParams) -> ToolOutput:
        """Recursively search file contents for a pattern."""
        return await _grep_impl(self.sandbox, params.pattern, params.path, params.include)

    @tool
    async def ls(self, params: LSParams) -> ToolOutput:
        """List directory contents (``ls -la``)."""
        return await _ls_impl(self.sandbox, params.path)

    @tool
    async def read(self, params: ReadParams) -> ToolOutput:
        """Read a file with optional line-range slicing; output has ``cat -n`` line numbers."""
        return await _read_impl(self.sandbox, params.file_path, params.offset, params.limit)

    @tool
    async def write(self, params: WriteParams) -> ToolOutput:
        """Write content to a file, creating parent directories as needed."""
        return await _write_impl(self.sandbox, params.file_path, params.content)

    @tool
    async def edit(self, params: EditParams) -> ToolOutput:
        """Exact-string replace in a file.

        ``old_string`` must be unique in the file unless ``replace_all=True``;
        multiline patterns and regex metacharacters are matched verbatim.
        """
        return await _edit_impl(
            self.sandbox,
            params.file_path,
            params.old_string,
            params.new_string,
            params.replace_all,
        )

    @tool
    async def multi_edit(self, params: MultiEditParams) -> ToolOutput:
        """Apply a sequence of edits to a single file atomically (in-memory)."""
        return await _multi_edit_impl(self.sandbox, params.file_path, params.edits)

    @tool
    def todo_write(self, params: TodoWriteParams) -> ToolOutput:
        """Replace the session todo list and return a formatted view."""
        try:
            self.todos = params.todos
            output_lines = ["=== TODO LIST ==="]
            for todo in self.todos:
                status = todo.get("status", "pending")
                priority = todo.get("priority", "medium")
                output_lines.append(
                    f"[{status}] [{priority}] {todo.get('content', 'No description')}"
                )
            text = "\n".join(output_lines)
            return ToolOutput(
                metadata={"todos": self.todos, "count": len(self.todos)},
                blocks=[TextBlock(text=text)],
                finished=False,
                reward=0.0,
            )
        except Exception as e:
            return ToolOutput(
                metadata={"error": str(e)},
                blocks=[TextBlock(text=f"Error managing todos: {str(e)}")],
                finished=False,
            )
