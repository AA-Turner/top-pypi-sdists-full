"""Terminal rendering — Rich markdown, code highlighting, streaming display, status indicators."""

from __future__ import annotations

import json
import re
import signal
import shutil
import sys
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from io import StringIO, TextIOBase
from itertools import chain

from rich.console import Console
from rich.live import Live
from rich.markup import escape
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskID, TextColumn
from rich.rule import Rule
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

from sage.core.thinking_filter import ThinkingSuppressionFilter


def normalize_tool_command_syntax(content: str) -> str:
    """Normalize permissive tool command spellings into canonical SAGE syntax.

    Weak models sometimes emit:
    - `READ README.md`
    - `SEARCH *.py`
    - `RUN pytest`

    Or XML-style tools (if bleeding from base model prompts):
    - `<execute_tool>search_code(query="...")</execute_tool>`

    We normalize those to the canonical `READ: ...` form so the runtime can
    execute them instead of failing a near-miss on syntax alone.
    """
    # 1. Normalize XML style tool calls
    xml_generic_pattern = re.compile(
        r"<execute_tool>\s*([a-zA-Z0-9_]+)\s*\(\s*[a-zA-Z0-9_]+\s*=\s*[\"'](.*?)[\"']\s*(?:,\s*[a-zA-Z0-9_]+\s*=\s*[\"'].*?[\"'])*\s*\)\s*</execute_tool>",
        re.MULTILINE | re.DOTALL,
    )

    def _rewrite_xml(match: re.Match[str]) -> str:
        tool_name = match.group(1).lower()
        arg = match.group(2)
        if "search" in tool_name:
            return f"SEARCH: {arg}"
        if "read" in tool_name or "file" in tool_name:
            return f"READ: {arg}"
        if "run" in tool_name or "command" in tool_name:
            return f"RUN: {arg}"
        return match.group(0)

    content = xml_generic_pattern.sub(_rewrite_xml, content)

    xml_block_pattern = re.compile(
        r"<execute_tool>\s*(.*?)\s*</execute_tool>", re.MULTILINE | re.DOTALL
    )

    def _rewrite_xml_block(match: re.Match[str]) -> str:
        inner = (match.group(1) or "").strip()
        if not inner:
            return ""
        normalized = normalize_tool_command_syntax(inner)
        if re.search(r"^\s*(READ|SEARCH|RUN|FILE):\s+\S", normalized, re.MULTILINE):
            return normalized

        # YAML-ish payload inside <execute_tool> ... </execute_tool>
        # Example (from user logs):
        # tool_name: read_file
        # parameters:
        #   file_path: ai-platform/sage/core/agent.py
        tool_name_match = re.search(r"^\s*tool_name\s*:\s*(?P<tool>\w+)\s*$", inner, re.I | re.M)
        if tool_name_match:
            tool_name = (tool_name_match.group("tool") or "").strip().lower()
            file_path_match = re.search(
                r"^\s*(?:file_path|path)\s*:\s*(?P<path>\S.+?)\s*$", inner, re.I | re.M
            )
            pattern_match = re.search(
                r"^\s*(?:pattern|query)\s*:\s*(?P<pattern>\S.+?)\s*$", inner, re.I | re.M
            )
            command_match = re.search(
                r"^\s*(?:command|cmd)\s*:\s*(?P<command>\S.+?)\s*$", inner, re.I | re.M
            )

            if tool_name in {"read_file", "read", "open_file", "open"} and file_path_match:
                path = (file_path_match.group("path") or "").strip().strip('"').strip("'")
                if path:
                    return f"READ: {path}"
            if tool_name in {"search_code", "search", "grep"} and pattern_match:
                pattern = (pattern_match.group("pattern") or "").strip().strip('"').strip("'")
                if pattern:
                    return f"SEARCH: {pattern}"
            if (
                tool_name in {"run", "run_command", "execute_command", "bash", "shell"}
                and command_match
            ):
                cmd = (command_match.group("command") or "").strip().strip('"').strip("'")
                if cmd:
                    return f"RUN: {cmd}"

        # JSON payload (weak models often emit MCP/OpenAI-style blobs inside <execute_tool>)
        def _first_json_object(text: str) -> str | None:
            start = text.find("{")
            if start < 0:
                return None
            depth = 0
            for i in range(start, len(text)):
                if text[i] == "{":
                    depth += 1
                elif text[i] == "}":
                    depth -= 1
                    if depth == 0:
                        return text[start : i + 1]
            return None

        json_blob = _first_json_object(inner)
        if json_blob:
            try:
                obj = json.loads(json_blob)
            except json.JSONDecodeError:
                obj = None
            if isinstance(obj, dict):
                tool_name = (
                    obj.get("tool_name") or obj.get("name") or obj.get("tool") or ""
                ).strip().lower()
                params = obj.get("parameters") or obj.get("arguments") or obj
                if isinstance(params, str):
                    try:
                        params = json.loads(params)
                    except json.JSONDecodeError:
                        params = {}
                if not isinstance(params, dict):
                    params = {}
                fp = params.get("file_path") or params.get("path")
                pat = params.get("pattern") or params.get("query")
                cmd = params.get("command") or params.get("cmd")
                if tool_name in {"read_file", "read", "open_file", "open"} and fp:
                    return f"READ: {fp}"
                if tool_name in {"search_code", "search", "grep"} and pat:
                    return f"SEARCH: {pat}"
                if tool_name in {"run", "run_command", "execute_command", "bash", "shell"} and cmd:
                    return f"RUN: {cmd}"

        call_match = re.search(
            r"\b(?P<name>read_file|read|open_file|open|search|search_code|grep|run|run_command|execute_command)\s*\(\s*(?P<args>.*?)\s*\)\s*$",
            inner,
            re.IGNORECASE | re.DOTALL,
        )
        if call_match:
            name = (call_match.group("name") or "").lower()
            args = call_match.group("args") or ""
            quoted = re.search(r"[\"'](.*?)[\"']", args, re.DOTALL)
            arg = quoted.group(1).strip() if quoted else args.strip()
            if arg:
                if "search" in name or "grep" in name:
                    return f"SEARCH: {arg}"
                if "read" in name or "open" in name or "file" in name:
                    return f"READ: {arg}"
                if "run" in name or "execute" in name:
                    return f"RUN: {arg}"
            return ""

        json_tool = re.search(
            r"\"tool\"\s*:\s*\"(?P<tool>read|search|run)\".*?\"(?:path|pattern|command)\"\s*:\s*\"(?P<arg>.*?)\"",
            inner,
            re.IGNORECASE | re.DOTALL,
        )
        if json_tool:
            tool = json_tool.group("tool").upper()
            arg = (json_tool.group("arg") or "").strip()
            if arg:
                return f"{tool}: {arg}"
        return match.group(0)

    content = xml_block_pattern.sub(_rewrite_xml_block, content)

    # 1.5 Handle write_file XML
    xml_write_pattern = re.compile(
        r"<execute_tool>\s*(?:write_file|write)\s*\(\s*path=[\"'](.*?)[\"']\s*,\s*content=[\"'](.*?)[\"']\s*\)\s*</execute_tool>",
        re.MULTILINE | re.DOTALL,
    )

    def _rewrite_xml_write(match: re.Match[str]) -> str:
        path = match.group(1)
        file_content = match.group(2)
        file_content = file_content.replace("\\n", "\n").replace('\\"', '"').replace("\\'", "'")
        return f"FILE: {path}\n```javascript\n{file_content}\n```"

    content = xml_write_pattern.sub(_rewrite_xml_write, content)

    # 1.6 Handle execute_bash XML
    xml_bash_pattern = re.compile(
        r"<execute_bash>\s*(.*?)\s*</execute_bash>", re.MULTILINE | re.DOTALL
    )
    content = xml_bash_pattern.sub(lambda m: f"RUN: {m.group(1)}", content)

    xml_tool_call_pattern = re.compile(
        r"<tool_call>\s*(.*?)\s*</tool_call>", re.MULTILINE | re.DOTALL
    )
    content = xml_tool_call_pattern.sub(
        lambda m: normalize_tool_command_syntax(m.group(1)), content
    )

    # 2. Normalize bare/bad-cased tool calls
    bare_tool_pattern = re.compile(
        r"^(\s*(?:[-*]\s*)?)(READ|SEARCH|RUN|FILE)\s+(\S.*)$",
        re.MULTILINE | re.IGNORECASE,
    )

    def _rewrite(match: re.Match[str]) -> str:
        prefix, tool, arg = match.groups()
        tool = tool.upper()
        if ":" in match.group(0) and match.group(0).split(":")[0].strip().upper() == tool:
            return match.group(0)
        return f"{prefix}{tool}: {arg}"

    content = bare_tool_pattern.sub(_rewrite, content)
    return _normalize_bare_shell_command_lines(content)


def _normalize_bare_shell_command_lines(text: str) -> str:
    """Turn bare one-line shell invocations into RUN: ... (weak models often emit `ls -F` without RUN:)."""
    out: list[str] = []
    in_code_fence = False
    for line in text.splitlines():
        st = line.strip()
        if st.startswith("```"):
            in_code_fence = not in_code_fence
            out.append(line)
            continue
        if in_code_fence:
            out.append(line)
            continue
        if re.match(r"^\s*(READ|SEARCH|RUN|FILE|RESULT):", line, re.I):
            out.append(line)
            continue
        m_ls = re.match(
            r"^(\s*)((?:ls|dir)(?:\s+-[A-Za-z0-9]+)+)\s*$",
            line,
            re.IGNORECASE,
        )
        if m_ls:
            out.append(f"{m_ls.group(1)}RUN: {m_ls.group(2)}")
            continue
        m_cat = re.match(r"^(\s*)(cat\s+\S.+?)\s*$", line, re.IGNORECASE)
        if m_cat:
            out.append(f"{m_cat.group(1)}RUN: {m_cat.group(2)}")
            continue
        m_tree = re.match(r"^(\s*)tree\s*$", line, re.IGNORECASE)
        if m_tree:
            out.append(f"{m_tree.group(1)}RUN: tree")
            continue
        out.append(line)
    return "\n".join(out)


def clean_malformed_tool_commands(content: str) -> str:
    """Remove malformed tool commands from response content.

    This allows valid content to be processed even when the model
    outputs some malformed tool commands mixed with valid content.

    Removes:
    - Blank tool commands: "READ:" with nothing after
    - Malformed tool commands: "READ: The user is..." (explanation instead of path)
    - Multiple consecutive blank READ/SEARCH/RUN lines

    Returns:
        Cleaned content with malformed commands removed
    """
    content = normalize_tool_command_syntax(content)
    lines = content.split("\n")
    cleaned_lines = []

    # Patterns for malformed tool commands
    blank_pattern = re.compile(r"^\s*(READ|SEARCH|RUN):\s*$")
    malformed_pattern = re.compile(
        r"^\s*(READ|SEARCH|RUN):\s+"
        r"(?:The|I|This|To|By|Let|Now|First|Next|Here|We|You|My|In|For|As|So|If|When|While|Since|After|Before)\s",
        re.IGNORECASE,
    )

    # Track consecutive blank commands to collapse them
    consecutive_blank_count = 0

    for line in lines:
        # Check for blank command
        if blank_pattern.match(line):
            consecutive_blank_count += 1
            # Only keep first blank if there are multiple (and even then, skip it)
            if consecutive_blank_count > 1:
                continue
            # Skip blank commands entirely
            continue

        # Check for malformed command (explanation instead of path)
        if malformed_pattern.match(line):
            # Skip this line - it's a malformed tool command
            continue

        # Valid line - reset counter and keep it
        consecutive_blank_count = 0
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def _parse_incremental_tool_calls(content: str) -> list | None:
    """Parse tool commands from partial streaming content.

    P1-1: Provides tool context to the pre-display validator so it can
    distinguish legitimate batch reads from garbage repetition.

    Returns list of ToolCall objects, or None if no valid commands found.
    """
    try:
        from sage.core.tools import ToolCall, ToolType

        content = normalize_tool_command_syntax(content)
        calls = []
        # Match only valid READ:/SEARCH:/RUN: with non-empty arguments
        for m in re.finditer(
            r"^\s*(?:[-*]\s*)?(READ|SEARCH|RUN):\s*(\S.+)$", content, re.MULTILINE
        ):
            tool_type_str = m.group(1).upper()
            arg = m.group(2).strip()

            if not arg:
                continue

            tool_type_map = {
                "READ": ToolType.READ,
                "SEARCH": ToolType.SEARCH,
                "RUN": ToolType.RUN,
            }
            tool_type = tool_type_map.get(tool_type_str)
            if not tool_type:
                continue

            if tool_type == ToolType.READ:
                arguments = {"path": arg}
            elif tool_type == ToolType.SEARCH:
                arguments = {"pattern": arg}
            else:
                arguments = {"command": arg}

            calls.append(
                ToolCall(
                    tool_type=tool_type,
                    arguments=arguments,
                    validated=True,  # Trust for validation context
                )
            )

        return calls if calls else None
    except ImportError:
        # ToolCall not available, return None
        return None


