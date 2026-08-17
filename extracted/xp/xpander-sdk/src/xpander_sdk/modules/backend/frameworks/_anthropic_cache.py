"""Anthropic Claude wrapper that caches tool definitions + rolling message history.

agno's stock :class:`~agno.models.anthropic.claude.Claude` only marks the
``system`` block with ``cache_control`` (via ``cache_system_prompt``). The tool
definitions and the growing message history are re-billed at full input price on
every turn of an agentic run - the dominant cost on long tool-calling runs.

This subclass adds an ephemeral ``cache_control`` breakpoint on the last tool and
on the last content block of the last message, so the whole
system + tools + prior-conversation prefix is written to cache and read back on
the next turn. System caching stays on via the inherited ``cache_system_prompt``.
One rolling breakpoint on the last message is enough: Anthropic reads the longest
previously-cached prefix automatically, so each turn reads the prior turn's write.
Total breakpoints stay within Anthropic's limit of 4 (system + tools + 1 message).

The four invoke entrypoints (sync/async, buffered/stream) are overridden because
agno 2.5.14's ``Claude`` builds each request inline - there is no shared per-request
hook to attach to. Pinned to ``agno==2.5.14``; revisit the copied bodies on bump.
"""

from typing import Any, Dict, List, Optional, Type, Union
from collections.abc import AsyncIterator

from loguru import logger
from pydantic import BaseModel

from agno.models.anthropic import Claude
from agno.models.message import Message
from agno.models.response import ModelResponse
from agno.run.agent import RunOutput
from agno.utils.models.claude import format_messages

from xpander_sdk.modules.backend.frameworks._cache_split import (
    resolve_volatile,
    split_system_text,
)
from xpander_sdk.modules.backend.utils.prompt_budget import log_wire_budget

# Claude families that support prompt caching. Anthropic ignores an unknown
# cache_control gracefully, but gating keeps intent explicit and mirrors
# _bedrock_cache._supports_cache.
_CACHE_SUPPORTED_MODELS = ("claude-3", "claude-fable-5", "claude-opus-4", "claude-opus-5", "claude-sonnet-4", "claude-sonnet-5", "claude-haiku-4")

_CACHE_CONTROL = {"type": "ephemeral"}


def _inject_tools_cache(request_kwargs: Dict[str, Any]) -> None:
    """Mark the last tool definition cacheable, in place."""
    tools = request_kwargs.get("tools")
    if tools and isinstance(tools[-1], dict):
        tools[-1]["cache_control"] = dict(_CACHE_CONTROL)


def _inject_system_split(
    request_kwargs: Dict[str, Any], volatile: Optional[str]
) -> None:
    """Split the system block so the stable half survives a changing tail, in place.

    agno emits one text block carrying instructions + per-request context. With a
    single breakpoint at its end, a tail that differs per turn misses the whole
    prefix — and the message breakpoint downstream of it misses too.

    The tail keeps its own breakpoint so a single arun's tool-call turns still cache
    the full system block. That puts a split request at Anthropic's ceiling of four
    (tools, system-stable, system-tail, last message) — do not add a fifth.
    """
    system = request_kwargs.get("system")
    if not isinstance(system, list):
        return
    for position, block in enumerate(system):
        if not isinstance(block, dict):
            continue
        split = split_system_text(block.get("text"), volatile)
        if not split:
            continue
        stable, tail = split
        request_kwargs["system"] = (
            system[:position]
            + [
                {"type": "text", "text": stable, "cache_control": dict(_CACHE_CONTROL)},
                {**block, "text": tail},
            ]
            + system[position + 1 :]
        )
        return


def _inject_message_cache(chat_messages: List[Dict[str, Any]]) -> None:
    """Mark the last content block of the last message cacheable, in place.

    Anthropic requires ``cache_control`` on a content *block*, so a string
    ``content`` is promoted to a single text block first.
    """
    if not chat_messages:
        return
    last = chat_messages[-1]
    content = last.get("content")
    if isinstance(content, str):
        if content == "":
            return
        last["content"] = [{"type": "text", "text": content, "cache_control": dict(_CACHE_CONTROL)}]
    elif isinstance(content, list) and content and isinstance(content[-1], dict):
        content[-1]["cache_control"] = dict(_CACHE_CONTROL)


