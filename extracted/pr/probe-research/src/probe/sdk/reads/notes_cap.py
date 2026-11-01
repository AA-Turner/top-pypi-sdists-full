"""When a notes document is close enough to its cap to say so, and how to say it.

The cap is enforced loudly (a write against a full document is refused with the cap in
the message), but nothing warned BEFORE the wall: `anthrogen/assignment-modeling` sat at
99,992 of 100,000 characters and every append was refused unnoticed. This module gives
the budget a signal before the cliff.

Caps are TOKENS (o200k_base), all published by the server (`notes_limit_tokens` /
`notes_tokens` / `notes_remaining_tokens`; unprefixed on a sub-note and the team note):
team note 30,000, every other note 1,000 since research-os 2026-10-25 (server setting
`notes_max_tokens`). Nothing is hardcoded here. The `*_chars` fields measure a looser
character backstop and are never read for advice. A note written before a cap was
lowered stays readable; only a write that leaves it over is refused (422).

The threshold is a FRACTION (`NOTES_WARN_FRACTION`), not an absolute: caps differ 30x,
move server-side, and the advice differs by kind (compact a maintained document; move a
run's annotation prose up to its experiment or project). One tier only: the message
carries exact figures, so a second "critical" level would need a second number to defend.

Rationale in full: DESIGN.md in this folder.
"""

from __future__ import annotations

import math

from ...foundation.safe_warn import safe_warn

#: Warn once this fraction of the cap is left: 0.40 starts the advice at 60% FULL.
#: Raised from 0.20 on purpose: the refusal at the cap carries no compaction advice
#: (the write raises before the success path), so this warning is the ONLY place it
#: appears and must leave room to act: 60% of 1,000 tokens leaves 400.
NOTES_WARN_FRACTION = 0.40

#: Keys the server publishes on every notes-carrying response (one place for CLI and SDK).
#: TOKENS, the unit the cap refuses in. A server that predates token caps publishes
#: only `notes_*_chars`, and then nothing here speaks: the client cannot tell from
#: the numbers whether that pair is the cap or the looser character backstop.
REMAINING_KEY = "notes_remaining_tokens"
LIMIT_KEY = "notes_limit_tokens"
#: Tokens held. Null when the server could not count it (backfill not reached), with `REMAINING_KEY` null too.
TOKENS_KEY = "notes_tokens"

#: A sub-note and the team note publish these unprefixed (`SubNoteOut`, `TeamNoteOut`);
#: callers map them to the entity spelling so one reader serves every carrier.
UNPREFIXED_KEYS = {
    "remaining_tokens": REMAINING_KEY,
    "limit_tokens": LIMIT_KEY,
    "tokens": TOKENS_KEY,
}


def _count(value: object) -> int | None:
    """`value` when a real int, else None (bool is an int: a JSON `true` would read "1 tokens left")."""
    if not isinstance(value, int) or isinstance(value, bool):
        return None
    return value


def notes_limit(response: object) -> int | None:
    """The token cap a notes response published, or None.

    Apart from `notes_fullness` because the cap is known even when the count is not
    (`notes_remaining_tokens: null`): the CLI's pre-send refusal still works."""
    if not isinstance(response, dict):
        return None
    limit = _count(response.get(LIMIT_KEY))
    if limit is None or limit <= 0:
        return None
    return limit


def notes_fullness(response: object) -> tuple[int, int] | None:
    """`(remaining, limit)` in TOKENS from a notes write/read response, or None.

    None whenever the answer would be a guess; all four read the same to a caller:

      * the write was JOURNALED, not sent (async mode, fail-open fallback);
      * the backend predates these fields (incl. one with only `notes_*_chars`,
        deliberately not read);
      * the response did not carry the document (`app.core.notes.notes_headroom`);
      * the server could not count it (`notes_remaining_tokens: null`).

    No client-side cap table: it would claim a fullness the server never asserted.
    """
    if not isinstance(response, dict):
        return None
    remaining = _count(response.get(REMAINING_KEY))
    limit = notes_limit(response)
    if remaining is None or limit is None:
        return None
    return remaining, limit