# Back-compat alias for internal use
_ThinkingSuppressionFilter = ThinkingSuppressionFilter


# =============================================================================
# P1-12: HARD GUARDRAIL VIOLATIONS
# =============================================================================
# These are violations that MUST stop execution - they cannot be bypassed or ignored


class HardGuardrailViolation(Exception):
    """Exception raised when a critical guardrail is violated.

    P1-12: Hard invariants that cannot be bypassed.
    Unlike soft warnings, these MUST stop execution.
    """

    def __init__(self, violation_type: str, message: str, context: str = ""):
        self.violation_type = violation_type
        self.message = message
        self.context = context
        super().__init__(f"[{violation_type}] {message}")


class GroundingViolation(HardGuardrailViolation):
    """Model generated content without file evidence."""

    def __init__(self, message: str, context: str = ""):
        super().__init__("GROUNDING", message, context)


class ToolSyntaxViolation(HardGuardrailViolation):
    """Model used invalid tool syntax (XML, function calls, etc.)."""

    def __init__(self, message: str, context: str = ""):
        super().__init__("TOOL_SYNTAX", message, context)


class FabricationViolation(HardGuardrailViolation):
    """Model fabricated content without reading files."""

    def __init__(self, message: str, context: str = ""):
        super().__init__("FABRICATION", message, context)


class StreamingTimeoutError(Exception):
    """Exception raised when streaming times out waiting for first token.

    P0-1: First-token timeout to detect stalled models.
    This exception is raised when the model fails to produce any tokens
    within the specified timeout period, indicating a potential hang.
    """

    def __init__(self, message: str = "No response from model within timeout period"):
        self.message = message
        super().__init__(message)


def _next_token_with_timeout(
    tokens: Iterator[str],
    timeout_seconds: float,
) -> tuple[bool, str | None]:
    """Fetch the first streaming token with a hard timeout.

    timeout_seconds <= 0 disables the timeout (wait forever).
    """
    result: dict[str, object] = {}
    error: dict[str, BaseException] = {}
    done = threading.Event()
    sentinel = object()

    def _runner() -> None:
        try:
            result["value"] = next(tokens, sentinel)
        except BaseException as exc:  # pragma: no cover - exercised via caller behavior
            error["exc"] = exc
        finally:
            done.set()

    thread = threading.Thread(target=_runner, daemon=True)
    thread.start()
    wait_seconds = timeout_seconds if timeout_seconds > 0 else None  # None = wait forever
    if not done.wait(wait_seconds):
        raise StreamingTimeoutError(f"No response from model within {timeout_seconds:.0f} seconds")
    if "exc" in error:
        raise error["exc"]

    value = result.get("value", sentinel)
    if value is sentinel:
        return False, None
    return True, str(value)


# =============================================================================
# RENDERER CLASS - Wrapper for streaming functionality
# =============================================================================


class Renderer:
    """Renderer for model output with streaming and timeout support.

    P0-1: Provides first-token timeout to prevent hangs from stalled models.
    """

    def __init__(self):
        self._console = console

    def stream_tokens_with_phase(
        self,
        tokens: Iterator[str],
        model_id: str = "",
        return_rejection_info: bool = False,
        first_token_timeout: float | None = None,
    ) -> str | tuple[str, bool, str]:
        """Stream tokens with a thinking spinner and first-token timeout.

        Args:
            tokens: Iterator of tokens from the model
            model_id: Model identifier for display
            return_rejection_info: If True, returns (response, was_rejected, reason)
            first_token_timeout: Seconds to wait for first token before timeout (P0-1)

        Returns:
            If return_rejection_info is False: response string (empty if rejected)
            If return_rejection_info is True: (response, was_rejected, rejection_reason)

        Raises:
            StreamingTimeoutError: If no token received within first_token_timeout
        """
        # Delegate to the module-level function with timeout support
        if first_token_timeout is None:
            import os
            raw = os.environ.get("SAGE_STREAM_TIMEOUT", "").strip()
            try:
                first_token_timeout = float(raw) if raw else 0.0  # 0 = no timeout
            except ValueError:
                first_token_timeout = 0.0
        return stream_tokens_with_phase(
            tokens,
            model_id=model_id,
            return_rejection_info=return_rejection_info,
            first_token_timeout=first_token_timeout,
        )

    def get_output_mode(self) -> str:
        """Get the current output verbosity mode."""
        return get_output_mode()

    def phase(self, name: str, detail: str = "") -> None:
        """Print a phase indicator."""
        phase(name, detail)

    def info(self, msg: str) -> None:
        """Print an info message."""
        info(msg)

    def warning(self, msg: str) -> None:
        """Print a warning message."""
        warning(msg)

    def debug_warning(self, msg: str) -> None:
        """Non-critical validation / filter messages (verbose mode only)."""
        globals()["debug_warning"](msg)

    def error(self, msg: str) -> None:
        """Print an error message."""
        error(msg)

    def activate_bottom_dock(
        self,
        *,
        todos: list[dict] | None = None,
        status_message: str = "Working...",
        prompt_message: str = "Working...",
    ) -> bool:
        """Enable the bottom-anchored task dock."""
        return activate_bottom_dock(
            todos=todos,
            status_message=status_message,
            prompt_message=prompt_message,
        )

    def set_bottom_dock_todos(self, todos: list[dict] | None) -> None:
        """Update the dock todo list."""
        set_bottom_dock_todos(todos)

    def set_bottom_dock_status(self, message: str) -> None:
        """Update the live dock status line."""
        set_bottom_dock_status(message)

    def clear_bottom_dock_todos(self) -> None:
        """Hide the dock todo list."""
        clear_bottom_dock_todos()

    def deactivate_bottom_dock(self) -> None:
        """Disable the bottom-anchored task dock."""
        deactivate_bottom_dock()

    def print_files_written(self, files: list[str]) -> None:
        """Print a summary of files written to disk."""
        print_files_written(files)

    def print_shell_start(self, cmd: str) -> None:
        """Print the start of a shell command execution."""
        print_shell_start(cmd)

    def print_shell_output(self, output: str) -> None:
        """Print the output of a shell command."""
        print_shell_output(output)

    @property
    def console(self) -> Console:
        """Return the rich console instance."""
        return self._console

    def print_validation_start(self, cmd_name: str) -> None:
        """Print the start of a validation check."""
        print_validation_start(cmd_name)

    def print_test_results(self, output: str, passed: bool = True) -> None:
        """Print the results of a test run."""
        print_test_results(output, passed=passed)

    def success(self, msg: str) -> None:
        """Print a success message."""
        success(msg)

    def print_assistant_response(self, response: str, markup: bool = True) -> None:
        """Print the model's response."""
        print_assistant_response(response, markup=markup)

    @contextmanager
    def status_spinner(self, message: str, status_type: str = "thinking"):
        """Context manager for showing a status spinner."""
        with status_spinner(message, status_type):
            yield


# =============================================================================
# EARLY STREAMING REJECTION - Detect bad patterns during streaming
# =============================================================================

# Check interval (every N tokens) - lower = more responsive to bad patterns
_STREAM_CHECK_INTERVAL = 15  # Reduced for faster garbage detection

# Pre-display validation: Hold first N tokens before showing anything
# This prevents users from seeing garbage at all
_PRE_DISPLAY_TOKEN_COUNT = 30  # Validate before showing any output


def _is_fatal_streaming_reason(reason: str) -> bool:
    """Return True when a streaming validation failure must abort immediately."""
    reason_lower = reason.lower()
    fatal_markers = (
        "invalid xml tool syntax",
        "invalid yaml tool syntax",
        "non-standard tool syntax",
        "described tool",
        "malformed tool command",
        "tool refusal",
        "argumentative behavior",
        "garbage repetitive path",
        "excessive repetition of path segment",
        "repeated identical tool command",
        "repeated identical content",
        "repeated identical path-like content",
        "hypothetical/speculative",
        "conventional path patterns",
        "fabrication detected",
        "excessive repetitive content",
        "output too long without valid file operations",
    )
    return any(marker in reason_lower for marker in fatal_markers)


