"""Copilot Agent Tasks provider."""

from __future__ import annotations

import json
import math
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, cast
from urllib.parse import urlsplit, urlunsplit

from .errors import ProviderError
from .http import DeliveryState, HttpResponse, HttpTransport, TransportError
from .models import FailureEnvelope, ModelRecord, TaskHandle, TaskRequest, TaskState
from .provider import AIProvider, ModelDiscovery
from .serialization import JsonMapping, JsonValue, _is_credential_key, thaw_json

_API_VERSION = "2026-03-10"
_SEGMENT_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")
_TASK_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
_HOST_LABEL_RE = re.compile(r"^[A-Za-z0-9-]{1,63}$")
_HEADER_NAME_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
_MAX_JSON_DEPTH = 64
_UNREADABLE_JSON_VALUE = "<unreadable>"
_TASK_STATES = frozenset(
    {
        "queued",
        "in_progress",
        "completed",
        "failed",
        "idle",
        "waiting_for_user",
        "timed_out",
        "cancelled",
    }
)
_TASK_STATE_ALIASES = {
    "requested": "queued",
    "waiting": "waiting_for_user",
    "running": "in_progress",
}


def _normalize_task_state(value: object) -> object:
    return _TASK_STATE_ALIASES.get(value, value) if isinstance(value, str) else value


def _validate_segment(name: str, value: object) -> str:
    if not isinstance(value, str) or not value or not _SEGMENT_PATTERN.fullmatch(value) or value in {".", ".."}:
        raise ValueError(f"{name} must be a safe non-empty path segment")
    return value


