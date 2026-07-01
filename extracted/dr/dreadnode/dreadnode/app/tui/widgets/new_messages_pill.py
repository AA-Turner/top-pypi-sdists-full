"""Floating indicator that appears when new transcript content arrives while the
user is scrolled up reading earlier messages.

Lives as a sibling of :class:`ConversationView` in ``#main-body`` so it takes
one row of vertical space between the conversation and the tool-progress row
when visible, and disappears completely otherwise.

The count tracks specific widget references rather than a raw integer, so as
the user scrolls down past unread messages the counter decrements per message
— matching Slack/Discord "unread pill" behavior. A message is considered read
once its last widget's top edge has entered the viewport from below. We use
"entered the viewport" rather than "passed above the top" because new
messages arrive at the *end* of the transcript — there is nothing below them
to push them above the top as the user scrolls, so the "passed above top"
semantic would never decrement for new arrivals.

Click posts :class:`NewMessagesPill.Jump` which the app handles by scrolling
the conversation to the end.
"""

import typing as t
from collections import deque

from rich.text import Text
from textual import events
from textual.css.query import NoMatches
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Static

from dreadnode.app.tui.theme import ACCENT, BG_LIGHT, BG_LIGHTER, FG_FAINTEST, FG_SUBTLE

if t.TYPE_CHECKING:
    from dreadnode.app.tui.widgets.conversation import ConversationView


class NewMessagesPill(Static):
    """Jump-to-bottom indicator shown while the user is scrolled up, with
    per-message unread tracking that decrements as the user scrolls down.
    """

    DEFAULT_CSS = f"""
    NewMessagesPill {{
        display: none;
        height: 1;
        padding: 0 2;
        content-align: center middle;
        text-align: center;
        color: {FG_SUBTLE};
        background: {BG_LIGHT};
    }}
    NewMessagesPill.-visible {{
        display: block;
    }}
    NewMessagesPill:hover {{
        background: {BG_LIGHTER};
    }}
    """

    class Jump(Message):
        """Posted when the user clicks the pill."""

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__("", **kwargs)
        # Oldest-first queue of "end-of-message" marker widgets. A message is
        # read once its marker's bottom edge has passed above the viewport.
        self._unread: deque[Widget] = deque()

    def on_mount(self) -> None:
        # Decrement the counter as the user scrolls past unread messages.
        # We look up the ConversationView by id rather than importing the
        # class here to avoid a circular import at module load time.
        conv = self._conversation()
        if conv is not None:
            self.watch(conv, "scroll_y", self._on_conv_scroll_y, init=False)

    def _conversation(self) -> "ConversationView | None":
        try:
            from dreadnode.app.tui.widgets.conversation import ConversationView

            return self.app.query_one("#conversation", ConversationView)
        except NoMatches:
            return None

    def _on_conv_scroll_y(self, _new_y: float) -> None:
        # The scroll_y reactive fires *before* layout propagates, so child
        # widget regions still report pre-scroll positions. Defer the
        # geometry check until after the refresh so we see the post-layout
        # regions and decrement against accurate coordinates.
        self.call_after_refresh(self._recompute_unread)

    def _recompute_unread(self) -> None:
        conv = self._conversation()
        if conv is None:
            return
        self.mark_read_entered(conv.region.y + conv.size.height)

    @property
    def count(self) -> int:
        return len(self._unread)

    def bump(self, widget: Widget | None = None) -> None:
        """Record a new unread message.

        ``widget`` should be the last widget produced when rendering the
        message — that's the widget we use to decide when the whole message
        has scrolled above the viewport. A ``None`` widget falls back to a
        pure counter bump (useful in focused tests).
        """
        if widget is not None:
            self._unread.append(widget)
        else:
            # Legacy counter-only path — push a sentinel so len() still grows.
            self._unread.append(_SENTINEL)
        self._render_label()
        self.add_class("-visible")

    def mark_read_entered(self, viewport_bottom_y: int) -> None:
        """Pop unread markers whose widgets have entered the viewport from below.

        ``viewport_bottom_y`` is the screen-space y coordinate of the bottom
        edge of the scroll viewport. A widget is "entered" when its top edge
        is at or above that line — i.e. the user has scrolled far enough down
        that the message has started to appear. Oldest-first ordering lets us
        stop at the first marker that hasn't entered yet.
        """
        if not self._unread:
            return
        changed = False
        while self._unread:
            marker = self._unread[0]
            if marker is _SENTINEL:
                # Counter-only marker — no geometry to evaluate.
                break
            if marker.region.y <= viewport_bottom_y:
                self._unread.popleft()
                changed = True
                continue
            break
        if not changed:
            return
        if not self._unread:
            self.remove_class("-visible")
            self.update("")
        else:
            self._render_label()

    def reset(self) -> None:
        """Clear all unread markers and hide the pill."""
        if not self._unread and not self.has_class("-visible"):
            return
        self._unread.clear()
        self.remove_class("-visible")
        self.update("")

    def _render_label(self) -> None:
        count = len(self._unread)
        noun = "message" if count == 1 else "messages"
        text = Text()
        text.append("↓ ", style=ACCENT)
        text.append(f"{count} new {noun}", style=FG_SUBTLE)
        text.append("  ·  click or press G to jump", style=FG_FAINTEST)
        self.update(text)

    def on_click(self, event: events.Click) -> None:
        event.stop()
        self.post_message(self.Jump())


# Sentinel used when a caller bumps without providing a widget. Keeps the
# pill usable as a pure counter in isolation tests; stops geometry-based
# decrement at the first sentinel encountered.
_SENTINEL: Widget = t.cast("Widget", object())
