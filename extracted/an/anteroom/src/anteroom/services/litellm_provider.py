"""LiteLLM provider for multi-provider streaming chat completions."""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
from typing import Any, AsyncGenerator

from ..config import AIConfig
from .ai_service import CompletionResult, classify_completion_error
from .egress_allowlist import check_egress_allowed
from .error_sanitizer import sanitize_provider_error
from .provider_messages import strip_local_message_fields
from .provider_validation import (
    ProviderRequestError,
    _is_anthropic_or_bedrock_route,
    validate_first_message_user,
    validate_not_bedrock_tools_without_confirmation,
)
from .token_provider import TokenProvider, TokenProviderError

logger = logging.getLogger(__name__)

try:
    import litellm
    from litellm.exceptions import APIConnectionError as LiteLLMConnectionError
    from litellm.exceptions import AuthenticationError as LiteLLMAuthError
    from litellm.exceptions import BadGatewayError as LiteLLMBadGatewayError
    from litellm.exceptions import BadRequestError as LiteLLMBadRequestError
    from litellm.exceptions import ContextWindowExceededError as LiteLLMContextError
    from litellm.exceptions import InternalServerError as LiteLLMInternalServerError
    from litellm.exceptions import RateLimitError as LiteLLMRateLimitError
    from litellm.exceptions import ServiceUnavailableError as LiteLLMServiceUnavailableError
    from litellm.exceptions import Timeout as LiteLLMTimeoutError

    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False


# Transient exception classes that should ride the retry path (#1343).
# Must be declared AFTER the imports above — any bump to the typed
# catch-all (`except Exception`) that runs after this tuple will
# otherwise silently regress retries. Mirrors the native openai path in
# ai_service.py:658 (`APITimeoutError, APIConnectionError`).
_LITELLM_TRANSIENT: tuple[type[BaseException], ...] = (
    (
        LiteLLMConnectionError,
        LiteLLMTimeoutError,
        LiteLLMServiceUnavailableError,
        LiteLLMInternalServerError,
        LiteLLMBadGatewayError,
    )
    if HAS_LITELLM
    else ()
)