def _detect_bad_streaming_patterns(
    content: str,
    tool_calls: list | None = None,
) -> tuple[bool, str]:
    """Detect patterns that should abort streaming early.

    Checks for:
    1. Invalid tool syntax (XML tags, YAML tool declarations, function calls)
    2. Garbage repetitive paths (same segment repeated many times)
    3. Tool refusal patterns (claims tools don't work)
    4. Argumentative/blocking behavior (asking for input instead of working)
    5. Non-standard tool syntax (read_file(), Command:, Action:)

    Args:
        content: The content to check
        tool_calls: Optional list of parsed ToolCall objects. When provided,
                   the validator becomes tool-aware and skips false positives
                   for legitimate batch reads (P1-4).

    Returns:
        Tuple of (is_bad, reason) - if is_bad, streaming should abort
    """
    raw_content = content
    # Native READ:/SEARCH:/RUN: lines as actually emitted by the model — before normalization
    # turns <execute_bash> into RUN: (which must not whitelist away XML validation).
    has_native_sage_tool_lines = bool(
        re.search(r"^(?:\s*[-*]\s*)?(READ|SEARCH|RUN):\s*\S", raw_content, re.MULTILINE)
    )
    # <execute_bash>...</execute_bash> is converted to `RUN: ...` in normalize_tool_command_syntax.
    # Do not reject it here: weak local models often emit only XML-wrapped shell with no prior READ: line;
    # rejecting the stream made their output look "empty" to the user. Remaining tags below stay strict.
    # tool_call / function_call wrappers must stay invalid even when inner text normalizes to READ:/SEARCH:
    if re.search(r"</?tool_call\b", raw_content, re.IGNORECASE):
        return True, "Invalid XML tool syntax detected: <tool_call>"
    if re.search(r"<function_call\b", raw_content, re.IGNORECASE):
        return True, "Invalid XML tool syntax detected: <function_call>"
    content = normalize_tool_command_syntax(content)
    # Strip stray XML stubs only when the model already emitted native READ:/SEARCH:/RUN: lines.
    if has_native_sage_tool_lines:
        content = re.sub(
            r"<execute_tool>\s*(?:read|search|run|file)\s*</execute_tool>\s*",
            "",
            content,
            flags=re.IGNORECASE | re.MULTILINE,
        )
        content = re.sub(r"<execute_tool>\s*</execute_tool>\s*", "", content, flags=re.IGNORECASE)

    content_lower = content.lower()

    # Allow incomplete XML tool blocks to finish streaming so we can normalize them
    # (e.g., when the first 30 tokens only include "<execute_tool>" and the YAML payload arrives later).
    def _tag_balance(tag: str) -> int:
        open_count = len(re.findall(rf"<{tag}>", content, re.IGNORECASE))
        close_count = len(re.findall(rf"</{tag}>", content, re.IGNORECASE))
        return open_count - close_count

    unclosed_execute_tool = _tag_balance("execute_tool") > 0
    unclosed_execute_bash = _tag_balance("execute_bash") > 0
    unclosed_tool_call = _tag_balance("tool_call") > 0
    has_unclosed_xml_block = unclosed_execute_tool or unclosed_execute_bash or unclosed_tool_call

    if has_unclosed_xml_block:
        # If the model never closes the tag, abort once it becomes clear it's not transient.
        if len(content) >= 800:
            if unclosed_execute_tool:
                return True, "Unterminated XML tool block detected: <execute_tool>"
            if unclosed_execute_bash:
                return True, "Unterminated XML tool block detected: <execute_bash>"
            return True, "Unterminated XML tool block detected: <tool_call>"
        # Otherwise, keep streaming until we can normalize the completed block.
        return False, ""

    # P1-2: Detect blank/empty tool commands early
    # These patterns catch "READ:\n", "SEARCH:\n", "RUN:\n" without arguments
    # P1-2b: Also detect malformed tool commands where READ: is followed by
    # explanatory text instead of a file path (e.g., "READ: The user is...")
    blank_command_patterns = [
        r"^READ:\s*$",  # READ: with nothing after (end of line)
        r"^SEARCH:\s*$",  # SEARCH: with nothing after
        r"^RUN:\s*$",  # RUN: with nothing after
    ]

    # Count blank commands - only reject if there are multiple (3+) consecutive
    blank_count = 0
    for pattern in blank_command_patterns:
        blank_count += len(re.findall(pattern, content, re.MULTILINE))

    if blank_count >= 3:
        return (
            True,
            "Multiple blank/empty tool commands detected. Tool commands must have arguments like 'READ: path/to/file.py'.",
        )

    # P1-2c: Detect malformed tool commands where READ/SEARCH/RUN is followed by
    # explanatory English text instead of a valid argument
    # Valid: "READ: sage/main.py" or "READ: ./src/utils.py"
    # Invalid: "READ: The user is..." or "READ: I will read..."
    malformed_tool_patterns = [
        # READ: followed by English words (not paths)
        r"^READ:\s+(?:The|I|This|To|By|Let|Now|First|Next|Here|We|You|My|In|For|As|So|If|When|While|Since|After|Before)\s",
        # SEARCH: followed by English sentence starters
        r"^SEARCH:\s+(?:The|I|This|To|By|Let|Now|First|Next|Here|We|You|My|In|For|As|So|If|When|While|Since|After|Before)\s",
        # RUN: followed by English sentence starters
        r"^RUN:\s+(?:The|I|This|To|By|Let|Now|First|Next|Here|We|You|My|In|For|As|So|If|When|While|Since|After|Before)\s",
    ]
    for pattern in malformed_tool_patterns:
        if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            return (
                True,
                "Malformed tool command detected. Use 'READ: path/to/file.py', not 'READ: explanation text'.",
            )

    # 1. Invalid tool syntax - XML-style tags (skip only when native sage lines exist — cleaned above)
    if not has_native_sage_tool_lines:
        xml_tool_patterns = [
            r"<execute_tool>",
            r"<execute_bash>",
            r"<tool_call>",
            r"<function_call",  # Match <function_call with or without attributes
            r"</execute_tool>",
            r"</execute_bash>",
            r"</tool_call>",
            r"</function_call>",
        ]
        for pattern in xml_tool_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True, f"Invalid XML tool syntax detected: {pattern}"

    # 2. Invalid tool syntax - YAML-style (skip when model already emitted native sage tools)
    if not has_native_sage_tool_lines:
        yaml_tool_patterns = [
            r"tool_name:\s*\w+",
            r"parameters:\s*\n",
            r"function:\s*\w+",
        ]
        for pattern in yaml_tool_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True, "Invalid YAML tool syntax detected"

    # 3. NON-STANDARD TOOL SYNTAX - function call style
    # Detects: read_file("path"), Command: read_file(), Action: Read, etc.
    nonstandard_tool_patterns = [
        r"\bread_file\s*\(",  # read_file("...")
        r"\bsearch_files?\s*\(",  # search_file("...")
        r"\brun_command\s*\(",  # run_command("...")
        r"\bexecute_command\s*\(",  # execute_command("...")
        r"\*\*Command:\*\*\s*\w+",  # **Command:** read_file
        r"\*\*Action:\*\*\s*\w+",  # **Action:** Read
        r"^Command:\s*\w+",  # Command: read_file
        r"^Action:\s*\w+",  # Action: Read
        r"Tool:\s*read",  # Tool: read
        r"Tool:\s*search",  # Tool: search
        r"Tool:\s*run",  # Tool: run
        # Note: Described tool patterns moved to separate check below (P1-7)
        # Note: Removed print() detection - it triggers false positives on code in markdown blocks
        # Bare `ls`/`cat`/`tree` lines are normalized to RUN: via _normalize_bare_shell_command_lines
    ]

    # P1-7: Separate check for DESCRIBED tools (higher priority, clearer message)
    described_tool_patterns = [
        r"I (?:will|would|'ll|'m going to) (?:use|call|invoke|execute)\s+(?:the\s+)?(?:READ|WRITE|SEARCH|RUN|BASH)",
        r"I (?:should|need to|have to|must) (?:use|call|invoke|execute)\s+(?:the\s+)?(?:READ|WRITE|SEARCH|RUN|BASH)",
        r"Let me (?:use|call|invoke|execute)\s+(?:the\s+)?(?:READ|WRITE|SEARCH|RUN|BASH)",
        r"I'll (?:use|call|invoke|execute)\s+(?:the\s+)?(?:READ|WRITE|SEARCH|RUN|BASH)",
        r"I'm going to (?:use|call|invoke|execute)\s+(?:the\s+)?(?:READ|WRITE|SEARCH|RUN|BASH)",
        r"(?:Using|Calling|Invoking) the (?:READ|WRITE|SEARCH|RUN|BASH) (?:tool|command)",
        r"First,? (?:I'll|I will|let me) (?:use|read|search|run)",
        r"Now (?:I'll|I will|let me) (?:use|read|search|run)",
        r"Next,? (?:I'll|I will|let me) (?:use|read|search|run)",
        r"To do this,? (?:I'll|I will|I need to) (?:use|read|search|run)",
    ]
    for pattern in described_tool_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return (
                True,
                "Non-standard syntax: DESCRIBED TOOL detected. Don't say 'I will use READ' — just execute READ: directly!",
            )

    for pattern in nonstandard_tool_patterns:
        if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            return (
                True,
                "Non-standard tool syntax detected. Use READ:, SEARCH:, RUN: format instead.",
            )

    # 3b. Repeated identical tool commands usually indicate a stuck loop, not progress.
    # Distinct batched READ:/SEARCH:/RUN: lines are still allowed.
    normalized_tool_lines = [
        re.sub(r"\s+", " ", match.group(0).strip())
        for match in re.finditer(r"^(READ|SEARCH|RUN):\s+\S.*$", content, re.MULTILINE)
    ]
    for line in set(normalized_tool_lines):
        if normalized_tool_lines.count(line) >= 6:
            return (
                True,
                f"Repeated identical tool command detected: {line[:80]}",
            )

    # 3c. Repeated long prose lines usually indicate a degenerative loop.
    prose_lines: list[str] = []
    in_code_block = False
    for raw_line in content.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if (
            in_code_block
            or not stripped
            or stripped.startswith(("READ:", "SEARCH:", "RUN:", "FILE:", "RESULT:"))
            or len(stripped) < 40
        ):
            continue
        prose_lines.append(re.sub(r"\s+", " ", stripped))

    for line in set(prose_lines):
        if prose_lines.count(line) >= 4:
            return (
                True,
                "Repeated identical content detected. Stop looping and execute grounded work.",
            )

    # 3d. Repeated short path-like lines usually indicate a degenerate copy loop.
    path_like_lines: list[str] = []
    in_code_block = False
    for raw_line in content.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if (
            in_code_block
            or not stripped
            or stripped.startswith(("READ:", "SEARCH:", "RUN:", "FILE:", "RESULT:"))
        ):
            continue
        normalized = stripped.strip("`")
        if re.fullmatch(
            r"(?:[\w.-]+/)*[\w.-]+\.(?:py|js|ts|tsx|jsx|json|yaml|yml|toml|md|txt|sh|sql|go|rs|java|css|html)",
            normalized,
            re.IGNORECASE,
        ):
            path_like_lines.append(normalized)

    for line in set(path_like_lines):
        if path_like_lines.count(line) >= 6:
            return (
                True,
                "Repeated identical path-like content detected. Stop looping and execute grounded work.",
            )

    # 4. Garbage repetitive paths - same directory repeated many times
    # Match BOTH single-segment and multi-segment repetitions:
    # - Single segment: "foo/foo/foo/foo/"
    # - Multi-segment: "ai-platform/backend/ai-platform/backend/ai-platform/backend/"
    #
    # P1-4: Skip this check when tool_calls are provided and valid.
    # Multiple READ: commands targeting the same directory are legitimate,
    # not garbage repetition.
    # Skip when READ:/SEARCH: lines exist (normalized). RUN-only blocks from <execute_bash>
    # normalization must NOT suppress repetitive-path detection.
    has_read_or_search_lines = bool(
        re.search(r"^(?:\s*[-*]\s*)?(READ|SEARCH):\s*\S", content, re.MULTILINE)
    )
    skip_repetitive_check = bool(tool_calls) or has_read_or_search_lines

    if not skip_repetitive_check:
        # Single segment pattern (original): e.g., foo/foo/foo/foo/
        repetitive_single = re.search(r"([\w-]+/)(\1){3,}", content)
        if repetitive_single:
            return True, f"Garbage repetitive path detected: {repetitive_single.group(0)[:50]}..."

        # Multi-segment pattern: e.g., ai-platform/backend/ai-platform/backend/ (2+ segments repeated 3+ times)
        # This catches "dir1/dir2/dir1/dir2/dir1/dir2/" patterns
        repetitive_multi = re.search(r"(([\w-]+/){1,3})(\1){2,}", content)
        if repetitive_multi:
            return True, f"Garbage repetitive path detected: {repetitive_multi.group(0)[:60]}..."

        # Also detect if the same path segment appears an excessive number of times (10+)
        # This catches edge cases where there's slight variation but still garbage
        if "/" in content:
            path_parts = content.split("/")
            for part in set(path_parts):
                if not part:
                    continue
                normalized = part.strip().lower()
                if normalized in {"src", "app", "apps", "lib", "libs", "test", "tests"}:
                    continue
                threshold = 20 if len(normalized) <= 4 else 10
                if len(part) > 2 and path_parts.count(part) >= threshold:
                    return (
                        True,
                        f"Excessive repetition of path segment '{part}' ({path_parts.count(part)}+ times)",
                    )

    # 4b. Tool refusal during streaming (MOVED BEFORE hypothetical check)
    # This ensures "cannot execute ... I will assume" is caught as refusal, not hypothetical
    refusal_patterns = [
        "cannot execute the read",  # "cannot execute the read command/commands"
        "cannot perform read",  # "cannot perform read operations"
        "tool commands will not work",
        "tool commands don't work",  # "don't work here/in this context"
        "tool commands do not work",  # "do not work here/in this context"
        "cannot run the read",  # "cannot run the read tool/command"
        "cannot access the file",  # "cannot access the file system/files"
        "unable to execute tool",  # "unable to execute tool commands"
        "i am unable to execute",  # "i am unable to execute tools"
        "tools are not available",
        "read command is not available",
    ]
    for pattern in refusal_patterns:
        if pattern in content_lower:
            return True, f"Tool refusal detected: '{pattern}'"

    # Obvious fabrication phrases — reject even when the response is short (no 400-char gate).
    high_confidence_speculative = [
        r"\bimplied context\b",
        r"not provided,\s*but implied",
        r"not provided but implied",
        r"not provided,\s*but the context suggests",
        r"hypothetical\s+(?:structure|plan|analysis|codebase)",
        r"if you can provide",
        r"if you cannot provide",
    ]
    for pattern in high_confidence_speculative:
        if re.search(pattern, content_lower):
            return (
                True,
                "Hypothetical/speculative content detected. Use READ: to get actual file contents.",
            )

    # 4c. HYPOTHETICAL/SPECULATIVE CONTENT
    # Detect when model generates hypothetical plans or asks for files instead of reading
    # Check for tool commands in the content - if present, be more lenient
    has_tool_commands = bool(re.search(r"^(SEARCH|READ|RUN):\s+\S", content, re.MULTILINE))

    hypothetical_patterns = [
        r"hypothetical\s+(?:structure|plan|analysis|codebase)",
        r"implied context",
        r"not provided,\s*but implied",
        r"not provided but implied",
        r"not provided,\s*but the context suggests",
        r"if you can provide",
        r"if you cannot provide",
        r"once the context is established",
        r"once the code is available",
        r"please provide the code",
        r"please upload",
        r"i require the actual",
        r"i need the actual source",
        r"without the actual (?:code|files|source)",
        r"no actual file system",
        r"no actual context",
        r"purely speculative",
        r"assuming a standard",
        r"assuming the existence",
        r"i will assume",
        # More specific patterns to avoid false positives
        r"cannot proceed without",
    ]

    # If model has executed tools, only flag the strongest patterns
    if has_tool_commands:
        # With tools executed, only flag explicit refusals
        # Note: omit "i will assume" — models legitimately reason from READ output with that phrase.
        strong_patterns = [
            r"cannot proceed without",
            r"purely speculative",
            r"no actual context",
            r"without the actual (?:code|files|source)",
            r"assuming the existence",
            r"please provide the code",
            r"i need the actual source",
        ]
        for pattern in strong_patterns:
            if re.search(pattern, content_lower):
                return (
                    True,
                    "Hypothetical/speculative content detected. Use READ: to get actual file contents.",
                )
    else:
        # Without tools, avoid aborting on tiny preambles only (hypothetical cues are short).
        if len(content) >= 35:
            for pattern in hypothetical_patterns:
                if re.search(pattern, content_lower):
                    return (
                        True,
                        "Hypothetical/speculative content detected. Use READ: to get actual file contents.",
                    )

    # 4c. DETECT GUESSED CONVENTIONAL PATHS
    # Model often guesses paths like src/main.py, ./src/utils/ that don't exist
    # This is a heuristic - if we see many "conventional" paths without any actual reads, flag it
    guessed_path_patterns = [
        r"\./src/",  # ./src/ prefix
        r"src/main\.py",  # src/main.py
        r"src/utils/",  # src/utils/
        r"src/services/",  # src/services/
        r"src/models/",  # src/models/
        r"src/api/",  # src/api/
        r"src/config/",  # src/config/
        r"src/components/",  # src/components/
        r"app/main\.py",  # app/main.py
        r"app/utils/",  # app/utils/
        r"lib/main",  # lib/main
    ]
    guessed_count = sum(1 for p in guessed_path_patterns if re.search(p, content))
    # If 3+ conventional paths are mentioned without any READ: commands, likely guessing
    # Require enough content that this isn't an early-stream partial before the READ batch.
    if (
        guessed_count >= 3
        and not re.search(r"^READ:\s+", content, re.MULTILINE)
        and len(content) >= 200
    ):
        return (
            True,
            f"Detected {guessed_count} conventional path patterns (src/main.py, etc.) without reading files. These paths likely don't exist. Use SEARCH: *.py to find actual files.",
        )

    # 5. ARGUMENTATIVE/BLOCKING BEHAVIOR - Model asking for input instead of working
    argumentative_patterns = [
        "please provide the output",
        "please share the output",
        "please paste the output",
        "please provide the file contents",
        "please share the file contents",
        "please share the contents",
        "i need you to provide",
        "i need the file contents",
        "could you provide the",
        "could you share the",
        "can you provide the",
        "can you share the",
        "waiting for the output",
        "waiting for you to",
        "please run the command",
        "please execute the",
        "once you provide",
        "once you share",
        "before i can proceed",
        "before i can continue",
        "before proceeding",
        "i cannot proceed without",
        "cannot continue without",
        "need you to run",
        "need you to execute",
        "shall i proceed with",
        "should i proceed with",
        "do you want me to proceed",
        "do you want me to implement",
        "would you like me to proceed",
        "would you like me to implement",
        "do you approve proceeding",
        "do you approve of proceeding",
        "awaiting your approval",
        "awaiting approval to",
        "please confirm if i should",
        "please confirm that i should",
        "let me know if you want me to",
        "let me know if i should proceed",
        "would you like me to continue",
        "would you like me to proceed",
        # Patterns for blocking behavior
        "please provide the following",
        "i need to know which files",
        "awaiting the file contents",
        "please provide the context",
        "i need the list of tasks",
        "i am ready to proceed",
        "i understand the request",
        "i understand the requirement",
        "no file structure or initial context",
        "since no file structure",
        "has not been provided",
        "have not yet received",
        "i have not yet received",
        "without the code context",
        "without the actual contents",
        "any list i generate would be",
        "pure speculation",
    ]
    for pattern in argumentative_patterns:
        if pattern in content_lower:
            return (
                True,
                f"Argumentative behavior detected: '{pattern}'. Execute tools directly with READ:/SEARCH:/RUN:",
            )

    # 7. CONTEXT OVERFLOW PROTECTION - Detect excessively long output without valid commands
    # If output exceeds ~2000 chars without any valid tool commands, likely garbage
    if len(content) > 2000:
        has_any_tool_command = bool(re.search(r"^(READ|SEARCH|RUN):\s+\S", content, re.MULTILINE))
        if not has_any_tool_command:
            # Check if it's just repeated garbage or prose
            unique_words = set(content.lower().split())
            word_count = len(content.split())
            # If word count is high but unique words are low, it's repetitive garbage
            if word_count > 50 and len(unique_words) < word_count * 0.3:
                return (
                    True,
                    f"Excessive repetitive content detected ({word_count} words, only {len(unique_words)} unique)",
                )

    # 7b. Absolute length limit - abort if output exceeds 8000 chars without progress
    # Allow long responses that contain thinking blocks (<thinking>...</thinking>) — thinking
    # models like gemma4 produce verbose reasoning before emitting FILE:/READ: content.
    # Also allow responses that contain FILE: blocks (implementation output).
    if len(content) > 8000:
        has_file_evidence = bool(
            re.search(r"^READ:\s+[\w./]+", content, re.MULTILINE)
            or re.search(r"^FILE:\s+[\w./]", content, re.MULTILINE)
            or re.search(r"<thinking>", content, re.IGNORECASE)
            or re.search(r"^SEARCH:\s+\S", content, re.MULTILINE)
            or re.search(r"^RUN:\s+\S", content, re.MULTILINE)
        )
        if not has_file_evidence:
            return True, "Output too long without valid file operations - possible context overflow"

    numbered_items = re.findall(r"^\s*\d+\.\s+", content, re.MULTILINE)
    has_read_commands = bool(re.search(r"^READ:\s+", content, re.MULTILINE))
    has_search_commands = bool(re.search(r"^SEARCH:\s+", content, re.MULTILINE))
    has_tool_execution = has_read_commands or has_search_commands

    # Numbered "audit" lists that cite line numbers before any READ: are often early-stream
    # summaries that precede a tool batch — don't abort until the response is long enough
    # that skipping tools is clearly intentional.
    _MIN_CONTENT_FOR_GROUNDED_FABRICATION = 900
    if len(numbered_items) >= 4 and not has_tool_execution:
        mentions_grounded_claims = bool(
            re.search(
                r"(\bat line\b|\bfound in\b|\bimplemented in\b|\bdefined in\b|\bimports from\b|\bline numbers\b|\b:\s*line\b|\bline\s*\d+\b|\bL\d+\b)",
                content_lower,
            )
        )
        if mentions_grounded_claims and len(content) >= _MIN_CONTENT_FOR_GROUNDED_FABRICATION:
            return (
                True,
                f"Fabrication detected: {len(numbered_items)} items generated without file evidence. Execute READ: or SEARCH: first.",
            )
        # Long generic numbered lists (weak models spam recommendations without reading).
        # Short/medium numbered plans (e.g. 7-step env fixes, auth checklists) are normal for coding tasks.
        if len(numbered_items) >= 10 and len(content) >= 450:
            return (
                True,
                f"Fabrication detected: {len(numbered_items)} items generated without file evidence. Execute READ: or SEARCH: first.",
            )

    return False, ""


