"""THE structured run-failure shape — built where the engine already knows.

At the moment a step fails, the engine holds every fact a person needs: which
step, the author's name for it, which field, what it expected, what it got.
Before this module all of that was ``str(exc)``-ed into one line, written into
the jsonb ``workflow.run.error`` column as ``{"message": "<raw python>"}``, and
then guessed at again on the client with a regex table. Measured on 2026-08-20
against all 144 failed/errored rows: 129 held ONLY ``message``, 108 of those
messages opened with a raw exception class name, and a client-side regex table
recovered a specific cause for fewer than a quarter of them.

The fix is one-directional: **derive the structure at the raise site, persist
it, and let every reader read fields instead of parsing English.**

What a :class:`RunFailure` carries
---------------------------------
``cause``       stable machine code (:class:`Cause`) — the ONLY thing a reader
                should branch on. Never localized, never renamed casually: a
                UI mapping and a metric both key off it.
``message``     one human sentence. Deliberately also the ``message`` key of
                the persisted dict, so every pre-existing reader
                (``errorMessage()`` on the client, agent_plans, replay) keeps
                working against a strictly richer payload.
``step_id``     the graph node id — for us, for deep links.
``step_label``  the AUTHOR's name for that step ("Study Pack"), which is the
                only name the reader has ever seen. Never the node id.
``field`` / ``expected`` / ``got``
                the primary field problem, when the exception carries one. A
                pydantic ``ValidationError`` already has ``.errors()`` with
                ``loc``/``type``/``msg``/``input`` parsed — we were throwing
                that away and re-deriving it with a regex.
``fields``      every field problem when there is more than one.
``technical``   the FULL raw text, ANSI-stripped. **Never dropped** — it is
                what the Expert hands back to us verbatim.

A failure is classified by its CLASS, never by the user's words
---------------------------------------------------------------
On 2026-09-12 run ``053e8b72`` ("Newsroom Desk") died on a matrx-orm
``QueryTimeoutError`` writing a 1.1 MB ``workflow.checkpoint`` row, and the
Expert was told **"This account needs an age check before AI can run."** The
ORM renders its error with the statement's ``Args:`` attached, the args were
that fan-out's per-item ``document`` inputs, one of those documents quoted a
Supreme Court line about *"legislatures are ultimate guardians of the liberties
…"* — and the message ladder's first rung is ``coppa|consent_required|guardian
|age_undeclared``. A database timeout reached a person as a legal refusal about
her own account.

Two rules came out of it, and both are structural, not a patched rung:

1. :func:`persistence_cause_for_exception` runs FIRST and decides by class —
   any exception from ``matrx_orm`` (``QueryTimeoutError``,
   ``LockContentionError``, ``PoolAcquireTimeoutError``, the whole
   ``DatabaseError`` family) and matrx-graph's own ``CheckpointError`` family
   are :attr:`Cause.PERSISTENCE_FAILED` before one character of prose is read.
   The type is hard evidence; prose is a guess.
2. :func:`classification_text` is the ONLY text the ladder ever sees — cut at
   the first ``Args:``/``Query:``-style payload marker, with pydantic
   ``input_value=`` blobs elided and a hard character bound. **A regex that
   decides what to tell a person must never run over what that person wrote.**

ANSI never reaches the database
-------------------------------
Three live rows carry terminal color escapes (``[91m``) persisted into a jsonb
column, because matrx-orm renders its ``IntegrityError`` for a terminal and the
engine stringified that render. :func:`strip_ansi` is applied on every field
this module produces, and again at the store boundary
(``run_store._sanitize_error``) so a payload built somewhere else cannot smuggle
one in.

Stranded runs are OUR failure
-----------------------------
A run force-failed by the watchdog, by cleanup, or by the force-fail endpoint
did not fail — *we dropped it*. It gets :attr:`Cause.RUN_STRANDED` so the UI can
say that truthfully and offer the run back, instead of blaming the person who
pressed the button.
"""

from __future__ import annotations

import re
from typing import Any

from matrx_utils import (  # noqa: F401 — CLASSIFY_TEXT_LIMIT is a deliberate re-export
    CLASSIFY_TEXT_LIMIT,
    classification_text,
    client_error_text,
)
from pydantic import BaseModel, ConfigDict, Field


class Cause:
    """The stable machine codes. Readers branch on these; nothing else.

    Adding one is cheap and safe. RENAMING one is a breaking change — the
    client's cause→copy map and the per-definition failure metric both key on
    the literal string, and rows already persisted keep the old value forever.
    """

    # --- the author / the run's inputs ---------------------------------
    MISSING_INPUT = "missing_input"
    """A required value was absent or empty. ``field`` names it."""
    INVALID_INPUT = "invalid_input"
    """A value was present but the wrong type/shape/range. ``field`` names it."""
    UNRESOLVED_VARIABLE = "unresolved_variable"
    """A ``{"$var": ...}`` reference had no value for this run."""
    DEFINITION_INVALID = "definition_invalid"
    """The workflow itself does not compile/validate — it never started."""
    WIRING_BROKEN = "wiring_broken"
    """An edge could not deliver: mapping miss, predicate failure, double writer."""

    # --- the platform's gates ------------------------------------------
    NO_ORGANIZATION = "no_organization"
    CONSENT_REQUIRED = "consent_required"
    NOT_AUTHORIZED = "not_authorized"
    MANDATE_UNRESOLVED = "mandate_unresolved"
    OUT_OF_CREDITS = "out_of_credits"
    USAGE_LIMIT_REACHED = "usage_limit_reached"
    """The usage gate refused the person's paid call: their plan's AI usage limit
    is reached (matrx-ai ``UsageLimitReachedError``, codes ``usage_limit_reached``
    / ``guest_ai_allowance_used``). A limit on THIS account, never "our side" —
    live 2026-10-24 (run ``ac8858af``) it read as engine_error."""

    MODEL_NOT_APPROVED = "model_not_approved"
    """The step's AI model is a top-tier one this account is not approved for (matrx-ai
    ``TopTierModelRefusedError``: "This model is limited to approved accounts"). Nothing ran and no
    other model was tried — not a missing AI binding, not our fault (a ``MandateError`` carrying the
    gate's sentence read "no AI assigned" until 3d2366ce, then ``engine_error``; 2026-10-27)."""

    AUTOMATION_PAUSED = "automation_paused"
    """Not a fault of this run: the automation's guardrail refused it ("Refused: retry storm — this
    automation was refused 5 times in 10 minutes on the same input ... It is paused" / "Refused:
    paused by its guardrail"; ``billing.automation_guardrails``, ``error_type`` ``automation_guardrail``).
    A person fixes why it repeats, then resumes it; it read as ``engine_error`` (2026-10-27)."""

    EXPRESSION_REJECTED = "expression_rejected"
    """An authored expression used something the safe evaluator refuses."""

    # --- the outside world ----------------------------------------------
    SITE_BLOCKED = "site_blocked"
    """A website the step reads turned us away (Cloudflare/WAF challenge, bot
    wall, captcha). The site's 403 is NOT_AUTHORIZED's word but not its
    meaning: nothing about this run's own permissions is wrong (live
    2026-10-14, run ``ce04563a``: rooterhero.com's "Just a moment..." page was
    reported as "This run isn't allowed to reach something it needs")."""
    RATE_LIMITED = "rate_limited"
    CONTENT_FILTERED = "content_filtered"
    PROVIDER_ERROR = "provider_error"
    AI_OUTPUT_UNUSABLE = "ai_output_unusable"
    """The model answered, but the answer could not be parsed into the shape
    the step declared. Distinct from PROVIDER_ERROR (the call itself failed)
    and from INVALID_INPUT (the AUTHOR's value was wrong) — here the AI is
    what came up short, which is the only one of the three a retry may fix."""
    OUTPUT_TRUNCATED = "output_truncated"
    """The model hit its token ceiling mid-answer."""
    TOOL_LOOP_STALLED = "tool_loop_stalled"
    """The AI kept calling a tool that kept failing (or ran out of iterations),
    so its loop was stopped. In a chat that exit is a resumable PAUSE the person
    answers; an unattended step has nobody to answer it, so it is a failure —
    and never ``ENGINE_ERROR``, which told a person "this step stopped partway
    through" while the orchestrator knew the tool, the count and the error
    (live 2026-09-12, run ``6fa6ad90`` node ``n_check``: ``rulebook`` failed 11
    of 11 calls on a slug passed where a UUID belongs)."""
    NOT_FOUND = "not_found"
    TIMED_OUT = "timed_out"

    HELD_FOR_APPROVAL = "held_for_approval"
    """Not a fault: the step's change is waiting in the organization's approval
    queue (the "Agent changes to this organization's data" setting). Nothing was
    written; a person approves or refuses it on the step's card or on the table's
    page. Set only from a step's own ``held_for_approval`` code, never guessed
    from prose (lane HELD-WRITE-TAILS, 2026-09-26)."""

    SPEND_APPROVAL_REQUIRED = "spend_approval_required"
    """Not a fault: a spend gate refused the step before it spent anything — the run, or an
    agent / mandate / workflow it belongs to, crossed its approval limit or is held for
    approval. Never retried and never auto-resumed (``matrx_graph.spend_gate``); the failure
    carries ``approval_url``, where a person approves it, then the run is retried (2026-10-27)."""

    REFUSED = "refused"
    """Not a fault: a person REFUSED the step's held change, so nothing was written and
    the run ended there (lane HELD-WRITE-RESUME, 2026-09-26). The terminal twin of
    ``HELD_FOR_APPROVAL``; set only by the resume route from the approval's own state."""

    # --- lifecycle -------------------------------------------------------
    CANCELLED = "cancelled"
    RUN_STRANDED = "run_stranded"
    """OUR failure: the run's task died without writing a terminal status."""
    CHILD_RUN_FAILED = "child_run_failed"
    """A subgraph.call child run ended badly; the child's own row has the cause."""
    FINAL_WRITE_FAILED = "final_write_failed"
    """OUR failure: the run finished its steps, but saving its final row failed, so it was ended
    failed instead of staying "running" (``run_store.apply_result``). ``intended_cause`` on the
    row names the cause the run meant to end with, when it was ending failed."""

    # --- ours ------------------------------------------------------------
    PERSISTENCE_FAILED = "persistence_failed"
    DATABASE_BUSY = "database_busy"
    """OUR transient failure: the database canceled a statement to break a lock queue (SQLSTATE 55P03
    lock timeout, 40P01/40001). Nothing of it committed, so running again is safe — never "couldn't save
    the result", which told a person a READ had lost her work (Vault reads, 2026-10-28)."""
    ENGINE_ERROR = "engine_error"
    """The honest fallback. A rising rate here is the signal to add a cause."""


