"""Prompt engine — loads system prompt and few-shot examples for the coding AI.

The system prompt defines LocalCoder's identity and behavior rules.
Few-shot examples teach response patterns. Both are loaded from disk
so users can customize them without changing code.
"""

import logging
from pathlib import Path

from .config import settings
from .schemas import ChatMessage

logger = logging.getLogger("ai-platform.prompt")

_BASE = Path(__file__).resolve().parent.parent
_PROMPTS_DIR = _BASE / "prompts"

_system_prompt_cache: str | None = None
_fewshot_cache: list[dict] | None = None


def load_system_prompt() -> str:
    """Load the system prompt from prompts/system.txt."""
    global _system_prompt_cache
    if _system_prompt_cache is not None:
        return _system_prompt_cache

    path = _PROMPTS_DIR / "system.txt"
    if not path.exists():
        logger.warning("No system prompt found at %s — using default", path)
        _system_prompt_cache = "You are a helpful coding assistant."
        return _system_prompt_cache

    _system_prompt_cache = path.read_text(encoding="utf-8").strip()
    logger.info("Loaded system prompt (%d chars) from %s", len(_system_prompt_cache), path)
    return _system_prompt_cache


def load_fewshot_examples() -> list[dict]:
    """Load few-shot examples from prompts/fewshot.md.

    Parses the markdown into user/assistant message pairs.
    """
    global _fewshot_cache
    if _fewshot_cache is not None:
        return _fewshot_cache

    path = _PROMPTS_DIR / "fewshot.md"
    if not path.exists():
        _fewshot_cache = []
        return _fewshot_cache

    text = path.read_text(encoding="utf-8")
    pairs = _parse_fewshot(text)
    _fewshot_cache = pairs
    logger.info("Loaded %d few-shot example pairs from %s", len(pairs), path)
    return _fewshot_cache


def build_messages(
    user_messages: list[ChatMessage],
    include_system: bool = True,
    include_fewshot: bool = False,
) -> list[ChatMessage]:
    """Build the full message list with system prompt and optional few-shot examples.

    Order: [system] + [fewshot pairs] + user_messages
    """
    result: list[ChatMessage] = []

    if include_system:
        system_text = load_system_prompt()
        result.append(ChatMessage(role="system", content=system_text))

    if include_fewshot:
        for pair in load_fewshot_examples():
            result.append(ChatMessage(role="user", content=pair["user"]))
            result.append(ChatMessage(role="assistant", content=pair["assistant"]))

    result.extend(user_messages)
    return result


def clear_cache() -> None:
    """Clear cached prompts (useful for testing or hot-reloading)."""
    global _system_prompt_cache, _fewshot_cache
    _system_prompt_cache = None
    _fewshot_cache = None


def _parse_fewshot(text: str) -> list[dict]:
    """Parse fewshot.md into [{user: ..., assistant: ...}, ...] pairs."""
    pairs = []
    sections = text.split("---")

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Skip if the section is ONLY a header with no User/Assistant markers
        if "**User:**" not in section:
            continue

        user_text = ""
        assistant_text = ""
        current = None

        for line in section.split("\n"):
            stripped = line.strip()
            if stripped.startswith("**User:**"):
                current = "user"
                user_text = stripped.replace("**User:**", "").strip()
                continue
            elif stripped.startswith("**Assistant:**"):
                current = "assistant"
                assistant_text = stripped.replace("**Assistant:**", "").strip()
                continue

            # Skip section headers like "## Example 1: Bug Fix"
            if current is None:
                continue

            if current == "user":
                user_text += "\n" + line
            elif current == "assistant":
                assistant_text += "\n" + line

        user_text = user_text.strip()
        assistant_text = assistant_text.strip()

        if user_text and assistant_text:
            pairs.append({"user": user_text, "assistant": assistant_text})

    return pairs