_no_color_enabled = False


class _BottomDockStream(TextIOBase):
    """A stream wrapper that keeps a Claude Code–style footer pinned to the bottom.

    Log output remains in normal terminal scrollback while the footer is redrawn
    after each write, so the upper log stays scrollable and the todo list/input
    hint remain visually anchored at the bottom of the viewport.
    """

    def __init__(self, target: TextIOBase):
        self._target = target
        self._lock = threading.RLock()
        self._footer_lines = 0
        self._status_message = "Working..."
        self._prompt_message = "Working..."
        self._todos: list[dict] = []
        self._active = False
        self._rendering_footer = False
        self._cursor_at_start = True

    @property
    def encoding(self) -> str | None:  # pragma: no cover - passthrough property
        return getattr(self._target, "encoding", None)

    def fileno(self) -> int:  # pragma: no cover - passthrough property
        return self._target.fileno()

    def isatty(self) -> bool:  # pragma: no cover - passthrough property
        return self._target.isatty()

    def flush(self) -> None:
        with self._lock:
            self._target.flush()

    def activate(
        self,
        *,
        status_message: str = "Working...",
        prompt_message: str = "Working...",
        todos: list[dict] | None = None,
    ) -> None:
        with self._lock:
            self._active = True
            self._status_message = status_message
            self._prompt_message = prompt_message
            self._todos = [dict(todo) for todo in (todos or [])]
            self._draw_footer_locked()

    def deactivate(self) -> None:
        with self._lock:
            if self._active:
                self._clear_footer_locked()
            self._active = False
            self._todos = []
            self._footer_lines = 0

    def set_status(self, message: str) -> None:
        with self._lock:
            self._status_message = message or "Working..."
            self._refresh_footer_locked()

    def set_prompt(self, message: str) -> None:
        with self._lock:
            self._prompt_message = message or "Working..."
            self._refresh_footer_locked()

    def set_todos(self, todos: list[dict] | None) -> None:
        with self._lock:
            self._todos = [dict(todo) for todo in (todos or [])]
            self._refresh_footer_locked()

    def clear_todos(self) -> None:
        with self._lock:
            self._todos = []
            self._refresh_footer_locked()

    def has_active_todos(self) -> bool:
        return any(todo.get("status") != "completed" for todo in self._todos)

    def snapshot(self, width: int | None = None) -> str:
        with self._lock:
            return self._build_footer_markup(width=width)

    def write(self, text: str) -> int:
        if not text:
            return 0

        with self._lock:
            if not self._active or self._rendering_footer:
                self._target.write(text)
                self._target.flush()
                self._cursor_at_start = text.endswith("\n")
                return len(text)

            self._clear_footer_locked()
            self._target.write(text)
            self._target.flush()
            self._cursor_at_start = text.endswith("\n")
            if self._cursor_at_start:
                self._draw_footer_locked()
            return len(text)

    def _refresh_footer_locked(self) -> None:
        if not self._active:
            return
        self._clear_footer_locked()
        if self._cursor_at_start:
            self._draw_footer_locked()

    def _clear_footer_locked(self) -> None:
        if self._footer_lines <= 0:
            return

        up_moves = self._footer_lines - 1

        if up_moves > 0:
            self._target.write(f"\r\x1b[{up_moves}F\x1b[J")
        else:
            self._target.write("\r\x1b[J")

        self._target.flush()
        self._footer_lines = 0

    def _draw_footer_locked(self) -> None:
        footer_markup = self._build_footer_markup()
        if not footer_markup:
            self._footer_lines = 0
            return

        width = shutil.get_terminal_size((100, 30)).columns
        capture = StringIO()
        footer_console = Console(
            file=capture,
            force_terminal=True,
            color_system=None if _no_color_enabled else "auto",
            no_color=_no_color_enabled,
            width=width,
            soft_wrap=False,
        )
        footer_console.print(footer_markup, markup=True, highlight=False, end="")
        rendered = capture.getvalue()

        self._footer_lines = rendered.count("\n") + 1

        self._rendering_footer = True
        try:
            self._target.write(rendered)
            self._target.flush()
        finally:
            self._rendering_footer = False

    def _build_footer_markup(self, width: int | None = None) -> str:
        todos = [dict(todo) for todo in self._todos if todo.get("content") or todo.get("name")]
        active_todos = [todo for todo in todos if todo.get("status") != "completed"]
        if not active_todos and not self._status_message:
            return ""

        columns = width or shutil.get_terminal_size((100, 30)).columns
        usable = max(32, columns - 2)
        divider = f"[#24446f]{'─' * usable}[/#24446f]"

        lines = [divider]
        if active_todos:
            lines.append("[bold #8bb8ff]  Current Plan[/bold #8bb8ff]")
            for todo in todos:
                if todo.get("status") == "completed" and not active_todos:
                    continue
                status = todo.get("status", "pending")
                content = todo.get("content") or todo.get("name") or ""
                trimmed = escape(content[: usable - 6] + ("…" if len(content) > usable - 6 else ""))
                if status == "completed":
                    icon = "[#73a7ff]✓[/#73a7ff]"
                    open_style = "[#93bbff]"
                    close_style = "[/#93bbff]"
                elif status == "in_progress":
                    icon = "[bold #b8dcff]◉[/bold #b8dcff]"
                    open_style = "[bold #d8ebff]"
                    close_style = "[/bold #d8ebff]"
                else:
                    icon = "[#6089bb]○[/#6089bb]"
                    open_style = "[#8aaed7]"
                    close_style = "[/#8aaed7]"
                lines.append(f"  {icon} {open_style}{trimmed}{close_style}")
            lines.append(divider)

        status = escape(self._status_message or "Working...")
        prompt = escape(self._prompt_message or "Working...")
        lines.append(
            f"[bold #6ea4ff]▸[/bold #6ea4ff] [bold white]{status}[/bold white] "
            f"[dim]· {prompt} · Ctrl+C to interrupt[/dim]"
        )
        return "\n".join(lines)


_bottom_dock_stream: _BottomDockStream | None = None


def _build_console(*, stderr: bool = False) -> Console:
    if _bottom_dock_stream is not None:
        return Console(
            file=_bottom_dock_stream,
            stderr=False,
            no_color=_no_color_enabled,
            color_system=None if _no_color_enabled else "auto",
        )
    if _no_color_enabled:
        return Console(stderr=stderr, no_color=True)
    return Console(stderr=stderr)


def _rebuild_consoles() -> None:
    global console, err_console
    console = _build_console(stderr=False)
    err_console = _build_console(stderr=True)


_rebuild_consoles()


def _output_stream() -> TextIOBase:
    """Return the active output stream."""
    if _bottom_dock_stream is not None:
        return _bottom_dock_stream
    return sys.stdout


