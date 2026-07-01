"""Conversation view — single scrollable stream.

Design: Clear visual hierarchy with breathing room between messages.
  > user message (orange, bold prompt)
  assistant markdown (primary content, flows naturally)
  · tool_name (dim, compact — tools are implementation detail)
  · system info (dim)

The conversation is a ``list[Message]`` — the SDK's canonical message
shape from :mod:`dreadnode.generators.message`. The TUI-only row kinds
(thinking blocks, inline error notices, compaction dividers) ride on
``Message.metadata`` flags so the transcript stays a real message list
from the LLM's perspective while still supporting the view-layer
annotations the TUI needs. The dispatch rules live in
:func:`_render_message` below.
"""

import asyncio
import time
import typing as t

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.message import Message as TextualMessage
from textual.widget import Widget
from textual.widgets import Markdown, Static

from dreadnode.app.tui.theme import ACCENT, ERROR, FG, FG_FAINTEST, FG_MUTED, FG_SUBTLE
from dreadnode.app.tui.widgets.tool import ToolCall
from dreadnode.generators.message import Message

# =============================================================================
# Metadata conventions
# =============================================================================
#
# TUI-specific annotations on Message rides on ``metadata`` so the list
# stays a normal LLM message list. Keys used:
#
#   - ``thinking``: bool — render as collapsible ThinkingBlock
#   - ``shell``: bool — user row is a shell command echo ("$ cmd")
#   - ``error``: bool — row is an error notice (role=system)
#   - ``error_title``: str — title shown in error rows ("agent", "tool", ...)
#   - ``compaction``: bool — row is a compaction divider (role=system)
#   - ``retry``: bool — row is a retry notice (role=system)
#   - ``tool_name``: str — tool label (role=tool)
#   - ``tool_args``: dict — tool arguments for label formatting (role=tool)
#   - ``summary``: str — one-line tool result summary shown as meta
#   - ``expanded_detail``: str — full detail text shown in compaction rows


def _meta(message: Message, key: str, default: t.Any = None) -> t.Any:
    return message.metadata.get(key, default)


def _is_thinking(message: Message) -> bool:
    return message.role == "assistant" and bool(_meta(message, "thinking"))


def _is_error(message: Message) -> bool:
    return message.role == "system" and bool(_meta(message, "error"))


def _is_compaction(message: Message) -> bool:
    return message.role == "system" and bool(_meta(message, "compaction"))


def _message_css_class(message: Message) -> str:
    """CSS class suffix matching the legacy ``TranscriptEntry.kind`` values.

    The stylesheet targets ``.user-entry``, ``.assistant-entry``,
    ``.tool-entry``, ``.error-entry``, ``.thinking-entry``, ``.system-entry``
    — preserve those class names so no CSS needs to change.
    """
    if _is_thinking(message):
        return "thinking-entry"
    if _is_error(message):
        return "error-entry"
    if _is_compaction(message):
        return "system-entry"
    if message.role == "tool":
        return "tool-entry"
    return f"{message.role}-entry"


class ThinkingBlock(Widget):
    """Collapsible thinking/reasoning block — follows app.output_mode at render time."""

    DEFAULT_CSS = """
    ThinkingBlock {
        height: auto;
        margin: 0;
        padding: 0;
    }
    """

    def __init__(self, *, body: str, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)
        self._body = body

    def on_mount(self) -> None:
        try:
            self.display = self.app.output_mode == "expanded"  # type: ignore[attr-defined]
        except Exception:
            self.display = False

    def render(self) -> Text:
        text = Text()
        lines = self._body.splitlines()
        for i, line in enumerate(lines):
            if i > 0:
                text.append("\n")
            text.append("  │ ", style=FG_FAINTEST)
            text.append(line, style=FG_FAINTEST)
        return text


class CompactionSummary(Widget):
    """Expandable compaction summary — hidden in compact mode, visible in expanded."""

    DEFAULT_CSS = """
    CompactionSummary {
        height: auto;
        margin: 0;
        padding: 0;
    }
    """

    def __init__(self, *, body: str, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)
        self._body = body

    def on_mount(self) -> None:
        try:
            self.display = self.app.output_mode == "expanded"  # type: ignore[attr-defined]
        except Exception:
            self.display = False

    def render(self) -> Text:
        text = Text()
        lines = self._body.splitlines()
        for i, line in enumerate(lines):
            if i > 0:
                text.append("\n")
            text.append("  │ ", style=FG_FAINTEST)
            text.append(line, style=FG_FAINTEST)
        return text


