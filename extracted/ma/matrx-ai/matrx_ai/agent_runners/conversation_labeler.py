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
stays as light as it was: one turn, no tools, not streamed (``HeldCall.send``). Its run
is kept as a hidden ``system_process`` conversation linked to the one it names — never a
helper in that chat's sidebar, never in any list. The day-one Holders are the old prompt verbatim
on the same model (``openai/gpt-oss-20b`` served by Groq, reasoning effort low,
JSON object mode, 2048 output tokens).

What stays in code is DATA bounding, never instructions: the character caps below
keep an untrusted 227K-character agent definition from blowing the provider's
per-minute token admission (regression tests in
``tests/test_conversation_labeler_provider.py``).
"""

from __future__ import annotations

import asyncio
import re
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


#: At most this many of the person's variable values reach the labeler.
USER_VARIABLES_MAX_COUNT = 30


def _bounded_user_variables(values: dict[str, Any] | str) -> dict[str, Any] | str:
    """The person's variable values, RAW (the prompt door renders them), each bounded.

    A dict stays a dict — never flattened into "name: value" lines in code — and
    each value that would blow the budget is trimmed. A string (a caller that
    already holds text) is trimmed as a whole.
    """
    if isinstance(values, str):
        return _trim_content(values, USER_VARIABLES_MAX_CHARS)
    kept = list(values.items())[:USER_VARIABLES_MAX_COUNT]
    per_value = max(200, USER_VARIABLES_MAX_CHARS // max(1, len(kept)))
    bounded: dict[str, Any] = {}
    for name, value in kept:
        text = value if isinstance(value, str) else str(value)
        if len(text) > per_value:
            bounded[name] = _trim_content(text, per_value)
        else:
            bounded[name] = value
    return bounded


def _agent_variables(
    agent_name: str,
    agent_description: str,
    user_variables: dict[str, Any] | str,
    user_prompt: str,
) -> dict[str, Any]:
    return {
        "agent_name": _trim_content(agent_name, AGENT_NAME_MAX_CHARS),
        "agent_description": _trim_content(agent_description, AGENT_DESCRIPTION_MAX_CHARS)
        if agent_description
        else NOT_AVAILABLE,
        "user_variables": _bounded_user_variables(user_variables)
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


_ARTIFACT_BLOCK = re.compile(r"<artifact\b([^>]*)>.*?(?:</artifact>|\Z)", re.DOTALL | re.IGNORECASE)
_ARTIFACT_TYPE = re.compile(r"""\btype\s*=\s*["']?([A-Za-z0-9_\- ]+)""")


def _strip_artifact_markup(text: str) -> str:
    """An ``<artifact …>`` block is stored markup, not words the person said or read.

    The namer used to read the tag itself and title chats "… with Artifact Chart"
    (review 4, F13). The block becomes one neutral word for what it holds ("chart",
    or "attachment" when the tag names no type); its body never reaches the namer.
    """

    def _label(match: re.Match[str]) -> str:
        kind = _ARTIFACT_TYPE.search(match.group(1))
        return f"[{kind.group(1).strip().lower() if kind else 'attachment'}]"

    return _ARTIFACT_BLOCK.sub(_label, text)


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
        content = _strip_artifact_markup(content)
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
    variables: dict[str, Any],
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
            # The labeler is the system's job, not the person's (Arman, 2026-10-19): its failure
            # record names the conversation it was labeling, never the person.
            user_id=None,
            conversation_id=getattr(ctx, "conversation_id", None) if ctx else None,
            source_app=getattr(ctx, "source_app", None) if ctx else None,
            source_feature=getattr(ctx, "source_feature", None),
            route=getattr(ctx, "route", None) if ctx else None,
            error_type=type(exc).__name__,
            error_text=str(exc),
            payload={"mandate_key": mandate_key, "model": model},
            context={name: len(str(value)) for name, value in variables.items()},
        )
    except Exception as capture_exc:
        vcprint(
            f"[ConversationLabeler] Failure capture failed: {capture_exc}",
            color="red",
        )


#: The system-process key the host's drain knows this work by (aidream services/system_processes).
LABEL_PROCESS_KEY = "conversation.name"


def system_process_scope(conversation_id: str | None) -> Any:
    """The platform identity a system process runs as (host seam), or a no-op when unset.

    Inside it the held call is billed to the platform and its run becomes a hidden
    ``system_process`` conversation linked to ``conversation_id`` (Arman, 2026-10-18).
    """
    import contextlib

    from matrx_ai._ext import get_system_process_scope

    scope = get_system_process_scope()
    if scope is None:
        return contextlib.nullcontext()
    return scope(feature="system_process", conversation_id=conversation_id)


async def _run_labeler(
    mandate_key: str, variables: dict[str, Any], *, conversation_id: str | None = None
) -> LabelResult:
    """One held labeler call: the Holder's model, prompt and settings, nothing else — run as the
    platform, inside the conversation it names."""
    from matrx_ai.mandates import Offer, RunOptions, get_mandate_runner, system_principal

    model: str | None = None
    try:
        async with system_process_scope(conversation_id):
            # Runner plan 25 step 6: prepared through the one runner, as SYSTEM (a system job — no user,
            # no user organization, no user billing); the held call sends itself and closes the run.
            prepared = await get_mandate_runner().prepare(
                mandate_key,
                Offer.given_values(variables),
                who=system_principal(),
                opts=RunOptions(door="package_code_call", consumer="conversation.labeler"),
            )
            held = prepared.held_call()
            model = held.model
            result = await held.send()
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
    *,
    conversation_id: str | None = None,
) -> LabelResult:
    from matrx_ai.code_call_mandate_keys import CONVERSATION_LABEL_CHAT_MANDATE

    return await _run_labeler(
        CONVERSATION_LABEL_CHAT_MANDATE,
        _chat_variables(conversation_content, recent_titles),
        conversation_id=conversation_id,
    )


async def label_agent_conversation(
    conversation_content: str,
    recent_titles: str,
    agent_name: str,
    agent_description: str,
    user_variables: dict[str, Any] | str,
    user_prompt: str,
    *,
    conversation_id: str | None = None,
) -> LabelResult:
    from matrx_ai.code_call_mandate_keys import CONVERSATION_LABEL_AGENT_RUN_MANDATE

    if not agent_name:
        return await label_chat_conversation(
            conversation_content, recent_titles, conversation_id=conversation_id
        )
    return await _run_labeler(
        CONVERSATION_LABEL_AGENT_RUN_MANDATE,
        {
            **_chat_variables(conversation_content, recent_titles),
            **_agent_variables(agent_name, agent_description, user_variables, user_prompt),
        },
        conversation_id=conversation_id,
    )