def tokens_past_cap(text: str, limit: int) -> int | None:
    """`text`'s o200k_base token count when it is OVER `limit`; else None.

    None means nothing to refuse: it fits, or this machine cannot count it (no
    tokenizer, a lone surrogate) and the server's check decides.

    Counted with the shipped checksummed o200k_base (`probe.foundation.token_budget`),
    as ordinary text (a special-token spelling is text).

    BYTE SHORTCUT: byte-level BPE means N bytes is at most N tokens, so text whose
    bytes fit the cap is never tokenized (skips the MCP import and the ~0.8 s vocabulary load)."""
    try:
        if len(text.encode("utf-8")) <= limit:
            return None
    except UnicodeError:
        return None  # a lone surrogate: the server decides what it counts as
    from ...foundation.token_budget.token_budget import SerializationError, TokenizerUnavailable, count_tokens

    try:
        counted = count_tokens(text)
    except (TokenizerUnavailable, SerializationError):
        return None
    return counted if counted > limit else None


#: Carriers holding a DOCUMENT someone maintains (vs an annotation on a row); decides
#: the advice. Keyed on kind, not cap size: a numeric threshold would re-encode the
#: caps in the client. The split is stable domain shape (app/core/notes.py).
DOCUMENT_KINDS = frozenset({"project", "experiment", "team_note"})


#: The two action clauses; THE WORDING IS THE CONTRACT. `MOVE_UP_ACTION` is two
#: non-atomic writes: append to the parent FIRST so a failed second write duplicates
#: the prose instead of losing it. Tests pin these by equality so a reword is
#: deliberate. (A regex "append before delete" check once passed delete-first prose,
#: since `append` matches inside `appending`: substring order is not operation order.)
COMPACT_ACTION = (
    "compact it: `probe notes checkout`, fold the paragraphs at the bottom up "
    "into the sections above, then `probe notes push`"
)
#: "A project or experiment", not "THE": only `kind` is known, so the parent cannot be named.
MOVE_UP_ACTION = (
    "move this prose up into a project or experiment notes document: append "
    "there FIRST, then delete it here, so a failed second write duplicates it "
    "rather than losing it"
)


#: What a document at its cap says: different in kind from the warning (below the cap a
#: write lands; at it NOTHING is stored, so the reader must learn it is closed, not tight).
FULL_PREFIX = "is FULL"


def full_note_message(kind: str, label: str | None = None) -> str:
    """What to print when a write was REFUSED because the document is at its cap.

    The refusal (422, SDK re-raises, CLI exits non-zero) skips `headroom_warning`, so
    this is that advice for the failure path. No counts: nothing was read back, and an
    earlier number would be stale.
    """
    what = f"{kind} notes ({label})" if label else f"{kind} notes"
    action = COMPACT_ACTION if kind in DOCUMENT_KINDS else MOVE_UP_ACTION
    return (
        f"{what} {FULL_PREFIX} — nothing further will be stored here until it is "
        f"compacted. {action[0].upper()}{action[1:]}."
    )


def headroom_warning(response: object, *, kind: str, label: str | None = None) -> str | None:
    """The sentence to show after a successful notes write, or None if it is fine.

    `label` names the document when known (the CLI resolved a slug or petname; the SDK has only an opaque id).
    """
    fullness = notes_fullness(response)
    if fullness is None:
        return None
    remaining, limit = fullness
    if remaining > limit * NOTES_WARN_FRACTION:
        return None
    used = limit - remaining
    # FLOOR, never round: "100% full" beside "8 left" is believed; 100% must mean the next write is refused.
    percent = math.floor(100 * used / limit)
    action = COMPACT_ACTION if kind in DOCUMENT_KINDS else MOVE_UP_ACTION
    what = f"{kind} notes ({label})" if label else f"{kind} notes"
    if remaining == 0:
        # Reachable on a SUCCESS (an edit can land exactly on the cap): closed, not tight.
        return (
            f"{what} {FULL_PREFIX} ({used:,} of {limit:,} tokens). Nothing "
            f"further will be stored here until it is compacted — {action}."
        )
    return (
        f"{what} is {percent}% full ({used:,} of {limit:,} tokens, "
        f"{remaining:,} left). Writes are refused at the cap — {action}."
    )


