"""Multi-line composer with Enter to submit and overlay-aware key routing.

Multiline input methods (matching Claude Code / Droid conventions):
  - \\ + Enter  — universal, works in all terminals
  - Shift+Enter — works in terminals that send distinct escape sequence
  - Ctrl+J      — line feed, always works

Overlay navigation (when slash/mention overlay is visible):
  - Up/Down     — navigate overlay items
  - Tab/Enter   — select highlighted item
  - Esc         — dismiss overlay

Shell mode:
  - Text starting with '!' enters shell mode (visual indicator)
"""

from __future__ import annotations

import difflib
import re
import typing as t
from dataclasses import dataclass

from rich.segment import Segment
from rich.style import Style
from textual import on
from textual.binding import Binding
from textual.message import Message
from textual.reactive import reactive
from textual.strip import Strip
from textual.widgets import TextArea

if t.TYPE_CHECKING:
    from textual.events import Key, Paste

    from dreadnode.app.tui.widgets.overlay_mixin import OverlayMixin


@dataclass(slots=True)
class PastedSegment:
    content: str
    line_count: int


_PASTE_RE = re.compile(r"\[pasted ~(\d+) lines?\]")


class ComposerInput(TextArea):
    """Multi-line input with overlay-aware key routing."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("ctrl+a", "app.select_agent", "Agent", show=False),
        Binding("ctrl+k", "app.select_model", "Model", show=False),
        Binding("ctrl+shift+k", "app.cycle_effort", "Effort", show=False),
        Binding("ctrl+b", "app.open_sessions", "Sessions", show=False),
        Binding("ctrl+w", "app.open_workspaces", "Workspaces", show=False),
        Binding("ctrl+o", "app.toggle_output_mode", "Output", show=False),
        Binding("ctrl+p", "app.open_capabilities", "Caps", show=False),
        Binding("ctrl+r", "app.open_runtimes", "Runs", show=False),
        Binding("ctrl+t", "app.open_traces", "Traces", show=False),
        Binding("ctrl+e", "app.open_evaluations", "Evals", show=False),
        Binding("f5", "app.open_console", "Console", show=False),
        Binding("ctrl+n", "app.new_session", "New", show=False),
        Binding("ctrl+q", "app.quit", "Quit", show=False, priority=True),
        # Alt/Option key bindings (Kitty keyboard protocol — Ghostty, WezTerm, Kitty)
        Binding("alt+backspace", "delete_word_left", "Delete word left", show=False),
        Binding("alt+delete", "delete_word_right", "Delete word right", show=False),
        Binding("alt+left", "cursor_word_left", "Word left", show=False),
        Binding("alt+right", "cursor_word_right", "Word right", show=False),
        Binding("alt+shift+left", "cursor_word_left(True)", "Select word left", show=False),
        Binding("alt+shift+right", "cursor_word_right(True)", "Select word right", show=False),
        Binding("alt+enter", "newline", "New line", show=False),
    ]

    class Submitted(Message):
        """Posted when the user presses Enter to submit."""

        def __init__(self, text_area: ComposerInput, value: str) -> None:
            self.value = value
            self.input = text_area
            super().__init__()

    class HelpRequested(Message):
        """Posted when ? is pressed in an empty composer."""

    DEFAULT_CSS = """
    ComposerInput {
        height: auto;
        min-height: 1;
        max-height: 6;
        border: none;
        background: transparent;
        padding: 0;
        width: 1fr;
    }
    """

    shell_mode: reactive[bool] = reactive(False)

    def __init__(self, placeholder: str = "", **kwargs: t.Any) -> None:
        kwargs.setdefault("highlight_cursor_line", False)
        super().__init__(**kwargs)
        self._placeholder = placeholder
        self._pastes: list[PastedSegment] = []
        self._last_display_text = ""

    @property
    def value(self) -> str:
        """Compatibility with Input API."""
        return self.text

    @value.setter
    def value(self, text: str) -> None:
        self.load_text(text)

    def watch_shell_mode(self, shell: bool) -> None:
        """Toggle shell mode visual class."""
        self.set_class(shell, "-shell")

    def action_newline(self) -> None:
        """Insert a newline at the cursor."""
        self.insert("\n")

    def clear_pastes(self) -> None:
        """Clear tracked pasted segments."""
        self._pastes.clear()

    def _document_index(self, location: tuple[int, int]) -> int:
        """Convert a document (row, column) location to a text index."""
        row, column = location
        lines = self.text.split("\n")
        return sum(len(line) + 1 for line in lines[:row]) + column

    def _document_location(self, index: int) -> tuple[int, int]:
        """Convert a text index to a document (row, column) location."""
        prefix = self.text[:index]
        row = prefix.count("\n")
        column = len(prefix.rsplit("\n", 1)[-1])
        return row, column

    async def _on_paste(self, event: Paste) -> None:
        pasted = event.text
        line_count = pasted.count("\n") + 1
        if line_count < 2:
            event.prevent_default()
            event.stop()
            await super()._on_paste(event)
            return

        event.prevent_default()
        event.stop()
        placeholder = f"[pasted ~{line_count} line{'s' if line_count != 1 else ''}]"
        insertion_index = self._document_index(self.cursor_location)
        visual_index = len(_PASTE_RE.findall(self.text[:insertion_index]))
        self._pastes.insert(visual_index, PastedSegment(content=pasted, line_count=line_count))
        self.insert(placeholder)
        self._last_display_text = self.text

    def _resolve_pastes(self, display_text: str) -> str:
        pastes = iter(self._pastes)

        def replacer(match: re.Match[str]) -> str:
            segment = next(pastes, None)
            return segment.content if segment else match.group(0)

        return _PASTE_RE.sub(replacer, display_text)

    def _sync_pastes(self, display_text: str) -> None:
        old_placeholders = [match.group(0) for match in _PASTE_RE.finditer(self._last_display_text)]
        new_placeholders = [match.group(0) for match in _PASTE_RE.finditer(display_text)]
        if len(new_placeholders) < len(old_placeholders) and self._pastes:
            matcher = difflib.SequenceMatcher(a=old_placeholders, b=new_placeholders)
            removed: list[int] = []
            for tag, start, end, _new_start, _new_end in matcher.get_opcodes():
                if tag in {"delete", "replace"}:
                    removed.extend(range(start, end))
            for index in reversed(removed):
                if index < len(self._pastes):
                    del self._pastes[index]
        if len(new_placeholders) < len(self._pastes):
            self._pastes = self._pastes[: len(new_placeholders)]
        elif not new_placeholders:
            self._pastes.clear()
        self._last_display_text = display_text

    def _remove_paste_at_cursor(self, *, forward: bool) -> bool:
        """Delete a tracked paste placeholder as one editing operation."""
        if not self.selection.is_empty:
            return False
        text = self.text
        cursor = self._document_index(self.cursor_location)
        placeholders = list(_PASTE_RE.finditer(text))
        for index, match in enumerate(placeholders):
            at_boundary = cursor == (match.end() if not forward else match.start())
            if not at_boundary or index >= len(self._pastes):
                continue
            start = self._document_location(match.start())
            end = self._document_location(match.end())
            del self._pastes[index]
            self.delete(start, end)
            self._last_display_text = self.text
            return True
        return False

    @on(TextArea.Changed)
    def _on_text_changed(self, event: TextArea.Changed) -> None:
        self._sync_pastes(event.text_area.text)

    def _paste_style(self) -> Style:
        if self.app:
            color = self.app.get_css_variables().get("fg-muted")
            if color:
                return Style(color=color)
        return Style(dim=True)

    async def _on_key(self, event: Key) -> None:
        overlay = self._get_active_overlay()

        # === Overlay-aware key routing ===
        if overlay is not None:
            if event.key in ("up", "down"):
                event.prevent_default()
                event.stop()
                overlay.move_highlight(-1 if event.key == "up" else 1)
                return

            if event.key in ("tab", "enter"):
                event.prevent_default()
                event.stop()
                overlay.select_highlighted()
                return

            if event.key == "escape":
                event.prevent_default()
                event.stop()
                overlay.hide()
                return

            # Forward unhandled keys to the overlay for custom handling
            if overlay.on_key(event):
                return

        if event.key in ("backspace", "delete"):
            forward = event.key == "delete"
            if self._remove_paste_at_cursor(forward=forward):
                self.shell_mode = self.text.startswith("!")
                event.prevent_default()
                event.stop()
                return

        # === Multiline: \\ + Enter ===
        if event.key == "enter":
            raw = self.text
            if raw.endswith("\\"):
                # Replace trailing \ with newline
                event.prevent_default()
                event.stop()
                self.load_text(raw[:-1] + "\n")
                # Move cursor to end
                self.move_cursor_relative(rows=9999, columns=9999)
                return

            # Normal Enter = submit (if text is non-empty)
            resolved = self._resolve_pastes(raw)
            text = resolved.strip()
            event.prevent_default()
            event.stop()
            if text:
                self.post_message(self.Submitted(self, text))
                self.load_text("")
                self.clear_pastes()
            return

        # === Multiline: Shift+Enter, Ctrl+J ===
        if event.key in ("shift+enter", "ctrl+j"):
            event.prevent_default()
            event.stop()
            self.action_newline()
            return

        # === ? toggles help when composer is empty ===
        if event.key == "question_mark" and not self.text:
            event.prevent_default()
            event.stop()
            # Bubble up to app — post a custom message
            self.post_message(self.HelpRequested())
            return

        await super()._on_key(event)

        # Update shell mode based on content
        self.shell_mode = self.text.startswith("!")

    def _render_line(self, y: int) -> Strip:
        strip = super()._render_line(y)
        if strip.cell_length <= 0:
            return strip

        y_offset = y + self.scroll_offset.y
        if y_offset >= self.wrapped_document.height:
            return strip

        try:
            line_info = self.wrapped_document._offset_to_line_info[y_offset]
        except IndexError:
            return strip

        if line_info is None:
            return strip

        line_index, section_offset = line_info
        line_text = self.document.get_line(line_index)
        matches = list(_PASTE_RE.finditer(line_text))
        if not matches:
            return strip

        wrap_offsets = self.wrapped_document.get_offsets(line_index)
        section_start = wrap_offsets[section_offset - 1] if section_offset else 0
        section_end = (
            wrap_offsets[section_offset] if section_offset < len(wrap_offsets) else len(line_text)
        )

        ranges: list[tuple[int, int]] = []
        for match in matches:
            visible_start = max(match.start(), section_start)
            visible_end = min(match.end(), section_end)
            if visible_start < visible_end:
                ranges.append((visible_start - section_start, visible_end - section_start))
        if not ranges:
            return strip

        cuts = sorted(
            {pos for start, end in ranges for pos in (start, end) if 0 < pos < strip.cell_length}
            | {strip.cell_length}
        )
        style = self._paste_style()
        segments = list(strip._segments)
        partitions = list(Segment.divide(segments, cuts))
        boundaries = [0, *cuts]
        styled_segments: list[Segment] = []

        for idx, segment_group in enumerate(partitions):
            start = boundaries[idx]
            end = boundaries[idx + 1]
            is_placeholder = any(
                start >= rng_start and end <= rng_end for rng_start, rng_end in ranges
            )
            if is_placeholder:
                styled_segments.extend(Segment.apply_style(segment_group, post_style=style))
            else:
                styled_segments.extend(segment_group)

        return Strip(Segment.simplify(styled_segments), strip.cell_length)

    def _get_active_overlay(self) -> OverlayMixin | None:
        # ID-based lookup goes through Textual's _nodes_by_id index (O(1)
        # per call) instead of walking the screen DOM for each overlay
        # class. Each overlay is a singleton mounted in DreadnodeTextualApp
        # .compose with a stable id; if any later widget is added here,
        # mirror its id in this table.
        from textual.css.query import NoMatches

        from dreadnode.app.tui.widgets.agent_dialog import AgentDialog
        from dreadnode.app.tui.widgets.mention_overlay import MentionOverlay
        from dreadnode.app.tui.widgets.profile_dialog import ProfileDialog
        from dreadnode.app.tui.widgets.rewind_picker import RewindPickerOverlay
        from dreadnode.app.tui.widgets.skills_dialog import SkillsDialog
        from dreadnode.app.tui.widgets.slash_overlay import SlashOverlay
        from dreadnode.app.tui.widgets.tools_dialog import ToolsDialog

        overlays: tuple[tuple[str, type[OverlayMixin]], ...] = (
            ("#slash-overlay", SlashOverlay),
            ("#mention-overlay", MentionOverlay),
            ("#rewind-picker-overlay", RewindPickerOverlay),
            ("#agent-dialog", AgentDialog),
            ("#profile-dialog", ProfileDialog),
            ("#skills-dialog", SkillsDialog),
            ("#tools-dialog", ToolsDialog),
        )
        screen = self.screen
        for selector, overlay_type in overlays:
            try:
                overlay = screen.query_one(selector, overlay_type)
            except NoMatches:
                continue
            if overlay.is_visible:
                return overlay
        return None
