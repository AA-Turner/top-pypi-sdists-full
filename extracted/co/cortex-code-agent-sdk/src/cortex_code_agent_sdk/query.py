"""High-level query() function for one-shot prompts and streamed responses.

Usage:
    async for message in query(prompt="Say hello"):
        ...
"""

from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterable, AsyncIterator
from typing import Any

from ._internal.transport import Transport
from .client import CortexCodeSDKClient
from .types import CortexCodeAgentOptions, Message, ResultMessage


async def query(
    *,
    prompt: str | AsyncIterable[dict[str, Any]],
    options: CortexCodeAgentOptions | None = None,
    transport: Transport | None = None,
) -> AsyncIterator[Message]:
    """Send a prompt to Cortex Code and stream back events.

    This is the primary one-shot API for sending a prompt and streaming the
    resulting messages.

    Args:
        prompt: The user prompt to send. Can be a string or an async iterable
                of dicts for streaming input.
        options: Configuration options. If not provided, uses defaults.
        transport: Optional custom transport. If not provided, uses
                   SubprocessCLITransport.

    Yields:
        Message objects (AssistantMessage, UserMessage, ResultMessage,
        SystemMessage, or StreamEvent).

    Example:
        async for message in query(prompt="Review utils.py for bugs"):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if hasattr(block, "text"):
                        print(block.text)
            elif isinstance(message, ResultMessage):
                print(f"Done: {message.subtype}")
    """
    if options is None:
        options = CortexCodeAgentOptions()

    client = CortexCodeSDKClient(options=options, transport=transport)
    close_input_task: asyncio.Task[None] | None = None
    try:
        await client.connect()
        await client.query(prompt)
        internal_query = client._query
        if internal_query is not None:
            close_input_task = asyncio.create_task(
                internal_query.wait_for_result_and_end_input()
            )
        async for message in client.receive_response():
            yield message
    finally:
        if close_input_task is not None:
            if close_input_task.done():
                await close_input_task
            else:
                close_input_task.cancel()
                try:
                    await close_input_task
                except asyncio.CancelledError:
                    pass
        await client.disconnect()
