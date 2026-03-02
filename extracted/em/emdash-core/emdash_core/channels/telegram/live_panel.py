"""Live status panel for Telegram.

Maintains a single message that displays thinking, tool calls, and progress
as the agent works. The message is continuously updated via edit_message_text,
giving users real-time visibility into what the LLM is doing.

Example panel output::

    💭 _Analyzing the code structure..._

      🔄 `glob` "src/**/*.py"
      ✅ `read_file` `models.py`
      ❌ `bash` `npm test`

    ⏳ Running `semantic_search`...

When finalized (session ends), the panel collapses to a summary::

    💭 _Analyzed the code structure_

      ✅ `glob` "src/**/*.py"
      ✅ `read_file` `models.py`

    ✨ 3 tools used
"""

from __future__ import annotations

from dataclasses import dataclass, field


# Panel icons
ICON_THINKING = "💭"
ICON_TOOL_RUNNING = "🔄"
ICON_TOOL_SUCCESS = "✅"
ICON_TOOL_ERROR = "❌"
ICON_PROGRESS = "⏳"
ICON_DONE = "✨"


@dataclass
class ToolEntry:
    """A single tool call tracked by the panel."""

    name: str
    args_summary: str = ""
    status: str = "running"  # "running" | "success" | "error"


class LiveStatusPanel:
    """Accumulates agent events and renders a live-updating status panel.

    The panel shows thinking, tool calls (with individual status), and
    progress in a single Telegram message that gets edited in-place.

    Usage::

        panel = LiveStatusPanel()

        panel.on_thinking("Analyzing the request...")
        text = panel.render()  # Send as new message

        panel.on_tool_start("glob", '"src/**/*.py"')
        text = panel.render()  # Edit same message

        panel.on_tool_result("glob", success=True)
        text = panel.render()  # Edit again

        panel.finalize()
        text = panel.render()  # Final edit with summary
    """

    def __init__(
        self,
        max_tools_shown: int = 8,
        max_thinking_len: int = 150,
    ) -> None:
        self.max_tools_shown = max_tools_shown
        self.max_thinking_len = max_thinking_len
        self.reset()

    def reset(self) -> None:
        """Reset panel state for a new session."""
        self._thinking: str | None = None
        self._tools: list[ToolEntry] = []
        self._progress: str | None = None
        self._has_content = False
        self._has_sent = False
        self._finalized = False

    # -- Properties ----------------------------------------------------------

    @property
    def is_active(self) -> bool:
        """Whether the panel has any content to display."""
        return self._has_content and not self._finalized

    @property
    def is_sent(self) -> bool:
        """Whether the panel message has been created (first send done)."""
        return self._has_sent

    def mark_sent(self) -> None:
        """Mark that the panel message has been delivered to Telegram."""
        self._has_sent = True

    # -- Event handlers ------------------------------------------------------

    def on_thinking(self, content: str) -> bool:
        """Update thinking section.

        Returns True if the panel content changed.
        """
        if not content:
            return False
        if len(content) > self.max_thinking_len:
            content = content[: self.max_thinking_len - 3] + "..."
        self._thinking = content
        self._has_content = True
        return True

    def on_tool_start(self, name: str, args_summary: str = "") -> bool:
        """Add a running tool to the panel.

        Returns True if the panel content changed.
        """
        self._tools.append(ToolEntry(name=name, args_summary=args_summary))
        self._progress = None  # clear stale progress
        self._has_content = True
        return True

    def on_tool_result(self, name: str, success: bool) -> bool:
        """Mark a tool as completed (success or error).

        Matches the most recent running entry with the given name.
        Returns True if the panel content changed.
        """
        for tool in reversed(self._tools):
            if tool.name == name and tool.status == "running":
                tool.status = "success" if success else "error"
                break
        self._has_content = True
        return True

    def on_progress(self, message: str, percent: float | None = None) -> bool:
        """Update the progress line.

        Returns True if the panel content changed.
        """
        if not message:
            return False
        if percent is not None:
            self._progress = f"{message} ({percent:.0f}%)"
        else:
            self._progress = message
        self._has_content = True
        return True

    def finalize(self) -> None:
        """Mark the panel as finalized (session complete)."""
        self._finalized = True

    # -- Rendering -----------------------------------------------------------

    def render(self) -> str:
        """Render the full panel as a Telegram-Markdown-safe string."""
        lines: list[str] = []

        # -- Thinking section ------------------------------------------------
        if self._thinking:
            escaped = self._thinking.replace("_", "\\_")
            lines.append(f"{ICON_THINKING} _{escaped}_")
            lines.append("")

        # -- Tools section ---------------------------------------------------
        if self._tools:
            visible_tools = self._tools
            collapsed_count = 0

            # Collapse oldest completed tools when there are too many
            if len(self._tools) > self.max_tools_shown:
                collapsed_count = len(self._tools) - self.max_tools_shown
                visible_tools = self._tools[collapsed_count:]
                done = sum(
                    1 for t in self._tools[:collapsed_count] if t.status != "running"
                )
                failed = sum(
                    1 for t in self._tools[:collapsed_count] if t.status == "error"
                )
                summary = f"_{done} earlier tool{'s' if done != 1 else ''}"
                if failed:
                    summary += f" ({failed} failed)"
                summary += "_"
                lines.append(summary)

            for tool in visible_tools:
                icon = {
                    "running": ICON_TOOL_RUNNING,
                    "success": ICON_TOOL_SUCCESS,
                    "error": ICON_TOOL_ERROR,
                }[tool.status]
                line = f"  {icon} `{tool.name}`"
                if tool.args_summary:
                    line += f" {tool.args_summary}"
                lines.append(line)

            lines.append("")

        # -- Progress / working indicator ------------------------------------
        if self._finalized:
            total = len(self._tools)
            failed = sum(1 for t in self._tools if t.status == "error")
            if total > 0:
                summary = f"{ICON_DONE} {total} tool{'s' if total != 1 else ''} used"
                if failed:
                    summary += f" ({failed} failed)"
                lines.append(summary)
            else:
                lines.append(f"{ICON_DONE} Done")
        elif self._progress:
            lines.append(f"{ICON_PROGRESS} {self._progress}")
        elif self._tools:
            running = [t for t in self._tools if t.status == "running"]
            if running:
                lines.append(f"{ICON_PROGRESS} Running `{running[-1].name}`...")

        return "\n".join(lines).strip()
