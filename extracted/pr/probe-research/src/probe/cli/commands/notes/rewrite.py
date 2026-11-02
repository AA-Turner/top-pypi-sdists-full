"""rewrite a note's text safely: version-pinned replace with retries, unconfirmed writes settled by reading back, cap refusals before sending."""

from __future__ import annotations
import sys
import uuid
import textwrap
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ....sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

import typer

from .... import errors


#: What a server's 422 says when a note is over its cap (`_notes_write`).
#: Unit-free on purpose: the number in front of each changed from characters
#: to tokens (research-os P2) and both spellings are live during a rollout.
_CAP_REFUSALS = ("notes limit", "sub-note body exceeds the")


def _notes_write(kind: str, label: str, write):
    """Run a notes write; on a CAP REFUSAL, add the advice the 422 cannot carry.

    The 422 says "this run note would exceed the 1,000-token notes limit" (or,
    for a note already over a lowered cap, "this note is over the 1,000-token
    notes limit and must be rewritten under it ...") and stops. That is the moment a writer most needs to know what to do, and it is
    the one path that never reaches `_report_notes_headroom` -- the advice rides
    the SUCCESS response, and there is no success. So the wall used to be the
    least informative state in the whole feature.

    Matched on the server's own wording rather than on the status code, because
    `Client.write` raises RosError for every 4xx and only this one means "the
    document is closed until you compact it". `_CAP_REFUSALS` holds the
    phrases, which every server says whatever the unit: "notes limit" in the
    entity 422 (older servers: "the 4000-character notes limit" or "the
    30,000-token notes limit"; current ones: "the 1,000-token notes limit", or
    the character backstop's) and the sub-note body 422's own sentence.
    """
    from ....sdk.reads.notes_cap import full_note_message

    try:
        return write()
    except errors.RosError as exc:
        if not any(phrase in str(exc) for phrase in _CAP_REFUSALS):
            raise
        print(f"error: {exc}", file=sys.stderr)
        for line in textwrap.wrap(full_note_message(kind, label), width=76):
            print(f"       {line}", file=sys.stderr)
        raise typer.Exit(1) from exc


# ------------------------------------------------- notes append / edit, no file
#
# The file model (checkout, edit, push) needs a file system and a second step. An
# agent that can only pass arguments -- the dashboard assistant, a sandboxed tool
# -- adds or corrects a note with these two instead. The text is ALWAYS literal:
# no `@file`, no `-` for stdin, so a command can never send a file it names.
#
# The server has no append or span edit any more (0.388.0.0), so both read the
# note, change its text here, and replace it pinned to the version they read
# (`base_version`, the `notes push` contract). If someone wrote in between, the
# server refuses with 409 and the change is applied again to the new text.

#: Reads-and-retries before giving up on a note that keeps moving. Each attempt
#: is a fresh read, so this runs out only under a continuous stream of writes.
_NOTE_REWRITE_ATTEMPTS = 5


def _note_carrier(
    c: Client,
    *,
    project: str | None,
    experiment: str | None,
    run: str | None,
    note: str | None,
) -> tuple[str, str, str | None, str]:
    """(kind, entity id, sub-note id or None, label) for a text-only write."""
    kind, entity_id, label = _note_target(
        c, project=project, experiment=experiment, run=run
    )
    if note is None:
        return kind, entity_id, None, label
    try:
        found = _resolve_sub_note_by_title(c, kind, entity_id, note)
    except errors.RosError as exc:
        _sub_notes_supported(exc)
        raise
    return kind, entity_id, found["id"], f"{label} › {note}"


def _send_note(
    c: Client, kind: str, entity_id: str, sub_id: str | None, text: str, version: int
) -> dict | None:
    """Replace one note pinned to `version`: the main note, or a sub-note by id."""
    op_key = uuid.uuid4().hex
    if sub_id is not None:
        return c._replace_sub_note(sub_id, text, base_version=version, op_key=op_key)
    return c._replace_notes(kind, entity_id, text, base_version=version, op_key=op_key)


def _stored_form(field: str, text: str) -> str:
    """`text` as Probe would store it under `field`.

    The client (`Client.write`) and the server (`app/security/content_guard.py`)
    both run the credential scrubber over every write body, so this is what lands.
    Some rules rewrite a span; some rewrite the WHOLE value to `<redacted>`.
    Applied until it stops changing, because it runs more than once on the way.
    """
    from ....sdk.redaction import default_scrub

    for _ in range(3):
        scrubbed = default_scrub({field: text})[field]
        if scrubbed == text:
            break
        text = scrubbed
    return text


