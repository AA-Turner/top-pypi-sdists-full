"""Session context bar (Zone 1) and page status (Zone 3).

SessionContextBar (Zone 1, 2 lines):
  Line 1: @agent_name · active                        Opus 4.6 (High)
  Line 2: ^A agent                                ^K model, ^⇧K reasoning

PageStatus (Zone 3, 1 line):
                         ctx 53.4k/200k tok · ⚒ 12 · usage $0.34 · subagents $0.12 · ? help

The token gauge shows ``last_input_tokens / model_max_tokens`` — i.e., the
size of the prompt the model just saw against the model's context window.
This is *not* a cumulative session usage figure; cumulative would routinely
exceed the model's max in any multi-turn session and rendering the fraction
would be meaningless (the platform splits the same way via
``last_generation_input_tokens``).

The ``⚒`` and ``$X.XX`` segments only render when their values are known
and non-zero; on a session with at least one generation that lacked a cost
rate the dollar segment is suppressed entirely (matching the backend's
null-propagation for ``total_cost_usd``) — partial sums are misleading.

The ``ctx`` prefix labels the token gauge as a context-window meter (not a
quota); the ``usage`` prefix labels the dollar figure as cumulative cost
for this session only (not balance, not account-wide spend). The dollar
segment also carries an OSC 8 hyperlink to the public pricing docs so a
confused user can resolve the unit mismatch with one click in any modern
terminal — terminals without OSC 8 support simply render plain text.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.text import Text
from textual.reactive import reactive
from textual.widgets import Static

if TYPE_CHECKING:
    from textual.timer import Timer

from dreadnode.app.model_catalog import display_name_with_effort
from dreadnode.app.tui.model_variants import render_tokens
from dreadnode.app.tui.theme import ACCENT, FG_FAINTEST, FG_MUTED, FG_SUBTLE, INFO, WARNING
from dreadnode.app.tui.widgets.status_bar import StatusBar, _pad_right


class SessionContextBar(Static):
    """Zone 1 — two-line bar showing agent + model context above the composer."""

    agent_name: reactive[str] = reactive("default")
    session_label: reactive[str] = reactive("none")
    model_name: reactive[str] = reactive("")
    effort_label: reactive[str] = reactive("")
    busy: reactive[bool] = reactive(False)
    status_text: reactive[str] = reactive("Ready")
    background_status: reactive[str] = reactive("")

    def render(self) -> Text:
        w = self.size.width

        # === Line 1: @agent (+ status)          Model (Effort) ===
        left = Text(no_wrap=True, overflow="ellipsis")
        left.append(f"@{self.agent_name or 'default'}", style=FG_SUBTLE)
        if self.session_label and self.session_label != "none":
            left.append(" · ", style=FG_FAINTEST)
            left.append(self.session_label, style=FG_MUTED)

        if self.busy:
            left.append(" · ", style=FG_FAINTEST)
            status = (self.status_text or "").strip().lower()
            if status.startswith("awaiting"):
                left.append(status, style=WARNING)
            else:
                left.append("active", style=ACCENT)
        elif self.background_status:
            left.append(" · ", style=FG_FAINTEST)
            left.append(self.background_status, style=WARNING)

        right = Text(no_wrap=True)
        if self.model_name:
            effort = self.effort_label or None
            right.append(display_name_with_effort(self.model_name, effort), style="bold")
            if self.model_name.startswith("dn/"):
                right.append(" · ", style=FG_FAINTEST)
                right.append("dreadnode", style=FG_FAINTEST)

        line1 = _pad_right(left, right, w)

        # === Line 2: keybind hints ===
        hints_left = Text(no_wrap=True)
        hints_left.append("^A", style=FG_FAINTEST)
        hints_left.append(" agent  ", style=FG_FAINTEST)
        hints_left.append("^O", style=FG_FAINTEST)
        hints_left.append(" output", style=FG_FAINTEST)

        hints_right = Text(no_wrap=True)
        hints_right.append("^K", style=FG_FAINTEST)
        hints_right.append(" model, ", style=FG_FAINTEST)
        hints_right.append("^⇧K", style=FG_FAINTEST)
        hints_right.append(" reasoning", style=FG_FAINTEST)

        line2 = _pad_right(hints_left, hints_right, w)

        result = line1.copy()
        result.append("\n")
        result.append_text(line2)
        return result


class ContextBar(SessionContextBar):
    """Public context bar with the broader legacy surface older code expects."""

    connection: reactive[str] = reactive("")
    workspace_label: reactive[str] = reactive("")
    last_input_tokens: reactive[int] = reactive(0)
    model_max_tokens: reactive[int] = reactive(0)
    output_mode: reactive[str] = reactive("compact")

    def render(self) -> Text:
        w = self.size.width

        left = Text(no_wrap=True, overflow="ellipsis")
        left.append(f"@{self.agent_name or 'default'}", style=FG_SUBTLE)
        if self.session_label and self.session_label != "none":
            left.append(" · ", style=FG_FAINTEST)
            left.append(self.session_label, style=FG_MUTED)

        if self.busy:
            left.append(" · ", style=FG_FAINTEST)
            status = (self.status_text or "").strip().lower()
            if status.startswith("awaiting"):
                left.append(status, style=WARNING)
            else:
                left.append("active", style=ACCENT)
        elif self.background_status:
            left.append(" · ", style=FG_FAINTEST)
            left.append(self.background_status, style=WARNING)

        if self.workspace_label:
            left.append(" · ", style=FG_FAINTEST)
            left.append(self.workspace_label, style=FG_MUTED)

        right = Text(no_wrap=True)
        if self.model_name:
            effort = self.effort_label or None
            right.append(display_name_with_effort(self.model_name, effort), style="bold")
            if self.model_name.startswith("dn/"):
                right.append(" · ", style=FG_FAINTEST)
                right.append("dreadnode", style=FG_FAINTEST)

        connection = (self.connection or "").strip()
        if connection:
            if right.plain:
                right.append(" · ", style=FG_FAINTEST)
            right.append(
                "platform" if connection.startswith("http") else connection, style=FG_MUTED
            )

        if self.last_input_tokens > 0:
            if right.plain:
                right.append(" · ", style=FG_FAINTEST)
            limit = self.model_max_tokens if self.model_max_tokens > 0 else None
            right.append_text(render_tokens(self.last_input_tokens, limit))

        line1 = _pad_right(left, right, w)

        hints_left = Text(no_wrap=True)
        hints_left.append("^A", style=FG_FAINTEST)
        hints_left.append(" agent  ", style=FG_FAINTEST)
        hints_left.append("^O", style=FG_FAINTEST)
        hints_left.append(
            " show more" if self.output_mode == "compact" else " show less", style=FG_FAINTEST
        )

        hints_right = Text(no_wrap=True)
        hints_right.append("^K", style=FG_FAINTEST)
        hints_right.append(" model, ", style=FG_FAINTEST)
        hints_right.append("^⇧K", style=FG_FAINTEST)
        hints_right.append(" reasoning", style=FG_FAINTEST)

        line2 = _pad_right(hints_left, hints_right, w)

        result = line1.copy()
        result.append("\n")
        result.append_text(line2)
        return result


_ISSUE_DISPLAY_SECONDS = 60

# Public docs page that explains credits, the USD-to-credits rate, what
# consumes credits, and how the usage-cost figure relates to the org
# balance. Hard-coded by design: the TUI ships independently of docs and a
# config lookup would just add a network hop for a value that almost never
# changes. If this URL moves, the previous one should redirect.
PRICING_DOCS_URL = "https://docs.dreadnode.io/platform/credits/"


class PageStatus(Static):
    """Zone 3 — single-line page status below the composer.

    runtime_issues is a tuple of (label, names, hint, kind) groups, e.g.:
        (("MCP", "burp, caido", "/mcp", "error"), ("updates", "web-security", "Ctrl+P", "update"))

    Issues auto-dismiss after 60 seconds.
    """

    last_input_tokens: reactive[int] = reactive(0)
    model_max_tokens: reactive[int] = reactive(0)
    tool_call_count: reactive[int] = reactive(0)
    cost_usd: reactive[float] = reactive(0.0)
    cost_unknown: reactive[bool] = reactive(False)
    subagent_cost_usd: reactive[float] = reactive(0.0)
    runtime_issues: reactive[tuple[tuple[str, str, str, str], ...]] = reactive(())
    _show_issues: reactive[bool] = reactive(False)
    _dismiss_timer: Timer | None = None

    def watch_runtime_issues(self, value: tuple[tuple[str, str, str, str], ...]) -> None:
        if self._dismiss_timer is not None:
            self._dismiss_timer.stop()
            self._dismiss_timer = None
        if value:
            self._show_issues = True
            self._dismiss_timer = self.set_timer(_ISSUE_DISPLAY_SECONDS, self._hide_issues)
        else:
            self._show_issues = False

    def _hide_issues(self) -> None:
        self._show_issues = False

    def render(self) -> Text:
        w = self.size.width

        left = Text(no_wrap=True)
        if self._show_issues:
            for i, (_label, names, hint, kind) in enumerate(self.runtime_issues):
                if i > 0:
                    left.append(" · ", style=FG_FAINTEST)
                if kind == "update":
                    left.append("↑ ", style=INFO)
                    left.append(names, style=INFO)
                else:
                    left.append("⚠ ", style=WARNING)
                    left.append(names, style=WARNING)
                left.append(f" ({hint})", style=FG_FAINTEST)

        right = Text(no_wrap=True)
        if self.last_input_tokens > 0:
            limit = self.model_max_tokens if self.model_max_tokens > 0 else None
            right.append("ctx ", style=FG_FAINTEST)
            right.append_text(render_tokens(self.last_input_tokens, limit))
            right.append(" · ", style=FG_FAINTEST)
        if self.tool_call_count > 0:
            right.append("⚒ ", style=FG_MUTED)
            right.append(str(self.tool_call_count), style=FG_MUTED)
            right.append(" · ", style=FG_FAINTEST)
        if not self.cost_unknown and self.cost_usd > 0:
            right.append("usage ", style=FG_FAINTEST)
            right.append(
                _format_cost_usd(self.cost_usd),
                style=f"{FG_MUTED} link {PRICING_DOCS_URL}",
            )
            right.append(" · ", style=FG_FAINTEST)
        if self.subagent_cost_usd > 0:
            right.append("subagents ", style=FG_FAINTEST)
            right.append(
                _format_cost_usd(self.subagent_cost_usd),
                style=FG_MUTED,
            )
            right.append(" · ", style=FG_FAINTEST)
        right.append("? help", style=FG_FAINTEST)

        return _pad_right(left, right, w)


def _format_cost_usd(usd: float) -> str:
    """Format a positive USD cost: ``<$0.01`` floor for sub-cent, ``$X.XX`` otherwise.

    Only called when the caller has confirmed ``usd > 0``; the zero case is
    a renderer-suppression decision (see :class:`PageStatus.render`), not a
    formatting one — keeping the two concerns separate avoids reintroducing
    the partial-sum / unknown-cost ambiguity at the formatter layer.
    """
    if usd < 0.01:
        return "<$0.01"
    return f"${usd:.2f}"


class AppBar(StatusBar):
    """Legacy navigation bar facade for older code and tests."""

    def render(self) -> Text:
        w = self.size.width

        left = Text(no_wrap=True)

        right = Text(no_wrap=True)
        for key, label, last in [
            ("?", "help", False),
            ("^B", "sessions", False),
            ("^T", "traces", False),
            ("^E", "env", False),
            ("F5", "console", True),
        ]:
            right.append(key, style=FG_FAINTEST)
            right.append(f" {label}", style=FG_FAINTEST)
            if not last:
                right.append("  ", style=FG_FAINTEST)

        return _pad_right(left, right, w)