# ---------------------------------------------------------------------------
# ANSI
# ---------------------------------------------------------------------------

# Well-formed escape sequences (ESC-prefixed), plus the ORPHANED form we
# actually found in the database: vcprint / the matrx-orm error renderer lose
# the ESC byte somewhere on the way through str() and leave a bare "[91m" —
# three live rows carry exactly that.
#
# The orphan pattern is deliberately NARROW: only reset ("[0m") and the real
# color parameter ranges (30-37/39, 40-47/49, 90-97, 100-107), optionally
# preceded by an intensity parameter ("[1;31m"). The bare single-digit codes
# ("[1m", "[5m") are EXCLUDED on purpose — without the ESC byte they are
# indistinguishable from ordinary English like "[1m ago]", and eating a
# person's text to tidy a color code is the worse failure of the two.
_ANSI_ESCAPED = re.compile(r"\x1b\[[0-9;:]*[ -/]*[@-~]")
_ANSI_ORPHAN = re.compile(r"\[(?:0|(?:[0-9];)?(?:3[0-79]|4[0-79]|9[0-7]|10[0-7]))m")


def strip_ansi(text: str) -> str:
    """Remove terminal color formatting. Terminal bytes are never a user-facing
    error and must never be persisted — applied to every field this module
    produces AND again at the store boundary."""
    return _ANSI_ORPHAN.sub("", _ANSI_ESCAPED.sub("", text))


# ---------------------------------------------------------------------------
# What a classifier is allowed to read
# ---------------------------------------------------------------------------

# THE primitive lives in matrx-utils (root of the package graph) because every
# layer has a ladder like ours — the worker's retry decision, matrx-ai's
# orchestrator, a router's status code — and they must all trim the same way.
# Imported at the top of this module, so ``matrx_graph.failure.classification_text``
# (and ``CLASSIFY_TEXT_LIMIT``) stay the names this package's callers use. What may
# be MATCHED, never what is KEPT: see matrx_utils/error_text.py.


# ---------------------------------------------------------------------------
# The shape
# ---------------------------------------------------------------------------


class FieldProblem(BaseModel):
    """One field's problem, exactly as the validator reported it."""

    model_config = ConfigDict(extra="forbid")

    field: str
    """Dotted path from the validator's ``loc`` — "sources", "match.id"."""
    expected: str | None = None
    """What the contract asked for, in words: "at least 1 item", "a whole number"."""
    got: str | None = None
    """A SHORT rendering of what arrived. Truncated; never a full payload dump."""
    code: str | None = None
    """The validator's own type key ("missing", "too_short") — for metrics."""


class RunFailure(BaseModel):
    """The structured failure written to ``workflow.run.error`` and merged into
    ``workflow.node_outcome.error``.

    ``model_dump(mode="json", exclude_none=True)`` is what goes to the column:
    absent facts stay absent rather than persisting a wall of nulls. ``cause``,
    ``message`` and ``technical`` are always present.
    """

    model_config = ConfigDict(extra="forbid")

    cause: str = Cause.ENGINE_ERROR
    message: str
    step_id: str | None = None
    step_label: str | None = None
    field: str | None = None
    expected: str | None = None
    got: str | None = None
    fields: list[FieldProblem] = Field(default_factory=list)
    error_type: str | None = None
    """The raised exception's class name. For us; readers branch on ``cause``."""
    approval_url: str | None = None
    """Where a person approves the spend this run is waiting on (``SPEND_APPROVAL_REQUIRED``)."""
    technical: str | None = None
    """The raw text, ANSI-stripped and cut before any SQL / bound args /
    traceback / maintainer hints (:func:`matrx_utils.client_error_text`). The
    full render goes to the logs, never to a column a client reads."""

    def to_column(self) -> dict[str, Any]:
        """The dict shape for the jsonb ``error`` column."""
        payload = self.model_dump(mode="json", exclude_none=True)
        if not payload.get("fields"):
            payload.pop("fields", None)
        return payload


_MAX_GOT = 120


def _render_got(value: Any) -> str | None:
    """A SHORT, safe rendering of the offending input.

    Truncated hard: a validation error's ``input`` can be the node's entire
    payload, and this string is destined for a jsonb column and a UI line.
    """
    if value is None:
        return "nothing"
    try:
        text = value if isinstance(value, str) else repr(value)
    except Exception:  # noqa: BLE001 — a hostile __repr__ must not break failure reporting
        return None
    text = strip_ansi(text).strip()
    if not text:
        return "an empty value"
    return text if len(text) <= _MAX_GOT else text[: _MAX_GOT - 1] + "…"


