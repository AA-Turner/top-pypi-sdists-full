from __future__ import annotations

from collections.abc import AsyncGenerator, Sequence
import json
import logging
import os
import types
from typing import TYPE_CHECKING, Any, ClassVar, NamedTuple

import httpx

logger = logging.getLogger(__name__)

from drydock.core.llm.backend.anthropic import AnthropicAdapter
from drydock.core.llm.backend.base import APIAdapter, PreparedRequest
from drydock.core.llm.backend.reasoning_adapter import ReasoningAdapter
from drydock.core.llm.backend.vertex import VertexAnthropicAdapter
from drydock.core.llm.exceptions import BackendErrorBuilder
from drydock.core.llm.message_utils import merge_consecutive_user_messages
from drydock.core.types import (
    AvailableTool,
    LLMChunk,
    LLMMessage,
    LLMUsage,
    Role,
    StrToolChoice,
)
from drydock.core.utils import async_generator_retry, async_retry

if TYPE_CHECKING:
    from drydock.core.config import ModelConfig, ProviderConfig


def _fix_invalid_json_escapes(s: str) -> str:
    """Fix invalid JSON escape sequences by doubling lone backslashes.

    Handles cases where vLLM produces JSON with unescaped backslashes
    in tool call arguments (e.g., regex patterns like \\d, \\w).
    Valid JSON escapes (\\", \\\\, \\/, \\b, \\f, \\n, \\r, \\t, \\uXXXX)
    are preserved.
    """
    result = []
    i = 0
    n = len(s)
    while i < n:
        if s[i] == '\\' and i + 1 < n:
            next_char = s[i + 1]
            if next_char in ('"', '\\', '/', 'b', 'f', 'n', 'r', 't'):
                # Valid JSON escape sequence - keep as-is
                result.append(s[i:i + 2])
                i += 2
            elif next_char == 'u':
                # Check for valid \uXXXX
                if i + 5 < n and all(
                    c in '0123456789abcdefABCDEF' for c in s[i + 2:i + 6]
                ):
                    result.append(s[i:i + 6])
                    i += 6
                else:
                    result.append('\\\\')
                    i += 1
            else:
                # Invalid escape like \d, \w, \s etc. - double the backslash
                result.append('\\\\')
                i += 1
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)


def _lenient_json_loads(s: str) -> dict[str, Any]:
    """Parse JSON with fallback for invalid escape sequences."""
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        if "escape" in str(e).lower():
            logger.warning("Fixing invalid JSON escape sequences in API response")
            fixed = _fix_invalid_json_escapes(s)
            return json.loads(fixed)
        raise


