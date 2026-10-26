"""When a notes document is close enough to its cap to say so, and how to say it.

THE SIGNAL THIS MODULE EXISTS TO PROVIDE. The cap is enforced correctly and
loudly -- a write against a full document is refused with the cap in the message
and exits non-zero, and has since CLI 0.105.2 stopped swallowing that refusal. What was missing is anything
BEFORE the wall. `anthrogen/assignment-modeling` sat at 99,992 of the old
100,000-character cap and was still being written to that same day; every append
was being refused and nobody noticed, because a refusal is only visible to whoever
reads the exit code of the one command that hit it. A number that only appears at
the moment it is too late to act on is not a budget, it is a cliff.

THE CAPS ARE TOKENS (o200k_base), and every number here is the server's. The
team note is capped at 30,000 tokens; every other note -- a project's, an
experiment's, a run's, and every sub-note of those -- at 1,000 since research-os
2026-10-25 (a server setting, `notes_max_tokens`, so it can move without a
client release). The server publishes the cap, the stored count and the room
left on every response that carries the document (`notes_limit_tokens` /
`notes_tokens` / `notes_remaining_tokens`; `limit_tokens` / `tokens` /
`remaining_tokens` on a sub-note and the team note), and nothing here hardcodes
it. The `*_chars` fields it still publishes measure a looser CHARACTER backstop
(150,000 for the team note, 5,000 for the rest) and are never read for advice
here: a fullness computed from them describes a limit that is not the one that
refuses first. A note written before the cap was lowered can sit above it: the
server keeps it readable and refuses only a write that changes it and leaves it
over, with a 422 saying it must be rewritten under the limit.

THE THRESHOLD IS A FRACTION, and the first figure was not a fresh guess: the
notes-first-class design settled on 20% for the team note ("skills instruct
agents to compact when `remaining_chars` drops below 20,000" -- 20% of the
100,000 characters it was capped at then), so the team note and every entity
note say "getting full" at the same point on the same scale. It has since been
raised to 40% (see `NOTES_WARN_FRACTION`).

WHY A FRACTION AND NOT AN ABSOLUTE. The caps differ by 30x (the team note's
30,000 against everyone else's 1,000), the server can move them, and the right
response to hearing this differs by KIND:

  * For a document someone maintains (project, experiment, team note) the
    answer is COMPACTION -- check the document out, fold the paragraphs at the
    bottom up into the head sections, and push it back. That is ongoing work,
    and it needs runway to keep working while it happens.
  * For a run the answer is usually not compaction at all. A run's notes is an
    annotation that rides on a row, so a run note approaching its cap is prose
    that belongs one level up, on the experiment or the project. That is a
    one-time move, and it needs less runway -- one or two more short notes,
    which is enough to finish the thought you are in the middle of and then
    move the document.

An absolute budget cannot express both, nor follow a cap the server moves.

ONE tier, not two. A second "critical" threshold would have to pick a second
number to defend, and the message already carries the exact figures, so the
difference between 82% and 99% is visible in the text rather than in a severity
level nobody configured.
"""

from __future__ import annotations

import math

from . import safe_warn

#: Warn once the document has this little of its cap left, as a fraction of the
#: cap. 0.40 means the advice starts at 60% FULL.
#:
#: Raised from 0.20 (80% full) deliberately. The refusal at the cap names the
#: limit and nothing else -- there is no compaction advice at the wall, because
#: the write raises before the success path that carries it. So the warning is
#: the ONLY place the advice appears, and it has to start early enough that a
#: reader has room to act in: 60% of a 1,000-token note leaves 400 tokens,
#: which is a few more paragraphs of runway rather than one.
NOTES_WARN_FRACTION = 0.40

#: Keys the server publishes on every notes-carrying response. Named here so the
#: CLI and the SDK read the same fields and a rename has one place to happen.
#: TOKENS, the unit the cap refuses in. A server that predates token caps
#: publishes only the `notes_*_chars` pair, and then nothing here speaks: that
#: pair measured the cap on such a server but measures the character backstop on
#: a current one, and a client cannot tell which from the numbers alone.
REMAINING_KEY = "notes_remaining_tokens"
LIMIT_KEY = "notes_limit_tokens"
#: How many tokens the document holds. Null when the server could not count it
#: (a row its backfill has not reached), and `REMAINING_KEY` is null with it.
TOKENS_KEY = "notes_tokens"