def _write_output(text: str) -> None:
    """Write text through the active output stream."""
    stream = _output_stream()
    stream.write(text)
    stream.flush()


# Indicator-only mode is now integrated with clean mode - no separate flag needed


# ── Thread Safety ──────────────────────────────────────────────


def _is_main_thread() -> bool:
    """Check if the current thread is the main thread.

    Returns:
        True if running on the main thread, False otherwise
    """
    return threading.current_thread() == threading.main_thread()


def set_no_color(enabled: bool) -> None:
    """Disable ANSI colors (e.g. ``--no-color``). Recreates Rich consoles."""
    global _no_color_enabled
    _no_color_enabled = enabled
    _rebuild_consoles()


def has_bottom_dock() -> bool:
    """Return True when the Claude Code-style footer is active."""
    return _bottom_dock_stream is not None and _bottom_dock_stream._active


def activate_bottom_dock(
    *,
    todos: list[dict] | None = None,
    status_message: str = "Working...",
    prompt_message: str = "Working...",
) -> bool:
    """Enable the bottom-anchored task dock for interactive terminals."""
    global _bottom_dock_stream
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        return False
    if _bottom_dock_stream is None:
        _bottom_dock_stream = _BottomDockStream(sys.stdout)
    _bottom_dock_stream.activate(
        status_message=status_message,
        prompt_message=prompt_message,
        todos=todos,
    )
    _rebuild_consoles()
    return True


def deactivate_bottom_dock() -> None:
    """Disable the bottom-anchored task dock and restore normal consoles."""
    global _bottom_dock_stream
    if _bottom_dock_stream is None:
        return
    _bottom_dock_stream.deactivate()
    _bottom_dock_stream = None
    _rebuild_consoles()


def set_bottom_dock_status(message: str) -> None:
    """Update the live dock status line."""
    if _bottom_dock_stream is not None:
        _bottom_dock_stream.set_status(message)


def set_bottom_dock_prompt(message: str) -> None:
    """Update the live dock prompt hint."""
    if _bottom_dock_stream is not None:
        _bottom_dock_stream.set_prompt(message)


def set_bottom_dock_todos(todos: list[dict] | None) -> None:
    """Update the dock todo list in real time."""
    if _bottom_dock_stream is not None:
        _bottom_dock_stream.set_todos(todos)


def clear_bottom_dock_todos() -> None:
    """Hide the dock todo list."""
    if _bottom_dock_stream is not None:
        _bottom_dock_stream.clear_todos()


def render_bottom_dock_snapshot(
    *,
    todos: list[dict] | None = None,
    status_message: str = "Working...",
    prompt_message: str = "Working...",
    width: int = 100,
) -> str:
    """Render the current dock/footer markup without mutating terminal state."""
    preview = _BottomDockStream(StringIO())
    preview._status_message = status_message
    preview._prompt_message = prompt_message
    preview._todos = [dict(todo) for todo in (todos or [])]
    return preview.snapshot(width=width)


@contextmanager
def bottom_task_dock(
    *,
    todos: list[dict] | None = None,
    status_message: str = "Working...",
    prompt_message: str = "Working...",
):
    """Context manager for the bottom-anchored Claude Code-style task dock."""
    active = activate_bottom_dock(
        todos=todos,
        status_message=status_message,
        prompt_message=prompt_message,
    )
    try:
        yield active
    finally:
        if active:
            deactivate_bottom_dock()


# ── Output Mode Control ────────────────────────────────────
# Controls verbosity of output:
# - "clean": Default mode - only final output, no thinking/planning noise
# - "normal": Show progress phases but suppress thinking blocks
# - "verbose": Show all messages including thinking blocks (for debugging)

_output_mode: str = "clean"


def set_output_mode(mode: str) -> None:
    """Set the global output verbosity mode.

    Args:
        mode: One of "clean", "normal", or "verbose"
    """
    global _output_mode
    if mode not in ("clean", "normal", "verbose"):
        raise ValueError(f"Invalid output mode: {mode}. Must be 'clean', 'normal', or 'verbose'")
    _output_mode = mode


def get_output_mode() -> str:
    """Get the current output verbosity mode."""
    return _output_mode


def is_verbose() -> bool:
    """Check if output is in verbose mode (show everything including thinking)."""
    return _output_mode == "verbose"


def is_clean() -> bool:
    """Check if output is in clean mode (minimal output, no noise)."""
    return _output_mode == "clean"


def suppress_thinking() -> bool:
    """Check if thinking blocks should be suppressed (default: yes)."""
    return _output_mode != "verbose"


def strip_thinking_blocks(text: str) -> str:
    """Strip <thinking>...</thinking> blocks from text.

    This ensures thinking blocks are completely removed from any output,
    not just suppressed during streaming.

    Args:
        text: The text to process

    Returns:
        Text with thinking blocks removed
    """
    import re

    # Remove <thinking>...</thinking> blocks and any trailing whitespace
    cleaned = re.sub(r"<thinking>[\s\S]*?</thinking>\s*", "", text)
    return cleaned.strip()


def suppress_phases() -> bool:
    """Check if phase messages should be suppressed."""
    return _output_mode == "clean"


# Legacy compatibility
def is_quiet() -> bool:
    """Legacy: Check if in quiet mode (maps to clean)."""
    return _output_mode == "clean"


def is_minimal() -> bool:
    """Legacy: Check if in minimal mode (maps to clean/normal)."""
    return _output_mode in ("clean", "normal")


# ── Phase & Status Display ─────────────────────────────────


# Phase icons and colors for the agent workflow
_PHASE_STYLES = {
    "thinking": ("bold #9cc3ff", "◌"),
    "planning": ("bold #8bb8ff", "◎"),
    "reading": ("bold #b8dcff", "◍"),
    "coding": ("bold #c8b9ff", "◆"),
    "writing": ("bold #8fcd9d", "▸"),
    "testing": ("bold #d7bb83", "◈"),
    "fixing": ("bold #ef7f8c", "↺"),
    "executing": ("bold #8ec5ff", "▹"),
    "validating": ("bold #dce8ff", "◇"),
    "done": ("bold #8fcd9d", "✓"),
    "error": ("bold #ef7f8c", "✕"),
}


def phase(name: str, detail: str = "") -> None:
    """Print a phase indicator with icon and optional detail.

    Respects output mode:
    - clean: Only shows critical phases (done, error)
    - normal: Shows important phases (done, error, writing, reading)
    - verbose: Shows all phases
    """
    if has_bottom_dock():
        summary = f"{name.capitalize()}: {detail}" if detail else name.capitalize()
        set_bottom_dock_status(summary)

    if is_clean():
        # In clean mode, only show done/error
        if name not in ("done", "error"):
            return
    elif not is_verbose():
        # In normal mode, show essential phases only
        if name not in ("done", "error", "writing", "reading"):
            return
    style, icon = _PHASE_STYLES.get(name, ("dim", "·"))
    detail_str = f"  [dim]{detail}[/dim]" if detail else ""
    console.print(f"  [{style}]{icon} {name.capitalize()}[/{style}]{detail_str}")


@contextmanager
def status_spinner(message: str, phase_name: str = "thinking"):
    """Context manager that shows a Rich spinner with a message.

    Usage:
        with status_spinner("Analyzing your request..."):
            do_work()
    """
    if has_bottom_dock():
        set_bottom_dock_status(message)
        yield
        return

    style, icon = _PHASE_STYLES.get(phase_name, ("dim", "·"))
    spinner = Spinner("dots", text=Text.from_markup(f"  [{style}]{icon} {message}[/{style}]"))
    with Live(spinner, console=console, refresh_per_second=12, transient=True):
        yield


def step(number: int, total: int, description: str, style: str = "bold cyan") -> None:
    """Print a numbered step indicator."""
    console.print(f"  [{style}]Step {number}/{total}[/{style}] [dim]─[/dim] {description}")


def step_done(description: str) -> None:
    """Print a completed step."""
    console.print(f"  [green]✓[/green] {description}")


def step_fail(description: str) -> None:
    """Print a failed step."""
    console.print(f"  [red]✗[/red] {description}")


def divider(title: str = "", style: str = "dim") -> None:
    """Print a horizontal divider."""
    if title:
        console.print(Rule(title, style=style))
    else:
        console.print(Rule(style=style))


def print_assistant_response(content: str, *, markup: bool = False) -> None:
    """Print a complete assistant response in one atomic console write."""
    text = str(content)
    if suppress_thinking():
        text = strip_thinking_blocks(text)
    if not text.strip():
        return
    prefix = Text("sage> ", style="bold #6ea4ff")
    body = Text.from_markup(text) if markup else Text(text)
    console.print(prefix, body, sep="")
    console.print()


# ── Indicator-Only Mode Progress ──────────────────────────


@contextmanager
def sage_operation(operation: str, show_spinner: bool = True):
    """Context manager for SAGE operations - shows indicators in clean mode.

    Args:
        operation: Description of the operation (e.g., "Analyzing codebase")
        show_spinner: Whether to show a spinner during the operation

    Usage:
        with sage_operation("Reading files"):
            # do work
            pass
    """
    if has_bottom_dock():
        set_bottom_dock_status(operation)
        yield
    elif is_clean():
        # Clean mode: show progress indicator only
        if show_spinner:
            spinner = Spinner(
                "dots", text=Text.from_markup(f"  [bold cyan]●[/bold cyan] {operation}...")
            )
            with Live(spinner, console=console, refresh_per_second=12, transient=True):
                yield
        else:
            console.print(f"  [bold cyan]●[/bold cyan] {operation}...")
            yield
    else:
        # Normal/verbose mode: no extra output (calling code handles it)
        yield


def sage_step_complete(operation: str, result: str = "") -> None:
    """Mark a SAGE operation step as complete - only shown in clean mode.

    Args:
        operation: Description of what completed
        result: Optional result description
    """
    if is_clean():
        if result:
            console.print(f"  [green]✓[/green] {operation} → {result}")
        else:
            console.print(f"  [green]✓[/green] {operation}")


def sage_step_failed(operation: str, reason: str = "") -> None:
    """Mark a SAGE operation step as failed - only shown in clean mode.

    Args:
        operation: Description of what failed
        reason: Optional failure reason
    """
    if is_clean():
        if reason:
            console.print(f"  [red]✗[/red] {operation} → {reason}")
        else:
            console.print(f"  [red]✗[/red] {operation}")


def sage_final_output(content: str) -> None:
    """Show final output in clean mode.

    Args:
        content: The final output content to display
    """
    if is_clean():
        console.print()
        console.print(
            Panel(content, title="[bold green]Final Output[/bold green]", border_style="green")
        )
    else:
        # In normal/verbose mode, output is already shown
        pass


# ── Streaming with stats ───────────────────────────────────

# Streaming buffer settings for optimal performance
_STREAM_BUFFER_SIZE = 8  # Flush after this many tokens
_STREAM_FLUSH_INTERVAL = 0.05  # Or flush after this many seconds


def stream_tokens(tokens: Iterator[str], show_stats: bool = True) -> str:
    """Print tokens to stdout in real-time and return the full text.

    Uses buffered output with periodic flushes for better performance
    while maintaining responsiveness. Flushes every 8 tokens or 50ms.

    Tracks timing and token count for display after streaming completes.
    Ctrl+C cancels generation and returns what was collected so far.
    """
    parts: list[str] = []
    token_count = 0
    t0 = time.monotonic()
    last_flush = t0
    buffer: list[str] = []
    cancelled = False

    def _flush_buffer() -> None:
        nonlocal last_flush
        if buffer:
            _write_output("".join(buffer))
            buffer.clear()
            last_flush = time.monotonic()

    try:
        for token in tokens:
            buffer.append(token)
            parts.append(token)
            token_count += 1

            # Flush on buffer size or time interval
            now = time.monotonic()
            if len(buffer) >= _STREAM_BUFFER_SIZE or (now - last_flush) >= _STREAM_FLUSH_INTERVAL:
                _flush_buffer()

    except KeyboardInterrupt:
        cancelled = True

    # Final flush
    _flush_buffer()

    elapsed = time.monotonic() - t0
    _write_output("\n")

    if cancelled:
        console.print("  [dim yellow]─ Cancelled (Ctrl+C)[/dim yellow]")
    elif show_stats and token_count > 0 and elapsed > 0.1:
        tps = token_count / elapsed if elapsed > 0 else 0
        console.print(f"  [dim]─ {token_count} tokens · {elapsed:.1f}s · {tps:.0f} tok/s[/dim]")

    return "".join(parts)


