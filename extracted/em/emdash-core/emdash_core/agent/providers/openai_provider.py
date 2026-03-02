"""OpenAI SDK-based provider - unified interface to OpenAI-compatible APIs."""

import json
import os
import base64
import re
import time
import uuid
from typing import Any, Optional, Union

from openai import OpenAI

from .base import LLMProvider, LLMResponse, ToolCall, ImageContent
from .models import ModelRegistry, ModelEntry
from ...utils.logger import log


def _parse_xml_tool_calls(error_message: str) -> list[ToolCall]:
    """Parse XML-formatted tool calls from LLM error messages.

    Supports multiple XML formats used by different models:

    1. MiniMax M2 format:
       <invoke name="tool_name">
       <parameter name="param1">value1</parameter>
       </invoke>

    2. GLM-4 format (arg_key/arg_value):
       <tool_call>function_name
       <arg_key>param1</arg_key>
       <arg_value>value1</arg_value>
       </tool_call>

    3. GLM-4 JSON format:
       <tool_call>
       {"name": "function_name", "arguments": {...}}
       </tool_call>

    Args:
        error_message: The error message containing XML tool calls

    Returns:
        List of parsed ToolCall objects
    """
    tool_calls = []

    # Pattern 1: MiniMax format - <invoke name="...">...</invoke>
    invoke_pattern = r'<invoke\s+name="([^"]+)"[^>]*>(.*?)</invoke>'
    matches = re.findall(invoke_pattern, error_message, re.DOTALL | re.IGNORECASE)

    for tool_name, invoke_content in matches:
        # Extract parameters from within the invoke block
        param_pattern = r'<parameter\s+name="([^"]+)"[^>]*>(.*?)</parameter>'
        params = re.findall(param_pattern, invoke_content, re.DOTALL | re.IGNORECASE)

        # Build arguments dict
        arguments = {}
        for param_name, param_value in params:
            param_value = param_value.strip()
            try:
                arguments[param_name] = json.loads(param_value)
            except json.JSONDecodeError:
                arguments[param_name] = param_value

        tool_call_id = f"call_{uuid.uuid4().hex[:24]}"
        tool_calls.append(ToolCall(
            id=tool_call_id,
            name=tool_name,
            arguments=json.dumps(arguments),
        ))
        log.info("Parsed MiniMax XML tool call: name={} args={}", tool_name, arguments)

    # Pattern 2: GLM-4 format - <tool_call>...</tool_call>
    tool_call_pattern = r'<tool_call>(.*?)</tool_call>'
    tool_call_matches = re.findall(tool_call_pattern, error_message, re.DOTALL | re.IGNORECASE)

    for tool_call_content in tool_call_matches:
        content = tool_call_content.strip()

        # Try GLM-4 JSON format first: {"name": "...", "arguments": {...}}
        try:
            data = json.loads(content)
            if isinstance(data, dict) and "name" in data:
                tool_name = data["name"]
                args = data.get("arguments", {})
                if isinstance(args, str):
                    args = json.loads(args)
                tool_call_id = f"call_{uuid.uuid4().hex[:24]}"
                tool_calls.append(ToolCall(
                    id=tool_call_id,
                    name=tool_name,
                    arguments=json.dumps(args),
                ))
                log.info("Parsed GLM-4 JSON tool call: name={} args={}", tool_name, args)
                continue
        except json.JSONDecodeError:
            pass

        # Try GLM-4 arg_key/arg_value format
        # First line is function name, then <arg_key>/<arg_value> pairs
        lines = content.split('\n')
        if lines:
            func_name = lines[0].strip()
            if func_name and not func_name.startswith('<'):
                # Extract arg_key/arg_value pairs
                arg_key_pattern = r'<arg_key>(.*?)</arg_key>'
                arg_value_pattern = r'<arg_value>(.*?)</arg_value>'
                keys = re.findall(arg_key_pattern, content, re.DOTALL)
                values = re.findall(arg_value_pattern, content, re.DOTALL)

                if keys and len(keys) == len(values):
                    arguments = {}
                    for k, v in zip(keys, values):
                        k = k.strip()
                        v = v.strip()
                        try:
                            arguments[k] = json.loads(v)
                        except json.JSONDecodeError:
                            arguments[k] = v

                    tool_call_id = f"call_{uuid.uuid4().hex[:24]}"
                    tool_calls.append(ToolCall(
                        id=tool_call_id,
                        name=func_name,
                        arguments=json.dumps(arguments),
                    ))
                    log.info("Parsed GLM-4 arg_key/arg_value tool call: name={} args={}", func_name, arguments)

    return tool_calls


