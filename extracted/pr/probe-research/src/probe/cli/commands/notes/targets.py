"""which note a command means (entity, titled sub-note) and how full it is (headroom fields, stderr warning)."""

from __future__ import annotations
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ....sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

from .... import errors
from ....shared.reads import reads


# ---------------------------------------------------------------- notes, everywhere
#
# `notes show|write` above are PROJECT-scoped and stay that way -- the project's
# notes are the default destination and every shipped script calls them bare.
# What follows is the same document model on every other carrier (0124), plus the
# TEAM note (0125), through target flags rather than five parallel verb groups.

#: Every entity that carries notes, and how to resolve one from a CLI flag.
#: Files (artifacts) and sweep groups stopped carrying notes: what a file is
#: goes in its run's notes, what a sweep tested in its experiment's.
#: The TEAM note is not one of them: a session that has its file edits it and
#: syncs (`probe notes sync`, and the hooks that call it). Only `notes append`
#: and `notes edit` take `--team`, for a caller with no file, and they reach the
#: server-computed team-note writes rather than anything resolved here.
#: A TRIAL is deliberately absent, though `PATCH /v1/trials/{id}` takes the same
#: three notes writes and the dashboard offers the editor. Every carrier here is
#: something the agent CREATED, which is what gives it a moment to annotate;
#: a trial is materialized by a database trigger on any rollout span (0135), and
#: there is one per rollout, so a 500-rollout run would offer 500 documents for
#: an observation that belongs once on the run. Agents READ trial notes
#: (`probe trial get`); people write them in the dashboard.
_NOTE_TARGETS = reads.NOTE_TARGETS


def _sub_note_row_for_headroom(row: object) -> object:
    """Adapt a sub-note write/read response to the entity-notes headroom keys.

    Sub-note responses spell their numbers unprefixed -- `tokens` /
    `limit_tokens` / `remaining_tokens` and the character backstop's
    `remaining_chars` / `limit_chars` (the row prices itself); the shared
    fullness helpers and `_headroom_fields` read the entity spelling. A None
    row (journaled write) passes through — no server saw it, so there is no
    fullness to adapt.
    """
    from ....sdk.reads.notes_cap import UNPREFIXED_KEYS

    if not isinstance(row, dict):
        return row
    adapted = dict(row)
    aliases = {
        **UNPREFIXED_KEYS,
        "remaining_chars": "notes_remaining_chars",
        "limit_chars": "notes_limit_chars",
    }
    for key, entity_key in aliases.items():
        if key in adapted and entity_key not in adapted:
            adapted[entity_key] = adapted[key]
    return adapted


def _stderr_line(text: str) -> None:
    print(text, file=sys.stderr)


def _sub_notes_supported(exc: errors.RosError) -> None:
    """A ROUTE-shaped 404 said as the honest self-host answer (`reads.sub_notes_supported`)."""
    reads.sub_notes_supported(exc, _stderr_line)


#: The uuid inside an `id:<uuid>` --note value (`reads.sub_note_id_ref`).
_sub_note_id_ref = reads.sub_note_id_ref


def _resolve_sub_note_by_title(client: Client, kind: str, entity_id: str, title: str) -> dict:
    """The one sub-note `title` (or `id:<uuid>`) names (`reads.resolve_sub_note_by_title`)."""
    return reads.resolve_sub_note_by_title(client, kind, entity_id, title, _stderr_line)


def _note_target(
    client: Client,
    *,
    project: str | None,
    experiment: str | None,
    run: str | None,
) -> tuple[str, str, str]:
    """(kind, id, label) for a notes write. Exactly one target, or the default
    (`reads.note_target`)."""
    return reads.note_target(_api(client), project=project, experiment=experiment, run=run)


def _headroom_fields(row: object) -> dict[str, int]:
    """The fullness numbers for a write's JSON, or `{}` when there are none.

    Empty rather than nulls, and the difference is load-bearing for a caller
    piping this into `jq`: a write that was JOURNALED reached no server, so there
    is no fullness to report, and emitting `"remaining": null` invites a reader to
    treat absent as zero. A key that is not there cannot be misread as a number.

    `stored_chars`, not `chars`. These commands have printed `chars` since they
    shipped and it means the size of the CHUNK the caller sent; the document's
    own length is a different number and must not silently take that key.

    TWO SETS, each present only when the server published it. The cap is in
    TOKENS now: `stored_tokens` / `limit_tokens` / `remaining_tokens`, absent
    for a count the server could not give (or a server older than token caps).
    `remaining` / `limit` / `stored_chars` keep the CHARACTER meaning they
    always had, as the server kept `notes_*_chars`: a script reading them goes
    on parsing, and they now measure the character backstop, not the cap.
    """
    from ....sdk.reads.notes_cap import TOKENS_KEY, notes_fullness, notes_limit

    if not isinstance(row, dict):
        return {}
    fields: dict[str, int] = {}
    remaining, limit = row.get("notes_remaining_chars"), row.get("notes_limit_chars")
    if all(isinstance(v, int) and not isinstance(v, bool) for v in (remaining, limit)):
        fields.update({"remaining": remaining, "limit": limit, "stored_chars": limit - remaining})
    cap = notes_limit(row)
    if cap is not None:
        fields["limit_tokens"] = cap
    fullness = notes_fullness(row)
    if fullness is not None:
        fields["remaining_tokens"] = fullness[0]
    stored = row.get(TOKENS_KEY)
    if isinstance(stored, int) and not isinstance(stored, bool):
        fields["stored_tokens"] = stored
    return fields


def _note_landed(kind: str, entity_id: str) -> None:
    """A note on a run landed: what this session owed it is settled (`owed`;
    `probe run tag RUN invalid` owes one)."""
    if kind != "run":
        return
    from ....shared.notes import owed

    owed.settle(owed.NOTE, {f"run:{entity_id}"})


def _report_notes_headroom(row: object, kind: str, label: str) -> None:
    """Say on STDERR that this document is filling up, on the success path.

    The piece that would have caught `assignment-modeling`, which sat at 99,992
    of its then 100,000-character cap while every append was being refused: a cap is only a
    budget if you can see it coming down. Stderr, beside the "appended to ..."
    line, so it never enters the JSON a script parses.

    Silent when the write was journaled or the backend is too old to publish the
    numbers -- `headroom_warning` returns None rather than guessing, because a
    client-side cap table would let this print a fullness the server never said.
    """
    from ....sdk.reads.notes_cap import headroom_warning

    message = headroom_warning(row, kind=kind, label=label)
    if message is not None:
        print(f"warning: {message}", file=sys.stderr)
from probe.cli.commands.refs import _api  # noqa: E402 -- pieces need each other; the front door loads this one first