#: The line riding a note HANDED TO A READER (`headroom_warning` fires only after a write).
#:
#: Measured failure behind it: the "correct a note you disproved" instruction in
#: `track-work` (since #1282) produced 21 supersede markers across 25,104 notes. On
#: 2026-09-08 an agent read a 94k-character project note, found SIX claims the repo
#: contradicted, corrected NONE and reported them instead. So the reminder travels
#: WITH the document, not in a skill read 100k tokens ago.
#:
#: NO DATE on purpose: `notes_updated_at` advances on any append, so "last corrected"
#: would look fresh on exactly the rotting notes. Fullness predicts need and is on the row.
NOTES_READ_ADVISORY_ACTION = (
    "correct what your evidence contradicts before you move on"
)


def read_advisory(response: object, *, version: object = None) -> str | None:
    """The one line to show beside a note a caller is READING, or None.

    Never invented: no headroom in the response means no advisory (as `notes_fullness`),
    so an excerpt fetch gets silence, not a figure for a document it was not handed.
    """
    fullness = notes_fullness(response)
    if fullness is None:
        return None
    remaining, limit = fullness
    used = limit - remaining
    percent = math.floor(100 * used / limit)
    where = f"notes v{version}" if version is not None else "notes"
    # An excerpt, pinned version or collapsed projection is not the stored bytes; an edit composed against one targets text the document lacks.
    tail = "re-read the full document before editing it"
    if remaining > limit * NOTES_WARN_FRACTION:
        return f"{where} · {percent}% full — {NOTES_READ_ADVISORY_ACTION}; {tail}."
    return (
        f"{where} · {percent}% full ({used:,} of {limit:,} tokens) — "
        f"{NOTES_READ_ADVISORY_ACTION}, and tighten what you can verify; {tail}."
    )


# ---- text-only writes
# `probe notes append` / `edit` take text as an argument. The server dropped its own
# append and span edit in 0.388.0.0 (a note is a FILE there), so these compute the new
# document here and send a whole-document replace pinned to the version read
# (`base_version`, as `notes push`). A 409 means someone wrote in between: re-read, reapply.


def append_to_document(document: str, chunk: str) -> str:
    """`document` with `chunk` after a blank line, the old server append's rule.

    Two paragraphs joined by one newline render as ONE, so add newlines up to a blank
    line: none for an empty document or one ending in a blank line, one after a
    trailing newline, else two.
    """
    if not document or document.endswith("\n\n"):
        separator = ""
    elif document.endswith("\n"):
        separator = "\n"
    else:
        separator = "\n\n"
    return document + separator + chunk


def edit_match_count(document: str, old_text: str) -> int:
    """Occurrences of `old_text` as the old span edit counted: exact, NON-overlapping,
    unnormalised. An edit runs only when this is exactly 1."""
    return document.count(old_text)


# ---- removed carriers
# Files and sweep groups no longer carry notes (a file's description goes in its RUN's
# notes, a sweep's in its experiment's). The old doors stay callable so older scripts
# and skills do not fail: the text is dropped, never sent, and the caller is told once.

#: Why a file's `notes` goes nowhere (CLI stderr line, SDK warning, `probe artifact set` refusal).
FILE_NOTES_REMOVED = "notes on files were removed; say what a file is in its run's notes"
#: The same for a sweep group's `notes`.
GROUP_NOTES_REMOVED = "notes on sweep groups were removed; use the experiment's notes"


def warn_notes_ignored(notes: object, removed: str, *, stacklevel: int = 3) -> None:
    """A warning that `notes=` was dropped, when the caller passed one.

    Through `safe_warn`, never bare `warnings.warn`: under `-W error` a
    DeprecationWarning would RAISE and fail the upload this door keeps working. A
    UserWarning shows by default at any depth (incl. `probe.log_artifact`); a
    DeprecationWarning attributed to a library frame is hidden.

    `stacklevel=3` points at the caller of the public method that took `notes=`."""
    if notes is None:
        return
    safe_warn.warn(f"`notes=` is ignored: {removed}", stacklevel=stacklevel)
