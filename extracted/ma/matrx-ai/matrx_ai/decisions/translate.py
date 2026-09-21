"""The decision TRANSLATOR — one semantic part, two wires.

A decision model is a model in the agent system, exactly like an image, video
or TTS model: it rides ``UnifiedAIClient`` through a per-model wire translator
and thereby inherits the builder, the runner, battle, mandates and cost
tracking for free (Arman, 2026-09-20 — the refusal that used to stand in
``unified_client`` was the defect, this is the fix).

This module is the part of that translation with no provider or transport in
it, so both destinations read ONE description of what a question means:

* **native** — a ``typesafe_systemone`` route: the state becomes System One's
  ``state`` object and the questions become its typed question map. The holder
  computes the probabilities itself.
* **verbalized** — any text model: the same questions rendered as prose plus a
  structured-output contract that returns the identical ``decision_answers``
  shape. **Probabilities are ASKED FOR, never derived** (Arman, 2026-09-21:
  logprobs are useless on reasoning models, and no self-consistency sampling).
  ``method`` records which of the two produced a number, so a native
  probability is never silently read as a verbalized one.

THE STATE IS THE MESSAGE. A decision part carries no state of its own: the
state is the other text-bearing parts of the same message, plus the system
instruction and earlier user text when present, assembled as a JSON object with
descriptive keys. One source, nothing to drift.

COMPATIBILITY IS NEVER SILENT. A decision holder is text-only, so an image,
audio or video part standing beside the questions is REFUSED with a sentence
naming the part and the reason — never dropped while the model answers as if it
had seen it (the typed-messages compatibility law).
"""

from __future__ import annotations

import json
from typing import Any

from matrx_ai.decisions.kinds import (
    DecisionAnswer,
    DecisionAnswers,
    DecisionQuestion,
    DecisionQuestions,
    DecisionUsage,
)

__all__ = [
    "DecisionCompatibilityError",
    "DecisionQuestionsMissing",
    "build_decision_state",
    "decision_answers_from_system_one",
    "decision_answers_from_verbalized",
    "find_decision_questions",
    "refuse_incompatible_parts",
    "system_one_questions",
    "verbalized_instructions",
    "verbalized_response_schema",
    "VerbalizedDecisionOverlay",
    "prepare_verbalized_decision",
    "finalize_verbalized_decision",
]

#: Media part kinds a text-only decision holder cannot consume. The value is
#: the word used in the refusal sentence.
_UNREADABLE_PART_LABELS = {
    "image": "an image",
    "audio": "an audio clip",
    "video": "a video",
    "youtube_video": "a YouTube video",
    "document": "a document",
}


class DecisionCompatibilityError(ValueError):
    """A part beside the questions that this model cannot consume."""


class DecisionQuestionsMissing(ValueError):
    """A decision route was selected but nothing in the request asks anything."""


def _content_type(block: Any) -> str:
    value = getattr(block, "type", None)
    if isinstance(value, str) and value:
        return value
    if isinstance(block, dict):
        raw = block.get("type")
        if isinstance(raw, str):
            return raw
    return ""


def find_decision_questions(messages: list[Any]) -> tuple[int, DecisionQuestions]:
    """The LAST message carrying a questions part, and its validated batch.

    The last one wins for the same reason the last user message is the turn: an
    earlier decision in the same conversation is history, not the ask.
    """
    for index in range(len(messages) - 1, -1, -1):
        for block in getattr(messages[index], "content", None) or []:
            if _content_type(block) != "decision_questions":
                continue
            raw = getattr(block, "questions", None)
            if raw is None and isinstance(block, dict):
                raw = block.get("questions")
            return index, DecisionQuestions(questions=list(raw or []))
    raise DecisionQuestionsMissing(
        "This request is routed to a decision model, but no message carries a "
        "'decision_questions' part. A decision model answers declared questions "
        "about the state in its message; it has no free-text turn to fall back "
        "on. Attach a decision_questions part, or choose a chat model."
    )


def refuse_incompatible_parts(message: Any, *, model_name: str) -> None:
    """Refuse — loudly, by name — any part a text-only holder cannot read."""
    for block in getattr(message, "content", None) or []:
        block_type = _content_type(block)
        label = _UNREADABLE_PART_LABELS.get(block_type)
        if label is None and block_type == "media":
            label = _UNREADABLE_PART_LABELS.get(str(getattr(block, "kind", "") or ""))
        if label is None:
            continue
        raise DecisionCompatibilityError(
            f"The message sent to the decision model {model_name!r} contains "
            f"{label} beside its questions, and a decision model reads TEXT ONLY: "
            "its state is a text or JSON object, so this part cannot be put on the "
            "wire and will not be silently dropped. Either describe what it "
            "contains in text in the same message, or ask these questions of a "
            "model that can read it."
        )


