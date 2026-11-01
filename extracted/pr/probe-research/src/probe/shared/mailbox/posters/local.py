"""write the message file in this process (the service's own post, or the fallback)."""

from __future__ import annotations
from dataclasses import asdict
from pathlib import Path


def publish_here(msg: Message) -> Path:
    """`publish`, writing the file in this process (the service's own post)."""
    if not msg.expires_at:
        msg.expires_at = msg.made_at + _ttl(msg)
    folder = messages_dir(msg.session)
    name = _file_name(msg)
    # Published already? Looked for where a message can be, in the order it
    # moves there (waiting -> a service claim for a caller -> received or
    # claimed): a move between two looks lands where the next one looks, so a
    # claim's receipt racing this retry is always seen (Codex P2, 90f86ead6).
    if (folder / name).exists():
        return folder / name
    for done in claimed_dir(msg.session).glob(f"{name[: -len('.json')]}.*.json"):
        return done  # claimed by the service for a caller, its receipt pending
    if (claimed_dir(msg.session) / name).exists():
        return claimed_dir(msg.session) / name
    slot = _slot(asdict(msg))
    if slot is not None and folder.is_dir():
        same = [(other, data) for other in folder.glob("*.json")
                if (data := _read_json(other)) and _slot(data) == slot and data.get("id") != msg.id]
        if any(_made_at(data) > msg.made_at for _other, data in same):
            # A newer one of its slot waits (hints come from several triggers at
            # once, and a slow lookup lands late): this one is out of date already,
            # and is never written. Past the service's deadline it says nothing
            # either way: its caller decides, by this same rule.
            check_deadline()
            return folder / name
        for other, _data in same:
            # The service's step: past its deadline its caller writes this
            # message, and may have written a newer one since: delete nothing.
            check_deadline()
            other.unlink(missing_ok=True)
    _write_json(folder / name, asdict(msg))
    return folder / name
from probe.shared.mailbox.layout import _read_json, _write_json, check_deadline, claimed_dir, messages_dir  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.mailbox.mailbox import Message, _file_name, _ttl  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.mailbox.poster import _made_at, _slot  # noqa: E402 -- pieces need each other; the front door loads this one first