def _render_message(message: Message) -> list[t.Any]:
    """Render a :class:`Message` as one or more Rich/Textual renderables.

    Dispatches on ``role`` plus the TUI-specific metadata flags so all
    the legacy row kinds (user/assistant/system/tool/error/thinking
    /compacted/retry) keep working without a custom dataclass.
    """
    content = message.content or ""

    # Thinking block — an assistant message flagged with metadata.thinking
    if _is_thinking(message):
        return [ThinkingBlock(body=content)]

    # Error rows — a system message flagged with metadata.error
    if _is_error(message):
        title = _meta(message, "error_title") or "error"
        text = Text()
        text.append("✗ ", style=ERROR)
        text.append(title, style=f"bold {ERROR}")
        if content:
            text.append(f" — {content}", style=ERROR)
        return [text]

    # Compaction divider — a system message flagged with metadata.compaction
    if _is_compaction(message):
        text = Text()
        text.append("── ", style=FG_FAINTEST)
        text.append(content, style=FG_MUTED)
        text.append(" ──", style=FG_FAINTEST)
        items: list[t.Any] = [text]
        expanded = _meta(message, "expanded_detail")
        if expanded:
            items.append(CompactionSummary(body=expanded))
        return items

    if message.role == "user":
        text = Text()
        text.append("› ", style=f"bold {ACCENT}")
        text.append(content, style=FG)
        return [text]

    if message.role == "assistant":
        return [Markdown(content or "_(empty)_", classes="entry assistant-entry")]

    if message.role == "tool":
        # Tool label is computed at render time from (name, args) so we
        # don't duplicate formatted state on the message itself.
        from dreadnode.app.tui.tool_format import _format_tool_label

        tool_name = _meta(message, "tool_name") or "tool"
        tool_args = _meta(message, "tool_args") or {}
        label = _format_tool_label(tool_name, tool_args)
        summary = _meta(message, "summary")
        error = _meta(message, "error")
        report_url = _meta(message, "report_url") or None
        expanded_body: str | None = None
        expanded_body_format: str | None = None
        if tool_name == "report":
            content_arg = tool_args.get("content")
            expanded_body = content_arg if isinstance(content_arg, str) else None
            format_arg = tool_args.get("format")
            expanded_body_format = format_arg if isinstance(format_arg, str) else "markdown"
        return [
            ToolCall(
                name=label,
                details=content.strip(),
                meta=summary,
                error=error,
                url=report_url,
                expanded_body=expanded_body,
                expanded_body_format=expanded_body_format,
                classes="entry tool-entry",
            )
        ]

    # role="system" fallback (includes retry rows etc.)
    text = Text()
    text.append("· ", style=FG_FAINTEST)
    text.append(content, style=FG_FAINTEST)
    return [text]