# pydantic error ``type`` → (cause, human "expected" phrasing).
# The phrasing is the CONTRACT restated, not the error restated: the reader
# needs to know what would have been right.
_PYDANTIC_TYPES: dict[str, tuple[str, str]] = {
    "missing": (Cause.MISSING_INPUT, "a value"),
    "value_error.missing": (Cause.MISSING_INPUT, "a value"),
    "too_short": (Cause.MISSING_INPUT, "at least one entry"),
    "string_too_short": (Cause.MISSING_INPUT, "some text"),
    "none_required": (Cause.INVALID_INPUT, "nothing"),
    "extra_forbidden": (Cause.INVALID_INPUT, "not to be given at all"),
    "string_type": (Cause.INVALID_INPUT, "text"),
    "int_type": (Cause.INVALID_INPUT, "a whole number"),
    "int_parsing": (Cause.INVALID_INPUT, "a whole number"),
    "float_type": (Cause.INVALID_INPUT, "a number"),
    "bool_type": (Cause.INVALID_INPUT, "yes or no"),
    "dict_type": (Cause.INVALID_INPUT, "a set of named values"),
    "list_type": (Cause.INVALID_INPUT, "a list"),
    "model_type": (Cause.INVALID_INPUT, "a set of named values"),
    "too_long": (Cause.INVALID_INPUT, "fewer entries"),
    "string_too_long": (Cause.INVALID_INPUT, "shorter text"),
    "enum": (Cause.INVALID_INPUT, "one of the allowed choices"),
    "literal_error": (Cause.INVALID_INPUT, "one of the allowed choices"),
    "greater_than": (Cause.INVALID_INPUT, "a larger number"),
    "greater_than_equal": (Cause.INVALID_INPUT, "a larger number"),
    "less_than": (Cause.INVALID_INPUT, "a smaller number"),
    "less_than_equal": (Cause.INVALID_INPUT, "a smaller number"),
    "url_parsing": (Cause.INVALID_INPUT, "a web address"),
    "uuid_parsing": (Cause.INVALID_INPUT, "an id"),
    "json_invalid": (Cause.INVALID_INPUT, "valid JSON"),
}


def _loc_to_field(loc: tuple[Any, ...]) -> str:
    """Flatten a pydantic ``loc`` to a dotted path, dropping the union-branch
    tag segments pydantic injects (``function-after``, ``str``) that mean
    nothing to a reader."""
    parts = [
        str(p)
        for p in loc
        if not (isinstance(p, str) and (p.startswith("function-") or p in {"str", "dict", "list"}))
    ]
    return ".".join(parts) if parts else "(value)"


def problems_from_validation_error(exc: Any) -> list[FieldProblem]:
    """Read a pydantic ``ValidationError``'s ALREADY-PARSED ``.errors()``.

    This is the whole point of the change: the exception literally names
    ``sources`` / ``pasted_text`` / ``query`` / ``host_count`` and says exactly
    what it wanted. Returns ``[]`` for anything that is not a ValidationError,
    so callers can try it unconditionally.
    """
    errors = getattr(exc, "errors", None)
    if not callable(errors):
        return []
    try:
        raw = errors()
    except Exception:  # noqa: BLE001 — never let failure reporting fail
        return []
    problems: list[FieldProblem] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        err_type = str(item.get("type") or "")
        _, expected = _PYDANTIC_TYPES.get(err_type, (Cause.INVALID_INPUT, None))
        if expected is None:
            # No mapping yet: the validator's own msg is still a real sentence
            # ("Value error, unregistered source_feature ..."), far better than
            # dropping to a generic phrase.
            expected = strip_ansi(str(item.get("msg") or "")).strip() or None
        problems.append(
            FieldProblem(
                field=_loc_to_field(tuple(item.get("loc") or ())),
                expected=expected,
                got=_render_got(item.get("input")),
                code=err_type or None,
            )
        )
    return problems


# A pydantic ValidationError that has ALREADY been stringified — by an engine
# wrapper ("Node 'ingest' failed at step 0: 1 validation error for …"), by a
# node that caught and re-raised, or by a row written before this module
# existed. The rendered form still holds every fact ``.errors()`` had:
#
#     1 validation error for IngestFromMediaRefsInput
#     sources
#       Field required [type=missing, input_value={}, input_type=dict]
#
# Parsing it recovers ``field``/``expected``/``got`` for those paths too.
# Preferring the live exception is always right — this is the fallback, and it
# is why the client needs no equivalent.
_VALIDATION_TEXT_HEADER = re.compile(r"\d+ validation errors? for \s*\S+")
_VALIDATION_TEXT_ENTRY = re.compile(
    r"^(?P<loc>\S[^\n]*)\n\s+(?P<msg>[^\n\[]+?)\s*\[type=(?P<type>[^,\]]+)"
    r"(?:,\s*input_value=(?P<input>.*?))?(?:,\s*input_type=[^\]]*)?\]",
    re.M | re.S,
)


def problems_from_validation_text(text: str) -> list[FieldProblem]:
    """Recover per-field problems from a STRINGIFIED pydantic ValidationError."""
    if not _VALIDATION_TEXT_HEADER.search(text):
        return []
    problems: list[FieldProblem] = []
    for match in _VALIDATION_TEXT_ENTRY.finditer(text):
        err_type = match.group("type").strip()
        _, expected = _PYDANTIC_TYPES.get(err_type, (Cause.INVALID_INPUT, None))
        if expected is None:
            expected = strip_ansi(match.group("msg")).strip() or None
        raw_input = match.group("input")
        problems.append(
            FieldProblem(
                field=_loc_to_field(tuple(match.group("loc").strip().split("."))),
                expected=expected,
                got=_render_got(raw_input.strip()) if raw_input else None,
                code=err_type or None,
            )
        )
    return problems


_DB_PERMISSION_TEXT = re.compile(
    r"InsufficientPrivilege|SQLSTATE:?\s*42501|PermissionDeniedError|"
    r"permission denied for (?:table|relation|view|schema|sequence|function)\b",
    re.I,
)
# "permission denied for table collection_run" + matrx-orm's hint
# "GRANT SELECT ON seo.collection_run TO authenticated" -> (verb, "seo.collection_run").
_DB_GRANT_HINT = re.compile(r"GRANT\s+(\w+)\s+ON\s+([\w.\"]+)\s+TO", re.I)
_DB_DENIED_FOR = re.compile(
    r"permission denied for (?:table|relation|view|schema|sequence|function)\s+([\w.\"]+)", re.I
)


def db_permission_target(text: str) -> tuple[str | None, str] | None:
    """(access verb, table) when ``text`` is a database permission refusal naming one."""
    if not text or not _DB_PERMISSION_TEXT.search(text):
        return None
    grant = _DB_GRANT_HINT.search(text)
    denied = _DB_DENIED_FOR.search(text)
    table = (grant.group(2) if grant else denied.group(1) if denied else "").replace('"', "")
    if not table:
        return None
    verb = (grant.group(1).upper() if grant else "")
    return ("read" if verb == "SELECT" else "write" if verb else None), table


