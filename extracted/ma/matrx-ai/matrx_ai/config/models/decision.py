"""Pydantic twins for the decision modality's two content blocks.

Shadowed, not swapped — the dataclasses in
``matrx_ai.config.decision_input_config`` still own behaviour, exactly like
every other twin here.

These two are the easiest twins in the set, and for a reason worth recording:
their payload is ALREADY pydantic. ``decision_questions`` and
``decision_answers`` are registered kinds (``matrx_ai.decisions.kinds``), so
there is no corpus of stored blocks whose declared types turned out to be
hypotheses — the shape was a validated contract from its first write. The twin
therefore holds the block envelope and delegates the payload to the kind
models, which is what keeps the block, the kind, the registry row and the
generated TypeScript from ever describing three different things.
"""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_ai.decisions.kinds import DecisionAnswers, DecisionQuestion

_BLOCK = ConfigDict(extra="forbid", populate_by_name=True)


class DecisionQuestionsContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["decision_questions"] = "decision_questions"
    questions: list[DecisionQuestion] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DecisionAnswersContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["decision_answers"] = "decision_answers"
    answers: DecisionAnswers | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
