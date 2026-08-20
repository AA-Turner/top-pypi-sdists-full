"""Interactive scope policy configuration modal.

Three-view modal for configuring guard policy scope:
  1. Preset picker — select a baseline (recon_only, standard_pentest, red_team, blank)
  2. Capability editor — expand categories, toggle ALLOW/DENY/ASK per subcategory
  3. Rubric preview — see the rendered rubric the judge LLM will receive

Returns a scope config dict on confirm, ``None`` on cancel.
"""

import typing as t
from dataclasses import dataclass

from rich.text import Text
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Static

from dreadnode.app.tui.theme import ERROR, FG, FG_FAINTEST, FG_MUTED, FG_SUBTLE, SUCCESS, WARNING
from dreadnode.policies.scope import (
    PRESETS,
    Policy,
    ScopeCapabilities,
    ScopeConfig,
)

if t.TYPE_CHECKING:
    from textual.app import ComposeResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_POLICY_COLORS: dict[Policy, str] = {
    Policy.ALLOW: SUCCESS,
    Policy.DENY: ERROR,
    Policy.ASK: WARNING,
}

_POLICY_CYCLE: list[Policy] = [Policy.ALLOW, Policy.DENY, Policy.ASK]

_PRESET_DESCRIPTIONS: list[tuple[str, str]] = [
    ("recon_only", "Reconnaissance only, all else denied"),
    ("standard_pentest", "Standard assessment, no persistence/impact"),
    ("red_team", "Full offensive, only impact denied"),
    ("blank", "Start with all capabilities denied"),
]


@dataclass(slots=True)
class _Row:
    kind: t.Literal["category", "subcategory"]
    category: str
    subcategory: str | None = None


def _next_policy(current: Policy) -> Policy:
    idx = _POLICY_CYCLE.index(current)
    return _POLICY_CYCLE[(idx + 1) % len(_POLICY_CYCLE)]


def _display_name(name: str) -> str:
    return name.replace("_", " ")


_View = t.Literal["preset", "editor", "preview"]

# ---------------------------------------------------------------------------
# Modal
# ---------------------------------------------------------------------------