# Message-shape ladder for exceptions that carry no structure of their own.
# This is NOT the client's regex table moved server-side: here it runs ONCE,
# at the raise site, with the exception type in hand, and its output is a
# stable ``cause`` that is then persisted — so it never runs again on read.
_MESSAGE_LADDER: tuple[tuple[re.Pattern[str], str], ...] = (
    # FIRST on purpose. These three are OUR OWN machine words, stamped by the
    # orchestrator — not prose to be interpreted. The rung must outrank every
    # other because the text following them is a TOOL's error message, which is
    # arbitrary English: a stalled `rulebook` loop whose tool said "that
    # Rulebook does not exist" would otherwise classify as NOT_FOUND and tell a
    # person something was deleted.
    (
        re.compile(
            r"\btool_loop_stalled\b|\bpaused_loop_guard\b|\bmax_iterations_exceeded\b",
        ),
        Cause.TOOL_LOOP_STALLED,
    ),
    # A DATABASE permission refusal (asyncpg InsufficientPrivilegeError / SQLSTATE
    # 42501, or matrx-orm's PermissionDeniedError wrapping it) is an access
    # refusal, never money. Outranks the credits rung: its driver class name holds
    # "Insufficient", and the table it names can hold "credit"/"balance"
    # (live 2026-10-27, runs efa6d55d + db21bda7 read "out of AI credits" for
    # "permission denied for table collection_run").
    (_DB_PERMISSION_TEXT, Cause.NOT_AUTHORIZED),
    (
        re.compile(r"coppa|consent[_ ]required|guardian|age[_ ]undeclared", re.I),
        Cause.CONSENT_REQUIRED,
    ),
    (
        re.compile(r"belongs to an organization|organization[_ ]id|no organization", re.I),
        Cause.NO_ORGANIZATION,
    ),
    # A Run Mandate step WIRED wrong, or a template/edge path that does not resolve, is the
    # workflow's own wiring — never "no AI assigned" (live 2026-10-27: runs c7665149 / 6971d928
    # read "has no AI assigned" because the text merely contained the word "mandate").
    (
        re.compile(
            r"outside provision_values|template path .{0,200}? does not resolve|"
            r"\bTemplatePathMissing\b",
            re.I,
        ),
        Cause.WIRING_BROKEN,
    ),
    # A gate's own sentence carried inside a ``MandateError`` ("Mandate 'x': <Agent> could not finish
    # this job: <the gate's sentence>"): the words are matrx-ai's fixed refusal sentences
    # (``run_approval_gate.REFUSAL_SENTENCES``, ``model_tier_gate.TOP_TIER_MESSAGE``). Before the
    # resolution ladder below so the spend hold / model access refusal keeps its honest cause.
    (
        re.compile(
            r"paused until that hour's volume drops|waiting for an administrator to approve its "
            r"spending|exceeds? its approval limit|cost more than its approval limit|"
            r"temporary approval ran out|administrator declined this agent's spending",
            re.I,
        ),
        Cause.SPEND_APPROVAL_REQUIRED,
    ),
    (re.compile(r"limited to approved accounts|top_tier_model_refused", re.I), Cause.MODEL_NOT_APPROVED),
    (
        re.compile(r"Refused: retry storm|paused by its guardrail|\(automation_guardrail\)", re.I),
        Cause.AUTOMATION_PAUSED,
    ),
    # ONLY a real resolution refusal: the job is unknown, nothing holds it, or its contract is
    # not declared in this process. The bare word "mandate" is NOT evidence — values a job refused
    # are an input problem (``problems_from_refusal_text`` names them before this ladder runs).
    (
        re.compile(
            r"could not be resolved|not found in mandate\.|no agent (is )?(assigned|bound)|"
            r"\bno holder\b|which no code in this process declares|MandateResolutionUnavailable",
            re.I,
        ),
        Cause.MANDATE_UNRESOLVED,
    ),
    # Before RATE_LIMITED and NOT_AUTHORIZED: a challenge page arrives as a 403,
    # 429 or 503, and the status word would otherwise name the wrong culprit.
    (
        re.compile(
            r"cloudflare|just a moment\.\.\.|bot[_ -]?(wall|protection|detection)|captcha|"
            r"\bwaf\b|challenge page|site_blocked",
            re.I,
        ),
        Cause.SITE_BLOCKED,
    ),
    # Before RATE_LIMITED and OUT_OF_CREDITS: the usage gate's refusal names the
    # person's plan limit, and its words ("usage limit", "upgrade your plan")
    # must never fall through to "our side" (live 2026-10-24, run ac8858af).
    (
        re.compile(
            r"UsageLimitReachedError|usage_limit_reached|guest_ai_allowance_used|"
            r"AI usage limit|free AI tries",
            re.I,
        ),
        Cause.USAGE_LIMIT_REACHED,
    ),
    (re.compile(r"rate limit|\b429\b|overloaded|too many requests", re.I), Cause.RATE_LIMITED),
    # "insufficient" alone is not money: asyncpg's InsufficientPrivilegeError is a
    # permission refusal and read "out of AI credits" (live 2026-10-27, run 6033f4dc).
    (
        re.compile(
            r"credit|quota|insufficient[ _-]?(?:funds|credits?|balance|quota)|billing|"
            r"balance|exceeded your",
            re.I,
        ),
        Cause.OUT_OF_CREDITS,
    ),
    (
        re.compile(r"content filter|safety|policy violation|refused to answer", re.I),
        Cause.CONTENT_FILTERED,
    ),
    (
        re.compile(r"permission|not authorized|unauthorized|forbidden|\b403\b|row.level|RLS", re.I),
        Cause.NOT_AUTHORIZED,
    ),
    (re.compile(r"timed out|timeout|deadline exceeded", re.I), Cause.TIMED_OUT),
    (re.compile(r"not found|\b404\b|does not exist|no such", re.I), Cause.NOT_FOUND),
    (
        re.compile(r"disallowed (call target|expression element)|permitted: constants", re.I),
        Cause.EXPRESSION_REJECTED,
    ),
    # OUTPUT_TRUNCATED runs BEFORE the unusable-output rule on purpose: a
    # truncated reply is also unparseable, and the node's code carries both
    # words. The node-level code (``output_truncated``, emitted by matrx-ai's
    # one classifier) and the human sentence ("cut off at its output limit")
    # both land here — live 2026-09-12, a 32,000-token ceiling hit was
    # persisted as engine_error because neither spelling matched.
    (
        re.compile(
            r"output_truncated|max_tokens|token cap|output limit|"
            r"truncated (?:mid|before|response)|ran out of room",
            re.I,
        ),
        Cause.OUTPUT_TRUNCATED,
    ),
    (
        re.compile(
            r"failed to produce valid|no JSON found|parse_failed|"
            r"structured_output_invalid|kind_output_missing|not valid JSON|"
            r"could not be parsed|could not parse (?:the )?(?:model|llm|response)",
            re.I,
        ),
        Cause.AI_OUTPUT_UNUSABLE,
    ),
    (re.compile(r"child run .* ended|child_run_errored", re.I), Cause.CHILD_RUN_FAILED),
    (
        re.compile(r"persistence ?barrier|write failure|failed to persist", re.I),
        Cause.PERSISTENCE_FAILED,
    ),
    (re.compile(r"provider|anthropic|openai|gemini|google rejected", re.I), Cause.PROVIDER_ERROR),
)

