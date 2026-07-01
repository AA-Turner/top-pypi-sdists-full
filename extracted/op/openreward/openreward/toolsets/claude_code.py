"""Claude Code session toolset.

Provides the seven built-in tools that the Claude Code CLI exposes
(``bash``, ``glob``, ``grep``, ``read``, ``write``, ``edit``, ``todo_write``),
each backed by ``self.sandbox`` from the bound environment.

Tool descriptions are copied from the firehorse builtin descriptions
(``firehorse/firehorse/mcp/builtin_descriptions.py``) which were originally
extracted from ``claude-code/src/tools/*/prompt.ts``. They are inlined here
so the toolset has no runtime dependency on firehorse.

The actual sandbox-side logic (bash/glob/grep/read/write/edit) lives in
:mod:`openreward.environments._sandbox_tools` and is shared with
:class:`openreward.toolsets.cli.CLIToolset`. This file is now the
Pydantic param shapes, the firehorse-derived prompt strings, and thin
``@tool`` wrappers.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from openreward.environments._sandbox_tools import (
    _bash_impl,
    _edit_impl,
    _glob_impl,
    _grep_impl,
    _read_impl,
    _write_impl,
)
from openreward.environments.environment import tool
from openreward.environments.toolset import Toolset
from openreward.environments.types import TextBlock, ToolOutput


# ── Pydantic parameter models ──

class BashParams(BaseModel, extra="forbid"):
    command: str
    description: str = ""
    timeout: Optional[float] = 30.0


class GlobParams(BaseModel, extra="forbid"):
    pattern: str
    path: Optional[str] = None


class GrepParams(BaseModel, extra="forbid"):
    pattern: str
    path: Optional[str] = None
    glob: Optional[str] = None


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


class TodoWriteParams(BaseModel, extra="forbid"):
    todos: List[Dict[str, Any]]


# ── Tool descriptions (verbatim from firehorse builtin_descriptions.py) ──

BASH_DESCRIPTION = """\
Executes a given bash command and returns its output.

The working directory persists between commands, but shell state does not. The shell environment is initialized from the user's profile (bash or zsh).

IMPORTANT: Avoid using this tool to run `find`, `grep`, `cat`, `head`, `tail`, `sed`, `awk`, or `echo` commands, unless explicitly instructed or after you have verified that a dedicated tool cannot accomplish your task. Instead, use the appropriate dedicated tool as this will provide a much better experience for the user:

 - File search: Use mcp__openreward__glob if available (NOT find or ls)
 - Content search: Use mcp__openreward__grep if available (NOT grep or rg)
 - Read files: Use mcp__openreward__read if available (NOT cat/head/tail)
 - Edit files: Use mcp__openreward__edit if available (NOT sed/awk)
 - Write files: Use mcp__openreward__write if available (NOT echo >/cat <<EOF)
 - Communication: Output text directly (NOT echo/printf)
While the bash tool can do similar things, it's better to use the dedicated tools as they provide a better user experience and make it easier to review tool calls and give permission.

