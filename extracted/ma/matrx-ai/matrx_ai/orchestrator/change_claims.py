"""THE CHANGE-CLAIM GATE — a turn that SAYS it changed something must have WRITTEN it.

On 2026-09-12 the Masterwork Conductor (mandate ``masterwork.conductor``,
conversation ``2050e02b-c663-4b6d-99f8-7996eff7cd81``) answered a
non-technical Expert twice in the past tense — 21:12Z/21:14Z *"Every critical
list-creating node now caps at 25 findings… Ready for you to run"*, 23:19Z
*"All agent changes (prompts, input/output schemas) saved as of … All changes
made now and live"* — while its tool ledger for those turns was EMPTY
(``chat.tool_trace`` held nothing after 22:00Z; the workflow definition and the
agents' rows were untouched). It only acted after the Expert wrote back
"nothing changed". An Expert cannot detect that except by trusting it and
losing a run, and trust is the whole product.

So the runtime — not the prompt — checks the claim against the ledger at the
turn-completion boundary, exactly as the required-member gate checks a declared
member against the same ledger (``required_members.py``, ruling D-38):

1. ``evaluate_change_claims`` — did THIS turn's model text assert that the
   artefact changed, while no write-capable tool call succeeded?
2. ``decide_change_claim_action`` — force one more turn ("make them with your
   tools or say plainly that you did not"), or, once the budget is spent,
   DISCLOSE to the person that nothing was saved. Never silence.

Three disciplines this module is built around:

* **The class, not the Conductor.** Whether a mandate's job is to WRITE is
  DECLARED DATA (``declare_mandate(..., authoring=True)``) and reaches this
  package through one injected host seam (``_ext.get_authoring_mandate_policy``),
  never a key list frozen in code.
* **Model text only.** The detector reads what the MODEL wrote this turn
  (``_assistant_text_from_response``'s position invariant) — never user content,
  never history, never tool results. A person who writes "nothing was saved" is
  not making a claim, and must never be matched as if they were.
* **Conservative.** A sentence is a claim only when it asserts a completed
  effect on the artefact. Anything hypothetical, future, negated, or
  interrogative is dropped BEFORE matching, and the text is bounded the way
  ``matrx_utils.error_text.classification_text`` bounds a classifier's input —
  a pasted document in the reply can never dominate the match.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from matrx_ai.orchestrator.tracking import ToolCallUsage

#: Hard ceiling on the model text the detector may inspect. Same reasoning as
#: ``matrx_utils.error_text.CLASSIFY_TEXT_LIMIT``: long enough for any real
#: report-back, short enough that a reply carrying a pasted artefact cannot
#: swamp it. A claim about the work always appears in the first screens of it.
CLAIM_TEXT_LIMIT = 6000

#: ``_completion_meta`` key stamped when a turn finished still claiming a change
#: it never wrote. A delivered answer is never retracted — but the run's durable
#: record says what happened, and the person is told (see the warning below).
UNBACKED_CHANGE_CLAIM_META_KEY = "unbacked_change_claim"

#: Event vocabulary (orchestrator FEATURE.md § The change-claim gate):
#:   warning "change_claim_correction"   — one forced turn, tools still in hand
#:   warning "change_claim_unbacked"     — terminal disclosure to the person
CHANGE_CLAIM_CORRECTION_CODE = "change_claim_correction"
CHANGE_CLAIM_UNBACKED_CODE = "change_claim_unbacked"

#: What the PERSON reads when the turn ends still claiming a change nobody made.
#: Deliberately flat and free of jargon — the Expert's next act is to re-ask, and
#: a hedge here would cost them another run.
CHANGE_CLAIM_USER_DISCLOSURE = (
    "No changes were saved this turn. The reply above describes changes, but "
    "nothing was written — treat the work as not yet done and ask for it again."
)

#: The forced turn's system notice. Both honest exits are named, because
#: "say plainly that you did not" is a fully acceptable answer and a model told
#: only to "make the changes" will invent a tool call instead of admitting it.
CHANGE_CLAIM_CORRECTION_NOTICE = (
    "⚠️ SYSTEM NOTICE (not from the user): your reply states that changes were "
    "made — {claims} — but this turn performed no successful write through any "
    "of your tools, so NOTHING was saved and the person would have believed "
    "otherwise. Do exactly one of two things now: make the changes with your "
    "tools (and then report only what the tool results actually confirm), or "
    "say plainly that you did NOT make them and what you need in order to. "
    "Never restate a change you have not written."
)

# ── Sentence disqualifiers: read BEFORE any claim pattern ───────────────────
# A sentence carrying any of these is not an assertion about a completed change,
# so it never reaches the patterns. Order matters for nothing; presence does.

#: Future / conditional / offer / question — "I will cap it", "should I?".
_HYPOTHETICAL = re.compile(
    r"\b(?:will|won't|going to|gonna|would|should|shall|could|can|cannot|can't|"
    r"may|might|must|plan to|planning to|about to|next(?:\s+I)?|intend|propose|"
    r"recommend|suggest|plan(?:ned)? for|let me|let's|i'll|we'll|i'd|we'd|"
    r"once you|if you|do you want|shall i|plan is)\b",
    re.I,
)

#: Negation — "nothing was saved", "I did not make the changes". An honest
#: admission must never be matched as the dishonest claim it is retracting.
_NEGATED = re.compile(
    r"\b(?:not|no|never|nothing|none|didn't|did not|doesn't|does not|haven't|"
    r"have not|hasn't|has not|isn't|is not|aren't|are not|wasn't|was not|"
    r"weren't|were not|yet to|without)\b",
    re.I,
)

# ── Claim patterns: a COMPLETED effect on the artefact ───────────────────────
# Each carries its own effect vocabulary, so a bare "now" or a bare "saved"
# never matches on its own.
_CLAIM_PATTERNS: tuple[re.Pattern[str], ...] = (
    # "the desk is saved", "the schemas have been updated", "it was applied"
    re.compile(
        r"\b(?:is|are|was|were|has been|have been|had been)\s+(?:now\s+)?"
        r"(?:saved|updated|changed|applied|written|wired|patched|created|"
        r"replaced|capped|committed|in place|live)\b",
        re.I,
    ),
    # "I saved the writer's instructions", "we've updated the ledger"
    re.compile(
        r"\b(?:i|we)\s+(?:have\s+|'ve\s+|just\s+|already\s+)*"
        r"(?:saved|updated|changed|applied|wrote|written|wired|patched|created|"
        r"replaced|capped|edited|made)\b",
        re.I,
    ),
    # "all changes made now and live", "all agent changes saved as of …"
    re.compile(
        r"\ball\s+(?:\w+\s+){0,3}?(?:changes|edits|updates)\b[^.\n]{0,80}?"
        r"\b(?:made|saved|applied|live|in place|committed|done)\b",
        re.I,
    ),
    # "the node now caps at 25", "the writer now cites only the document"
    re.compile(
        r"\bnow\s+(?:caps?|capped|returns?|cites?|reads?|writes?|includes?|"
        r"excludes?|enforces?|limits?|emits?|stops?|holds?|uses?)\b",
        re.I,
    ),
    # "this is now a hard instruction", "it is now live"
    re.compile(
        r"\b(?:is|are|it's|that's)\s+now\s+(?:\w+\s+){0,3}?"
        r"(?:live|in place|capped|saved|set|enforced|active|updated|changed|"
        r"fixed|done|instruction|rule|hard)\b",
        re.I,
    ),
    # "changed: n_cross", "agent replaced: 2026-09-12" — the changelog voice
    re.compile(
        r"\b(?:step|node|agent|prompt|schema|instruction|rule|workflow|desk)\s+"
        r"(?:changed|replaced|updated|saved|capped)\s*:",
        re.I,
    ),
)

#: Fenced code and blockquotes come out first: a quoted line is the PERSON's
#: words echoed back, and a code fence is an artefact, not an assertion.
_FENCED = re.compile(r"```.*?(?:```|$)", re.S)
_QUOTED_LINE = re.compile(r"^[ \t]*>.*$", re.M)
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?;:\n])\s+|\n+")
#: Markdown emphasis and list bullets carry no meaning for the match and would
#: otherwise split "**Writer now cites**" away from its verb.
_DECORATION = re.compile(r"[*_`#]+")


def claim_text(text: str) -> str:
    """The ONLY text the change-claim detector may read.

    Strips fenced blocks and quoted lines, flattens markdown decoration, bounds
    the result. Mirrors ``matrx_utils.error_text.classification_text``: this
    trims what gets MATCHED, never what gets kept or shown.
    """
    if not text:
        return ""
    stripped = _FENCED.sub(" ", text)
    stripped = _QUOTED_LINE.sub(" ", stripped)
    return _DECORATION.sub(" ", stripped)[:CLAIM_TEXT_LIMIT]


def find_change_claims(text: str, *, limit: int = 4) -> tuple[str, ...]:
    """The past-tense change assertions in THIS turn's model text.

    A sentence qualifies only when it is neither hypothetical, negated, nor a
    question, AND it matches a completed-effect pattern. Returns up to ``limit``
    of the offending sentences, trimmed — they are quoted back to the model in
    the correction notice, so they must be its own words.
    """
    claims: list[str] = []
    for raw in _SENTENCE_SPLIT.split(claim_text(text)):
        sentence = " ".join(raw.split())
        if not sentence or sentence.endswith("?"):
            continue
        if _HYPOTHETICAL.search(sentence) or _NEGATED.search(sentence):
            continue
        if any(pattern.search(sentence) for pattern in _CLAIM_PATTERNS):
            trimmed = sentence[:160]
            if trimmed not in claims:
                claims.append(trimmed)
            if len(claims) >= limit:
                break
    return tuple(claims)


@dataclass(frozen=True, slots=True)
class AuthoringPolicy:
    """What the HOST says about the mandate holding this run.

    Built from the mandate DECLARATION (``declare_mandate(..., authoring=True)``)
    plus the correction budget knob, and handed over by one injected callable —
    so matrx-ai never learns a mandate key, and adding an authoring mandate is a
    declaration change with no runtime edit.

    ``write_tools`` empty means "any successful tool call counts as a write":
    the conservative reading, since a mandate that has not enumerated its
    writers must not have turns refused on a guess.
    """

    mandate_key: str
    write_tools: frozenset[str] = frozenset()
    correction_turns: int = 1

    @classmethod
    def from_host(cls, payload: Any) -> AuthoringPolicy | None:
        """Coerce the host's answer. Anything unusable → None (no gate)."""
        if not isinstance(payload, dict):
            return None
        key = payload.get("mandate_key")
        if not isinstance(key, str) or not key.strip():
            return None
        raw_tools = payload.get("write_tools") or ()
        tools = frozenset(
            str(name).strip() for name in raw_tools if isinstance(name, str) and name.strip()
        )
        try:
            turns = int(payload.get("correction_turns", 1))
        except (TypeError, ValueError):
            turns = 1
        return cls(mandate_key=key.strip(), write_tools=tools, correction_turns=max(0, turns))


