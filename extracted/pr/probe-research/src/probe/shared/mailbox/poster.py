"""the MessagePoster interface and publish(): idempotent by id, newest unasked/hint replaces the waiting one."""

from __future__ import annotations
from pathlib import Path
#: One unasked message per researcher turn -- and one more per this long of a
#: long turn (Richard 2026-09-28): a one-prompt autonomous session otherwise got
#: the reader's first message and none after it, corrections included.
UNASKED_WINDOW_S = 10 * 60
#: The turn's delivery slot files the hooks create (`turns/<sid>.<slot>-<token>-
#: <window>`): one for the reader's unasked message, one for a hint, so one of
#: each can go out in the same turn (and window).
SLOT_UNASKED = "unasked"
SLOT_HINT = "hint"


def publish(msg: Message) -> Path:
    """Put `msg` in the session's mailbox: through the Probe service when one
    answers (`post_via_service`), else here (`publish_here`); the same file
    either way. Idempotent by id: a message already published (waiting or
    claimed) is not written twice. A new UNASKED message of the reader's
    replaces any unasked one of the reader's still waiting, and a new hint any
    hint still waiting: only the newest of each goes out, and neither ever
    replaces the other (a `keep` message neither replaces nor is replaced, nor
    does a run alert, and the writer's receipts are each a record of their own)."""
    if not msg.expires_at:
        msg.expires_at = msg.made_at + _ttl(msg)
    if post_via_service(msg):
        name = _file_name(msg)
        done = claimed_dir(msg.session) / name
        return done if done.exists() else messages_dir(msg.session) / name
    return publish_here(msg)


def _made_at(data: dict) -> float:
    try:
        return float(data.get("made_at") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _slot(data: dict) -> "str | None":
    """Which slot a message waits in -- SLOT_UNASKED for the reader's own unasked
    message, SLOT_HINT for a hint: a newer message in the same slot replaces it,
    it goes stale, and the hooks deliver one of each a turn -- or None (an
    answer, a run alert, a `keep` message, a writer's receipt: nothing replaces it)."""
    if data.get("kind") != Kind.MESSAGE or data.get("keep") or data.get("origin") in (ORIGIN_WRITER, ORIGIN_INBOX):
        return None
    return SLOT_HINT if data.get("origin") == ORIGIN_HINT else SLOT_UNASKED


def withdraw_unasked(session_id: str, *, made_before: float) -> int:
    """Remove the unasked messages still waiting that were made before
    `made_before` (an answer's ask time). The reader wrote that answer with its
    earlier message in the same conversation, so the two would arrive in one
    hook as a repeat (live end-to-end test, 2026-09-29) -- the same rule as a
    newer unasked message replacing one not yet delivered. Never a hint: the
    reader did not write it. Returns how many."""
    removed = 0
    for path, msg in waiting(session_id):
        if (msg.kind == Kind.MESSAGE and not msg.keep and not msg.from_writer and not msg.from_hint
                and not msg.from_inbox and msg.made_at < made_before):
            try:
                path.unlink()
            except FileNotFoundError:
                continue  # a hook delivered it first
            removed += 1
    return removed
from probe.shared.mailbox.delivery import waiting  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.mailbox.layout import claimed_dir, messages_dir  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.mailbox.mailbox import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    Kind,
    Message,
    ORIGIN_HINT,
    ORIGIN_INBOX,
    ORIGIN_WRITER,
    _file_name,
    _ttl,
)
from probe.shared.mailbox.posters.local import publish_here  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.mailbox.posters.service import post_via_service  # noqa: E402 -- pieces need each other; the front door loads this one first