# Instructions
 - If your command will create new directories or files, first use this tool to run `ls` to verify the parent directory exists and is the correct location.
 - Always quote file paths that contain spaces with double quotes in your command (e.g., cd "path with spaces/file.txt")
 - Try to maintain your current working directory throughout the session by using absolute paths and avoiding usage of `cd`. You may use `cd` if the User explicitly requests it.
 - You may specify an optional timeout in milliseconds (up to 600000ms / 10 minutes). By default, your command will timeout after 120000ms (2 minutes).
 - You can use the `run_in_background` parameter to run the command in the background. Only use this if you don't need the result immediately and are OK being notified when the command completes later. You do not need to check the output right away - you'll be notified when it finishes. You do not need to use '&' at the end of the command when using this parameter.
 - When issuing multiple commands:
  - If the commands are independent and can run in parallel, make multiple Bash tool calls in a single message. Example: if you need to run "git status" and "git diff", send a single message with two Bash tool calls in parallel.
  - If the commands depend on each other and must run sequentially, use a single Bash call with '&&' to chain them together.
  - Use ';' only when you need to run commands sequentially but don't care if earlier commands fail.
  - DO NOT use newlines to separate commands (newlines are ok in quoted strings).
 - For git commands:
  - Prefer to create a new commit rather than amending an existing commit.
  - Before running destructive operations (e.g., git reset --hard, git push --force, git checkout --), consider whether there is a safer alternative that achieves the same goal. Only use destructive operations when they are truly the best approach.
  - Never skip hooks (--no-verify) or bypass signing (--no-gpg-sign, -c commit.gpgsign=false) unless the user has explicitly asked for it. If a hook fails, investigate and fix the underlying issue.
 - Avoid unnecessary `sleep` commands:
  - Do not sleep between commands that can run immediately — just run them.
  - If your command is long running and you would like to be notified when it finishes — use `run_in_background`. No sleep needed.
  - Do not retry failing commands in a sleep loop — diagnose the root cause.
  - If waiting for a background task you started with `run_in_background`, you will be notified when it completes — do not poll.
  - If you must poll an external process, use a check command (e.g. `gh run view`) rather than sleeping first.
  - If you must sleep, keep the duration short (1-5 seconds) to avoid blocking the user.
"""

GREP_DESCRIPTION = """\
A powerful search tool built on ripgrep

  Usage:
  - ALWAYS use Grep for search tasks. NEVER invoke `grep` or `rg` as a Bash command. The Grep tool has been optimized for correct permissions and access.
  - Supports full regex syntax (e.g., "log.*Error", "function\\s+\\w+")
  - Filter files with glob parameter (e.g., "*.js", "**/*.tsx") or type parameter (e.g., "js", "py", "rust")
  - Output modes: "content" shows matching lines, "files_with_matches" shows only file paths (default), "count" shows match counts
  - Use Agent tool for open-ended searches requiring multiple rounds
  - Pattern syntax: Uses ripgrep (not grep) - literal braces need escaping (use `interface\\{\\}` to find `interface{}` in Go code)
  - Multiline matching: By default patterns match within single lines only. For cross-line patterns like `struct \\{[\\s\\S]*?field`, use `multiline: true`
"""

GLOB_DESCRIPTION = """\
- Fast file pattern matching tool that works with any codebase size
- Supports glob patterns like "**/*.js" or "src/**/*.ts"
- Returns matching file paths sorted by modification time
- Use this tool when you need to find files by name patterns
- When you are doing an open ended search that may require multiple rounds of globbing and grepping, use the Agent tool instead"""

READ_DESCRIPTION = """\
Reads a file from the local filesystem. You can access any file directly by using this tool.
Assume this tool is able to read all files on the machine. If the User provides a path to a file assume that path is valid. It is okay to read a file that does not exist; an error will be returned.

Usage:
- The file_path parameter must be an absolute path, not a relative path
- By default, it reads up to 2000 lines starting from the beginning of the file
- When you already know which part of the file you need, only read that part. This can be important for larger files.
- Results are returned using cat -n format, with line numbers starting at 1
- This tool allows Claude Code to read images (eg PNG, JPG, etc). When reading an image file the contents are presented visually as Claude Code is a multimodal LLM.
- This tool can read PDF files (.pdf). For large PDFs (more than 10 pages), you MUST provide the pages parameter to read specific page ranges (e.g., pages: "1-5"). Reading a large PDF without the pages parameter will fail. Maximum 20 pages per request.
- This tool can read Jupyter notebooks (.ipynb files) and returns all cells with their outputs, combining code, text, and visualizations.
- This tool can only read files, not directories. To read a directory, use an ls command via the mcp__openreward__bash tool, if available.
- You will regularly be asked to read screenshots. If the user provides a path to a screenshot, ALWAYS use this tool to view the file at the path. This tool will work with all temporary file paths.
- If you read a file that exists but has empty contents you will receive a system reminder warning in place of file contents."""

EDIT_DESCRIPTION = """\
Performs exact string replacements in files.