class CachingClaude(Claude):
    """``Claude`` that also caches tool definitions and the rolling message prefix."""

    # Per-request system tail, set by the agno builder once additional_context is
    # final. Splitting on it keeps the stable instructions cacheable across turns.
    xp_volatile_system: Optional[str] = None

    def _supports_cache(self) -> bool:
        model_id = (self.id or "").lower()
        return any(name in model_id for name in _CACHE_SUPPORTED_MODELS)

    def _parse_provider_response(self, response: Any, **kwargs: Any) -> ModelResponse:
        # Observability only: a max_tokens stop on a tool-use turn means the
        # tool-call JSON was truncated (empty-args dispatch upstream). The
        # truncated-call guard in the agno hook handles control flow.
        if getattr(response, "stop_reason", None) == "max_tokens":
            logger.warning(
                f"[{self.id}] response hit the max_tokens output cap "
                f"(max_tokens={getattr(self, 'max_tokens', None)}); tool-call "
                f"JSON in this turn may be truncated"
            )
        return super()._parse_provider_response(response, **kwargs)

    def _build_cached_request(
        self,
        messages: List[Message],
        tools: Optional[List[Dict[str, Any]]],
        response_format: Optional[Union[Dict, Type[BaseModel]]],
        compress_tool_results: bool,
    ) -> tuple:
        """Format messages + request kwargs, then attach cache breakpoints."""
        chat_messages, system_message = format_messages(
            messages,
            compress_tool_results=compress_tool_results,
            append_trailing_user_message=self.append_trailing_user_message,
            trailing_user_message_content=self.trailing_user_message_content,
        )
        request_kwargs = self._prepare_request_kwargs(
            system_message, tools=tools, response_format=response_format, messages=messages
        )
        if self._supports_cache():
            _inject_tools_cache(request_kwargs)
            _inject_system_split(request_kwargs, resolve_volatile(self.xp_volatile_system))
            _inject_message_cache(chat_messages)
        log_wire_budget(
            provider="anthropic",
            system_text="".join(
                b.get("text", "")
                for b in (request_kwargs.get("system") or [])
                if isinstance(b, dict) and "text" in b
            ),
            tools=request_kwargs.get("tools"),
        )
        return chat_messages, request_kwargs

    def invoke(
        self,
        messages: List[Message],
        assistant_message: Message,
        response_format: Optional[Union[Dict, Type[BaseModel]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        run_response: Optional[RunOutput] = None,
        compress_tool_results: bool = False,
    ) -> ModelResponse:
        try:
            chat_messages, request_kwargs = self._build_cached_request(
                messages, tools, response_format, compress_tool_results
            )
            if self._has_beta_features(response_format=response_format, tools=tools):
                assistant_message.metrics.start_timer()
                provider_response = self.get_client().beta.messages.create(
                    model=self.id, messages=chat_messages, **request_kwargs
                )
            else:
                assistant_message.metrics.start_timer()
                provider_response = self.get_client().messages.create(
                    model=self.id, messages=chat_messages, **request_kwargs
                )
            assistant_message.metrics.stop_timer()
            return self._parse_provider_response(provider_response, response_format=response_format)
        except Exception as e:
            self._handle_api_error(e)

    def invoke_stream(
        self,
        messages: List[Message],
        assistant_message: Message,
        response_format: Optional[Union[Dict, Type[BaseModel]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        run_response: Optional[RunOutput] = None,
        compress_tool_results: bool = False,
    ) -> Any:
        try:
            chat_messages, request_kwargs = self._build_cached_request(
                messages, tools, response_format, compress_tool_results
            )
            if self._has_beta_features(response_format=response_format, tools=tools):
                assistant_message.metrics.start_timer()
                with self.get_client().beta.messages.stream(
                    model=self.id, messages=chat_messages, **request_kwargs
                ) as stream:
                    for chunk in stream:
                        yield self._parse_provider_response_delta(chunk, response_format=response_format)
            else:
                assistant_message.metrics.start_timer()
                with self.get_client().messages.stream(
                    model=self.id, messages=chat_messages, **request_kwargs
                ) as stream:
                    for chunk in stream:
                        yield self._parse_provider_response_delta(chunk, response_format=response_format)
            assistant_message.metrics.stop_timer()
        except Exception as e:
            self._handle_api_error(e)

    async def ainvoke(
        self,
        messages: List[Message],
        assistant_message: Message,
        response_format: Optional[Union[Dict, Type[BaseModel]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        run_response: Optional[RunOutput] = None,
        compress_tool_results: bool = False,
    ) -> ModelResponse:
        try:
            chat_messages, request_kwargs = self._build_cached_request(
                messages, tools, response_format, compress_tool_results
            )
            if self._has_beta_features(response_format=response_format, tools=tools):
                assistant_message.metrics.start_timer()
                provider_response = await self.get_async_client().beta.messages.create(
                    model=self.id, messages=chat_messages, **request_kwargs
                )
            else:
                assistant_message.metrics.start_timer()
                provider_response = await self.get_async_client().messages.create(
                    model=self.id, messages=chat_messages, **request_kwargs
                )
            assistant_message.metrics.stop_timer()
            return self._parse_provider_response(provider_response, response_format=response_format)
        except Exception as e:
            self._handle_api_error(e)

    async def ainvoke_stream(
        self,
        messages: List[Message],
        assistant_message: Message,
        response_format: Optional[Union[Dict, Type[BaseModel]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        run_response: Optional[RunOutput] = None,
        compress_tool_results: bool = False,
    ) -> AsyncIterator[ModelResponse]:
        try:
            chat_messages, request_kwargs = self._build_cached_request(
                messages, tools, response_format, compress_tool_results
            )
            if self._has_beta_features(response_format=response_format, tools=tools):
                assistant_message.metrics.start_timer()
                async with self.get_async_client().beta.messages.stream(
                    model=self.id, messages=chat_messages, **request_kwargs
                ) as stream:
                    async for chunk in stream:
                        yield self._parse_provider_response_delta(chunk, response_format=response_format)
            else:
                assistant_message.metrics.start_timer()
                async with self.get_async_client().messages.stream(
                    model=self.id, messages=chat_messages, **request_kwargs
                ) as stream:
                    async for chunk in stream:
                        yield self._parse_provider_response_delta(chunk, response_format=response_format)
            assistant_message.metrics.stop_timer()
        except Exception as e:
            self._handle_api_error(e)