class ScopePolicyModal(ModalScreen[dict[str, t.Any] | None]):
    """Interactive scope policy configuration modal."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("escape", "back", "Back/Cancel", show=False),
        Binding("enter", "select", "Select/Confirm", show=False),
        Binding("up", "cursor_up", "Up", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("down", "cursor_down", "Down", show=False),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("space", "cycle", "Cycle policy", show=False),
        Binding("tab", "next_view", "Next view", show=False),
        Binding("a", "set_allow", "Set ALLOW", show=False),
        Binding("d", "set_deny", "Set DENY", show=False),
        Binding("s", "set_ask", "Set ASK", show=False),
        Binding("p", "pick_preset", "Back to presets", show=False),
        Binding("c", "confirm", "Confirm", show=False),
    ]

    def __init__(
        self,
        capabilities: ScopeCapabilities | None = None,
        preset: str | None = None,
    ) -> None:
        super().__init__()
        has_existing = capabilities is not None
        self._view: _View = "editor" if has_existing else "preset"
        self._preset_cursor: int = 0
        self._editor_cursor: int = 0
        self._expanded: set[str] = set()
        self._capabilities: ScopeCapabilities = (
            capabilities.model_copy(deep=True) if capabilities else ScopeCapabilities()
        )
        self._selected_preset: str | None = preset

    # -- Compose ---------------------------------------------------------------

    def compose(self) -> "ComposeResult":
        with Vertical(id="scope-box"):
            yield Static(id="scope-header")
            with Vertical(id="scope-preset-view"):
                yield Static(id="scope-preset-list")
            with VerticalScroll(id="scope-editor-view", classes="-hidden"):
                yield Static(id="scope-capability-list")
            with VerticalScroll(id="scope-preview-view", classes="-hidden"):
                yield Static(id="scope-rubric-content")
            yield Static(id="scope-hint-bar")

    def on_mount(self) -> None:
        self._show_view(self._view)

    # -- View switching --------------------------------------------------------

    def _show_view(self, view: _View) -> None:
        self._view = view
        for name in ("preset", "editor", "preview"):
            container_id = f"scope-{name}-view"
            container = self.query_one(f"#{container_id}")
            if name == view:
                container.remove_class("-hidden")
            else:
                container.add_class("-hidden")
        self._render_current_view()

    def _render_current_view(self) -> None:
        if self._view == "preset":
            self._render_preset()
        elif self._view == "editor":
            self._render_editor()
        else:
            self._render_preview()
        self._render_header()
        self._render_hints()

    # -- Preset view -----------------------------------------------------------

    def _render_preset(self) -> None:
        text = Text()
        for i, (name, desc) in enumerate(_PRESET_DESCRIPTIONS):
            is_selected = i == self._preset_cursor
            if is_selected:
                text.append("  \u276f ", style=f"bold {FG}")
            else:
                text.append("    ", style=FG_FAINTEST)
            text.append(f"{name:<20}", style=f"bold {FG}" if is_selected else FG_MUTED)
            text.append(f" {desc}", style=FG_SUBTLE if is_selected else FG_FAINTEST)
            if i < len(_PRESET_DESCRIPTIONS) - 1:
                text.append("\n")
        self.query_one("#scope-preset-list", Static).update(text)

    def _select_preset(self) -> None:
        name = _PRESET_DESCRIPTIONS[self._preset_cursor][0]
        if name == "blank":
            self._capabilities = ScopeCapabilities()
            self._selected_preset = None
        else:
            preset = PRESETS[name]
            self._capabilities = preset.capabilities.model_copy(deep=True)
            self._selected_preset = name
        self._expanded.clear()
        self._editor_cursor = 0
        self._show_view("editor")

    # -- Editor view -----------------------------------------------------------

    def _build_rows(self) -> list[_Row]:
        rows: list[_Row] = []
        for cat_name in self._capabilities.category_names():
            rows.append(_Row("category", cat_name))
            if cat_name in self._expanded:
                cat = self._capabilities.get_category(cat_name)
                for sub_name in cat.subcategory_names():
                    rows.append(_Row("subcategory", cat_name, sub_name))
        return rows

    def _render_editor(self) -> None:
        rows = self._build_rows()
        if self._editor_cursor >= len(rows):
            self._editor_cursor = max(0, len(rows) - 1)

        text = Text()
        for i, row in enumerate(rows):
            is_selected = i == self._editor_cursor
            cat = self._capabilities.get_category(row.category)

            if row.kind == "category":
                glyph = "▾" if row.category in self._expanded else "▸"
                effective = cat.policy or Policy.DENY
                cursor = "\u276f" if is_selected else " "

                text.append(f" {cursor} {glyph} ", style=f"bold {FG}" if is_selected else FG_MUTED)
                text.append(
                    f"{_display_name(row.category):<24}",
                    style=f"bold {FG}" if is_selected else FG_SUBTLE,
                )
                text.append(
                    f" {effective.value.upper()}",
                    style=_POLICY_COLORS[effective],
                )
            else:
                assert row.subcategory is not None
                explicit = getattr(cat, row.subcategory, None)
                effective = cat.resolve(row.subcategory)
                is_override = isinstance(explicit, Policy) and explicit != cat.policy
                cursor = "\u276f" if is_selected else " "

                text.append(f" {cursor}     ", style=FG_FAINTEST)
                text.append(
                    f"{_display_name(row.subcategory):<22}",
                    style=FG_SUBTLE if is_selected else FG_FAINTEST,
                )
                color = _POLICY_COLORS[effective]
                policy_style = color if is_override else f"{color} dim"
                text.append(f" {effective.value.upper()}", style=policy_style)

            if i < len(rows) - 1:
                text.append("\n")

        self.query_one("#scope-capability-list", Static).update(text)

        # Scroll cursor into view
        scroll = self.query_one("#scope-editor-view", VerticalScroll)
        scroll.scroll_to(y=max(0, self._editor_cursor - 6), animate=False)

    def _cycle_at_cursor(self, target: Policy | None = None) -> None:
        if self._view != "editor":
            return
        rows = self._build_rows()
        if not rows or self._editor_cursor >= len(rows):
            return

        row = rows[self._editor_cursor]
        cat = self._capabilities.get_category(row.category)

        if row.kind == "category":
            current = cat.policy or Policy.DENY
            new_val = target if target is not None else _next_policy(current)
            cat.policy = new_val
            # Clear subcategory overrides so blanket cascades cleanly
            for sub in cat.subcategory_names():
                setattr(cat, sub, None)
        else:
            assert row.subcategory is not None
            current = cat.resolve(row.subcategory)
            new_val = target if target is not None else _next_policy(current)
            # If new value matches blanket, set to None (inherit)
            if new_val == cat.policy:
                setattr(cat, row.subcategory, None)
            else:
                setattr(cat, row.subcategory, new_val)

        self._render_editor()

    def _toggle_expand(self) -> None:
        rows = self._build_rows()
        if not rows or self._editor_cursor >= len(rows):
            return
        row = rows[self._editor_cursor]
        if row.kind != "category":
            return
        if row.category in self._expanded:
            self._expanded.discard(row.category)
        else:
            self._expanded.add(row.category)
        self._render_editor()

    # -- Preview view ----------------------------------------------------------

    def _render_preview(self) -> None:
        config = ScopeConfig(
            preset=self._selected_preset,
            capabilities=self._capabilities,
        )
        resolved = config.resolve()
        rubric = resolved.render_rubric()
        self.query_one("#scope-rubric-content", Static).update(Text(rubric, style=FG_SUBTLE))

    # -- Header & hints --------------------------------------------------------

    def _render_header(self) -> None:
        text = Text()
        text.append(" Scope Policy", style=f"bold {FG}")
        if self._view == "preset":
            text.append("\n Select a preset to start", style=FG_FAINTEST)
        elif self._view == "editor":
            if self._selected_preset:
                text.append(f"  ({self._selected_preset})", style=FG_MUTED)
            text.append("\n Tab to preview the rendered judge prompt", style=FG_FAINTEST)
        elif self._view == "preview":
            text.append("  — Rubric Preview", style=FG_MUTED)
        self.query_one("#scope-header", Static).update(text)

    def _render_hints(self) -> None:
        text = Text(justify="right")
        hints: list[tuple[str, str]]
        if self._view == "preset":
            hints = [("Enter", "select"), ("Esc", "cancel")]
        elif self._view == "editor":
            hints = [
                ("↑↓", "navigate"),
                ("a/d/s", "allow/deny/ask"),
                ("Space", "cycle"),
                ("Enter", "expand/collapse"),
                ("c", "confirm & apply"),
                ("Tab", "preview"),
                ("Esc", "back"),
            ]
        else:
            hints = [("Enter", "confirm"), ("Tab", "back"), ("Esc", "back")]

        for i, (key, action) in enumerate(hints):
            if i > 0:
                text.append("  ", style=FG_FAINTEST)
            text.append(key, style=f"bold {FG_MUTED}")
            text.append(f" {action}", style=FG_FAINTEST)
        self.query_one("#scope-hint-bar", Static).update(text)

    # -- Actions ---------------------------------------------------------------

    def action_back(self) -> None:
        if self._view == "preset":
            self.dismiss(None)
        elif self._view == "editor":
            self._show_view("preset")
        else:
            self._show_view("editor")

    def action_select(self) -> None:
        if self._view == "preset":
            self._select_preset()
        elif self._view == "editor":
            self._toggle_expand()
        else:
            # Preview — confirm
            self._confirm()

    def action_cursor_up(self) -> None:
        if self._view == "preset":
            self._preset_cursor = max(0, self._preset_cursor - 1)
            self._render_preset()
        elif self._view == "editor":
            self._editor_cursor = max(0, self._editor_cursor - 1)
            self._render_editor()

    def action_cursor_down(self) -> None:
        if self._view == "preset":
            self._preset_cursor = min(len(_PRESET_DESCRIPTIONS) - 1, self._preset_cursor + 1)
            self._render_preset()
        elif self._view == "editor":
            rows = self._build_rows()
            self._editor_cursor = min(len(rows) - 1, self._editor_cursor + 1)
            self._render_editor()

    def action_cycle(self) -> None:
        self._cycle_at_cursor()

    def action_next_view(self) -> None:
        if self._view == "editor":
            self._show_view("preview")
        elif self._view == "preview":
            self._show_view("editor")

    def action_set_allow(self) -> None:
        self._cycle_at_cursor(target=Policy.ALLOW)

    def action_set_deny(self) -> None:
        self._cycle_at_cursor(target=Policy.DENY)

    def action_set_ask(self) -> None:
        self._cycle_at_cursor(target=Policy.ASK)

    def action_pick_preset(self) -> None:
        if self._view == "editor":
            self._show_view("preset")

    def action_confirm(self) -> None:
        if self._view in ("editor", "preview"):
            self._confirm()

    # -- Confirm ---------------------------------------------------------------

    def _confirm(self) -> None:
        result: dict[str, t.Any] = {
            "preset": self._selected_preset,
            "capabilities": self._capabilities.model_dump(exclude_none=True),
        }
        self.dismiss(result)