class OpenAIAdapter(APIAdapter):
    endpoint: ClassVar[str] = "/chat/completions"

    @staticmethod
    def _strip_control_chars(value: Any) -> Any:
        """Recursively strip C0 control chars (except \\t \\n \\r) from strings.

        vLLM's tool-call parser re-parses ``tool_calls.function.arguments``
        as JSON; an embedded NUL or ESC byte from a bash result that rode
        through the conversation history makes the second-level
        ``json.loads`` fail with "Invalid control character at line 1 col N"
        and the whole request 400s. Sanitize here so no path through the
        OpenAI adapter can emit raw control bytes — covers ``content``,
        ``arguments``, tool descriptions, and anything else recursively.
        """
        if isinstance(value, str):
            return "".join(c for c in value if c >= " " or c in "\n\r\t")
        if isinstance(value, dict):
            return {k: OpenAIAdapter._strip_control_chars(v) for k, v in value.items()}
        if isinstance(value, list):
            return [OpenAIAdapter._strip_control_chars(v) for v in value]
        return value

    def build_payload(
        self,
        model_name: str,
        converted_messages: list[dict[str, Any]],
        temperature: float,
        tools: list[AvailableTool] | None,
        max_tokens: int | None,
        tool_choice: StrToolChoice | AvailableTool | None,
        extra_sampling: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = {
            "model": model_name,
            "messages": converted_messages,
            "temperature": temperature,
        }

        if tools:
            payload["tools"] = [tool.model_dump(exclude_none=True) for tool in tools]
        if tool_choice:
            payload["tool_choice"] = (
                tool_choice
                if isinstance(tool_choice, str)
                else tool_choice.model_dump()
            )
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        # Loop-breaker sampling overrides (frequency_penalty, seed, etc).
        # These override temperature if provided (our anti-loop code bumps
        # temperature directly here too). vLLM ignores unknown keys.
        if extra_sampling:
            for k, v in extra_sampling.items():
                if v is not None:
                    payload[k] = v

        # 2026-06-06 PRD §5.3.5: grammar-constrained sampling.
        # When a `grammar` (GBNF string) is supplied via extra_sampling,
        # llama.cpp's sampler masks logits to physically prevent invalid
        # JSON during generation. Eliminates the "missing closing quote"
        # failure mode that 80 commits of client-side patches couldn't fix.
        # The grammar is generated from each tool's Pydantic args schema
        # via drydock.core.llm.grammar.pydantic_to_gbnf().
        # No-op when extra_sampling doesn't include "grammar".

        return payload

    def build_headers(self, api_key: str | None = None) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        return headers

    def _reasoning_to_api(
        self, msg_dict: dict[str, Any], field_name: str
    ) -> dict[str, Any]:
        if field_name != "reasoning_content" and "reasoning_content" in msg_dict:
            msg_dict[field_name] = msg_dict.pop("reasoning_content")
        return msg_dict

    def _reasoning_from_api(
        self, msg_dict: dict[str, Any], field_name: str
    ) -> dict[str, Any]:
        if field_name != "reasoning_content" and field_name in msg_dict:
            msg_dict["reasoning_content"] = msg_dict.pop(field_name)
        return msg_dict

    def prepare_request(  # noqa: PLR0913
        self,
        *,
        model_name: str,
        messages: Sequence[LLMMessage],
        temperature: float,
        tools: list[AvailableTool] | None,
        max_tokens: int | None,
        tool_choice: StrToolChoice | AvailableTool | None,
        enable_streaming: bool,
        provider: ProviderConfig,
        api_key: str | None = None,
        thinking: str = "off",
        extra_sampling: dict[str, Any] | None = None,
    ) -> PreparedRequest:
        merged_messages = merge_consecutive_user_messages(messages)
        field_name = provider.reasoning_field_name
        converted_messages = [
            self._reasoning_to_api(
                msg.model_dump(exclude_none=True, exclude={"message_id"}), field_name
            )
            for msg in merged_messages
        ]
        # 2026-06-05: vision support. read_file embeds image data with
        # [[DRYDOCK_IMG_BEGIN:<mime>]]<b64>[[DRYDOCK_IMG_END]] markers.
        # Transform those messages to OpenAI multimodal `content: [parts]`
        # format that llama.cpp (with --mmproj) and OpenAI both accept.
        # Skip transformation if the env var disables it.
        if os.environ.get("DRYDOCK_VISION_DISABLE", "0").strip() != "1":
            import re as _re_img
            _IMG_RE = _re_img.compile(
                r"\[\[DRYDOCK_IMG_BEGIN:([\w./+-]+)\]\](.*?)\[\[DRYDOCK_IMG_END\]\]",
                _re_img.DOTALL,
            )
            for md in converted_messages:
                c = md.get("content")
                if not isinstance(c, str) or "DRYDOCK_IMG_BEGIN" not in c:
                    continue
                parts: list[dict[str, Any]] = []
                last_end = 0
                for m in _IMG_RE.finditer(c):
                    text_before = c[last_end:m.start()].strip()
                    if text_before:
                        parts.append({"type": "text", "text": text_before})
                    mime = m.group(1)
                    b64 = m.group(2)
                    parts.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64}"},
                    })
                    last_end = m.end()
                text_after = c[last_end:].strip()
                if text_after:
                    parts.append({"type": "text", "text": text_after})
                if parts:
                    md["content"] = parts

        payload = self.build_payload(
            model_name, converted_messages, temperature, tools, max_tokens, tool_choice,
            extra_sampling=extra_sampling,
        )

        # Enable thinking for models that support it (Gemma 4)
        if thinking and thinking not in ("off", ""):
            payload["chat_template_kwargs"] = {"enable_thinking": True}
        # 2026-05-31: TRIED explicitly setting enable_thinking=False when
        # adaptive selector returns "off". REVERTED — observed in operator
        # session 2026-05-31 14:54: it caused the model to emit a flood of
        # malformed tool calls (bash({}) with empty args) for 5+ minutes,
        # presumably because Gemma 4's tool-call training was conditioned
        # on having a thinking block before the JSON. Leaving the key
        # absent (and accepting the template's default enable_thinking=True)
        # is safer for tool reliability; the latency cost is real but the
        # malformed-call thrash is worse.
        # NOTE: thinking budget (max thinking tokens) is a llamacpp SERVER startup
        # flag (--reasoning-budget N / LLAMA_ARG_THINK_BUDGET), not an API parameter.
        # The Gemma4 jinja template does not expose a thinking_budget variable, so
        # chat_template_kwargs.thinking_budget is silently ignored. Update
        # start_gemma4_llamacpp.sh to set --reasoning-budget on the next container start.

        if enable_streaming:
            payload["stream"] = True
            stream_options = {"include_usage": True}
            if provider.name == "mistral":
                stream_options["stream_tool_calls"] = True
            payload["stream_options"] = stream_options

        headers = self.build_headers(api_key)
        # Strip C0 control bytes from strings anywhere in the payload before
        # serialization. ensure_ascii=True escapes them in the OUTER JSON,
        # but vLLM re-parses tool_calls.function.arguments as JSON and a
        # raw \x00/\x1b ridden through from a bash result blows up the
        # second-level parse with the 400 the user hits in issue #13.
        payload = self._strip_control_chars(payload)
        body = json.dumps(payload, ensure_ascii=True).encode("utf-8")

        return PreparedRequest(self.endpoint, headers, body)

    def _parse_message(
        self, data: dict[str, Any], field_name: str
    ) -> LLMMessage | None:
        if data.get("choices"):
            choice = data["choices"][0]
            if "message" in choice:
                msg_dict = self._reasoning_from_api(choice["message"], field_name)
                return LLMMessage.model_validate(msg_dict)
            if "delta" in choice:
                msg_dict = self._reasoning_from_api(choice["delta"], field_name)
                return LLMMessage.model_validate(msg_dict)
            raise ValueError("Invalid response data: missing message or delta")

        if "message" in data:
            msg_dict = self._reasoning_from_api(data["message"], field_name)
            return LLMMessage.model_validate(msg_dict)
        if "delta" in data:
            msg_dict = self._reasoning_from_api(data["delta"], field_name)
            return LLMMessage.model_validate(msg_dict)

        return None

    def parse_response(
        self, data: dict[str, Any], provider: ProviderConfig
    ) -> LLMChunk:
        message = self._parse_message(data, provider.reasoning_field_name)
        if message is None:
            message = LLMMessage(role=Role.assistant, content="")

        usage_data = data.get("usage") or {}
        usage = LLMUsage(
            prompt_tokens=usage_data.get("prompt_tokens", 0),
            completion_tokens=usage_data.get("completion_tokens", 0),
        )

        return LLMChunk(message=message, usage=usage)


