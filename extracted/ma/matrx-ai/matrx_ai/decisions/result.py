"""Find the ``decision_answers`` part a completed turn carries — ONE reader.

WHY THIS EXISTS. A decision agent's assistant turn is ONE typed part
(``DecisionAnswersContent``) and no text. Every consumer that reads a
completed turn by its TEXT — the workflow ``ai.agent.start`` step, the
``pipe.step`` AI leg, a mandate's parsed artifact, the MCP ``agent_run`` tool —
saw an empty string and either failed ("no answer") or passed ``""``
downstream, while the decision had in fact run, been paid for and persisted
(measured 2026-09-26: the Feedback triage agent through the shared agent
runner returned ``final_text=''``, ``structured_output=None``, ``content=[]``).

The answer is not text, so it is never recovered by parsing text. Every
consumer reads it here, from the turn's own content, in whatever shape the
turn arrived: a ``UnifiedResponse``, a ``UnifiedMessage``, a content list, a
persisted message dict, or an already-dumped part.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.decisions.kinds import DecisionAnswers

__all__ = [
    "decision_answers_in",
    "decision_answers_part",
    "declared_decision_names",
    "declared_decision_questions",
    "output_keys_of",
]

_KIND = "decision_answers"


def _from_part(part: Any) -> DecisionAnswers | None:
    if part is None:
        return None
    if isinstance(part, DecisionAnswers):
        return part
    if isinstance(part, dict):
        marker = part.get("type") or part.get("__kind")
        if marker != _KIND:
            return None
        payload = {k: v for k, v in part.items() if k not in ("type", "metadata")}
        payload.setdefault("__kind", _KIND)
        return DecisionAnswers.model_validate(payload)
    marker = getattr(part, "type", None)
    if marker != _KIND:
        return None
    answers = getattr(part, "answers", None)
    if isinstance(answers, DecisionAnswers):
        return answers
    to_storage = getattr(part, "to_storage_dict", None)
    if callable(to_storage):
        return _from_part(to_storage())
    return None


def _from_content(content: Any) -> DecisionAnswers | None:
    if not isinstance(content, list):
        return _from_part(content) if content is not None else None
    for part in reversed(content):
        found = _from_part(part)
        if found is not None:
            return found
    return None


def _role(message: Any) -> Any:
    if isinstance(message, dict):
        return message.get("role")
    return getattr(message, "role", None)


def _content(message: Any) -> Any:
    if isinstance(message, dict):
        return message.get("content")
    return getattr(message, "content", None)


def decision_answers_in(source: Any) -> DecisionAnswers | None:
    """The decision answers the LAST assistant turn of ``source`` carries.

    ``source`` may be a response (``.messages``), one message (``.content``), a
    list of messages, a content list, or a single part. Returns ``None`` when
    the turn is not a decision turn — never a guess.
    """
    if source is None:
        return None
    direct = _from_part(source)
    if direct is not None:
        return direct
    messages = source.get("messages") if isinstance(source, dict) else getattr(source, "messages", None)
    if isinstance(messages, list) and messages:
        return decision_answers_in(messages)
    if isinstance(source, list):
        if source and all(_role(item) is not None for item in source):
            for message in reversed(source):
                if _role(message) == "assistant":
                    return _from_content(_content(message))
            return None
        return _from_content(source)
    message = getattr(source, "message", None)
    if message is not None and message is not source:
        found = decision_answers_in(message)
        if found is not None:
            return found
    content = _content(source)
    if content is not None:
        return _from_content(content)
    return None


def decision_answers_part(source: Any) -> dict[str, Any] | None:
    """The same answers as the kind instance a graph payload carries (``__kind`` set)."""
    answers = decision_answers_in(source)
    return answers.to_part() if answers is not None else None


def _as_message_list(messages: Any) -> list[Any]:
    if messages is None or isinstance(messages, str | dict | bytes):
        return []
    if isinstance(messages, list):
        return messages
    inner = getattr(messages, "messages", None)
    if isinstance(inner, list):
        return inner
    try:
        return list(messages)
    except TypeError:
        return []


def declared_decision_names(messages: Any) -> list[str]:
    """The answer field names an agent DEFINITION declares through its Questions parts.

    A decision agent declares its output contract as ``decision_questions``
    parts, not as an ``output_schema``: each question's ``name`` is one answer
    key. Every contract check that asks "which output keys does this holder
    produce?" (the mandate bind/run pre-flight, the MCP catalog, the workflow
    decision node's handles) reads them here, so a decision holder is never
    refused as "declares no structured output at all".
    """
    if isinstance(messages, str):
        import json

        try:
            messages = json.loads(messages)
        except ValueError:
            return []
    messages = _as_message_list(messages)
    names: list[str] = []
    for message in messages:
        content = _content(message)
        if not isinstance(content, list):
            continue
        for part in content:
            if not isinstance(part, dict):
                to_storage = getattr(part, "to_storage_dict", None)
                part = to_storage() if callable(to_storage) else None
            if not isinstance(part, dict):
                continue
            if (part.get("type") or part.get("__kind")) != "decision_questions":
                continue
            for question in part.get("questions") or []:
                name = question.get("name") if isinstance(question, dict) else None
                if isinstance(name, str) and name and name not in names:
                    names.append(name)
    return names


def declared_decision_questions(messages: Any) -> list[dict[str, Any]]:
    """The full question dicts (name, type, suggested_threshold …) a definition declares."""
    if isinstance(messages, str):
        import json

        try:
            messages = json.loads(messages)
        except ValueError:
            return []
    out: list[dict[str, Any]] = []
    for message in _as_message_list(messages):
        content = _content(message)
        if not isinstance(content, list):
            continue
        for part in content:
            if not isinstance(part, dict):
                to_storage = getattr(part, "to_storage_dict", None)
                part = to_storage() if callable(to_storage) else None
            if isinstance(part, dict) and (part.get("type") or part.get("__kind")) == "decision_questions":
                out.extend(q for q in part.get("questions") or [] if isinstance(q, dict))
    return out


def output_keys_of(artifact: Any) -> set[str]:
    """The output keys an artifact ANSWERS — the one reading every key check uses.

    A flat structured answer's keys are its top-level keys. A
    ``decision_answers`` artifact answers its question names inside
    ``answers``; a refusal in ``unanswerable`` is an answer too, never a
    missing key.
    """
    if not isinstance(artifact, dict):
        return set()
    if artifact.get("__kind") == _KIND:
        return set(artifact.get("answers") or {}) | set(artifact.get("unanswerable") or {})
    return set(artifact)