Usage:
- You must use the `mcp__openreward__read` tool, if available, at least once in the conversation before editing. This tool will error if you attempt an edit without reading the file.
- When editing text from read tool output, ensure you preserve the exact indentation (tabs/spaces) as it appears AFTER the line number prefix. The line number prefix format is: line number + tab. Everything after that is the actual file content to match. Never include any part of the line number prefix in the old_string or new_string.
- ALWAYS prefer editing existing files in the codebase. NEVER write new files unless explicitly required.
- Only use emojis if the user explicitly requests it. Avoid adding emojis to files unless asked.
- The edit will FAIL if `old_string` is not unique in the file. Either provide a larger string with more surrounding context to make it unique or use `replace_all` to change every instance of `old_string`.
- Use `replace_all` for replacing and renaming strings across the file. This parameter is useful if you want to rename a variable for instance."""

WRITE_DESCRIPTION = """\
Writes a file to the local filesystem.

Usage:
- This tool will overwrite the existing file if there is one at the provided path.
- If this is an existing file, you MUST use the mcp__openreward__read tool first, if available, to read the file's contents. This tool will fail if you did not read the file first.
- Prefer the mcp__openreward__edit tool, if available, for modifying existing files — it only sends the diff. Only use this tool to create new files or for complete rewrites.
- NEVER create documentation files (*.md) or README files unless explicitly requested by the User.
- Only use emojis if the user explicitly requests it. Avoid writing emojis to files unless asked."""

TODO_WRITE_DESCRIPTION = """\
Manage todo list for task planning and progress tracking.

Each todo item should have: id, content, status, priority.
Status options: "pending", "in_progress", "completed"
Priority options: "high", "medium", "low\""""


# ── Toolset ──

class ClaudeCodeToolset(Toolset):
    """Session toolset exposing the Claude Code seven-tool surface.

    The toolset is bound to a session by passing it to ``env.session(...)``::

        from openreward.toolsets import ClaudeCodeToolset

        with env.session(task=task, toolset="claude-code") as session:
            session.call_tool("bash", {"command": "ls"})

    Requires the bound environment to define ``self.sandbox``.
    """

    @classmethod
    def name(cls) -> str:
        return "claude-code"

    def __init__(self, env: Optional[Any] = None, sandbox_attr: str = "sandbox"):
        super().__init__(env, sandbox_attr)
        self.todos: List[Dict[str, Any]] = []

    @tool
    async def bash(self, params: BashParams) -> ToolOutput:
        return await _bash_impl(self.sandbox, params.command)

    @tool
    async def glob(self, params: GlobParams) -> ToolOutput:
        return await _glob_impl(self.sandbox, params.pattern, params.path)

    @tool
    async def grep(self, params: GrepParams) -> ToolOutput:
        return await _grep_impl(self.sandbox, params.pattern, params.path, params.glob)

    @tool
    async def read(self, params: ReadParams) -> ToolOutput:
        return await _read_impl(self.sandbox, params.file_path, params.offset, params.limit)

    @tool
    async def write(self, params: WriteParams) -> ToolOutput:
        return await _write_impl(self.sandbox, params.file_path, params.content)

    @tool
    async def edit(self, params: EditParams) -> ToolOutput:
        return await _edit_impl(
            self.sandbox,
            params.file_path,
            params.old_string,
            params.new_string,
            params.replace_all,
        )

    @tool
    def todo_write(self, params: TodoWriteParams) -> ToolOutput:
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


# Assign descriptions onto each tool method's __doc__ so the framework's
# introspection (which reads fn.__doc__ for ToolSpec.description) picks them up.
ClaudeCodeToolset.bash.__doc__ = BASH_DESCRIPTION
ClaudeCodeToolset.glob.__doc__ = GLOB_DESCRIPTION
ClaudeCodeToolset.grep.__doc__ = GREP_DESCRIPTION
ClaudeCodeToolset.read.__doc__ = READ_DESCRIPTION
ClaudeCodeToolset.write.__doc__ = WRITE_DESCRIPTION
ClaudeCodeToolset.edit.__doc__ = EDIT_DESCRIPTION
ClaudeCodeToolset.todo_write.__doc__ = TODO_WRITE_DESCRIPTION