# Exception class name → cause, checked BEFORE the message ladder. The type is
# harder evidence than the prose.
_TYPE_CAUSES: dict[str, str] = {
    "NodeInputValidationError": Cause.MISSING_INPUT,
    "UnresolvedVariableError": Cause.UNRESOLVED_VARIABLE,
    "EdgeRoutingError": Cause.WIRING_BROKEN,
    "CompilationError": Cause.DEFINITION_INVALID,
    "DefinitionError": Cause.DEFINITION_INVALID,
    "ValidationError": Cause.INVALID_INPUT,
    "NodeTimeoutError": Cause.TIMED_OUT,
    "ActionAuthorizationError": Cause.NOT_AUTHORIZED,
    "PermissionError": Cause.NOT_AUTHORIZED,
    "EducationConsentRequiredError": Cause.CONSENT_REQUIRED,
    # matrx-ai's usage gate: the class name and the two refusal codes it stamps.
    "UsageLimitReachedError": Cause.USAGE_LIMIT_REACHED,
    "usage_limit_reached": Cause.USAGE_LIMIT_REACHED,
    "guest_ai_allowance_used": Cause.USAGE_LIMIT_REACHED,
    "PersistenceBarrierError": Cause.PERSISTENCE_FAILED,
    "IntegrityError": Cause.PERSISTENCE_FAILED,
    # A lock collision the database broke (matrx-orm's typed refusal, or asyncpg's raw 55P03): the
    # statement rolled back in full, so the honest sentence is "busy, run it again".
    "LockContentionError": Cause.DATABASE_BUSY,
    "LockNotAvailableError": Cause.DATABASE_BUSY,
    "asyncio.CancelledError": Cause.CANCELLED,
    "CancelledError": Cause.CANCELLED,
    # matrx-orm says "this is the DATABASE" in its class name. Before 2026-09-12
    # none of these were here, so every one of them fell through to the prose
    # ladder — over a message with the statement's args attached.
    "PermissionDeniedError": Cause.NOT_AUTHORIZED,
    "InsufficientPrivilegeError": Cause.NOT_AUTHORIZED,
    # SQLSTATE P0002 — our functions' honest access refusal ("dataset … is not
    # available to this account"). A refusal, never "couldn't save the result".
    "RecordNotAvailableError": Cause.NOT_AUTHORIZED,
    # Not an exception class — the ``error_type`` matrx-ai stamps on a stalled
    # tool loop. ``cause_from_text`` checks this map by name first, so the
    # machine word settles it before any prose is read.
    "tool_loop_stalled": Cause.TOOL_LOOP_STALLED,
    "TemplatePathMissing": Cause.WIRING_BROKEN,
    # Spend refusals (matrx-ai providers/run_approval_gate + the host's per-run spend gate).
    "run_approval_required": Cause.SPEND_APPROVAL_REQUIRED,
    "top_tier_model_refused": Cause.MODEL_NOT_APPROVED,
    "automation_guardrail": Cause.AUTOMATION_PAUSED,
    "TopTierModelRefusedError": Cause.MODEL_NOT_APPROVED,
    "run_spend_limit_reached": Cause.SPEND_APPROVAL_REQUIRED,
    "RunApprovalRequiredError": Cause.SPEND_APPROVAL_REQUIRED,
    "protected_account_run_refused": Cause.NOT_AUTHORIZED,
    "ProtectedAccountRunRefusedError": Cause.NOT_AUTHORIZED,
    # subgraph.call's own Failure codes (the scheduler passes a returned Failure's code as its type): a child
    # that did not hand back an answer is child_run_failed STRUCTURALLY, never read off the sentence, which
    # names the child workflow ("Permissions audit" read not_authorized, 2026-10-27).
    "child_run_failed": Cause.CHILD_RUN_FAILED,
    "child_run_errored": Cause.CHILD_RUN_FAILED,
}

#: Causes that are a GATE or a refusal, never a fault in the steps that ran: the remedy is outside the
#: run (billing, access, an approval, an organization, our own write). A step whose code IS one of these
#: keeps it as its cause, and a called workflow that stopped on one hands it up unchanged — the caller's
#: person reads "reached its AI usage limit" + Open Billing, never "press Run it again" behind a generic
#: ``child_run_failed`` (2026-10-27 review). ``mandate_unresolved`` is the child's own binding, so the
#: caller reads ``child_run_failed`` and opens the child.
GATE_CAUSES: frozenset[str] = frozenset(
    {
        Cause.NO_ORGANIZATION,
        Cause.CONSENT_REQUIRED,
        Cause.NOT_AUTHORIZED,
        Cause.OUT_OF_CREDITS,
        Cause.USAGE_LIMIT_REACHED,
        Cause.MODEL_NOT_APPROVED,
        Cause.AUTOMATION_PAUSED,
        Cause.HELD_FOR_APPROVAL,
        Cause.SPEND_APPROVAL_REQUIRED,
        Cause.REFUSED,
        Cause.PERSISTENCE_FAILED,
        Cause.DATABASE_BUSY,
    }
)

#: Gate causes that are OUR failure, so a step that stopped on one may be retried, re-dispatched or
#: resumed — never a caller refusal.
OUR_GATE_CAUSES: frozenset[str] = frozenset({Cause.PERSISTENCE_FAILED, Cause.DATABASE_BUSY})

#: The persistence family, by class name. Anything here is OUR write failing,
#: never the person's input and never a gate they must clear.
_PERSISTENCE_TYPES: frozenset[str] = frozenset(
    {
        # matrx-orm
        "QueryTimeoutError",
        "PoolAcquireTimeoutError",
        "LockContentionError",
        "DatabaseError",
        "DatabaseConnectError",
        "UnknownDatabaseError",
        "SchemaMismatchError",
        "TransactionError",
        "ReadOnlyTransactionError",
        "ReadOnlyModelError",
        "QueryError",
        "ParameterError",
        "OptimisticLockError",
        "WriteQueueFullError",
        "WriteQueueTimeoutError",
        # matrx-graph's own
        "CheckpointError",
        "CheckpointWriteFailedError",
    }
)

for _name in _PERSISTENCE_TYPES:
    _TYPE_CAUSES.setdefault(_name, Cause.PERSISTENCE_FAILED)


def persistence_cause_for_exception(exc: BaseException) -> str | None:
    """The cause established by the exception's CLASS, or None.

    Walks the real MRO, so an ORM error class added tomorrow — or a host
    subclass of one — classifies without being listed. A ``matrx_orm``
    exception is a persistence failure by definition: the database refused or
    could not complete OUR write, which is never something the person did.
    """
    for klass in type(exc).__mro__:
        name = klass.__name__
        mapped = _TYPE_CAUSES.get(name)
        if mapped is not None:
            return mapped
        module = getattr(klass, "__module__", "") or ""
        if module.split(".")[0] == "matrx_orm" and name.endswith(("Error", "Exception")):
            return Cause.PERSISTENCE_FAILED
    return None


def cause_from_text(text: str, error_type: str | None = None) -> str:
    """Best cause for a message we have no structure for. Type first, prose second.

    The prose leg reads :func:`classification_text` — never the raw text. See
    the module docstring: the raw text can contain the person's documents, and a
    ladder that matches them lies to her about her own account.
    """
    if error_type and error_type in _TYPE_CAUSES:
        return _TYPE_CAUSES[error_type]
    safe = classification_text(text)
    for pattern, cause in _MESSAGE_LADDER:
        if pattern.search(safe):
            return cause
    return Cause.ENGINE_ERROR


_ENGINE_ERROR_SENTENCE = (
    "Something went wrong on our side, not with what you entered. Try again; if it stops again, tell us."
)


