"""
Semantic streaming parser for <timeline> blocks.

Instead of waiting for </timeline> and parsing once, this parser
maintains state across token calls and emits a structured data update
every time a "renderable unit" is sealed:

  1. Opening tag detected        → empty shell  { title:"", periods:[] }
  2. Header line ends            → title + description populated
  3. Phase title line ends       → new period card appended (events=[])
  4. Each event sealed           → event appended to current period
     (event is "sealed" when the next "- " or next "**..." or closing
      tag is seen — i.e. we use one-token lookahead via the buffer)
  5. </timeline> / finalize      → final flush of any pending item

The parser is attached to the ContentBlock and called by
_apply_block_content on every token update.  It returns a
TimelineBlockData (the complete growing state) whenever new data
was appended, or None when the content hasn't moved past a boundary.

Output contract: emitted data is always a fully valid TimelineBlockData
that the React TimelineBlock component can render directly — no special
updateType envelope, no protocol changes required on the client.
"""

from __future__ import annotations

import re
from enum import Enum, auto

from matrx_ai.processing.blocks.models.timeline import TimelineBlockData, TimelineEvent, TimelinePeriod

# ---------------------------------------------------------------------------
# Regex constants
# ---------------------------------------------------------------------------

_TITLE_RE = re.compile(r'^#{1,3}\s+(.+)$')
_PERIOD_RE = re.compile(r'^\*\*([^*]+)\*\*$')
_EVENT_RE = re.compile(r'^-\s+(.+)$')
_BOLD_TITLE_RE = re.compile(r'^\*\*([^*]+)\*\*(.*)$')
_DATE_RE = re.compile(r'^\s*\(([^)]+)\)(.*)')
_CAT_RE = re.compile(r'^\s*\[([^\]]+)\](.*)')
_STATUS_WORDS = {'completed': 'completed', 'in-progress': 'in-progress',
                 'in progress': 'in-progress', 'pending': 'pending'}


class _State(Enum):
    BEFORE_TITLE = auto()
    AFTER_TITLE = auto()       # title seen, may still get description
    IN_CONTENT = auto()        # description done, processing phases/events