def _text_of(block: Any) -> str:
    """The text a block contributes to the state, or ``''``."""
    text = getattr(block, "text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()
    metadata = getattr(block, "metadata", None)
    if isinstance(metadata, dict):
        resolved = metadata.get("resolved_text")
        if isinstance(resolved, str) and resolved.strip():
            return resolved.strip()
    return ""


def _message_text(message: Any, *, skip_questions: bool = True) -> str:
    parts: list[str] = []
    for block in getattr(message, "content", None) or []:
        if skip_questions and _content_type(block) == "decision_questions":
            continue
        text = _text_of(block)
        if text:
            parts.append(text)
    return "\n\n".join(parts)


def _instruction_text(system_instruction: Any) -> str:
    """The author's instruction, without the chat decorations.

    ``config.system_instruction`` is normally a ``SystemInstruction`` whose
    ``__str__`` renders the date, the tools list and the guidelines blocks — all
    of which are chat furniture a decision holder must not be told to reason
    about. The state carries the AUTHORED instruction only.
    """
    if system_instruction is None:
        return ""
    base = getattr(system_instruction, "base_instruction", None)
    if isinstance(base, str):
        return base.strip()
    return str(system_instruction).strip()


def build_decision_state(
    messages: list[Any],
    question_index: int,
    *,
    system_instruction: Any = None,
) -> dict[str, Any]:
    """The JSON state object a decision holder reasons over.

    Keys are descriptive because the holder READS them: ``subject`` is what the
    questions are about (the other parts of their own message), ``instructions``
    is the agent's system instruction, and ``earlier_conversation`` is the user
    text that came before, in order. Empty sections are omitted rather than sent
    blank — an empty key is a claim that there was nothing to say.
    """
    state: dict[str, Any] = {}
    instruction = _instruction_text(system_instruction)
    if instruction:
        state["instructions"] = instruction

    earlier: list[str] = []
    for message in messages[:question_index]:
        role = str(getattr(message, "role", "") or "")
        text = _message_text(message, skip_questions=True)
        if not text:
            continue
        if role == "system" and "instructions" not in state:
            state["instructions"] = text
            continue
        earlier.append(f"{role or 'user'}: {text}" if role else text)
    if earlier:
        state["earlier_conversation"] = "\n\n".join(earlier)

    subject = _message_text(messages[question_index], skip_questions=True)
    if subject:
        state["subject"] = subject
    if not state:
        raise DecisionCompatibilityError(
            "The decision questions arrived with no state at all — no text beside "
            "them, no earlier message, no instruction. A decision is made ABOUT "
            "something; send the material to judge in the same message as the "
            "questions."
        )
    return state


def system_one_questions(batch: DecisionQuestions) -> dict[str, Any]:
    """The questions as TypeSafe System One's typed question map."""
    out: dict[str, Any] = {}
    for question in batch.questions:
        if question.type == "choice":
            out[question.name] = {
                "type": "choice",
                "instructions": question.instructions,
                "criteria": dict(question.criteria or {}),
            }
        elif question.type == "score":
            out[question.name] = {
                "type": "score",
                "instructions": question.instructions,
                "criteria": question.score_levels(),
            }
        else:
            payload: dict[str, Any] = {
                "type": "noul",
                "instructions": question.instructions,
            }
            if isinstance(question.criteria, dict) and question.criteria:
                payload["criteria"] = dict(question.criteria)
            out[question.name] = payload
    return out


def _score_legend(question: DecisionQuestion) -> dict[str, str]:
    """Level key → what that level means.

    ZERO-INDEXED, because the native holder is. Measured against live TypeSafe
    System One on 2026-09-20: a five-level score comes back with the keys
    ``0..4`` and a ``score`` on that same scale, so a verbalized answer keyed
    ``1..5`` would read one whole level more urgent than a native answer to the
    identical question — and battle puts the two side by side. The contract doc
    (`common-docs/systems/agents/typed-messages/FEATURE.md`) illustrates the
    shape with ``1..5``; the holder's own convention wins, and the legend
    travels ON the answer so no consumer has to know which it was.
    """
    return {str(index): level for index, level in enumerate(question.score_levels())}


def decision_answers_from_system_one(
    raw_answers: dict[str, Any],
    batch: DecisionQuestions,
    *,
    model: str,
    input_tokens: int,
    output_tokens: int,
    cost_usd: float,
) -> DecisionAnswers:
    """The NATIVE path's provider answers as the platform's answer kind.

    A question the holder did not answer becomes an entry in ``unanswerable``
    with the reason — a refusal is an answer, and it is never replaced by a
    guess or quietly missing.
    """
    by_name = batch.by_name()
    answers: dict[str, DecisionAnswer] = {}
    unanswerable: dict[str, str] = {}

    for name, question in by_name.items():
        raw = raw_answers.get(name)
        if raw is None:
            unanswerable[name] = "the decision model returned no answer for this question"
            continue
        payload = raw if isinstance(raw, dict) else raw.model_dump(mode="json")
        if question.type == "noul":
            probability = float(payload.get("noul", 0.0))
            threshold = (
                question.suggested_threshold if question.suggested_threshold is not None else 0.5
            )
            verdict = probability >= threshold
            answers[name] = DecisionAnswer(
                type="noul",
                answer=verdict,
                probability=probability,
                confidence=probability if verdict else 1.0 - probability,
            )
        elif question.type == "choice":
            probabilities = {
                str(key): float(value)
                for key, value in (payload.get("probabilities") or {}).items()
            }
            answers[name] = DecisionAnswer(
                type="choice",
                answer=str(payload.get("choice", "")),
                probabilities=probabilities,
                confidence=float(payload.get("confidence", 0.0)),
            )
        else:
            probabilities = {
                str(key): float(value)
                for key, value in (payload.get("probabilities") or {}).items()
            }
            legend_raw = payload.get("legend") or {}
            legend = (
                {str(key): str(value) for key, value in legend_raw.items()}
                if legend_raw
                else _score_legend(question)
            )
            answers[name] = DecisionAnswer(
                type="score",
                answer=float(payload.get("score", 0.0)),
                probabilities=probabilities,
                confidence=float(payload.get("confidence", 0.0)),
                legend=legend,
            )

    return DecisionAnswers(
        model=model,
        method="native",
        answers=answers,
        unanswerable=unanswerable,
        usage=DecisionUsage(input_tokens=input_tokens, output_tokens=output_tokens),
        cost_usd=cost_usd,
    )


# ---------------------------------------------------------------------------
# The verbalized path — the same questions asked of a text model
# ---------------------------------------------------------------------------


def verbalized_instructions(state: dict[str, Any], batch: DecisionQuestions) -> str:
    """The prose a text model is given: the state, then each question."""
    lines = [
        "You are answering a fixed set of decision questions about the state below.",
        "",
        "## State",
        "```json",
        json.dumps(state, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Questions",
        "",
    ]
    for question in batch.questions:
        lines.append(f"### {question.name} ({question.type})")
        lines.append(question.instructions)
        if question.type == "choice":
            lines.append("Choose exactly one option:")
            lines.extend(
                f"- {name}: {meaning}" for name, meaning in (question.criteria or {}).items()
            )
            lines.append(
                "Give a probability for EVERY option; the probabilities must sum to 1."
            )
        elif question.type == "score":
            lines.append("Levels, lowest first:")
            lines.extend(
                f"- {index}: {level}" for index, level in enumerate(question.score_levels())
            )
            lines.append(
                "Give a probability for EVERY level key; the probabilities must sum to 1. "
                "The answer is the probability-weighted level, so it may be fractional."
            )
        else:
            if isinstance(question.criteria, dict) and question.criteria:
                lines.extend(
                    f"- {value}: {meaning}" for value, meaning in question.criteria.items()
                )
            lines.append("Give the probability that the answer is true.")
        lines.append("")
    lines.extend(
        [
            "State your own probabilities directly — do not hedge, and do not refuse a "
            "question you can answer.",
            "If a question genuinely cannot be answered from this state, name it under "
            "'unanswerable' with the reason instead of guessing.",
        ]
    )
    return "\n".join(lines)


def verbalized_response_schema(batch: DecisionQuestions) -> dict[str, Any]:
    """The JSON Schema that forces the answers shape out of a text model."""
    properties: dict[str, Any] = {}
    for question in batch.questions:
        if question.type == "noul":
            properties[question.name] = {
                "type": "object",
                "properties": {
                    "answer": {"type": "boolean"},
                    "probability": {"type": "number", "minimum": 0, "maximum": 1},
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                },
                "required": ["answer", "probability", "confidence"],
                "additionalProperties": False,
            }
        elif question.type == "choice":
            options = question.choice_options()
            properties[question.name] = {
                "type": "object",
                "properties": {
                    "answer": {"type": "string", "enum": options},
                    "probabilities": {
                        "type": "object",
                        "properties": {
                            option: {"type": "number", "minimum": 0, "maximum": 1}
                            for option in options
                        },
                        "required": options,
                        "additionalProperties": False,
                    },
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                },
                "required": ["answer", "probabilities", "confidence"],
                "additionalProperties": False,
            }
        else:
            levels = [str(i) for i in range(len(question.score_levels()))]
            properties[question.name] = {
                "type": "object",
                "properties": {
                    "probabilities": {
                        "type": "object",
                        "properties": {
                            level: {"type": "number", "minimum": 0, "maximum": 1}
                            for level in levels
                        },
                        "required": levels,
                        "additionalProperties": False,
                    },
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                },
                "required": ["probabilities", "confidence"],
                "additionalProperties": False,
            }
    names = [question.name for question in batch.questions]
    return {
        "type": "object",
        "properties": {
            "answers": {
                "type": "object",
                "properties": properties,
                "required": names,
                "additionalProperties": False,
            },
            "unanswerable": {
                "type": "object",
                "description": "question name → why it could not be answered",
                "additionalProperties": {"type": "string"},
            },
        },
        "required": ["answers"],
        "additionalProperties": False,
    }


def decision_answers_from_verbalized(
    payload: dict[str, Any],
    batch: DecisionQuestions,
    *,
    model: str,
    input_tokens: int,
    output_tokens: int,
    cost_usd: float,
) -> DecisionAnswers:
    """A text model's own stated probabilities as the platform's answer kind.

    ``method`` is ``verbalized`` and stays that way: calibration is a separate,
    per-agent-version correction applied by whoever holds the ground-truth
    verdicts, and it renames the method when it runs.
    """
    raw_answers = payload.get("answers") or {}
    raw_unanswerable = payload.get("unanswerable") or {}
    answers: dict[str, DecisionAnswer] = {}
    unanswerable = {
        str(key): str(value)
        for key, value in raw_unanswerable.items()
        if str(key) in batch.by_name()
    }

    for question in batch.questions:
        if question.name in unanswerable:
            continue
        raw = raw_answers.get(question.name)
        if not isinstance(raw, dict):
            unanswerable[question.name] = (
                "the model returned no answer for this question in its structured output"
            )
            continue
        if question.type == "noul":
            probability = float(raw.get("probability", 0.0))
            threshold = (
                question.suggested_threshold if question.suggested_threshold is not None else 0.5
            )
            answer = raw.get("answer")
            verdict = bool(answer) if isinstance(answer, bool) else probability >= threshold
            answers[question.name] = DecisionAnswer(
                type="noul",
                answer=verdict,
                probability=probability,
                confidence=float(
                    raw.get("confidence", probability if verdict else 1.0 - probability)
                ),
            )
        elif question.type == "choice":
            probabilities = {
                str(key): float(value) for key, value in (raw.get("probabilities") or {}).items()
            }
            chosen = str(raw.get("answer", "") or "")
            if chosen not in probabilities and probabilities:
                chosen = max(probabilities, key=lambda key: probabilities[key])
            answers[question.name] = DecisionAnswer(
                type="choice",
                answer=chosen,
                probabilities=probabilities,
                confidence=float(raw.get("confidence", probabilities.get(chosen, 0.0))),
            )
        else:
            probabilities = {
                str(key): float(value) for key, value in (raw.get("probabilities") or {}).items()
            }
            # THE SCORE ANSWER IS THE PROBABILITY-WEIGHTED LEVEL, computed here
            # and never taken from the model: a model that states a distribution
            # and separately states a mean can contradict itself, and the
            # distribution is the thing it was actually asked for.
            total = sum(probabilities.values())
            weighted = (
                sum(float(level) * weight for level, weight in probabilities.items()) / total
                if total > 0
                else 0.0
            )
            answers[question.name] = DecisionAnswer(
                type="score",
                answer=weighted,
                probabilities=probabilities,
                confidence=float(raw.get("confidence", 0.0)),
                legend=_score_legend(question),
            )

    return DecisionAnswers(
        model=model,
        method="verbalized",
        answers=answers,
        unanswerable=unanswerable,
        usage=DecisionUsage(input_tokens=input_tokens, output_tokens=output_tokens),
        cost_usd=cost_usd,
    )


# ---------------------------------------------------------------------------
# The verbalized overlay — the same part, rendered for a text model
# ---------------------------------------------------------------------------


class VerbalizedDecisionOverlay:
    """What a text-model turn needs to become a decision turn.

    Held for the duration of ONE request: the batch that was asked and the
    question part's message index, so the response can be turned back into the
    same ``decision_answers`` shape a native holder would have produced. The
    two paths differ in the number they return and in ``method`` — never in the
    question that was asked.
    """

    __slots__ = ("batch", "message_index", "state")

    def __init__(self, batch: DecisionQuestions, message_index: int, state: dict[str, Any]):
        self.batch = batch
        self.message_index = message_index
        self.state = state


def prepare_verbalized_decision(
    config: Any,
    *,
    model_name: str,
    supports_structured_output: bool,
) -> VerbalizedDecisionOverlay | None:
    """Render a ``decision_questions`` part for a NON-decision model.

    The part is replaced in place by prose — the state, then each question with
    its criteria — and the request is bound to a response schema that returns
    the ``decision_answers`` shape. The schema is built PER BATCH rather than
    from the registered kind because the question names are the answer's field
    names: a generic ``decision_answers`` schema would let a model invent or
    omit a question, which is the one thing a decision contract exists to stop.

    Returns ``None`` when there is nothing to do. Raises when the model cannot
    honour the contract at all — a decision asked of a model that cannot return
    a structured answer would come back as prose nobody can score, and the
    compatibility law says say so, never guess.
    """
    messages = list(getattr(config, "messages", None) or [])
    try:
        index, batch = find_decision_questions(messages)
    except DecisionQuestionsMissing:
        return None

    refuse_incompatible_parts(messages[index], model_name=model_name)
    if not supports_structured_output:
        raise DecisionCompatibilityError(
            f"The message asks decision questions, but {model_name!r} does not "
            "support structured output, so it cannot return the answers with "
            "their probabilities in a shape anything can read. Choose a model "
            "that supports structured output, or a native decision model."
        )

    state = build_decision_state(
        messages,
        index,
        system_instruction=getattr(config, "system_instruction", None),
    )

    from matrx_ai.config.response_format import (
        OutputSchemaEnvelope,
        ResponseFormatJsonSchema,
    )
    from matrx_ai.config.unified_content import TextContent

    message = messages[index]
    message.content = [
        block
        for block in (getattr(message, "content", None) or [])
        if _content_type(block) != "decision_questions"
    ]
    message.content.append(TextContent(text=verbalized_instructions(state, batch)))

    config.response_format = ResponseFormatJsonSchema(
        type="json_schema",
        json_schema=OutputSchemaEnvelope(
            name="decision_answers",
            schema=verbalized_response_schema(batch),
            strict=True,
        ),
    )
    return VerbalizedDecisionOverlay(batch, index, state)


def finalize_verbalized_decision(
    response: Any,
    overlay: VerbalizedDecisionOverlay,
    *,
    model_name: str,
    cost_usd: float,
) -> Any:
    """Turn the text model's structured reply back into a decision turn.

    The assistant message's content becomes ONE ``decision_answers`` part, so a
    verbalized decision is indistinguishable from a native one everywhere
    downstream EXCEPT in ``method``, which is exactly the distinction that must
    survive. A reply that is not parseable JSON is not silently turned into an
    all-refusal answer: it raises, because a decision system that answers
    "unanswerable" when it actually failed to read its own model is lying about
    the model.
    """
    from matrx_ai.agents.response_parser import extract_json
    from matrx_ai.config.decision_input_config import DecisionAnswersContent

    messages = list(getattr(response, "messages", None) or [])
    if not messages:
        raise DecisionCompatibilityError(
            f"{model_name!r} returned no message for a decision request."
        )
    text = "\n".join(
        block.text
        for block in (getattr(messages[-1], "content", None) or [])
        if isinstance(getattr(block, "text", None), str) and block.text.strip()
    )
    payload = extract_json(text)
    if not isinstance(payload, dict):
        raise DecisionCompatibilityError(
            f"{model_name!r} answered the decision questions with text that is not "
            "the structured answer it was bound to return, so there are no "
            f"probabilities to record. First 200 characters: {text[:200]!r}"
        )

    usage = getattr(response, "usage", None)
    answers = decision_answers_from_verbalized(
        payload,
        overlay.batch,
        model=model_name,
        input_tokens=int(getattr(usage, "input_tokens", 0) or 0),
        output_tokens=int(getattr(usage, "output_tokens", 0) or 0),
        cost_usd=cost_usd,
    )
    messages[-1].content = [DecisionAnswersContent(answers=answers)]
    response.messages = messages
    metadata = getattr(response, "metadata", None)
    if isinstance(metadata, dict):
        metadata["decision"] = True
        metadata["method"] = answers.method
    return response
