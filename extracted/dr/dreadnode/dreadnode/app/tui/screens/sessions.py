"""Full-screen session picker — DataTable with labeled status + lifecycle actions.

Column analysis (vs. the web UI ``/agents/sessions`` grid in
``frontend/src/routes/[org_key]/agents/sessions/columns.ts``):

| Web column   | Width   | TUI status | Reason                                        |
|--------------|---------|-----------:|-----------------------------------------------|
| title        | flex 2  | ✓ keep     | Anchor for every row; carries the inline      |
|              |         |            | status tokens too (see "Inline status").      |
| origin       | 64 (i)  | ⤵ inline   | Icon-only column reads as garbage in a TUI;   |
|              |         |            | most rows are ``user`` so cell stays empty.   |
|              |         |            | Surface as ``(eval)`` / ``(worker)`` token    |
|              |         |            | on the title row only when non-default.       |
| agent        | flex 1  | ✓ keep     | Distinct identity per session.                |
| model        | flex 1  | ✓ keep     | Per-row signal when workspaces mix models.    |
| owner        | flex 1  | ✗ drop     | Single-user TUI assumption — re-add when we   |
|              |         |            | grow into multi-user collaborative sessions.  |
| messageCount | 72px    | ✓ keep     | Right-aligned numeric — quick freshness cue.  |
| totalTokens  | 80px    | ✓ keep     | Right-aligned, k/M-formatted to keep narrow.  |
| project      | flex 1  | ✓ keep     | Useful when juggling multiple projects.       |
| labels       | flex 1  | ✓ keep     | Up-to-3 ``key=val`` chips + overflow count.   |
| lastMessageAt| 88px    | ✓ keep     | Recency is the primary picker signal.         |
| visibility   | 80 (i)  | ⤵ inline   | Glyph-only column was unreadable. Inline as   |
| (status)     |         |            | labeled words on the title row.               |

Inline status tokens (the row's runtime + lifecycle + origin state) all
ride together AFTER the title in a single ``·``-separated strip, in a
fixed order. No state gets a special leading-prefix slot — every token
gets the same position so the row reads predictably whether it's running,
archived, both, or neither. Color encodes intent (red = failed, orange =
running, yellow = needs-action, muted = lifecycle, subtle = origin/counts);
position never carries meaning a glyph would otherwise have to.

The "is this the active session?" indicator isn't a token at all — the
active row is pinned to position 0 (see ``_rebuild_rows``), so position
is the indicator and we don't need a redundant ``active`` chip.

Actions match the web UI's detail pane: archive (default — easy to undo,
no confirm), freeze (terminal, modal confirm), delete (destructive, modal
confirm). All execute immediately against the runtime/platform — there is
no "queue and apply on exit" pattern. ``ctrl+o`` opens the focused row in
the web UI, reusing the same monitoring deep-link the report tool uses.

Search vs. action conflict: typed characters always feed the search bar;
actions live exclusively on ctrl-prefixed bindings.

Return contract:
  None                — Escape pressed, no selection
  "__new__"           — ctrl+n pressed, create new session
  "<session_id>"      — Enter on a row
"""

import typing as t
from dataclasses import dataclass
from datetime import UTC, datetime

from loguru import logger
from rich.text import Text
from textual import work
from textual.binding import Binding
from textual.coordinate import Coordinate
from textual.screen import Screen
from textual.widgets import DataTable, Static

from dreadnode.app.client.models import SessionInfo
from dreadnode.app.tui.screens.base import (
    _bind_status_bar_to_app,
    handle_search_input_key,
    handle_search_input_paste,
    render_hint_bar,
    render_screen_header,
    render_search_bar,
)
from dreadnode.app.tui.theme import (
    ACCENT,
    ERROR,
    FG,
    FG_FAINTEST,
    FG_MUTED,
    FG_SUBTLE,
    WARNING,
)
from dreadnode.app.tui.turn_state_phase import (
    TurnStatePhase,
    is_running_phase,
)
from dreadnode.app.tui.widgets.confirm_modal import ConfirmModal
from dreadnode.app.tui.widgets.status_bar import StatusBar

if t.TYPE_CHECKING:
    from textual.app import ComposeResult
    from textual.events import Key, Paste

    from dreadnode.app.client.runtime_client import RuntimeClient
    from dreadnode.app.tui.app import SessionRecord


# ── Helpers ──────────────────────────────────────────────────────────────────


def _relative_time(iso_ts: str | None) -> str:
    """Format an ISO timestamp as a human-friendly relative string."""
    if not iso_ts:
        return "-"
    try:
        dt = datetime.fromisoformat(iso_ts)
    except ValueError:
        return iso_ts[:16]
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    delta = datetime.now(tz=UTC) - dt
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return "just now"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours}h ago"
    days = hours // 24
    if days < 7:
        return f"{days}d ago"
    return dt.strftime("%b %d")


