"""
Editor-Style Output Mode for PraisonAI Agents.

Provides a user-friendly display format with:
- Numbered steps: Step 1: 📄 Creating file: /path
- Human-readable tool names (not technical names)
- Smart result formatting (JSON → summary, exit → ✓ Done)
- Completion summary with duration and block count

Usage:
    # Via preset:
    agent = Agent(output="editor")

    # Programmatic:
    from praisonaiagents.output.editor import enable_editor_output
    enable_editor_output()
"""

import time
import threading
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, TextIO
from enum import Enum


# ─────────────────────────────────────────────────────────────────────────────
# Module-level state (same pattern as status.py)
# ─────────────────────────────────────────────────────────────────────────────
_editor_output_enabled = False
_editor_output: Optional['EditorOutput'] = None


class BlockType(Enum):
    """Types of display blocks."""
    NARRATIVE = "narrative"
    COMMAND = "command"
    SUMMARY = "summary"
    ACTION = "action"
    CODE = "code"
    LIST = "list"


@dataclass
class DisplayBlock:
    """A single display block."""
    type: BlockType
    content: str
    title: Optional[str] = None
    items: List[str] = field(default_factory=list)
    output: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# Human-readable tool name mappings
TOOL_LABELS: Dict[str, tuple] = {
    # Web / search
    'internet_search': ('🔍', 'Searching the web'),
    'search_web': ('🔍', 'Searching the web'),
    'web_search': ('🔍', 'Searching the web'),
    # File operations
    'read_file': ('📖', 'Reading file'),
    'write_file': ('📝', 'Writing file'),
    'create_file': ('📄', 'Creating file'),
    'acp_create_file': ('📄', 'Creating file'),
    'acp_edit_file': ('✏️', 'Editing file'),
    'acp_delete_file': ('🗑️', 'Deleting file'),
    # Execution
    'execute_command': ('⚡', 'Running command'),
    'acp_execute_command': ('⚡', 'Running command'),
    # Directory
    'list_files': ('📂', 'Listing files'),
    'get_system_info': ('💻', 'Getting system info'),
    # LSP
    'lsp_get_diagnostics': ('🔬', 'Analyzing code'),
    'lsp_list_symbols': ('🔎', 'Finding code symbols'),
    'lsp_find_definition': ('📍', 'Finding definition'),
    'lsp_find_references': ('🔗', 'Finding references'),
}


