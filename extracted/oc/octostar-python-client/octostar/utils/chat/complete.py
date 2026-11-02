import json
from typing import AsyncIterator, Literal, Optional, TypedDict

import httpx

from ...client import Client, get_default_client
from ..commons import network_retry_strategy
from ..exceptions import ApiConnectionError


class CompletionMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


class CompletionUsage(TypedDict):
    input_tokens: int
    output_tokens: int
    total_tokens: int


class Completion(TypedDict):
    content: str
    model_name: str
    finish_reason: Optional[str]
    usage: Optional[CompletionUsage]


def _prepare_complete_request(
    client,
    messages,
    model_name,
    temperature,
    max_output_tokens,
    enable_thinking,
    stream,
):
    body = {"messages": messages, "enable_thinking": enable_thinking, "stream": stream}
    if model_name is not None:
        body["model_name"] = model_name
    if temperature is not None:
        body["temperature"] = temperature
    if max_output_tokens is not None:
        body["max_output_tokens"] = max_output_tokens
    return {
        "url": f"{client.get_base_url_v1()}/api/v2/ai/llm/complete",
        "headers": {
            "Authorization": f"Bearer {client.token}",
            "x-ontology": client.ontology,
        },
        "json": body,
    }


def sync(
    messages: list[CompletionMessage],
    model_name: Optional[str] = None,
    temperature: Optional[float] = None,
    max_output_tokens: Optional[int] = None,
    enable_thinking: bool = False,
    timeout: Optional[float] = 300.0,
    retries: int = 2,
    client: Optional[Client] = None,
) -> Completion:
    """
    # Generate the next assistant message for a conversation.

    One LLM call: no tools and no system prompt besides the ones in `messages`.

    ## Arguments
    - `messages`: The conversation, oldest first, as `{"role", "content"}` dicts.
    - `model_name`: The model to run. If None, the platform's default model is used.
    - `temperature`: Sampling temperature. If None, the model's default.
    - `max_output_tokens`: Cap on generated tokens. If None, the model's platform default.
    - `enable_thinking`: Let local LLM deployments reason before answering.
    - `timeout`: Seconds to wait for the reply.
    - `retries`: Attempts on network errors; errors the API returns are not retried.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The reply: `content`, `model_name`, `finish_reason` and `usage`.

    ## Raises
    - `ApiConnectionError`: If the query was unsuccessful.
    """
    if not client:
        client = get_default_client()
    request = _prepare_complete_request(
        client,
        messages,
        model_name,
        temperature,
        max_output_tokens,
        enable_thinking,
        False,
    )
    response = None
    try:
        for attempt in network_retry_strategy(retries=retries):
            with attempt:
                with httpx.Client() as httpx_client:
                    response = httpx_client.post(**request, timeout=timeout)
                    response.raise_for_status()
        return response.json()  # pyright: ignore[reportOptionalMemberAccess]
    except Exception:
        raise ApiConnectionError("complete", response, client)


async def asyncio(
    messages: list[CompletionMessage],
    model_name: Optional[str] = None,
    temperature: Optional[float] = None,
    max_output_tokens: Optional[int] = None,
    enable_thinking: bool = False,
    timeout: Optional[float] = 300.0,
    retries: int = 2,
    client: Optional[Client] = None,
) -> Completion:
    """
    # Generate the next assistant message for a conversation, asynchronously.

    See `sync` for the arguments, return value and errors.
    """
    if not client:
        client = get_default_client()
    request = _prepare_complete_request(
        client,
        messages,
        model_name,
        temperature,
        max_output_tokens,
        enable_thinking,
        False,
    )
    response = None
    try:
        for attempt in network_retry_strategy(retries=retries):
            with attempt:
                async with httpx.AsyncClient() as httpx_client:
                    response = await httpx_client.post(**request, timeout=timeout)
                    response.raise_for_status()
        return response.json()  # pyright: ignore[reportOptionalMemberAccess]
    except Exception:
        raise ApiConnectionError("complete", response, client)


async def streaming(
    messages: list[CompletionMessage],
    model_name: Optional[str] = None,
    temperature: Optional[float] = None,
    max_output_tokens: Optional[int] = None,
    enable_thinking: bool = False,
    timeout: Optional[float] = 300.0,
    client: Optional[Client] = None,
) -> AsyncIterator[str]:
    """
    # Stream the next assistant message for a conversation.

    See `sync` for the arguments.

    ## Returns
    An async iterator over the text as it is generated.

    ## Raises
    - `ApiConnectionError`: If the request fails, or the stream reports an error
      or ends before the reply is complete.
    """
    if not client:
        client = get_default_client()
    request = _prepare_complete_request(
        client,
        messages,
        model_name,
        temperature,
        max_output_tokens,
        enable_thinking,
        True,
    )
    try:
        async with httpx.AsyncClient() as httpx_client:
            async with httpx_client.stream(
                "POST", **request, timeout=timeout
            ) as response:
                if response.status_code != 200:
                    await response.aread()
                    raise ConnectionError(
                        f"complete streaming: HTTP {response.status_code}: {response.text[:500]}"
                    )
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    event = json.loads(line)
                    if event.get("type") == "text":
                        yield event["content"]
                    elif event.get("type") == "done":
                        return
                    elif event.get("type") == "error":
                        raise ConnectionError(
                            f"complete streaming: {event.get('detail')}"
                        )
                raise ConnectionError(
                    "complete streaming: the stream ended without a done event"
                )
    except (ConnectionError, httpx.HTTPError, ValueError) as e:
        raise ApiConnectionError("complete streaming", None, client) from e
