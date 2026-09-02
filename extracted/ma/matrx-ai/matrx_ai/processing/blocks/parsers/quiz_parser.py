"""Quiz parser.

Accepts both snake_case and camelCase field names from the LLM — small models
in particular often mix conventions.  The canonical output is always the
validated QuizBlockData model serialized with camelCase keys (via by_alias=True).

Expected LLM JSON shape (either key style accepted):
    {
        "quiz_title" | "quizTitle": str,
        "category": str,                   # optional
        "multiple_choice" | "multipleChoice": [
            {
                "id": int,                 # OPTIONAL — position is used when absent
                "question": str,
                "options": [str, ...],
                "correct_answer" | "correctAnswer": int | str,
                "explanation": str
            },
            ...
        ]
    }

🚨 TWO THINGS THIS ACCEPTS THAT IT USED TO REJECT, and why (2026-08-22).

A live agent asked for "a quiz as a fenced json block" wrote the shape any
person would write: no `id` on the questions, and `"correct_answer":
"Chlorophyll"` — the ANSWER, not its index. The parser required a numeric id
and an integer index, so it returned None; the block was stamped
``parseError`` with no ``data``; no ``__ir`` envelope could be built; and
``content_from_text`` folded the whole quiz into prose. What the reader got
was a wall of raw JSON where a quiz component should have been — measured on
run 41ee2991 and on Arman's own run a268ba41.

Both are NORMALISED, never loosened: the output is still exactly
``QuizBlockData`` with an int id and an int answer index, so every consumer
downstream is untouched.

- **Missing `id`** → the question's POSITION in the list. An id is a render
  key here, not data the model has any way to know.
- **String `correct_answer`** → the index of the option it matches (exact,
  then case/whitespace-insensitive). An answer that matches NO option is
  still a failure: that is a genuinely wrong quiz, and inventing an index
  would silently mark the wrong option correct.
"""

from __future__ import annotations

import json

from matrx_ai.processing.blocks.models.quiz import QuizBlockData, QuizQuestion
from matrx_ai.processing.blocks.parsers._llm_json import loads_block_json


# ---------------------------------------------------------------------------
# Key normalisation helpers
# ---------------------------------------------------------------------------

def _get(d: dict, *keys: str, default=None):
    """Return the first value found for any of the given key names."""
    for k in keys:
        if k in d:
            return d[k]
    return default


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_quiz(content: str) -> QuizBlockData | None:
    """
    Parse quiz JSON into a validated QuizBlockData.

    Returns None if the content is not valid JSON, or if it fails structural
    validation.  The caller records the failure reason in block metadata.
    """
    try:
        data = loads_block_json(content)
    except json.JSONDecodeError:
        return None

    if not isinstance(data, dict):
        return None

    # Accept both key styles for the title
    title = _get(data, "quiz_title", "quizTitle")
    if not title or not isinstance(title, str):
        return None

    # Accept both key styles for the question list
    mc = _get(data, "multiple_choice", "multipleChoice")
    if not isinstance(mc, list) or len(mc) == 0:
        return None

    questions: list[QuizQuestion] = []
    # Position is the fallback id, so the sort key has to be the position for
    # any question that lacks one — sorting an id-less list by a constant 0
    # would leave document order intact today and is one implementation
    # detail away from scrambling it.
    ordered = sorted(
        enumerate(mc),
        key=lambda pair: (
            pair[1].get("id")
            if isinstance(pair[1], dict) and isinstance(pair[1].get("id"), (int, float))
            else pair[0]
        ),
    )
    for position, q in ordered:
        parsed_q = _parse_question(q, position=position)
        if parsed_q is None:
            return None  # One bad question invalidates the whole block
        questions.append(parsed_q)

    return QuizBlockData(
        quiz_title=title,
        category=data.get("category"),
        multiple_choice=questions,
    )


def _answer_index(correct, options: list[str]) -> int | None:
    """The index of the correct option, from an index OR the answer text.

    A model that is handed an options list and asked which one is right
    answers with the OPTION, not with a subscript. Resolving it here keeps
    the model's natural output renderable while the stored value stays the
    index every consumer expects. No match is a real failure — a guessed
    index marks the wrong answer correct, which is worse than no quiz.
    """
    if isinstance(correct, bool):
        return None
    if isinstance(correct, (int, float)):
        index = int(correct)
        return index if 0 <= index < len(options) else None
    if not isinstance(correct, str):
        return None
    if correct in options:
        return options.index(correct)
    folded = correct.strip().casefold()
    for index, option in enumerate(options):
        if option.strip().casefold() == folded:
            return index
    return None


def _parse_question(q: dict, *, position: int = 0) -> QuizQuestion | None:
    """
    Parse a single question dict.  Returns None if any required field is missing
    or the wrong type — a partial question is worse than no question.

    ``position`` is the question's place in the list, used as its id when the
    model did not write one (see the module docstring).
    """
    if not isinstance(q, dict):
        return None

    q_id = q.get("id")
    question = q.get("question")
    options = q.get("options")
    # Accept both correctAnswer (camelCase) and correct_answer (snake_case)
    correct = _get(q, "correctAnswer", "correct_answer")
    explanation = q.get("explanation")

    if not isinstance(question, str) or not question.strip():
        return None
    if not isinstance(options, list) or len(options) < 2:
        return None
    rendered_options = [str(o) for o in options]
    answer_index = _answer_index(correct, rendered_options)
    if answer_index is None:
        return None
    if not isinstance(explanation, str):
        return None

    return QuizQuestion(
        id=int(q_id) if isinstance(q_id, (int, float)) and not isinstance(q_id, bool) else position,
        question=question,
        options=rendered_options,
        correct_answer=answer_index,
        explanation=explanation,
    )
