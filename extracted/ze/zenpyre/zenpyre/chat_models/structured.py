r"""Contain shared helpers for single-shot structured LLM calls."""

from __future__ import annotations

__all__ = ["ainvoke_structured_llm", "invoke_structured_llm"]

import logging
from typing import TYPE_CHECKING, Any

from coola.utils.timing import timeblock
from coola.validation import validate_non_negative
from langchain_core.messages import HumanMessage, SystemMessage

from zenpyre.runnables import structured_output_runnable
from zenpyre.utils.token_usage import log_token_usage

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel, LanguageModelInput
    from langchain_core.runnables import Runnable
    from pydantic import BaseModel

logger: logging.Logger = logging.getLogger(__name__)


async def ainvoke_structured_llm(
    *,
    chat_model: BaseChatModel,
    output_type: type[BaseModel],
    system_prompt: str,
    user_content: str,
    timeblock_message: str = "LLM generated answer in {time}",
    max_retries: int = 0,
) -> tuple[Any, dict[str, Any]]:
    """Invoke *chat_model* for a structured *output_type* response.

    Shared by every agent's single-shot structured LLM call (adaptive
    query planning, assessment, judging): build the structured-output
    runnable, invoke it with a system/user message pair, and log token
    usage.

    If ``max_retries`` is greater than ``0`` and the response fails to
    parse (``raw_response["parsing_error"]`` is set), this makes a
    fresh call to *chat_model*, up to ``max_retries`` additional times,
    stopping as soon as an attempt succeeds. Each retry is a brand-new
    invocation -- nothing about a failed attempt is reused -- since
    re-generating is typically more reliable than patching malformed
    output.

    Args:
        chat_model: LangChain chat model to invoke.
        output_type: Pydantic model the response must conform to.
        system_prompt: System prompt for the call.
        user_content: User message content for the call.
        timeblock_message: Message template passed to :func:`timeblock`
            (e.g. ``"LLM generated AI risk assessment in {time}"``).
        max_retries: The number of additional attempts to make if a
            call's response fails to parse. ``0`` (default) means no
            retries -- a single attempt is made.

    Returns:
        A tuple ``(parsed, raw_response)`` where ``parsed`` is the
        structured output (``None`` if the LLM failed to produce it) and
        ``raw_response`` is the raw LangChain response dict (from the
        last attempt made), for callers that need to inspect
        ``parsing_error`` or log the raw content on failure.
    """
    structured_llm, messages, max_attempts = _prepare_structured_llm_call(
        chat_model, output_type, system_prompt, user_content, max_retries
    )
    raw_response: dict[str, Any] | None = None
    for attempt in range(1, max_attempts + 1):
        with timeblock(timeblock_message):
            raw_response = await structured_llm.ainvoke(messages)
        if _handle_attempt_result(raw_response, attempt=attempt, max_attempts=max_attempts):
            break
    assert raw_response is not None  # noqa: S101
    return raw_response["parsed"], raw_response


def invoke_structured_llm(
    *,
    chat_model: BaseChatModel,
    output_type: type[BaseModel],
    system_prompt: str,
    user_content: str,
    timeblock_message: str = "LLM generated answer in {time}",
    max_retries: int = 0,
) -> tuple[Any, dict[str, Any]]:
    """Invoke *chat_model* for a structured *output_type* response.

    Shared by every agent's single-shot structured LLM call (adaptive
    query planning, assessment, judging): build the structured-output
    runnable, invoke it with a system/user message pair, and log token
    usage.

    If ``max_retries`` is greater than ``0`` and the response fails to
    parse (``raw_response["parsing_error"]`` is set), this makes a
    fresh call to *chat_model*, up to ``max_retries`` additional times,
    stopping as soon as an attempt succeeds. Each retry is a brand-new
    invocation -- nothing about a failed attempt is reused -- since
    re-generating is typically more reliable than patching malformed
    output.

    Args:
        chat_model: LangChain chat model to invoke.
        output_type: Pydantic model the response must conform to.
        system_prompt: System prompt for the call.
        user_content: User message content for the call.
        timeblock_message: Message template passed to :func:`timeblock`
            (e.g. ``"LLM generated AI risk assessment in {time}"``).
        max_retries: The number of additional attempts to make if a
            call's response fails to parse. ``0`` (default) means no
            retries -- a single attempt is made.

    Returns:
        A tuple ``(parsed, raw_response)`` where ``parsed`` is the
        structured output (``None`` if the LLM failed to produce it) and
        ``raw_response`` is the raw LangChain response dict (from the
        last attempt made), for callers that need to inspect
        ``parsing_error`` or log the raw content on failure.
    """
    structured_llm, messages, max_attempts = _prepare_structured_llm_call(
        chat_model, output_type, system_prompt, user_content, max_retries
    )
    raw_response: dict[str, Any] | None = None
    for attempt in range(1, max_attempts + 1):
        with timeblock(timeblock_message):
            raw_response = structured_llm.invoke(messages)
        if _handle_attempt_result(raw_response, attempt=attempt, max_attempts=max_attempts):
            break
    assert raw_response is not None  # noqa: S101
    return raw_response["parsed"], raw_response


def _prepare_structured_llm_call(
    chat_model: BaseChatModel,
    output_type: type[BaseModel],
    system_prompt: str,
    user_content: str,
    max_retries: int,
) -> tuple[Runnable[LanguageModelInput, dict[str, Any]], list[SystemMessage | HumanMessage], int]:
    """Validate arguments and build the pieces shared by
    :func:`invoke_structured_llm` and :func:`ainvoke_structured_llm`.

    Args:
        chat_model: LangChain chat model to invoke.
        output_type: Pydantic model the response must conform to.
        system_prompt: System prompt for the call.
        user_content: User message content for the call.
        max_retries: The number of additional attempts allowed beyond
            the first; must be ``>= 0``.

    Returns:
        A ``(structured_llm, messages, max_attempts)`` tuple: the
        structured-output runnable to invoke, the system/user message
        pair to invoke it with, and the total number of attempts
        allowed (``max_retries + 1``).
    """
    validate_non_negative(max_retries, name="max_retries")
    structured_llm = structured_output_runnable(
        chat_model, output_type=output_type, include_raw=True
    )
    messages = _build_messages(system_prompt, user_content)
    return structured_llm, messages, max_retries + 1


def _handle_attempt_result(
    raw_response: dict[str, Any], *, attempt: int, max_attempts: int
) -> bool:
    """Log token usage for one attempt and report whether it succeeded.

    Args:
        raw_response: The raw LangChain response dict for this attempt.
        attempt: The 1-indexed number of this attempt.
        max_attempts: The total number of attempts allowed.

    Returns:
        ``True`` if the attempt produced valid structured output (i.e.
        ``raw_response["parsing_error"]`` is ``None``), in which case
        the retry loop should stop; ``False`` otherwise, in which case
        this has already logged a warning for the failed attempt.
    """
    log_token_usage(raw_response)
    if raw_response["parsing_error"] is None:
        return True
    logger.warning(
        "Attempt %d/%d failed to produce valid structured output: %s",
        attempt,
        max_attempts,
        raw_response["parsing_error"],
    )
    return False


def _build_messages(system_prompt: str, user_content: str) -> list[SystemMessage | HumanMessage]:
    return [SystemMessage(content=system_prompt), HumanMessage(content=user_content)]
