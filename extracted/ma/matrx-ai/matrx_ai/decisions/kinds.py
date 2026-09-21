"""The decision typed-message contracts as real ``KindModel`` classes.

THE CONTRACTS ARE NOT OURS TO INVENT. They are ruled and written down once, in
``common-docs/systems/agents/typed-messages/FEATURE.md`` ("Contracts (build
against these)"), on Arman's 2026-09-21 ruling. These models are that document
expressed in pydantic so the platform can validate, publish, render and
generate types from ONE source instead of three hand-copies.

Three kinds live here:

``decision_questions``  the QUESTION side — what an author asks. It rides
                        inside a message as a content part (the part model is
                        ``matrx_ai.db.message_parts.DecisionQuestionsPart``,
                        which reuses these same question models), so the state
                        it reasons over is simply the OTHER parts of the same
                        message.
``decision_answer``     ONE answer. It is its own kind and not merely nested
                        structure because a surface renders a single answer bar
                        (question · answer · distribution · confidence) without
                        knowing which batch it came from.
``decision_answers``    the batch an assistant turn returns: the answers map,
                        the refusals, the method, the usage and the cost.

``method`` is load-bearing and never inferred at read time: ``native`` is a
probability the holder itself computed (TypeSafe System One), ``verbalized`` is
a text model stating its own probability, and ``verbalized_calibrated`` is a
verbalized probability corrected by a per-agent-version calibration learned
from ground-truth verdicts. Confusing the three is how a decision system starts
lying about how sure it is.

Registration (label, family, canonical example) happens host-side in
``aidream/kinds/decisions.py`` — the package declares the SHAPE, the host
publishes it, exactly as ``criteria_gate`` does.
"""

from __future__ import annotations

import re
from typing import Any, Literal

from matrx_graph.content_ir.model import KindModel, KindSubModel
from pydantic import Field, model_validator

__all__ = [
    "DECISION_METHODS",
    "MAX_CHOICE_OPTIONS",
    "MAX_SCORE_LEVELS",
    "DecisionAnswer",
    "DecisionAnswers",
    "DecisionQuestion",
    "DecisionQuestions",
    "DecisionUsage",
    "QUESTION_NAME_PATTERN",
]

# Vendor limits, mirrored from the TypeSafe adapter
# (``matrx_ai.providers.typesafe.client``) so a question is refused with a
# remedy at AUTHORING time rather than as a 422 on a paid round trip. They are
# also the contract for the verbalized path, which must be able to ask a text
# model the exact same question.
MAX_CHOICE_OPTIONS = 255
MAX_SCORE_LEVELS = 10
MIN_CHOICE_OPTIONS = 2
MIN_SCORE_LEVELS = 2

DECISION_METHODS = ("native", "verbalized", "verbalized_calibrated")

#: ``name`` is the OUTPUT FIELD NAME of the answer, so it must be a legal
#: identifier in every consumer (JSON key, python attribute, SQL column, a
#: response_format property). snake_case is the platform spelling.
QUESTION_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


