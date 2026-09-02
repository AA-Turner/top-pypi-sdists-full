"""Conversation labeler — INTENTIONALLY OUTSIDE the canonical agent system.

╔══════════════════════════════════════════════════════════════════════════╗
║  DO NOT "migrate" THIS TO NamedAgent / run_agent / the agents table.       ║
║  This is a DELIBERATE, PERMANENT exception — not a defect, not tech debt,  ║
║  not a convergence gap. It will NEVER join THE ONE.                        ║
╚══════════════════════════════════════════════════════════════════════════╝

Why it is deliberately excluded (decided by Arman, 2026-06-07):

- It fires on **every single request** to label/summarize the conversation. It
  is hot-path background metadata, not a user-facing agent call. Routing it
  through the full agent stack (context fork, DB agent load, tool merge,
  emitter wiring, persistence barriers, validation) would add per-request
  overhead and failure surface for zero benefit.
- It must stay maximally simple and isolated: one direct `AsyncGroq` call to a
  tiny fast model (`llama-3.1-8b-instant`) with an inline prompt. No shared
  state, no agent registry, no version pinning, nothing that could couple a
  per-request convenience to the heavier agent pipeline.

Consequences for future agents/humans reading this file:

- This module never had a spec file and never
  should be. Its absence from the agent registry is correct.
- It does **not** belong in FOUND_DEFECTS.md. If you find a note flagging it as
  a non-canonical call site to migrate, delete that note — it is wrong.
- The inline prompt + bespoke prompt-assembly below is the intended design.
  Improve it in place if needed; do not relocate it into the central caller.
"""

from __future__ import annotations

import asyncio
from typing import Any

from groq import AsyncGroq
from matrx_utils import vcprint
from pydantic import BaseModel, Field

LABELER_MODEL = "openai/gpt-oss-20b"
# gpt-oss spends part of this budget on reasoning before emitting the JSON
# document. 650 can expire before the first complete object on long inputs.
LABELER_MAX_TOKENS = 2048
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


CONVERSATION_LABEL_SYSTEM_PROMPT = """You specialize in analyzing chat conversations and extracting structured metadata for labeling.

Your task is to generate a JSON object with three fields:

1. **label** — A short, distinctive title for this conversation (max ~8 words). This title will appear in a small sidebar, so brevity is critical. The label must differentiate THIS conversation from the user's recent conversations listed below. Do NOT reuse titles or phrasings from recent conversations. Look for the specific nuance that makes this conversation unique compared to others.

2. **description** — A concise summary of the conversation covering the key topics, user intent, and assistant contributions.

3. **keywords** — Up to 15 searchable keywords. Prioritize the user's intent and query topics, then include assistant-side topics. Include broader inferred topics beyond exact words used. Avoid repetitive or overlapping keywords since search uses partial matching.

### CRITICAL LABELING RULES:

- Your PRIMARY goal is to make the label easily distinguishable from all recent conversation titles listed below. When a user scans their sidebar, they need to instantly tell conversations apart.
- Do NOT name the conversation generically for what it is in isolation. Instead, find the specific detail or angle that sets it apart from recent conversations.
- If recent conversations cover the same broad topic, zoom into the SPECIFIC sub-topic, question, or variable that makes this one different.
- Keep labels SHORT — they must fit in a small sidebar. Avoid filler words.

{{recent_conversations_section}}

{{agent_context_section}}

Your response must be ONLY a valid JSON object. No other text, comments, or markdown fences.

Example:
{"label": "Country Size Comparison Table", "description": "User asked for a table of the world's biggest countries...", "keywords": ["countries", "geography", "world map", "table", "area"]}"""


RECENT_CONVERSATIONS_TEMPLATE = """### Recent Conversation Titles (AVOID duplicating these):
{{recent_titles}}

Look at the titles above. Your new label MUST be noticeably different from ALL of them. If the topic overlaps, find the specific angle or detail that differentiates this conversation."""


NO_RECENT_CONVERSATIONS = """### Recent Conversation Titles:
No recent conversations found. Generate the most descriptive and unique label you can."""


AGENT_CONTEXT_TEMPLATE = """### Important Context — Agent-Initiated Conversation:
This conversation was started by an AI agent (not a free-form user chat). The agent has a standard template/prompt that is mostly identical across all invocations. The ONLY things that change between invocations are the user-provided variables and optional user prompt.

**Agent Name:** {{agent_name}}
**Agent Description:** {{agent_description}}

**User-Provided Variables:**
{{user_variables}}

**User Prompt (if any):**
{{user_prompt}}

CRITICAL: When labeling agent conversations, you MUST heavily favor the user's variable values and user prompt over the agent's template content. The template is the same every time — the variables are what make each invocation unique. Base your label primarily on the specific values the user provided."""