def _sentence(cause: str, *, step_label: str | None, problem: FieldProblem | None) -> str:
    """The one human sentence, generated from the STRUCTURE.

    Generated — not written per workflow. "Study Pack needs the material you
    paste in — that box was empty" comes out of ``step_label`` + ``field`` +
    the cause, with no pattern authored for Study Pack anywhere.
    """
    where = step_label or "This step"
    if problem is not None and problem.field and problem.field != "(value)":
        name = problem.field.replace("_", " ").replace(".", " → ")
        if cause == Cause.MISSING_INPUT:
            return f"{where} needs “{name}”, and it was empty."
        want = f" — it expects {problem.expected}" if problem.expected else ""
        return f"{where} couldn't use the “{name}” it was given{want}."
    defaults = {
        Cause.HELD_FOR_APPROVAL: (
            f"{where} is waiting for your approval — nothing was written yet."
        ),
        Cause.REFUSED: (
            f"{where}'s change was refused, so nothing was written and the run ended there."
        ),
        Cause.SPEND_APPROVAL_REQUIRED: (
            f"{where} didn't run — this run is waiting for spending approval."
        ),
        Cause.MISSING_INPUT: f"{where} is missing something it needs.",
        Cause.INVALID_INPUT: f"{where} was given a value it couldn't use.",
        Cause.UNRESOLVED_VARIABLE: f"{where} referred to a value this run never received.",
        Cause.DEFINITION_INVALID: "This workflow doesn't yet hold together, so it never started.",
        Cause.WIRING_BROKEN: f"{where} never received what the step before it was meant to hand over.",
        Cause.NO_ORGANIZATION: "This run couldn't tell which workspace to run in.",
        Cause.CONSENT_REQUIRED: "This account needs an age check before AI can run.",
        Cause.NOT_AUTHORIZED: "This run isn't allowed to reach something it needs.",
        Cause.MANDATE_UNRESOLVED: f"{where} has no AI assigned to do the job.",
        Cause.AUTOMATION_PAUSED: f"{where} didn't run — this automation is paused by its safety limit.",
        Cause.MODEL_NOT_APPROVED: f"{where} didn't run — its AI model is limited to approved accounts.",
        Cause.OUT_OF_CREDITS: "This workspace is out of AI credits.",
        Cause.USAGE_LIMIT_REACHED: f"{where} didn't run — this account reached its AI usage limit.",
        Cause.SITE_BLOCKED: f"{where} was turned away by the website's bot protection.",
        Cause.RATE_LIMITED: f"{where} couldn't get through — the AI provider was too busy.",
        Cause.CONTENT_FILTERED: "The AI declined this job — something tripped its safety filter.",
        Cause.PROVIDER_ERROR: f"{where} couldn't complete — the AI provider returned an error.",
        Cause.AI_OUTPUT_UNUSABLE: (
            f"{where} got an answer from the AI, but not in the form it needs."
        ),
        Cause.OUTPUT_TRUNCATED: f"{where} ran out of room mid-answer and stopped short.",
        Cause.TOOL_LOOP_STALLED: (
            f"{where} kept retrying a tool that kept failing, so it was stopped. "
            f"The details name the tool and what it said — that tool, or the value "
            f"this step gives it, is what needs fixing."
        ),
        Cause.EXPRESSION_REJECTED: (f"{where} uses a formula the safe evaluator won't run."),
        Cause.NOT_FOUND: f"{where} looked for something that isn't there any more.",
        Cause.TIMED_OUT: f"{where} ran past its time limit and was stopped.",
        Cause.CANCELLED: "This run was canceled before it finished.",
        Cause.RUN_STRANDED: "This run was dropped by our system before it could finish.",
        Cause.CHILD_RUN_FAILED: f"{where} runs another workflow, and that one stopped.",
        Cause.PERSISTENCE_FAILED: f"{where} finished its work but couldn't save the result.",
        Cause.DATABASE_BUSY: f"{where} stopped because the database was busy. Run it again.",
        # The honest fallback tells the person what happened and what to do, never the step's label:
        # "Read the request stopped partway through." named engine plumbing (live 2026-10-22). The
        # technical detail stays on the record (``technical``), never in this line.
        Cause.ENGINE_ERROR: _ENGINE_ERROR_SENTENCE,
    }
    return defaults.get(cause, _ENGINE_ERROR_SENTENCE)


# "EdgeRoutingError: edge 'e_plan…" → "EdgeRoutingError". Anchored and
# CamelCase-shaped so it cannot swallow an ordinary sentence that happens to
# contain a colon.
# THE VALUES A JOB REFUSED, named (2026-10-27). A mandate that refuses because a value it
# guarantees was not given, or was the wrong shape, is the CALL's input problem — it said "has no
# AI assigned to do the job" for months (run d92b06b3: "charter: guaranteed offered value was not
# supplied"), sending the reader to the agent binding instead of the missing value. The refusal
# texts are our own two formats (aidream ``ProvisionInputError`` and the holder-input refusal);
# parsing our own words at our own boundary, once, like ``_problem_from_gate_line``.
_REFUSAL_HEADS = (
    re.compile(r"this run cannot start on the values it was given\s+[—-]+\s+(?P<body>.+)", re.S),
    re.compile(r"did not get every value it requires:\s+(?P<body>.+?)(?:\.\s+(?:Nothing in this binding|The binding)|\.?$)", re.S),
    re.compile(r"(?P<body>references workflow input '[^']+' but no value landed.*)", re.S),
)
_REFUSAL_ENTRY = re.compile(r"^\s*(?P<field>[A-Za-z_][\w.]*)\s*:\s*(?P<detail>.+)$", re.S)
_INPUT_NO_VALUE = re.compile(r"references workflow input '(?P<field>[^']+)' but no value landed")
_REFUSAL_MISSING = re.compile(
    r"not supplied|guarantees this value|\babsent\b|nothing left after|no value landed", re.I
)
_TRAILING_BRACKET = re.compile(r"\s*\[[^\[\]]*\]\s*$")


def problems_from_refusal_text(text: str) -> list[FieldProblem]:
    """The fields a refused job named, recovered from its refusal text (empty when none)."""
    text = strip_ansi(text or "")
    for head in _REFUSAL_HEADS:
        match = head.search(text)
        if not match:
            continue
        body = _TRAILING_BRACKET.sub("", match.group("body")).strip()
        no_value = _INPUT_NO_VALUE.search(body)
        if no_value:
            return [FieldProblem(field=no_value.group("field"), expected="a value", got="nothing", code="missing")]
        problems: list[FieldProblem] = []
        for part in re.split(r";\s+(?=[A-Za-z_][\w.]*\s*:)", body):
            entry = _REFUSAL_ENTRY.match(part.strip())
            if not entry:
                continue
            detail = entry.group("detail").strip()
            missing = bool(_REFUSAL_MISSING.search(detail))
            problems.append(
                FieldProblem(
                    field=entry.group("field"),
                    expected="a value" if missing else re.sub(r"^expected\s+", "", detail)[:300],
                    got="nothing" if missing else None,
                    code="missing" if missing else "invalid",
                )
            )
        if problems:
            return problems
    return []


def _refusal_message(step_label: str | None, problems: list[FieldProblem]) -> str | None:
    """One sentence naming EVERY missing value (the generated sentence names only the first)."""
    missing = [p.field.replace("_", " ") for p in problems if p.code == "missing" and p.field]
    if not missing or len(missing) != len(problems):
        return None
    if len(missing) == 1:
        return f"{step_label or 'This step'} needs “{missing[0]}”, and it was not given."
    names = ", ".join(f"“{m}”" for m in missing[:-1]) + f" and “{missing[-1]}”"
    return f"{step_label or 'This step'} needs {names}, and they were not given."


def _failure_from_refusal(
    text: str, *, step_id: str | None, step_label: str | None, error_type: str | None
) -> RunFailure | None:
    problems = problems_from_refusal_text(text)
    if not problems:
        return None
    missing = all(p.code == "missing" for p in problems)
    return build_failure(
        cause=Cause.MISSING_INPUT if missing else Cause.INVALID_INPUT,
        technical=text,
        step_id=step_id,
        step_label=step_label,
        error_type=error_type,
        problems=problems,
        message=_refusal_message(step_label, problems),
    )


_LEADING_EXC_TYPE = re.compile(r"^(?P<type>[A-Z][A-Za-z0-9_]*(?:Error|Exception|Interrupt)):")
#: Wrapper exception types that carry another failure's text; the class opening that text is the cause.
_WRAPPER_TYPES: frozenset[str] = frozenset({"ExecutionError"})


def failure_from_text(
    text: str,
    *,
    step_id: str | None = None,
    step_label: str | None = None,
    error_type: str | None = None,
) -> RunFailure:
    """Best structure obtainable when all we hold is a string.

    Used by the store boundary for callers that never had an exception (a
    sweeper, a host route) and by the engine when a failure arrives already
    flattened. Tries the stringified-ValidationError parser first, then falls
    back to the type/prose ladder.
    """
    prefix = _LEADING_EXC_TYPE.match(text)
    if error_type is None:
        # 108 of the 144 live messages open with a raw exception class name
        # ("EdgeRoutingError: …", "NodeInputValidationError: …"). When all we
        # have is the string, that prefix is the same hard evidence the
        # exception's type would have been — recover it rather than dropping
        # to prose matching.
        error_type = prefix.group("type") if prefix else None
    elif error_type in _WRAPPER_TYPES and prefix and prefix.group("type") in _TYPE_CAUSES:
        # The generic wrapper says nothing; the known class it wraps does (a QueryTimeoutError while saving a
        # step's result is OUR write failing, never "the step ran past its time limit" — run bcf4958b).
        error_type = prefix.group("type")

    problems = problems_from_validation_text(text)
    if problems:
        missing = all(p.code in {"missing", "too_short", "string_too_short"} for p in problems)
        return build_failure(
            cause=Cause.MISSING_INPUT if missing else Cause.INVALID_INPUT,
            technical=text,
            step_id=step_id,
            step_label=step_label,
            error_type=error_type,
            problems=problems,
        )
    refused = _failure_from_refusal(
        text, step_id=step_id, step_label=step_label, error_type=error_type
    )
    if refused is not None:
        return refused
    return build_failure(
        cause=cause_from_text(text, error_type=error_type),
        technical=text,
        step_id=step_id,
        step_label=step_label,
        error_type=error_type,
    )