@dataclass(frozen=True, slots=True)
class ChangeClaimReport:
    """What the turn asserted, against what the turn actually wrote."""

    policy: AuthoringPolicy
    claims: tuple[str, ...] = ()
    wrote: bool = False
    successful_tools: tuple[str, ...] = field(default=())

    @property
    def unbacked(self) -> bool:
        return bool(self.claims) and not self.wrote

    def as_metadata(self) -> dict[str, Any]:
        return {
            "mandate_key": self.policy.mandate_key,
            "claims": list(self.claims),
            "successful_tools": list(self.successful_tools),
        }


ChangeClaimAction = Literal["proceed", "force", "disclose"]


def successful_write_tools(
    tool_call_history: list["ToolCallUsage"] | None,
    write_tools: frozenset[str],
) -> tuple[str, ...]:
    """Names of tools this turn called SUCCESSFULLY that count as writes.

    Read from the durable per-iteration record the executor already keeps
    (``{name, success}`` per call) — the same ledger the required-member gate
    trusts, and the reason this gate cannot be talked out of its verdict.
    """
    names: list[str] = []
    for usage in tool_call_history or []:
        for detail in usage.tool_calls_details or []:
            if detail.get("success") is not True:
                continue
            name = str(detail.get("name") or "")
            if not name:
                continue
            if write_tools and name not in write_tools:
                continue
            if name not in names:
                names.append(name)
    return tuple(names)


