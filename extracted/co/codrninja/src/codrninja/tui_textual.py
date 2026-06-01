"""Textual TUI for CodrNinja — split layout, collapsible tools, artifacts, PTY terminal."""

from __future__ import annotations

import json
import os
import random
import shlex
import threading
import time
import urllib.request
import uuid
from queue import Queue
from typing import Any, Optional

from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import (
    Button, Input, Label, ListItem, ListView,
    RichLog, Static, TabbedContent, TabPane,
)

from .agent import Agent, AgentMode
from .auth import OAuthFlow, TokenManager
from .core import AICode
from .mcp import MCPManager
from .oauth_providers import AnthropicOAuth, OpenAIOAuth
from .permissions import PermissionRule
from .session_viewmodel import SessionViewModel, ToolCallEntry
from .skills import SkillRegistry
from .todo import TodoManager, format_todo_item
from .tools import ToolRegistry

SLASH_COMMANDS = {
    "/build":       "Implement a task in build mode",
    "/clear":       "Clear messages",
    "/commit":      "Git commit changes",
    "/context":     "Show project context",
    "/customize":   "Customize agent name and persona",
    "/exec":        "Execute shell command",
    "/exit":        "Exit codrninja",
    "/explain":     "Explain code or concept",
    "/fetch":       "Fetch and clean a web page",
    "/files":       "List files in directory",
    "/help":        "Show detailed help",
    "/mcp":         "Manage MCP servers and tools",
    "/maxsteps":    "Set max steps limit",
    "/model":       "Show or change AI configuration",
    "/permissions": "Manage permission rules",
    "/plan":        "Plan a feature or task",
    "/reasoning":   "Set reasoning level (none/low/medium/high)",
    "/read":        "Read file",
    "/review":      "Review code for issues",
    "/search":      "Search the web",
    "/session":     "Show session info",
    "/skills":      "List installed skills",
    "/subagents":   "List active subagents",
    "/test":        "Run tests",
    "/todo":        "Manage session todos",
}

BUILTIN_SUBAGENTS = {
    "general": AgentMode.BUILD,
    "explore": AgentMode.PLAN,
}

PROVIDERS = {
    "ollama":     {"name": "Ollama (local)", "models": [], "needs_key": False, "default_url": "http://localhost:11434", "can_custom_url": True},
    "openai":     {"name": "OpenAI",         "models": ["gpt-4o", "gpt-4", "gpt-3.5-turbo"], "needs_key": True, "env_var": "OPENAI_API_KEY"},
    "anthropic":  {"name": "Anthropic",      "models": ["claude-3-opus-20240229", "claude-3-sonnet-20240229"], "needs_key": True, "env_var": "ANTHROPIC_API_KEY"},
    "openrouter": {"name": "OpenRouter",     "models": ["openai/gpt-4", "anthropic/claude-3-opus"], "needs_key": True, "env_var": "OPENROUTER_API_KEY"},
}

THINKING_MESSAGES = [
    "asking rubberduck", "cooking", "asking GPT for help",
    "downloading more RAM", "turning it off and on again",
    "consulting the rubber duck", "blaming the intern",
    "reading the docs (jk)", "stack overflowing",
    "vibing with the codebase", "pretending to understand",
    "grepping for answers", "checking if it works on my machine",
    "counting semicolons", "git blaming you",
    "deploying to prod (don't tell anyone)", "summoning the AI spirits",
    "sacrificing a function to the garbage collector",
    "asking the senior dev", "ignoring all previous instructions",
]

CONFIG_DIR  = os.path.expanduser("~/.config/codrninja")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


# ── helpers ───────────────────────────────────────────────────────────────────

def _format_tool_args(tool_name: str, args: dict[str, Any]) -> str:
    if tool_name in ("bash", "execute_command"):
        return str(args.get("command", ""))[:120]
    if tool_name in ("read_file", "write_file", "edit_file"):
        return str(args.get("path", args.get("file_path", "")))
    if tool_name in ("search", "search_files", "grep"):
        return str(args.get("pattern", args.get("query", "")))
    return str(args)[:120]


def _extract_reasoning(response: str) -> tuple[Optional[str], str]:
    import re
    patterns = [
        r"<thinking>(.*?)</thinking>",
        r"<reasoning>(.*?)</reasoning>",
        r"Reasoning:(.*?)(?=\n\n|$)",
        r"### Reasoning\n(.*?)(?=\n###|\Z)",
    ]
    parts, cleaned = [], response
    for p in patterns:
        for m in re.finditer(p, cleaned, re.DOTALL | re.IGNORECASE):
            t = m.group(1).strip()
            if t:
                parts.append(t)
        cleaned = re.sub(p, "", cleaned, flags=re.DOTALL | re.IGNORECASE)
    return ("\n\n".join(parts).strip() or None), cleaned.strip()


def _render_content(text: str):
    s = text.strip()
    if s.startswith("```") and s.endswith("```"):
        lines = s.split("\n")
        lang = lines[0].strip("`").strip() or "text"
        code = "\n".join(lines[1:-1])
        return Syntax(code, lang, theme="monokai", line_numbers=False)
    return Markdown(text or "")


# ── ToolCallWidget ─────────────────────────────────────────────────────────────

class ToolCallWidget(Widget):
    """
    Collapsible widget for a single tool call + result.
    Header: tool name | status | duration | step
    Body:   args (when expanded) + result (when expanded)
    """

    DEFAULT_CSS = """
    ToolCallWidget {
        height: auto;
        margin: 0 1;
        margin-bottom: 1;
    }
    ToolCallWidget .tool-header {
        height: 1;
        background: #1a1a1a;
        color: #888;
        padding: 0 1;
    }
    ToolCallWidget .tool-header:hover {
        background: #222;
        color: #aaa;
    }
    ToolCallWidget .tool-body {
        padding: 0 2;
        display: none;
        background: #111;
        border-left: solid #333;
        margin-left: 1;
    }
    ToolCallWidget .tool-body.expanded {
        display: block;
    }
    """

    def __init__(self, entry: ToolCallEntry) -> None:
        super().__init__(id=f"tool-{entry.call_id}")
        self.entry = entry
        self._expanded = False

    def compose(self) -> ComposeResult:
        yield Static(self._header_text(), classes="tool-header", id=f"th-{self.entry.call_id}")
        with Container(classes="tool-body", id=f"tb-{self.entry.call_id}"):
            args_str = json.dumps(self.entry.args, indent=2, ensure_ascii=False)
            yield Static(f"[dim]args[/dim]\n{args_str}", id=f"ta-{self.entry.call_id}", markup=True)
            yield Static("", id=f"tr-{self.entry.call_id}")

    def _header_text(self) -> str:
        entry = self.entry
        if entry.success is None:
            status = "[yellow]running[/yellow]"
        elif entry.success:
            status = f"[green]done[/green] [dim]{entry.duration_ms}ms[/dim]"
        else:
            status = "[red]failed[/red]"

        args_preview = _format_tool_args(entry.tool_name, entry.args)
        toggle = "v" if self._expanded else ">"
        return (
            f"[dim]{toggle}[/dim] [bold yellow]{entry.tool_name}[/bold yellow]"
            f"  [dim]{args_preview[:60]}[/dim]"
            f"  {status}"
            f"  [dim]step {entry.step}[/dim]"
        )

    def on_click(self) -> None:
        self._expanded = not self._expanded
        body = self.query_one(f"#tb-{self.entry.call_id}", Container)
        if self._expanded:
            body.add_class("expanded")
        else:
            body.remove_class("expanded")
        self.query_one(f"#th-{self.entry.call_id}", Static).update(self._header_text())

    def update_result(self, output: str, success: bool) -> None:
        self.entry.finish(output, success)
        self.query_one(f"#th-{self.entry.call_id}", Static).update(self._header_text())
        color = "green" if success else "red"
        preview = output[:500] + ("..." if len(output) > 500 else "")
        if output.strip().startswith(("{", "[")):
            content = Syntax(preview, "json", theme="monokai", line_numbers=False)
        else:
            content = Text(preview, style="dim")
        result_static = self.query_one(f"#tr-{self.entry.call_id}", Static)
        result_static.update(Panel(content, border_style=f"{color} dim", padding=(0, 1)))

    def update_running(self) -> None:
        self.query_one(f"#th-{self.entry.call_id}", Static).update(self._header_text())