class OpenAIProvider(LLMProvider):
    """
    Unified LLM provider using OpenAI SDK.

    Supports OpenAI-compatible APIs (OpenAI, Fireworks, etc.).
    Just change the model - the provider auto-configures based on the model's provider.
    """

    def __init__(self, model: Union[ModelEntry, str]):
        """
        Initialize the provider.

        Args:
            model: ModelEntry or model string
        """
        registry = ModelRegistry.get()

        if isinstance(model, ModelEntry):
            self.chat_model = model
            self.model = model.api_model
            self._context_limit = model.context_window
            self._provider = model.provider
        else:
            # Raw model string - try to look up in registry
            parsed = registry.get_model(model)
            if parsed:
                self.chat_model = parsed
                self.model = parsed.api_model
                self._context_limit = parsed.context_window
                self._provider = parsed.provider
            else:
                configured_models = sorted(
                    {entry["name"] for entry in registry.list_all() if entry.get("name")}
                )
                preview = ", ".join(configured_models[:8]) or "(none)"
                raise ValueError(
                    f"Model '{model}' is not configured in {registry.config_path}. "
                    f"Use a model from .emdash/config.json. "
                    f"Configured models include: {preview}"
                )

        # Get provider config from registry
        prov_config = registry.get_provider_config(self._provider)
        if not prov_config:
            configured = list(registry.providers.keys()) or ["(none)"]
            raise ValueError(
                f"Model '{self.model}' requires provider '{self._provider}' "
                f"which is not configured. "
                f"Configured providers: {', '.join(configured)}. "
                f"Add the provider to .emdash/config.json or switch to a configured model."
            )
        raw_base_url = prov_config.base_url
        config_api_key = prov_config.api_key

        # Resolve base_url: "$VAR" reads from env, bare string is literal, None stays None
        if raw_base_url:
            config_base_url, _ = self._resolve_value(raw_base_url)
        else:
            config_base_url = None

        # Resolve api_key: "$VAR" reads from env, bare string is a literal key
        raw_api_key, api_key_source = self._resolve_value(config_api_key)

        api_key = self._sanitize_api_key(raw_api_key)
        if not api_key:
            # Allow empty api_key when headers provide authentication
            if prov_config and prov_config.headers:
                api_key = "header-auth"  # Dummy key; OpenAI SDK requires non-empty value
                api_key_source = "header-auth (no api_key, using headers)"
                log.debug(
                    "No API key for provider='{}', using header-based auth",
                    self._provider,
                )
            else:
                raise ValueError(
                    f"Missing API key for provider '{self._provider}'. "
                    f"Config has api_key={config_api_key!r}. "
                    f"Model: {self.model}"
                )
        self._api_key = api_key
        if raw_api_key and api_key != raw_api_key:
            log.debug(
                f"Sanitized API key for provider={self._provider} source={api_key_source} "
                "(trimmed whitespace/quotes)."
            )
        log_api_key = self._setting_bool(registry, "log_llm_api_key")
        if log_api_key:
            log.debug(
                "LLM provider init provider={} model={} base_url={} key_source={} api_key={}",
                self._provider,
                self.model,
                config_base_url or "https://api.openai.com/v1",
                api_key_source,
                api_key,
            )
        else:
            log.debug(
                "LLM provider init provider={} model={} base_url={} key_source={} key_len={} key_hint={}",
                self._provider,
                self.model,
                config_base_url or "https://api.openai.com/v1",
                api_key_source,
                len(api_key),
                self._mask_api_key(api_key),
            )
        if len(api_key) < 20:
            log.warning(
                "API key for provider={} looks short (len={}). Source: {}",
                self._provider,
                len(api_key),
                api_key_source,
            )

        # Provider-level streaming flag (some proxies require stream=true)
        self._force_stream = bool(prov_config and prov_config.stream)

        self._reasoning_override = self._setting_bool(registry, "reasoning")
        self._thinking_override = self._setting_bool(registry, "thinking")
        self._thinking_budget = self._setting_int(registry, "thinking_budget", 10000)
        # Reasoning effort for Fireworks thinking models: none, low, medium, high
        self._reasoning_effort = str(registry.get_setting("reasoning_effort", "medium"))
        # Parallel tool calls for OpenAI-compatible APIs (Fireworks supports this)
        self._parallel_tool_calls = self._setting_bool(registry, "parallel_tool_calls")
        # Optional global max_output_tokens override from config settings.
        self._max_output_tokens_override = self._setting_int(registry, "max_output_tokens", 0)
        self._log_payload = bool(self._setting_bool(registry, "log_llm_payload"))

        base_url = config_base_url
        self._is_custom_openai_base_url = bool(self._provider == "openai" and base_url)

        # Configure timeout from config settings (default 300 seconds / 5 minutes)
        # LLM calls can take a while with large contexts, so we use a generous default
        timeout_seconds = self._setting_int(registry, "llm_timeout", 300)
        self._timeout = timeout_seconds

        # Resolve provider headers: "$VAR" reads from env, bare string is literal
        # Skip headers whose env var didn't resolve
        default_headers = {}
        if prov_config and prov_config.headers:
            for header_name, header_value in prov_config.headers:
                resolved, source = self._resolve_value(header_value)
                if resolved:
                    default_headers[header_name] = resolved
                    log.info(
                        "Header resolved {}={} provider={} value_len={}",
                        header_name,
                        source,
                        self._provider,
                        len(resolved),
                    )
                else:
                    log.warning(
                        "Header NOT resolved {}={} provider={} — env var not set?",
                        header_name,
                        source,
                        self._provider,
                    )
        else:
            log.debug(
                "No custom headers for provider={} prov_config={} headers={}",
                self._provider,
                prov_config is not None,
                prov_config.headers if prov_config else "N/A",
            )

        # Print full provider init summary (visible in server stdout)
        header_preview = {k: v[:20] + "..." if len(v) > 20 else v for k, v in default_headers.items()} if default_headers else {}
        print(
            f"[LLM] provider={self._provider} model={self.model} "
            f"base_url={base_url or 'default'} "
            f"api_key={self._mask_api_key(api_key)} "
            f"headers={header_preview}"
        )

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout_seconds,
            default_headers=default_headers or None,
        )

    @staticmethod
    def _resolve_value(value: str) -> tuple[Optional[str], str]:
        """Resolve a config value.

        "$ENV_VAR" reads from environment variable ENV_VAR.
        Any other string is used as a literal value.

        Returns:
            (resolved_value, source_description) tuple
        """
        if value.startswith("$"):
            env_var = value[1:]
            return os.environ.get(env_var), value
        else:
            return value, "literal"

    @staticmethod
    def _sanitize_api_key(api_key: Optional[str]) -> Optional[str]:
        """Normalize API key values loaded from env/.env."""
        if api_key is None:
            return None
        cleaned = api_key.strip()
        if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {"'", '"'}:
            cleaned = cleaned[1:-1].strip()
        return cleaned or None

    @staticmethod
    def _parse_bool(value: Any) -> Optional[bool]:
        """Parse a bool from config values."""
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        cleaned = str(value).strip().lower()
        if cleaned in {"1", "true", "yes", "y", "on"}:
            return True
        if cleaned in {"0", "false", "no", "n", "off"}:
            return False
        return None

    @classmethod
    def _setting_bool(cls, registry: ModelRegistry, key: str) -> Optional[bool]:
        return cls._parse_bool(registry.get_setting(key))

    @staticmethod
    def _setting_int(registry: ModelRegistry, key: str, default: int) -> int:
        raw = registry.get_setting(key, default)
        try:
            return int(raw)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _mask_api_key(api_key: str) -> str:
        """Mask API key for safe logging."""
        if len(api_key) <= 8:
            return "*" * len(api_key)
        return f"{api_key[:4]}...{api_key[-4:]}"

    def _infer_provider(self, model: str) -> str:
        """Infer provider from model string.

        Returns the appropriate provider based on model name.
        Only returns a provider name if it's actually configured in the registry.
        OPENAI_BASE_URL only affects the openai provider's base URL,
        not provider selection.
        """
        registry = ModelRegistry.get()
        model_lower = model.lower()
        if "fireworks" in model_lower or "accounts/fireworks" in model_lower:
            if registry.get_provider_config("fireworks"):
                return "fireworks"
        return "openai"  # Default

    def chat(
        self,
        messages: list[dict],
        tools: Optional[list[dict]] = None,
        system: Optional[str] = None,
        reasoning: bool = False,
        thinking: bool = False,
        images: Optional[list[ImageContent]] = None,
    ) -> LLMResponse:
        """
        Send a chat completion request via OpenAI SDK.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool schemas (OpenAI format)
            system: Optional system prompt
            reasoning: Enable reasoning mode (for models that support it)
            thinking: Enable extended thinking (for models that support it)
            images: Optional list of images for vision-capable models

        Returns:
            LLMResponse with content and/or tool calls
        """
        # Add model-specific instructions for MiniMax models
        # MiniMax M2 is trained to output XML tool calls, but Fireworks API expects JSON
        # Adding explicit JSON format instructions helps ensure compatibility
        if tools and "minimax" in self.model.lower():
            minimax_tool_instruction = (
                "\n\n## CRITICAL: Tool Call Format\n"
                "When calling tools/functions, you MUST use the standard OpenAI function calling format. "
                "DO NOT use XML format like <invoke> or <parameter> tags. "
                "The API will automatically handle your tool calls - just specify which function to call and its arguments."
            )
            if system:
                system = system + minimax_tool_instruction
            else:
                system = minimax_tool_instruction.strip()

        # Prepend system message if provided
        if system:
            messages = [{"role": "system", "content": system}] + messages

        if self._reasoning_override is not None:
            reasoning = self._reasoning_override
        if self._thinking_override is not None:
            thinking = self._thinking_override

        # Build completion kwargs
        kwargs = {
            "model": self.model,
            "messages": messages,
        }

        # Set max_tokens from model spec or env override
        max_tokens = self._max_output_tokens_override
        if max_tokens == 0 and self.chat_model:
            max_tokens = self.chat_model.spec.max_output_tokens
        if max_tokens > 0:
            kwargs["max_tokens"] = max_tokens

        # Enable streaming when the provider config requires it,
        # or when Fireworks-backed models need it for large max_tokens.
        use_streaming = False
        is_fireworks_model = self.model.startswith("accounts/fireworks/models/")
        if self._force_stream:
            kwargs["stream"] = True
            use_streaming = True
            log.debug(
                "Enabling streaming for provider={} (stream=true in config)",
                self._provider,
            )
        elif max_tokens > 4096 and (self._provider == "fireworks" or is_fireworks_model):
            kwargs["stream"] = True
            use_streaming = True
            log.debug(
                "Enabling streaming for Fireworks-backed model (provider={} model={} max_tokens={} > 4096)",
                self._provider,
                self.model,
                max_tokens,
            )

        # Add tools if provided
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
            # Add parallel_tool_calls if enabled (Fireworks and OpenAI support this)
            if self._parallel_tool_calls is True:
                kwargs["parallel_tool_calls"] = True
                log.debug(
                    "Parallel tool calls enabled provider={} model={}",
                    self._provider,
                    self.model,
                )

        # Add reasoning support via extra_body for providers that support it
        # Skip reasoning for custom base URLs (they may not support it)
        is_custom_api = self._is_custom_openai_base_url
        if reasoning and self._provider == "openai" and not is_custom_api:
            kwargs["extra_body"] = {"reasoning": {"enabled": True}}

        # Add reasoning_effort for Fireworks models that support it
        # We'll try with it first, and if rejected, retry without
        if thinking and self._provider == "fireworks" and self._reasoning_effort != "none":
            if not getattr(self, '_reasoning_effort_unsupported', False):
                kwargs["reasoning_effort"] = self._reasoning_effort
                log.info(
                    "Reasoning effort enabled provider={} model={} effort={}",
                    self._provider,
                    self.model,
                    self._reasoning_effort,
                )

        # Add images if provided (vision support)
        if images:
            log.info(
                "Adding {} images to request provider={} model={}",
                len(images),
                self._provider,
                self.model,
            )
            # Find the last user message and add images to it
            for i in range(len(messages) - 1, -1, -1):
                if messages[i].get("role") == "user":
                    messages[i]["content"] = self._format_content_with_images(
                        messages[i].get("content", ""), images
                    )
                    break

        extra_headers = {}

        messages_summary = [
            {
                "role": m.get("role"),
                "content_len": len(str(m.get("content", ""))),
            }
            for m in messages
        ]
        log.info(
            "LLM request start provider={} model={} messages={} tools={} reasoning={} max_tokens={}",
            self._provider,
            self.model,
            len(messages),
            bool(tools),
            reasoning,
            kwargs.get("max_tokens", "default"),
        )
        log_payload = self._log_payload
        if log_payload:
            log.debug(
                "LLM request payload provider={} model={} headers={} payload={}",
                self._provider,
                self.model,
                sorted(extra_headers.keys()),
                kwargs,
            )
        else:
            log.debug(
                "LLM request provider={} model={} messages={} tools={} reasoning={} headers={}",
                self._provider,
                self.model,
                messages_summary,
                bool(tools),
                reasoning,
                sorted(extra_headers.keys()),
            )

        # Call OpenAI SDK
        # Use with_raw_response to capture the original JSON (for reasoning_content extraction)
        start_time = time.time()
        raw_json_data = None  # Store raw JSON for reasoning_content extraction
        try:
            if use_streaming:
                # Streaming doesn't support with_raw_response the same way
                response = self.client.chat.completions.create(**kwargs)
                response = self._collect_stream(response)
            else:
                # Use with_raw_response to get access to original JSON
                # This preserves fields like reasoning_content that Pydantic drops
                raw_response = self.client.chat.completions.with_raw_response.create(**kwargs)
                response = raw_response.parse()
                # Extract raw JSON for reasoning_content
                try:
                    raw_json_data = raw_response.http_response.json()
                except Exception:
                    pass
        except Exception as exc:  # pragma: no cover - defensive logging
            elapsed = time.time() - start_time
            status = getattr(exc, "status_code", None)
            code = getattr(exc, "code", None)
            error_msg = str(exc).lower()

            # Check if error is XML tool call format issue (MiniMax or GLM-4)
            # MiniMax M2 outputs <invoke> format, GLM-4 outputs <tool_call> format
            # Fireworks sometimes fails to parse these - we can extract from error message
            has_xml_tool_call = "<invoke" in error_msg or "<tool_call>" in error_msg
            if "json does not contain content for both" in error_msg and has_xml_tool_call:
                # Try to parse XML tool calls from the error message
                original_error = str(exc)
                parsed_tool_calls = _parse_xml_tool_calls(original_error)

                if parsed_tool_calls:
                    elapsed = time.time() - start_time
                    log.info(
                        "Successfully parsed {} XML tool call(s) from MiniMax error "
                        "provider={} model={} elapsed={:.1f}s",
                        len(parsed_tool_calls),
                        self._provider,
                        self.model,
                        elapsed,
                    )
                    # Return a synthetic LLMResponse with the parsed tool calls
                    return LLMResponse(
                        content=None,
                        thinking=None,
                        tool_calls=parsed_tool_calls,
                        raw=None,  # No raw response since we parsed from error
                        stop_reason="tool_calls",
                        input_tokens=0,  # Unknown
                        output_tokens=0,  # Unknown
                        thinking_tokens=0,
                    )
                else:
                    log.error(
                        "MiniMax XML tool call format error detected but failed to parse. "
                        "provider={} model={} error={}",
                        self._provider,
                        self.model,
                        exc,
                    )
                    # Re-raise with helpful message
                    raise RuntimeError(
                        f"MiniMax tool call format error: The model output XML-formatted tool calls "
                        f"which could not be parsed. Original error: {exc}"
                    ) from exc

            # Check if error is about reasoning_effort not being supported
            if "reasoning_effort" in error_msg or "reasoning" in error_msg and "not support" in error_msg:
                if "reasoning_effort" in kwargs:
                    log.warning(
                        "Model doesn't support reasoning_effort, retrying without it provider={} model={}",
                        self._provider,
                        self.model,
                    )
                    # Remember this model doesn't support reasoning_effort
                    self._reasoning_effort_unsupported = True
                    # Remove reasoning_effort and retry
                    del kwargs["reasoning_effort"]
                    try:
                        # Use with_raw_response to capture reasoning_content
                        raw_resp = self.client.chat.completions.with_raw_response.create(**kwargs)
                        response = raw_resp.parse()
                        retry_raw_json = None
                        try:
                            retry_raw_json = raw_resp.http_response.json()
                        except Exception:
                            pass
                        # Success - continue to return response below
                        elapsed = time.time() - start_time
                        log.info(
                            "LLM request completed (without reasoning_effort) provider={} model={} elapsed={:.1f}s",
                            self._provider,
                            self.model,
                            elapsed,
                        )
                        return self._to_llm_response(response, retry_raw_json)
                    except Exception as retry_exc:
                        log.exception(
                            "LLM retry request failed provider={} model={} error={}",
                            self._provider,
                            self.model,
                            retry_exc,
                        )
                        raise

            log.exception(
                "LLM request failed provider={} model={} status={} code={} elapsed={:.1f}s error={}",
                self._provider,
                self.model,
                status,
                code,
                elapsed,
                exc,
            )
            raise

        elapsed = time.time() - start_time
        log.info(
            "LLM request completed provider={} model={} elapsed={:.1f}s",
            self._provider,
            self.model,
            elapsed,
        )

        return self._to_llm_response(response, raw_json_data)

    def _collect_stream(self, stream):
        """Collect streaming chunks into a single response object.

        This is used for Fireworks API which requires streaming for max_tokens > 4096.
        We collect all chunks and build a response object that matches the non-streaming format.
        """
        content_parts = []
        reasoning_parts = []  # Collect reasoning/thinking content
        tool_calls_data = {}  # id -> {name, arguments}
        finish_reason = None
        model = None
        usage = None

        for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            model = chunk.model or model

            # Collect content
            if delta.content:
                content_parts.append(delta.content)

            # Collect reasoning_content if present in delta
            # Check multiple ways since the SDK might not expose extra fields directly
            reasoning_chunk = None
            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                reasoning_chunk = delta.reasoning_content
            elif hasattr(delta, "model_extra"):
                reasoning_chunk = delta.model_extra.get("reasoning_content")
            elif hasattr(chunk, "_raw_response"):
                # Try to get from raw response
                try:
                    raw = chunk._raw_response
                    if hasattr(raw, "json"):
                        raw_json = raw.json()
                        choices = raw_json.get("choices", [])
                        if choices and choices[0].get("delta"):
                            reasoning_chunk = choices[0]["delta"].get("reasoning_content")
                except Exception:
                    pass
            if reasoning_chunk:
                reasoning_parts.append(reasoning_chunk)

            # Collect tool calls
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    tc_id = tc.id or str(tc.index)
                    if tc_id not in tool_calls_data:
                        tool_calls_data[tc_id] = {"id": tc.id, "name": "", "arguments": ""}
                    if tc.function:
                        if tc.function.name:
                            tool_calls_data[tc_id]["name"] = tc.function.name
                        if tc.function.arguments:
                            tool_calls_data[tc_id]["arguments"] += tc.function.arguments

            # Capture finish reason
            if chunk.choices[0].finish_reason:
                finish_reason = chunk.choices[0].finish_reason

            # Capture usage if present
            if hasattr(chunk, "usage") and chunk.usage:
                usage = chunk.usage

        # Build a mock response object that matches non-streaming format
        collected_reasoning = "".join(reasoning_parts) if reasoning_parts else None
        if collected_reasoning:
            log.info(
                "Stream reasoning collected provider={} model={} len={}",
                self._provider,
                self.model,
                len(collected_reasoning),
            )

        class MockMessage:
            def __init__(self):
                self.content = "".join(content_parts) if content_parts else None
                self.tool_calls = []
                self.reasoning_content = collected_reasoning

                for tc_data in tool_calls_data.values():
                    tc = type("ToolCall", (), {
                        "id": tc_data["id"],
                        "type": "function",
                        "function": type("Function", (), {
                            "name": tc_data["name"],
                            "arguments": tc_data["arguments"],
                        })(),
                    })()
                    self.tool_calls.append(tc)

                if not self.tool_calls:
                    self.tool_calls = None

        class MockChoice:
            def __init__(self):
                self.message = MockMessage()
                self.finish_reason = finish_reason

        class MockResponse:
            def __init__(self):
                self.choices = [MockChoice()]
                self.model = model
                self.usage = usage

        return MockResponse()

    def _to_llm_response(self, response, raw_json_data: dict | None = None) -> LLMResponse:
        """Convert OpenAI response to our LLMResponse format.

        Args:
            response: The parsed OpenAI response object
            raw_json_data: Optional raw JSON from the API (preserves fields like reasoning_content)
        """
        response_model = getattr(response, "model", None)
        log.info(
            "LLM response received provider={} model={} response_model={}",
            self._provider,
            self.model,
            response_model,
        )
        log.debug(
            "LLM response provider={} model={} response_model={}",
            self._provider,
            self.model,
            response_model,
        )
        choice = response.choices[0]
        message = choice.message

        # Debug: Log message attributes to help trace reasoning_content extraction
        msg_attrs = [attr for attr in dir(message) if not attr.startswith('_')]
        log.debug(
            "Message attributes provider={} model={} attrs={}",
            self._provider,
            self.model,
            msg_attrs[:20],  # First 20 to avoid log spam
        )
        if hasattr(message, "model_extra") and message.model_extra:
            log.debug(
                "Message model_extra keys provider={} keys={}",
                self._provider,
                list(message.model_extra.keys()),
            )

        # Extract content and thinking
        content = message.content
        thinking = None

        # Check for reasoning_content field (Fireworks/OpenAI thinking models)
        # This is separate from Anthropic's content blocks format
        # The OpenAI SDK drops extra fields, so we check raw JSON first
        reasoning_content = None

        # Method 0: Use raw_json_data if available (most reliable)
        # This comes from with_raw_response and preserves all fields
        if raw_json_data:
            try:
                choices = raw_json_data.get("choices", [])
                if choices:
                    msg_data = choices[0].get("message", {})
                    reasoning_content = msg_data.get("reasoning_content")
                    if reasoning_content:
                        log.info(
                            "reasoning_content found in raw_json_data provider={} model={} len={}",
                            self._provider,
                            self.model,
                            len(reasoning_content),
                        )
            except Exception as e:
                log.debug(f"Failed to extract reasoning_content from raw_json_data: {e}")

        # Method 1: Direct attribute access
        if not reasoning_content and hasattr(message, "reasoning_content"):
            reasoning_content = message.reasoning_content

        # Method 2: Check model_extra (Pydantic v2 stores extra fields here)
        if not reasoning_content and hasattr(message, "model_extra"):
            reasoning_content = message.model_extra.get("reasoning_content")

        # Method 3: Try to access via __dict__ or model_dump
        if not reasoning_content:
            try:
                if hasattr(message, "model_dump"):
                    msg_dict = message.model_dump()
                    reasoning_content = msg_dict.get("reasoning_content")
                elif hasattr(message, "__dict__"):
                    reasoning_content = message.__dict__.get("reasoning_content")
            except Exception:
                pass

        # Method 4: Access raw response data through OpenAI client's internal structure
        # The SDK stores raw JSON in _raw_response or similar attributes
        if not reasoning_content:
            try:
                # Check if response has _raw_response (httpx response)
                if hasattr(response, "_raw_response"):
                    raw = response._raw_response
                    if hasattr(raw, "json"):
                        raw_json = raw.json()
                        choices = raw_json.get("choices", [])
                        if choices:
                            msg = choices[0].get("message", {})
                            reasoning_content = msg.get("reasoning_content")
                            if reasoning_content:
                                log.debug("reasoning_content found in _raw_response")
            except Exception as e:
                log.debug(f"Failed to extract reasoning_content from _raw_response: {e}")

        # Method 5: Try model_dump with mode='json' or include extra
        if not reasoning_content:
            try:
                if hasattr(message, "model_dump"):
                    # Try with all fields mode
                    msg_dict = message.model_dump(mode='python', by_alias=True, exclude_unset=False)
                    reasoning_content = msg_dict.get("reasoning_content")
                    if not reasoning_content:
                        # Also check for snake_case variant
                        reasoning_content = msg_dict.get("reasoning")
            except Exception:
                pass

        # Method 6: Check choice-level for reasoning_content (some APIs put it there)
        if not reasoning_content:
            try:
                if hasattr(choice, "reasoning_content"):
                    reasoning_content = choice.reasoning_content
                elif hasattr(choice, "model_extra"):
                    reasoning_content = choice.model_extra.get("reasoning_content")
            except Exception:
                pass

        if reasoning_content:
            thinking = reasoning_content
            log.info(
                "Reasoning content extracted provider={} model={} len={}",
                self._provider,
                self.model,
                len(thinking),
            )

        # Check for inline <think>...</think> tags (used by some models like DeepSeek, Kimi, etc.)
        # Extract thinking content and remove from main content
        if not thinking and content:
            import re
            think_pattern = r'<think>(.*?)</think>'
            think_matches = re.findall(think_pattern, content, re.DOTALL)
            if think_matches:
                thinking = "\n".join(think_matches)
                content = re.sub(think_pattern, '', content, flags=re.DOTALL).strip()
                log.debug(
                    "Thinking extracted from <think> tags provider={} len={}",
                    self._provider,
                    len(thinking),
                )

        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=tc.function.arguments,
                ))

        # Extract token usage if available
        input_tokens = 0
        output_tokens = 0
        thinking_tokens = 0
        if hasattr(response, "usage") and response.usage:
            input_tokens = getattr(response.usage, "prompt_tokens", 0) or 0
            output_tokens = getattr(response.usage, "completion_tokens", 0) or 0
            # Try to get reasoning/thinking tokens from the API response
            # Different providers use different field names
            thinking_tokens = (
                getattr(response.usage, "reasoning_tokens", 0)
                or getattr(response.usage, "thinking_tokens", 0)
                or 0
            )
            # If no explicit thinking tokens but we have thinking content, estimate
            if not thinking_tokens and thinking:
                thinking_tokens = len(thinking) // 4  # Rough estimate

        if thinking:
            log.info(
                "Extended thinking captured provider={} model={} thinking_len={} thinking_tokens={}",
                self._provider,
                self.model,
                len(thinking),
                thinking_tokens,
            )

        return LLMResponse(
            content=content,
            thinking=thinking,
            tool_calls=tool_calls,
            raw=response,
            stop_reason=choice.finish_reason,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            thinking_tokens=thinking_tokens,
        )

    def get_context_limit(self) -> int:
        """Get the context window size for this model."""
        return self._context_limit

    def get_max_image_size(self) -> int:
        """Get maximum image size in bytes for this model."""
        return 5 * 1024 * 1024  # 5MB default for OpenAI-compatible APIs

    def supports_vision(self) -> bool:
        """Check if this model supports image input."""
        # Allow explicit override via env var
        vision_override = os.environ.get("EMDASH_ENABLE_VISION", "").lower()
        if vision_override in ("1", "true", "yes"):
            return True
        if vision_override in ("0", "false", "no"):
            return False

        if self.chat_model:
            return self.chat_model.spec.supports_vision

        # For unknown models, check if model name suggests vision support
        model_lower = self.model.lower()
        vision_indicators = ["-vl", "vl-", "vision", "4o", "gpt-4-turbo"]
        return any(ind in model_lower for ind in vision_indicators)

    def supports_thinking(self) -> bool:
        """Check if this model supports extended thinking."""
        if self.chat_model:
            return self.chat_model.spec.supports_thinking

        # Unknown models default to no thinking support
        return False

    def _format_image_for_api(self, image: ImageContent) -> dict:
        """Format an image for OpenAI-compatible API.

        Args:
            image: ImageContent with raw image data

        Returns:
            Dict with image_url for the API
        """
        encoded = base64.b64encode(image.image_data).decode("utf-8")
        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/{image.format};base64,{encoded}"
            }
        }

    def _format_content_with_images(
        self,
        text: str,
        images: Optional[list[ImageContent]] = None
    ):
        """Format message content with optional images.

        For vision models, returns a list of content blocks.
        For non-vision models, returns text only.

        Args:
            text: Text content
            images: Optional list of images

        Returns:
            Content formatted for this provider
        """
        if not images:
            return text

        if not self.supports_vision():
            log.warning(
                "Model {} does not support vision, images will be stripped",
                self.model,
            )
            return text

        # Vision model: create content blocks
        content = [{"type": "text", "text": text}]
        for img in images:
            content.append(self._format_image_for_api(img))

        return content

    def format_tool_result(self, tool_call_id: str, result: str) -> dict:
        """
        Format a tool result message.

        Uses OpenAI format.
        """
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": result,
        }

    def format_assistant_message(self, response: LLMResponse) -> dict:
        """
        Format an assistant response to add back to messages.

        Uses OpenAI format.
        """
        message: dict[str, Any] = {"role": "assistant"}

        if response.content:
            message["content"] = response.content

        if response.tool_calls:
            message["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.name,
                        "arguments": tc.arguments,
                    }
                }
                for tc in response.tool_calls
            ]

        return message
