"""
chat() against a language-model server of your choosing: `server="openrouter"` with your own OpenRouter key, or the
address of a server of your own with the OpenAI chat completions API, given as `server`.

    result = sequence_ai.chat("qwen/qwen3-next-80b-a3b-instruct", messages, server="openrouter")  # $OPENROUTER_API_KEY
    result = sequence_ai.chat("my-model", messages, server="http://localhost:8000/v1")

In one sentence: chat(server=...) builds the request under the API's own names → POST `<address>/chat/completions`, the
key as its bearer when there is one → the reply's first choice becomes the same ChatResult the platform's chat returns,
and a streamed reply's chunks the same ChatStream - its reasoning blocks put together, its cost when the server reports
one, each failure one of the SDK's errors.

WHY the same result types: code that plans with chat() runs with the platform's models or with a server of its own,
and only `server` changes. WHY nothing of the platform is asked: no catalogue and no key of General Sequences - the
model is the server's own name for it, and what it costs is what the server reports.
"""
from __future__ import annotations

import json
import os
from collections.abc import Iterator
from typing import Any

from ..errors import AuthError, InvalidRequest, OutOfCredit, Unavailable
from .types import ChatResult, ChatStream, result_from_wire

PATH = "/chat/completions"


NAMED = {"openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY")}


_EXPLICIT_CACHE_VENDORS = frozenset({"anthropic", "qwen", "google"})
_BREAKPOINT = {"type": "ephemeral"}
_DETAIL_TEXT = ("text", "summary", "data")


def target(server: str, api_key: str | None) -> tuple[str, str | None]:
    """(the API's address, the key sent to it) for `server` - an address, or a name of NAMED - and the key chat() was
    given: a named server's key from its environment variable when none was given, and AuthError when there is none;
    an address's key only as given."""
    named = NAMED.get(server.strip().lower())
    if named is None:
        return server, api_key
    address, variable = named
    key = api_key or os.environ.get(variable)
    if not key:
        raise AuthError(f'chat(server="{server.strip().lower()}") needs your own key: set {variable}, or pass api_key=')
    return address, key


def is_named(server: str) -> bool:
    return server.strip().lower() in NAMED


def url(address: str) -> str:
    """The chat completions URL of a server whose API is at `address` (".../v1")."""
    return address.rstrip("/") + PATH


def headers(api_key: str | None) -> dict[str, str]:
    return {"Authorization": f"Bearer {api_key}"} if api_key else {}


def with_cache_breakpoint(messages: list[dict[str, Any]], model: str) -> list[dict[str, Any]]:
    """`messages` with the end of the last system message marked as a prompt-cache breakpoint, for a model that caches
    only behind one - so the system prompt and tools are read from the cache on later turns - unless the caller placed a
    breakpoint of their own. Copies what it changes."""
    vendor, _, name = model.partition("/")
    if vendor not in _EXPLICIT_CACHE_VENDORS or (vendor == "google" and name.startswith("gemini-2.5")):
        return messages
    if any(isinstance(m.get("content"), list) and any(isinstance(b, dict) and "cache_control" in b
                                                       for b in m["content"]) for m in messages):
        return messages
    at = max((i for i, m in enumerate(messages) if m.get("role") == "system"), default=None)
    if at is None:
        return messages
    message = dict(messages[at])
    content = message.get("content")
    if isinstance(content, str) and content:
        message["content"] = [{"type": "text", "text": content, "cache_control": dict(_BREAKPOINT)}]
    elif isinstance(content, list):
        blocks = [dict(b) if isinstance(b, dict) else b for b in content]
        last = max((k for k, b in enumerate(blocks) if isinstance(b, dict) and b.get("type") == "text"), default=None)
        if last is None:
            return messages
        blocks[last]["cache_control"] = dict(_BREAKPOINT)
        message["content"] = blocks
    else:
        return messages
    out = list(messages)
    out[at] = message
    return out