class TimelineStreamParser:
    """
    Stateful semantic parser for timeline blocks.

    Attach one instance to a ContentBlock and call feed(content) on every
    content update.  Returns a TimelineBlockData when new data should be
    emitted, or None if the token didn't cross a semantic boundary.

    Call finalize() when the block closes to flush any pending buffered item.
    """

    def __init__(self) -> None:
        self._state: _State = _State.BEFORE_TITLE
        self._title: str = ""
        self._description: str = ""
        self._periods: list[TimelinePeriod] = []
        self._current_period: TimelinePeriod | None = None
        self._pending_event_text: str | None = None   # event line buffered for sub-bullet
        self._pending_sub_bullets: list[str] = []
        self._last_emitted_snapshot: TimelineBlockData | None = None
        self._prev_content: str = ""   # content from the last call

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def feed(self, content: str) -> TimelineBlockData | None:
        """
        Feed the current (growing) content string.  Only the delta
        (lines added since the previous call) is processed.

        Returns a TimelineBlockData if a new renderable unit was sealed,
        otherwise None.
        """
        # Strip XML tags; work on the inner text only
        inner = re.sub(r'</?timeline>', '', content).strip()
        prev_inner = re.sub(r'</?timeline>', '', self._prev_content).strip()
        self._prev_content = content

        # Split both into lines and find the delta
        new_lines = inner.split('\n')
        old_lines = prev_inner.split('\n')

        if len(new_lines) <= len(old_lines):
            # Same line count — the tail line grew but no new line boundary
            # was crossed.  No semantic boundary possible yet.
            return None

        # Process each newly completed line (all but the last, which is still
        # being written).  The last element of old_lines was partial; the same
        # index in new_lines is now complete.
        start = max(0, len(old_lines) - 1)
        newly_completed = new_lines[start:-1]   # completed lines
        # The last line in new_lines is still partial — do NOT process it yet

        emitted = False
        for line in newly_completed:
            if self._process_line(line.rstrip()):
                emitted = True

        if not emitted:
            return None

        return self._snapshot()

    def finalize(self) -> TimelineBlockData:
        """
        Flush any pending buffered event and return the final complete state.
        Always returns a valid TimelineBlockData regardless of parse state.
        """
        self._flush_pending_event()
        if self._current_period and self._current_period.events:
            if self._current_period not in self._periods:
                self._periods.append(self._current_period)
        return self._snapshot()

    # ------------------------------------------------------------------
    # Internal line processor
    # ------------------------------------------------------------------

    def _process_line(self, line: str) -> bool:
        """
        Process one completed line.  Returns True if a semantic boundary
        was crossed (i.e. a new renderable unit is ready to emit).
        """
        stripped = line.strip()

        # Ignore empty lines and the closing tag
        if not stripped or stripped == '</timeline>':
            return False

        # --- Title ---
        if self._state == _State.BEFORE_TITLE:
            m = _TITLE_RE.match(stripped)
            if m:
                self._title = m.group(1).strip()
                self._state = _State.AFTER_TITLE
                # Don't emit yet — wait for description or first phase
                return False
            return False

        # --- Description (optional line after title, before first phase) ---
        if self._state == _State.AFTER_TITLE:
            pm = _PERIOD_RE.match(stripped)
            if pm:
                # No description — jump straight into content
                self._state = _State.IN_CONTENT
                # Fall through to period handling below
            elif not stripped.startswith('#') and not stripped.startswith('-'):
                self._description = stripped
                self._state = _State.IN_CONTENT
                # Emit the header now that we have title + description
                return True
            else:
                self._state = _State.IN_CONTENT

        # --- In-content: phases and events ---
        if self._state == _State.IN_CONTENT:
            pm = _PERIOD_RE.match(stripped)
            if pm:
                # Seal any pending event from the previous phase
                self._flush_pending_event()
                # Seal the previous period
                if self._current_period is not None and self._current_period not in self._periods:
                    self._periods.append(self._current_period)
                # Open new period
                self._current_period = TimelinePeriod(period=pm.group(1).strip())
                # Emit: new phase container visible immediately
                return True

            # Event bullet (top-level "- ", not indented)
            if line.startswith('- ') and not line.startswith('  - '):
                if stripped.startswith('- ') and not line.startswith('  '):
                    # Flush previous pending event — it's now sealed
                    flushed = self._flush_pending_event()
                    # Buffer this new event; we need the next line to check
                    # for a sub-bullet before we can emit it
                    self._pending_event_text = stripped[2:].strip()
                    self._pending_sub_bullets = []
                    return flushed   # emit if we flushed a complete event

            # Sub-bullet (indented "  - ...")
            elif line.startswith('  ') and stripped.startswith('- '):
                if self._pending_event_text is not None:
                    self._pending_sub_bullets.append(stripped[2:].strip())
                return False

            # Continuation line (indented, no dash)
            elif line.startswith('  ') and self._pending_event_text is not None:
                self._pending_sub_bullets.append(stripped)
                return False

        return False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _flush_pending_event(self) -> bool:
        """Build and append the buffered event to the current period. Returns True if flushed."""
        if self._pending_event_text is None or self._current_period is None:
            return False

        text = self._pending_event_text
        sub = ' '.join(self._pending_sub_bullets)
        ev = _parse_event(text, sub, self._current_period.period, len(self._current_period.events))
        self._current_period.events.append(ev)
        self._pending_event_text = None
        self._pending_sub_bullets = []
        return True

    def _snapshot(self) -> TimelineBlockData:
        """Return the current complete state as a TimelineBlockData."""
        # Build the final periods list: confirmed periods + current open period
        periods: list[TimelinePeriod] = list(self._periods)
        if self._current_period is not None and self._current_period not in self._periods:
            periods.append(self._current_period)
        return TimelineBlockData(
            title=self._title or "Timeline",
            description=self._description or None,
            periods=periods,
        )


# ---------------------------------------------------------------------------
# Event text parser (reused from original full parser)
# ---------------------------------------------------------------------------

def _parse_event(text: str, sub_desc: str, period_name: str, index: int) -> TimelineEvent:
    ev_title = text
    ev_date = ""
    ev_category = ""
    ev_status: str | None = None
    remainder = ""

    bold_m = _BOLD_TITLE_RE.match(text)
    if bold_m:
        ev_title = bold_m.group(1).strip()
        remainder = bold_m.group(2).strip()
    else:
        date_m = re.match(r'^(.+?)\s*\(([^)]+)\)(.*)$', text)
        if date_m:
            ev_title = date_m.group(1).strip()
            remainder = f"({date_m.group(2)}){date_m.group(3)}"
        else:
            cat_m = re.match(r'^(.+?)\s*\[([^\]]+)\](.*)$', text)
            if cat_m:
                ev_title = cat_m.group(1).strip()
                ev_category = cat_m.group(2).strip()

    date_m2 = _DATE_RE.match(remainder)
    if date_m2:
        ev_date = date_m2.group(1).strip()
        remainder = date_m2.group(2).strip()

    cat_m2 = _CAT_RE.match(remainder)
    if cat_m2:
        ev_category = cat_m2.group(1).strip()
        remainder = cat_m2.group(2).strip()

    lower = remainder.lower()
    for kw, status in _STATUS_WORDS.items():
        if kw in lower:
            ev_status = status
            break

    ev_desc = sub_desc or ev_title
    ev_id = f"{period_name}-{index}"

    return TimelineEvent(
        id=ev_id,
        title=ev_title,
        date=ev_date or "TBD",
        description=ev_desc,
        status=ev_status,  # type: ignore[arg-type]
        category=ev_category or None,
    )