def build_failure(
    *,
    cause: str,
    technical: str,
    step_id: str | None = None,
    step_label: str | None = None,
    error_type: str | None = None,
    problems: list[FieldProblem] | None = None,
    message: str | None = None,
) -> RunFailure:
    """Assemble a :class:`RunFailure` with every string ANSI-stripped."""
    problems = problems or []
    primary = problems[0] if problems else None
    access = db_permission_target(technical) if cause == Cause.NOT_AUTHORIZED else None
    access_sentence = (
        f"This step can't {access[0] or 'reach'} {access[1]} with your access." if access else None
    )
    return RunFailure(
        cause=cause,
        message=client_error_text(message)
        or access_sentence
        or _sentence(cause, step_label=step_label, problem=primary),
        step_id=step_id,
        step_label=step_label,
        field=primary.field if primary else None,
        expected=primary.expected if primary else None,
        got=primary.got if primary else None,
        fields=problems,
        error_type=error_type,
        technical=client_error_text(technical, limit=TECHNICAL_TEXT_LIMIT) or None,
    )


#: Ceiling on the persisted/wired ``technical`` text — room for a real reason,
#: never room for a payload.
TECHNICAL_TEXT_LIMIT = 8000

#: The keys of an error payload that carry prose a client renders. Only these are
#: redacted — ``got`` / ``details`` values are the person's own data and are
#: never rewritten.
_CLIENT_PROSE_KEYS = ("message", "error_message", "technical", "technical_message")


def client_safe_error_payload(error: Any) -> Any:
    """Redact the prose keys of an error dict (and its ``error`` / ``details``
    children) for a client: no ANSI, SQL, bound args, tracebacks or hints.

    THE gate on every client-bound error payload — the workflow event models
    and the ``workflow.run.error`` / ``node_outcome.error`` store boundary both
    call it, so a payload assembled anywhere cannot carry a terminal banner out.
    """
    if not isinstance(error, dict):
        return error
    out = dict(error)
    for key in _CLIENT_PROSE_KEYS:
        value = out.get(key)
        if isinstance(value, str):
            limit = TECHNICAL_TEXT_LIMIT if key.startswith("technical") else None
            cleaned = (
                client_error_text(value, limit=limit) if limit else client_error_text(value)
            )
            out[key] = cleaned or ("" if not value.strip() else _REDACTED_FALLBACK)
    for child in ("error", "details", "wrapper"):
        if isinstance(out.get(child), dict):
            out[child] = client_safe_error_payload(out[child])
    return out


def _is_orm_exception(exc: BaseException) -> bool:
    return any(
        (getattr(klass, "__module__", "") or "").split(".")[0] == "matrx_orm"
        for klass in type(exc).__mro__
    )


_REDACTED_FALLBACK = "This step stopped with an internal error. The details are in our logs."


def client_message_for_exception(exc: BaseException, *, step_label: str | None = None) -> str:
    """The one sentence a client is shown for a raised exception.

    Order: the exception's own ``person_message`` (or a structured refusal's
    ``error_info.user_message``); then, for a class that settles the cause
    (every ``matrx_orm`` error, authorization, cancellation), the generated
    sentence for that cause — an ORM exception's ``str()`` is a terminal banner
    with the statement's bound args, and is NEVER a client message; then the
    exception's own text through :func:`client_error_text`.
    """
    person = getattr(exc, "person_message", None)
    if isinstance(person, str) and person.strip():
        return client_error_text(person) or person.strip()
    user_message = getattr(getattr(exc, "error_info", None), "user_message", None)
    if isinstance(user_message, str) and user_message.strip():
        return client_error_text(user_message) or user_message.strip()
    if _is_orm_exception(exc):
        return failure_from_exception(exc, step_label=step_label).message
    return client_error_text(str(exc)) or _sentence(
        Cause.ENGINE_ERROR, step_label=step_label, problem=None
    )


def gate_failure(
    node_error: Any,
    *,
    technical: str,
    step_id: str | None,
    step_label: str | None,
) -> RunFailure | None:
    """A node's ``Failure`` whose code IS a gate cause (:data:`GATE_CAUSES`): that cause, the node's
    own sentence and its approval link — before any prose is read. ONE classification for the run's
    failure (:func:`failure_from_exception`) and the step's outcome (the scheduler's returned-failure
    path), so a called workflow's gate reads the same on the step and on the run (2026-10-27)."""
    code = str(getattr(node_error, "code", "") or "")
    if code not in GATE_CAUSES:
        return None
    details = getattr(node_error, "details", None)
    approval_url = details.get("approval_url") if isinstance(details, dict) else None
    gated = build_failure(
        cause=code, technical=technical, step_id=step_id, step_label=step_label,
        error_type=code, message=strip_ansi(str(getattr(node_error, "message", "") or "")) or None,
    )
    if isinstance(approval_url, str) and approval_url:
        return gated.model_copy(update={"approval_url": approval_url})
    return gated


def _refusal_failure(
    node_error: Any,
    *,
    code: str,
    node_message: str,
    technical: str,
    step_id: str | None,
    step_label: str | None,
) -> RunFailure | None:
    """A CALLER REFUSAL's run failure: the gate's own sentence, the refusal's cause, and the
    approval link — never ``engine_error``'s "something went wrong on our side" (live run
    1aa73a14, 2026-10-27, told a person its spend hold was our fault)."""
    details = getattr(node_error, "details", None)
    if not isinstance(details, dict) or details.get("caller_refusal") is not True:
        return None
    refusal_code = str(details.get("refusal_code") or details.get("error_type") or code)
    approval_url = details.get("approval_url")
    approval_url = str(approval_url) if isinstance(approval_url, str) and approval_url else None
    cause = (refusal_code if refusal_code in GATE_CAUSES else None) or _TYPE_CAUSES.get(refusal_code) or (
        Cause.SPEND_APPROVAL_REQUIRED if approval_url else Cause.NOT_AUTHORIZED
    )
    failure = build_failure(
        cause=cause,
        technical=technical,
        step_id=step_id,
        step_label=step_label,
        error_type=refusal_code,
        message=node_message or None,
    )
    return failure.model_copy(update={"approval_url": approval_url}) if approval_url else failure


def _approval_refusal_in(exc: BaseException, *, max_depth: int = 16) -> tuple[BaseException, str] | None:
    """The caller refusal on ``exc``'s chain that names where a person approves it, with that link."""
    seen: set[int] = set()
    stack: list[Any] = [exc]
    while stack and len(seen) < max_depth:
        node = stack.pop()
        if node is None or id(node) in seen:
            continue
        seen.add(id(node))
        approval_url = getattr(node, "approval_url", None)
        if getattr(node, "is_caller_refusal", False) is True and isinstance(approval_url, str) and approval_url:
            return node, approval_url
        # Explicit wrapping only (``raise ... from``, a carried exception): an exception merely
        # raised WHILE handling a refusal (``__context__``) is not that refusal.
        for attr in ("__cause__", "terminal_exception", "exception"):
            carried = getattr(node, attr, None)
            if isinstance(carried, BaseException):
                stack.append(carried)
    return None