def stream_tokens_with_phase(
    tokens: Iterator[str],
    model_id: str = "",
    return_rejection_info: bool = False,
    first_token_timeout: float = 0.0,
) -> str | tuple[str, bool, str]:
    """Stream tokens with a thinking spinner that transitions to output.

    Shows 'Thinking...' spinner until first token arrives, then streams normally.
    Uses buffered output with periodic flushes for better performance.
    Ctrl+C cancels generation at any point — during thinking or streaming.

    Output mode behavior:
    - clean: Show only a spinner, suppress ALL streaming output. Returns full response.
    - normal: Show progress phases, suppress thinking blocks, stream output.
    - verbose: Show everything including thinking blocks.

    Args:
        tokens: Iterator of tokens from the model
        model_id: Model identifier for display
        return_rejection_info: If True, returns (response, was_rejected, reason)
        first_token_timeout: Seconds to wait for first token (P0-1: prevents hangs)

    Returns:
        If return_rejection_info is False: response string (empty if rejected)
        If return_rejection_info is True: (response, was_rejected, rejection_reason)

    Raises:
        StreamingTimeoutError: If no token received within first_token_timeout (P0-1)

    Uses a SIGINT handler to reliably catch Ctrl+C even inside Rich.Live,
    which can swallow KeyboardInterrupt in its refresh thread.
    """
    parts: list[str] = []
    buffer: list[str] = []
    token_count = 0
    t0 = time.monotonic()
    last_flush = t0
    first_token_time = None
    cancelled = False

    # In clean mode, suppress ALL streaming output - just show spinner
    clean_mode = is_clean()
    should_suppress_thinking = suppress_thinking()  # Suppress unless verbose mode
    think_filter: _ThinkingSuppressionFilter | None = (
        _ThinkingSuppressionFilter() if should_suppress_thinking else None
    )

    def _flush_buffer() -> None:
        nonlocal last_flush
        if buffer and not clean_mode:  # Don't flush in clean mode
            _write_output("".join(buffer))
            buffer.clear()
            last_flush = time.monotonic()

    # Install a SIGINT handler that sets a flag — Rich.Live can swallow
    # KeyboardInterrupt, but our handler always fires.
    # CRITICAL: Only install signal handlers on the main thread to avoid crashes
    _sigint_received = False
    _original_handler = None
    _on_main_thread = _is_main_thread()

    def _handle_sigint(signum, frame):
        nonlocal _sigint_received
        _sigint_received = True

    # Only install signal handler if we're on the main thread
    if _on_main_thread:
        _original_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, _handle_sigint)

    # In clean mode, always show spinner (processing indicator)
    # In verbose mode, show thinking spinner
    # In normal mode, no spinner (phases shown by caller)
    show_spinner = (clean_mode or is_verbose()) and not has_bottom_dock()
    spinner_text = (
        "  [bold cyan]● Processing...[/bold cyan]  [dim](Ctrl+C to cancel)[/dim]"
        if clean_mode
        else "  [bold yellow]⟡ Thinking...[/bold yellow]  [dim](Ctrl+C to cancel)[/dim]"
        + (f"  [dim]({model_id})[/dim]" if model_id else "")
    )
    spinner = Spinner("dots", text=Text.from_markup(spinner_text))
    live = Live(spinner, console=console, refresh_per_second=12, transient=True)
    if show_spinner:
        live.start()

    # Track if response was rejected due to bad patterns
    streaming_rejected = False
    rejection_reason = ""
    # PRE-DISPLAY VALIDATION: Hold tokens until we pass initial validation
    pre_display_validated = False
    held_display_tokens: list[str] = []

    try:
        tokens_iter = iter(tokens)
        has_first_token, first_token = _next_token_with_timeout(tokens_iter, first_token_timeout)
        token_stream = chain([first_token], tokens_iter) if has_first_token else iter(())

        for token in token_stream:
            if _sigint_received:
                cancelled = True
                break

            # Always capture the full response (including thinking) for callers
            parts.append(token)
            token_count += 1

            # PRE-DISPLAY VALIDATION: Check BEFORE showing anything to user
            # P1-2e: Be more lenient - only abort for truly fatal patterns
            # Recoverable issues (blank commands, malformed syntax) are handled post-stream
            if not pre_display_validated and token_count >= _PRE_DISPLAY_TOKEN_COUNT:
                current_content = "".join(parts)
                # P1-1: Parse tool commands incrementally to provide context to validator
                # This prevents false positives on legitimate batch reads
                incremental_tool_calls = _parse_incremental_tool_calls(current_content)
                is_bad, reason = _detect_bad_streaming_patterns(
                    current_content, tool_calls=incremental_tool_calls
                )
                if is_bad:
                    # Abort immediately for severe looping, refusal, fabrication,
                    # or syntax failures so users never see the garbage stream.
                    is_fatal = _is_fatal_streaming_reason(reason)

                    if is_fatal:
                        streaming_rejected = True
                        rejection_reason = reason
                        # Stop the spinner and show rejection message
                        if live.is_started:
                            live.stop()
                        if is_verbose():
                            console.print()
                            console.print(
                                f"  [bold red]❌ PRE-DISPLAY VALIDATION FAILED:[/bold red] {reason}"
                            )
                            console.print(
                                "  [dim]Bad response detected before display. No garbage shown.[/dim]"
                            )
                        break
                    else:
                        # Log warning but continue - cleanup will handle it
                        # Don't show to user, just note for debugging
                        pass
                pre_display_validated = True

            # PERIODIC DETECTION - continue checking after initial validation
            # P1-2g: Be lenient - only abort for fatal patterns, let others through for cleanup
            if pre_display_validated and token_count % _STREAM_CHECK_INTERVAL == 0:
                current_content = "".join(parts)
                # P1-1: Parse tool commands incrementally to provide context to validator
                incremental_tool_calls = _parse_incremental_tool_calls(current_content)
                is_bad, reason = _detect_bad_streaming_patterns(
                    current_content, tool_calls=incremental_tool_calls
                )
                if is_bad:
                    is_fatal = _is_fatal_streaming_reason(reason)

                    if is_fatal:
                        streaming_rejected = True
                        rejection_reason = reason
                        # Stop the spinner and show rejection message
                        if live.is_started:
                            live.stop()
                        if is_verbose():
                            console.print()
                            console.print(f"  [bold red]❌ STREAMING ABORTED:[/bold red] {reason}")
                            console.print(
                                "  [dim]The model produced invalid output. Stopping generation.[/dim]"
                            )
                        break
                    # Non-fatal issues - continue streaming, cleanup handles it later

            # In clean mode, don't process for display - just collect
            if clean_mode:
                continue

            display_chunk = think_filter.feed(token) if think_filter else token
            if first_token_timeout > 0 and first_token_time is None and (time.monotonic() - t0) >= first_token_timeout:
                raise StreamingTimeoutError(
                    f"No visible response from model within {first_token_timeout:.0f} seconds"
                )
            if think_filter and not display_chunk:
                continue

            # Hold display tokens until pre-display validation passes
            if not pre_display_validated:
                held_display_tokens.append(display_chunk)
                continue

            # Flush held tokens after validation passes
            if held_display_tokens and first_token_time is None:
                first_token_time = time.monotonic()
                if live.is_started:
                    live.stop()
                ttft = first_token_time - t0
                if is_verbose():
                    console.print(f"  [dim]─ First token in {ttft:.1f}s[/dim]")
                # Flush held tokens
                if has_bottom_dock():
                    _write_output("sage> " + "".join(held_display_tokens))
                else:
                    console.print("[bold green]sage>[/bold green] ", end="")
                    _write_output("".join(held_display_tokens))
                held_display_tokens.clear()

            if first_token_time is None and display_chunk:
                first_token_time = time.monotonic()
                if live.is_started:
                    live.stop()
                ttft = first_token_time - t0
                if is_verbose():
                    console.print(f"  [dim]─ First token in {ttft:.1f}s[/dim]")
                if has_bottom_dock():
                    buffer.append("sage> ")
                else:
                    console.print("[bold green]sage>[/bold green] ", end="")

            buffer.append(display_chunk)

            # Buffered flush for better performance
            now = time.monotonic()
            if len(buffer) >= _STREAM_BUFFER_SIZE or (now - last_flush) >= _STREAM_FLUSH_INTERVAL:
                _flush_buffer()

            if _sigint_received:
                cancelled = True
                break

        # Handle remaining thinking filter content (not in clean mode)
        if think_filter and not clean_mode:
            tail = think_filter.flush_display_tail()
            if tail:
                if first_token_time is None:
                    first_token_time = time.monotonic()
                    if live.is_started:
                        live.stop()
                    ttft = first_token_time - t0
                    if is_verbose():
                        console.print(f"  [dim]─ First token in {ttft:.1f}s[/dim]")
                    if has_bottom_dock():
                        buffer.append("sage> ")
                    else:
                        console.print("[bold green]sage>[/bold green] ", end="")
                buffer.append(tail)
    except KeyboardInterrupt:
        cancelled = True
    finally:
        if live.is_started:
            live.stop()
        # Restore the original signal handler (only if we installed one)
        if _on_main_thread and _original_handler is not None:
            signal.signal(signal.SIGINT, _original_handler)

    # If streaming was rejected due to bad patterns, signal to caller
    if streaming_rejected:
        console.print()
        if return_rejection_info:
            return "", True, rejection_reason
        return ""  # Return empty to signal rejection

    # Final flush (only in non-clean mode)
    if not clean_mode:
        _flush_buffer()
        elapsed = time.monotonic() - t0
        _write_output("\n")

        if cancelled:
            console.print("  [dim yellow]─ Cancelled (Ctrl+C)[/dim yellow]")
        elif token_count > 0 and elapsed > 0.1 and is_verbose():
            tps = token_count / elapsed if elapsed > 0 else 0
            console.print(f"  [dim]─ {token_count} tokens · {elapsed:.1f}s · {tps:.0f} tok/s[/dim]")
    # In clean mode, show final response after stripping thinking blocks
    elif cancelled:
        console.print("  [dim yellow]● Cancelled[/dim yellow]")
    else:
        # Show the cleaned response (without thinking blocks)
        full_response = "".join(parts)
        cleaned_response = strip_thinking_blocks(full_response)
        if cleaned_response:
            console.print()
            console.print("[bold green]sage>[/bold green] ", end="")
            console.print(cleaned_response)
            console.print()

    result = "".join(parts)
    if return_rejection_info:
        return result, False, ""  # Not rejected
    return result


def stream_tokens_minimal(tokens: Iterator[str], model_id: str = "") -> str:
    """Stream tokens with minimal output - collapses thinking blocks.

    This provides a cleaner output by:
    - Showing a brief "thinking..." indicator instead of full thinking content
    - Only displaying the actual response content
    - Keeping stats minimal

    Returns the full response (including thinking) for processing.
    """
    parts: list[str] = []
    buffer: list[str] = []
    token_count = 0
    t0 = time.monotonic()
    last_flush = t0
    first_token_time = None
    cancelled = False
    think_filter = _ThinkingSuppressionFilter()

    def _flush_buffer() -> None:
        nonlocal last_flush
        if buffer:
            _write_output("".join(buffer))
            buffer.clear()
            last_flush = time.monotonic()

    # Signal handler for Ctrl+C
    # CRITICAL: Only install signal handlers on the main thread to avoid crashes
    _sigint_received = False
    _original_handler = None
    _on_main_thread = _is_main_thread()

    def _handle_sigint(signum, frame):
        nonlocal _sigint_received
        _sigint_received = True

    # Only install signal handler if we're on the main thread
    if _on_main_thread:
        _original_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, _handle_sigint)

    # Show thinking spinner
    spinner = Spinner(
        "dots",
        text=Text.from_markup(
            "  [bold yellow]⟡ Thinking...[/bold yellow]"
            + (f"  [dim]({model_id})[/dim]" if model_id else "")
        ),
    )
    live = Live(spinner, console=console, refresh_per_second=12, transient=True)
    if not has_bottom_dock():
        live.start()

    try:
        for token in tokens:
            if _sigint_received:
                cancelled = True
                break

            parts.append(token)
            token_count += 1

            display_chunk = think_filter.feed(token)
            if not display_chunk:
                continue

            if first_token_time is None:
                first_token_time = time.monotonic()
                live.stop()
                ttft = first_token_time - t0
                console.print(f"  [dim]─ First token in {ttft:.1f}s[/dim]")
                if has_bottom_dock():
                    buffer.append("sage> ")
                else:
                    console.print("[bold green]sage>[/bold green] ", end="")

            buffer.append(display_chunk)
            now = time.monotonic()
            if len(buffer) >= _STREAM_BUFFER_SIZE or (now - last_flush) >= _STREAM_FLUSH_INTERVAL:
                _flush_buffer()

            if _sigint_received:
                cancelled = True
                break

        tail = think_filter.flush_display_tail()
        if tail:
            if first_token_time is None:
                first_token_time = time.monotonic()
                live.stop()
                ttft = first_token_time - t0
                console.print(f"  [dim]─ First token in {ttft:.1f}s[/dim]")
                if has_bottom_dock():
                    buffer.append("sage> ")
                else:
                    console.print("[bold green]sage>[/bold green] ", end="")
            buffer.append(tail)
    except KeyboardInterrupt:
        cancelled = True
    finally:
        if live.is_started:
            live.stop()
        # Restore the original signal handler (only if we installed one)
        if _on_main_thread and _original_handler is not None:
            signal.signal(signal.SIGINT, _original_handler)

    # Final flush
    _flush_buffer()

    elapsed = time.monotonic() - t0
    _write_output("\n")

    if cancelled:
        console.print("  [dim yellow]─ Cancelled (Ctrl+C)[/dim yellow]")
    elif token_count > 0 and elapsed > 0.1:
        tps = token_count / elapsed if elapsed > 0 else 0
        console.print(f"  [dim]─ {token_count} tokens · {elapsed:.1f}s · {tps:.0f} tok/s[/dim]")

    return "".join(parts)


