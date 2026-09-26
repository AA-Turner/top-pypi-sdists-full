"""Conversation labeler — title, description and keywords for every conversation.

Held by two mandates (2026-09-25, BYPASS-CENSUS aidream section): a plain chat is
labeled by ``conversation.label_chat``; a conversation an agent started is labeled
by ``conversation.label_agent_run``, whose prompt tells it to weigh the user's
variables over the agent's fixed template. Each call runs on its Holder's model,
prompt and settings — including the JSON response format and reasoning effort — so
a change to the mandate (a rebind, a model swap, a prompt edit) takes effect with
no deploy.

This used to be a deliberate exception (Arman, 2026-06-07): a direct ``AsyncGroq``
call with an inline prompt, to keep a per-request background job cheap. Arman's
2026-09-25 law supersedes it — nothing works around the mandate system. The call
stays as light as it was: one turn, no tools, not streamed, not persisted as a
conversation (``run_held_call``). The day-one Holders are the old prompt verbatim
on the same model (``openai/gpt-oss-20b`` served by Groq, reasoning effort low,
JSON object mode, 2048 output tokens).

What stays in code is DATA bounding, never instructions: the character caps below
keep an untrusted 227K-character agent definition from blowing the provider's
per-minute token admission (regression tests in
``tests/test_conversation_labeler_provider.py``).
"""

from __future__ import annotations

import asyncio
from typing import Any

from matrx_utils import vcprint
from pydantic import BaseModel, Field

# This call is shared background metadata work. Agent definitions and variable
# values can be hundreds of thousands of characters, but a label needs only a
# compact identifying sample. Keep the complete request comfortably below the
# provider's token-per-minute admission boundary.
RECENT_TITLES_MAX_CHARS = 2000
AGENT_NAME_MAX_CHARS = 500
AGENT_DESCRIPTION_MAX_CHARS = 3000
USER_VARIABLES_MAX_CHARS = 6000
USER_PROMPT_MAX_CHARS = 3000


class ConversationLabelResult(BaseModel):
    label: str = ""
    description: str = ""
    keywords: list[str] = Field(default_factory=list)


#: What a variable reads when there is nothing to put in it. Values, not prompt.
NONE_VALUE = "None"
NOT_AVAILABLE = "N/A"
NONE_PROVIDED = "None provided"


def _chat_variables(conversation_content: str, recent_titles: str) -> dict[str, str]:
    return {
        "conversation_content": conversation_content,
        "recent_titles": _trim_content(recent_titles, RECENT_TITLES_MAX_CHARS)
        if recent_titles and recent_titles.strip()
        else NONE_VALUE,
    }


def _agent_variables(
    agent_name: str,
    agent_description: str,
    user_variables: str,
    user_prompt: str,
) -> dict[str, str]:
    return {
        "agent_name": _trim_content(agent_name, AGENT_NAME_MAX_CHARS),
        "agent_description": _trim_content(agent_description, AGENT_DESCRIPTION_MAX_CHARS)
        if agent_description
        else NOT_AVAILABLE,
        "user_variables": _trim_content(user_variables, USER_VARIABLES_MAX_CHARS)
        if user_variables
        else NONE_PROVIDED,
        "user_prompt": _trim_content(user_prompt, USER_PROMPT_MAX_CHARS)
        if user_prompt
        else NONE_PROVIDED,
    }


def _trim_content(content: str, max_chars: int = 5000) -> str:
    if len(content) <= max_chars:
        return content
    trim_msg = "\n\n[... content trimmed ...]\n\n"
    available = max_chars - len(trim_msg)
    if available < 100:
        available = 100
    half = available // 2
    return f"{content[:half]}{trim_msg}{content[-half:]}"


def _format_messages_for_labeling(
    messages: list[dict[str, Any]], max_total_chars: int = 5000
) -> str:
    parts: list[str] = []
    for msg in messages:
        role = msg.get("role", "unknown")
        if role not in ("user", "assistant"):
            continue
        content = msg.get("content", "")
        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
                elif isinstance(item, str):
                    text_parts.append(item)
            content = "\n".join(text_parts)
        if not isinstance(content, str):
            content = str(content)
        parts.append(f"{role.capitalize()}:\n{content}")

    combined = "\n\n".join(parts)
    return _trim_content(combined, max_total_chars)


class LabelResult(BaseModel):
    success: bool
    output: str
    error: str = ""


async def _capture_labeler_failure(
    exc: BaseException,
    *,
    mandate_key: str,
    model: str | None,
    variables: dict[str, str],
) -> None:
    """Capture a paid labeler failure without persisting conversation text."""
    try:
        from matrx_connect import try_get_app_context
        from matrx_connect.streaming.error_capture import capture_error

        ctx = try_get_app_context()
        await capture_error(
            exc,
            kind="conversation_labeler_failed",
            request_id=getattr(ctx, "request_id", None) if ctx else None,
            user_id=getattr(ctx, "user_id", None) if ctx else None,
            conversation_id=getattr(ctx, "conversation_id", None) if ctx else None,
            source_app=getattr(ctx, "source_app", None) if ctx else None,
            source_feature=getattr(ctx, "source_feature", None),
            route=getattr(ctx, "route", None) if ctx else None,
            error_type=type(exc).__name__,
            error_text=str(exc),
            payload={"mandate_key": mandate_key, "model": model},
            context={name: len(value) for name, value in variables.items()},
        )
    except Exception as capture_exc:
        vcprint(
            f"[ConversationLabeler] Failure capture failed: {capture_exc}",
            color="red",
        )


async def _run_labeler(mandate_key: str, variables: dict[str, str]) -> LabelResult:
    """One held labeler call: the Holder's model, prompt and settings, nothing else."""
    from matrx_ai.mandates import hold_code_call, run_held_call

    model: str | None = None
    try:
        held = await hold_code_call(
            mandate_key, consumer="conversation.labeler", variables=variables
        )
        model = held.model
        result = await run_held_call(held, store=False)
        return LabelResult(success=True, output=result.final_text or "")
    except asyncio.CancelledError as exc:
        await _capture_labeler_failure(
            exc, mandate_key=mandate_key, model=model, variables=variables
        )
        raise
    except Exception as e:
        await _capture_labeler_failure(e, mandate_key=mandate_key, model=model, variables=variables)
        vcprint(f"[ConversationLabeler] {mandate_key} call failed: {e}", color="red")
        return LabelResult(success=False, output="", error=str(e))


async def label_chat_conversation(
    conversation_content: str,
    recent_titles: str,
) -> LabelResult:
    from matrx_ai.code_call_mandate_keys import CONVERSATION_LABEL_CHAT_MANDATE

    return await _run_labeler(
        CONVERSATION_LABEL_CHAT_MANDATE, _chat_variables(conversation_content, recent_titles)
    )


async def label_agent_conversation(
    conversation_content: str,
    recent_titles: str,
    agent_name: str,
    agent_description: str,
    user_variables: str,
    user_prompt: str,
) -> LabelResult:
    from matrx_ai.code_call_mandate_keys import CONVERSATION_LABEL_AGENT_RUN_MANDATE

    if not agent_name:
        return await label_chat_conversation(conversation_content, recent_titles)
    return await _run_labeler(
        CONVERSATION_LABEL_AGENT_RUN_MANDATE,
        {
            **_chat_variables(conversation_content, recent_titles),
            **_agent_variables(agent_name, agent_description, user_variables, user_prompt),
        },
    )