# ── MessageTimeline ────────────────────────────────────────────────────────────

class MessageTimeline(ScrollableContainer):
    """
    Left panel — chat messages + inline tool call widgets.
    Uses individual Static/ToolCallWidget nodes so streaming
    updates a single node without re-rendering everything.
    """

    DEFAULT_CSS = """
    MessageTimeline {
        background: #0d0d0d;
        padding: 1 2;
    }
    MessageTimeline .msg-user {
        margin-bottom: 1;
    }
    MessageTimeline .msg-assistant {
        margin-bottom: 1;
    }
    MessageTimeline .msg-system {
        margin-bottom: 1;
    }
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._assistant_widgets: dict[str, Static] = {}
        self._reasoning_widgets: dict[str, Static] = {}
        self._tool_widgets: dict[str, ToolCallWidget] = {}
        self._thinking_widget: Optional[Static] = None
        self._thinking_widget_key: str = ""

    # ── public API ──────────────────────────────────────────────────────────

    def add_user_message(self, text: str) -> None:
        w = Static(
            Panel(Text(text, style="white"), title="[bold cyan]you[/bold cyan]", border_style="cyan", padding=(0, 1)),
            classes="msg-user",
        )
        self.mount(w)
        self.scroll_end(animate=False)

    def add_system_message(self, text: str, title: str = "system") -> None:
        w = Static(
            Panel(_render_content(text), title=f"[bold white]{title}[/bold white]", border_style="#555555", padding=(0, 1)),
            classes="msg-system",
        )
        self.mount(w)
        self.scroll_end(animate=False)

    def add_error(self, error: str) -> None:
        w = Static(
            Panel(Text(error, style="red"), title="[bold red]error[/bold red]", border_style="red"),
            classes="msg-system",
        )
        self.mount(w)
        self.scroll_end(animate=False)

    def upsert_assistant(self, full_text: str, model: str, message_id: str = "assistant", agent_name: str = "assistant") -> None:
        renderable = Panel(
            _render_content(full_text),
            title=f"[bold green]{agent_name}[/bold green] [dim]{model}[/dim]",
            border_style="green",
            padding=(0, 1),
        )
        if message_id in self._assistant_widgets:
            self._assistant_widgets[message_id].update(renderable)
        else:
            w = Static(renderable, classes="msg-assistant")
            self._assistant_widgets[message_id] = w
            self.mount(w)
        self.scroll_end(animate=False)

    def upsert_reasoning(self, full_text: str, model: str, message_id: str = "reasoning") -> None:
        renderable = Panel(
            _render_content(full_text),
            title=f"[dim]reasoning[/dim] [dim]{model}[/dim]",
            border_style="dim",
            padding=(0, 1),
        )
        if message_id in self._reasoning_widgets:
            self._reasoning_widgets[message_id].update(renderable)
        else:
            w = Static(renderable, classes="msg-assistant")
            self._reasoning_widgets[message_id] = w
            self.mount(w)
        self.scroll_end(animate=False)

    def add_tool_call(self, entry: ToolCallEntry) -> ToolCallWidget:
        w = ToolCallWidget(entry)
        self._tool_widgets[entry.call_id] = w
        self.mount(w)
        self.scroll_end(animate=False)
        return w

    def update_tool_result(self, call_id: str, output: str, success: bool) -> None:
        if call_id in self._tool_widgets:
            self._tool_widgets[call_id].update_result(output, success)
        self.scroll_end(animate=False)

    def show_thinking(self, msg: str, dots: str, widget_key: str) -> None:
        renderable = Panel(
            Text(f"  {msg} {dots}", style="dim italic"),
            title="[dim yellow]thinking[/dim yellow]",
            border_style="#665500",
            padding=(0, 0),
        )
        if self._thinking_widget is not None and self._thinking_widget_key == widget_key:
            self._thinking_widget.update(renderable)
        else:
            if self._thinking_widget is not None:
                try:
                    self._thinking_widget.remove()
                except Exception:
                    pass
            w = Static(renderable, classes="msg-system")
            self._thinking_widget = w
            self._thinking_widget_key = widget_key
            self.mount(w)
            self.scroll_end(animate=False)

    def remove_thinking(self, widget_key: str = "") -> None:
        if self._thinking_widget is not None:
            if not widget_key or self._thinking_widget_key == widget_key:
                try:
                    self._thinking_widget.remove()
                except Exception:
                    pass
                self._thinking_widget = None
                self._thinking_widget_key = ""

    def clear(self) -> None:
        self.query("*").remove()
        self._assistant_widgets.clear()
        self._reasoning_widgets.clear()
        self._tool_widgets.clear()
        self._thinking_widget = None
        self._thinking_widget_key = ""


# ── Context Panel ──────────────────────────────────────────────────────────────

class ContextPanel(RichLog):
    """Session info, tokens, steps, permissions."""

    def refresh_context(self, vm: SessionViewModel, agent: Optional[Agent]) -> None:
        self.clear()
        lines = [
            f"Session:   {vm.session_name}",
            f"Model:     {vm.model}",
            f"Provider:  {vm.provider}",
            f"Steps:     {vm.current_steps}/{vm.max_steps}",
            f"Tokens:    {vm.tokens}",
            f"Status:    {vm.status}",
        ]
        if agent:
            lines.append(f"Mode:      {agent.mode}")
            lines.append(f"Perms:     {agent.permissions.mode}")
        self.write(Panel("\n".join(lines), title="[bold white]context[/bold white]", border_style="#555555"))


# ── Modal screens ──────────────────────────────────────────────────────────────

class SessionPickerScreen(ModalScreen[Optional[str]]):
    CSS = """
    SessionPickerScreen { align: center middle; }
    #session-picker-dialog {
        width: 84; height: 30;
        background: $surface; border: round $accent; padding: 1;
    }
    #session-picker-list { height: 1fr; border: solid #444; margin-top: 1; }
    #session-picker-new-name { margin-top: 1; }
    #session-picker-hint { margin-top: 1; color: #888; }
    """

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("enter", "select", "Select"),
    ]

    def __init__(self, sessions: list[dict[str, Any]]) -> None:
        super().__init__()
        self.sessions = sessions

    def compose(self) -> ComposeResult:
        with Container(id="session-picker-dialog"):
            yield Label("Select a session or create a new one")
            items = [ListItem(Label(self._format_session_label(session))) for session in self.sessions]
            items.append(ListItem(Label("+ new session")))
            yield ListView(*items, id="session-picker-list")
            yield Input(placeholder="New session name...", id="session-picker-new-name")
            yield Label("[dim]enter select  escape cancel[/dim]", id="session-picker-hint", markup=True)

    def _format_session_label(self, session: dict[str, Any]) -> str:
        name = str(session.get("name", "unnamed"))
        count = int(session.get("message_count", 0) or 0)
        suffix = "message" if count == 1 else "messages"
        return f"{name}  [dim]{count} {suffix}[/dim]"

    def on_mount(self) -> None:
        lv = self.query_one("#session-picker-list", ListView)
        lv.focus()
        if lv.children:
            lv.index = 0
            lv.scroll_visible()

    def _selected_index(self) -> int:
        lv = self.query_one("#session-picker-list", ListView)
        return lv.index or 0

    def _selection_value(self) -> Optional[str]:
        idx = self._selected_index()
        if idx < len(self.sessions):
            return str(self.sessions[idx].get("name", "")) or None
        name = self.query_one("#session-picker-new-name", Input).value.strip()
        return name or None

    def action_select(self) -> None:
        self.dismiss(self._selection_value())

    def action_cancel(self) -> None:
        self.dismiss(None)

    @on(ListView.Selected, "#session-picker-list")
    def select_item(self, event: ListView.Selected) -> None:
        idx = event.list_view.index or 0
        if idx == len(self.sessions):
            self.query_one("#session-picker-new-name", Input).focus()
            return
        self.dismiss(str(self.sessions[idx].get("name", "")) or None)

    @on(Input.Submitted, "#session-picker-new-name")
    def submit_new_session(self, event: Input.Submitted) -> None:
        name = event.value.strip()
        self.dismiss(name or None)


class PermissionPromptScreen(ModalScreen[str]):
    CSS = """
    PermissionPromptScreen { align: center middle; }
    #permission-dialog {
        width: 80; height: auto;
        background: $surface; border: round $accent; padding: 1 2;
    }
    #permission-buttons { height: auto; margin-top: 1; }
    Button { margin-right: 1; }
    """

    def __init__(self, tool_name: str, params: dict[str, Any], action: str, target: str) -> None:
        super().__init__()
        self.tool_name = tool_name
        self.params    = params
        self.action    = action
        self.target    = target

    def compose(self) -> ComposeResult:
        formatted = json.dumps(self.params, indent=2, ensure_ascii=False)
        with Container(id="permission-dialog"):
            yield Static(
                f"[bold]Permission Request[/bold]\n\n"
                f"Tool:   {self.tool_name}\n"
                f"Action: {self.action}\n"
                f"Target: {self.target or '(none)'}\n\n"
                f"[dim]{formatted}[/dim]",
                markup=True,
            )
            with Horizontal(id="permission-buttons"):
                yield Button("Allow",        id="allow",  variant="success")
                yield Button("Always Allow", id="always", variant="primary")
                yield Button("Deny",         id="deny",   variant="error")
                yield Button("Never Allow",  id="never",  variant="error")

    @on(Button.Pressed)
    def handle_button(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id or "deny")


class SelectionScreen(ModalScreen[Optional[str]]):
    CSS = """
    SelectionScreen { align: center middle; }
    #selection-dialog {
        width: 80; height: 28;
        background: $surface; border: round $accent; padding: 1;
    }
    ListView { height: 1fr; border: solid #444; }
    """

    def __init__(self, title: str, options: list[str]) -> None:
        super().__init__()
        self.dialog_title = title
        self.options      = options

    def compose(self) -> ComposeResult:
        with Container(id="selection-dialog"):
            yield Label(self.dialog_title)
            yield ListView(*[ListItem(Label(opt)) for opt in self.options], id="selection-list")
            yield Label("[dim]enter select  esc cancel[/dim]")

    def on_mount(self) -> None:
        lv = self.query_one(ListView)
        lv.focus()
        if self.options:
            lv.index = 0
            lv.scroll_visible()

    @on(ListView.Selected)
    def select_item(self, event: ListView.Selected) -> None:
        self.dismiss(self.options[event.list_view.index or 0])

    def on_key(self, event: Any) -> None:
        if event.key == "escape":
            self.dismiss(None)


class CommandPalette(Widget):
    DEFAULT_CSS = """
    CommandPalette {
        height: auto;
        dock: bottom;
        background: #111;
        border-top: solid #333;
        display: none;
        max-height: 10;
    }
    CommandPalette.visible {
        display: block;
    }
    CommandPalette ListView {
        height: auto;
        max-height: 8;
        border: none;
        background: #111;
    }
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.matches: list[str] = []

    def compose(self) -> ComposeResult:
        yield ListView(id="cmd-palette-list")

    def show_matches(self, query: str) -> None:
        self.matches = [cmd for cmd in SLASH_COMMANDS if cmd.startswith(query)] if query.startswith("/") else []
        lv = self.query_one("#cmd-palette-list", ListView)
        lv.clear()
        for cmd in self.matches:
            lv.append(ListItem(Label(f"{cmd}  [dim]{SLASH_COMMANDS[cmd]}[/dim]", markup=True)))
        if self.matches:
            self.add_class("visible")
            lv.index = 0
        else:
            self.hide()

    def hide(self) -> None:
        self.remove_class("visible")

    def visible(self) -> bool:
        return self.has_class("visible") and bool(self.matches)

    def current_selection(self) -> Optional[str]:
        if not self.matches:
            return None
        lv = self.query_one("#cmd-palette-list", ListView)
        idx = lv.index or 0
        if idx < 0 or idx >= len(self.matches):
            return None
        return self.matches[idx]


# ── StatusBar ──────────────────────────────────────────────────────────────────

class StatusBar(Label):
    def update_status(self, model: str, steps: int, max_steps: int, status: str, tokens: int, thinking_msg: str = "") -> None:
        color = {"ready": "green", "thinking": "yellow", "running": "cyan", "error": "red"}.get(status, "green")
        suffix = f"  [dim]{thinking_msg}[/dim]" if thinking_msg and status in {"thinking", "running"} else ""
        self.update(
            f"[bold]{model}[/bold]  [{color}]{status}[/{color}]"
            f"  [dim]{steps}/{max_steps} steps  {tokens} tokens[/dim]"
            f"{suffix}"
        )


# ── Main App ───────────────────────────────────────────────────────────────────

class CodrninjaTUI(App[None]):

    CSS = """
    Screen { background: #0d0d0d; }

    StatusBar {
        height: 1; dock: top;
        background: #1a1a1a; color: #888;
        padding: 0 2; border-bottom: solid #333;
    }

    #bottom-bar {
        height: 1;
        background: #1a1a1a; color: #555; padding: 0 2;
    }

    #input-row {
        height: 3; dock: bottom;
        background: #111; border-top: solid #333; padding: 0 1;
    }

    Input {
        background: #111; border: none; color: white; padding: 0 1;
    }
    Input:focus { border: solid #444; }

    #main-split { height: 1fr; }

    MessageTimeline {
        width: 1fr;
        border-right: solid #222;
    }

    #side-panel {
        width: 45;
        background: #0d0d0d;
    }

    TabbedContent { height: 1fr; }

    TabPane { padding: 0; }

    ContextPanel { height: 1fr; padding: 1; }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+l", "clear", "Clear"),
        Binding("ctrl+y", "copy_last", "Copy last response"),
        Binding("escape", "cancel", "Cancel"),
    ]

    model          = reactive("codellama")
    is_busy        = reactive(False)
    current_status = reactive("ready")

    def __init__(self, ai: AICode, session_name: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.ai            = ai
        self.session_name  = session_name
        self.console_tools = ToolRegistry()
        self.mcp           = MCPManager()
        self.skill_registry = SkillRegistry()
        self.skill_registry.discover()
        self.skill_registry.register_tools(self.console_tools)
        self.agent:          Optional[Agent]          = None
        self.pending_agent:  Optional[Agent]          = None
        self.vm:             Optional[SessionViewModel] = None
        self.last_tokens     = 0
        self.current_steps   = 0
        self.current_max_steps = int(os.environ.get("CODRNINJA_MAX_STEPS", "50"))
        self.model           = self.ai.config.default_model
        cfg = self._load_config()
        self._agent_name     = str(cfg.get("agent_name", "assistant"))
        self._thinking_msg: str = ""
        self._current_turn_id: str = str(uuid.uuid4())
        self._thinking_placeholder: bool = False
        self._dots_frame: int = 0
        self._progress_queue: Queue[tuple[str, dict[str, Any]]] = Queue()
        self._input_history: list[str] = []
        self._history_idx: int = 0
        self._history_draft: str = ""

    # ── layout ─────────────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        yield StatusBar("ready", id="status")

        with Horizontal(id="main-split"):
            yield MessageTimeline(id="timeline")

            with Container(id="side-panel"):
                with TabbedContent():
                    with TabPane("context", id="tab-context"):
                        yield ContextPanel(id="context-panel", highlight=False, markup=True)

        yield CommandPalette(id="cmd-palette")

        with Horizontal(id="input-row"):
            yield Input(placeholder=" Type a message or /command...", id="prompt")

        yield Label(
            "[dim]enter send  ctrl+l clear  ctrl+c quit[/dim]",
            id="bottom-bar",
        )

    def on_mount(self) -> None:
        self.set_interval(0.05, self._drain_progress_queue)
        self.set_interval(2.0, self._rotate_thinking_msg)
        self.set_interval(0.4, self._tick_dots)
        self._set_status("ready")
        if self.session_name is None:
            self.run_worker(self._show_session_picker(), exclusive=True)
        else:
            self._init_session(self.session_name)

    def _init_session(self, session_name: str) -> None:
        self.session_name = session_name
        if self.session_name and not self.ai.get_session(self.session_name):
            self.ai.create_session(self.session_name)
        if self.session_name:
            self.agent = Agent(self.ai, self.session_name)
            self.current_max_steps = self.agent.max_steps
        self.vm = SessionViewModel(
            session_name=self.session_name or "default",
            model=self.model,
            provider=self.ai.config.default_provider,
            max_steps=self.current_max_steps,
        )
        self.query_one("#prompt", Input).focus()
        timeline = self.query_one("#timeline", MessageTimeline)
        timeline.add_system_message(
            f"Session: {self.session_name}\nProvider: {self.ai.config.default_provider}\nType /help for commands.",
            title="codrninja",
        )
        # Load previous messages from this session
        try:
            past = self.ai.session_manager.get_messages(session_name, limit=50)
            # Agent saves the full context blob ("Current directory: ...") as
            # the "user" message — filter those out, only keep clean human input.
            _CTX_MARKERS = ("Current directory:", "You are an expert", "Available tools:")
            visible = [
                m for m in past
                if m.get("content")
                and not (
                    m.get("role") == "user"
                    and (
                        len(m["content"]) > 800
                        or any(m["content"].lstrip().startswith(mk) for mk in _CTX_MARKERS)
                    )
                )
            ]
            if visible:
                timeline.add_system_message(
                    f"{len(visible)} previous message(s)",
                    title="history",
                )
                for msg in visible:
                    role = msg.get("role", "")
                    content = msg.get("content", "")
                    if role == "user":
                        timeline.add_user_message(content)
                    elif role == "assistant":
                        model_name = msg.get("model") or self.model
                        timeline.upsert_assistant(
                            content, model_name,
                            str(uuid.uuid4()),
                            self._agent_name,
                        )
        except Exception:
            pass
        self._refresh_context()

    async def _show_session_picker(self) -> None:
        session_name = await self._interactive_session_flow()
        if not session_name:
            session_name = self._ensure_session()
        self._init_session(session_name)

    # ── input ──────────────────────────────────────────────────────────────

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id != "prompt":
            return
        if not event.value.strip() or self.is_busy:
            return
        msg = event.value.strip()
        if msg:
            self._input_history.append(msg)
            self._history_idx = len(self._input_history)
            self._history_draft = ""
        event.input.value = ""
        if msg.startswith("/"):
            self.handle_command(msg)
            return
        if self._handle_subagent_mention(msg):
            return
        self.run_agent_task(msg, AgentMode.BUILD)

    # ── agent task ─────────────────────────────────────────────────────────

    @work(exclusive=True)
    async def handle_command(self, message: str) -> None:
        self.query_one("#timeline", MessageTimeline).add_user_message(message)
        stripped = message.strip()
        if stripped == "/model":
            await self._interactive_model_flow()
            self.query_one("#prompt", Input).focus()
            return
        if stripped == "/session":
            await self._interactive_session_flow()
            self.query_one("#prompt", Input).focus()
            return
        keep = self._execute_command(message)
        if not keep:
            self.exit()
        self.query_one("#prompt", Input).focus()

    @work(thread=True, exclusive=True)
    def run_agent_task(self, message: str, mode: str) -> None:
        self.call_from_thread(self._begin_task_ui, message)
        try:
            self.agent = Agent(self.ai, self.session_name, mode=mode)
            self.pending_agent = self.agent
            self.current_steps = 0
            self.current_max_steps = self.agent.max_steps
            if self.vm:
                self.vm.max_steps = self.agent.max_steps
            self.agent.permission_handler = self._handle_permission_request
            final_result: Optional[dict[str, Any]] = None
            for event in self.agent.stream_run(message, auto_approve=False):
                etype = event.get("type")
                if etype == "assistant_chunk":
                    self._progress_queue.put(("assistant_chunk", {
                        "text": event.get("text", ""),
                        "id":   self._current_turn_id,
                    }))
                elif etype == "result":
                    final_result = event.get("result")
                elif etype in {"tool_start", "tool_result", "status"}:
                    self._progress_queue.put((etype, event))
            if final_result is not None:
                self.call_from_thread(self._render_agent_result, final_result)
        except Exception as exc:
            self.call_from_thread(self.query_one("#timeline", MessageTimeline).add_error, str(exc))
            self.call_from_thread(self._set_status, "error")
        finally:
            self.pending_agent = None
            self.is_busy = False
            self.call_from_thread(self.query_one("#prompt", Input).focus)

    def _begin_task_ui(self, message: str) -> None:
        self.is_busy = True
        self._current_turn_id = str(uuid.uuid4())
        self._dots_frame = 0
        timeline = self.query_one("#timeline", MessageTimeline)
        timeline.add_user_message(message)
        self._set_status("thinking")
        self._thinking_placeholder = True
        self._update_thinking_display()

    def _render_agent_result(self, result: dict[str, Any]) -> None:
        self._thinking_placeholder = False
        timeline = self.query_one("#timeline", MessageTimeline)
        timeline.remove_thinking(self._current_turn_id)
        self.current_steps = int(result.get("tool_calls", self.current_steps))
        self.current_max_steps = int(result.get("max_steps", self.current_max_steps))
        if not result.get("success"):
            timeline.add_error(str(result.get("error", "Unknown error")))
            self._set_status("error")
            return
        response = str(result.get("response", ""))
        reasoning, cleaned = _extract_reasoning(response)
        self.last_tokens = int(result.get("tokens", {}).get("output", 0) or len(cleaned) // 4)
        if reasoning:
            timeline.upsert_reasoning(reasoning, self.model, f"reasoning-{self._current_turn_id}")
        if cleaned:
            timeline.upsert_assistant(cleaned, self.model, self._current_turn_id, self._agent_name)
        if self.vm:
            self.vm.tokens = self.last_tokens
            self.vm.refresh_all_artifacts()
        self._refresh_artifacts()
        self._refresh_context()
        self._set_status("ready", self.last_tokens)

    # ── progress queue ─────────────────────────────────────────────────────

    def _drain_progress_queue(self) -> None:
        timeline = self.query_one("#timeline", MessageTimeline)
        processed = 0
        while not self._progress_queue.empty() and processed < 20:
            processed += 1
            event, payload = self._progress_queue.get()

            if event == "tool_start":
                call_id = payload.get("call_id", str(uuid.uuid4()))
                tool_name = payload.get("tool", "")
                args = payload.get("args", {})
                step = payload.get("step", self.current_steps + 1)
                if self.vm:
                    entry = self.vm.on_tool_start(call_id, tool_name, args, step)
                    timeline.add_tool_call(entry)
                self._set_status("running")

            elif event == "tool_result":
                call_id = payload.get("call_id", "")
                output = payload.get("output", "")
                success = payload.get("success", True)
                if self.vm:
                    self.vm.on_tool_result(call_id, output, success)
                    timeline.update_tool_result(call_id, output, success)
                self._set_status("thinking")

            elif event == "assistant_chunk":
                text = payload.get("text", "")
                mid = payload.get("id", "assistant")
                if self._thinking_placeholder:
                    self._thinking_placeholder = False
                    timeline.remove_thinking(self._current_turn_id)
                reasoning, cleaned = _extract_reasoning(text)
                if reasoning:
                    timeline.upsert_reasoning(reasoning, self.model, f"reasoning-{mid}")
                if cleaned:
                    timeline.upsert_assistant(cleaned, self.model, mid, self._agent_name)

            elif event == "status":
                self._set_status("thinking")

    # ── permission ──────────────────────────────────────────────────────────

    def _handle_permission_request(self, tool_name: str, params: dict[str, Any], action: str, target: str) -> str:
        done = threading.Event()
        holder: dict[str, str] = {"v": "deny"}

        def _on_dismiss(value: Optional[str]) -> None:
            selected = value or "deny"
            allowed = {"allow", "always", "deny", "never"}
            holder["v"] = selected if selected in allowed else "deny"
            done.set()

        def _show() -> None:
            try:
                self.push_screen(
                    PermissionPromptScreen(tool_name, params, action, target),
                    callback=_on_dismiss,
                )
            except Exception:
                done.set()

        self.call_from_thread(_show)
        done.wait(timeout=120)
        return holder.get("v", "deny")

    # ── actions ─────────────────────────────────────────────────────────────

    def action_copy_last(self) -> None:
        """Copy the last assistant response to the system clipboard."""
        timeline = self.query_one("#timeline", MessageTimeline)
        # Find the last assistant widget (most recently added key)
        if not timeline._assistant_widgets:
            self.query_one("#status", StatusBar).update(
                "[dim]nothing to copy[/dim]"
            )
            return
        last_key = list(timeline._assistant_widgets)[-1]
        widget = timeline._assistant_widgets[last_key]
        # Extract plain text from the renderable stored in the Static widget
        try:
            renderable = widget.renderable
            from rich.console import Console as _Console
            from io import StringIO
            buf = StringIO()
            c = _Console(file=buf, highlight=False, markup=False, width=9999)
            c.print(renderable)
            text = buf.getvalue().strip()
        except Exception:
            text = ""
        if not text:
            return
        copied = False
        try:
            import subprocess, sys as _sys
            if _sys.platform == "darwin":
                subprocess.run(["pbcopy"], input=text.encode(), check=True)
                copied = True
            elif _sys.platform.startswith("linux"):
                for cmd in (["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]):
                    try:
                        subprocess.run(cmd, input=text.encode(), check=True)
                        copied = True
                        break
                    except FileNotFoundError:
                        continue
            elif _sys.platform == "win32":
                subprocess.run(["clip"], input=text.encode("utf-16"), check=True)
                copied = True
        except Exception:
            pass
        tl = self.query_one("#timeline", MessageTimeline)
        if copied:
            tl.add_system_message(f"Copied {len(text)} chars to clipboard", title="copy")
        else:
            tl.add_system_message("Could not access clipboard (install xclip or xsel on Linux)", title="copy")

    def action_clear(self) -> None:
        self._thinking_placeholder = False
        self.query_one("#timeline", MessageTimeline).clear()
        if self.vm:
            self.vm.tool_calls.clear()
            self.vm.terminal_lines.clear()

    def action_cancel(self) -> None:
        self.is_busy = False
        self._set_status("ready", self.last_tokens)

    # ── status ──────────────────────────────────────────────────────────────

    def _set_status(self, status: str, tokens: Optional[int] = None) -> None:
        self.current_status = status
        if status in {"thinking", "running"}:
            choices = [m for m in THINKING_MESSAGES if m != self._thinking_msg] or THINKING_MESSAGES
            self._thinking_msg = random.choice(choices)
        else:
            self._thinking_msg = ""
        if self.vm:
            self.vm.status = status
        self.query_one("#status", StatusBar).update_status(
            self.model,
            self.current_steps,
            self.current_max_steps,
            status,
            self.last_tokens if tokens is None else tokens,
            self._thinking_msg,
        )

    def _refresh_artifacts(self) -> None:
        return

    def _refresh_context(self) -> None:
        if self.vm:
            self.query_one("#context-panel", ContextPanel).refresh_context(self.vm, self.agent)

    def _rotate_thinking_msg(self) -> None:
        if not self.is_busy or self.current_status not in {"thinking", "running"}:
            return
        try:
            idx = THINKING_MESSAGES.index(self._thinking_msg)
        except ValueError:
            idx = -1
        self._thinking_msg = THINKING_MESSAGES[(idx + 1) % len(THINKING_MESSAGES)]
        self._dots_frame = 0
        self.query_one("#status", StatusBar).update_status(
            self.model,
            self.current_steps,
            self.current_max_steps,
            self.current_status,
            self.last_tokens,
            self._thinking_msg,
        )
        if self._thinking_placeholder:
            self._update_thinking_display()

    def _update_thinking_display(self) -> None:
        dots = ["·  ", "·· ", "···"][self._dots_frame % 3]
        try:
            self.query_one("#timeline", MessageTimeline).show_thinking(
                self._thinking_msg, dots, self._current_turn_id
            )
        except Exception:
            pass

    def _tick_dots(self) -> None:
        if not self._thinking_placeholder:
            return
        self._dots_frame = (self._dots_frame + 1) % 3
        self._update_thinking_display()

    @on(Input.Changed, "#prompt")
    def on_input_changed(self, event: Input.Changed) -> None:
        palette = self.query_one("#cmd-palette", CommandPalette)
        value = event.value.strip()
        if value.startswith("/"):
            palette.show_matches(value)
        else:
            palette.hide()

    def on_key(self, event: Any) -> None:
        palette = self.query_one("#cmd-palette", CommandPalette)
        prompt = self.query_one("#prompt", Input)
        if palette.visible():
            lv = palette.query_one("#cmd-palette-list", ListView)
            if event.key == "escape":
                palette.hide()
                event.stop()
            elif event.key == "down":
                if palette.matches:
                    lv.index = min((lv.index or 0) + 1, len(palette.matches) - 1)
                event.stop()
            elif event.key == "up":
                if palette.matches:
                    lv.index = max((lv.index or 0) - 1, 0)
                event.stop()
            elif event.key == "tab":
                selection = palette.current_selection()
                if selection:
                    prompt.value = f"{selection} "
                    prompt.cursor_position = len(prompt.value)
                palette.hide()
                event.stop()
            elif event.key == "enter":
                selection = palette.current_selection()
                if selection:
                    prompt.value = f"{selection} "
                    prompt.cursor_position = len(prompt.value)
                    palette.hide()
                    event.stop()
            return

        if self.focused is not prompt or event.key not in {"up", "down"}:
            return
        if not self._input_history:
            return

        if event.key == "up":
            if self._history_idx == len(self._input_history):
                self._history_draft = prompt.value
            if self._history_idx > 0:
                self._history_idx -= 1
                prompt.value = self._input_history[self._history_idx]
                prompt.cursor_position = len(prompt.value)
            event.stop()
            return

        if self._history_idx < len(self._input_history) - 1:
            self._history_idx += 1
            prompt.value = self._input_history[self._history_idx]
        else:
            self._history_idx = len(self._input_history)
            prompt.value = self._history_draft
        prompt.cursor_position = len(prompt.value)
        event.stop()

    # ── commands ─────────────────────────────────────────────────────────────

    def _execute_command(self, message: str) -> bool:
        parts = shlex.split(message)
        if not parts:
            return True
        cmd  = parts[0].lower()
        args = parts[1:]
        tl   = self.query_one("#timeline", MessageTimeline)

        handlers: dict[str, Any] = {
            "/exit":        lambda: False,
            "/clear":       lambda: (self.action_clear(), True)[1],
            "/help":        lambda: (tl.add_system_message("\n".join(f"{n:14} {d}" for n, d in SLASH_COMMANDS.items()), title="help"), True)[1],
            "/session":     lambda: (self._show_session_info(), True)[1],
            "/context":     lambda: (self._show_context(), True)[1],
            "/customize":   lambda: (self._handle_customize(args), True)[1],
            "/maxsteps":    lambda: (self._set_maxsteps(args), True)[1],
            "/model":       lambda: (self._show_model_info(args), True)[1],
            "/files":       lambda: (self._list_files(args), True)[1],
            "/read":        lambda: (self._read_file(args), True)[1],
            "/exec":        lambda: (self._exec_command_handler(args), True)[1],
            "/search":      lambda: (self._search_web(args), True)[1],
            "/fetch":       lambda: (self._fetch_page(args), True)[1],
            "/build":       lambda: (self.run_agent_task(" ".join(args), AgentMode.BUILD), True)[1],
            "/plan":        lambda: (self.run_agent_task(" ".join(args), AgentMode.PLAN), True)[1],
            "/review":      lambda: (self.run_agent_task(f"Review this code:\n\n{' '.join(args)}", AgentMode.PLAN), True)[1],
            "/explain":     lambda: (self.run_agent_task(f"Explain: {' '.join(args)}", AgentMode.PLAN), True)[1],
            "/test":        lambda: (self._run_tests(args), True)[1],
            "/commit":      lambda: (self._commit_changes(args), True)[1],
            "/reasoning":   lambda: (self._set_reasoning(args), True)[1],
            "/todo":        lambda: (self._handle_todo(args), True)[1],
            "/permissions": lambda: (self._handle_permissions(args), True)[1],
            "/mcp":         lambda: (self._handle_mcp_command(args), True)[1],
            "/skills":      lambda: (self._show_skills(), True)[1],
            "/subagents":   lambda: (self._list_subagents(), True)[1],
        }

        if cmd in handlers:
            result = handlers[cmd]()
            return result if result is not None else True

        tl.add_error(f"Unknown command: {cmd}")
        return True

    # ── session helpers ───────────────────────────────────────────────────

    def _ensure_session(self) -> str:
        if (e := os.environ.get("CODRNINJA_SESSION")):
            return e
        sessions = self.ai.list_sessions()
        return sessions[0].get("name", "default") if sessions else "default"

    def _handle_subagent_mention(self, message: str) -> bool:
        if not message.startswith("@"):
            return False
        parts = message.split(None, 1)
        name  = parts[0][1:]
        task  = parts[1] if len(parts) > 1 else ""
        self.run_agent_task(task, BUILTIN_SUBAGENTS.get(name.lower(), AgentMode.BUILD))
        return True

    def _show_session_info(self) -> None:
        tl = self.query_one("#timeline", MessageTimeline)
        if not self.session_name:
            tl.add_error("No active session")
            return
        history = self.ai.get_history(self.session_name)
        if not history:
            tl.add_error(f"Session '{self.session_name}' not found")
            return
        msgs = history.get("messages", [])
        tl.add_system_message(
            f"Name: {self.session_name}\nMessages: {len(msgs)}\nCreated: {history.get('created_at', 'Unknown')}",
            title="session",
        )

    def _show_context(self) -> None:
        self._refresh_context()
        self.query_one("#timeline", MessageTimeline).add_system_message(
            f"Model: {self.ai.config.default_model}\n"
            f"Provider: {self.ai.config.default_provider}\n"
            f"Steps: {self.current_steps}/{self.current_max_steps}",
            title="context",
        )

    async def _interactive_session_flow(self) -> Optional[str]:
        chosen = await self.push_screen_wait(SessionPickerScreen(self._session_picker_items()))
        if chosen is None:
            return None
        chosen = chosen.strip()
        if not chosen:
            return None
        if chosen != self.session_name:
            self._init_session(chosen)
        return chosen

    def _session_picker_items(self) -> list[dict[str, Any]]:
        sessions = []
        for session in self.ai.list_sessions():
            name = str(session.get("name", "")).strip()
            if not name:
                continue
            history = self.ai.get_history(name) or {}
            messages = history.get("messages", []) or []
            sessions.append({
                **session,
                "message_count": len(messages),
            })
        return sessions

    # ── model flow ─────────────────────────────────────────────────────────

    async def _interactive_model_flow(self) -> None:
        cfg = self._load_config()
        current_provider = cfg.get("provider", self.ai.config.default_provider)
        current_model = cfg.get("model", self.ai.config.default_model)
        provider_keys = list(PROVIDERS.keys())
        provider_labels = [
            f"* {info['name']}" if key == current_provider else info["name"]
            for key, info in PROVIDERS.items()
        ]
        chosen = await self.push_screen_wait(SelectionScreen("Select AI provider", provider_labels))
        if chosen is None:
            return
        provider_index = provider_labels.index(chosen)
        provider_key = provider_keys[provider_index]
        provider_info = PROVIDERS[provider_key]

        env_var = provider_info.get("env_var", "")
        stored_key = str(cfg.get("api_keys", {}).get(provider_key, "") or "")
        existing_key = os.environ.get(env_var, "") if env_var else ""
        if env_var and not existing_key and stored_key:
            os.environ[env_var] = stored_key
            existing_key = stored_key

        if provider_info.get("needs_key") and not existing_key:
            if await self._maybe_authenticate_provider(provider_key, provider_info) is False:
                return
            existing_key = os.environ.get(env_var, "") if env_var else ""

        ollama_url = None
        if provider_key == "ollama":
            ollama_url = cfg.get("ollama_url", cfg.get("url", provider_info.get("default_url", "http://localhost:11434")))

        models = self._fetch_provider_models(provider_key, provider_info, ollama_url) or list(provider_info.get("models", []))
        if current_model and current_model not in models:
            models.insert(0, current_model)
        model_labels = [f"* {m}" if provider_key == current_provider and m == current_model else m for m in models]
        model_choice = await self.push_screen_wait(SelectionScreen("Select model", model_labels or [current_model]))
        if model_choice is None:
            return
        model_value = model_choice[2:] if model_choice.startswith("* ") else model_choice

        if env_var and existing_key:
            api_keys = cfg.get("api_keys", {}) or {}
            api_keys[provider_key] = existing_key
            cfg["api_keys"] = api_keys
            self._save_config(cfg)

        self._apply_model_config(provider_key, model_value, ollama_url)
        self.query_one("#timeline", MessageTimeline).add_system_message(
            f"Provider: {provider_key}\nModel: {model_value}", title="model"
        )

    async def _maybe_authenticate_provider(self, provider_key: str, provider_info: dict[str, Any]) -> Optional[bool]:
        env_var = provider_info.get("env_var", "")
        auth_options = ["API Key"]
        if provider_key == "openai":
            auth_options.append("OpenAI OAuth (ChatGPT Plus/Pro)")
        auth_options.append("Skip")
        choice = await self.push_screen_wait(SelectionScreen("Authentication method", auth_options))
        if choice is None or choice == "Skip":
            return True
        tl = self.query_one("#timeline", MessageTimeline)
        if choice == "API Key":
            tl.add_system_message(f"Set {env_var} in your environment, then rerun /model.", title="auth")
            return True
        if choice.startswith("OpenAI OAuth"):
            try:
                flow    = OAuthFlow("openai", provider=OpenAIOAuth(), callback_port=1455)
                ok, msg = flow.run(open_browser=True)
                if ok:
                    tokens = TokenManager().get_tokens("openai")
                    if tokens and tokens.get("access_token"):
                        os.environ[env_var] = tokens["access_token"]
                    tl.add_system_message(msg, title="auth")
                    return True
                tl.add_error(msg)
                return False
            except Exception as exc:
                tl.add_error(str(exc))
                return False
        return True

    def _fetch_provider_models(self, provider_key: str, provider_info: dict[str, Any], ollama_url: Optional[str]) -> list[str]:
        try:
            if provider_key == "ollama":
                url = ollama_url or provider_info.get("default_url", "http://localhost:11434")
                req = urllib.request.Request(f"{url}/api/tags")
                with urllib.request.urlopen(req, timeout=5) as resp:
                    return [m["name"] for m in json.loads(resp.read()).get("models", [])]
            if provider_key == "openai":
                api_key = os.environ.get("OPENAI_API_KEY", "")
                if api_key and not api_key.startswith("sk-"):
                    import re
                    all_models = [
                        "gpt-5.5","gpt-5.4","gpt-5.4-mini","gpt-5.3-codex",
                        "gpt-5.3-codex-spark","gpt-5.2","gpt-5","gpt-4o",
                        "gpt-4o-mini","gpt-4-turbo","gpt-4","gpt-3.5-turbo",
                    ]
                    allowed = {"gpt-5.5","gpt-5.2","gpt-5.3-codex","gpt-5.3-codex-spark","gpt-5.4","gpt-5.4-mini"}
                    def _ok(m: str) -> bool:
                        if m in allowed:
                            return True
                        match = re.match(r"^gpt-(\d+\.\d+)", m)
                        return bool(match and float(match.group(1)) > 5.4)
                    return [m for m in all_models if _ok(m)]
        except Exception:
            pass
        return list(provider_info.get("models", []))

    def _apply_model_config(self, provider: str, model: str, ollama_url: Optional[str]) -> None:
        cfg = self._load_config()
        cfg.update({"provider": provider, "model": model})
        if provider == "ollama" and ollama_url:
            cfg["ollama_url"] = ollama_url
            cfg["url"]        = ollama_url
        self._save_config(cfg)
        self.ai.config.default_provider = provider
        self.ai.config.default_model    = model
        if provider == "ollama" and ollama_url:
            self.ai.config.ollama_url = ollama_url
            os.environ["OLLAMA_URL"]  = ollama_url
        self.ai.refresh_provider()
        self.model = model
        if self.vm:
            self.vm.model    = model
            self.vm.provider = provider
        self._set_status("ready", self.last_tokens)

    def _show_model_info(self, args: list[str]) -> None:
        tl  = self.query_one("#timeline", MessageTimeline)
        cfg = self._load_config()
        if not args:
            tl.add_system_message(
                f"Provider: {cfg.get('provider', self.ai.config.default_provider)}\n"
                f"Model: {cfg.get('model', self.ai.config.default_model)}",
                title="model",
            )
            return
        provider = args[0].lower()
        if provider not in PROVIDERS:
            tl.add_error(f"Unknown provider: {provider}")
            return
        model = args[1] if len(args) > 1 else self.ai.config.default_model
        self._apply_model_config(provider, model, args[2] if provider == "ollama" and len(args) > 2 else None)
        tl.add_system_message(f"Provider: {provider}\nModel: {model}", title="model")

    # ── tool helpers ──────────────────────────────────────────────────────

    def _render_tool_output(self, title: str, result: Any) -> None:
        tl = self.query_one("#timeline", MessageTimeline)
        if result.success:
            tl.add_system_message(str(result.output), title=title)
        else:
            tl.add_error(str(result.error or result.output))

    def _list_files(self, args: list[str]) -> None:
        self._render_tool_output(f"files: {args[0] if args else '.'}", self.ai.tools.list_files(args[0] if args else "."))

    def _read_file(self, args: list[str]) -> None:
        if not args:
            self.query_one("#timeline", MessageTimeline).add_error("Usage: /read <file>")
            return
        self._render_tool_output(args[0], self.ai.tools.read_file(args[0]))

    def _exec_command_handler(self, args: list[str]) -> None:
        if not args:
            self.query_one("#timeline", MessageTimeline).add_error("Usage: /exec <command>")
            return
        cmd = " ".join(args)
        self._render_tool_output(f"$ {cmd}", self.ai.tools.execute_command(cmd))

    def _search_web(self, args: list[str]) -> None:
        if not args:
            self.query_one("#timeline", MessageTimeline).add_error("Usage: /search <query>")
            return
        self._render_tool_output(f"search: {' '.join(args)}", self.ai.tools.web_search(" ".join(args)))

    def _fetch_page(self, args: list[str]) -> None:
        if not args:
            self.query_one("#timeline", MessageTimeline).add_error("Usage: /fetch <url>")
            return
        self._render_tool_output(args[0], self.ai.tools.web_fetch(args[0]))

    def _run_tests(self, args: list[str]) -> None:
        cmd = " ".join(args) if args else "pytest -q"
        self._render_tool_output(f"test: {cmd}", self.ai.tools.execute_command(cmd))

    def _commit_changes(self, args: list[str]) -> None:
        if not args:
            self.query_one("#timeline", MessageTimeline).add_error("Usage: /commit <message>")
            return
        msg = " ".join(args)
        self.ai.tools.execute_command("git add -A")
        self._render_tool_output(f"commit: {msg}", self.ai.tools.execute_command(f"git commit -m {shlex.quote(msg)}"))
        if self.vm:
            self.vm.refresh_all_artifacts()
        self._refresh_artifacts()

    def _set_reasoning(self, args: list[str]) -> None:
        tl = self.query_one("#timeline", MessageTimeline)
        if not args:
            tl.add_system_message(f"Current: {self.ai.config.reasoning_level}", title="reasoning")
            return
        level = args[0].lower()
        if level not in ("none", "low", "medium", "high"):
            tl.add_error("Use: none low medium high")
            return
        self.ai.config.reasoning_level = level
        cfg = self._load_config()
        cfg["reasoning_level"] = level
        self._save_config(cfg)
        tl.add_system_message(f"Reasoning level: {level}", title="reasoning")

    def _handle_todo(self, args: list[str]) -> None:
        tl      = self.query_one("#timeline", MessageTimeline)
        manager = TodoManager()
        if not args:
            todos = manager.list(self.session_name)
            tl.add_system_message("\n".join(format_todo_item(t) for t in todos) or "No todos", title="todo")
            return
        action = args[0].lower()
        if action == "add" and len(args) >= 2:
            manager.add(" ".join(args[1:]), self.session_name)
            tl.add_system_message("Todo added", title="todo")
        elif action == "done" and len(args) >= 2:
            manager.complete(args[1])
            tl.add_system_message("Todo done", title="todo")
        elif action == "remove" and len(args) >= 2:
            manager.remove(args[1])
            tl.add_system_message("Todo removed", title="todo")
        else:
            tl.add_error("Usage: /todo [add|done|remove] <...>")

    def _handle_customize(self, args: list[str]) -> None:
        tl = self.query_one("#timeline", MessageTimeline)
        if not args:
            tl.add_system_message(
                f"Agent name: {self._agent_name}\nPersona: {self._load_config().get('system_prompt', '')}",
                title="customize",
            )
            return
        name = args[0]
        persona = " ".join(args[1:]).strip()
        cfg = self._load_config()
        cfg["agent_name"] = name
        if persona:
            cfg["system_prompt"] = persona
        self._save_config(cfg)
        self._agent_name = name
        tl.add_system_message(f"Agent name: {name}" + (f"\nPersona: {persona}" if persona else ""), title="customize")

    def _set_maxsteps(self, args: list[str]) -> None:
        tl = self.query_one("#timeline", MessageTimeline)
        if not args:
            tl.add_system_message(f"Max steps: {self.current_max_steps}", title="maxsteps")
            return
        try:
            n = int(args[0])
        except ValueError:
            tl.add_error("Usage: /maxsteps <number>")
            return
        if n < 1:
            tl.add_error("Must be >= 1")
            return
        if self.agent:
            self.agent.max_steps = n
            self.agent.safety.config.max_steps = n
        self.current_max_steps = n
        if self.vm:
            self.vm.max_steps = n
        os.environ["CODRNINJA_MAX_STEPS"] = str(n)
        tl.add_system_message(f"Max steps: {n}", title="maxsteps")
        self._set_status(self.current_status)

    def _handle_permissions(self, args: list[str]) -> None:
        tl = self.query_one("#timeline", MessageTimeline)
        if not self.agent:
            self.agent = Agent(self.ai, self.session_name)
        if not args:
            tl.add_system_message(f"Mode: {self.agent.permissions.mode}", title="permissions")
            return
        action = args[0].lower()
        if action == "mode" and len(args) >= 2:
            self.agent.permissions.set_mode(args[1].lower())
            self.agent.permissions.save_config()
            cfg = self._load_config()
            cfg["permissions_mode"] = args[1].lower()
            self._save_config(cfg)
            tl.add_system_message(f"Permission mode: {args[1].lower()}", title="permissions")
        elif action == "add" and len(args) >= 4:
            self.agent.permissions.add_rule(PermissionRule(args[1], args[3], args[2]))
            tl.add_system_message("Rule added", title="permissions")
        elif action == "remove" and len(args) >= 2:
            self.agent.permissions.remove_rule(args[1])
            tl.add_system_message("Rule removed", title="permissions")
        else:
            tl.add_error("Usage: /permissions [mode|add|remove] <...>")

    def _list_subagents(self) -> None:
        tl = self.query_one("#timeline", MessageTimeline)
        if not self.agent or not self.agent.subagent_manager:
            tl.add_system_message("No subagents", title="subagents")
            return
        subs = self.agent.subagent_manager.list()
        tl.add_system_message("\n".join(f"- {s['name']} [{s['status']}]" for s in subs) or "No active subagents", title="subagents")

    def _handle_mcp_command(self, args: list[str]) -> None:
        tl     = self.query_one("#timeline", MessageTimeline)
        action = args[0].lower() if args else "list"
        if action == "list":
            self.console_tools.refresh_mcp_tools(force=True)
            servers = self.mcp.list_servers()
            if not servers:
                tl.add_system_message("No MCP servers configured.", title="mcp")
                return
            tl.add_system_message(
                "\n".join(f"- {s.name} [{s.type}] {'enabled' if s.enabled else 'disabled'} ({len(s.tools)} tools)" for s in servers),
                title="mcp",
            )
        elif action in {"enable", "disable"} and len(args) >= 2:
            ok = self.mcp.enable(args[1]) if action == "enable" else self.mcp.disable(args[1])
            if ok:
                self.console_tools.refresh_mcp_tools(force=True)
                tl.add_system_message(f"MCP server {action}d: {args[1]}", title="mcp")
            else:
                tl.add_error(f"Unknown MCP server: {args[1]}")
        elif action == "add" and len(args) >= 2:
            try:
                cfg = json.loads(" ".join(args[1:]))
                self.mcp.add_server(cfg)
                self.console_tools.refresh_mcp_tools(force=True)
                tl.add_system_message(f"Added: {cfg['name']}", title="mcp")
            except Exception as exc:
                tl.add_error(f"Failed: {exc}")
        else:
            tl.add_error("Usage: /mcp [list|add|enable|disable]")

    def _show_skills(self) -> None:
        tl = self.query_one("#timeline", MessageTimeline)
        self.skill_registry.discover()
        skills = self.skill_registry.list_skills()
        tl.add_system_message(
            "\n".join(f"- {s['name']}: {s['description']}" for s in skills) or "No skills installed.",
            title="skills",
        )

    def _load_config(self) -> dict[str, Any]:
        if not os.path.exists(CONFIG_FILE):
            return {}
        with open(CONFIG_FILE) as f:
            return json.load(f)

    def _save_config(self, config: dict[str, Any]) -> None:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)


# ── entrypoint ─────────────────────────────────────────────────────────────────

def main_tui() -> None:
    session_name = os.environ.get("CODRNINJA_SESSION")
    ai = AICode()
    CodrninjaTUI(ai=ai, session_name=session_name).run()


if __name__ == "__main__":
    main_tui()