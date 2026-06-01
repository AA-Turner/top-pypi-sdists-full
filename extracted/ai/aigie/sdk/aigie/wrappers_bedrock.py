"""
AWS Bedrock integration for Aigie SDK

Automatically traces AWS Bedrock API calls
"""

import json
from typing import Any

from .cost_tracking import extract_and_calculate_cost


def wrap_bedrock(
    client: Any,
    name: str | None = None,
    metadata: dict[str, Any] | None = None,
    tags: list[str] | None = None,
) -> Any:
    """
    Wrap AWS Bedrock Runtime client for automatic tracing

    Args:
        client: Bedrock Runtime client instance
        name: Optional span name
        metadata: Additional metadata
        tags: Tags to apply

    Returns:
        Wrapped client with automatic tracing

    Example:
        >>> import boto3
        >>> from aigie.wrappers_bedrock import wrap_bedrock
        >>>
        >>> client = boto3.client('bedrock-runtime', region_name='us-east-1')
        >>> traced_client = wrap_bedrock(client)
        >>>
        >>> response = traced_client.invoke_model(
        ...     modelId='anthropic.claude-v2',
        ...     body=json.dumps({'prompt': 'Hello!'})
        ... )
    """
    from .client import get_aigie

    aigie = get_aigie()

    if not aigie or not aigie._enabled:
        return client

    # Store original methods
    original_invoke_model = getattr(client, "invoke_model", None)
    original_invoke_model_with_response_stream = getattr(
        client, "invoke_model_with_response_stream", None
    )

    # Wrap invoke_model
    if original_invoke_model:

        async def traced_invoke_model(**kwargs):
            """Traced version of invoke_model"""
            model_id = kwargs.get("modelId", "unknown")

            async def execute():
                import time

                start_time = time.time()

                try:
                    response = original_invoke_model(**kwargs)
                    duration = time.time() - start_time

                    # Parse response body
                    parsed_body = {}
                    try:
                        body_text = response["body"].read()
                        parsed_body = json.loads(body_text)
                    except Exception:
                        pass

                    # Extract metrics
                    metrics = _extract_bedrock_metrics(model_id, parsed_body)

                    # Calculate cost
                    cost_info = extract_and_calculate_cost(response, "bedrock")

                    # Update span with metrics
                    context = aigie.get_current_context()
                    if context and context.get("spanId"):
                        span_metadata = {
                            "model": model_id,
                            "provider": "bedrock",
                            "duration": duration,
                            **metrics,
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
                                "output": parsed_body,
                                "metadata": span_metadata,
                            },
                        )

                    return response

                except Exception as error:
                    raise error

            return await aigie.span(
                name or f"bedrock:{model_id}",
                execute,
                type="llm",
                input=_parse_bedrock_input(kwargs.get("body")),
                tags=[*(tags or []), "bedrock", "aws"],
                metadata={
                    **(metadata or {}),
                    "model": model_id,
                    "provider": "bedrock",
                    "contentType": kwargs.get("contentType", "application/json"),
                },
            )

        client.invoke_model = traced_invoke_model

    # Wrap invoke_model_with_response_stream
    if original_invoke_model_with_response_stream:

        async def traced_invoke_model_with_response_stream(**kwargs):
            """Traced version of invoke_model_with_response_stream"""
            import time
            import uuid

            model_id = kwargs.get("modelId", "unknown")
            context = aigie.get_current_context()
            span_id = str(uuid.uuid4())
            start_time = time.time()

            # Create span for streaming
            await aigie._send_span(
                {
                    "id": span_id,
                    "traceId": context.get("traceId"),
                    "parentSpanId": context.get("spanId"),
                    "name": name or f"bedrock:{model_id}",
                    "type": "llm",
                    "input": _parse_bedrock_input(kwargs.get("body")),
                    "status": "pending",
                    "tags": [*(tags or []), "bedrock", "aws", "streaming"],
                    "metadata": {
                        **(metadata or {}),
                        "model": model_id,
                        "provider": "bedrock",
                        "streaming": True,
                        "contentType": kwargs.get("contentType", "application/json"),
                    },
                    "startTime": time.time(),
                    "createdAt": time.time(),
                }
            )

            try:
                response = original_invoke_model_with_response_stream(**kwargs)

                # Wrap the response stream
                collected_output = ""
                token_count = 0

                async def wrapped_stream():
                    nonlocal collected_output, token_count

                    try:
                        for event in response.get("body", []):
                            chunk = event.get("chunk")
                            if chunk:
                                chunk_bytes = chunk.get("bytes")
                                if chunk_bytes:
                                    try:
                                        text = chunk_bytes.decode("utf-8")
                                        parsed = json.loads(text)

                                        if "completion" in parsed:
                                            collected_output += parsed["completion"]

                                        if "amazon-bedrock-invocationMetrics" in parsed:
                                            metrics = parsed["amazon-bedrock-invocationMetrics"]
                                            token_count = metrics.get("outputTokenCount", 0)
                                    except Exception:
                                        pass

                            yield event

                        # Update span on completion
                        duration = time.time() - start_time

                        # Build metadata with token info
                        span_metadata = {
                            "outputTokens": token_count,
                            "duration": duration,
                        }

                        # Calculate cost if token info is available
                        if token_count > 0:
                            # Create a mock response object for cost calculation
                            mock_response = {
                                "usage": {
                                    "output_tokens": token_count,
                                    "input_tokens": 0,  # Not available in streaming
                                },
                                "model": model_id,
                            }
                            cost_info = extract_and_calculate_cost(mock_response, "bedrock")
                            if cost_info:
                                span_metadata["cost"] = {
                                    "input_cost": float(cost_info.input_cost),
                                    "output_cost": float(cost_info.output_cost),
                                    "total_cost": float(cost_info.total_cost),
                                    "currency": cost_info.currency,
                                }

                        await aigie._update_span(
                            span_id,
                            {
                                "output": collected_output,
                                "status": "success",
                                "endTime": time.time(),
                                "durationNs": int(duration * 1_000_000_000),
                                "metadata": span_metadata,
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

                response["body"] = wrapped_stream()
                return response

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

        client.invoke_model_with_response_stream = traced_invoke_model_with_response_stream

    return client


def _parse_bedrock_input(body: Any) -> Any:
    """Parse Bedrock input from body"""
    if not body:
        return None

    try:
        if isinstance(body, str):
            return json.loads(body)
        if isinstance(body, bytes):
            return json.loads(body.decode("utf-8"))
        return body
    except Exception:
        return body


def _extract_bedrock_metrics(model_id: str, body: dict[str, Any]) -> dict[str, Any]:
    """Extract metrics from Bedrock response"""
    metrics = {}

    # Different models have different response formats
    if "completion" in body:
        # Anthropic Claude
        metrics["completion"] = body["completion"]
        metrics["stopReason"] = body.get("stop_reason")

    if "results" in body:
        # AI21 Jurassic
        metrics["results"] = body["results"]

    if "generations" in body:
        # Cohere
        metrics["generations"] = body["generations"]

    if "outputText" in body:
        # Amazon Titan
        metrics["outputText"] = body["outputText"]

    # Token usage (if available)
    if "amazon-bedrock-invocationMetrics" in body:
        invocation_metrics = body["amazon-bedrock-invocationMetrics"]
        metrics["inputTokens"] = invocation_metrics.get("inputTokenCount")
        metrics["outputTokens"] = invocation_metrics.get("outputTokenCount")
        metrics["totalTokens"] = invocation_metrics.get(
            "inputTokenCount", 0
        ) + invocation_metrics.get("outputTokenCount", 0)
        metrics["latency"] = invocation_metrics.get("invocationLatency")

    return metrics


def create_traced_bedrock(
    region_name: str,
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    name: str | None = None,
    metadata: dict[str, Any] | None = None,
    tags: list[str] | None = None,
) -> Any:
    """
    Create traced Bedrock client

    Args:
        region_name: AWS region
        aws_access_key_id: AWS access key ID
        aws_secret_access_key: AWS secret access key
        name: Optional span name
        metadata: Additional metadata
        tags: Tags to apply

    Returns:
        Traced Bedrock client

    Example:
        >>> from aigie.wrappers_bedrock import create_traced_bedrock
        >>>
        >>> client = create_traced_bedrock(region_name='us-east-1')
    """
    try:
        import boto3

        client = boto3.client(
            "bedrock-runtime",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        return wrap_bedrock(client, name=name, metadata=metadata, tags=tags)

    except ImportError:
        raise ImportError("boto3 not found. Install with: pip install boto3")