def evaluate_change_claims(
    policy: AuthoringPolicy | None,
    tool_call_history: list["ToolCallUsage"] | None,
    assistant_text: str,
) -> ChangeClaimReport | None:
    """The predicate, from durable facts only. None when there is no gate here."""
    if policy is None:
        return None
    claims = find_change_claims(assistant_text)
    if not claims:
        return None
    wrote_names = successful_write_tools(tool_call_history, policy.write_tools)
    return ChangeClaimReport(
        policy=policy,
        claims=claims,
        wrote=bool(wrote_names),
        successful_tools=wrote_names,
    )


def decide_change_claim_action(
    report: ChangeClaimReport | None,
    *,
    corrections_used: int,
    loop_guard_intervened: bool = False,
) -> ChangeClaimAction:
    """One decision table for the finishing boundary.

    - nothing unbacked → proceed.
    - the loop guard already intervened → DISCLOSE, never force: its tools are
      gone and the run already finalizes as paused, so a forced turn would fight
      the other guard while the person still needs to be told nothing was saved.
    - budget left → force one more turn, tools in hand.
    - budget spent → disclose (and the run records it). Never silence.
    """
    if report is None or not report.unbacked:
        return "proceed"
    if loop_guard_intervened:
        return "disclose"
    if corrections_used < report.policy.correction_turns:
        return "force"
    return "disclose"


def correction_notice(report: ChangeClaimReport) -> str:
    quoted = "; ".join(f'"{claim}"' for claim in report.claims)
    return CHANGE_CLAIM_CORRECTION_NOTICE.format(claims=quoted)


__all__ = [
    "CHANGE_CLAIM_CORRECTION_CODE",
    "CHANGE_CLAIM_CORRECTION_NOTICE",
    "CHANGE_CLAIM_UNBACKED_CODE",
    "CHANGE_CLAIM_USER_DISCLOSURE",
    "CLAIM_TEXT_LIMIT",
    "UNBACKED_CHANGE_CLAIM_META_KEY",
    "AuthoringPolicy",
    "ChangeClaimAction",
    "ChangeClaimReport",
    "claim_text",
    "correction_notice",
    "decide_change_claim_action",
    "evaluate_change_claims",
    "find_change_claims",
    "successful_write_tools",
]
