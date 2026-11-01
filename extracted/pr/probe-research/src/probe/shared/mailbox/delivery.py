"""deliverers take waiting messages: claim one, log the claim, mark what was shown."""

from __future__ import annotations
import json
import os
import re
import time
from pathlib import Path
from probe.shared.mailbox.inbox_format import (
    TEXT_ALERT,
    TEXT_ANSWER,
    TEXT_FAILED,
    TEXT_INBOX_PERSON,
    TEXT_MESSAGE,
    TEXT_WRITER_FAILED,
    TEXT_WRITER_RECEIPT,
    TEXT_WRITER_RELAY,
    TEXT_WRITER_REPLY,
    WRITER_RELAY_PREFIX,
)


def shown_log_path(session_id: str) -> Path:
    """The messages a deliverer handed the agent (`mark_shown`)."""
    return claimed_dir(session_id) / "shown.jsonl"


def mark_shown(session_id: str, message_ids: "list[str]", *, by: str, now: "float | None" = None) -> None:
    """The deliverer's output carrying `message_ids` went out: one line each.
    Never raises (the handoff happened either way)."""
    if not message_ids:
        return
    at = time.time() if now is None else now
    path = shown_log_path(session_id)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as log:
            log.write("".join(json.dumps({"id": mid, "by": by, "at": at}) + "\n" for mid in message_ids))
    except OSError:
        pass


def waiting(session_id: str, *, now: "float | None" = None) -> list[tuple[Path, Message]]:
    """Messages waiting for delivery, oldest first; expired ones are skipped."""
    now = time.time() if now is None else now
    folder = messages_dir(session_id)
    out = []
    if not folder.is_dir():
        return out
    for path in sorted(folder.glob("*.json")):
        data = _read_json(path)
        msg = Message.from_dict(data) if data else None
        if msg is None or (msg.expires_at and msg.expires_at < now):
            continue
        out.append((path, msg))
    return out


def claim(session_id: str, path: Path, *, by: str, now: "float | None" = None,
          token: "str | None" = None) -> "Message | None":
    """Take one message for delivery. None when someone else took it first.

    `token`: the Probe service's claim for one request (`mailbox.claim`). The
    one rename then goes to `claimed/<stem>.<token>.json`: the claim and who it
    is for, together, so a caller that never got the service's answer (it
    stalled, or died a moment after) finds it by its token's name alone. The
    caller's receipt renames it to the plain name before it shows it."""
    if token is not None and not TOKEN.fullmatch(token):
        raise ValueError("a claim token is letters, digits and underscores")
    name = path.name if token is None else f"{path.name[: -len('.json')]}.{token}.json"
    dst = claimed_dir(session_id) / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    # A service claim's ledger line goes in right after the rename, before the
    # claimed file is read (a caller that gave up finds its claim there): what
    # the message is (its origin) is read from it first. A message file never
    # changes once written.
    origin = (_read_json(path) or {}).get("origin") if token else None
    try:
        os.rename(path, dst)
    except FileNotFoundError:
        return None
    if token:
        _log_claim(session_id, message_id_of(path), by, now, token, origin)  # the ledger, the id from the name
    data = _read_json(dst)
    msg = Message.from_dict(data) if data else None
    if not token:
        _log_claim(session_id, msg.id if msg else path.name, by, now, None, msg.origin if msg else None)
    return msg


def _log_claim(session_id: str, message_id: str, by: str, now: "float | None", token: "str | None",
               origin: object = None) -> None:
    entry = {"id": message_id, "by": by, "at": time.time() if now is None else now}
    if token:
        entry["token"] = token
    if isinstance(origin, str) and origin:
        entry["origin"] = origin  # a hint, the writer's (none: the reader's)
    try:
        with claim_log_path(session_id).open("a", encoding="utf-8") as log:
            log.write(json.dumps(entry) + "\n")
    except OSError:
        pass


#: Where a message a deliverer hands the agent starts: a `TEXT_*` up to its
#: first field, at the start of the text or after a blank line ("nothing found"
#: shares the answer's start). A hook joins its messages with a blank line,
#: after any other hook's context.
_DELIVERY_START = re.compile("(?:^|\n\n)(?:" + "|".join(
    re.escape(t.split("{", 1)[0]) for t in (TEXT_MESSAGE, TEXT_ANSWER, TEXT_FAILED, TEXT_ALERT, TEXT_WRITER_REPLY,
                                            TEXT_WRITER_RECEIPT, TEXT_WRITER_FAILED, TEXT_INBOX_PERSON,
                                            TEXT_WRITER_RELAY.format(message=WRITER_RELAY_PREFIX))) + ")")


def before_deliveries(text: str) -> str:
    """`text` up to the first message a deliverer handed the agent: what a hook's
    context held besides them. The daemon reads the messages themselves whole
    from the claim log, so a transcript's copy of them is not read again."""
    m = _DELIVERY_START.search(text)
    return text if m is None else text[:m.start()]


def claim_log_path(session_id: str) -> Path:
    """Every deliverer's record of what it took (the hooks, pi's extension,
    `probe ask --wait`): one `{"id", "by", "at"}` line per claim, append-only,
    with the message's `origin` when it has one (ORIGIN_HINT: a delivered hint)."""
    return claimed_dir(session_id) / "log.jsonl"


def claimed_ids(session_id: str) -> set[str]:
    """Ids of the messages a deliverer moved into `claimed/` (`<ns>-<id>.json`),
    until the sweep removes them (KEEP_CLAIMED_S)."""
    folder = claimed_dir(session_id)
    if not folder.is_dir():
        return set()
    return {message_id_of(path) for path in folder.glob("*.json")}


def claim_answer(session_id: str, ask_id: str, *, by: str = "probe ask --wait") -> "Message | None":
    """The waiting `probe ask --wait`'s own claim: the message that ends its ask."""
    for path, msg in waiting(session_id):
        if msg.ask == ask_id and msg.kind != Kind.MESSAGE:
            return claim(session_id, path, by=by)
    return None
from probe.shared.mailbox.layout import _read_json, claimed_dir, messages_dir  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.mailbox.mailbox import Kind, Message, TOKEN, message_id_of  # noqa: E402 -- pieces need each other; the front door loads this one first