# ── Todo/Progress display ──────────────────────────────────


def print_todos(todos: list[dict]) -> None:
    """Print a minimal todo list showing task progress."""
    if not todos:
        return

    if has_bottom_dock():
        set_bottom_dock_todos(todos)
        return

    console.print()
    console.print("  [bold cyan]📋 Tasks:[/bold cyan]")
    for todo in todos:
        status = todo.get("status", "pending")
        content = todo.get("content", "")
        if status == "completed":
            icon = "[green]✓[/green]"
        elif status == "in_progress":
            icon = "[yellow]►[/yellow]"
        else:
            icon = "[dim]○[/dim]"
        console.print(f"    {icon} {content}")


def print_step_progress(current: int, total: int, description: str) -> None:
    """Print a minimal step progress indicator."""
    if has_bottom_dock():
        set_bottom_dock_status(f"Step {current}/{total}: {description}")
    console.print(f"  [cyan]Step {current}/{total}:[/cyan] {description}")


# ── File operation display ─────────────────────────────────


def print_files_written(files: list[str]) -> None:
    """Print a styled list of written files."""
    console.print()
    phase("writing", f"{len(files)} file(s)")
    for f in files:
        console.print(f"    [green]+ {f}[/green]")


def print_files_deleted(files: list[str]) -> None:
    """Print a styled list of deleted files."""
    for f in files:
        console.print(f"    [red]- {f}[/red]")


def print_file_read(filepath: str, line_count: int) -> None:
    """Print a styled file-read indicator."""
    phase("reading", f"{filepath} ({line_count} lines)")


# ── Test result display ────────────────────────────────────


def print_test_results(output: str, passed: bool) -> None:
    """Print test results with pass/fail styling."""
    if passed:
        console.print()
        phase("done", "All tests passed")
        # Extract summary line if present
        for line in output.splitlines():
            if "passed" in line.lower():
                console.print(f"    [green]{line.strip()}[/green]")
                break
    else:
        console.print()
        phase("error", "Tests failed")
        # Show the failure summary
        in_failures = False
        shown = 0
        for line in output.splitlines():
            if "FAILED" in line or "ERROR" in line:
                console.print(f"    [red]{line.strip()}[/red]")
                shown += 1
            elif "short test summary" in line.lower():
                in_failures = True
            elif in_failures and line.strip() and shown < 10:
                console.print(f"    [red]{line.strip()}[/red]")
                shown += 1


def print_validation_start(cmd: str) -> None:
    """Print the start of a validation step."""
    console.print()
    phase("validating", cmd)


def print_retry(attempt: int, max_retries: int) -> None:
    """Print a retry indicator."""
    console.print()
    phase("fixing", f"Auto-fixing (attempt {attempt}/{max_retries})")


# ── Command execution display ──────────────────────────────


def print_shell_start(cmd: str) -> None:
    """Print shell command being executed."""
    phase("executing", cmd[:100] + ("..." if len(cmd) > 100 else ""))


def print_shell_output(output: str, max_lines: int = 30) -> None:
    """Print shell output, truncated if too long."""
    lines = output.splitlines()
    if len(lines) > max_lines:
        for line in lines[:10]:
            console.print(f"    [dim]{line}[/dim]")
        console.print(f"    [dim]... ({len(lines) - 20} lines hidden) ...[/dim]")
        for line in lines[-10:]:
            console.print(f"    [dim]{line}[/dim]")
    else:
        for line in lines:
            console.print(f"    [dim]{line}[/dim]")


# ── Existing functions (upgraded) ──────────────────────────


def render_markdown(text: str) -> None:
    """Render a complete response as Rich Markdown with code highlighting."""
    content = strip_thinking_blocks(text) if suppress_thinking() else text
    if not content.strip():
        return
    console.print(Markdown(content))


def print_model_table(
    models: list[dict],
    *,
    max_rows: int = 45,
    filter_hint: str | None = None,
    show_details: bool = False,
    show_all: bool = False,
) -> None:
    """Print a formatted table of available models.

    Large catalogs are truncated with a hint to use CLI ``sage models --search`` or ``/models <kw>``.

    Args:
        models: List of model dicts with id, provider, name, local, description, pros, cons
        max_rows: Maximum rows to show
        filter_hint: Filter keyword for title
        show_details: If True, show expanded view with pros/cons
    """
    title = "Available Models"
    if filter_hint:
        title = f"{title} (filter: {filter_hint})"
    table = Table(title=title, show_lines=show_details)
    table.add_column("Model ID", style="cyan bold")
    table.add_column("Provider", style="green")
    table.add_column("Name", style="white")
    table.add_column("Type", style="yellow")
    if show_details:
        table.add_column("Description", style="dim")
    else:
        # Show brief description in compact mode
        table.add_column("Description", style="dim", max_width=40)

    effective_max = len(models) if show_all else max_rows
    shown = models[:effective_max]
    for m in shown:
        desc = m.get("description", "")
        if show_details and (m.get("pros") or m.get("cons")):
            # Expanded view with pros/cons
            pros = m.get("pros", "")
            cons = m.get("cons", "")
            if pros or cons:
                desc_parts = [desc] if desc else []
                if pros:
                    desc_parts.append(f"[green]✓ {pros}[/green]")
                if cons:
                    desc_parts.append(f"[red]✗ {cons}[/red]")
                desc = "\n".join(desc_parts)
        elif len(desc) > 40:
            desc = desc[:37] + "..."
        table.add_row(
            m["id"],
            m["provider"],
            m["name"],
            "local" if m["local"] else "API",
            desc,
        )
    console.print(table)
    remaining = len(models) - len(shown)
    if remaining > 0:
        console.print(
            f"[dim]… {remaining} more not shown. "
            "Use [cyan]/models --all[/cyan] to see all, "
            "or [cyan]/models <keyword>[/cyan] to filter.[/dim]"
        )
    if not show_details:
        console.print("[dim]Use /models --details for full descriptions with pros/cons[/dim]")


def print_catalog_table(models: list[dict], show_status: bool = True) -> None:
    """Print a formatted table of models from the catalog."""
    table = Table(title="Downloadable Models", show_lines=False)
    table.add_column("Name", style="cyan bold")
    table.add_column("Size", style="yellow", justify="right")
    table.add_column("Params", style="green")
    table.add_column("Family", style="magenta")
    table.add_column("Description", style="white")
    if show_status:
        table.add_column("Status", style="bold")

    for m in models:
        row = [m["name"], m["size"], m["params"], m["family"], m["description"]]
        if show_status:
            row.append(m.get("status", ""))
        table.add_row(*row)
    console.print(table)


def print_download_complete(name: str, path: str, size_gb: float) -> None:
    """Print a success message after a model download."""
    console.print()
    console.print(
        Panel(
            f"[bold green]Downloaded:[/bold green] {name}\n"
            f"[dim]Path:[/dim] {path}\n"
            f"[dim]Size:[/dim] {size_gb:.1f} GB\n\n"
            f"Run with: [bold cyan]sage run --model llama_cpp:{name}[/bold cyan]",
            title="Model Ready",
            border_style="green",
        )
    )


def print_config(data: dict) -> None:
    """Pretty-print config as a panel."""
    import json

    text = json.dumps(data, indent=2)
    console.print(Panel(text, title="~/.sage/config.json", border_style="dim"))


def header(msg: str) -> None:
    """Print a header/title message."""
    console.print(f"[bold cyan]{msg}[/bold cyan]")


def info(msg: str) -> None:
    """Print an info message.

    Only shown in verbose mode.
    """
    if not is_verbose():
        return
    console.print(f"[dim]{msg}[/dim]")


def success(msg: str) -> None:
    """Print a success message."""
    console.print(f"[green]{msg}[/green]")


def error(msg: str) -> None:
    """Print an error message to stderr."""
    err_console.print(f"[red bold]Error:[/red bold] {msg}")


def warning(msg: str) -> None:
    """Print a warning to stderr.

    Important warnings that should show even in clean mode.
    For debug/validation warnings, use debug_warning() instead.
    """
    err_console.print(f"[yellow]Warning:[/yellow] {msg}")


def debug_warning(msg: str) -> None:
    """Print a debug warning (only in verbose mode).

    Use this for non-critical validation messages like:
    - File rejection reasons
    - Import validation failures
    - Garbage content rejections

    These are useful for debugging but noisy in clean mode.
    """
    if not is_verbose():
        return
    err_console.print(f"[dim yellow]Debug:[/dim yellow] {msg}")


def print_welcome(model_id: str) -> None:
    """Print the REPL welcome banner."""
    console.print(
        Panel(
            Text.from_markup(
                f"[bold #6ea4ff]SAGE[/bold #6ea4ff]  [dim]local-first AI workspace[/dim]\n"
                f"[dim]Model[/dim]   {model_id}\n"
                f"[dim]Use[/dim]     /help  /clear  /model  /system  /exit\n"
                f'[dim]Input[/dim]   Multi-line with """..."""'
            ),
            border_style="#6ea4ff",
            padding=(0, 2),
        )
    )


def print_help() -> None:
    """Print REPL command reference."""
    help_text = (
        "[bold #6ea4ff]REPL commands[/bold #6ea4ff]\n"
        "  [#8bb8ff]/help[/#8bb8ff]           Show this help\n"
        "  [#8bb8ff]/clear[/#8bb8ff]          Clear conversation history\n"
        "  [#8bb8ff]/update[/#8bb8ff]         Update SAGE AI to the latest CLI version\n"
        "  [#8bb8ff]/model[/#8bb8ff] [id]     Show or change active model\n"
        "  [#8bb8ff]/system[/#8bb8ff] [text]  Show or set system prompt\n"
        "  [#8bb8ff]/history[/#8bb8ff]        Show conversation turn count\n"
        "  [#8bb8ff]/exit[/#8bb8ff]           Quit\n"
    )
    console.print(Panel(help_text, title="SAGE Help", border_style="#6ea4ff"))


def print_agent_welcome(model_id: str, cwd: str, *, is_local: bool = False) -> None:
    """Print the agent-mode welcome banner (Claude Code–style interactive agent)."""
    kind = "local (Ollama / llama.cpp / etc.)" if is_local else "cloud / API"
    console.print()
    console.print(
        Panel(
            Text.from_markup(
                f"[bold #6ea4ff]SAGE Code[/bold #6ea4ff]  [dim]interactive coding workspace[/dim]\n"
                f"\n"
                f"[dim]Model[/dim]    [bold]{model_id}[/bold]\n"
                f"[dim]Backend[/dim]  {kind}\n"
                f"[dim]Project[/dim]  {cwd}\n"
                f"\n"
                f"[dim]READ / SEARCH / edit / run with your model catalog, locally or in the cloud.[/dim]\n"
                f"[dim]Switch models with /model and browse them with /models.[/dim]\n"
                f"\n"
                f"[#8bb8ff]Commands[/#8bb8ff]  /help  /models  /prompts  /autopolit  /autoorg  /update  /think  /test  /read  /files  /compact  /clear  /exit\n"
                f'[#8bb8ff]Shell[/#8bb8ff]     !<command>    [#8bb8ff]Multi-line[/#8bb8ff] """..."""\n'
                f"[#8bb8ff]Models[/#8bb8ff]    sage pull --list    sage pull <name>\n"
                f"[#8bb8ff]Update[/#8bb8ff]    sage update"
            ),
            border_style="#6ea4ff",
            padding=(0, 2),
        )
    )
    console.print()