#: A sub-note and the team note publish the same three numbers unprefixed
#: (`SubNoteOut`, `TeamNoteOut`). A caller maps them onto the entity spelling
#: before reading them here, so one reader serves every carrier.
UNPREFIXED_KEYS = {
    "remaining_tokens": REMAINING_KEY,
    "limit_tokens": LIMIT_KEY,
    "tokens": TOKENS_KEY,
}


def _count(value: object) -> int | None:
    """`value` when it is a real int, else None.

    bool is an int in Python, and a JSON `true` reaching here would render as
    "1 tokens left" -- a plausible-looking number from a malformed payload is
    worse than no warning."""
    if not isinstance(value, int) or isinstance(value, bool):
        return None
    return value


def notes_limit(response: object) -> int | None:
    """The token cap a notes response published, or None.

    Apart from `notes_fullness` because the cap is known even when the count is
    not: a document the server has not counted publishes its cap beside
    `notes_remaining_tokens: null`. A write can still be checked against the cap
    (the CLI's pre-send refusal); only the FULLNESS is unknown."""
    if not isinstance(response, dict):
        return None
    limit = _count(response.get(LIMIT_KEY))
    if limit is None or limit <= 0:
        return None
    return limit


def notes_fullness(response: object) -> tuple[int, int] | None:
    """`(remaining, limit)` in TOKENS from a notes write/read response, or None.

    None whenever the answer would be a guess, and there are four ways for that
    to happen, all of which must read the same to a caller:

      * the write was JOURNALED rather than sent (async mode, or a fail-open
        fallback), so `Client.write` returned None and no server ever saw it;
      * the backend predates these fields, so the keys are simply absent --
        including one that predates TOKEN caps and publishes only the
        `notes_*_chars` pair, which is deliberately not read (module docstring);
      * the response did not carry the document, so the server published no
        headroom (see `app.core.notes.notes_headroom`);
      * the server carried the document but could not count it, so it published
        `notes_remaining_tokens: null`.

    A backend too old to publish the pair is the case that decides the return
    type. Substituting a client-side cap table here would let this module claim
    a fullness the server never asserted -- which is the same class of confident
    wrong answer the whole feature exists to remove.
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

    None means "nothing to refuse here": the text fits, or this machine cannot
    count it (no tokenizer, a lone surrogate), and then the server's own check
    is the answer -- a client that guessed would refuse a write the server takes.

    Counted with the vocabulary this package ships (`probe.mcp.budget`, the
    checksummed o200k_base the server's tiktoken loads), as ordinary text the
    way the server counts it: a special-token spelling is text, not a token.

    THE BYTE SHORTCUT. o200k is byte-level BPE, so every token covers at least
    one UTF-8 byte and a text of N bytes is at most N tokens. A text whose bytes
    fit the cap is never tokenized -- the common case, and the one that never
    imports the MCP package or loads its 200k-entry vocabulary (~0.8 s)."""
    try:
        if len(text.encode("utf-8")) <= limit:
            return None
    except UnicodeError:
        return None  # a lone surrogate: the server decides what it counts as
    from ..mcp.budget import SerializationError, TokenizerUnavailable, count_tokens

    try:
        counted = count_tokens(text)
    except (TokenizerUnavailable, SerializationError):
        return None
    return counted if counted > limit else None


#: The carriers that hold a DOCUMENT someone maintains, as opposed to an
#: annotation that rides on a row. It decides what a writer should DO about a
#: full document, and the two answers are different enough that one sentence
#: cannot serve both -- see the module docstring.
#:
#: Keyed on the kind rather than on the size of the cap. A numeric threshold
#: ("caps above 10,000 are documents") would be a second place the caps are
#: encoded in a client, which is exactly what `notes_limit_tokens` exists to
#: remove; the split itself is stable domain shape, stated in app/core/notes.py.
DOCUMENT_KINDS = frozenset({"project", "experiment", "team_note"})


