"""THE ANSWER CHECK — an answer that breaks a rule its own kind sets is sent back once, with the text named.

Sibling of the change-claim gate (``change_claims.py``), at the same finishing boundary and with the same
discipline: the runtime, not the prompt, refuses. Born 2026-10-24 (lane L6e): the Messaging House Builder twice
wrote claims into pillars, pitches and boilerplate that the SAME answer flagged no-proof or contradicted, and two
prompt-only improve builds did not stop it.

* **Declared by the host, per answer kind.** matrx-ai knows no kind's rules. When a finishing turn's text is a JSON
  object carrying ``__kind``, the host seam (``_ext.get_answer_check``) is asked for that answer's problems; the host
  answers ``{"kind", "problems": [sentence, ...], "correction_turns": n}`` or None. Unconfigured = no gate.
* **One sentence per problem, naming the offending text**, so the corrective turn can fix exactly that.
* **Bounded.** ``correction_turns`` (host knob ``mandate_honesty.answer_check_correction_turns``) forced turns; once
  spent the answer goes through and the problems are recorded on the run and announced. The host's save step is the
  deterministic backstop (it drops what still offends).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Literal

#: Warning code when a turn is sent back by the answer check.
ANSWER_CHECK_CORRECTION_CODE = "answer_check_correction"
#: Warning code when the budget is spent and the answer still breaks its rules.
ANSWER_CHECK_UNMET_CODE = "answer_check_unmet"
#: Problems quoted into one notice (each is one sentence naming the text).
MAX_PROBLEMS_IN_NOTICE = 20
#: The longest answer text parsed (a structured answer, not a document).
ANSWER_TEXT_LIMIT = 400_000


@dataclass
class AnswerCheckReport:
    kind: str
    problems: list[str] = field(default_factory=list)
    correction_turns: int = 1

    @classmethod
    def from_host(cls, payload: Any) -> AnswerCheckReport | None:
        if not isinstance(payload, dict):
            return None
        problems = [str(p) for p in payload.get("problems") or [] if str(p).strip()]
        if not problems:
            return None
        try:
            turns = max(0, int(payload.get("correction_turns", 1)))
        except (TypeError, ValueError):
            turns = 1
        return cls(kind=str(payload.get("kind") or ""), problems=problems, correction_turns=turns)

    def as_metadata(self) -> dict[str, Any]:
        return {"kind": self.kind, "problems": self.problems[:MAX_PROBLEMS_IN_NOTICE],
                "problem_count": len(self.problems)}


def structured_answer(text: str) -> dict[str, Any] | None:
    """The turn's answer as a kind instance (a JSON object with ``__kind``), or None. Never raises."""
    t = (text or "").strip()
    if not t.startswith("{") or len(t) > ANSWER_TEXT_LIMIT:
        return None
    try:
        obj = json.loads(t)
    except ValueError:
        return None
    return obj if isinstance(obj, dict) and isinstance(obj.get("__kind"), str) and obj["__kind"] else None


def decide_answer_check_action(
    report: AnswerCheckReport | None, *, corrections_used: int
) -> Literal["proceed", "force", "disclose"]:
    if report is None or not report.problems:
        return "proceed"
    return "force" if corrections_used < report.correction_turns else "disclose"


def correction_notice(report: AnswerCheckReport) -> str:
    shown = report.problems[:MAX_PROBLEMS_IN_NOTICE]
    more = len(report.problems) - len(shown)
    lines = "\n".join(f"- {p}" for p in shown) + (f"\n- …and {more} more of the same kind." if more > 0 else "")
    return (
        "SYSTEM NOTICE (not from the user): your answer was refused because it breaks a rule of its own answer "
        f"format ({report.kind}). Fix every item below, change nothing else, and return the WHOLE corrected answer "
        f"again in the same format:\n{lines}"
    )