ADAPTERS: dict[str, APIAdapter] = {
    "openai": OpenAIAdapter(),
    "anthropic": AnthropicAdapter(),
    "vertex-anthropic": VertexAnthropicAdapter(),
    "reasoning": ReasoningAdapter(),
}


class GenericBackend:
    def __init__(
        self,
        *,
        client: httpx.AsyncClient | None = None,
        provider: ProviderConfig,
        timeout: float = 300.0,
    ) -> None:
        """Initialize the backend.

        Args:
            client: Optional httpx client to use. If not provided, one will be created.
        """
        self._client = client
        self._owns_client = client is None
        self._provider = provider
        # 2026-06-05: default 720s → 300s. Operator session: LLM backend
        # down, drydock waited 10+ min before giving up because read
        # timeout was 12 min. 300s still allows long completions (Gemma
        # 4 large generations finish in 60-120s) but bounds the
        # backend-down recovery time. Override via DRYDOCK_LLM_TIMEOUT.
        env_to = os.environ.get("DRYDOCK_LLM_TIMEOUT", "").strip()
        if env_to:
            try:
                timeout = float(env_to)
            except ValueError:
                pass
        self._timeout = timeout

    async def __aenter__(self) -> GenericBackend:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(
                    self._timeout, connect=10.0, write=15.0, pool=15.0
                ),
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
            )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        if self._owns_client and self._client:
            await self._client.aclose()
            self._client = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(
                    self._timeout, connect=10.0, write=15.0, pool=15.0
                ),
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
            )
            self._owns_client = True
        return self._client

    async def complete(
        self,
        *,
        model: ModelConfig,
        messages: Sequence[LLMMessage],
        temperature: float = 0.2,
        tools: list[AvailableTool] | None = None,
        max_tokens: int | None = None,
        tool_choice: StrToolChoice | AvailableTool | None = None,
        extra_headers: dict[str, str] | None = None,
        metadata: dict[str, str] | None = None,
        extra_sampling: dict[str, Any] | None = None,
    ) -> LLMChunk:
        api_key = (
            os.getenv(self._provider.api_key_env_var)
            if self._provider.api_key_env_var
            else None
        )

        api_style = getattr(self._provider, "api_style", "openai")
        adapter = ADAPTERS[api_style]

        req = adapter.prepare_request(
            model_name=model.name,
            messages=messages,
            temperature=temperature,
            tools=tools,
            max_tokens=max_tokens,
            tool_choice=tool_choice,
            enable_streaming=False,
            provider=self._provider,
            api_key=api_key,
            thinking=model.thinking,
            extra_sampling=extra_sampling,
        )

        headers = req.headers
        if extra_headers:
            headers.update(extra_headers)

        base = req.base_url or self._provider.api_base
        url = f"{base}{req.endpoint}"

        try:
            res_data, _ = await self._make_request(url, req.body, headers)
            return adapter.parse_response(res_data, self._provider)

        except httpx.HTTPStatusError as e:
            raise BackendErrorBuilder.build_http_error(
                provider=self._provider.name,
                endpoint=url,
                response=e.response,
                headers=e.response.headers,
                model=model.name,
                messages=messages,
                temperature=temperature,
                has_tools=bool(tools),
                tool_choice=tool_choice,
            ) from e
        except httpx.RequestError as e:
            raise BackendErrorBuilder.build_request_error(
                provider=self._provider.name,
                endpoint=url,
                error=e,
                model=model.name,
                messages=messages,
                temperature=temperature,
                has_tools=bool(tools),
                tool_choice=tool_choice,
            ) from e

    async def complete_streaming(
        self,
        *,
        model: ModelConfig,
        messages: Sequence[LLMMessage],
        temperature: float = 0.2,
        tools: list[AvailableTool] | None = None,
        max_tokens: int | None = None,
        tool_choice: StrToolChoice | AvailableTool | None = None,
        extra_headers: dict[str, str] | None = None,
        metadata: dict[str, str] | None = None,
    ) -> AsyncGenerator[LLMChunk, None]:
        api_key = (
            os.getenv(self._provider.api_key_env_var)
            if self._provider.api_key_env_var
            else None
        )

        api_style = getattr(self._provider, "api_style", "openai")
        adapter = ADAPTERS[api_style]

        req = adapter.prepare_request(
            model_name=model.name,
            messages=messages,
            temperature=temperature,
            tools=tools,
            max_tokens=max_tokens,
            tool_choice=tool_choice,
            enable_streaming=True,
            provider=self._provider,
            api_key=api_key,
            thinking=model.thinking,
        )

        headers = req.headers
        if extra_headers:
            headers.update(extra_headers)

        base = req.base_url or self._provider.api_base
        url = f"{base}{req.endpoint}"

        try:
            async for res_data in self._make_streaming_request(url, req.body, headers):
                yield adapter.parse_response(res_data, self._provider)

        except httpx.HTTPStatusError as e:
            raise BackendErrorBuilder.build_http_error(
                provider=self._provider.name,
                endpoint=url,
                response=e.response,
                headers=e.response.headers,
                model=model.name,
                messages=messages,
                temperature=temperature,
                has_tools=bool(tools),
                tool_choice=tool_choice,
            ) from e
        except httpx.RequestError as e:
            raise BackendErrorBuilder.build_request_error(
                provider=self._provider.name,
                endpoint=url,
                error=e,
                model=model.name,
                messages=messages,
                temperature=temperature,
                has_tools=bool(tools),
                tool_choice=tool_choice,
            ) from e

    class HTTPResponse(NamedTuple):
        data: dict[str, Any]
        headers: dict[str, str]

    @async_retry(tries=3)
    async def _make_request(
        self, url: str, data: bytes, headers: dict[str, str]
    ) -> HTTPResponse:
        client = self._get_client()
        response = await client.post(url, content=data, headers=headers)
        response.raise_for_status()

        response_headers = dict(response.headers.items())
        response_body = _lenient_json_loads(response.text)
        return self.HTTPResponse(response_body, response_headers)

    @async_generator_retry(tries=3)
    async def _make_streaming_request(
        self, url: str, data: bytes, headers: dict[str, str]
    ) -> AsyncGenerator[dict[str, Any]]:
        client = self._get_client()
        async with client.stream(
            method="POST", url=url, content=data, headers=headers
        ) as response:
            if not response.is_success:
                await response.aread()
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.strip() == "":
                    continue

                DELIM_CHAR = ":"
                if f"{DELIM_CHAR} " not in line:
                    raise ValueError(
                        f"Stream chunk improperly formatted. "
                        f"Expected `key{DELIM_CHAR} value`, received `{line}`"
                    )
                delim_index = line.find(DELIM_CHAR)
                key = line[0:delim_index]
                value = line[delim_index + 2 :]

                if key != "data":
                    # This might be the case with openrouter, so we just ignore it
                    continue
                if value == "[DONE]":
                    return
                yield _lenient_json_loads(value.strip())

    async def count_tokens(
        self,
        *,
        model: ModelConfig,
        messages: Sequence[LLMMessage],
        temperature: float = 0.0,
        tools: list[AvailableTool] | None = None,
        tool_choice: StrToolChoice | AvailableTool | None = None,
        extra_headers: dict[str, str] | None = None,
        metadata: dict[str, str] | None = None,
    ) -> int:
        probe_messages = list(messages)
        if not probe_messages or probe_messages[-1].role != Role.user:
            probe_messages.append(LLMMessage(role=Role.user, content=""))

        # 2026-06-02: chicken-and-egg fix. The original implementation
        # sent the FULL message history to the backend just to read
        # usage.prompt_tokens — but when the history exceeds the
        # backend's n_ctx (32768 on the 3090/romulus/Jetson; only
        # the local Docker llamacpp has 65536), the count call itself
        # gets rejected with 400 Bad Request "exceeds context size".
        # That blocks compact() from ever running because compact()
        # calls count_tokens to decide its strategy. Result: drydock
        # crashes with an unrecoverable BackendError on any session
        # that grows past 32K tokens on a small-context backend.
        # Observed in tbench probe v2937: 2 of 4 trials died here.
        #
        # Fix: try the real probe; on context-overflow specifically,
        # fall back to a local char-based heuristic (~4 chars/token,
        # then add 30% headroom). Returns a slightly-pessimistic count
        # which is the right direction — callers (compact, middleware)
        # use this to DECIDE whether to compact; overestimating means
        # we compact slightly earlier than needed, which is fine.
        try:
            result = await self.complete(
                model=model,
                messages=probe_messages,
                temperature=temperature,
                tools=tools,
                max_tokens=16,  # Minimal amount for openrouter with openai models
                tool_choice=tool_choice,
                extra_headers=extra_headers,
            )
            if result.usage is None:
                raise ValueError("Missing usage in non streaming completion")
            return result.usage.prompt_tokens
        except Exception as e:
            msg = str(e).lower()
            if (
                "exceeds the available context size" in msg
                or "exceed_context_size_error" in msg
                or "context length" in msg
                or "maximum context" in msg
            ):
                # Local fallback: 4 chars ≈ 1 token, +30% headroom for
                # tool-call JSON, chat-template overhead, etc.
                total_chars = sum(len(str(m.content or "")) for m in probe_messages)
                est_tokens = int((total_chars / 4) * 1.3)
                return est_tokens
            raise

    async def close(self) -> None:
        if self._owns_client and self._client:
            await self._client.aclose()
            self._client = None
