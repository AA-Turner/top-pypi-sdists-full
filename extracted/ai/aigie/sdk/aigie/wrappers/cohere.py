"""
Cohere integration for Aigie SDK

Automatically traces Cohere API calls
"""

from collections.abc import AsyncGenerator
from typing import Any

from aigie.cost_tracking import extract_and_calculate_cost


def wrap_cohere(
    client: Any,
    name: str | None = None,
    metadata: dict[str, Any] | None = None,
    tags: list[str] | None = None,
) -> Any:
    """
    Wrap Cohere client for automatic tracing

    Args:
        client: Cohere client instance
        name: Optional span name
        metadata: Additional metadata
        tags: Tags to apply

    Returns:
        Wrapped client with automatic tracing

    Example:
        >>> import cohere
        >>> from aigie.wrappers import wrap_cohere
        >>>
        >>> co = cohere.Client(api_key='your-api-key')
        >>> traced_co = wrap_cohere(co)
        >>>
        >>> response = traced_co.generate(
        ...     model='command',
        ...     prompt='Hello!'
        ... )
    """
    from aigie.client import get_aigie

    aigie = get_aigie()

    if not aigie or not aigie._enabled:
        return client

    # Store original methods
    original_generate = getattr(client, "generate", None)
    original_chat = getattr(client, "chat", None)
    original_chat_stream = getattr(client, "chat_stream", None)
    original_embed = getattr(client, "embed", None)
    original_rerank = getattr(client, "rerank", None)

    # Wrap generate
    if original_generate:

        async def traced_generate(**kwargs):
            """Traced version of generate"""
            model = kwargs.get("model", "command")

            async def execute():
                import time

                start_time = time.time()

                try:
                    response = original_generate(**kwargs)
                    duration = time.time() - start_time

                    # Calculate cost
                    cost_info = extract_and_calculate_cost(response, "cohere")

                    # Update span with metrics
                    context = aigie.get_current_context()
                    if context and context.get("spanId"):
                        span_metadata = {
                            "model": model,
                            "provider": "cohere",
                            "duration": duration,
                            "generationId": response.id,
                            "finishReason": (
                                response.generations[0].finish_reason
                                if response.generations
                                else None
                            ),
                        }

                        # Add cost information if available
                        if cost_info:
                            span_metadata["cost"] = {
                                "input_cost": float(cost_info.input_cost),
                                "output_cost": float(cost_info.output_cost),
                                "total_cost": float(cost_info.total_cost),
                                "currency": cost_info.currency,
                            }

                        await aigie._update_span(
                            context["spanId"],
                            {
                                "output": (
                                    response.generations[0].text
                                    if response.generations
                                    else response
                                ),
                                "metadata": span_metadata,
                            },
                        )

                    return response

                except Exception as error:
                    raise error

            return await aigie.span(
                name or f"cohere:generate:{model}",
                execute,
                type="llm",
                input=kwargs.get("prompt"),
                tags=[*(tags or []), "cohere", "generate"],
                metadata={
                    **(metadata or {}),
                    "model": model,
                    "provider": "cohere",
                    "maxTokens": kwargs.get("max_tokens"),
                    "temperature": kwargs.get("temperature"),
                },
            )

        client.generate = traced_generate

    # Wrap chat
    if original_chat:

        async def traced_chat(**kwargs):
            """Traced version of chat"""
            model = kwargs.get("model", "command")

            async def execute():
                import time

                start_time = time.time()

                try:
                    response = original_chat(**kwargs)
                    duration = time.time() - start_time

                    # Calculate cost
                    cost_info = extract_and_calculate_cost(response, "cohere")

                    # Update span with metrics
                    context = aigie.get_current_context()
                    if context and context.get("spanId"):
                        span_metadata = {
                            "model": model,
                            "provider": "cohere",
                            "duration": duration,
                            "conversationId": response.conversation_id,
                            "generationId": response.generation_id,
                            "finishReason": response.finish_reason,
                            "citations": (len(response.citations) if response.citations else 0),
                            "documents": (len(response.documents) if response.documents else 0),
                        }

                        # Add cost information if available
                        if cost_info:
                            span_metadata["cost"] = {
                                "input_cost": float(cost_info.input_cost),
                                "output_cost": float(cost_info.output_cost),
                                "total_cost": float(cost_info.total_cost),
                                "currency": cost_info.currency,
                            }

                        await aigie._update_span(
                            context["spanId"],
                            {
                                "output": response.text or response,
                                "metadata": span_metadata,
                            },
                        )

                    return response

                except Exception as error:
                    raise error

            return await aigie.span(
                name or f"cohere:chat:{model}",
                execute,
                type="llm",
                input=kwargs.get("message") or kwargs.get("chat_history"),
                tags=[*(tags or []), "cohere", "chat"],
                metadata={
                    **(metadata or {}),
                    "model": model,
                    "provider": "cohere",
                    "conversationId": kwargs.get("conversation_id"),
                    "searchQueriesOnly": kwargs.get("search_queries_only"),
                },
            )

        client.chat = traced_chat

    # Wrap chat_stream
    if original_chat_stream:

        async def traced_chat_stream(**kwargs) -> AsyncGenerator:
            """Traced version of chat_stream"""
            import time
            import uuid

            model = kwargs.get("model", "command")
            context = aigie.get_current_context()
            span_id = str(uuid.uuid4())
            start_time = time.time()

            # Create span for streaming
            await aigie._send_span(
                {
                    "id": span_id,
                    "traceId": context.get("traceId"),
                    "parentSpanId": context.get("spanId"),
                    "name": name or f"cohere:chat:{model}",
                    "type": "llm",
                    "input": kwargs.get("message") or kwargs.get("chat_history"),
                    "status": "pending",
                    "tags": [*(tags or []), "cohere", "chat", "streaming"],
                    "metadata": {
                        **(metadata or {}),
                        "model": model,
                        "provider": "cohere",
                        "streaming": True,
                        "conversationId": kwargs.get("conversation_id"),
                    },
                    "startTime": time.time(),
                    "createdAt": time.time(),
                }
            )

            try:
                collected_text = ""
                conversation_id = None
                finish_reason = None

                for event in original_chat_stream(**kwargs):
                    if event.event_type == "text-generation":
                        collected_text += event.text
                    elif event.event_type == "stream-end":
                        if hasattr(event, "response"):
                            conversation_id = event.response.conversation_id
                        finish_reason = event.finish_reason

                    yield event

                # Update span on completion
                duration = time.time() - start_time
                await aigie._update_span(
                    span_id,
                    {
                        "output": collected_text,
                        "status": "success",
                        "endTime": time.time(),
                        "durationNs": int(duration * 1_000_000_000),
                        "metadata": {
                            "conversationId": conversation_id,
                            "finishReason": finish_reason,
                            "duration": duration,
                        },
                    },
                )

            except Exception as error:
                duration = time.time() - start_time
                await aigie._update_span(
                    span_id,
                    {
                        "status": "failed",
                        "errorMessage": str(error),
                        "endTime": time.time(),
                        "durationNs": int(duration * 1_000_000_000),
                    },
                )
                raise

        client.chat_stream = traced_chat_stream

    # Wrap embed
    if original_embed:

        async def traced_embed(**kwargs):
            """Traced version of embed"""
            model = kwargs.get("model", "embed-english-v3.0")

            async def execute():
                import time

                start_time = time.time()

                try:
                    response = original_embed(**kwargs)
                    duration = time.time() - start_time

                    # Calculate cost
                    cost_info = extract_and_calculate_cost(response, "cohere")

                    # Update span with metrics
                    context = aigie.get_current_context()
                    if context and context.get("spanId"):
                        span_metadata = {
                            "model": model,
                            "provider": "cohere",
                            "duration": duration,
                            "inputType": kwargs.get("input_type"),
                            "textCount": (
                                len(kwargs.get("texts", [])) if kwargs.get("texts") else 0
                            ),
                        }

                        # Add cost information if available
                        if cost_info:
                            span_metadata["cost"] = {
                                "input_cost": float(cost_info.input_cost),
                                "output_cost": float(cost_info.output_cost),
                                "total_cost": float(cost_info.total_cost),
                                "currency": cost_info.currency,
                            }

                        await aigie._update_span(
                            context["spanId"],
                            {
                                "output": {
                                    "embeddings": (
                                        len(response.embeddings) if response.embeddings else 0
                                    ),
                                    "dimensions": (
                                        len(response.embeddings[0]) if response.embeddings else 0
                                    ),
                                },
                                "metadata": span_metadata,
                            },
                        )

                    return response

                except Exception as error:
                    raise error

            return await aigie.span(
                name or f"cohere:embed:{model}",
                execute,
                type="embedding",
                input=kwargs.get("texts"),
                tags=[*(tags or []), "cohere", "embed"],
                metadata={
                    **(metadata or {}),
                    "model": model,
                    "provider": "cohere",
                    "inputType": kwargs.get("input_type"),
                    "truncate": kwargs.get("truncate"),
                },
            )

        client.embed = traced_embed

    # Wrap rerank
    if original_rerank:

        async def traced_rerank(**kwargs):
            """Traced version of rerank"""
            model = kwargs.get("model", "rerank-english-v3.0")

            async def execute():
                import time

                start_time = time.time()

                try:
                    response = original_rerank(**kwargs)
                    duration = time.time() - start_time

                    # Update span with metrics
                    context = aigie.get_current_context()
                    if context and context.get("spanId"):
                        await aigie._update_span(
                            context["spanId"],
                            {
                                "output": {
                                    "results": (len(response.results) if response.results else 0),
                                    "topResult": (
                                        response.results[0] if response.results else None
                                    ),
                                },
                                "metadata": {
                                    "model": model,
                                    "provider": "cohere",
                                    "duration": duration,
                                    "documentCount": (
                                        len(kwargs.get("documents", []))
                                        if kwargs.get("documents")
                                        else 0
                                    ),
                                    "topN": kwargs.get("top_n"),
                                },
                            },
                        )

                    return response

                except Exception as error:
                    raise error

            return await aigie.span(
                name or f"cohere:rerank:{model}",
                execute,
                type="chain",
                input={
                    "query": kwargs.get("query"),
                    "documentCount": (
                        len(kwargs.get("documents", [])) if kwargs.get("documents") else 0
                    ),
                },
                tags=[*(tags or []), "cohere", "rerank"],
                metadata={
                    **(metadata or {}),
                    "model": model,
                    "provider": "cohere",
                    "topN": kwargs.get("top_n"),
                    "returnDocuments": kwargs.get("return_documents"),
                },
            )

        client.rerank = traced_rerank

    return client


def create_traced_cohere(
    api_key: str,
    name: str | None = None,
    metadata: dict[str, Any] | None = None,
    tags: list[str] | None = None,
) -> Any:
    """
    Create traced Cohere client

    Args:
        api_key: Cohere API key
        name: Optional span name
        metadata: Additional metadata
        tags: Tags to apply

    Returns:
        Traced Cohere client

    Example:
        >>> from aigie.wrappers import create_traced_cohere
        >>>
        >>> client = create_traced_cohere(api_key='your-api-key')
    """
    try:
        import cohere

        client = cohere.Client(api_key=api_key)

        return wrap_cohere(client, name=name, metadata=metadata, tags=tags)

    except ImportError as err:
        raise ImportError("cohere not found. Install with: pip install cohere") from err