def _truncate(text: str, max_len: int) -> str:
    text = text.strip().replace("\n", " ")
    if len(text) > max_len:
        return text[: max_len - 1] + "…"
    return text


def _row_title(info: SessionInfo, record: "SessionRecord | None") -> str:
    """Title line for the picker row — never empty.

    For in-process rows this defers to :meth:`SessionRecord.display_title`
    (real title, else ``"<agent> session"``). Platform-only rows mirror
    the same fallback inline since they don't have a ``SessionRecord``.
    Mirrors the frontend monitoring grid (columns.ts:138).
    """
    if record is not None:
        return record.display_title()
    if info.title:
        return info.title
    agent = info.agent or "default"
    return f"{agent} session"


def _row_preview(info: SessionInfo, record: "SessionRecord | None") -> str | None:
    """First user-message snippet for the picker row, or None.

    For in-process rows defers to :meth:`SessionRecord.display_preview`,
    which prefers the server preview and falls back to the local
    transcript. Platform-only rows use ``info.preview`` directly.
    """
    if record is not None:
        return record.display_preview()
    return info.preview


# ── Status tokens ────────────────────────────────────────────────────────────


def _status_tokens(info: SessionInfo, record: "SessionRecord | None") -> list[tuple[str, str]]:
    """Inline status tokens for the title row, in fixed display order.

    Every token gets the same positional treatment — same separator,
    same line, same anchor — so a row that's both ``running`` and
    ``archived`` reads predictably regardless of which states are set.
    Color is the only differentiator between phase / lifecycle / origin /
    counts; position never carries meaning a glyph would have to.

    Order is fixed so a row with the same state always renders the same
    way (no shuffling on every render): phase → lifecycle → origin →
    runtime counts.

    "Active" is intentionally absent — the active row is pinned to
    position 0, so position already carries that signal and an
    additional chip would just be noise.
    """
    tokens: list[tuple[str, str]] = []

    # Phase: at most one — failed > approval > input > running. These
    # are mutually exclusive in practice (they're successive points in
    # the turn lifecycle), so picking the highest-severity one is
    # honest about what the user actually needs to know.
    state = record.turn_state if record is not None else None
    if state is not None:
        if state.phase is TurnStatePhase.FAILED:
            tokens.append(("failed", ERROR))
        elif state.phase is TurnStatePhase.AWAITING_PERMISSION:
            tokens.append(("approval", WARNING))
        elif state.phase is TurnStatePhase.AWAITING_INPUT:
            tokens.append(("input", WARNING))
        elif is_running_phase(state.phase):
            tokens.append(("running", ACCENT))

    # Lifecycle — only render when non-default, matching the web UI
    # stateRenderer convention (columns.ts:231).
    if info.archived_at:
        tokens.append(("archived", FG_MUTED))
    if info.frozen_at:
        tokens.append(("frozen", WARNING))
    if info.visibility == "workspace":
        tokens.append(("shared", FG_SUBTLE))

    # Origin — only when non-user. Parens differentiate "where it came
    # from" visually from lifecycle words without changing color load.
    if info.origin and info.origin != "user":
        tokens.append((f"({info.origin})", FG_SUBTLE))

    # Runtime-only counts — TUI-specific, no web analogue.
    if record is not None:
        if record.unread_events > 0:
            label = "1 unread" if record.unread_events == 1 else f"{record.unread_events} unread"
            tokens.append((label, FG_MUTED))
        if record.queued_messages:
            n = len(record.queued_messages)
            label = "1 queued" if n == 1 else f"{n} queued"
            tokens.append((label, FG_MUTED))
        if record.resync_required:
            tokens.append(("stale", WARNING))

    return tokens


def _title_cell(
    info: SessionInfo,
    record: "SessionRecord | None",
    *,
    max_len: int = 56,
) -> Text:
    """Two-line title cell — title + status strip, then preview.

    Layout::

        {title}  ·  {status1}  ·  {status2}  ·  …
        {preview}

    Every status token sits in the same trailing strip with the same
    middle-dot separator and the same position — no token gets a special
    "leading prefix" slot, so a row that's running + archived reads as
    cleanly as one that's just running. Color encodes intent (red /
    orange / yellow / muted / subtle); position is consistent.

    Title truncates so a row with many status tokens doesn't push the
    strip off-screen. Preview lives on the second line in muted text;
    rows without a preview leave it blank so cursor movement and zebra
    stripes stay even.
    """
    cell = Text()
    cell.append(_truncate(_row_title(info, record), max_len), style=FG)
    for label, style in _status_tokens(info, record):
        cell.append("  ·  ", style=FG_FAINTEST)
        cell.append(label, style=style)
    cell.append("\n")
    preview = _row_preview(info, record)
    if preview:
        cell.append(_truncate(preview, max_len), style=FG_MUTED)
    return cell


