"""ask_user tool — pauses the agent loop to ask the user a question (#299)."""

from __future__ import annotations

import logging
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)

AskCallback = Callable[[str, list[str] | None], Coroutine[Any, Any, str | None]]
MAX_ANSWER_CHARS = 4096

DEFINITION: dict[str, Any] = {
    "name": "ask_user",
    "description": (
        "Ask the user a question and wait for their response. "
        "Use this when you need information you cannot infer from context, tools, or prior conversation. "
        "Do NOT ask questions in your text output — use this tool instead. "
        "Provide options when the user should see suggested choices; users may still provide custom text."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question to ask the user. Be specific and focused — ask one thing at a time.",
            },
            "options": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Optional list of suggested choices for the user to pick from. "
                    "Omit for freeform text input. When provided, users may select an option or type custom text."
                ),
            },
        },
        "required": ["question"],
    },
}

_CANCEL_SENTINEL: None = None


async def handle(
    question: str,
    options: list[str] | None = None,
    _ask_callback: AskCallback | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Prompt the user and return their answer.

    The _ask_callback is injected by the tool_executor at call time.
    Callback contract: returns ``None`` for cancel (user typed ``x``,
    pressed Ctrl-D/Ctrl-C, or system aborted the prompt); returns a
    string — including ``""`` — for a real submission (an empty string
    means "user pressed Enter with no content").
    """
    if not question or not question.strip():
        return {"error": "Question cannot be empty"}

    if _ask_callback is None:
        logger.warning("ask_user called with no callback — failing closed")
        return {
            "error": "No interactive input available. Make your best judgment and proceed.",
        }

    _clean_options_list = [o[:256] for o in (options or []) if o and o.strip()][:20]
    clean_options: list[str] | None = _clean_options_list if _clean_options_list else None

    try:
        answer = await _ask_callback(question.strip(), clean_options)
        if answer is _CANCEL_SENTINEL:
            return {"cancelled": True, "answer": ""}
        if len(answer) > MAX_ANSWER_CHARS:
            answer = answer[:MAX_ANSWER_CHARS]
        return {"answer": answer}
    except (EOFError, KeyboardInterrupt):
        return {"cancelled": True, "answer": ""}
    except Exception as e:
        logger.error("ask_user callback failed: %s", e)
        return {"error": f"Failed to get user input: {type(e).__name__}"}