class EditorOutput:
    """
    User-friendly display for agent output.

    Renders tool calls as numbered steps with emoji icons and
    human-readable labels. Formats results smartly (JSON → summary).

    Thread-safe for multi-agent execution.
    """

    def __init__(self, console=None, use_rich: bool = True):
        self._use_rich = use_rich
        self._console = console
        self._blocks: List[DisplayBlock] = []
        self._start_time = time.time()
        self._step_count = 0
        self._lock = threading.Lock()

        if use_rich and console is None:
            try:
                from rich.console import Console
                self._console = Console()
            except ImportError:
                self._use_rich = False

    # ─────────────────────────────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────────────────────────────

    def tool_call(
        self,
        tool_name: str,
        args: Optional[Dict[str, Any]] = None,
        result: Optional[str] = None,
        duration: Optional[float] = None,
    ) -> None:
        """Display a tool call as a numbered step with emoji."""
        with self._lock:
            self._step_count += 1
            step_num = self._step_count

        # Get human-readable label
        icon, label = TOOL_LABELS.get(tool_name, ('🔧', f'Using {tool_name}'))

        # Format action description with step number and context
        step_prefix = f"Step {step_num}: "
        action = self._format_action(step_prefix, icon, label, args)

        # Format result for display
        display_result = self._format_result(result)

        self._add_block(BlockType.COMMAND, action, output=display_result)
        self._render_command(action, display_result)

    def output(self, content: str, agent_name: Optional[str] = None) -> None:
        """Display final agent output."""
        if self._use_rich:
            self._console.print()
            self._console.print(content)
            self._console.print()
        else:
            print()
            print(content)
            print()

    def summary(self, title: str, items: Optional[List[str]] = None) -> None:
        """Display completion summary."""
        self._add_block(BlockType.SUMMARY, "", title=title, items=items or [])
        self._render_summary(title, items)

    def elapsed_time(self) -> float:
        """Get elapsed time since display started."""
        return time.time() - self._start_time

    def get_blocks(self) -> List[DisplayBlock]:
        """Get all display blocks."""
        return self._blocks.copy()

    # ─────────────────────────────────────────────────────────────────────
    # Formatting helpers
    # ─────────────────────────────────────────────────────────────────────

    @staticmethod
    def _format_action(
        step_prefix: str,
        icon: str,
        label: str,
        args: Optional[Dict[str, Any]],
    ) -> str:
        """Build human-readable action string from tool args."""
        if not args:
            return f"{step_prefix}{icon} {label}"

        # Extract the most meaningful argument for context
        for key in ('query', 'filepath', 'file_path', 'directory', 'command'):
            if key in args:
                val = args[key]
                if key == 'query':
                    return f'{step_prefix}{icon} {label} for "{val}"'
                return f"{step_prefix}{icon} {label}: {val}"

        return f"{step_prefix}{icon} {label}"

    @staticmethod
    def _format_result(result: Optional[str]) -> Optional[str]:
        """Convert raw tool result to a user-friendly summary."""
        if not result:
            return None

        result_str = str(result)

        # JSON → summary
        if result_str.startswith(('[', '{')):
            try:
                import json
                data = json.loads(result_str)
                if isinstance(data, list):
                    return f"✓ Found {len(data)} items"
                if isinstance(data, dict):
                    if data.get('success') is True:
                        return f"✓ Created: {data['file_created']}" if data.get('file_created') else "✓ Success"
                    if data.get('success') is False:
                        return f"⚠ Failed: {data.get('error', 'Unknown')[:80]}"
                    if data.get('error'):
                        return f"⚠ {data['error'][:80]}"
                    if data.get('stdout'):
                        first_line = data['stdout'].strip().split('\n')[0][:80]
                        return f"✓ {first_line}"
                    if data.get('exit_code') == 0:
                        return "✓ Command completed"
                    return "✓ Done"
            except (ValueError, TypeError):
                return "✓ Done"

        # Boolean strings
        if result_str.lower() == 'true':
            return "✓ Success"
        if result_str.lower() == 'false':
            return "⚠ Failed"

        # Short plain text → show it; long text → "Done"
        if len(result_str) <= 80 and '\n' not in result_str:
            return result_str
        return "✓ Done"

    # ─────────────────────────────────────────────────────────────────────
    # Internal rendering
    # ─────────────────────────────────────────────────────────────────────

    def _add_block(self, block_type, content, **kwargs):
        block = DisplayBlock(type=block_type, content=content, **kwargs)
        with self._lock:
            self._blocks.append(block)

    def _render_command(self, cmd: str, output: Optional[str] = None):
        if self._use_rich:
            self._console.print(f"[dim]{cmd}[/dim]")
            if output:
                self._console.print(output)
        else:
            print(cmd)
            if output:
                print(output)

    def _render_summary(self, title: str, items: Optional[List[str]] = None):
        if self._use_rich:
            self._console.print()
            self._console.print(f"[bold]{title}[/bold]")
            if items:
                for item in items:
                    self._console.print(f"- {item}")
        else:
            print()
            print(title)
            if items:
                for item in items:
                    print(f"- {item}")


# ─────────────────────────────────────────────────────────────────────────────
# Module-level enable / disable (same pattern as status.py)
# ─────────────────────────────────────────────────────────────────────────────

def is_editor_output_enabled() -> bool:
    """Check whether editor output mode is currently active."""
    return _editor_output_enabled


def enable_editor_output(
    use_color: bool = True,
) -> EditorOutput:
    """
    Enable editor output mode globally.

    Registers display callbacks that render tool calls as numbered steps.

    Returns:
        EditorOutput instance for programmatic access.
    """
    global _editor_output_enabled, _editor_output

    _editor_output = EditorOutput(use_rich=use_color)
    _editor_output_enabled = True

    # Register callbacks with the display system
    from ..main import register_display_callback

    def on_tool_call(
        message: str = None,
        tool_name: str = None,
        tool_input: dict = None,
        tool_output: str = None,
        **kwargs,
    ):
        if not _editor_output_enabled or _editor_output is None:
            return
        if tool_name:
            _editor_output.tool_call(
                tool_name=tool_name,
                args=tool_input,
                result=str(tool_output)[:500] if tool_output else None,
            )

    def on_interaction(
        message: str = None,
        response: str = None,
        agent_name: str = None,
        generation_time: float = None,
        **kwargs,
    ):
        if not _editor_output_enabled or _editor_output is None:
            return
        if response:
            _editor_output.output(response, agent_name)

    def on_error(message: str = None, **kwargs):
        if not _editor_output_enabled or _editor_output is None:
            return
        if message and _editor_output._use_rich:
            _editor_output._console.print(f"[red]✗ Error: {message}[/red]")
        elif message:
            print(f"✗ Error: {message}")

    register_display_callback('tool_call', on_tool_call)
    register_display_callback('interaction', on_interaction)
    register_display_callback('error', on_error)

    return _editor_output


def disable_editor_output() -> None:
    """Disable editor output mode."""
    global _editor_output_enabled, _editor_output
    _editor_output_enabled = False
    _editor_output = None
