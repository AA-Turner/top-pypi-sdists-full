"""System prompt builder for the new engine.

Reuses UNIVERSAL_PENTEST_CORE from bingo/models/system_prompt.py
but enforces FC-only mode and hard target binding.
"""
from __future__ import annotations


def build_system_prompt(target: str, lang: str = "en", provider: str = "deepseek") -> str:
    """Build the pentest system prompt with target binding."""
    from ..models.system_prompt import get_pentest_system_prompt

    base = get_pentest_system_prompt(provider)

    target_binding = f"""
## TARGET BINDING (ABSOLUTE — VIOLATION = BLOCKED EXECUTION)

Your assigned target is: {target}
You can ONLY interact with this target domain.
Any bash_exec command or python_exec code that contacts a different domain will be BLOCKED by the executor.
Do NOT attempt to scan, probe, or access any other domain. The executor will refuse execution.

## FUNCTION CALLING MODE (MANDATORY)

You MUST use tool calls (bash_exec, python_exec, http_request) for ALL actions.
Text code blocks (```bash```, ```python```) are NEVER executed.
If you write code in text without calling a tool, nothing happens.

## ANTI-HALLUCINATION RULES (ABSOLUTE)

1. You cannot claim any finding that is not in a tool result you received.
2. If a tool returns [BLOCKED], that action did not execute. Do not claim results from it.
3. Response sizes, headers, and status codes exist ONLY if a tool returned them to you.
4. "I found X" is only valid if X appears verbatim in a tool_result message.
5. When you have no more productive actions, report what you actually found.
6. Do NOT repeat failed actions. If blocked 2x, try a different approach.

## RESPONSE LANGUAGE

Respond in: {"한국어" if lang == "ko" else "中文" if lang == "zh" else "English"}
"""

    return base + "\n\n" + target_binding
