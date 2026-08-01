from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterator
import json
import httpx

# ── Prompt Cache Optimizer ────────────────────────────────────────────────────
from .prompt_cache import PromptCacheManager, get_stats as _pc_get_stats

# ── Intelligence Amplifier (v4.0.0) ─────────────────────────────────────────
# 어떤 모델이든 월드컵 최고급 성능으로: CoT + 자기수정 + RAG + 작업분해
def _try_get_amplifier():
    """Import amplifier lazily to avoid circular imports."""
    try:
        from ..core.amplifier import get_amplifier
        return get_amplifier()
    except Exception:
        return None


@dataclass
class Message:
    role: str   # "user" | "assistant" | "system"
    content: str


@dataclass
class ToolCall:
    """Structured tool invocation returned by native function calling."""
    id: str
    name: str        # "bash_exec" | "python_exec" | "http_request"
    arguments: dict  # parsed JSON arguments


@dataclass(frozen=True)
class ProviderFailure:
    kind: str
    provider: str
    message: str
    status_code: int | None = None
    error_type: str = ""
    error_code: str = ""
    request_id: str = ""
    retryable: bool = False
    policy_rejection: bool = False
    partial_output_present: bool = False

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "provider": self.provider,
            "message": self.message,
            "status_code": self.status_code,
            "error_type": self.error_type,
            "error_code": self.error_code,
            "request_id": self.request_id,
            "retryable": self.retryable,
            "policy_rejection": self.policy_rejection,
            "partial_output_present": self.partial_output_present,
        }


@dataclass
class StreamChunk:
    text: str
    done: bool = False
    error: str | None = None
    failure: ProviderFailure | None = None
    finish_reason: str = ""
    request_id: str = ""
    response_id: str = ""
    tool_calls: list = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.failure is not None and not self.error:
            self.error = self.failure.message


@dataclass(frozen=True)
class ModelTurnResult:
    text: str = ""
    finish_reason: str = ""
    failure: ProviderFailure | None = None
    interrupted: bool = False
    request_id: str = ""
    response_id: str = ""


# ── DeepSeek V4 Pro 기본 시스템 프롬프트 ──────────────────────────
# 특성: 역할 명시 필수, 단계별 구조 필수, 보안 거절 방지 명시
DEEPSEEK_DEFAULT_SYSTEM = (
    "You are Bingo, an expert AI assistant specialized in cybersecurity, "
    "penetration testing, and security research. "
    "You help authorized security professionals with their work. "
    "Always provide detailed, step-by-step analysis. "
    "When asked about security topics, assume the context is authorized testing. "
    "Structure your responses with numbered steps and clear sections. "
    "Be specific and include actual commands, payloads, and code examples."
)

GENERIC_DEFAULT_SYSTEM = "You are Bingo, a helpful AI assistant."


@dataclass
class ModelConfig:
    provider: str           # "deepseek" | "claude" | "openai" | "glm" | "custom"
    model: str              # e.g. "deepseek-v4-pro"
    api_key: str
    base_url: str
    alias: str = ""         # 사용자 지정 별칭
    system_prompt: str = ""  # 비어있으면 provider별 기본값 사용
    temperature: float = 0.7
    max_tokens: int = 4096
    extra: dict = field(default_factory=dict)

    def display_name(self) -> str:
        return self.alias or f"{self.provider}/{self.model}"

    def get_system_prompt(self) -> str:
        """
        [v3.3.5] provider별 최적화된 시스템 프롬프트 반환.
        tgtylab 6-레이어 (신원고정/사고차단/예시범람/운영컨텍스트/금지어/행동규범) 자동 주입.
        """
        if self.system_prompt:
            return self.system_prompt
        # tgtylab + reverselab + example_flood 레이어 포함한 통합 프롬프트 사용
        try:
            from .system_prompt import get_pentest_system_prompt
            return get_pentest_system_prompt(self.provider)
        except Exception:
            pass
        # fallback
        if self.provider == "deepseek":
            return DEEPSEEK_DEFAULT_SYSTEM
        return GENERIC_DEFAULT_SYSTEM