def _validate_base_url(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("base_url must be an absolute HTTPS URL")
    parsed = urlsplit(value)
    try:
        port = parsed.port
        hostname = parsed.hostname
    except ValueError as exc:
        raise ValueError("base_url must be an absolute HTTPS URL") from exc
    if port == 0:
        raise ValueError("base_url must be an absolute HTTPS URL")
    if (
        parsed.scheme != "https"
        or not parsed.netloc
        or not hostname
        or any(ord(char) < 32 or ord(char) == 127 or char.isspace() for char in parsed.netloc)
        or not _is_valid_hostname(hostname)
        or parsed.path not in {"", "/"}
    ):
        raise ValueError("base_url must be an absolute HTTPS URL without a path")
    if parsed.query or parsed.fragment or parsed.username is not None or parsed.password is not None:
        raise ValueError("base_url must not contain credentials, query, or fragment")
    return value.rstrip("/")


def _is_valid_hostname(hostname: str) -> bool:
    if len(hostname) > 253:
        return False
    labels = hostname.split(".")
    return all(
        label and _HOST_LABEL_RE.fullmatch(label) and not label.startswith("-") and not label.endswith("-")
        for label in labels
    )


def _validate_timeout(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError("timeout_seconds must be a positive finite number")
    return float(value)


@dataclass(frozen=True)
class CopilotProviderConfig:
    """Explicit, immutable configuration for :class:`CopilotProvider`."""

    owner: str
    repo: str
    base_url: str
    api_version: str
    timeout_seconds: float
    transport: HttpTransport
    model_discovery: ModelDiscovery
    auth_header_factory: Callable[[], Mapping[str, str]]

    def __post_init__(self) -> None:
        _validate_segment("owner", self.owner)
        _validate_segment("repo", self.repo)
        _validate_base_url(self.base_url)
        if self.api_version != _API_VERSION:
            raise ValueError(f"api_version must be {_API_VERSION}")
        _validate_timeout(self.timeout_seconds)
        if not callable(getattr(self.transport, "request", None)):
            raise ValueError("transport must provide a request() method")
        if not callable(getattr(self.model_discovery, "discover_models", None)):
            raise ValueError("model_discovery must provide discover_models()")
        if not callable(self.auth_header_factory):
            raise ValueError("auth_header_factory must be callable")


def _redact_text(
    value: object,
    headers: Mapping[str, str] | None = None,
    extra_secrets: frozenset[str] | None = None,
) -> str:
    text = str(value)
    secrets = _redaction_secrets(headers)
    if extra_secrets is not None:
        secrets.update(extra_secrets)
    for secret in tuple(secrets):
        if secret.lower().startswith("bearer "):
            bearer_token = secret[7:]
            if bearer_token:
                secrets.add(bearer_token)
    for secret in sorted(secrets, key=len, reverse=True):
        text = text.replace(secret, "<redacted>")
    return re.sub(r"(?i)(bearer\s+)[^\s,;]+", r"\1<redacted>", text)


def _redaction_secrets(
    headers: Mapping[str, str] | None = None,
    payload: object = None,
) -> set[str]:
    secrets: set[str] = set()
    for key, secret in (headers or {}).items():
        if (
            isinstance(key, str)
            and isinstance(secret, str)
            and secret
            and not (key.lower() == "x-github-api-version" and secret == _API_VERSION)
        ):
            secrets.add(secret)
    if payload is not None:
        secrets.update(_credential_payload_secrets(payload))
    return secrets


def _failure(
    category: str,
    message: str,
    *,
    details: Mapping[str, object] | None = None,
    retryable: bool = False,
    headers: Mapping[str, str] | None = None,
    payload_secrets: frozenset[str] | None = None,
) -> FailureEnvelope:
    safe_details: JsonMapping | None = None
    if details is not None:
        safe = _normalize_json_value(details)
        if not isinstance(safe, Mapping):
            safe = {"value": safe}
        details_secrets = frozenset(_credential_payload_secrets(safe))
        effective_secrets = (payload_secrets or frozenset()) | details_secrets
        redacted = cast(Mapping[str, object], _redact_json_strings(safe, headers, effective_secrets))
        safe_details = cast(JsonMapping, dict(redacted))
    return FailureEnvelope(
        category=category,  # type: ignore[arg-type]
        message=message,
        details=safe_details,
        retryable=retryable,
    )


def _safe_json_value(
    value: object,
    _seen: frozenset[int] = frozenset(),
    _remaining_depth: int = _MAX_JSON_DEPTH,
) -> JsonValue:
    """Recursively convert a value into a safe JSON-serializable form.

    Non-finite floats are replaced with their string name (``"inf"``, ``"-inf"``,
    ``"nan"``).  Unsupported leaf types are replaced with a stable
    ``"<TypeName>"`` placeholder so that no arbitrary ``__repr__`` is executed.
    Cyclic container references are replaced with ``"<cycle>"`` and overly deep
    nesting is summarized as ``"<max-depth>"``.
    """
    if _remaining_depth <= 0:
        return "<max-depth>"
    if value is None or isinstance(value, (bool, str)):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else str(value)
    if isinstance(value, Mapping):
        oid = id(value)
        if oid in _seen:
            return "<cycle>"
        seen = _seen | {oid}
        return {
            k if isinstance(k, str) else f"<{type(k).__name__}>": _safe_json_value(v, seen, _remaining_depth - 1)
            for k, v in value.items()
        }
    if isinstance(value, (list, tuple)):
        oid = id(value)
        if oid in _seen:
            return "<cycle>"
        seen = _seen | {oid}
        return [_safe_json_value(v, seen, _remaining_depth - 1) for v in value]
    return f"<{type(value).__name__}>"


def _normalize_json_value(value: object) -> JsonValue:
    try:
        return _safe_json_value(value)
    except RecursionError:
        return "<max-depth>"
    except Exception:
        return _UNREADABLE_JSON_VALUE


def _task_id_alias_values(body: Mapping[str, object]) -> list[object]:
    values: list[object] = []
    for key in ("task_id", "taskId", "id"):
        if key in body:
            values.append(body[key])
    nested = body.get("task")
    if isinstance(nested, Mapping):
        for key in ("task_id", "taskId", "id"):
            if key in nested:
                values.append(nested[key])
    return values


def _conflicting_alias_values(values: list[object]) -> bool:
    if len(values) <= 1:
        return False
    first = values[0]
    return any(candidate != first for candidate in values[1:])


def _redact_json_strings(
    value: object,
    headers: Mapping[str, str] | None = None,
    payload_secrets: frozenset[str] | None = None,
) -> object:
    if isinstance(value, str):
        return _redact_text(value, headers, payload_secrets)
    if (
        payload_secrets is not None
        and isinstance(value, (int, float))
        and not isinstance(value, bool)
        and str(value) in payload_secrets
    ):
        return "<redacted>"
    if isinstance(value, Mapping):
        return {k: _redact_json_strings(v, headers, payload_secrets) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_redact_json_strings(v, headers, payload_secrets) for v in value]
    return value


def _parse_response_body(response: HttpResponse) -> object:
    """Parse the response body without redacting, for structural field extraction.

    Returns the normalized JSON value for JSON bodies, or the raw string for
    non-JSON text bodies.  Never applies redaction so that lifecycle fields
    (state, created_at, error) cannot be corrupted by auth-token collisions.
    """
    body = response.body
    if isinstance(body, str):
        try:
            return _normalize_json_value(json.loads(body))
        except (json.JSONDecodeError, RecursionError, ValueError):
            return body
    return _normalize_json_value(body)


def _string_leaves(
    value: object,
    _seen: frozenset[int] = frozenset(),
    _remaining_depth: int = _MAX_JSON_DEPTH,
) -> set[str]:
    if value is None or _remaining_depth <= 0:
        return set()
    if isinstance(value, str):
        return {value} if value else set()
    if isinstance(value, bool):
        return set()
    if isinstance(value, (int, float)):
        return {str(value)}
    if isinstance(value, Mapping):
        oid = id(value)
        if oid in _seen:
            return set()
        seen = _seen | {oid}
        secrets: set[str] = set()
        for nested in value.values():
            secrets.update(_string_leaves(nested, seen, _remaining_depth - 1))
        return secrets
    if isinstance(value, (list, tuple)):
        oid = id(value)
        if oid in _seen:
            return set()
        seen = _seen | {oid}
        list_secrets: set[str] = set()
        for nested in value:
            list_secrets.update(_string_leaves(nested, seen, _remaining_depth - 1))
        return list_secrets
    return set()


def _is_safe_header_value(value: str) -> bool:
    if value and value[0] in {" ", "\t"}:
        return False
    return all(ord(char) == 9 or 32 <= ord(char) <= 126 or 128 <= ord(char) <= 255 for char in value)


def _credential_payload_secrets(
    value: object,
    _seen: frozenset[int] = frozenset(),
    _remaining_depth: int = _MAX_JSON_DEPTH,
) -> set[str]:
    if value is None or _remaining_depth <= 0:
        return set()
    if isinstance(value, Mapping):
        oid = id(value)
        if oid in _seen:
            return set()
        seen = _seen | {oid}
        secrets: set[str] = set()
        for key, nested in value.items():
            if isinstance(key, str) and _is_credential_key(key):
                secrets.update(_string_leaves(nested, seen, _remaining_depth - 1))
            else:
                secrets.update(_credential_payload_secrets(nested, seen, _remaining_depth - 1))
        return secrets
    if isinstance(value, (list, tuple)):
        oid = id(value)
        if oid in _seen:
            return set()
        seen = _seen | {oid}
        list_secrets: set[str] = set()
        for nested in value:
            list_secrets.update(_credential_payload_secrets(nested, seen, _remaining_depth - 1))
        return list_secrets
    return set()


def _task_id_from_body(body: Mapping[str, object]) -> object:
    values = _task_id_alias_values(body)
    if values:
        return values[0]
    return None


def _created_at(body: Mapping[str, object]) -> str | None:
    for key in ("created_at", "createdAt", "timestamp"):
        value = body.get(key)
        if isinstance(value, str):
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                continue
            return value
    return None


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _has_non_empty_error_field(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, Mapping):
        return bool(value)
    if isinstance(value, (list, tuple, set, frozenset)):
        return bool(value)
    return True


def _non_blank_string(value: object) -> str | None:
    if isinstance(value, str) and value.strip():
        return value
    return None


class CopilotProvider(AIProvider):
    """Create and retrieve GitHub Agent Tasks through one provider boundary."""

    def __init__(self, config: CopilotProviderConfig) -> None:
        if not isinstance(config, CopilotProviderConfig):
            raise ValueError("config must be a CopilotProviderConfig")
        self._config = config
        self._owner = _validate_segment("owner", config.owner)
        self._repo = _validate_segment("repo", config.repo)
        self._base_url = _validate_base_url(config.base_url)
        self._timeout = _validate_timeout(config.timeout_seconds)

    @property
    def provider_name(self) -> str:
        return "copilot"

    def _discover_models(self) -> list[ModelRecord]:
        return self._config.model_discovery.discover_models()

    def _headers(self) -> dict[str, str]:
        raw_headers: object = None
        auth_failed = False
        try:
            raw_headers = self._config.auth_header_factory()
        except Exception:
            auth_failed = True
        if auth_failed:
            raise ProviderError("Authentication header creation failed", category="provider_error")
        if not isinstance(raw_headers, Mapping):
            raise ProviderError("auth_header_factory must return a mapping", category="validation_error")
        unreadable = False
        try:
            headers: dict[str, str] = {}
            for key, value in raw_headers.items():
                if (
                    not isinstance(key, str)
                    or not key
                    or not _HEADER_NAME_RE.fullmatch(key)
                    or not isinstance(value, str)
                    or not _is_safe_header_value(value)
                ):
                    raise ProviderError(
                        "auth_header_factory returned invalid HTTP headers", category="validation_error"
                    )
                if key.lower() == "x-github-api-version":
                    continue
                headers[key] = value
        except ProviderError:
            raise
        except Exception:
            unreadable = True
        if unreadable:
            raise ProviderError("auth_header_factory returned unreadable HTTP headers", category="provider_error")
        headers["X-GitHub-Api-Version"] = _API_VERSION
        return headers

    def _url(self, task_id: str | None = None) -> str:
        path = f"/agents/repos/{self._owner}/{self._repo}/tasks"
        if task_id is not None:
            if not isinstance(task_id, str) or not _TASK_ID_PATTERN.fullmatch(task_id):
                raise ValueError("task_id must be a safe non-empty path segment")
            path += f"/{task_id}"
        parsed = urlsplit(self._base_url)
        return urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))

    @staticmethod
    def _request_body(request: TaskRequest) -> dict[str, object]:
        return {
            "model": request.model_id,
            "prompt": request.prompt,
            "context": request.context,
            "parameters": thaw_json(request.parameters),
            "metadata": thaw_json(request.metadata) if request.metadata is not None else None,
        }

    def _create_task(self, request: TaskRequest) -> TaskHandle:
        if not request.prompt:
            return TaskHandle(
                task_id=None,
                state=None,
                failure=_failure("validation_error", "prompt must be a non-empty string"),
                metadata={},
            )
        headers: Mapping[str, str] = {}
        payload = self._request_body(request)
        payload_secrets = frozenset(_credential_payload_secrets(payload))
        response: object
        for attempt in range(2):  # pragma: no branch - attempt 0 always executes
            try:
                headers = self._headers()
            except ProviderError as exc:
                return TaskHandle(
                    task_id=None,
                    state=None,
                    failure=_failure(exc.category, _redact_text(exc)),
                    metadata={},
                )
            try:
                response = self._config.transport.request(
                    "POST",
                    self._url(),
                    headers=headers,
                    json_body=payload,
                    timeout=self._timeout,
                )
            except TransportError as exc:
                if attempt == 0 and exc.delivery_state is DeliveryState.NOT_DELIVERED and exc.retryable:
                    continue
                return TaskHandle(
                    task_id=None,
                    state=None,
                    failure=_failure(
                        "transport_error",
                        "Transport request failed",
                        details=exc.details,
                        retryable=exc.retryable and attempt == 0,
                        headers=headers,
                        payload_secrets=payload_secrets,
                    ),
                    metadata={},
                )
            except Exception as exc:
                return TaskHandle(
                    task_id=None,
                    state=None,
                    failure=_failure(
                        "transport_error",
                        "Transport request raised an unexpected exception",
                        details={"exception_type": type(exc).__name__},
                        headers=headers,
                        payload_secrets=payload_secrets,
                    ),
                    metadata={},
                )
            break
        if (
            not isinstance(response, HttpResponse)
            or not isinstance(response.status_code, int)
            or isinstance(response.status_code, bool)
        ):
            return TaskHandle(
                task_id=None,
                state=None,
                failure=_failure("logic_error", "Transport returned an invalid response"),
                metadata={},
            )
        if response.delivery_state is not DeliveryState.DELIVERED:
            return TaskHandle(
                task_id=None,
                state=None,
                failure=_failure("logic_error", "Transport returned an unconfirmed delivery state"),
                metadata={},
            )
        raw_body = _parse_response_body(response)
        response_secrets = frozenset(_credential_payload_secrets(raw_body))
        payload_secrets = frozenset({*payload_secrets, *response_secrets})
        if not 200 <= response.status_code < 300:
            return TaskHandle(
                task_id=None,
                state=None,
                failure=_failure(
                    "provider_error",
                    f"Agent Task creation failed with HTTP {response.status_code}",
                    details={"status_code": response.status_code, "response": raw_body},
                    retryable=False,
                    headers=headers,
                    payload_secrets=payload_secrets,
                ),
                metadata={},
            )
        if not isinstance(raw_body, Mapping):
            return TaskHandle(
                task_id=None,
                state=None,
                failure=_failure("provider_error", "Agent Task creation response was not a JSON object"),
                metadata={},
            )
        state_value = raw_body.get("state")
        status_value = raw_body.get("status")
        if ("state" in raw_body and state_value is None) or ("status" in raw_body and status_value is None):
            safe_body = cast(JsonMapping, _redact_json_strings(raw_body, headers, payload_secrets))
            return TaskHandle(
                task_id=None,
                state=None,
                failure=_failure(
                    "provider_error",
                    "Agent Task creation response contained an invalid lifecycle field",
                    details={"response": safe_body},
                    headers=headers,
                    payload_secrets=payload_secrets,
                ),
                metadata={"response": safe_body},
            )
        normalized_state_value = _normalize_task_state(state_value)
        normalized_status_value = _normalize_task_state(status_value)
        if (
            normalized_state_value is not None
            and normalized_status_value is not None
            and normalized_state_value != normalized_status_value
        ):
            safe_body = cast(JsonMapping, _redact_json_strings(raw_body, headers, payload_secrets))
            return TaskHandle(
                task_id=None,
                state=None,
                failure=_failure(
                    "provider_error",
                    "Agent Task creation response contained conflicting state fields",
                    details={"response": safe_body},
                    headers=headers,
                    payload_secrets=payload_secrets,
                ),
                metadata={"response": safe_body},
            )
        lifecycle_state = normalized_state_value if normalized_state_value is not None else normalized_status_value
        if lifecycle_state is not None and (
            not isinstance(lifecycle_state, str) or lifecycle_state not in _TASK_STATES
        ):
            safe_body = cast(JsonMapping, _redact_json_strings(raw_body, headers, payload_secrets))
            return TaskHandle(
                task_id=None,
                state=None,
                failure=_failure(
                    "provider_error",
                    "Agent Task creation response contained an unknown state",
                    details={"response": safe_body},
                    headers=headers,
                    payload_secrets=payload_secrets,
                ),
                metadata={"response": safe_body},
            )
        error_value = raw_body.get("error")
        if lifecycle_state != "failed" and _has_non_empty_error_field(error_value):
            safe_body = cast(JsonMapping, _redact_json_strings(raw_body, headers, payload_secrets))
            return TaskHandle(
                task_id=None,
                state=None,
                failure=_failure(
                    "provider_error",
                    "Agent Task creation response contained conflicting state and error fields",
                    details={"response": safe_body},
                    headers=headers,
                    payload_secrets=payload_secrets,
                ),
                metadata={"response": safe_body},
            )
        safe_body = cast(JsonMapping, _redact_json_strings(raw_body, headers, payload_secrets))
        response_task_ids = _task_id_alias_values(raw_body)
        if _conflicting_alias_values(response_task_ids):
            return TaskHandle(
                task_id=None,
                state=None,
                failure=_failure(
                    "provider_error",
                    "Agent Task creation response contained conflicting task id fields",
                    details={"response": safe_body},
                    headers=headers,
                    payload_secrets=payload_secrets,
                ),
                metadata={"response": safe_body},
            )
        task_id_value = _task_id_from_body(raw_body)
        if task_id_value is not None and (
            not isinstance(task_id_value, str) or not _TASK_ID_PATTERN.fullmatch(task_id_value)
        ):
            return TaskHandle(
                task_id=None,
                state=None,
                failure=_failure("provider_error", "Agent Task creation response did not contain a valid task id"),
                metadata={"response": safe_body},
            )
        if lifecycle_state == "failed":
            message = (
                _non_blank_string(error_value) or _non_blank_string(raw_body.get("message")) or "Agent Task failed"
            )
            return TaskHandle(
                task_id=cast(str | None, task_id_value),
                state=None,
                failure=_failure(
                    "provider_error",
                    _redact_text(message, headers, payload_secrets),
                    details={"response": safe_body},
                    headers=headers,
                    payload_secrets=payload_secrets,
                ),
                metadata={"response": safe_body},
            )
        if task_id_value is None:
            return TaskHandle(
                task_id=None,
                state=None,
                failure=_failure("provider_error", "Agent Task creation response did not contain a valid task id"),
                metadata={"response": safe_body},
            )
        return TaskHandle(task_id=task_id_value, state=None, failure=None, metadata=safe_body)

    def _failed_state(
        self,
        failure: FailureEnvelope,
        task_id: str,
        body: object = None,
        headers: Mapping[str, str] | None = None,
        payload_secrets: frozenset[str] | None = None,
    ) -> TaskState:
        safe_body = (
            _redact_json_strings(_normalize_json_value(body), headers, payload_secrets) if body is not None else None
        )
        metadata_value: dict[str, object] = {"task_id": task_id}
        if safe_body is not None:
            metadata_value["response"] = safe_body
        metadata = cast(JsonMapping, metadata_value)
        return TaskState(state=None, failure=failure, created_at=_now_iso(), metadata=metadata)

    def _get_task(self, task_id: str) -> TaskState:
        try:
            headers = self._headers()
        except ProviderError as exc:
            return self._failed_state(_failure(exc.category, _redact_text(exc)), task_id)
        try:
            response = self._config.transport.request(
                "GET",
                self._url(task_id),
                headers=headers,
                json_body=None,
                timeout=self._timeout,
            )
        except TransportError as exc:
            return self._failed_state(
                _failure(
                    "transport_error",
                    "Transport request failed",
                    details=exc.details,
                    retryable=exc.retryable,
                    headers=headers,
                ),
                task_id,
            )
        except Exception as exc:
            return self._failed_state(
                _failure(
                    "transport_error",
                    "Transport request raised an unexpected exception",
                    details={"exception_type": type(exc).__name__},
                    headers=headers,
                ),
                task_id,
            )
        if (
            not isinstance(response, HttpResponse)
            or not isinstance(response.status_code, int)
            or isinstance(response.status_code, bool)
        ):
            return self._failed_state(_failure("logic_error", "Transport returned an invalid response"), task_id)
        if response.delivery_state is not DeliveryState.DELIVERED:
            return self._failed_state(
                _failure("logic_error", "Transport returned an unconfirmed delivery state"), task_id
            )
        raw_body = _parse_response_body(response)
        payload_secrets = frozenset(_credential_payload_secrets(raw_body))
        if not 200 <= response.status_code < 300:
            return self._failed_state(
                _failure(
                    "provider_error",
                    f"Agent Task retrieval failed with HTTP {response.status_code}",
                    details={"status_code": response.status_code, "response": raw_body},
                    headers=headers,
                    payload_secrets=payload_secrets,
                ),
                task_id,
                raw_body,
                headers,
                payload_secrets,
            )
        if not isinstance(raw_body, Mapping):
            return self._failed_state(
                _failure("provider_error", "Agent Task response was not a JSON object"),
                task_id,
                raw_body,
                headers,
                payload_secrets,
            )
        state_value = raw_body.get("state")
        status_value = raw_body.get("status")
        if ("state" in raw_body and state_value is None) or ("status" in raw_body and status_value is None):
            return self._failed_state(
                _failure(
                    "provider_error",
                    "Agent Task response contained an invalid lifecycle field",
                    payload_secrets=payload_secrets,
                ),
                task_id,
                raw_body,
                headers,
                payload_secrets,
            )
        normalized_state_value = _normalize_task_state(state_value)
        normalized_status_value = _normalize_task_state(status_value)
        if (
            normalized_state_value is not None
            and normalized_status_value is not None
            and normalized_state_value != normalized_status_value
        ):
            return self._failed_state(
                _failure(
                    "provider_error",
                    "Agent Task response contained conflicting state fields",
                    payload_secrets=payload_secrets,
                ),
                task_id,
                raw_body,
                headers,
                payload_secrets,
            )
        state = normalized_state_value if normalized_state_value is not None else normalized_status_value
        if not isinstance(state, str) or state not in _TASK_STATES:
            return self._failed_state(
                _failure(
                    "provider_error", "Agent Task response contained an unknown state", payload_secrets=payload_secrets
                ),
                task_id,
                raw_body,
                headers,
                payload_secrets,
            )
        created_at = _created_at(raw_body)
        if created_at is None:
            return self._failed_state(
                _failure(
                    "provider_error",
                    "Agent Task response lacked a valid created_at",
                    payload_secrets=payload_secrets,
                ),
                task_id,
                raw_body,
                headers,
                payload_secrets,
            )
        remote_error = raw_body.get("error")
        if state != "failed" and _has_non_empty_error_field(remote_error):
            return self._failed_state(
                _failure(
                    "provider_error",
                    "Agent Task response contained conflicting state and error fields",
                    payload_secrets=payload_secrets,
                ),
                task_id,
                raw_body,
                headers,
                payload_secrets,
            )
        response_task_ids = _task_id_alias_values(raw_body)
        if _conflicting_alias_values(response_task_ids):
            return self._failed_state(
                _failure(
                    "provider_error",
                    "Agent Task response contained conflicting task id fields",
                    payload_secrets=payload_secrets,
                ),
                task_id,
                raw_body,
                headers,
                payload_secrets,
            )
        if any(candidate != task_id for candidate in response_task_ids):
            return self._failed_state(
                _failure(
                    "provider_error",
                    "Agent Task response task id did not match requested task id",
                    payload_secrets=payload_secrets,
                ),
                task_id,
                raw_body,
                headers,
                payload_secrets,
            )
        safe_body = cast(Mapping[str, object], _redact_json_strings(raw_body, headers, payload_secrets))
        failure = None
        if state == "failed":
            message = (
                _non_blank_string(remote_error) or _non_blank_string(raw_body.get("message")) or "Agent Task failed"
            )
            failure = _failure(
                "provider_error",
                _redact_text(message, headers, payload_secrets),
                details={"response": safe_body},
                headers=headers,
                payload_secrets=payload_secrets,
            )
        try:
            metadata = dict(safe_body)
            metadata["task_id"] = task_id
            return TaskState(
                state=cast(Any, state),
                failure=failure,
                created_at=created_at,
                metadata=cast(JsonMapping, metadata),
            )
        except ValueError as exc:
            return self._failed_state(
                _failure("provider_error", _redact_text(exc, headers, payload_secrets)),
                task_id,
                raw_body,
                headers,
                payload_secrets,
            )


__all__ = ["CopilotProvider", "CopilotProviderConfig"]