class LiteLLMService:
    """LiteLLM wrapper matching the AIService interface.

    Uses litellm.acompletion() for streaming, supporting 100+ providers
    via model name prefixes (e.g. openrouter/openai/gpt-4o).
    """

    def __init__(self, config: AIConfig, token_provider: TokenProvider | None = None) -> None:
        if not HAS_LITELLM:
            raise ImportError("The litellm package is not installed. Install it with: pip install anteroom[providers]")
        self.config = config
        self._token_provider = token_provider
        self._cached_models: list[str] | None = None
        self._validate_egress()

    def _validate_egress(self) -> None:
        if self.config.base_url and not check_egress_allowed(
            self.config.base_url,
            self.config.allowed_domains,
            block_localhost=self.config.block_localhost_api,
        ):
            raise ValueError("Egress blocked: the configured base_url is not permitted by the egress allowlist.")

    def _resolve_api_key(self) -> str:
        if self._token_provider:
            return self._token_provider.get_token()
        return self.config.api_key

    def _try_refresh_token(self) -> bool:
        if not self._token_provider:
            return False
        try:
            self._token_provider.refresh()
            return True
        except TokenProviderError:
            logger.exception("Token refresh failed")
            return False

    def _validate_request(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> None:
        """Pre-flight validation for the LiteLLM provider.

        Only applies provider-specific rules when the model route targets
        Anthropic or Bedrock (other providers accept flexible message ordering).
        """
        model = self.config.model
        if _is_anthropic_or_bedrock_route(model):
            validate_first_message_user(
                messages,
                allow_leading_system=True,
                provider="litellm",
                model=model,
            )
        validate_not_bedrock_tools_without_confirmation(
            model,
            tools,
            confirmed=self.config.litellm_bedrock_tools_confirmed,
            provider="litellm",
        )

    def _build_kwargs(
        self,
        messages: list[dict[str, Any]],
        *,
        stream: bool = False,
        tools: list[dict[str, Any]] | None = None,
        max_completion_tokens: int | None = None,
    ) -> dict[str, Any]:
        """Build kwargs dict for litellm.acompletion()."""
        kwargs: dict[str, Any] = {
            "model": self.config.model,
            "messages": strip_local_message_fields(messages),
            "stream": stream,
            "timeout": float(self.config.request_timeout),
        }
        # Only pass api_key when explicitly configured. Omitting it lets
        # LiteLLM fall through to provider-native auth (e.g. boto3 for
        # Bedrock, GCP ADC for Vertex AI).
        api_key = self._resolve_api_key()
        if api_key:
            kwargs["api_key"] = api_key
        if self.config.base_url:
            kwargs["api_base"] = self.config.base_url
        if tools:
            kwargs["tools"] = tools
        if max_completion_tokens is not None:
            kwargs["max_completion_tokens"] = max_completion_tokens
        if self.config.temperature is not None:
            kwargs["temperature"] = self.config.temperature
        if self.config.top_p is not None:
            kwargs["top_p"] = self.config.top_p
        if self.config.seed is not None:
            kwargs["seed"] = self.config.seed
        if stream:
            kwargs["stream_options"] = {"include_usage": True}
        # OpenRouter-specific headers
        if "openrouter" in self.config.model.lower() or "openrouter" in (self.config.base_url or "").lower():
            kwargs["extra_headers"] = {
                "HTTP-Referer": "https://anteroom.ai",
                "X-Title": "Anteroom",
            }
        return kwargs

    def _estimate_fallback_usage(
        self,
        full_messages: list[dict[str, Any]],
        response_content: str,
        tool_schemas: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any] | None:
        """Estimate usage when the API omits streaming usage."""
        try:
            from .token_estimator import estimate_usage

            return estimate_usage(
                full_messages,
                response_content,
                self.config.model,
                tool_schemas=tool_schemas,
            )
        except Exception:
            logger.debug("Token estimation fallback failed", exc_info=True)
            return None

    async def stream_chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        cancel_event: asyncio.Event | None = None,
        extra_system_prompt: str | None = None,
        *,
        _retry_on_auth: bool = True,
    ) -> AsyncGenerator[dict[str, Any], None]:
        system_content = self.config.system_prompt
        if extra_system_prompt:
            system_content = extra_system_prompt + "\n\n" + system_content
        system_msg = {"role": "system", "content": system_content}
        full_messages = [system_msg] + messages

        try:
            self._validate_request(full_messages, tools)
        except ProviderRequestError as exc:
            yield exc.to_error_event()
            return

        max_attempts = max(1, self.config.retry_max_attempts + 1)

        for attempt in range(max_attempts):
            if cancel_event and cancel_event.is_set():
                return

            # Rebuild kwargs each attempt so api_key reflects any token refresh
            kwargs = self._build_kwargs(full_messages, stream=True, tools=tools)

            try:
                yield {"event": "phase", "data": {"phase": "connecting"}}

                stream = await litellm.acompletion(**kwargs)

                yield {"event": "phase", "data": {"phase": "waiting"}}

                current_tool_calls: dict[int, dict[str, Any]] = {}
                usage_data: dict[str, Any] | None = None
                _response_parts: list[str] = []

                async for chunk in stream:
                    if cancel_event and cancel_event.is_set():
                        return

                    if hasattr(chunk, "usage") and chunk.usage is not None:
                        usage_data = {
                            "prompt_tokens": getattr(chunk.usage, "prompt_tokens", 0) or 0,
                            "completion_tokens": getattr(chunk.usage, "completion_tokens", 0) or 0,
                            "total_tokens": getattr(chunk.usage, "total_tokens", 0) or 0,
                            "model": self.config.model,
                        }

                    choice = chunk.choices[0] if chunk.choices else None
                    if not choice:
                        continue

                    delta = choice.delta

                    if hasattr(delta, "content") and delta.content:
                        _response_parts.append(delta.content)
                        yield {"event": "token", "data": {"content": delta.content}}

                    if hasattr(delta, "tool_calls") and delta.tool_calls:
                        for tc in delta.tool_calls:
                            idx = tc.index
                            if idx not in current_tool_calls:
                                current_tool_calls[idx] = {
                                    "id": tc.id or "",
                                    "function_name": "",
                                    "arguments": "",
                                }
                            if tc.id:
                                current_tool_calls[idx]["id"] = tc.id
                            if tc.function and tc.function.name:
                                current_tool_calls[idx]["function_name"] = tc.function.name
                            if tc.function and tc.function.arguments:
                                current_tool_calls[idx]["arguments"] += tc.function.arguments
                                yield {
                                    "event": "tool_call_args_delta",
                                    "data": {
                                        "index": idx,
                                        "tool_name": current_tool_calls[idx]["function_name"],
                                        "delta": tc.function.arguments,
                                    },
                                }

                    if choice.finish_reason == "tool_calls":
                        for _idx, tc_data in sorted(current_tool_calls.items()):
                            try:
                                args = json.loads(tc_data["arguments"])
                            except json.JSONDecodeError:
                                args = {}
                            yield {
                                "event": "tool_call",
                                "data": {
                                    "id": tc_data["id"],
                                    "function_name": tc_data["function_name"],
                                    "arguments": args,
                                },
                            }
                        if not usage_data:
                            usage_data = self._estimate_fallback_usage(
                                full_messages,
                                "".join(_response_parts),
                                tools,
                            )
                        if usage_data:
                            yield {"event": "usage", "data": usage_data}
                        return

                    if choice.finish_reason == "stop":
                        if not usage_data:
                            usage_data = self._estimate_fallback_usage(
                                full_messages,
                                "".join(_response_parts),
                                tools,
                            )
                        if usage_data:
                            yield {"event": "usage", "data": usage_data}
                        yield {"event": "done", "data": {}}
                        return

                # Stream ended without explicit finish_reason
                if not usage_data:
                    usage_data = self._estimate_fallback_usage(
                        full_messages,
                        "".join(_response_parts),
                        tools,
                    )
                if usage_data:
                    yield {"event": "usage", "data": usage_data}
                yield {"event": "done", "data": {}}
                return

            except LiteLLMAuthError:
                if _retry_on_auth and self._try_refresh_token():
                    async for event in self.stream_chat(
                        messages, tools, cancel_event, extra_system_prompt, _retry_on_auth=False
                    ):
                        yield event
                else:
                    yield {
                        "event": "error",
                        "data": {
                            "message": "Authentication failed. Check your API key.",
                            "code": "auth_failed",
                            "retryable": False,
                            "provider": "litellm",
                            "model": self.config.model,
                        },
                    }
                return

            except LiteLLMContextError:
                yield {
                    "event": "error",
                    "data": {
                        "message": "Conversation too long for model context window.",
                        "code": "context_length_exceeded",
                        "retryable": False,
                        "provider": "litellm",
                        "model": self.config.model,
                    },
                }
                return

            except LiteLLMRateLimitError:
                if cancel_event and cancel_event.is_set():
                    return
                yield {
                    "event": "error",
                    "data": {
                        "message": "Rate limited by API provider",
                        "code": "rate_limit",
                        "retryable": True,
                        "provider": "litellm",
                        "model": self.config.model,
                    },
                }
                return

            except LiteLLMBadRequestError as e:
                err_msg = str(e).lower()
                if "too many" in err_msg and "tool" in err_msg:
                    yield {
                        "event": "error",
                        "data": {
                            "message": (
                                "Too many tools for this API provider. Reduce MCP tools or set ai.max_tools in config."
                            ),
                            "code": "too_many_tools",
                            "retryable": False,
                            "provider": "litellm",
                            "model": self.config.model,
                        },
                    }
                else:
                    user_msg = sanitize_provider_error(str(e))
                    logger.warning("AI bad request error: %s", e)
                    yield {
                        "event": "error",
                        "data": {
                            "message": user_msg,
                            "code": "bad_request",
                            "retryable": False,
                            "provider": "litellm",
                            "model": self.config.model,
                        },
                    }
                return

            except _LITELLM_TRANSIENT as e:
                # Explicitly transient: connection, timeout, service
                # unavailable, internal server, bad gateway. These ride the
                # retry path (#1343). Mirrors the native openai path in
                # ai_service.py:658 (APITimeoutError, APIConnectionError).
                if attempt < max_attempts - 1:
                    delay = self.config.retry_backoff_base * (2**attempt)
                    logger.warning(
                        "Transient %s (attempt %d/%d): %s. Retrying in %.1fs...",
                        type(e).__name__,
                        attempt + 1,
                        max_attempts,
                        e,
                        delay,
                    )
                    yield {
                        "event": "retrying",
                        "data": {
                            "attempt": attempt + 2,
                            "max_attempts": max_attempts,
                            "delay": delay,
                            "reason": "transient_error",
                            "exception_type": type(e).__name__,
                        },
                    }
                    if cancel_event:
                        try:
                            await asyncio.wait_for(cancel_event.wait(), timeout=delay)
                            return
                        except asyncio.TimeoutError:
                            pass
                    else:
                        await asyncio.sleep(delay)
                    continue
                # Retries exhausted on a transient error: structured error event
                logger.error(
                    "Transient %s exhausted %d attempts: %s",
                    type(e).__name__,
                    max_attempts,
                    e,
                )
                yield {
                    "event": "error",
                    "data": {
                        "message": (
                            f"Transient {type(e).__name__} after {max_attempts} attempts: "
                            + sanitize_provider_error(str(e))
                        ),
                        "code": "timeout" if isinstance(e, LiteLLMTimeoutError) else "connection_error",
                        "retryable": True,
                        "provider": "litellm",
                        "model": self.config.model,
                    },
                }
                return

            except Exception as e:
                # Unknown/unmapped error shape. Tighten to fail-fast (not
                # retry) so bad-request-style failures don't burn retry
                # budget. Transient classes are caught by the typed
                # handler above (#1343).
                logger.exception("LiteLLM unexpected error: %s", type(e).__name__)
                yield {
                    "event": "error",
                    "data": {
                        "message": sanitize_provider_error(str(e)),
                        "code": "provider_error",
                        "retryable": False,
                        "provider": "litellm",
                        "model": self.config.model,
                    },
                }
                return

    async def generate_title(self, user_message: str) -> str:
        try:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "Generate a short title (3-6 words) for a conversation that starts"
                        " with the following message. Return only the title, no quotes or punctuation."
                    ),
                },
                {"role": "user", "content": user_message},
            ]
            self._validate_request(messages)
            kwargs = self._build_kwargs(messages, max_completion_tokens=20)
            response = await litellm.acompletion(**kwargs)
            title = response.choices[0].message.content or "New Conversation"
            return title.strip().strip('"').strip("'")
        except Exception:
            logger.exception("Failed to generate title")
            return "New Conversation"

    async def validate_connection(self) -> tuple[bool, str, list[str]]:
        try:
            messages = [{"role": "user", "content": "Hi"}]
            self._validate_request(messages)
            kwargs = self._build_kwargs(messages, max_completion_tokens=5)
            response = await litellm.acompletion(**kwargs)
            if response.choices:
                return True, "Connected successfully", [self.config.model]
            return False, "No response from API", []
        except Exception:
            logger.exception("Connection validation failed")
            return False, "Connection failed", []

    async def list_models(self) -> list[str]:
        """Return available models. LiteLLM has no standard listing endpoint."""
        if self._cached_models is not None:
            return self._cached_models
        if self.config.allowed_models:
            self._cached_models = sorted(self.config.allowed_models)
        else:
            self._cached_models = [self.config.model]
        return self._cached_models

    async def complete(
        self,
        messages: list[dict[str, Any]],
        max_completion_tokens: int = 1000,
        *,
        cancel_event: asyncio.Event | None = None,
    ) -> str | None:
        result = await self.complete_result(
            messages,
            max_completion_tokens=max_completion_tokens,
            cancel_event=cancel_event,
        )
        return result.text

    async def complete_result(
        self,
        messages: list[dict[str, Any]],
        max_completion_tokens: int = 1000,
        *,
        cancel_event: asyncio.Event | None = None,
    ) -> CompletionResult:
        try:
            self._validate_request(messages)
            kwargs = self._build_kwargs(messages, max_completion_tokens=max_completion_tokens)
            provider_coro = litellm.acompletion(**kwargs)
            if cancel_event is None:
                response = await provider_coro
            else:
                provider_task = asyncio.ensure_future(provider_coro)
                cancel_wait = asyncio.ensure_future(cancel_event.wait())
                done, pending = await asyncio.wait(
                    {provider_task, cancel_wait},
                    return_when=asyncio.FIRST_COMPLETED,
                )
                for task in pending:
                    task.cancel()
                for task in pending:
                    with contextlib.suppress(asyncio.CancelledError, Exception):
                        await task
                if cancel_wait in done:
                    return CompletionResult(text=None, error_code="cancelled", error_message="cancelled")
                response = provider_task.result()
            text = response.choices[0].message.content if response.choices else None
            if not text:
                return CompletionResult(text=None, error_code="empty_completion", error_message="empty completion")
            return CompletionResult(text=text)
        except LiteLLMAuthError:
            return CompletionResult(text=None, error_code="auth_failed", error_message="authentication failed")
        except LiteLLMContextError:
            return CompletionResult(
                text=None,
                error_code="context_length_exceeded",
                error_message="Conversation too long for model context window.",
            )
        except Exception as exc:
            error_code, error_message = classify_completion_error(exc)
            if error_code == "context_length_exceeded":
                logger.warning("LiteLLM completion request exceeded context window: %s", exc)
            else:
                logger.exception("Failed to generate completion")
            return CompletionResult(text=None, error_code=error_code, error_message=error_message)

    async def complete_with_usage(
        self,
        messages: list[dict[str, Any]],
        *,
        max_completion_tokens: int = 4096,
        temperature: float | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> tuple[str | None, dict[str, int]]:
        """Bounded completion with usage metadata.

        Returns (response_text, {"prompt_tokens": N, "completion_tokens": N, "total_tokens": N}).
        """
        try:
            self._validate_request(messages)
            kwargs = self._build_kwargs(messages, max_completion_tokens=max_completion_tokens)
            if temperature is not None:
                kwargs["temperature"] = temperature
            if response_format is not None:
                kwargs["response_format"] = response_format
            response = await litellm.acompletion(**kwargs)
            text = response.choices[0].message.content if response.choices else None
            usage: dict[str, int] = {}
            if response.usage:
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens or 0,
                    "completion_tokens": response.usage.completion_tokens or 0,
                    "total_tokens": response.usage.total_tokens or 0,
                }
            return text, usage
        except Exception:
            logger.exception("Failed to generate completion with usage")
            raise