class ConversationView(VerticalScroll):
    """Main chat area — single scrollable stream.

    Everything lives here: messages, tool calls, streaming text, activity.
    StreamingDraft is mounted as the last child so streaming text appears
    right after the latest message with no gap.
    """

    class FollowingChanged(TextualMessage):
        """Posted when the user transitions between following the stream and scrolled-up."""

        def __init__(self, following: bool) -> None:
            self.following = following
            super().__init__()

    class HiddenAppend(TextualMessage):
        """Posted when content is appended while the user is not at the bottom.

        ``widget`` is the last widget produced for the message — used as the
        "end-of-message" marker so the unread pill can decide when the whole
        message has scrolled past the top of the viewport.
        """

        def __init__(self, widget: Widget | None = None) -> None:
            self.widget = widget
            super().__init__()

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)
        self._prev_following = True
        # Perf telemetry — counts virtual_size growth events between
        # ``perf_snapshot_and_reset`` calls. Each event triggers a reflow
        # via ``scroll_end`` while following, so a per-turn delta tells us
        # how thrashy streaming + tool mounts are at current DOM size.
        self._perf_vsize_changes = 0

    def perf_snapshot_and_reset(self) -> tuple[int, int]:
        """Return (entry_widget_count, virtual_size_changes_since_last_call).

        Entry count excludes the streaming draft so it tracks the DOM
        cost that grows with session length.
        """
        try:
            entries = sum(1 for _ in self.query(".entry"))
        except Exception:
            entries = len(self.children)
        vsize = self._perf_vsize_changes
        self._perf_vsize_changes = 0
        return entries, vsize

    def compose(self) -> ComposeResult:
        """Compose the content of the conversation view."""
        yield StreamingDraft(id="draft", classes="-empty")

    def on_mount(self) -> None:
        # Watch our own scroll position so the app can react to the user
        # entering/leaving "following" state without polling.
        self.watch(self, "scroll_y", self._on_scroll_y_changed, init=False)
        # Watch virtual_size so the streaming draft can stay pinned to the
        # bottom as tokens arrive — Markdown content growth doesn't reliably
        # fire Resize on the draft itself, but it always grows virtual_size
        # here.
        self.watch(self, "virtual_size", self._on_virtual_size_changed, init=False)

    def _on_virtual_size_changed(self, _new_size: t.Any) -> None:
        """Stay pinned to the bottom while the user is following.

        Layout can grow ``virtual_size`` across multiple refresh cycles
        (Markdown widgets re-measure, streaming tokens arrive, etc.), so a
        one-shot ``scroll_end`` from ``load_session``/``append_entry`` can
        miss the final height. Re-pinning on every growth keeps the user
        glued to the bottom until they scroll away themselves.
        """
        self._perf_vsize_changes += 1
        if self._prev_following:
            self.scroll_end(animate=False)

    def _on_scroll_y_changed(self, _new_y: float) -> None:
        now_following = self.is_following
        if now_following != self._prev_following:
            self._prev_following = now_following
            # Sync the streaming draft's follow flag *synchronously* so any
            # in-flight deferred scroll-to-end (scheduled from the draft's
            # on_resize) sees the user's new state before it runs. Posting
            # FollowingChanged alone isn't enough — message handlers dispatch
            # after call_after_refresh, which lets a stale scroll clobber a
            # user-initiated scroll-up.
            try:
                draft = self.query_one("#draft", StreamingDraft)
            except NoMatches:
                pass
            else:
                draft.set_follow(now_following)
            self.post_message(self.FollowingChanged(now_following))

    @property
    def is_following(self) -> bool:
        """True when the view is at (or near) the bottom — i.e. the user is "following" the stream.

        Callers should snapshot this *before* mutating content, because Textual's
        reflow extends ``max_scroll_y`` after a mount/update. Checking afterwards
        would misread a following user as having scrolled up.
        """
        if self.max_scroll_y <= 0:
            return True
        return self.scroll_y >= self.max_scroll_y - 2

    def show_empty(self) -> None:
        """Show an empty-state hint."""
        self._remove_entries()
        if self.query("#empty-hint"):
            return
        hint = Text()
        hint.append("Type a message, ", style=FG_MUTED)
        hint.append("/help", style=ACCENT)
        hint.append(", or ", style=FG_MUTED)
        hint.append("?", style=ACCENT)
        hint.append(" to get started.", style=FG_MUTED)
        self.mount(Static(hint, id="empty-hint", classes="entry"))

    def load_session(self, messages: list[Message]) -> None:
        """Replace the conversation with the given messages."""
        self._remove_entries()
        if not messages:
            self.show_empty()
            return
        widgets: list[Static | Markdown | ToolCall | ThinkingBlock | CompactionSummary] = []
        for message in messages:
            css_class = _message_css_class(message)
            for item in _render_message(message):
                if isinstance(item, (Markdown, ToolCall, ThinkingBlock, CompactionSummary)):
                    widgets.append(item)
                else:
                    widgets.append(Static(item, classes=f"entry {css_class}"))
        try:
            draft = self.query_one("#draft")
            self.mount_all(widgets, before=draft)
        except NoMatches:
            self.mount_all(widgets)
        # A fresh session always lands at the bottom, even if the previous
        # session left the view scrolled up. The virtual_size watcher will
        # re-pin as layout settles.
        self._prev_following = True
        self.call_after_refresh(self.scroll_end, animate=False)

    def append_entry(self, message: Message, *, scroll: bool = True) -> None:
        """Add a single message to the stream."""
        # Remove empty-state hint if present
        for w in self.query("#empty-hint"):
            w.remove()
        css_class = _message_css_class(message)
        widgets: list[Static | Markdown | ToolCall | ThinkingBlock | CompactionSummary] = []
        for item in _render_message(message):
            if isinstance(item, (Markdown, ToolCall, ThinkingBlock, CompactionSummary)):
                widgets.append(item)
            else:
                widgets.append(Static(item, classes=f"entry {css_class}"))
        was_at_bottom = self.is_following
        try:
            draft = self.query_one("#draft")
            self.mount_all(widgets, before=draft)
        except NoMatches:
            self.mount_all(widgets)
        if scroll and was_at_bottom:
            self.call_after_refresh(self.scroll_end, animate=False)
        elif not was_at_bottom:
            self.post_message(self.HiddenAppend(widgets[-1] if widgets else None))

    def append_entry_widget(self, widget: Static | ToolCall, *, scroll: bool = True) -> None:
        """Mount a pre-built widget into the conversation stream."""
        for w in self.query("#empty-hint"):
            w.remove()
        was_at_bottom = self.is_following
        try:
            self.mount(widget, before=self.query_one("#draft"))
        except NoMatches:
            self.mount(widget)
        if scroll and was_at_bottom:
            self.call_after_refresh(self.scroll_end, animate=False)
        elif not was_at_bottom:
            self.post_message(self.HiddenAppend(widget))

    def write(self, renderable: t.Any) -> None:
        """Write a renderable to the stream."""
        widget = Static(renderable, classes="entry")
        was_at_bottom = self.is_following
        try:
            self.mount(widget, before=self.query_one("#draft"))
        except NoMatches:
            self.mount(widget)
        if was_at_bottom:
            self.call_after_refresh(self.scroll_end, animate=False)
        else:
            self.post_message(self.HiddenAppend(widget))

    def write_system(self, message: str, *, style: str = FG_FAINTEST) -> None:
        """Write an inline system/activity message."""
        text = Text()
        text.append("· ", style=style)
        text.append(message, style=style)
        self.write(text)

    def write_activity(self, message: str) -> None:
        """Write a removable activity indicator (replaces any existing one)."""
        text = Text()
        text.append("· ", style=FG_SUBTLE)
        text.append(message, style=FG_SUBTLE)
        existing = self.query("#inline-activity")
        if existing:
            existing.first(Static).update(text)
            return
        widget = Static(text, id="inline-activity", classes="entry")
        was_at_bottom = self.is_following
        try:
            self.mount(widget, before=self.query_one("#draft"))
        except NoMatches:
            self.mount(widget)
        if was_at_bottom:
            self.call_after_refresh(self.scroll_end, animate=False)

    def clear_activity(self) -> None:
        """Remove the activity indicator if present."""
        for w in self.query("#inline-activity"):
            w.remove()

    def _remove_entries(self) -> None:
        """Remove all entry widgets, keeping StreamingDraft."""
        for child in list(self.query(".entry")):
            child.remove()