def _is_version(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _refuse_scrubbed_old(old: str) -> None:
    """Refuse an `--old` the scrubber would rewrite (the server scrubs `old_text`
    before matching it, so it would match the `<redacted>` text instead)."""
    if _stored_form("old_text", old) != old:
        print(
            "error: --old holds text Probe's credential scrubber rewrites, so it would "
            "match the wrong text; nothing was written. Match a nearby piece of the note "
            "instead.",
            file=sys.stderr,
        )
        raise typer.Exit(1)


def _read_note(
    c: Client, kind: str, entity_id: str, sub_id: str | None
) -> tuple[dict, str, object]:
    """(row, document, notes_version) for the main note or one sub-note.

    Raises ValueError for a reply that is not Probe's JSON row."""
    row = c.get_sub_note(sub_id) if sub_id is not None else _entity_notes_row(c, kind, entity_id)
    if not isinstance(row, dict):
        raise ValueError(f"the reply was not a {kind} note")
    if sub_id is not None:
        return _sub_note_row_for_headroom(row), row.get("body") or "", row.get("notes_version")
    return row, row.get("notes") or "", row.get("notes_version")


@dataclass(frozen=True)
class _Unconfirmed:
    """Why a write's reply did not confirm it, and whether it can still land.

    `may_still_land`: the request reached Probe and nobody saw it finish -- a
    timeout, a reply lost after sending, a 502/504 from the ingress. The CLI
    gives up after 30 s and the server keeps working for up to 300 s, and a
    read is not blocked by the write's row lock, so a note that reads unchanged
    NOW can still change. Only when the app itself answered (a redirect, a
    non-JSON 200, its own 500/503) does unchanged mean nothing was written."""

    why: str
    may_still_land: bool


#: A reply with no version: a redirect, or a 200 that is not Probe's JSON.
_NO_VERSION_REPLY = _Unconfirmed("Probe's reply did not say what it stored", False)

#: Gateway answers: the ingress gave up on the app, which may still be working.
_GATEWAY_STATUSES = frozenset({502, 504})


def _settle_unconfirmed(
    read, base: int, sent: str, what: str, *, why: _Unconfirmed, shown: str
) -> dict:
    """A write whose reply did not confirm it. Never sent again: read the note.

    One version on with exactly the text sent is this write, landed. The same
    version is nothing written only when the app answered; after a timeout it
    is "not there yet". Anything else may be this write or someone else's, and
    only a person reading the note can tell. `read()` returns
    (row, document, version); `shown` is the command that prints the note.
    """
    try:
        row, document, version = read()
    except (errors.RosError, ValueError) as exc:
        # ValueError: a reply that was not JSON (an ingress page).
        print(
            f"error: {why.why}; the {what} could not be re-read ({exc}), so the write may "
            f"have landed. Read it (`{shown}`) before running this again.",
            file=sys.stderr,
        )
        raise typer.Exit(1) from None
    if version == base + 1 and document == sent:
        print(f"{why.why}; the {what} shows this write landed", file=sys.stderr)
        return row
    if version == base and why.may_still_land:
        print(
            f"error: {why.why}; the {what} does not show this write yet, but Probe may still "
            f"be applying it. Read it (`{shown}`) in a few minutes, before running this again.",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    if version == base:
        print(
            f"error: {why.why}; the {what} is unchanged, so nothing was written. Run it again.",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    print(
        f"error: {why.why}; the {what} changed meanwhile, so this write may have landed. "
        f"Read it (`{shown}`) before running this again.",
        file=sys.stderr,
    )
    raise typer.Exit(1)


def _unconfirmed_reason(exc: errors.RosError) -> _Unconfirmed | None:
    """Why a failed write MAY have landed, or None when it surely did not.

    A connection that never reached Probe wrote nothing. A timeout, a reply
    lost after sending or a gateway 502/504 may still land; a 5xx the app
    answered itself (500, 503) did not write."""
    if isinstance(exc, errors.TransportError):
        if getattr(exc, "unreachable", False):
            return None
        return _Unconfirmed(f"the reply was lost ({exc})", True)
    if isinstance(exc, errors.ServerError):
        if exc.status in _GATEWAY_STATUSES:
            return _Unconfirmed(f"Probe's gateway gave up waiting ({exc})", True)
        return _Unconfirmed(f"Probe answered with an error ({exc})", False)
    return None


def _refuse_over_cap(row: object, text: str, kind: str, label: str, *, appending: bool) -> None:
    """Refuse, before sending, a note the server would refuse for its size.

    Against the limits the READ published, in the order the server checks them:
    the character backstop (`notes_limit_chars`), then the TOKEN cap
    (`notes_limit_tokens`), counted with the packaged o200k_base vocabulary and
    only when the text's bytes could pass it (`tokens_past_cap`). On a server
    older than token caps `notes_limit_chars` IS the cap and there is no token
    limit, so the first check alone is that server's rule. A limit the read did
    not publish, or a text this machine cannot count, is left to the server,
    which answers for itself.

    HOW FAR, IN THE UNIT IT IS OVER (notes parity N4, as the server's 422):
    the token cap whenever the text is past it, else the backstop, each with
    how many to cut -- a text under the token cap is never told it is over it."""
    from ....sdk.reads.notes_cap import full_note_message, notes_limit, tokens_past_cap

    if not isinstance(row, dict):
        return
    backstop = row.get("notes_limit_chars")
    if not (isinstance(backstop, int) and not isinstance(backstop, bool) and 0 < backstop):
        backstop = None
    over_chars = len(text) - backstop if backstop is not None and backstop < len(text) else 0
    cap = notes_limit(row)
    # A server older than token caps has none: its backstop IS its cap.
    size = tokens_past_cap(text, cap) if cap is not None else None
    over_tokens = size - cap if size is not None else 0
    if not (over_tokens or over_chars):
        return
    limit, unit = (cap, "token") if over_tokens else (backstop, "character")
    words = " and ".join(f"{n:,} {u}{'s' if n != 1 else ''}"
                         for n, u in ((over_tokens, "token"), (over_chars, "character")) if n)
    over = f"by {words}; cut at least {words}"
    if appending:
        print(
            f"error: appending would exceed the {limit:,}-{unit} notes limit {over}; "
            "nothing was written",
            file=sys.stderr,
        )
        for line in textwrap.wrap(full_note_message(kind, label), width=76):
            print(f"       {line}", file=sys.stderr)
    else:
        at = f"at {size:,} tokens, " if size is not None else ""
        print(
            f"error: the edit would leave the {kind} note ({label}) {at}over its "
            f"{limit:,}-{unit} limit {over}; nothing was written",
            file=sys.stderr,
        )
    raise typer.Exit(1)


def _rewrite_note(
    c: Client,
    kind: str,
    entity_id: str,
    sub_id: str | None,
    label: str,
    change: Callable[[str], tuple[str, str, str]],
    *,
    appending: bool,
) -> dict:
    """Read the note, `change` its text, replace it pinned to the version read.

    `change(document)` returns (kept before, new text, kept after) and refuses
    by raising (an edit whose `--old` does not match once). On a stale-version
    409 the note is read again and `change` runs on the new text, so a
    concurrent writer's words are kept, never overwritten.

    Nothing already in the note may change except what the caller asked for,
    and the scrubber every write passes through can change it: a note holding
    text it would rewrite is refused, and so is new text whose scrub would
    rewrite the rest of the note. A reply that does not confirm the write is
    settled by reading the note, never by sending it again."""
    field = "body" if sub_id is not None else "notes"
    what = f"{kind} note ({label})"

    def read() -> tuple[dict, str, object]:
        return _read_note(c, kind, entity_id, sub_id)

    for _ in range(_NOTE_REWRITE_ATTEMPTS):
        try:
            row, document, version = read()
        except ValueError:
            # Not JSON: an ingress page answered the read, not Probe.
            print(
                f"error: reading the {what} did not return Probe's answer; nothing was "
                "written.",
                file=sys.stderr,
            )
            raise typer.Exit(1) from None
        if not _is_version(version):
            print(
                f"error: Probe did not say which version of the {what} it read, so a "
                "write could overwrite someone else's; nothing was written.",
                file=sys.stderr,
            )
            raise typer.Exit(1)
        if _stored_form(field, document) != document:
            print(
                f"error: the {what} holds text Probe's credential scrubber would rewrite, "
                "and saving the note would rewrite it; nothing was written. Review it with "
                "`probe notes checkout`, then `probe notes push`.",
                file=sys.stderr,
            )
            raise typer.Exit(1)
        before, middle, after = change(document)
        text = before + middle + after
        sent = _stored_form(field, text)
        if not (
            sent.startswith(before)
            and sent.endswith(after)
            and len(sent) >= len(before) + len(after)
        ):
            print(
                f"error: the new text holds something Probe's credential scrubber would "
                f"rewrite, and the rewrite would change the rest of the {what} too; nothing "
                "was written. Leave the credential-shaped text out.",
                file=sys.stderr,
            )
            raise typer.Exit(1)
        _refuse_over_cap(row, sent, kind, label, appending=appending)
        try:
            written = _notes_write(
                kind, label, lambda: _send_note(c, kind, entity_id, sub_id, text, version)
            )
        except errors.ConflictError as exc:
            # `stale_replace`: the document moved since the read. Any other 409
            # is a refusal this loop cannot fix.
            if isinstance(exc.detail, dict) and "notes_version" in exc.detail:
                continue
            raise
        except errors.RosError as exc:
            why = _unconfirmed_reason(exc)
            if why is None:
                raise
            return _settle_unconfirmed(
                read, version, sent, what, why=why, shown="probe notes show"
            )
        written = _sub_note_row_for_headroom(written)
        if not (isinstance(written, dict) and _is_version(written.get("notes_version"))):
            return _settle_unconfirmed(
                read, version, sent, what, why=_NO_VERSION_REPLY, shown="probe notes show"
            )
        return written
    print(
        f"error: the {what} kept changing while this wrote; nothing was written. "
        "Run it again.",
        file=sys.stderr,
    )
    raise typer.Exit(1)
from probe.cli.commands.notes.notes import _entity_notes_row  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.notes.targets import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _note_target,
    _resolve_sub_note_by_title,
    _sub_note_row_for_headroom,
    _sub_notes_supported,
)