# ── Numeric / collection cells ───────────────────────────────────────────────


def _format_token_count(value: int) -> str:
    """Compact ``k`` / ``M`` formatter — mirrors the web UI's
    ``formatTokenCount`` (columns.ts:275) so a tokens cell fits in 6
    characters and reads as the same shorthand the web UI uses.
    """
    if value <= 0:
        return "-"
    if value < 1_000:
        return str(value)
    if value < 1_000_000:
        scaled = value / 1_000
        return f"{scaled:.1f}k" if value < 10_000 else f"{int(scaled)}k"
    scaled_m = value / 1_000_000
    return f"{scaled_m:.1f}M" if value < 10_000_000 else f"{int(scaled_m)}M"


def _msgs_cell(info: SessionInfo) -> Text:
    """Right-aligned message count, dim when zero so empty rows fade."""
    count = info.message_count or 0
    if count <= 0:
        return Text("-", style=FG_FAINTEST, justify="right")
    return Text(str(count), style=FG_SUBTLE, justify="right")


def _tokens_cell(info: SessionInfo) -> Text:
    """Right-aligned compact token total, dim when unknown/zero."""
    formatted = _format_token_count(info.total_tokens or 0)
    style = FG_FAINTEST if formatted == "-" else FG_SUBTLE
    return Text(formatted, style=style, justify="right")


def _model_cell(record: "SessionRecord | None") -> Text:
    """Per-row model identifier — pulled from the in-process record where
    available, else ``-`` for platform-only rows that don't carry it.
    ``SessionInfo`` doesn't model this field, so platform rows render as
    ``-`` until the platform browse envelope grows it.
    """
    if record is not None and record.model:
        return Text(_truncate(record.model, 18), style=FG_SUBTLE)
    return Text("-", style=FG_FAINTEST)


def _labels_cell(info: SessionInfo) -> Text:
    """Up-to-3 ``key=value`` chips with an overflow count.

    Mirrors the web UI's labelsRenderer (columns.ts:187) at TUI density:
    same maximum, same overflow indicator. Each chip renders as plain
    ``key=val`` text instead of a CodeTag (no border-drawing in
    DataTable cells), but the information density is the same.
    """
    cell = Text()
    total = sum(len(values or ()) for values in info.labels.values())
    if total == 0:
        cell.append("-", style=FG_FAINTEST)
        return cell

    shown = 0
    max_chips = 3
    for key in sorted(info.labels):
        for value in info.labels[key]:
            if shown >= max_chips:
                break
            if shown > 0:
                cell.append(" ", style=FG_FAINTEST)
            cell.append(f"{key}=", style=FG_FAINTEST)
            cell.append(_truncate(value, 12), style=FG_SUBTLE)
            shown += 1
        if shown >= max_chips:
            break

    overflow = total - shown
    if overflow > 0:
        cell.append(f"  +{overflow}", style=FG_FAINTEST)
    return cell


# ── Search bar filter grammar ────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class _ParsedSearch:
    """Decomposed query string: free-text plus structured `key:value` filters.

    Grammar matches the runtimes-picker style (``state:running``, etc.)
    so muscle memory transfers. Known keys become server-side filter
    params on :meth:`RuntimeClient.browse_sessions`; any unknown
    ``key:value`` token is dropped into ``free_text`` so it becomes
    part of the full-text ``search`` param rather than silently
    disappearing.
    """

    free_text: str = ""
    archived: t.Literal["active", "inactive", "archived", "any"] = "active"
    origin: str | None = None
    project: str | None = None

    def browse_kwargs(self) -> dict[str, t.Any]:
        kwargs: dict[str, t.Any] = {"archived": self.archived}
        if self.origin is not None:
            kwargs["origin"] = [self.origin]
            # SES-LST-015 / SES-LST-009: an explicit workload origin
            # (``eval`` today) needs the workload-hide default toggled
            # off to return non-empty results.
            if self.origin != "user":
                kwargs["include_workload_sessions"] = True
        if self.project is not None:
            kwargs["project_id"] = [self.project]
        if self.free_text:
            kwargs["search"] = self.free_text
        return kwargs


def _parse_search(query: str) -> _ParsedSearch:
    text_terms: list[str] = []
    archived: t.Literal["active", "inactive", "archived", "any"] = "active"
    origin: str | None = None
    project: str | None = None
    for token in query.split():
        if ":" in token:
            key, value = token.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            if key == "status" and value in {"active", "inactive", "archived", "any"}:
                archived = t.cast(
                    "t.Literal['active', 'inactive', 'archived', 'any']",
                    value,
                )
                continue
            if key == "origin" and value:
                origin = value
                continue
            if key == "project" and value:
                project = value
                continue
        text_terms.append(token)
    return _ParsedSearch(
        free_text=" ".join(text_terms).strip(),
        archived=archived,
        origin=origin,
        project=project,
    )


# ── Row model ────────────────────────────────────────────────────────────────