#: The two action clauses, as named constants because THE WORDING IS THE
#: CONTRACT. `MOVE_UP_ACTION` describes two writes against two entities that
#: nothing makes atomic: appending to the parent first means a failed second
#: write duplicates the prose, the other order LOSES it. That ordering survives
#: only as long as the sentence says it, so the tests pin these by equality --
#: a reword has to be deliberate, not a tidy-up that quietly drops the order.
#:
#: An earlier attempt asserted `append` before `delete` with a regex. It was
#: lexical, not semantic, and passed on delete-first prose: "stop appending
#: here -- FIRST make sure you have the text, then delete it here, and append
#: it to the project afterwards" matches, because `append` matches inside
#: `appending`. Substring order is not operation order.
COMPACT_ACTION = (
    "compact it: `probe notes checkout`, fold the paragraphs at the bottom up "
    "into the sections above, then `probe notes push`"
)
#: "A project or experiment", not "THE experiment or project": this function is
#: given only `kind`, so it cannot name the right parent, and the indefinite
#: article stays true whichever one the run is filed under.
MOVE_UP_ACTION = (
    "move this prose up into a project or experiment notes document: append "
    "there FIRST, then delete it here, so a failed second write duplicates it "
    "rather than losing it"
)


#: What a document at its cap says. Distinct from the warning above because the
#: state is different in kind, not degree: below the cap a write still lands and
#: the advice is a budget: at the cap NOTHING further is stored, and the reader
#: needs to know the document is closed until it is compacted rather than that it
#: is merely tight.
FULL_PREFIX = "is FULL"


def full_note_message(kind: str, label: str | None = None) -> str:
    """What to print when a write was REFUSED because the document is at its cap.

    The refusal path never reaches `headroom_warning`: the server answers 422,
    the SDK re-raises it and the CLI exits non-zero, so the success-path advice
    is skipped at exactly the moment it is most needed. This is that advice,
    reachable from the failure path.

    It carries no counts. The write failed, so nothing was read back,
    and a number recalled from an earlier response would describe the document
    before whatever else has been written to it since.
    """
    what = f"{kind} notes ({label})" if label else f"{kind} notes"
    action = COMPACT_ACTION if kind in DOCUMENT_KINDS else MOVE_UP_ACTION
    return (
        f"{what} {FULL_PREFIX} — nothing further will be stored here until it is "
        f"compacted. {action[0].upper()}{action[1:]}."
    )


def headroom_warning(response: object, *, kind: str, label: str | None = None) -> str | None:
    """The sentence to show after a successful notes write, or None if it is fine.

    `label` names the specific document when the caller knows it -- the CLI just
    resolved a project slug or a run petname and can say which one filled up,
    where the SDK holds only an opaque id and is better off not repeating it.
    """
    fullness = notes_fullness(response)
    if fullness is None:
        return None
    remaining, limit = fullness
    if remaining > limit * NOTES_WARN_FRACTION:
        return None
    used = limit - remaining
    # FLOOR, never round: rounding prints "100% full" beside "8 left", and a
    # reader resolves that contradiction by believing the percentage. 100% here
    # means the next write is refused, and nothing else does.
    percent = math.floor(100 * used / limit)
    action = COMPACT_ACTION if kind in DOCUMENT_KINDS else MOVE_UP_ACTION
    what = f"{kind} notes ({label})" if label else f"{kind} notes"
    if remaining == 0:
        # Reachable on a SUCCESS: an edit can land exactly on the cap. The next
        # write is already refused, so this says closed, not tight.
        return (
            f"{what} {FULL_PREFIX} ({used:,} of {limit:,} tokens). Nothing "
            f"further will be stored here until it is compacted — {action}."
        )
    return (
        f"{what} is {percent}% full ({used:,} of {limit:,} tokens, "
        f"{remaining:,} left). Writes are refused at the cap — {action}."
    )


#: The line that rides a note when it is HANDED TO A READER, as opposed to
#: `headroom_warning`, which fires only after a successful write.
#:
#: THIS IS THE WHOLE MECHANISM, and it exists because of a measured failure. The
#: instruction to correct a note you have just disproved has shipped in
#: `track-work` since #1282 and produced 21 supersede markers across 25,104
#: notes. Watched directly (2026-09-08): an agent read a 94k-character project
#: note, found SIX claims the repository contradicted, cited the commit for each,
#: corrected NONE, and reported them to the researcher instead. Its context
#: carried the skill. Nothing carried the note.
#:
#: So the reminder travels WITH the document rather than living in a skill file
#: the model read once, forty minutes and a hundred thousand tokens ago.
#:
#: NO DATE, deliberately. `notes_updated_at` advances on any write including an
#: append, so "last corrected" would read as fresh on precisely the notes that
#: are rotting -- appended to weekly, never checked. Fullness is the number that
#: actually predicts a note needing work, and it is already on the row.
NOTES_READ_ADVISORY_ACTION = (
    "correct what your evidence contradicts before you move on"
)