def print_agent_help() -> None:
    """Print agent-mode command reference."""
    help_text = (
        "[bold #6ea4ff]Workspace commands[/bold #6ea4ff]\n"
        "  [#8bb8ff]/help[/#8bb8ff]             Show this help\n"
        "  [#8bb8ff]/models[/#8bb8ff]           List all available AI models\n"
        "  [#8bb8ff]/model[/#8bb8ff] [id]       Show or change the active model\n"
        "  [#8bb8ff]/think[/#8bb8ff] [on|off]   Enable/disable thinking blocks visibility\n"
        "  [#8bb8ff]/read[/#8bb8ff] <file>      Read a file into conversation context\n"
        "  [#8bb8ff]/test[/#8bb8ff] [cmd]       Run tests (default: pytest -v --tb=short)\n"
        "  [#8bb8ff]/files[/#8bb8ff]            Show written files from this session\n"
        "  [#8bb8ff]/undo[/#8bb8ff]             Restore files to previous state\n"
        "  [#8bb8ff]/compact[/#8bb8ff]          Trim conversation state to free context\n"
        "  [#8bb8ff]/clear[/#8bb8ff]            Clear conversation and file history\n"
        "  [#8bb8ff]/system[/#8bb8ff] [text]    Show or set system prompt\n"
        "  [#8bb8ff]/update[/#8bb8ff]           Update SAGE AI to the latest CLI version\n"
        "  [#8bb8ff]/history[/#8bb8ff]          Show conversation turn count\n"
        "  [#8bb8ff]/exit[/#8bb8ff]             Quit\n"
        "\n[bold #6ea4ff]Shell[/bold #6ea4ff]\n"
        "  [#8bb8ff]!<command>[/#8bb8ff]        Run a shell command (e.g. !ls -la)\n"
        "\n[bold #6ea4ff]SAGE phases[/bold #6ea4ff]\n"
        "  [dim]◌ Thinking[/dim]      Analyzing the request\n"
        "  [dim]◎ Planning[/dim]      Breaking the task into steps\n"
        "  [dim]◆ Coding[/dim]        Generating code\n"
        "  [dim]▸ Writing[/dim]       Saving files to disk\n"
        "  [dim]◈ Testing[/dim]       Running tests automatically\n"
        "  [dim]↺ Fixing[/dim]        Recovering from failures\n"
        "  [dim]✓ Done[/dim]          Task complete\n"
        "\n[bold #6ea4ff]Flags[/bold #6ea4ff]\n"
        "  [dim]--output clean|normal|verbose  Terminal verbosity (default: clean)[/dim]\n"
        "  [dim]-v / --verbose                 Same as --output verbose[/dim]\n"
        "  [dim]--no-color                     Disable ANSI colors[/dim]\n"
        "  [dim]--auto-run                     Skip bash execution prompts[/dim]\n"
    )
    console.print(Panel(help_text, title="SAGE Code Help", border_style="#6ea4ff"))


# ── Pull-Update-Delete Cycle Progress Bar ──────────────────


class SyncProgress:
    """Multi-phase progress bar for pull-update-delete sync cycles.

    Displays a rich progress bar that tracks three phases:
    1. Pull   - Fetching/downloading new items
    2. Update - Updating existing items
    3. Delete - Removing stale items

    Usage:
        with SyncProgress() as progress:
            # Pull phase
            progress.start_pull(total=10)
            for item in items_to_pull:
                pull(item)
                progress.advance_pull()

            # Update phase
            progress.start_update(total=5)
            for item in items_to_update:
                update(item)
                progress.advance_update()

            # Delete phase
            progress.start_delete(total=3)
            for item in items_to_delete:
                delete(item)
                progress.advance_delete()
    """

    _PHASE_ICONS = {
        "pull": ("cyan", "↓"),
        "update": ("yellow", "↻"),
        "delete": ("red", "×"),
    }

    def __init__(self, title: str = "Syncing") -> None:
        self._title = title
        self._progress: Progress | None = None
        self._overall_task: TaskID | None = None
        self._phase_task: TaskID | None = None
        self._current_phase: str | None = None
        self._phases_completed = 0
        self._total_phases = 3

    def __enter__(self) -> SyncProgress:
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold]{task.description}[/bold]"),
            BarColumn(bar_width=30),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("[dim]{task.fields[status]}[/dim]"),
            console=console,
            transient=False,
        )
        self._progress.start()

        # Overall progress bar
        self._overall_task = self._progress.add_task(
            f"[bold cyan]{self._title}[/bold cyan]",
            total=self._total_phases,
            status="starting...",
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._progress and self._overall_task is not None:
            if exc_type is None:
                # Success - mark complete
                self._progress.update(
                    self._overall_task,
                    completed=self._total_phases,
                    status="[green]complete[/green]",
                )
            else:
                # Error occurred
                self._progress.update(
                    self._overall_task,
                    status=f"[red]failed ({exc_type.__name__})[/red]",
                )
            self._progress.stop()

    def _start_phase(self, phase: str, total: int, description: str = "") -> None:
        """Start a new phase with its own progress bar."""
        color, icon = self._PHASE_ICONS.get(phase, ("white", "·"))
        desc = description or phase.capitalize()

        # Complete previous phase task if exists
        if self._phase_task is not None and self._progress:
            self._progress.remove_task(self._phase_task)

        self._current_phase = phase

        if self._progress and self._overall_task is not None:
            # Update overall status
            self._progress.update(
                self._overall_task,
                status=f"[{color}]{icon} {desc}[/{color}]",
            )

            # Create phase-specific task
            self._phase_task = self._progress.add_task(
                f"  [{color}]{icon}[/{color}] {desc}",
                total=total,
                status="",
            )

    def _advance_phase(self, amount: int = 1, status: str = "") -> None:
        """Advance the current phase progress."""
        if self._progress and self._phase_task is not None:
            self._progress.update(self._phase_task, advance=amount, status=status)

    def _complete_phase(self) -> None:
        """Mark the current phase as complete and update overall progress."""
        if self._progress and self._phase_task is not None:
            # Mark phase task complete
            task = self._progress.tasks[self._phase_task]
            self._progress.update(self._phase_task, completed=task.total or 0)

        self._phases_completed += 1
        if self._progress and self._overall_task is not None:
            self._progress.update(self._overall_task, completed=self._phases_completed)

    # ── Pull Phase ─────────────────────────────────────────

    def start_pull(self, total: int, description: str = "Pulling") -> None:
        """Start the pull phase."""
        self._start_phase("pull", total, description)

    def advance_pull(self, amount: int = 1, item: str = "") -> None:
        """Advance pull progress."""
        status = f"[dim]{item}[/dim]" if item else ""
        self._advance_phase(amount, status)

    def complete_pull(self) -> None:
        """Complete the pull phase."""
        self._complete_phase()

    # ── Update Phase ───────────────────────────────────────

    def start_update(self, total: int, description: str = "Updating") -> None:
        """Start the update phase."""
        self._start_phase("update", total, description)

    def advance_update(self, amount: int = 1, item: str = "") -> None:
        """Advance update progress."""
        status = f"[dim]{item}[/dim]" if item else ""
        self._advance_phase(amount, status)

    def complete_update(self) -> None:
        """Complete the update phase."""
        self._complete_phase()

    # ── Delete Phase ───────────────────────────────────────

    def start_delete(self, total: int, description: str = "Cleaning up") -> None:
        """Start the delete phase."""
        self._start_phase("delete", total, description)

    def advance_delete(self, amount: int = 1, item: str = "") -> None:
        """Advance delete progress."""
        status = f"[dim]{item}[/dim]" if item else ""
        self._advance_phase(amount, status)

    def complete_delete(self) -> None:
        """Complete the delete phase."""
        self._complete_phase()


@contextmanager
def sync_progress(title: str = "Syncing") -> Iterator[SyncProgress]:
    """Context manager for pull-update-delete sync progress.

    Usage:
        with sync_progress("Syncing models") as progress:
            progress.start_pull(total=10)
            for model in models_to_pull:
                download(model)
                progress.advance_pull(item=model.name)
            progress.complete_pull()

            progress.start_update(total=5)
            for model in models_to_update:
                update(model)
                progress.advance_update(item=model.name)
            progress.complete_update()

            progress.start_delete(total=3)
            for model in models_to_delete:
                remove(model)
                progress.advance_delete(item=model.name)
            progress.complete_delete()
    """
    sp = SyncProgress(title)
    with sp:
        yield sp


# ── Autopolit Progress Tracking (P1-28, P1-30) ──────────────


class AutopolitProgress:
    """Progress tracker for autopolit cycles.

    Tracks:
    - Current cycle number
    - Files written per cycle
    - Tests passed/failed
    - Time elapsed
    - Errors encountered
    """

    def __init__(self, max_cycles: int | None = None):
        self.max_cycles = max_cycles
        self.current_cycle = 0
        self.start_time = time.time()
        self.cycle_stats: list[dict] = []
        self._current_cycle_stats: dict = {}

    def start_cycle(self, cycle: int) -> None:
        """Start a new cycle."""
        self.current_cycle = cycle
        self._current_cycle_stats = {
            "cycle": cycle,
            "start_time": time.time(),
            "files_written": [],
            "tests_passed": False,
            "errors": [],
            "phase": "starting",
        }

        max_str = f"/{self.max_cycles}" if self.max_cycles else ""
        elapsed = time.time() - self.start_time
        elapsed_str = f"{elapsed:.0f}s" if elapsed < 60 else f"{elapsed / 60:.1f}m"

        console.print()
        console.print(
            Rule(
                f"[bold cyan]Autopolit Cycle {cycle}{max_str}[/bold cyan] "
                f"[dim]({elapsed_str} elapsed)[/dim]",
                style="cyan",
            )
        )

    def update_phase(self, phase: str, detail: str = "") -> None:
        """Update current phase."""
        self._current_cycle_stats["phase"] = phase
        _phase(phase, detail)

    def add_file(self, filepath: str) -> None:
        """Record a file written."""
        self._current_cycle_stats["files_written"].append(filepath)

    def add_error(self, error: str) -> None:
        """Record an error."""
        self._current_cycle_stats["errors"].append(error)

    def set_tests_passed(self, passed: bool) -> None:
        """Record test result."""
        self._current_cycle_stats["tests_passed"] = passed

    def end_cycle(self) -> None:
        """End the current cycle and record stats."""
        self._current_cycle_stats["end_time"] = time.time()
        self._current_cycle_stats["duration"] = (
            self._current_cycle_stats["end_time"] - self._current_cycle_stats["start_time"]
        )
        self.cycle_stats.append(self._current_cycle_stats.copy())

        # Print cycle summary
        stats = self._current_cycle_stats
        files = len(stats["files_written"])
        errors = len(stats["errors"])
        duration = stats["duration"]

        status_parts = []
        if files > 0:
            status_parts.append(f"[green]{files} file(s)[/green]")
        if stats["tests_passed"]:
            status_parts.append("[green]tests ✓[/green]")
        elif errors > 0:
            status_parts.append(f"[red]{errors} error(s)[/red]")

        status = " · ".join(status_parts) if status_parts else "[dim]no changes[/dim]"
        console.print(
            f"  [dim]Cycle {self.current_cycle} completed in {duration:.1f}s[/dim] — {status}"
        )

    def print_summary(self) -> None:
        """Print final autopolit summary (P1-30)."""
        total_time = time.time() - self.start_time
        total_cycles = len(self.cycle_stats)
        total_files = sum(len(s["files_written"]) for s in self.cycle_stats)
        total_errors = sum(len(s["errors"]) for s in self.cycle_stats)
        successful_cycles = sum(1 for s in self.cycle_stats if s["tests_passed"])

        time_str = f"{total_time:.0f}s" if total_time < 60 else f"{total_time / 60:.1f}m"

        console.print()
        console.print(Rule("[bold]Autopolit Summary[/bold]", style="cyan"))
        console.print()

        # Create summary table
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style="dim")
        table.add_column(style="bold")

        table.add_row("Total cycles", str(total_cycles))
        table.add_row("Successful cycles", f"[green]{successful_cycles}[/green]")
        table.add_row("Files written", f"[cyan]{total_files}[/cyan]")
        table.add_row(
            "Errors encountered",
            f"[red]{total_errors}[/red]" if total_errors else "[green]0[/green]",
        )
        table.add_row("Total time", time_str)

        console.print(table)

        # List files written
        if total_files > 0:
            console.print()
            console.print("[dim]Files written:[/dim]")
            all_files = set()
            for s in self.cycle_stats:
                all_files.update(s["files_written"])
            for f in sorted(all_files)[:20]:
                console.print(f"  [green]+ {f}[/green]")
            if len(all_files) > 20:
                console.print(f"  [dim]... and {len(all_files) - 20} more[/dim]")

        console.print()


def _phase(name: str, detail: str = "") -> None:
    """Internal phase printer (avoids name conflict)."""
    style, icon = _PHASE_STYLES.get(name, ("dim", "·"))
    detail_str = f"  [dim]{detail}[/dim]" if detail else ""
    console.print(f"  [{style}]{icon} {name.capitalize()}[/{style}]{detail_str}")