@dataclass(slots=True)
class _Row:
    """One visible session — backed by a SessionRecord for in-process rows,
    or a plain SessionInfo for platform-only rows arrived from browse.

    ``record`` is ``None`` for rows that exist only on the platform; in
    that case the row has no live TurnState, unread count, or queued
    messages — it's strictly metadata for browsing purposes.
    """

    session_id: str
    info: SessionInfo
    record: "SessionRecord | None" = None

    @property
    def sort_key(self) -> str:
        return self.info.updated_at or self.info.created_at or ""


# ── Screen ───────────────────────────────────────────────────────────────────


class SessionPickerScreen(Screen[str | None]):
    """Full-screen session picker with labeled status + lifecycle actions."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        # Navigation / selection — declared so DataTable doesn't swallow
        # keys we want the screen to drive (cursor mirrors `_cursor`).
        Binding("up", "cursor_up", "Up", show=False),
        Binding("down", "cursor_down", "Down", show=False),
        Binding("enter", "select", "Open", show=False),
        Binding("escape", "escape", "Back", show=False),
        # Lifecycle actions — ctrl-prefixed so typing into the search bar
        # never accidentally archives or deletes a session.
        Binding("ctrl+x", "archive_toggle", "Archive", show=False),
        Binding("ctrl+l", "freeze", "Freeze", show=False),
        Binding("ctrl+d", "delete", "Delete", show=False),
        Binding("ctrl+o", "open_in_browser", "Open in browser", show=False),
        # Create-new mirrors the app-level binding so a fresh session
        # cleanly dismisses the picker first.
        Binding("ctrl+n", "new_session", "New", show=False),
    ]

    def __init__(
        self,
        sessions: dict[str, "SessionRecord"],
        active_session_id: str | None = None,
        managed_client: "RuntimeClient | None" = None,
        on_session_deleted: t.Callable[[str], None] | None = None,
        session_web_url: t.Callable[[str], str | None] | None = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)
        self._sessions = dict(sessions)
        self._active_session_id = active_session_id
        self._managed_client = managed_client
        # Invoked after a successful in-picker delete so the parent app
        # can drop the session from its own ``self.sessions`` map and
        # re-route the active session if needed. Archive and freeze
        # mutate ``record.info`` in place — those propagate via shared
        # ``SessionRecord`` references and don't need a callback.
        self._on_session_deleted = on_session_deleted
        # Resolves a session id to its public web-UI URL. ``None`` from
        # this callback (or no callback at all) means the action is
        # unavailable — the picker degrades to a notify toast in that
        # case rather than opening a half-formed URL.
        self._session_web_url = session_web_url

        # Merged row state. `_platform_rows` holds the latest platform
        # page; `_rows` is the computed union used for rendering.
        self._platform_rows: dict[str, SessionInfo] = {}
        self._rows: list[_Row] = []

        # UI state.
        self._cursor: int = 0
        self._search_query: str = ""

    # ── Compose ──────────────────────────────────────────────────────────

    def compose(self) -> "ComposeResult":
        yield Static(id="session-header")
        yield Static(id="session-search")
        yield DataTable(id="session-table")
        yield Static(id="session-hint-bar")
        yield StatusBar(id="global-status-bar")

    def on_mount(self) -> None:
        _bind_status_bar_to_app(self, self.query_one("#global-status-bar", StatusBar))

        table = self.query_one("#session-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        # Eight columns — see module docstring for the column-by-column
        # analysis vs. the web UI grid. Status / lifecycle / origin /
        # runtime state all ride inline on the Title cell as labeled
        # words; there is no separate icon or status column.
        table.add_columns(
            "Title",
            "Updated",
            "Agent",
            "Model",
            "Msgs",
            "Tokens",
            "Project",
            "Labels",
        )

        self._rebuild_rows()
        self._render_all()
        table.focus()
        self._load_platform_page()

    # ── Keyboard handling ────────────────────────────────────────────────

    def on_key(self, event: "Key") -> None:
        """Route typed characters into the search input.

        All non-character keys (arrows, enter, ctrl combos, function keys)
        are declared in ``BINDINGS`` and fire via ``action_*`` methods.
        This handler only exists to feed the search bar and to let
        ``escape`` clear the search before the binding's dismiss fires.
        """
        key = event.key

        # Control combos and function keys pass through to BINDINGS / app.
        if key.startswith("ctrl+") or (key.startswith("f") and key[1:].isdigit()):
            return

        # Escape clears search when active; BINDINGS handles dismiss otherwise.
        if key == "escape" and self._search_query:
            self._search_query = ""
            self._cursor = 0
            self._reload_on_search_change()
            event.prevent_default()
            event.stop()
            return

        if key == "escape":
            return  # let BINDINGS handle

        search_result = handle_search_input_key(
            self._search_query, key=key, character=event.character
        )
        if not search_result.handled:
            return
        if search_result.new_query == self._search_query:
            return
        self._search_query = search_result.new_query
        if search_result.cursor_should_reset:
            self._cursor = 0
        self._reload_on_search_change()
        event.prevent_default()
        event.stop()

    def on_paste(self, event: "Paste") -> None:
        """Append bracketed-paste text to the search query."""
        result = handle_search_input_paste(self._search_query, text=event.text)
        if not result.handled:
            return
        self._search_query = result.new_query
        if result.cursor_should_reset:
            self._cursor = 0
        self._reload_on_search_change()
        event.prevent_default()
        event.stop()

    # ── BINDINGS actions ─────────────────────────────────────────────────

    def action_cursor_up(self) -> None:
        if not self._rows:
            return
        self._cursor = max(0, self._cursor - 1)
        self._apply_cursor_to_table()

    def action_cursor_down(self) -> None:
        if not self._rows:
            return
        self._cursor = min(len(self._rows) - 1, self._cursor + 1)
        self._apply_cursor_to_table()

    def action_select(self) -> None:
        if not self._rows or not (0 <= self._cursor < len(self._rows)):
            return
        sid = self._rows[self._cursor].session_id
        self.dismiss(sid)

    def action_escape(self) -> None:
        # Search-clear is handled in ``on_key`` so it can intercept Escape
        # before this binding fires. Reaching this action means search is
        # already empty — dismiss the screen.
        self.dismiss(None)

    def action_new_session(self) -> None:
        self.dismiss("__new__")

    def action_archive_toggle(self) -> None:
        """Toggle archive state for the focused row — primary lifecycle action.

        No confirm: archive is reversible (unarchive flips it right back),
        and forcing a confirm on a non-destructive action just trains the
        user to ack-and-ignore prompts. Mirrors the web UI's direct-fire
        Archive button (no confirm dialog there either).
        """
        row = self._focused_row()
        if row is None:
            return
        currently_archived = row.info.archived_at is not None
        verb = "Unarchive" if currently_archived else "Archive"
        self._run_lifecycle_action(
            verb=verb,
            session_id=row.session_id,
            session_title=_row_title(row.info, row.record),
            kind="archive",
            archived_target=not currently_archived,
        )

    def action_freeze(self) -> None:
        """Freeze the focused row — terminal, gated by an explicit modal."""
        row = self._focused_row()
        if row is None:
            return
        if row.info.frozen_at:
            self.notify("Session already frozen", title="Sessions", severity="warning")
            return
        title = _row_title(row.info, row.record)
        self.app.push_screen(
            ConfirmModal(
                title="Freeze this session?",
                message=(
                    f"“{_truncate(title, 60)}” will be frozen — no new "
                    "messages can be appended and there is no way to thaw it."
                ),
                confirm_label="Freeze",
                intent="warning",
            ),
            callback=lambda confirmed: self._on_freeze_confirmed(
                confirmed=bool(confirmed),
                session_id=row.session_id,
                session_title=title,
            ),
        )

    def _on_freeze_confirmed(self, *, confirmed: bool, session_id: str, session_title: str) -> None:
        if not confirmed:
            return
        self._run_lifecycle_action(
            verb="Freeze",
            session_id=session_id,
            session_title=session_title,
            kind="freeze",
        )

    def action_delete(self) -> None:
        """Delete the focused row — destructive, gated by an explicit modal.

        Mirrors the web UI's pendingConfirm dialog (``handleDeleteAction``):
        modal blocks the picker until the user explicitly confirms or
        cancels. Default focus on the cancel button so a fat-fingered
        Enter doesn't fire.
        """
        row = self._focused_row()
        if row is None:
            return
        title = _row_title(row.info, row.record)
        self.app.push_screen(
            ConfirmModal(
                title="Delete this session?",
                message=(
                    f"“{_truncate(title, 60)}” and its transcript will be "
                    "removed. Sessions referenced by evaluations cannot be "
                    "deleted."
                ),
                confirm_label="Delete",
                intent="danger",
            ),
            callback=lambda confirmed: self._on_delete_confirmed(
                confirmed=bool(confirmed),
                session_id=row.session_id,
                session_title=title,
            ),
        )

    def _on_delete_confirmed(self, *, confirmed: bool, session_id: str, session_title: str) -> None:
        if not confirmed:
            return
        self._run_lifecycle_action(
            verb="Delete",
            session_id=session_id,
            session_title=session_title,
            kind="delete",
        )

    def action_open_in_browser(self) -> None:
        """Open the focused row in the web UI ``/agents/sessions`` view.

        Reuses the same deep-link pattern the report tool uses (see
        ``DreadnodeTextualApp._build_app_url`` / ``report_url``). Falls
        back to a notify toast when no platform context is available
        (unauthenticated, local-only, missing org/workspace).
        """
        row = self._focused_row()
        if row is None:
            return
        if self._session_web_url is None:
            self.notify(
                "Open-in-browser requires a connected platform workspace",
                title="Sessions",
                severity="warning",
            )
            return
        url = self._session_web_url(row.session_id)
        if not url:
            self.notify(
                "Open-in-browser requires a connected platform workspace",
                title="Sessions",
                severity="warning",
            )
            return
        # Textual's ``App.open_url`` shells out to ``webbrowser.open``
        # which handles platform-specific launchers — we don't want to
        # import webbrowser here directly because Textual already wraps
        # it with the right error handling for the headless case.
        self.app.open_url(url)
        self.notify(
            f"Opened in browser: {url}",
            title="Sessions",
            severity="information",
        )

    # ── Row helpers ──────────────────────────────────────────────────────

    def _focused_row(self) -> _Row | None:
        if not self._rows or not (0 <= self._cursor < len(self._rows)):
            return None
        return self._rows[self._cursor]

    # ── Lifecycle action runner ──────────────────────────────────────────

    @work(group="session-action")
    async def _run_lifecycle_action(
        self,
        *,
        verb: str,
        session_id: str,
        session_title: str,
        kind: t.Literal["archive", "delete", "freeze"],
        archived_target: bool = False,
    ) -> None:
        """Execute one lifecycle mutation against the runtime/platform.

        Local row state is updated optimistically on success so the row
        appears/disappears (archive/delete) or picks up its lifecycle
        label (freeze) without waiting for the next browse refresh. We
        still kick a background ``_load_platform_page`` so any cascading
        platform side-effects (e.g. last-message-at touched on freeze)
        land in the table.
        """
        if self._managed_client is None:
            self.notify(
                f"{verb} requires a connected runtime",
                title="Sessions",
                severity="warning",
            )
            return

        try:
            if kind == "archive":
                await self._managed_client.archive_session(session_id, archived=archived_target)
            elif kind == "freeze":
                await self._managed_client.freeze_session(session_id)
            elif kind == "delete":
                await self._managed_client.delete_session(session_id)
        except Exception as exc:
            logger.opt(exception=True).warning(
                "Session {} failed | session={} kind={}",
                verb.lower(),
                session_id[:8],
                kind,
            )
            self.notify(
                f"{verb} failed: {exc}",
                title="Sessions",
                severity="error",
            )
            return

        self._apply_optimistic_local_update(
            session_id=session_id, kind=kind, archived_target=archived_target
        )
        self.notify(
            f"{verb}d “{_truncate(session_title, 40)}”",
            title="Sessions",
            severity="information",
        )
        # The screen may have been popped while the mutation was in flight.
        # The optimistic update above still matters (it patches shared
        # records the parent app renders from), but rendering would
        # query_one against a dead widget tree (NoMatches).
        if not self.is_mounted:
            return
        # Surgical render — only the affected row changes. Avoids the
        # full ``table.clear()`` + rebuild flash that ``_render_all``
        # would cause on every action. We also intentionally do NOT
        # re-fetch the platform page here: the optimistic update is
        # the same write the platform just applied, so a reconcile
        # would only produce a delayed second-render flash without
        # changing the visible state.
        self._apply_lifecycle_render(session_id=session_id, kind=kind)

    def _apply_optimistic_local_update(
        self,
        *,
        session_id: str,
        kind: t.Literal["archive", "delete", "freeze"],
        archived_target: bool,
    ) -> None:
        """Mirror a successful platform write onto the in-memory row state.

        Keeps the picker consistent without a full re-fetch round-trip.
        Platform-only rows live in ``_platform_rows``; in-process rows
        live in ``_sessions`` — both need the same patch so whichever
        the row was sourced from picks up the change.
        """
        now = datetime.now(tz=UTC).isoformat()

        if kind == "delete":
            self._sessions.pop(session_id, None)
            self._platform_rows.pop(session_id, None)
            if self._on_session_deleted is not None:
                # Bubble the delete to the parent app so its ``self.sessions``
                # stays in lockstep — without this the sidebar would still
                # render a phantom row until the next server refresh.
                try:
                    self._on_session_deleted(session_id)
                except Exception:
                    logger.opt(exception=True).warning(
                        "on_session_deleted callback failed | session={}",
                        session_id[:8],
                    )
            return

        record = self._sessions.get(session_id)
        platform_row = self._platform_rows.get(session_id)

        if kind == "archive":
            ts = now if archived_target else None
            if record is not None:
                record.info.archived_at = ts
            if platform_row is not None:
                platform_row.archived_at = ts
            return

        if kind == "freeze":
            if record is not None:
                record.info.frozen_at = now
            if platform_row is not None:
                platform_row.frozen_at = now

    # ── Surgical render after a lifecycle action ─────────────────────────

    def _apply_lifecycle_render(
        self,
        *,
        session_id: str,
        kind: t.Literal["archive", "delete", "freeze"],
    ) -> None:
        """Apply a minimal DataTable mutation for one lifecycle action.

        Avoids the visible flash that a full ``table.clear()`` + re-add
        would produce. Three paths:

        - **Delete or filter-out**: ``remove_row`` deletes the affected
          row in place; surrounding rows slide up without re-painting.
        - **Stays visible**: only the title cell changes (the new
          ``frozen`` / ``archived`` token gets added) — update that
          single cell with ``update_cell_at`` and leave the rest of the
          row alone.
        - **Cursor moves past the end**: clamp ``self._cursor`` to the
          new row count and re-anchor the table cursor; the search bar
          re-renders to pick up the new ``visible_count``.

        Falls back to a full ``_rebuild_rows`` + ``_render_all`` if the
        targeted row isn't found in the table — keeps the picker
        consistent if the row state ever drifts.
        """
        table = self.query_one("#session-table", DataTable)

        if kind == "delete":
            self._render_lifecycle_remove_row(table, session_id)
            return

        # Recompute whether the post-mutation row should still be shown
        # under the current filter. ``_apply_optimistic_local_update``
        # has already patched the underlying ``info`` object that the
        # row holds, so the existing row reference reflects the new state.
        row_index = next(
            (i for i, r in enumerate(self._rows) if r.session_id == session_id),
            None,
        )
        if row_index is None:
            self._rebuild_rows()
            self._render_all()
            return

        row = self._rows[row_index]
        parsed = _parse_search(self._search_query)
        still_visible = not self._skip_by_archive_filter(
            row.info, parsed
        ) and self._row_matches_filter(row, parsed)

        if not still_visible:
            self._render_lifecycle_remove_row(table, session_id)
            return

        # Stays visible — only the Title cell content changed (status
        # tokens). Title is column 0; ``update_cell_at`` keys by
        # coordinate so we don't have to thread column keys through.
        try:
            table.update_cell_at(
                Coordinate(row_index, 0),
                _title_cell(row.info, row.record),
                update_width=False,
            )
        except Exception:
            logger.opt(exception=True).debug(
                "Surgical title update failed; falling back to full re-render"
            )
            self._rebuild_rows()
            self._render_all()

    def _render_lifecycle_remove_row(self, table: DataTable, session_id: str) -> None:
        """Drop one row from the table and re-anchor the cursor.

        ``remove_row`` raises if the key isn't tracked — when that
        happens (a stale render or a row that wasn't materialized yet)
        we fall back to the full re-render so the table stays correct.
        """
        try:
            table.remove_row(session_id)
        except Exception:
            logger.opt(exception=True).debug(
                "Surgical row removal failed; falling back to full re-render"
            )
            self._rebuild_rows()
            self._render_all()
            return

        self._rows = [r for r in self._rows if r.session_id != session_id]
        self._cursor = min(self._cursor, max(0, len(self._rows) - 1))
        # Header carries the row count and the search bar carries the
        # cursor / visible-count text — both need a refresh. The table
        # itself doesn't get re-cleared.
        self._render_header()
        self._render_search()
        if self._rows:
            self._apply_cursor_to_table()

    # ── Data merge ───────────────────────────────────────────────────────

    def _rebuild_rows(self) -> None:
        """Recompute the merged row list from in-process + platform state,
        applying the current search filter and pinning the active row first.
        """
        parsed = _parse_search(self._search_query)

        # Union — in-process SessionRecord wins over platform SessionInfo
        # when the same session_id appears in both.
        unified: dict[str, _Row] = {}
        for sid, info in self._platform_rows.items():
            if self._skip_by_archive_filter(info, parsed):
                continue
            unified[sid] = _Row(session_id=sid, info=info, record=None)
        for sid, record in self._sessions.items():
            if self._skip_by_archive_filter(record.info, parsed):
                continue
            unified[sid] = _Row(session_id=sid, info=record.info, record=record)

        rows = list(unified.values())
        rows = [r for r in rows if self._row_matches_filter(r, parsed)]
        rows.sort(key=lambda r: r.sort_key, reverse=True)

        if self._active_session_id is not None:
            active_row = unified.get(self._active_session_id)
            if active_row is not None and self._row_matches_filter(active_row, parsed):
                rows = [active_row] + [r for r in rows if r.session_id != active_row.session_id]

        self._rows = rows
        self._cursor = min(self._cursor, max(0, len(self._rows) - 1))

    @staticmethod
    def _skip_by_archive_filter(info: SessionInfo, parsed: _ParsedSearch) -> bool:
        """Filter out rows whose archived state doesn't match the parsed
        archived tri-state. The platform already respects this param on
        the browse path, but in-process rows bypass that filter — we
        apply the same predicate here so the merged view stays coherent.
        """
        if parsed.archived == "any":
            return False
        is_archived = info.archived_at is not None
        if parsed.archived == "archived":
            return not is_archived
        # "active"
        return is_archived

    @staticmethod
    def _row_matches_filter(row: _Row, parsed: _ParsedSearch) -> bool:
        """Client-side free-text fallback for in-process rows.

        The platform `browse_sessions` call already applies `search` on
        its side, but in-process rows don't round-trip the platform on
        this path. Mirroring the free-text predicate here means typing
        in the search bar filters both sets consistently.

        Searches across the same signals the row visually presents —
        title, preview snippet (server or local transcript), session id,
        agent / capability / project — so a row that's findable on
        screen is also findable by typing what the user can see.
        """
        info = row.info
        if parsed.origin is not None:
            if info.origin != parsed.origin:
                return False
        if parsed.project is not None and info.project != parsed.project:
            return False
        if not parsed.free_text:
            return True
        needle = parsed.free_text.lower()
        haystack_parts: list[str] = [
            info.title or "",
            info.preview or "",
            info.session_id,
            info.agent or "",
            info.capability or "",
            info.project or "",
        ]
        if row.record is not None:
            for entry in row.record.transcript:
                if entry.role == "user" and entry.content:
                    haystack_parts.append(entry.content)
                    break  # first user message is enough for search
        return needle in " ".join(haystack_parts).lower()

    # ── Async platform load ──────────────────────────────────────────────

    def _reload_on_search_change(self) -> None:
        self._rebuild_rows()
        self._render_all()
        self._load_platform_page()

    @work(exclusive=True, group="session-browse")
    async def _load_platform_page(self) -> None:
        """Fetch the current filter's browse page + facets from the runtime.

        Single in-flight policy via ``exclusive=True`` — rapid search
        typing cancels stale fetches so the UI only ever reflects the
        latest query. The in-process view stays visible the whole time.
        """
        if self._managed_client is None:
            return
        parsed = _parse_search(self._search_query)
        browse_kwargs = parsed.browse_kwargs()
        try:
            envelope = await self._managed_client.browse_sessions(limit=50, **browse_kwargs)
        except Exception:
            logger.opt(exception=True).warning("Failed to browse platform sessions")
            return
        if not self.is_mounted:
            return
        self._platform_rows = {s.session_id: s for s in envelope.sessions}
        self._rebuild_rows()
        self._render_all()

    # ── Render ───────────────────────────────────────────────────────────

    def _render_all(self) -> None:
        self._render_header()
        self._render_search()
        self._render_table()
        self._render_hints()

    def _render_header(self) -> None:
        self.query_one("#session-header", Static).update(
            render_screen_header(
                "Sessions",
                "Browse and resume conversation sessions",
                count=len(self._rows),
            )
        )

    def _render_search(self) -> None:
        self.query_one("#session-search", Static).update(
            render_search_bar(
                self._search_query,
                cursor=self._cursor,
                visible_count=len(self._rows),
                placeholder=("Search…  filters: status:archived  origin:user  project:default"),
            )
        )

    def _render_table(self) -> None:
        table = self.query_one("#session-table", DataTable)
        table.clear()
        for row in self._rows:
            title_cell = _title_cell(row.info, row.record)
            agent = Text(
                row.info.agent or row.info.capability or "default",
                style=FG_SUBTLE,
            )
            model = _model_cell(row.record)
            msgs = _msgs_cell(row.info)
            tokens = _tokens_cell(row.info)
            project = Text(row.info.project or "-", style=FG_SUBTLE)
            labels = _labels_cell(row.info)
            updated = Text(
                _relative_time(row.info.updated_at or row.info.created_at),
                style=FG_SUBTLE,
                justify="right",
            )
            # Row height of 2 makes room for the muted preview line under
            # the title; rows without a preview leave the second line blank
            # so cursor movement and zebra striping stay even.
            table.add_row(
                title_cell,
                updated,
                agent,
                model,
                msgs,
                tokens,
                project,
                labels,
                key=row.session_id,
                height=2,
            )

        if self._rows:
            self._apply_cursor_to_table()

    def _apply_cursor_to_table(self) -> None:
        table = self.query_one("#session-table", DataTable)
        if 0 <= self._cursor < len(self._rows):
            table.move_cursor(row=self._cursor, column=0, animate=False, scroll=True)
            self._render_search()

    def _render_hints(self) -> None:
        hints: list[tuple[str, str]] = [
            ("Enter", "open"),
            ("^N", "new"),
            ("^O", "browser"),
            ("^X", "archive"),
            ("^L", "freeze"),
            ("^D", "delete"),
            ("Esc", "back"),
            ("Type", "search"),
        ]
        self.query_one("#session-hint-bar", Static).update(render_hint_bar(hints))

    # ── DataTable click / highlight wiring ───────────────────────────────

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        self._cursor = event.cursor_row
        self._render_search()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.row_key is None:
            return
        sid = str(event.row_key.value)
        self.dismiss(sid)