class DecisionQuestion(KindSubModel):
    """One question. Not a kind: it has no meaning outside its batch."""

    name: str = Field(min_length=1, max_length=128)
    type: Literal["noul", "choice", "score"]
    instructions: str = Field(min_length=1)
    #: ``choice`` → an option map (2–255 named options, values describe them).
    #: ``score``  → an ORDERED list of 2–10 level descriptions.
    #: ``noul``   → optional clarifying text under the keys ``true``/``false``.
    criteria: dict[str, str] | list[str] | None = None
    #: The author's hint to the consumer, never a gate this code applies.
    suggested_threshold: float | None = Field(default=None, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def _shape_matches_type(self) -> DecisionQuestion:
        if not QUESTION_NAME_PATTERN.match(self.name):
            raise ValueError(
                f"Decision question name {self.name!r} is not snake_case. The name "
                "becomes the answer's field name, so it must start with a lowercase "
                "letter and contain only lowercase letters, digits and underscores."
            )
        if self.type == "choice":
            if not isinstance(self.criteria, dict):
                raise ValueError(
                    f"Choice question {self.name!r} needs a criteria MAP of named "
                    "options (option name → what it means)."
                )
            if not MIN_CHOICE_OPTIONS <= len(self.criteria) <= MAX_CHOICE_OPTIONS:
                raise ValueError(
                    f"Choice question {self.name!r} has {len(self.criteria)} options; "
                    f"a choice takes {MIN_CHOICE_OPTIONS}–{MAX_CHOICE_OPTIONS}."
                )
            if any(not str(option).strip() for option in self.criteria):
                raise ValueError(f"Choice question {self.name!r} has a blank option name.")
        elif self.type == "score":
            if not isinstance(self.criteria, list):
                raise ValueError(
                    f"Score question {self.name!r} needs criteria as an ORDERED LIST "
                    "of level descriptions, lowest first."
                )
            if not MIN_SCORE_LEVELS <= len(self.criteria) <= MAX_SCORE_LEVELS:
                raise ValueError(
                    f"Score question {self.name!r} has {len(self.criteria)} levels; "
                    f"a score takes {MIN_SCORE_LEVELS}–{MAX_SCORE_LEVELS}."
                )
        elif isinstance(self.criteria, list):
            raise ValueError(
                f"Noul question {self.name!r} takes criteria as an optional map with "
                "the keys 'true' and 'false', not a list."
            )
        elif isinstance(self.criteria, dict):
            unknown = set(self.criteria) - {"true", "false"}
            if unknown:
                raise ValueError(
                    f"Noul question {self.name!r} may only describe 'true' and 'false'; "
                    f"got {sorted(unknown)}."
                )
        return self

    def score_levels(self) -> list[str]:
        """The ordered level descriptions of a score question (``[]`` otherwise)."""
        if self.type == "score" and isinstance(self.criteria, list):
            return [str(level) for level in self.criteria]
        return []

    def choice_options(self) -> list[str]:
        """The option names of a choice question (``[]`` otherwise)."""
        if self.type == "choice" and isinstance(self.criteria, dict):
            return list(self.criteria)
        return []


class DecisionQuestions(KindModel, kind="decision_questions"):
    """A batch of questions asked of whatever state shares their message."""

    questions: list[DecisionQuestion] = Field(min_length=1)

    @model_validator(mode="after")
    def _names_are_unique(self) -> DecisionQuestions:
        seen: set[str] = set()
        for question in self.questions:
            if question.name in seen:
                raise ValueError(
                    f"Decision question name {question.name!r} appears twice. Each "
                    "name is one output field, so names must be unique in a batch."
                )
            seen.add(question.name)
        return self

    def by_name(self) -> dict[str, DecisionQuestion]:
        return {question.name: question for question in self.questions}


class DecisionAnswer(KindModel, kind="decision_answer"):
    """One answer, with the holder's own uncertainty attached."""

    type: Literal["noul", "choice", "score"]
    #: noul → bool · choice → the chosen option name · score → the
    #: probability-weighted level (a float, deliberately not an integer: "3.4"
    #: carries information "3" throws away).
    answer: bool | float | str
    #: noul only — P(true).
    probability: float | None = Field(default=None, ge=0.0, le=1.0)
    #: choice/score — the full distribution. Never a single winner.
    probabilities: dict[str, float] | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    #: score only — level key → what that level means, echoed so a renderer
    #: never has to hold the question to draw the answer.
    legend: dict[str, str] | None = None

    @model_validator(mode="after")
    def _shape_matches_type(self) -> DecisionAnswer:
        if self.type == "noul":
            if not isinstance(self.answer, bool):
                raise ValueError("A noul answer is true or false.")
            if self.probability is None:
                raise ValueError("A noul answer carries its probability of true.")
            if self.probabilities is not None:
                raise ValueError("A noul answer has one probability, not a distribution.")
        elif self.type == "choice":
            if not isinstance(self.answer, str) or not self.answer.strip():
                raise ValueError("A choice answer is the chosen option name.")
            if not self.probabilities:
                raise ValueError("A choice answer carries a probability per option.")
            if self.answer not in self.probabilities:
                raise ValueError(
                    f"Choice answer {self.answer!r} is not one of the options it scored "
                    f"({sorted(self.probabilities)})."
                )
        else:
            if isinstance(self.answer, bool) or not isinstance(self.answer, int | float):
                raise ValueError("A score answer is a number on the question's scale.")
            if not self.probabilities:
                raise ValueError("A score answer carries a probability per level.")
        return self


class DecisionUsage(KindSubModel):
    """What the decision call consumed. Zero is a real value, never a stand-in."""

    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)


class DecisionAnswers(KindModel, kind="decision_answers"):
    """The assistant turn a decision request produces."""

    model: str = Field(min_length=1)
    method: Literal["native", "verbalized", "verbalized_calibrated"]
    answers: dict[str, DecisionAnswer] = Field(default_factory=dict)
    #: question name → why the holder would not answer it. A refusal is an
    #: answer; it is never replaced by a guess and never silently dropped.
    unanswerable: dict[str, str] = Field(default_factory=dict)
    usage: DecisionUsage
    cost_usd: float = Field(ge=0.0)

    @model_validator(mode="after")
    def _answered_or_refused(self) -> DecisionAnswers:
        both = set(self.answers) & set(self.unanswerable)
        if both:
            raise ValueError(
                f"Questions {sorted(both)} are both answered and listed unanswerable."
            )
        if not self.answers and not self.unanswerable:
            raise ValueError(
                "A decision_answers part with no answers and no refusals says nothing; "
                "every question is answered or named unanswerable."
            )
        return self

    def to_part(self) -> dict[str, Any]:
        """The wire part an assistant message carries."""
        return self.model_dump(mode="json")