def failure_from_exception(
    exc: BaseException,
    *,
    step_id: str | None = None,
    step_label: str | None = None,
) -> RunFailure:
    """Derive the structure from whatever the exception already carries.

    Order matters — richest evidence first:

    0. the exception's CLASS, when the class alone settles it — a ``matrx_orm``
       or ``CheckpointError`` failure is persistence, full stop (and an
       exception carrying its own ``person_message`` already knows how to say
       so in plain English). This runs before any text is read;
    1. a pydantic ``ValidationError`` (directly, or wrapped as ``__cause__`` /
       ``__context__`` by an engine error that re-raised it) → per-field facts;
    2. ``NodeInputValidationError.field_errors`` → the engine's own per-field
       list, produced by the JSON-Schema input gate;
    3. ``NodeFailureError.node_error`` → the node's structured ``NodeError``
       whose ``code`` is already a stable machine key;
    4. the exception's TYPE, then its prose.
    """
    error_type = type(exc).__name__
    technical = f"{error_type}: {exc}"

    node_id = getattr(exc, "node_id", None)
    if isinstance(node_id, str) and node_id and step_id is None:
        step_id = node_id

    person_message = getattr(exc, "person_message", None)
    person_message = person_message if isinstance(person_message, str) and person_message else None

    # 0 — the class, when the class alone settles it. Persistence and the
    # cancellation/authorization families need no prose, and reading prose here
    # is what turned a checkpoint timeout into an age-verification refusal.
    class_cause = persistence_cause_for_exception(exc)
    if class_cause in {Cause.PERSISTENCE_FAILED, Cause.DATABASE_BUSY, Cause.NOT_AUTHORIZED, Cause.CANCELLED}:
        return build_failure(
            cause=class_cause,
            technical=technical,
            step_id=step_id,
            step_label=step_label,
            error_type=error_type,
            message=person_message,
        )

    # 0b — a RAISED caller refusal carrying where a person approves it (matrx-ai's
    # RunApprovalRequiredError under tool.call / an action, possibly wrapped): its own cause and
    # sentence, and the approval link — never a spend hold without its Approve link (2026-10-27).
    approval = _approval_refusal_in(exc)
    if approval is not None:
        refusal, approval_url = approval
        refusal_sentence = getattr(refusal, "message", None)
        # A refusal that names its own gate (``refusal_code``: a called mandate's ``held_for_approval``)
        # is that gate; otherwise its class decides, and a link alone means a spend hold.
        named = getattr(refusal, "refusal_code", None)
        gated = build_failure(
            cause=(named if named in GATE_CAUSES else None)
            or persistence_cause_for_exception(refusal)
            or Cause.SPEND_APPROVAL_REQUIRED,
            technical=technical,
            step_id=step_id,
            step_label=step_label,
            error_type=type(refusal).__name__,
            message=person_message or (refusal_sentence if isinstance(refusal_sentence, str) else None),
        )
        return gated.model_copy(update={"approval_url": approval_url})

    # 1 — pydantic, here or one hop down the __cause__/__context__ chain.
    for candidate in (exc, getattr(exc, "__cause__", None), getattr(exc, "__context__", None)):
        if candidate is None:
            continue
        problems = problems_from_validation_error(candidate)
        if problems:
            missing = all(p.code in {"missing", "too_short", "string_too_short"} for p in problems)
            return build_failure(
                cause=Cause.MISSING_INPUT if missing else Cause.INVALID_INPUT,
                technical=technical,
                step_id=step_id,
                step_label=step_label,
                error_type=error_type,
                problems=problems,
            )

    # 2 — the engine's JSON-Schema input gate, which reports per field already.
    field_errors = getattr(exc, "field_errors", None)
    if isinstance(field_errors, list) and field_errors:
        problems = [p for p in (_problem_from_gate_line(str(line)) for line in field_errors) if p]
        if problems:
            missing = all(p.code == "missing" for p in problems)
            return build_failure(
                cause=Cause.MISSING_INPUT if missing else Cause.INVALID_INPUT,
                technical=technical,
                step_id=step_id,
                step_label=step_label,
                error_type=error_type,
                problems=problems,
            )

    # 3 — a returned Failure envelope's NodeError: ``code`` is already stable.
    node_error = getattr(exc, "node_error", None)
    if node_error is not None:
        code = str(getattr(node_error, "code", "") or "")
        node_message = strip_ansi(str(getattr(node_error, "message", "") or ""))
        refusal = _refusal_failure(
            node_error, code=code, node_message=node_message, technical=technical,
            step_id=step_id, step_label=step_label,
        )
        if refusal is not None:
            return refusal
        gated = gate_failure(
            node_error, technical=technical, step_id=step_id, step_label=step_label
        )
        if gated is not None:
            return gated
        refused = _failure_from_refusal(
            node_message, step_id=step_id, step_label=step_label, error_type=code or error_type
        )
        if refused is not None:
            return refused
        return build_failure(
            # A code that IS a cause is the cause — no prose ladder second-guesses it. The code is also the
            # type ``_TYPE_CAUSES`` reads first (as the scheduler's step failure does): a failed child is
            # ``child_run_failed`` whatever the child workflow is named ("Permissions audit", 2026-10-27).
            cause=cause_from_text(f"{code} {node_message}", error_type=code or None),
            technical=technical,
            step_id=step_id,
            step_label=step_label,
            error_type=code or error_type,
            message=node_message or None,
        )

    # 4 — nothing structured left. failure_from_text still recovers per-field
    # facts from a ValidationError that some layer already stringified before
    # it reached us, then falls back to the type/prose ladder.
    derived = failure_from_text(
        technical, step_id=step_id, step_label=step_label, error_type=error_type
    )
    # ...but an exception that already knows how to say it in plain English is
    # BELIEVED, exactly as at step 0. The derived sentence for a cause is a
    # generic one ("This step ran past its time limit and was stopped."), true
    # and a shrug: no step, no ceiling, no remedy. NodeTimeoutError knows all
    # three (2026-09-15), and dropping that is the silent-failure shape.
    if person_message is not None:
        return derived.model_copy(update={"message": person_message})
    return derived


# The input gate formats each violation as "<path>: <jsonschema message>", e.g.
# "(value): 'topic' is a required property" or "sources: [] is too short".
_GATE_LINE = re.compile(r"^\s*(?:-\s*)?(?P<path>[^:]*?)\s*:\s*(?P<detail>.+)$", re.S)
_GATE_REQUIRED = re.compile(r"'(?P<name>[^']+)' is a required property")


def _problem_from_gate_line(line: str) -> FieldProblem | None:
    """Turn ONE ``NodeInputValidationError.field_errors`` line back into structure.

    The gate already knew the field; it just formatted it into prose on the way
    out. Parsing our OWN format at our OWN boundary is not the client-side
    guessing this change removes — the result is persisted as ``field``, so it
    is parsed once, here, forever.
    """
    line = strip_ansi(line).strip()
    if not line:
        return None
    match = _GATE_LINE.match(line)
    path, detail = (match.group("path"), match.group("detail")) if match else ("(value)", line)
    required = _GATE_REQUIRED.search(detail)
    if required:
        name = required.group("name")
        field = f"{path}.{name}" if path and path not in {"(value)", ""} else name
        return FieldProblem(field=field, expected="a value", got="nothing", code="missing")
    return FieldProblem(
        field=path or "(value)",
        expected=detail,
        got=None,
        code="invalid",
    )


def stranded_failure(*, technical: str, message: str | None = None) -> RunFailure:
    """The run our system dropped — never the person's failure.

    Used by every force-fail path (the watchdog sweep, the cleanup script, the
    ``/runs/{id}/force-fail`` endpoint). Its own cause exists so the UI can say
    the truth — *our system dropped this; here's your run back* — and never
    render it as "your run failed".
    """
    return build_failure(
        cause=Cause.RUN_STRANDED,
        technical=technical,
        message=message
        or (
            "This run was dropped by our system before it could finish — nothing you did caused it."
        ),
        error_type="run_stranded",
    )