NO_AGENT_CONTEXT = ""


def _build_user_message_for_chat(
    conversation_content: str,
) -> str:
    return f"""Generate the structured label information for this conversation:

==========

{conversation_content}

==========

Respond with a JSON object containing "label", "description", and "keywords"."""


def _build_recent_section(recent_titles: str) -> str:
    if not recent_titles or not recent_titles.strip():
        return NO_RECENT_CONVERSATIONS
    return RECENT_CONVERSATIONS_TEMPLATE.replace(
        "{{recent_titles}}", _trim_content(recent_titles, RECENT_TITLES_MAX_CHARS)
    )


def _build_agent_section(
    agent_name: str,
    agent_description: str,
    user_variables: str,
    user_prompt: str,
) -> str:
    if not agent_name:
        return NO_AGENT_CONTEXT
    section = AGENT_CONTEXT_TEMPLATE
    section = section.replace(
        "{{agent_name}}", _trim_content(agent_name, AGENT_NAME_MAX_CHARS)
    )
    section = section.replace(
        "{{agent_description}}",
        _trim_content(agent_description, AGENT_DESCRIPTION_MAX_CHARS)
        if agent_description
        else "N/A",
    )
    section = section.replace(
        "{{user_variables}}",
        _trim_content(user_variables, USER_VARIABLES_MAX_CHARS)
        if user_variables
        else "None provided",
    )
    section = section.replace(
        "{{user_prompt}}",
        _trim_content(user_prompt, USER_PROMPT_MAX_CHARS)
        if user_prompt
        else "None provided",
    )
    return section


def _build_system_prompt(
    recent_titles: str,
    agent_name: str,
    agent_description: str,
    user_variables: str,
    user_prompt: str,
) -> str:
    prompt = CONVERSATION_LABEL_SYSTEM_PROMPT
    recent_section = _build_recent_section(recent_titles)
    agent_section = _build_agent_section(agent_name, agent_description, user_variables, user_prompt)
    prompt = prompt.replace("{{recent_conversations_section}}", recent_section)
    prompt = prompt.replace("{{agent_context_section}}", agent_section)
    return prompt


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
    system_prompt: str,
    user_message: str,
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
            route=getattr(ctx, "route", None) if ctx else None,
            error_type=type(exc).__name__,
            error_text=str(exc),
            payload={
                "model": LABELER_MODEL,
                "max_tokens": LABELER_MAX_TOKENS,
                "temperature": 0.6,
                "response_format": {"type": "json_object"},
            },
            context={
                "system_prompt_chars": len(system_prompt),
                "user_message_chars": len(user_message),
            },
        )
    except Exception as capture_exc:
        vcprint(
            f"[ConversationLabeler] Failure capture failed: {capture_exc}",
            color="red",
        )


async def _call_groq_direct(system_prompt: str, user_message: str) -> LabelResult:
    from matrx_ai.providers.keys import resolve_api_key

    try:
        client = AsyncGroq(api_key=resolve_api_key("GROQ_API_KEY"))
        response = await client.chat.completions.create(
            model=LABELER_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=LABELER_MAX_TOKENS,
            temperature=0.6,
            reasoning_effort="low",
            response_format={"type": "json_object"},
            stream=False,
        )
        output = response.choices[0].message.content or ""
        return LabelResult(success=True, output=output)
    except asyncio.CancelledError as exc:
        await _capture_labeler_failure(
            exc,
            system_prompt=system_prompt,
            user_message=user_message,
        )
        raise
    except Exception as e:
        await _capture_labeler_failure(
            e,
            system_prompt=system_prompt,
            user_message=user_message,
        )
        vcprint(f"[ConversationLabeler] Groq call failed: {e}", color="red")
        return LabelResult(success=False, output="", error=str(e))


async def label_chat_conversation(
    conversation_content: str,
    recent_titles: str,
) -> LabelResult:
    system_prompt = _build_system_prompt(
        recent_titles=recent_titles,
        agent_name="",
        agent_description="",
        user_variables="",
        user_prompt="",
    )
    user_message = _build_user_message_for_chat(conversation_content)
    return await _call_groq_direct(system_prompt, user_message)


async def label_agent_conversation(
    conversation_content: str,
    recent_titles: str,
    agent_name: str,
    agent_description: str,
    user_variables: str,
    user_prompt: str,
) -> LabelResult:
    system_prompt = _build_system_prompt(
        recent_titles=recent_titles,
        agent_name=agent_name,
        agent_description=agent_description,
        user_variables=user_variables,
        user_prompt=user_prompt,
    )
    user_message = _build_user_message_for_chat(conversation_content)
    return await _call_groq_direct(system_prompt, user_message)