def read_advisory(response: object, *, version: object = None) -> str | None:
    """The one line to show beside a note a caller is READING, or None.

    Never invented: with no headroom in the response there is no advisory, the
    same "absent means this response did not carry it" rule `notes_fullness`
    already applies. A caller that fetched an excerpt therefore gets silence
    rather than a fullness figure describing a document it was not handed.
    """
    fullness = notes_fullness(response)
    if fullness is None:
        return None
    remaining, limit = fullness
    used = limit - remaining
    percent = math.floor(100 * used / limit)
    where = f"notes v{version}" if version is not None else "notes"
    # Re-reading is not pedantry: an excerpt, a pinned version or a collapsed
    # projection all read fine and none of them are the stored bytes, so an edit
    # composed against one targets text the document does not contain.
    tail = "re-read the full document before editing it"
    if remaining > limit * NOTES_WARN_FRACTION:
        return f"{where} · {percent}% full — {NOTES_READ_ADVISORY_ACTION}; {tail}."
    return (
        f"{where} · {percent}% full ({used:,} of {limit:,} tokens) — "
        f"{NOTES_READ_ADVISORY_ACTION}, and tighten what you can verify; {tail}."
    )


# ---------------------------------------------------------------- text-only writes
#
# `probe notes append` and `probe notes edit` change a note without a file: the
# text arrives as an argument. The server dropped its own append and span edit
# in 0.388.0.0 (a note is a FILE there), so these two compute the new document
# here and send it as a whole-document replace pinned to the version they read,
# the same `base_version` contract `notes push` uses. A 409 means someone wrote
# in between: the caller re-reads and applies the change again.


def append_to_document(document: str, chunk: str) -> str:
    """`document` with `chunk` after a blank line, the old server append's rule.

    Notes are one markdown document, and two paragraphs joined by a single
    newline render as ONE paragraph. So add however many newlines it takes to
    reach a blank line: none for an empty document or one already ending in a
    blank line, one after a trailing newline, two otherwise.
    """
    if not document or document.endswith("\n\n"):
        separator = ""
    elif document.endswith("\n"):
        separator = "\n"
    else:
        separator = "\n\n"
    return document + separator + chunk


def edit_match_count(document: str, old_text: str) -> int:
    """How many times `old_text` occurs in `document`, counted the way the old
    span edit counted: exact substring, NON-overlapping, no normalisation. An
    edit runs only when this is exactly 1, so its replacement is unambiguous."""
    return document.count(old_text)


# ---------------------------------------------------------------- removed carriers
#
# Files (artifacts) and sweep groups stopped carrying notes: notes live on
# projects, experiments, runs and the team note. What a file IS, and where it
# lives, goes in its RUN's notes; what a sweep tested goes in its experiment's.
# The old doors stay callable so a training script or an agent on an older skill
# does not fail its upload or its group create: the text is dropped, never sent,
# and the caller is told once.

#: Why a file's `notes` goes nowhere. One sentence for the CLI's stderr line, the
#: SDK's warning and `probe artifact set`'s refusal.
FILE_NOTES_REMOVED = "notes on files were removed; say what a file is in its run's notes"
#: The same for a sweep group's `notes`.
GROUP_NOTES_REMOVED = "notes on sweep groups were removed; use the experiment's notes"


def warn_notes_ignored(notes: object, removed: str, *, stacklevel: int = 3) -> None:
    """A warning that `notes=` was dropped, when the caller passed one.

    Through `safe_warn`, never a bare `warnings.warn`: `log_artifact` runs beside
    a training loop, and under `-W error` a DeprecationWarning would RAISE and
    fail the very upload this door stays open to keep working. A UserWarning
    also shows by default however deep the call came in (the fluent
    `probe.log_artifact` included), where a DeprecationWarning attributed to a
    library frame is hidden.

    `stacklevel=3` points at the caller of the public method that took `notes=`
    (this helper, then that method, then its caller)."""
    if notes is None:
        return
    safe_warn.warn(f"`notes=` is ignored: {removed}", stacklevel=stacklevel)