class StreamingDraft(Markdown):
    """Live streaming markdown preview.

    Background streams are stopped via :meth:`_schedule_stop` rather than
    via fire-and-forget ``asyncio.ensure_future`` calls. The previous
    implementation lost the cleanup task reference (so the stop coroutine
    could be garbage-collected mid-flight) and silently swallowed any
    exception raised by ``MarkdownStream.stop()``. The new path keeps every
    in-flight stop in :attr:`_pending_stops` so the event loop holds a
    strong reference, attaches a done callback that logs failures, and
    discards finished tasks from the set automatically.
    """

    DEFAULT_CSS = f"""
    StreamingDraft {{
        display: none;
        height: auto;
        padding: 0;
        margin: 0;
        color: {FG_SUBTLE};
    }}
    StreamingDraft.-active {{
        display: block;
        margin-top: 1;
    }}
    StreamingDraft.-empty {{
        display: none;
    }}
    """

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__("", **kwargs)
        self._stream: t.Any | None = None
        self._buffer = ""
        self._pending_stops: set[asyncio.Task[None]] = set()
        # When True, append_token asks the enclosing ConversationView to keep
        # its viewport pinned to the bottom so the user sees tokens arrive in
        # real time. Snapshotted at stream start; flipped by the app when the
        # user actively scrolls during a stream.
        self._follow = False
        # Perf telemetry — synchronous wall-time of each append_token call
        # (microseconds). The async MarkdownStream.write runs separately,
        # but the sync portion (buffer concat + task creation + any
        # bookkeeping) is what blocks the event loop turn; if it grows
        # with session length we want to see it.
        self._perf_token_us: list[float] = []

    def _conversation(self) -> "ConversationView | None":
        """Walk up to the enclosing ConversationView, or None if detached."""
        node: t.Any = self.parent
        while node is not None:
            if isinstance(node, ConversationView):
                return node
            node = node.parent
        return None

    def set_follow(self, following: bool) -> None:
        """Update the follow flag — called by the app when the user scrolls."""
        self._follow = following

    def _schedule_stop(self, stream: t.Any) -> None:
        """Schedule a previous stream's ``stop()`` and track its task.

        The set keeps the task alive until completion so it can't be GC'd
        mid-stop, and the done callback ensures any exception raised inside
        the stop coroutine is logged rather than silently swallowed.
        """
        try:
            task = asyncio.create_task(self._safe_stop(stream))
        except RuntimeError:
            # No running event loop (e.g. teardown). Best-effort: nothing
            # we can do, the stream will be GC'd along with the widget.
            return
        self._pending_stops.add(task)
        task.add_done_callback(self._pending_stops.discard)

    async def _safe_stop(self, stream: t.Any) -> None:
        """Await ``stream.stop()``, swallowing only the *exception value*.

        Logs any failure with traceback so the silent-swallow bug can't
        recur. Cancellation is silent — it only happens during widget
        teardown when nothing useful can be done about it.
        """
        try:
            await stream.stop()
        except asyncio.CancelledError:
            raise
        except Exception:
            from loguru import logger

            logger.opt(exception=True).debug(
                "StreamingDraft: error stopping previous markdown stream"
            )

    def start_stream(self) -> None:
        """Begin a new streaming response.

        Any previous stream is detached *before* the new one is created so
        the new ``self._stream`` reference is unambiguously the active one
        from this point forward. The detached stream's ``stop()`` runs as
        a tracked background task via :meth:`_schedule_stop`.
        """
        if self._stream is not None:
            old_stream = self._stream
            self._stream = None
            self._schedule_stop(old_stream)
        self._buffer = ""
        self._stream = self.get_stream(self)
        self.remove_class("-empty")
        self.add_class("-active")
        # Snapshot "following" at stream start: if the user was at the bottom
        # when the stream began, keep them pinned to the bottom as tokens
        # arrive. Otherwise they were reading back — leave them alone.
        conv = self._conversation()
        self._follow = conv.is_following if conv is not None else False

    def append_token(self, text: str) -> None:
        """Append a token — MarkdownStream batches re-renders automatically."""
        start_ns = time.perf_counter_ns()
        if self._stream is None:
            self.start_stream()
        self._buffer += text
        if self._stream is not None:
            try:
                task = asyncio.create_task(self._stream.write(text))
            except RuntimeError:
                self._perf_token_us.append((time.perf_counter_ns() - start_ns) / 1000.0)
                return
            # The write task is fire-and-forget per token; failures are
            # silent because a single dropped token isn't worth alerting
            # on, but the task is still kept alive via _pending_stops to
            # prevent premature GC.
            self._pending_stops.add(task)
            task.add_done_callback(self._pending_stops.discard)
        self._perf_token_us.append((time.perf_counter_ns() - start_ns) / 1000.0)

    def perf_snapshot_and_reset(self) -> tuple[int, float, float, float]:
        """Return (count, p50_us, p95_us, max_us) since last call, then reset.

        Times are the synchronous wall-time of :meth:`append_token`.
        Returns zeros when no tokens have been observed.
        """
        samples = self._perf_token_us
        self._perf_token_us = []
        if not samples:
            return 0, 0.0, 0.0, 0.0
        samples_sorted = sorted(samples)
        n = len(samples_sorted)
        p50 = samples_sorted[n // 2]
        # ceil-style p95 index, clamped to last element
        p95 = samples_sorted[min(n - 1, int(n * 0.95))]
        return n, p50, p95, samples_sorted[-1]

    def finish_stream(self) -> str:
        """End the stream and return accumulated text."""
        content = self._buffer
        if self._stream is not None:
            old_stream = self._stream
            self._stream = None
            self._schedule_stop(old_stream)
        return content

    def clear_stream(self) -> None:
        """Reset to empty idle state."""
        if self._stream is not None:
            old_stream = self._stream
            self._stream = None
            self._schedule_stop(old_stream)
        self._buffer = ""
        self.update("")
        self.add_class("-empty")
        self.remove_class("-active")

    def set_buffer(self, text: str) -> None:
        """Project stored draft text into the widget without opening a live stream."""
        if self._stream is not None:
            old_stream = self._stream
            self._stream = None
            self._schedule_stop(old_stream)
        self._buffer = text
        if not text:
            self.update("")
            self.add_class("-empty")
            self.remove_class("-active")
            return
        self.update(text)
        self.remove_class("-empty")
        self.add_class("-active")
