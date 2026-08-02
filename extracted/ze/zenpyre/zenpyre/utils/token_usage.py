r"""Contain utilities to compute token usage."""

from __future__ import annotations

__all__ = [
    "format_token_usage",
    "get_token_usage",
    "log_token_usage",
]

import logging
from typing import Any

from coola.iterator import dfs_iterate, filter_by_type
from langchain_core.messages import AIMessage, UsageMetadata

logger: logging.Logger = logging.getLogger(__name__)


def format_token_usage(usage: UsageMetadata) -> str:
    """Format token usage as a human-readable string for terminal
    display.

    Args:
        usage: The token usage to format, as returned by
            :func:`~zenpyre.utils.tokens.get_invoke_token_usage` or
            :func:`~zenpyre.utils.tokens.get_batch_token_usage`.

    Returns:
        A single-line string summarizing input, output, and total
        token counts, suitable for printing to a terminal.

    Example:
        ```pycon
        >>> from langchain_core.messages import UsageMetadata
        >>> from zenpyre.utils.token_usage import format_token_usage
        >>> usage = UsageMetadata(input_tokens=1234, output_tokens=567, total_tokens=1801)
        >>> print(format_token_usage(usage))
        [tokens] in=1,234 | out=567 | total=1,801

        ```
    """
    input_tokens = f"{usage.get('input_tokens', 0):,}"
    output_tokens = f"{usage.get('output_tokens', 0):,}"
    total_tokens = f"{usage.get('total_tokens', 0):,}"
    return f"[tokens] in={input_tokens} | out={output_tokens} | total={total_tokens}"


def _sum_usage(messages: list[AIMessage]) -> UsageMetadata:
    """Sum token usage across a collection of AI messages.

    Messages without ``usage_metadata`` (e.g. the provider didn't
    report it) are silently skipped.

    ``total_tokens`` is summed independently from ``input_tokens`` and
    ``output_tokens`` rather than derived from them, since some
    providers may report additional token categories (e.g. cached or
    reasoning tokens) that make ``total_tokens`` differ from their
    simple sum.

    Args:
        messages: The AI messages to sum usage over.

    Returns:
        A ``UsageMetadata`` dict with ``input_tokens``, ``output_tokens``,
            and ``total_tokens`` summed across all given messages.
    """
    total_input = 0
    total_output = 0
    total_tokens = 0

    for msg in messages:
        usage = msg.usage_metadata
        if not usage:
            continue
        total_input += usage.get("input_tokens", 0)
        total_output += usage.get("output_tokens", 0)
        total_tokens += usage.get("total_tokens", 0)

    return UsageMetadata(
        input_tokens=total_input,
        output_tokens=total_output,
        total_tokens=total_tokens,
    )


def get_token_usage(result: Any) -> UsageMetadata:
    """Sum token usage across every AI message found anywhere within
    ``result``.

    Unlike :func:`get_invoke_token_usage` and :func:`get_batch_token_usage`,
    this function does not branch on the shape of ``result``. Instead it
    walks ``result`` depth-first (via ``coola``'s ``dfs_iterate``) and
    collects every ``AIMessage`` instance found, regardless of how deeply
    it is nested. This makes it a convenient, shape-agnostic entry point
    that works for a single ``BaseMessage``, the dict returned by
    ``agent.invoke(...)``, the list returned by ``agent.batch(...)``, or
    any other structure that contains ``AIMessage`` objects.

    If ``result`` contains no ``AIMessage`` instances (including cases
    where ``result`` is of an unrecognized type, e.g. an ``int`` or a
    plain ``str``), this function returns all-zero usage rather than
    raising an error.

    Args:
        result: Any object potentially containing ``AIMessage``
            instances, such as a ``BaseMessage``, the dict returned by
            ``agent.invoke(...)``, or the list returned by
            ``agent.batch(...)``.

    Returns:
        A ``UsageMetadata`` dict with token counts summed across every
            ``AIMessage`` found within ``result``.
    """
    ai_messages = list(filter_by_type(dfs_iterate(result), AIMessage))
    return _sum_usage(ai_messages)


def log_token_usage(result: Any, *, only_if_nonzero: bool = True) -> None:
    """Log the token usage for a single invocation or a batch of them.

    Args:
        result: The dict returned by ``agent.invoke(...)``, or the list
            of dicts returned by ``agent.batch(...)``.
        only_if_nonzero: If ``True`` (the default), nothing is logged
            when ``result`` has no ``total_tokens`` (i.e.
            ``total_tokens == 0``), which is typically the case when
            ``result`` contains no ``AIMessage`` with usage metadata.
            Set to ``False`` to always log, even when ``total_tokens``
            is zero.
    """
    usage = get_token_usage(result)
    if only_if_nonzero and not usage.get("total_tokens", 0):
        return
    logger.info(format_token_usage(usage))
