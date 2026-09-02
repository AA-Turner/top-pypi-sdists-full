"""OpenAI-compatible non-streaming Chat Completions provider."""

from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Mapping
from urllib.error import URLError

from ..errors import (
    ProviderAuthError,
    ProviderConnectionError,
    ProviderRateLimitError,
    ProviderResponseError,
    ProviderTimeoutError,
)
from ..generation import (
    GenerationRequest,
    GenerationResult,
    ModelInfo,
    TokenUsage,
    _thaw_json,
)
from ._http import (
    ResponseTooLargeError,
    UrllibTransport,
    decode_json_object,
    endpoint_url,
    is_timeout_error,
    normalize_base_url,
    response_error_detail,
    retry_after_seconds,
    validate_headers,
)
from .base import HttpResponse, HttpTransport, RequestPolicy

_RETRYABLE_STATUSES = frozenset({408, 429, 500, 502, 503, 504})
_RESERVED_HEADERS = frozenset(
    {"authorization", "content-length", "content-type", "accept", "host"}
)
_MODEL_METADATA_FIELDS = (
    "owned_by",
    "created",
    "context_length",
)
_RESULT_METADATA_FIELDS = (
    "created",
    "service_tier",
    "system_fingerprint",
    "timings",
)


class OpenAICompatibleProvider:
    """Call an explicitly configured OpenAI-compatible HTTP endpoint.

    Constructing a provider is side-effect free. Network access occurs only
    when :meth:`generate`, :meth:`list_models`, or their async variants are
    called.
    """

    __slots__ = (
        "_api_key",
        "_base_url",
        "_headers",
        "_max_tokens_field",
        "_name",
        "_policy",
        "_secrets",
        "_transport",
    )

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        *,
        name: str = "custom",
        headers: Mapping[str, str] | None = None,
        policy: RequestPolicy | None = None,
        transport: HttpTransport | None = None,
        max_tokens_field: str = "max_tokens",
    ) -> None:
        if type(name) is not str:
            raise TypeError("name must be a string")
        if not name.strip():
            raise ValueError("name must not be empty or whitespace")
        if api_key is not None:
            if type(api_key) is not str:
                raise TypeError("api_key must be a string or None")
            if not api_key:
                raise ValueError("api_key must not be empty")
        if policy is not None and not isinstance(policy, RequestPolicy):
            raise TypeError("policy must be a RequestPolicy or None")
        if transport is not None and not isinstance(transport, HttpTransport):
            raise TypeError("transport must implement HttpTransport")
        if max_tokens_field not in {"max_tokens", "max_completion_tokens"}:
            raise ValueError(
                "max_tokens_field must be 'max_tokens' or "
                "'max_completion_tokens'"
            )

        normalized_base_url = normalize_base_url(base_url)
        safe_headers = validate_headers(headers, reserved=_RESERVED_HEADERS)
        secret_values = [normalized_base_url]
        if api_key:
            secret_values.append(api_key)
        secret_values.extend(
            value for value in safe_headers.values() if len(value) >= 4
        )

        self._name = name
        self._base_url = normalized_base_url
        self._api_key = api_key
        self._headers = safe_headers
        self._policy = policy if policy is not None else RequestPolicy()
        self._transport = transport if transport is not None else UrllibTransport()
        self._max_tokens_field = max_tokens_field
        self._secrets = tuple(secret_values)

    @property
    def name(self) -> str:
        """Return the stable provider label stored in generation metadata."""

        return self._name

    def __repr__(self) -> str:
        key_state = "***" if self._api_key is not None else "None"
        return (
            f"{type(self).__name__}(name={self._name!r}, "
            f"api_key={key_state})"
        )

    def __reduce_ex__(self, protocol: int) -> object:
        del protocol
        raise TypeError(
            "provider configurations contain runtime secrets and cannot be serialized"
        )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate one explicit, non-streaming chat completion."""

        if not isinstance(request, GenerationRequest):
            raise TypeError("request must be a GenerationRequest")
        payload: dict[str, object] = {
            "model": request.model,
            "messages": [message.to_dict() for message in request.messages],
            "stream": False,
        }
        if request.max_tokens is not None:
            payload[self._max_tokens_field] = request.max_tokens
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        if request.seed is not None:
            payload["seed"] = request.seed
        if request.stop:
            payload["stop"] = list(request.stop)
        payload.update(_thaw_json(request.extra_body))  # type: ignore[arg-type]

        started = time.monotonic()
        response, attempts = self._request_json(
            method="POST",
            path="chat/completions",
            payload=payload,
        )
        latency = time.monotonic() - started
        try:
            return self._parse_generation(
                response,
                request=request,
                latency_seconds=latency,
                attempts=attempts,
            )
        except (TypeError, ValueError, KeyError) as error:
            raise ProviderResponseError(
                "provider returned an invalid chat completion",
                provider=self._name,
                status_code=response.status,
                attempts=attempts,
            ) from error

    async def agenerate(self, request: GenerationRequest) -> GenerationResult:
        """Run :meth:`generate` in a worker thread."""

        return await asyncio.to_thread(self.generate, request)

    def list_models(self) -> tuple[ModelInfo, ...]:
        """List model IDs from the configured OpenAI-compatible endpoint."""

        response, attempts = self._request_json(
            method="GET",
            path="models",
            payload=None,
        )
        try:
            decoded = decode_json_object(response.body)
            data = decoded["data"]
            if type(data) is not list:
                raise TypeError("data must be a list")

            models: list[ModelInfo] = []
            for item in data:
                if not isinstance(item, Mapping):
                    raise TypeError("model entries must be objects")
                model_id = item.get("id")
                if type(model_id) is not str or not model_id.strip():
                    raise ValueError("model entries must contain a non-empty id")
                display_name = item.get("name")
                if display_name is not None and type(display_name) is not str:
                    display_name = None
                metadata = {
                    key: item[key]
                    for key in _MODEL_METADATA_FIELDS
                    if key in item
                }
                models.append(
                    ModelInfo(
                        id=model_id,
                        provider=self._name,
                        display_name=display_name,
                        metadata=metadata,
                    )
                )
            return tuple(models)
        except (TypeError, ValueError, KeyError) as error:
            raise ProviderResponseError(
                "provider returned an invalid model list",
                provider=self._name,
                status_code=response.status,
                attempts=attempts,
            ) from error

    async def alist_models(self) -> tuple[ModelInfo, ...]:
        """Run :meth:`list_models` in a worker thread."""

        return await asyncio.to_thread(self.list_models)

    def _request_json(
        self,
        *,
        method: str,
        path: str,
        payload: Mapping[str, object] | None,
    ) -> tuple[HttpResponse, int]:
        url = endpoint_url(self._base_url, path)
        headers = {
            "Accept": "application/json",
            "User-Agent": "localarena",
            **self._headers,
        }
        body = None
        if payload is not None:
            try:
                body = json.dumps(
                    payload,
                    ensure_ascii=False,
                    allow_nan=False,
                    separators=(",", ":"),
                ).encode("utf-8")
            except (TypeError, ValueError) as error:
                raise ProviderResponseError(
                    "generation request is not JSON-compatible",
                    provider=self._name,
                ) from error
            headers["Content-Type"] = "application/json"
        if self._api_key is not None:
            headers["Authorization"] = f"Bearer {self._api_key}"

        for attempt in range(1, self._policy.max_attempts + 1):
            try:
                response = self._transport.request(
                    method=method,
                    url=url,
                    headers=headers,
                    body=body,
                    timeout=self._policy.timeout,
                    max_response_bytes=self._policy.max_response_bytes,
                )
                if len(response.body) > self._policy.max_response_bytes:
                    raise ResponseTooLargeError
            except BaseException as error:
                if isinstance(error, (KeyboardInterrupt, SystemExit)):
                    raise
                if isinstance(error, ResponseTooLargeError):
                    raise ProviderResponseError(
                        "provider response exceeded the configured size limit",
                        provider=self._name,
                        attempts=attempt,
                    ) from error
                if not isinstance(error, (OSError, URLError, TimeoutError)):
                    raise
                timed_out = is_timeout_error(error)
                if attempt < self._policy.max_attempts:
                    self._sleep_before_retry(attempt=attempt, response=None)
                    continue
                error_type = (
                    ProviderTimeoutError if timed_out else ProviderConnectionError
                )
                message = (
                    "request timed out"
                    if timed_out
                    else "could not connect to the provider"
                )
                raise error_type(
                    message,
                    provider=self._name,
                    retryable=True,
                    attempts=attempt,
                ) from error

            if 200 <= response.status < 300:
                return response, attempt
            if (
                response.status in _RETRYABLE_STATUSES
                and attempt < self._policy.max_attempts
            ):
                self._sleep_before_retry(attempt=attempt, response=response)
                continue
            self._raise_http_error(response, attempts=attempt)

        # The loop always returns or raises. This guards future policy changes.
        raise ProviderConnectionError(
            "could not connect to the provider",
            provider=self._name,
            retryable=True,
            attempts=self._policy.max_attempts,
        ) from None

    def _sleep_before_retry(
        self,
        *,
        attempt: int,
        response: HttpResponse | None,
    ) -> None:
        retry_after = None
        if response is not None:
            retry_after = retry_after_seconds(
                response.headers,
                maximum=self._policy.max_retry_after_seconds,
            )
        delay = (
            retry_after
            if retry_after is not None
            else min(
                self._policy.backoff_seconds * (2 ** (attempt - 1)),
                self._policy.max_backoff_seconds,
            )
        )
        if delay > 0:
            time.sleep(delay)

    def _raise_http_error(self, response: HttpResponse, *, attempts: int) -> None:
        detail = response_error_detail(
            response.body,
            secrets=self._secrets,
        )
        message = f"request failed with status {response.status}: {detail}"
        if response.status in {401, 403}:
            raise ProviderAuthError(
                message,
                provider=self._name,
                status_code=response.status,
                attempts=attempts,
            )
        if response.status == 429:
            raise ProviderRateLimitError(
                message,
                provider=self._name,
                status_code=response.status,
                retryable=True,
                attempts=attempts,
            )
        raise ProviderResponseError(
            message,
            provider=self._name,
            status_code=response.status,
            retryable=response.status in _RETRYABLE_STATUSES,
            attempts=attempts,
        )

    def _parse_generation(
        self,
        response: HttpResponse,
        *,
        request: GenerationRequest,
        latency_seconds: float,
        attempts: int,
    ) -> GenerationResult:
        decoded = decode_json_object(response.body)
        choices = decoded["choices"]
        if type(choices) is not list or not choices:
            raise ValueError("choices must be a non-empty list")
        choice = choices[0]
        if not isinstance(choice, Mapping):
            raise TypeError("choice must be an object")
        message = choice["message"]
        if not isinstance(message, Mapping):
            raise TypeError("message must be an object")
        text = _extract_text(message.get("content"))

        finish_reason = choice.get("finish_reason")
        if finish_reason is not None and type(finish_reason) is not str:
            raise TypeError("finish_reason must be a string or null")
        response_model = decoded.get("model")
        if response_model is not None and type(response_model) is not str:
            raise TypeError("model must be a string or null")
        response_id = decoded.get("id")
        if response_id is not None and type(response_id) is not str:
            raise TypeError("id must be a string or null")
        if response_id is None:
            response_id = _header(response.headers, "x-request-id")

        metadata = {
            key: decoded[key]
            for key in _RESULT_METADATA_FIELDS
            if key in decoded and decoded[key] is not None
        }
        return GenerationResult(
            text=text,
            provider=self._name,
            model=request.model,
            response_model=response_model,
            finish_reason=finish_reason,
            usage=_parse_usage(decoded.get("usage")),
            latency_seconds=latency_seconds,
            attempts=attempts,
            response_id=response_id,
            metadata=metadata,
        )


def _header(headers: Mapping[str, str], name: str) -> str | None:
    for key, value in headers.items():
        if key.lower() == name:
            return value
    return None


def _extract_text(content: object) -> str:
    if type(content) is str:
        return content
    if type(content) is list:
        parts: list[str] = []
        for part in content:
            if not isinstance(part, Mapping):
                raise TypeError("content parts must be objects")
            part_type = part.get("type")
            text = part.get("text")
            if part_type not in {"text", "output_text"} or type(text) is not str:
                raise TypeError("content parts must contain text")
            parts.append(text)
        return "".join(parts)
    raise TypeError("message content must be text")


def _parse_usage(value: object) -> TokenUsage:
    if value is None:
        return TokenUsage()
    if not isinstance(value, Mapping):
        raise TypeError("usage must be an object")

    prompt_details = value.get("prompt_tokens_details")
    completion_details = value.get("completion_tokens_details")
    cached_tokens = None
    reasoning_tokens = None
    if isinstance(prompt_details, Mapping):
        cached_tokens = prompt_details.get("cached_tokens")
    if isinstance(completion_details, Mapping):
        reasoning_tokens = completion_details.get("reasoning_tokens")
    return TokenUsage(
        input_tokens=_usage_count(value.get("prompt_tokens"), "prompt_tokens"),
        output_tokens=_usage_count(
            value.get("completion_tokens"),
            "completion_tokens",
        ),
        total_tokens=_usage_count(value.get("total_tokens"), "total_tokens"),
        cached_input_tokens=_usage_count(cached_tokens, "cached_tokens"),
        reasoning_tokens=_usage_count(reasoning_tokens, "reasoning_tokens"),
    )


def _usage_count(value: object, field_name: str) -> int | None:
    if value is None:
        return None
    if type(value) is not int or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")
    return value