def _usage(usage: dict[str, Any] | None) -> dict[str, Any]:
    """The API's usage under the names ChatResult reads: cached, cache-write and reasoning tokens lifted out of their
    details."""
    usage = dict(usage or {})
    prompt = usage.get("prompt_tokens_details") or {}
    for name, value in (("cached_tokens", prompt.get("cached_tokens")),
                        ("cache_write_tokens", prompt.get("cache_write_tokens")),
                        ("reasoning_tokens", (usage.get("completion_tokens_details") or {}).get("reasoning_tokens"))):
        if value is not None:
            usage[name] = value
    return usage


def _cost(usage: dict[str, Any] | None) -> float:
    """What the server reports the turn cost (`usage.cost`), else 0."""
    try:
        return float((usage or {}).get("cost") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _functions(calls: list[Any] | None) -> list[dict[str, Any]] | None:
    """The tool calls a caller runs: those of type function, as the platform's chat hands them."""
    kept = [c for c in calls or [] if isinstance(c, dict) and c.get("type", "function") == "function"]
    return kept or None


def _message(message: dict[str, Any]) -> dict[str, Any]:
    """The reply's message, its reasoning under ChatResult's name (servers say reasoning_content or reasoning) and its
    tool calls those of type function."""
    message = dict(message or {})
    if "reasoning" not in message and message.get("reasoning_content"):
        message["reasoning"] = message.pop("reasoning_content")
    if "tool_calls" in message:
        message["tool_calls"] = _functions(message["tool_calls"])
    return message


def _retry_after(response: Any) -> float | None:
    try:
        return float(response.headers.get("retry-after"))
    except (TypeError, ValueError):
        return None


def _raise_for(response: Any, where: str) -> None:
    """The server's refusal as the SDK's errors, each with the server's own words: 401 and 403 AuthError, 402
    OutOfCredit (the key's credit is spent: stop, do not retry), 408, 429 and 5xx Unavailable with the wait the server
    asks for, another 4xx InvalidRequest."""
    if response.status_code < 400:
        return
    try:
        said = _said(response.json())
    except ValueError:
        said = None
    status = response.status_code
    message = f"{where} answered {status}: {said or response.text[:300]}"
    if status in (401, 403):
        raise AuthError(message, status=status)
    if status == 402:
        raise OutOfCredit(message, status=status)
    if status < 500 and status not in (408, 429):
        raise InvalidRequest(message, status=status)
    raise Unavailable(message, status=status, retry_after_s=_retry_after(response))


def _said(body: Any) -> str | None:
    """The words of an API error body: {"error": {"message": ...}} or {"error": "..."}."""
    error = body.get("error") if isinstance(body, dict) else None
    return error.get("message") if isinstance(error, dict) else error


def post(address: str, body: dict[str, Any], api_key: str | None, timeout_s: float | None) -> ChatResult:
    """One turn, not streamed: the ChatResult of the reply's first choice."""
    import httpx

    try:
        response = httpx.post(url(address), json=body, headers=headers(api_key), timeout=timeout_s or 120.0)
    except httpx.HTTPError as exc:
        raise Unavailable(f"no answer from {url(address)}: {exc}") from exc
    _raise_for(response, url(address))
    try:
        said = response.json()
    except ValueError:
        raise Unavailable(f"{url(address)} answered with no JSON: {response.text[:300]}") from None
    if not isinstance(said, dict) or not said.get("choices"):
        raise Unavailable(f"{url(address)} answered with no reply: {_said(said) or str(said)[:300]}")
    choice = said["choices"][0]
    usage = said.get("usage")
    return result_from_wire({"id": said.get("id", ""), "model": said.get("model", body["model"]),
                             "message": _message(choice.get("message") or {}),
                             "finish_reason": choice.get("finish_reason") or "", "usage": _usage(usage),
                             "cost_usd": _cost(usage), "logprobs": choice.get("logprobs")}, body["model"])


def stream(address: str, body: dict[str, Any], api_key: str | None, timeout_s: float | None) -> ChatStream:
    """One turn, streamed: a ChatStream fed the API's chunks as the platform's events - a chat.chunk for each piece of
    text or reasoning, then a chat.response with the whole message, tool calls and reasoning blocks put together from
    their pieces."""
    import httpx

    client = httpx.Client(timeout=timeout_s or 120.0)
    try:
        request = client.build_request("POST", url(address), json={**body, "stream": True}, headers=headers(api_key))
        response = client.send(request, stream=True)
    except httpx.HTTPError as exc:
        client.close()
        raise Unavailable(f"no answer from {url(address)}: {exc}") from exc
    if response.status_code >= 400:
        response.read()
        response.close()
        client.close()
        _raise_for(response, url(address))

    def close() -> None:
        response.close()
        client.close()

    return ChatStream(_events(_lines(response, url(address)), body["model"]), body["model"], close=close)


def _lines(response: Any, where: str) -> Iterator[str]:
    """The response's lines; a connection that fails mid-reply as Unavailable, the SDK's error rather than httpx's."""
    import httpx

    try:
        yield from response.iter_lines()
    except httpx.HTTPError as exc:
        raise Unavailable(f"{where} stopped mid-reply: {exc}") from exc


def merge_details(held: list[dict[str, Any]], blocks: list[Any]) -> None:
    """Fold streamed reasoning_details blocks into whole ones, as the platform's chat does: a block with the index of one
    already held extends it (its text, summary or data appended, a later signature, format or id set), a new index
    starts a block, and a block with no index stands alone."""
    for block in blocks or []:
        if not isinstance(block, dict):
            continue
        index = block.get("index")
        prev = next((b for b in held if index is not None and b.get("index") == index), None)
        if prev is None:
            held.append(dict(block))
            continue
        for key, value in block.items():
            if key in _DETAIL_TEXT and isinstance(value, str) and isinstance(prev.get(key), str):
                prev[key] += value
            elif value is not None:
                prev[key] = value


def _events(lines: Iterator[str], model: str) -> Iterator[Any]:
    """The API's server-sent chunks as the events ChatStream reads; an error the server sends mid-reply, or a reply that
    ends before it says why it stopped, as its error event."""
    text: list[str] = []
    thought: list[str] = []
    details: list[dict[str, Any]] = []
    tokens: list[Any] = []
    calls: dict[int, dict[str, Any]] = {}
    finish, usage, ident, named = "", {}, "", model
    for line in lines:
        if not line.startswith("data:"):
            continue
        data = line[len("data:"):].strip()
        if data == "[DONE]":
            break
        try:
            chunk = json.loads(data)
        except ValueError:
            continue
        if chunk.get("error"):
            error = chunk["error"] if isinstance(chunk["error"], dict) else {"message": str(chunk["error"])}
            yield {"object": "error", "error": {"status": error.get("code"), "message": error.get("message")}}
            return
        ident, named = chunk.get("id") or ident, chunk.get("model") or named
        usage = chunk.get("usage") or usage
        for choice in chunk.get("choices") or []:
            delta = choice.get("delta") or {}
            piece = delta.get("content") or ""
            reasoning = delta.get("reasoning") or delta.get("reasoning_content") or ""
            merge_details(details, delta.get("reasoning_details"))
            tokens.extend((choice.get("logprobs") or {}).get("content") or [])
            for call in delta.get("tool_calls") or []:
                held = calls.setdefault(int(call.get("index", 0)), {"id": "", "type": call.get("type") or "function",
                                                                     "function": {"name": "", "arguments": ""}})
                held["id"] = call.get("id") or held["id"]
                function = call.get("function") or {}
                held["function"]["name"] += function.get("name") or ""
                held["function"]["arguments"] += function.get("arguments") or ""
            finish = choice.get("finish_reason") or finish
            if piece or reasoning:
                text.append(piece)
                thought.append(reasoning)
                yield {"object": "chat.chunk", "delta": {"content": piece, "reasoning": reasoning}}
    if not finish:
        yield {"object": "error", "error": {"status": None, "message": "the reply ended before the server said it was "
                                                                       "done: ask again"}}
        return
    message: dict[str, Any] = {"role": "assistant", "content": "".join(text) or None}
    if "".join(thought):
        message["reasoning"] = "".join(thought)
    if details:
        message["reasoning_details"] = details
    kept = _functions([calls[i] for i in sorted(calls)])
    if kept:
        message["tool_calls"] = kept
    yield {"object": "chat.response", "id": ident, "model": named, "message": message, "finish_reason": finish,
           "usage": _usage(usage), "cost_usd": _cost(usage), "logprobs": {"content": tokens} if tokens else None}
