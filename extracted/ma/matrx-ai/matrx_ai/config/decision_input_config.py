"""The decision modality's content parts — ``decision_questions`` (the ask)
and ``decision_answers`` (what comes back).

WHY A PART AND NOT A CONTROL (`common-docs/systems/agents/typed-messages/FEATURE.md`,
the primitives table): it is what is being ASKED, inside the conversation
content. The raw provider call puts it in the body next to the state, so it is
a part, and it rides in ``UnifiedMessage.content`` beside text, tables and
media exactly like every other one.

**The state is the other parts of the same message.** There is deliberately no
``state`` field here: a second copy of the text the user already attached is a
second thing to keep in sync, and it would be wrong the first time somebody
edits the message. The translator reads the sibling parts.

**Parts are semantic; translators decide the wire.** The SAME part reaches a
native decision holder as a typed System One request and a text model as prose
plus a structured-output contract. ``to_prose()`` is that second rendering and
lives here, beside the shape, so both translators read one description of what
a question means.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from matrx_ai.decisions.kinds import DecisionAnswers, DecisionQuestion, DecisionQuestions

__all__ = ["DecisionAnswersContent", "DecisionQuestionsContent"]


@dataclass
class DecisionQuestionsContent:
    type: Literal["decision_questions"] = "decision_questions"
    questions: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def typed(self) -> DecisionQuestions:
        """The validated kind instance — the contract, enforced."""
        return DecisionQuestions(questions=self.questions)

    def to_storage_dict(self) -> dict[str, Any]:
        typed = self.typed()
        result: dict[str, Any] = typed.model_dump(mode="json")
        result["type"] = "decision_questions"
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result

    def replace_variables(self, variables: dict[str, Any]) -> bool:
        """Substitute ``{{variable_name}}`` in every author-written string.

        Every string an author writes into a question is a slot (typed-messages
        FEATURE.md: "Any string field is a slot"): the ``instructions``, every
        ``criteria`` meaning (a noul/choice mapping's values, a score's level
        labels). Identifiers are NOT slots — ``name`` is the output field, a
        choice's option keys are the answer vocabulary, ``type`` is the
        contract — so a variable can never rename what comes back.

        Values pass through ``prompt_safe_value``, the same door text parts
        use, so a question reads exactly what the text beside it reads.
        Never drops the part: returns False always.
        """
        if not variables:
            return False
        from matrx_ai.config.prompt_values import prompt_safe_value

        rendered = {name: prompt_safe_value(value) for name, value in variables.items()}

        def fill(text: str) -> str:
            for name, value in rendered.items():
                text = text.replace(f"{{{{{name}}}}}", value)
            return text

        filled: list[dict[str, Any]] = []
        for question in self.questions:
            q = dict(question)
            if isinstance(q.get("instructions"), str):
                q["instructions"] = fill(q["instructions"])
            criteria = q.get("criteria")
            if isinstance(criteria, dict):
                q["criteria"] = {k: fill(v) if isinstance(v, str) else v for k, v in criteria.items()}
            elif isinstance(criteria, list):
                q["criteria"] = [fill(v) if isinstance(v, str) else v for v in criteria]
            elif isinstance(criteria, str):
                q["criteria"] = fill(criteria)
            filled.append(q)
        self.questions = filled
        return False

    def get_output(self) -> str:
        """Nothing. A question is what was ASKED, never what came back.

        ``UnifiedMessage.get_output()`` concatenates the answer of a turn, and
        it walks EVERY content class — so this method must exist even though a
        questions part only ever rides a user turn. Returning the prose here
        would put the author's own questions into the run's answer, into
        ``raw_response``, and into the completion event.
        """
        return ""

    def to_prose(self) -> str:
        """How a TEXT model is shown the same questions.

        Each question names its output field, states the instruction, and spells
        out its criteria, so a text model answers the identical question a
        native decision holder would — that equivalence is the whole point of
        one semantic part with two translators.
        """
        lines: list[str] = ["## Questions", ""]
        for question in self.typed().questions:
            lines.append(f"### {question.name} ({question.type})")
            lines.append(question.instructions)
            lines.extend(_criteria_lines(question))
            lines.append("")
        return "\n".join(lines).rstrip()


def _criteria_lines(question: DecisionQuestion) -> list[str]:
    if question.type == "choice":
        options = question.criteria if isinstance(question.criteria, dict) else {}
        return ["Options:", *[f"- {name}: {meaning}" for name, meaning in options.items()]]
    if question.type == "score":
        levels = question.score_levels()
        return [
            "Levels (1 is lowest):",
            *[f"- {index}: {level}" for index, level in enumerate(levels, start=1)],
        ]
    if isinstance(question.criteria, dict) and question.criteria:
        return [
            "Answer true or false:",
            *[f"- {value}: {meaning}" for value, meaning in question.criteria.items()],
        ]
    return ["Answer true or false."]


@dataclass
class DecisionAnswersContent:
    """The assistant turn a decision request produces — ONE part, never prose.

    The whole answer (verdicts, distributions, confidence, the method that
    produced them, usage and cost) is one typed kind instance, so the runner
    renders it with a primitive and battle can put two of them side by side.
    A decision turn that came back as text would be a decision system that
    cannot be compared, scored, or trusted about its own certainty.
    """

    type: Literal["decision_answers"] = "decision_answers"
    answers: DecisionAnswers | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_storage_dict(self) -> dict[str, Any]:
        if self.answers is None:
            raise ValueError("DecisionAnswersContent carries no answers.")
        result: dict[str, Any] = self.answers.model_dump(mode="json")
        result["type"] = "decision_answers"
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result

    def to_text(self) -> str:
        """A plain reading of the same answers, for a text-only consumer."""
        if self.answers is None:
            return ""
        import json

        return json.dumps(self.answers.model_dump(mode="json"), ensure_ascii=False, indent=2)

    def get_output(self) -> str:
        """THE OUTPUT of a decision turn — the answers, as JSON.

        Every content class on the platform answers ``get_output()`` and
        ``UnifiedMessage.get_output()`` calls it on every non-thinking block.
        Without it a decision turn raised ``AttributeError`` the moment anything
        asked what the run produced: ``_emit_completion`` (aidream
        ``services/ai_execution/ai_task.py``) right before ``send_end()``,
        ``Agent._clean_up_response``, the parallel executor, and conversation
        rehydration — so a PAID, PERSISTED, correct answer was reported to the
        client as a failed run. Returning ``to_text()`` keeps the one rule the
        string carries: it is what a consumer parses (``extract_json`` finds
        the answers object), persists as ``raw_response``, and emits.
        """
        return self.to_text()
