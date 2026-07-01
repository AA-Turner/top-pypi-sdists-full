"""Inline rewind picker overlay for the Dreadnode TUI.

Lists user-message rewind targets oldest-first so the newest turn sits
at the bottom (shell-history convention: ``Up`` walks back through
older entries). On Enter the picker posts a :class:`RewindSelected`
message; the app cancels any in-flight turn, calls the rewind
endpoint, reloads the truncated transcript, and restores the deleted
message's content to the composer.

Locked design lives in `ENG-6766` (axes), `ENG-6776` (TUI scope), and
the `SES-RWD-*` rule block in ``specs/sessions.md``.
"""

from __future__ import annotations

import typing as t
from datetime import UTC, datetime

from rich.text import Text
from textual.message import Message
from textual.widgets.option_list import Option

from dreadnode.app.tui.theme import BRAND, FG, FG_FAINTEST, FG_MUTED
from dreadnode.app.tui.widgets.overlay_mixin import OverlayMixin

_PREVIEW_MAX_LEN = 80
_EMPTY_OPTION_ID = "__empty__"


class RewindCandidate(t.TypedDict):
    """A user-message target the picker can rewind to.

    ``seq`` is the platform-side message sequence — the value the
    runtime's rewind endpoint accepts. ``content`` is the original
    user-message body the picker echoes back to the composer on commit.
    ``created_at`` is an ISO-8601 timestamp used for the row label;
    callers may omit it (then no timestamp is rendered).
    """

    seq: int
    content: str
    created_at: t.NotRequired[str | None]


class RewindPickerOverlay(OverlayMixin):
    """Inline overlay listing user messages eligible for rewind."""

    class RewindSelected(Message):
        """Posted when the user picks a target seq."""

        def __init__(self, seq: int, restored_content: str) -> None:
            self.seq = seq
            self.restored_content = restored_content
            super().__init__()

    def show_candidates(self, candidates: list[RewindCandidate]) -> None:
        """Populate the option list, oldest-first (newest at the bottom).

        Matches shell-history convention: the freshest turn sits next
        to the composer and ``Up`` walks back through older entries.
        An empty input renders a disabled "Nothing to rewind to" row
        rather than a blank list — the gesture must always feel
        anchored to a definite state.
        """
        self.clear_options()
        self._candidate_by_id: dict[str, RewindCandidate] = {}

        if not candidates:
            self.add_option(
                Option(
                    Text(" Nothing to rewind to", style=FG_MUTED),
                    id=_EMPTY_OPTION_ID,
                    disabled=True,
                )
            )
            self.add_class("-visible")
            return

        # Oldest-first: lower seqs at the top, newest at the bottom.
        # Sorted copy keeps caller's input untouched.
        ordered = sorted(candidates, key=lambda c: c["seq"])
        latest_idx = len(ordered) - 1
        for idx, candidate in enumerate(ordered):
            option_id = f"rewind-{candidate['seq']}"
            self._candidate_by_id[option_id] = candidate
            label = self._format_row(candidate, is_latest=(idx == latest_idx))
            self.add_option(Option(label, id=option_id))

        # Anchor selection on the newest row — same target as the
        # implicit "rewind one turn" gesture and the natural starting
        # point for ``Up`` to walk back from.
        self.highlighted = latest_idx
        self.add_class("-visible")

    def _format_row(self, candidate: RewindCandidate, *, is_latest: bool) -> Text:
        """Render one row: marker, timestamp, truncated content."""
        label = Text()

        # Marker — solid dot for the most recent (= the implicit
        # auto-recovery target), open dot otherwise.
        if is_latest:
            label.append(" ● ", style=BRAND)
        else:
            label.append(" ○ ", style=FG_FAINTEST)

        timestamp = _format_timestamp(candidate.get("created_at"))
        if timestamp:
            label.append(f"{timestamp}  ", style=FG_FAINTEST)

        preview = _make_preview(candidate.get("content") or "")
        label.append(preview, style="bold" if is_latest else FG)
        return label

    def select_highlighted(self) -> bool:
        """Commit the highlighted candidate. Returns True when handled."""
        if not self.is_visible or self.option_count == 0:
            return False

        # OptionList skips disabled rows when auto-highlighting, so the
        # empty-state row leaves ``highlighted is None``. Treat that as
        # "Enter on the dismissable empty state" rather than swallowing
        # the keypress — same user-visible effect as Esc.
        idx = self.highlighted
        if idx is None:
            self.hide()
            return True
        if not (0 <= idx < self.option_count):
            return False
        option = self.get_option_at_index(idx)
        if not option.id or option.id == _EMPTY_OPTION_ID:
            self.hide()
            return True
        candidate = self._candidate_by_id.get(option.id)
        if candidate is None:
            return False
        self.post_message(
            self.RewindSelected(
                seq=candidate["seq"],
                restored_content=candidate.get("content") or "",
            )
        )
        self.hide()
        return True

    def on_option_list_option_selected(self, event: OverlayMixin.OptionSelected) -> None:
        """Mouse-click handler — same path as Enter on the highlight."""
        option_id = event.option.id
        if not option_id or option_id == _EMPTY_OPTION_ID:
            self.hide()
            return
        candidate = self._candidate_by_id.get(option_id)
        if candidate is None:
            return
        self.post_message(
            self.RewindSelected(
                seq=candidate["seq"],
                restored_content=candidate.get("content") or "",
            )
        )
        self.hide()


def _make_preview(content: str) -> str:
    """One-line preview, ellipsised at ``_PREVIEW_MAX_LEN``."""
    cleaned = content.strip().replace("\n", " ")
    if not cleaned:
        return "(empty)"
    if len(cleaned) > _PREVIEW_MAX_LEN:
        return cleaned[: _PREVIEW_MAX_LEN - 1] + "…"
    return cleaned


def _format_timestamp(raw: t.Any) -> str:
    """Format ``created_at`` as a relative or absolute label.

    Picker rows want a short anchor — "5m ago" for recent turns,
    "2h ago" for a few hours back, ISO date for anything older. The
    full timestamp is overkill for the picker context; a fuzzy label
    matches how Claude Code / opencode render their rewind targets.
    """
    if not isinstance(raw, str) or not raw:
        return ""
    try:
        # Accept both ``Z``-suffixed and offset forms.
        normalized = raw.replace("Z", "+00:00") if raw.endswith("Z") else raw
        ts = datetime.fromisoformat(normalized)
    except ValueError:
        return ""
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=UTC)

    delta = datetime.now(UTC) - ts
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return "just now"
    if seconds < 3600:
        return f"{seconds // 60}m ago"
    if seconds < 86400:
        return f"{seconds // 3600}h ago"
    if seconds < 7 * 86400:
        return f"{seconds // 86400}d ago"
    return ts.date().isoformat()