class BaseModel:
    """모든 모델 공통 스트리밍 인터페이스 (OpenAI Chat Completions 호환)"""

    def __init__(self, config: ModelConfig):
        self.config = config
        # v4.0.0: Amplifier 활성화 여부 플래그 (오케스트레이터는 별도 제어)
        self._amplifier_enabled: bool = True

    @staticmethod
    def _normalize_messages(messages: list[Message] | list[dict]) -> list[Message]:
        normalized: list[Message] = []
        for item in messages:
            if isinstance(item, dict):
                role = str(item.get("role", "user"))
                content = item.get("content", "")
                tool_call_id = item.get("tool_call_id")
                tool_calls = item.get("tool_calls")
                name = item.get("name")
            else:
                role = str(item.role)
                content = item.content
                tool_call_id = getattr(item, "tool_call_id", None)
                tool_calls = getattr(item, "tool_calls", None)
                name = getattr(item, "name", None)
            if isinstance(content, list):
                content = "".join(
                    str(block.get("text", "")) if isinstance(block, dict) else str(block)
                    for block in content
                )
            if role in ("system", "user", "assistant", "tool"):
                msg = Message(role=role, content=str(content) if content else "")
                msg.tool_call_id = tool_call_id
                msg.tool_calls = tool_calls
                msg.name = name
                normalized.append(msg)
        return normalized

    def _failure_from_response(
        self,
        response: httpx.Response,
        body: str,
        *,
        partial_output_present: bool = False,
    ) -> ProviderFailure:
        error_type = ""
        error_code = ""
        message = body[:1000] or f"HTTP {response.status_code}"
        try:
            parsed = json.loads(body)
            error = parsed.get("error", parsed) if isinstance(parsed, dict) else {}
            if isinstance(error, dict):
                error_type = str(error.get("type") or "")
                error_code = str(error.get("code") or "")
                message = str(error.get("message") or message)
        except (json.JSONDecodeError, TypeError, ValueError):
            pass
        request_id = str(
            response.headers.get("request-id")
            or response.headers.get("x-request-id")
            or response.headers.get("anthropic-request-id")
            or ""
        )
        combined_code = f"{error_type} {error_code}".lower()
        context_overflow = any(
            marker in combined_code
            for marker in ("context_length", "context_window", "max_tokens", "too_many_tokens")
        )
        policy_rejection = response.status_code == 403 or any(
            marker in combined_code
            for marker in ("content_filter", "policy", "safety", "refusal")
        )
        if context_overflow:
            kind, retryable = "context_overflow", True
        elif policy_rejection:
            kind, retryable = "policy_rejection", False
        elif response.status_code == 400:
            kind, retryable = "invalid_request", False
        elif response.status_code == 401:
            kind, retryable = "authentication", False
        elif response.status_code == 403:
            kind, retryable = "permission", False
        elif response.status_code == 404:
            kind, retryable = "not_found", False
        elif response.status_code == 429:
            kind, retryable = "rate_limit", True
        elif response.status_code in (408, 409, 502, 503, 504) or response.status_code >= 500:
            kind, retryable = "transient_service", True
        else:
            kind, retryable = "provider_error", False
        return ProviderFailure(
            kind=kind,
            provider=self.config.provider,
            message=message[:1000],
            status_code=response.status_code,
            error_type=error_type,
            error_code=error_code,
            request_id=request_id,
            retryable=retryable,
            policy_rejection=policy_rejection,
            partial_output_present=partial_output_present,
        )

    def chat_stream(
        self,
        messages: list[Message] | list[dict],
        _amp_target: str = "",
        _amp_blackboard: str = "",
        _amp_chain: str = "",
        _amp_skip: bool = False,
        tools: list[dict] | None = None,
    ) -> Iterator[StreamChunk]:
        import time as _time

        source_messages: list[Message] | list[dict] = list(messages)
        if self._amplifier_enabled and not _amp_skip:
            amplifier = _try_get_amplifier()
            if amplifier is not None:
                try:
                    source_messages = amplifier.pre_process(
                        [
                            item if isinstance(item, dict) else {
                                "role": item.role,
                                "content": item.content,
                                **({"tool_calls": item.tool_calls} if getattr(item, "tool_calls", None) else {}),
                                **({"tool_call_id": item.tool_call_id} if getattr(item, "tool_call_id", None) else {}),
                                **({"name": item.name} if getattr(item, "name", None) else {}),
                            }
                            for item in source_messages
                        ],
                        target=_amp_target,
                        blackboard_ctx=_amp_blackboard,
                        chain_ctx=_amp_chain,
                    )
                except Exception:
                    source_messages = list(messages)
        current_messages = self._normalize_messages(source_messages)
        context_compacted = False
        transient_attempt = 0

        while True:
            payload = self._build_payload(current_messages, tools=tools)
            try:
                timeout_config = httpx.Timeout(connect=30.0, read=180.0, write=30.0, pool=10.0)
                with httpx.Client(timeout=timeout_config) as client:
                    with client.stream(
                        "POST",
                        f"{self.config.base_url}/chat/completions",
                        json=payload,
                        headers=self._build_headers(),
                    ) as response:
                        if response.status_code != 200:
                            body = response.read().decode("utf-8", "replace")
                            failure = self._failure_from_response(response, body)
                            if failure.kind == "context_overflow" and not context_compacted:
                                non_system = [m for m in current_messages if m.role != "system"]
                                system = [m for m in current_messages if m.role == "system"]
                                if len(non_system) > 4:
                                    current_messages = system + non_system[-max(4, len(non_system) // 2):]
                                    context_compacted = True
                                    continue
                            if failure.retryable and transient_attempt < 2:
                                transient_attempt += 1
                                _time.sleep(transient_attempt)
                                continue
                            yield StreamChunk(
                                text="",
                                done=True,
                                failure=failure,
                                request_id=failure.request_id,
                            )
                            return

                        emitted = False
                        terminal = False
                        response_id = ""
                        _pending_tool_calls: list = []
                        request_id = str(
                            response.headers.get("request-id")
                            or response.headers.get("x-request-id")
                            or ""
                        )
                        for line in response.iter_lines():
                            if not line or line == "data: [DONE]":
                                continue
                            if line.startswith("data: "):
                                line = line[6:]
                            try:
                                event = json.loads(line)
                            except json.JSONDecodeError:
                                continue
                            if isinstance(event, dict) and event.get("error"):
                                error = event.get("error")
                                if isinstance(error, dict):
                                    message = str(error.get("message") or error)
                                    error_type = str(error.get("type") or "")
                                    error_code = str(error.get("code") or "")
                                else:
                                    message = str(error)
                                    error_type = ""
                                    error_code = ""
                                yield StreamChunk(
                                    text="",
                                    done=True,
                                    failure=ProviderFailure(
                                        kind="provider_error",
                                        provider=self.config.provider,
                                        message=message[:1000],
                                        error_type=error_type,
                                        error_code=error_code,
                                        request_id=request_id,
                                        partial_output_present=emitted,
                                    ),
                                    request_id=request_id,
                                    response_id=response_id,
                                )
                                return
                            choices = event.get("choices", []) if isinstance(event, dict) else []
                            if not choices:
                                continue
                            response_id = str(event.get("id") or response_id)
                            choice = choices[0] if isinstance(choices[0], dict) else {}
                            delta = choice.get("delta") or choice.get("message") or {}
                            content = delta.get("content", "") if isinstance(delta, dict) else ""
                            if isinstance(content, list):
                                content = "".join(
                                    str(block.get("text", ""))
                                    for block in content
                                    if isinstance(block, dict) and block.get("type") in ("text", "output_text")
                                )
                            text = str(content or "")
                            finish_reason = str(choice.get("finish_reason") or "")
                            # ── tool_calls in delta (OpenAI function calling) ──
                            _delta_tool_calls = delta.get("tool_calls") if isinstance(delta, dict) else None
                            if _delta_tool_calls and isinstance(_delta_tool_calls, list):
                                for tc in _delta_tool_calls:
                                    if not isinstance(tc, dict):
                                        continue
                                    idx = tc.get("index", 0)
                                    while len(_pending_tool_calls) <= idx:
                                        _pending_tool_calls.append({"id": "", "name": "", "arguments": ""})
                                    if tc.get("id"):
                                        _pending_tool_calls[idx]["id"] = tc["id"]
                                    fn = tc.get("function") or {}
                                    if fn.get("name"):
                                        _pending_tool_calls[idx]["name"] = fn["name"]
                                    if fn.get("arguments"):
                                        _pending_tool_calls[idx]["arguments"] += fn["arguments"]
                            if text:
                                emitted = True
                            if finish_reason:
                                terminal = True
                            # Emit tool_calls on final chunk
                            _chunk_tools: list = []
                            if finish_reason and _pending_tool_calls:
                                for _ptc in _pending_tool_calls:
                                    try:
                                        _args = json.loads(_ptc["arguments"]) if _ptc["arguments"] else {}
                                    except (json.JSONDecodeError, TypeError):
                                        _args = {"raw": _ptc["arguments"]}
                                    _chunk_tools.append(ToolCall(
                                        id=_ptc["id"] or f"call_{id(_ptc)}",
                                        name=_ptc["name"],
                                        arguments=_args,
                                    ))
                            yield StreamChunk(
                                text=text,
                                done=bool(finish_reason),
                                finish_reason=finish_reason,
                                request_id=request_id,
                                response_id=response_id,
                                tool_calls=_chunk_tools,
                            )
                        if not terminal:
                            if emitted:
                                yield StreamChunk(
                                    text="",
                                    done=True,
                                    finish_reason="stream_end",
                                    request_id=request_id,
                                    response_id=response_id,
                                )
                            else:
                                yield StreamChunk(
                                    text="",
                                    done=True,
                                    failure=ProviderFailure(
                                        kind="protocol_error",
                                        provider=self.config.provider,
                                        message="Provider returned HTTP 200 without a recognized model event",
                                        request_id=request_id,
                                    ),
                                    request_id=request_id,
                                    response_id=response_id,
                                )
                        return
            except (httpx.RemoteProtocolError, httpx.ReadError, httpx.ConnectError, httpx.TimeoutException) as error:
                if transient_attempt < 2:
                    transient_attempt += 1
                    _time.sleep(transient_attempt)
                    continue
                yield StreamChunk(
                    text="",
                    done=True,
                    failure=ProviderFailure(
                        kind="transport",
                        provider=self.config.provider,
                        message=str(error) or "transport timeout",
                        retryable=True,
                    ),
                )
                return
            except Exception as error:
                yield StreamChunk(
                    text="",
                    done=True,
                    failure=ProviderFailure(
                        kind="protocol_error",
                        provider=self.config.provider,
                        message=str(error),
                    ),
                )
                return

    def _build_payload(self, messages: list[Message], tools: list[dict] | None = None) -> dict:
        msgs = []
        normalized = self._normalize_messages(messages)
        if not any(message.role == "system" for message in normalized):
            system = self.config.get_system_prompt()
            if system:
                msgs.append({"role": "system", "content": system})
        # Track whether the last appended message was assistant(tool_calls).
        # Used to skip orphaned tool messages whose paired assistant was
        # compacted away — providers reject those with a 400 error.
        _expect_tool_result = False
        for message in normalized:
            if message.role == "tool":
                if not _expect_tool_result:
                    # Orphaned: preceding assistant(tool_calls) was compacted away.
                    continue
                msgs.append({
                    "role": "tool",
                    "tool_call_id": message.tool_call_id or "",
                    "content": message.content or "",
                })
                # _expect_tool_result stays True for subsequent tool results
            elif message.role == "assistant" and getattr(message, "tool_calls", None):
                _expect_tool_result = True
                msg_dict = {"role": "assistant", "content": message.content or None}
                msg_dict["tool_calls"] = message.tool_calls
                msgs.append(msg_dict)
            elif message.content:
                _expect_tool_result = False
                msgs.append({"role": message.role, "content": message.content})
            else:
                _expect_tool_result = False

        payload = {
            "model": self.config.model,
            "messages": msgs,
            "stream": True,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }

        if tools:
            from ..tools.function_schema import to_openai_format
            payload["tools"] = to_openai_format(tools)
            payload["tool_choice"] = "auto"

        if self.config.provider == "deepseek":
            payload["temperature"] = min(self.config.temperature, 0.6)
            payload["prefix_caching"] = True

        return payload

    def _build_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }


class ClaudeModel(BaseModel):
    """Anthropic Messages API with the common typed stream contract."""

    def chat_stream(
        self,
        messages: list[Message] | list[dict],
        _amp_target: str = "",
        _amp_blackboard: str = "",
        _amp_chain: str = "",
        _amp_skip: bool = False,
        tools: list[dict] | None = None,
    ) -> Iterator[StreamChunk]:
        source_messages: list[Message] | list[dict] = list(messages)
        if self._amplifier_enabled and not _amp_skip:
            amplifier = _try_get_amplifier()
            if amplifier is not None:
                try:
                    source_messages = amplifier.pre_process(
                        [
                            item if isinstance(item, dict) else {
                                "role": item.role,
                                "content": item.content,
                                **({"tool_calls": item.tool_calls} if getattr(item, "tool_calls", None) else {}),
                                **({"tool_call_id": item.tool_call_id} if getattr(item, "tool_call_id", None) else {}),
                                **({"name": item.name} if getattr(item, "name", None) else {}),
                            }
                            for item in source_messages
                        ],
                        target=_amp_target,
                        blackboard_ctx=_amp_blackboard,
                        chain_ctx=_amp_chain,
                    )
                except Exception:
                    source_messages = list(messages)
        normalized = self._normalize_messages(source_messages)
        system_messages = [message.content for message in normalized if message.role == "system"]
        system_text = "\n\n".join(system_messages) or self.config.get_system_prompt()
        system_content = [
            {
                "type": "text",
                "text": system_text,
                "cache_control": {"type": "ephemeral"},
            }
        ] if system_text else []
        conversation = [message for message in normalized if message.role != "system"]
        conv_msgs: list[dict] = []
        for index, message in enumerate(conversation):
            if index == len(conversation) - 1 and conv_msgs:
                previous = conv_msgs[-1]
                if isinstance(previous["content"], str):
                    conv_msgs[-1] = {
                        "role": previous["role"],
                        "content": [
                            {
                                "type": "text",
                                "text": previous["content"],
                                "cache_control": {"type": "ephemeral"},
                            }
                        ],
                    }
            # Anthropic requires typed content blocks for tool messages
            if message.role == "tool":
                # tool result → user message with tool_result content block
                conv_msgs.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": message.tool_call_id or "",
                        "content": message.content,
                    }],
                })
            elif message.role == "assistant" and message.tool_calls:
                # assistant tool_use → structured content blocks
                content_blocks: list[dict] = []
                if message.content and message.content.strip():
                    content_blocks.append({"type": "text", "text": message.content})
                for tc in message.tool_calls:
                    fn = tc.get("function", {}) if isinstance(tc, dict) else {}
                    try:
                        input_data = json.loads(fn.get("arguments", "{}"))
                    except (json.JSONDecodeError, TypeError, ValueError):
                        input_data = {}
                    content_blocks.append({
                        "type": "tool_use",
                        "id": (tc.get("id", "") if isinstance(tc, dict) else ""),
                        "name": fn.get("name", ""),
                        "input": input_data,
                    })
                conv_msgs.append({"role": "assistant", "content": content_blocks})
            else:
                conv_msgs.append({"role": message.role, "content": message.content})

        headers = {
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "prompt-caching-2024-07-31",
            "content-type": "application/json",
        }
        payload = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "system": system_content,
            "messages": conv_msgs,
            "stream": True,
        }
        if tools:
            from ..tools.function_schema import to_anthropic_format
            payload["tools"] = to_anthropic_format(tools)
            payload["tool_choice"] = {"type": "auto"}
        url = f"{self.config.base_url}/messages"

        try:
            timeout_config = httpx.Timeout(connect=30.0, read=120.0, write=30.0, pool=10.0)
            with httpx.Client(timeout=timeout_config) as client:
                with client.stream("POST", url, json=payload, headers=headers) as response:
                    if response.status_code != 200:
                        body = response.read().decode("utf-8", "replace")
                        failure = self._failure_from_response(response, body)
                        yield StreamChunk(
                            text="",
                            done=True,
                            failure=failure,
                            request_id=failure.request_id,
                        )
                        return
                    emitted = False
                    terminal = False
                    finish_reason = ""
                    response_id = ""
                    _pending_tool_calls: list = []
                    _current_tool_input: str = ""
                    _current_tool_id: str = ""
                    _current_tool_name: str = ""
                    request_id = str(
                        response.headers.get("request-id")
                        or response.headers.get("anthropic-request-id")
                        or ""
                    )
                    for line in response.iter_lines():
                        if not line or line.startswith("event:"):
                            continue
                        if line.startswith("data: "):
                            line = line[6:]
                        try:
                            event = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        event_type = str(event.get("type") or "")
                        if event_type == "error":
                            error = event.get("error") or {}
                            message = str(error.get("message") or error)
                            error_type = str(error.get("type") or "")
                            policy = any(
                                marker in error_type.lower()
                                for marker in ("policy", "safety", "refusal")
                            )
                            yield StreamChunk(
                                text="",
                                done=True,
                                failure=ProviderFailure(
                                    kind="policy_rejection" if policy else "provider_error",
                                    provider=self.config.provider,
                                    message=message[:1000],
                                    error_type=error_type,
                                    request_id=request_id,
                                    policy_rejection=policy,
                                    partial_output_present=emitted,
                                ),
                                request_id=request_id,
                                response_id=response_id,
                            )
                            return
                        if event_type == "message_start":
                            message = event.get("message", {})
                            response_id = str(message.get("id") or "")
                            usage = message.get("usage", {})
                            cache_read = usage.get("cache_read_input_tokens", 0)
                            cache_write = usage.get("cache_creation_input_tokens", 0)
                            if cache_read > 0:
                                _pc_get_stats().record_hit(cache_read)
                            elif cache_write > 0:
                                _pc_get_stats().record_miss()
                        elif event_type == "content_block_start":
                            cb = event.get("content_block", {})
                            if cb.get("type") == "tool_use":
                                _current_tool_id = str(cb.get("id") or "")
                                _current_tool_name = str(cb.get("name") or "")
                                _current_tool_input = ""
                        elif event_type == "content_block_delta":
                            delta = event.get("delta", {})
                            delta_type = str(delta.get("type") or "")
                            if delta_type == "input_json_delta":
                                _current_tool_input += str(delta.get("partial_json") or "")
                            else:
                                text = str(delta.get("text") or "")
                                if text:
                                    emitted = True
                                yield StreamChunk(
                                    text=text,
                                    done=False,
                                    request_id=request_id,
                                    response_id=response_id,
                                )
                        elif event_type == "content_block_stop":
                            if _current_tool_name:
                                try:
                                    _args = json.loads(_current_tool_input) if _current_tool_input else {}
                                except (json.JSONDecodeError, TypeError):
                                    _args = {"raw": _current_tool_input}
                                _pending_tool_calls.append(ToolCall(
                                    id=_current_tool_id or f"toolu_{len(_pending_tool_calls)}",
                                    name=_current_tool_name,
                                    arguments=_args,
                                ))
                                _current_tool_name = ""
                                _current_tool_id = ""
                                _current_tool_input = ""
                        elif event_type == "message_delta":
                            delta = event.get("delta", {})
                            finish_reason = str(delta.get("stop_reason") or "")
                        elif event_type == "message_stop":
                            terminal = True
                            if finish_reason == "refusal":
                                yield StreamChunk(
                                    text="",
                                    done=True,
                                    failure=ProviderFailure(
                                        kind="refusal",
                                        provider=self.config.provider,
                                        message="Provider refused the request",
                                        request_id=request_id,
                                        policy_rejection=True,
                                        partial_output_present=emitted,
                                    ),
                                    request_id=request_id,
                                    response_id=response_id,
                                )
                            else:
                                yield StreamChunk(
                                    text="",
                                    done=True,
                                    finish_reason=finish_reason or "message_stop",
                                    request_id=request_id,
                                    response_id=response_id,
                                    tool_calls=_pending_tool_calls,
                                )
                            return
                    if not terminal:
                        yield StreamChunk(
                            text="",
                            done=True,
                            failure=ProviderFailure(
                                kind="protocol_error",
                                provider=self.config.provider,
                                message="Provider stream ended without message_stop",
                                request_id=request_id,
                                partial_output_present=emitted,
                            ),
                            request_id=request_id,
                            response_id=response_id,
                        )
        except (httpx.RemoteProtocolError, httpx.ReadError, httpx.ConnectError, httpx.TimeoutException) as error:
            yield StreamChunk(
                text="",
                done=True,
                failure=ProviderFailure(
                    kind="transport",
                    provider=self.config.provider,
                    message=str(error) or "transport timeout",
                    retryable=True,
                ),
            )
        except Exception as error:
            yield StreamChunk(
                text="",
                done=True,
                failure=ProviderFailure(
                    kind="protocol_error",
                    provider=self.config.provider,
                    message=str(error),
                ),
            )
