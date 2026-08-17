r"""Contain shared helpers for single-shot structured LLM calls."""

from __future__ import annotations

__all__ = ["ainvoke_structured_llm", "invoke_structured_llm"]

import logging
from typing import TYPE_CHECKING, Any

from coola.utils.timing import timeblock
from langchain_core.messages import HumanMessage, SystemMessage

from zenpyre.runnables import structured_output_runnable
from zenpyre.utils.token_usage import log_token_usage

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel
    from pydantic import BaseModel

logger: logging.Logger = logging.getLogger(__name__)


async def ainvoke_structured_llm(
    *,
    chat_model: BaseChatModel,
    output_type: type[BaseModel],
    system_prompt: str,
    user_content: str,
    timeblock_message: str = "LLM generated answer in {time}",
) -> tuple[Any, dict[str, Any]]:
    """Invoke *chat_model* for a structured *output_type* response.

    Shared by every agent's single-shot structured LLM call (adaptive
    query planning, assessment, judging): build the structured-output
    runnable, invoke it with a system/user message pair, and log token
    usage.

    Args:
        chat_model: LangChain chat model to invoke.
        output_type: Pydantic model the response must conform to.
        system_prompt: System prompt for the call.
        user_content: User message content for the call.
        timeblock_message: Message template passed to :func:`timeblock`
            (e.g. ``"LLM generated AI risk assessment in {time}"``).

    Returns:
        A tuple ``(parsed, raw_response)`` where ``parsed`` is the
        structured output (``None`` if the LLM failed to produce it) and
        ``raw_response`` is the raw LangChain response dict, for callers
        that need to inspect ``parsing_error`` or log the raw content on
        failure.
    """
    structured_llm = structured_output_runnable(
        chat_model, output_type=output_type, include_raw=True
    )
    with timeblock(timeblock_message):
        raw_response = await structured_llm.ainvoke(_build_messages(system_prompt, user_content))
    log_token_usage(raw_response)
    return raw_response["parsed"], raw_response


def invoke_structured_llm(
    *,
    chat_model: BaseChatModel,
    output_type: type[BaseModel],
    system_prompt: str,
    user_content: str,
    timeblock_message: str = "LLM generated answer in {time}",
) -> tuple[Any, dict[str, Any]]:
    """Invoke *chat_model* for a structured *output_type* response.

    Shared by every agent's single-shot structured LLM call (adaptive
    query planning, assessment, judging): build the structured-output
    runnable, invoke it with a system/user message pair, and log token
    usage.

    Args:
        chat_model: LangChain chat model to invoke.
        output_type: Pydantic model the response must conform to.
        system_prompt: System prompt for the call.
        user_content: User message content for the call.
        timeblock_message: Message template passed to :func:`timeblock`
            (e.g. ``"LLM generated AI risk assessment in {time}"``).

    Returns:
        A tuple ``(parsed, raw_response)`` where ``parsed`` is the
        structured output (``None`` if the LLM failed to produce it) and
        ``raw_response`` is the raw LangChain response dict, for callers
        that need to inspect ``parsing_error`` or log the raw content on
        failure.
    """
    structured_llm = structured_output_runnable(
        chat_model, output_type=output_type, include_raw=True
    )
    with timeblock(timeblock_message):
        raw_response = structured_llm.invoke(_build_messages(system_prompt, user_content))
    log_token_usage(raw_response)
    return raw_response["parsed"], raw_response


def _build_messages(system_prompt: str, user_content: str) -> list[SystemMessage | HumanMessage]:
    return [SystemMessage(content=system_prompt), HumanMessage(content=user_content)]
