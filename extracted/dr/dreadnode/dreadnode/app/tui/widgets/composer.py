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
    from textual.widgets.text_area import Edit, EditResult

    from dreadnode.app.tui.widgets.overlay_mixin import OverlayMixin


@dataclass(slots=True)
class PastedSegment:
    content: str
    line_count: int


_PASTE_RE = re.compile(r"\[pasted ~(\d+) lines?\]")
# Snapshots are keyed by undo checkpoint, and Textual keeps 50 of those, so a
# checkpoint we can no longer undo back to is one we need no content for.
_PASTE_HISTORY_LIMIT = 50


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
        # One entry per placeholder in the display text, in document order. None means
        # the placeholder has no backing content — the user typed the literal text.
        self._pastes: list[PastedSegment | None] = []
        self._paste_history: dict[int, tuple[str, list[PastedSegment | None]]] = {}
        self._pending_paste: PastedSegment | None = None

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
        self._paste_history.clear()

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
        self._pending_paste = PastedSegment(content=pasted, line_count=line_count)
        try:
            self.insert(placeholder)
        finally:
            self._pending_paste = None

    def _resolve_pastes(self, display_text: str) -> str:
        pastes = iter(self._pastes)

        def replacer(match: re.Match[str]) -> str:
            segment = next(pastes, None)
            return segment.content if segment else match.group(0)

        return _PASTE_RE.sub(replacer, display_text)

    def _paste_at(self, index: int) -> PastedSegment | None:
        return self._pastes[index] if 0 <= index < len(self._pastes) else None

    def edit(self, edit: Edit) -> EditResult:
        """Re-index tracked segments across an edit by the document range it replaces.

        Placeholder text carries no identity — two pastes of the same line count read
        identically — so a diff of the placeholder strings cannot say which one an
        edit removed. The range being replaced can: segments are matched to the
        positions that survive it. Undo and redo do not come through here at all;
        `_sync_pastes` restores those from the snapshot history.
        """
        kept_before, kept_after = self._split_pastes_around(edit)
        result = super().edit(edit)
        added = len(_PASTE_RE.findall(edit.text))
        if added == 1 and self._pending_paste is not None:
            added_pastes: list[PastedSegment | None] = [self._pending_paste]
        else:
            added_pastes = [None] * added
        self._pastes = kept_before + added_pastes + kept_after
        # Snapshot ahead of the queued Changed message so this is what lands.
        self._remember_pastes(self.text)
        return result

    def _split_pastes_around(
        self, edit: Edit
    ) -> tuple[list[PastedSegment | None], list[PastedSegment | None]]:
        """Partition segments into those wholly before and wholly after the edit.

        A segment whose placeholder the edit overlaps is dropped: its text no longer
        survives in the document, so nothing backs it.
        """
        start = self._document_index(edit.top)
        end = self._document_index(edit.bottom)
        kept_before: list[PastedSegment | None] = []
        kept_after: list[PastedSegment | None] = []
        for index, match in enumerate(_PASTE_RE.finditer(self.text)):
            if match.end() <= start:
                kept_before.append(self._paste_at(index))
            elif match.start() >= end:
                kept_after.append(self._paste_at(index))
        return kept_before, kept_after

    def _remember_pastes(self, display_text: str) -> None:
        """Snapshot the current segments against the undo checkpoint they belong to.

        Keying on the checkpoint rather than the display text is what makes this
        safe: the same text recurs with different content — paste, delete, paste
        again — and a text-keyed snapshot hands the second paste's content back to
        the first. The text is kept only to verify a hit before trusting it.
        """
        depth = len(self.history.undo_stack)
        for redo_only in [key for key in self._paste_history if key > depth]:
            del self._paste_history[redo_only]
        if any(self._pastes):
            self._paste_history[depth] = (display_text, list(self._pastes))
        else:
            self._paste_history.pop(depth, None)
        while len(self._paste_history) > _PASTE_HISTORY_LIMIT:
            del self._paste_history[min(self._paste_history)]

    def _restore_pastes(self, display_text: str) -> bool:
        """Bring back the segments for an undo or redo target, if we still hold them."""
        remembered = self._paste_history.get(len(self.history.undo_stack))
        if remembered is None or remembered[0] != display_text:
            return False
        self._pastes = list(remembered[1])
        return True

    def load_text(self, text: str) -> None:
        """Replace the document wholesale.

        Textual drops its undo history here, so the snapshots keyed against it go
        too, and nothing in the new text is backed by a tracked paste.
        """
        super().load_text(text)
        self.clear_pastes()

    def _sync_pastes(self, display_text: str) -> None:
        """Re-bind segments to the placeholders on screen after the document changes.

        Forward edits are already re-indexed by `edit`, which knows the range it
        replaced. Undo and redo bypass `edit` entirely and restore placeholder
        *text* whose segment was dropped, so they are served from the checkpoint
        snapshots. Anything else leaves the placeholders unbacked, and they resolve
        to their own literal label — visibly wrong in the composer, rather than
        quietly binding someone else's content.
        """
        if not self._restore_pastes(display_text):
            placeholders = len(_PASTE_RE.findall(display_text))
            if placeholders != len(self._pastes):
                self._pastes = [None] * placeholders
        self._remember_pastes(display_text)

    def _remove_paste_at_cursor(self, *, forward: bool) -> bool:
        """Delete a tracked paste placeholder as one editing operation."""
        if not self.selection.is_empty:
            return False
        text = self.text
        cursor = self._document_index(self.cursor_location)
        placeholders = list(_PASTE_RE.finditer(text))
        for index, match in enumerate(placeholders):
            at_boundary = cursor == (match.end() if not forward else match.start())
            if not at_boundary or self._paste_at(index) is None:
                continue
            start = self._document_location(match.start())
            end = self._document_location(match.end())
            self.delete(start, end)
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
