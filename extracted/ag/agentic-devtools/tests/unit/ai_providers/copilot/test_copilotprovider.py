import json
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path
from typing import Any, cast

import pytest

from agentic_devtools.ai_providers import (
    AIProvider,
    CopilotProvider,
    CopilotProviderConfig,
    DeliveryState,
    HttpResponse,
    ModelDiscovery,
    ModelRecord,
    ProviderError,
    TaskRequest,
    TaskState,
    TransportError,
)
from agentic_devtools.ai_providers import copilot as copilot_module

_FIXTURE_ROOT = Path(__file__).resolve().parents[3] / "fixtures" / "ai_providers" / "copilot"


def _fixture(name: str) -> Any:
    return json.loads((_FIXTURE_ROOT / name).read_text(encoding="utf-8"))


_CREATE_TASK_FIXTURES = cast(dict[str, Any], _fixture("create_task_responses.json"))
_GET_TASK_FIXTURES = cast(dict[str, Any], _fixture("get_task_responses.json"))
_TRANSPORT_CASES = cast(dict[str, Any], _fixture("transport_cases.json"))


def _delivery_state(name: str) -> DeliveryState:
    return DeliveryState[name.upper()]


def _transport_exception(case: Mapping[str, object]) -> BaseException:
    if case["kind"] == "runtime_error":
        return RuntimeError(cast(str, case["message"]))
    return TransportError(
        cast(str, case["message"]),
        delivery_state=_delivery_state(cast(str, case["delivery_state"])),
    )


class FakeTransport:
    def __init__(self, responses: list[object]) -> None:
        self.responses = list(responses)
        self.calls: list[dict[str, Any]] = []

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        json_body: Mapping[str, Any] | None,
        timeout: float,
    ) -> HttpResponse:
        self.calls.append(
            {
                "method": method,
                "url": url,
                "headers": dict(headers),
                "json_body": json_body,
                "timeout": timeout,
            }
        )
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return cast(HttpResponse, response)


class FakeDiscovery(ModelDiscovery):
    def __init__(self) -> None:
        self.calls = 0

    def _discover_models(self) -> list[ModelRecord]:
        self.calls += 1
        return []


def _config(transport: FakeTransport, discovery: ModelDiscovery | None = None, auth=None) -> CopilotProviderConfig:
    return CopilotProviderConfig(
        owner="octo",
        repo="demo",
        base_url="https://api.github.com",
        api_version="2026-03-10",
        timeout_seconds=3.5,
        transport=transport,
        model_discovery=discovery or FakeDiscovery(),
        auth_header_factory=auth or (lambda: {"Authorization": "******"}),
    )


def _request() -> TaskRequest:
    return TaskRequest(
        model_id="gpt-5-mini",
        prompt="repair this",
        context="context",
        parameters={"nested": ["value"]},
        metadata={"request_id": "fixture"},
    )


def _delivered_response(status_code: int, body: object) -> HttpResponse:
    return HttpResponse(status_code, body, DeliveryState.DELIVERED)


def test_provider_is_explicit_and_discovery_is_delegated_once() -> None:
    transport = FakeTransport([])
    discovery = FakeDiscovery()
    provider = CopilotProvider(_config(transport, discovery))

    assert isinstance(provider, AIProvider)
    assert provider.provider_name == "copilot"
    assert provider.discover_models() == []
    assert discovery.calls == 1
    assert transport.calls == []


def test_create_uses_one_safe_route_and_lazy_auth() -> None:
    accepted = cast(Mapping[str, object], _CREATE_TASK_FIXTURES["accepted"])
    transport = FakeTransport([_delivered_response(cast(int, accepted["status_code"]), accepted["body"])])
    auth_calls: list[bool] = []

    def auth() -> dict[str, str]:
        auth_calls.append(True)
        return {"Authorization": "******"}

    provider = CopilotProvider(_config(transport, auth=auth))

    assert auth_calls == []
    handle = provider.create_task(_request())

    assert handle.task_id == "fixture-task-1"
    assert handle.failure is None
    assert len(transport.calls) == 1
    assert auth_calls == [True]
    call = transport.calls[0]
    assert call["method"] == "POST"
    assert call["url"] == "https://api.github.com/agents/repos/octo/demo/tasks"
    assert call["headers"] == {
        "Authorization": "******",
        "X-GitHub-Api-Version": "2026-03-10",
    }
    assert call["timeout"] == 3.5
    assert call["json_body"]["prompt"] == "repair this"
    assert call["json_body"]["model"] == "gpt-5-mini"


def test_create_rejects_empty_prompt_before_auth_or_transport() -> None:
    transport = FakeTransport([])
    auth_calls: list[bool] = []

    def auth() -> dict[str, str]:
        auth_calls.append(True)
        return {}

    provider = CopilotProvider(_config(transport, auth=auth))
    request = replace(_request(), prompt="")

    result = provider.create_task(request)

    assert result.failure is not None
    assert result.failure.category == "validation_error"
    assert auth_calls == []
    assert transport.calls == []


def test_create_retries_only_proven_non_delivery() -> None:
    transport = FakeTransport(
        [
            TransportError(
                "not delivered",
                delivery_state=DeliveryState.NOT_DELIVERED,
                retryable=True,
            ),
            _delivered_response(202, {"task_id": "task-2"}),
        ]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id == "task-2"
    assert len(transport.calls) == 2


@pytest.mark.parametrize(
    "error",
    [_transport_exception(case) for case in _TRANSPORT_CASES["create_unproven_failures"]],
    ids=[case["name"] for case in _TRANSPORT_CASES["create_unproven_failures"]],
)
def test_create_does_not_retry_unproven_failures(error: BaseException) -> None:
    transport = FakeTransport([error])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id is None
    assert result.failure is not None
    assert len(transport.calls) == 1


def test_create_refreshes_auth_headers_before_retry() -> None:
    transport = FakeTransport(
        [
            TransportError("not delivered", delivery_state=DeliveryState.NOT_DELIVERED, retryable=True),
            _delivered_response(202, {"id": "task-2"}),
        ]
    )
    auth_calls = 0

    def auth() -> dict[str, str]:
        nonlocal auth_calls
        auth_calls += 1
        return {"Authorization": f"token-{auth_calls}"}

    provider = CopilotProvider(_config(transport, auth=auth))
    result = provider.create_task(_request())

    assert result.task_id == "task-2"
    assert auth_calls == 2
    assert [call["headers"]["Authorization"] for call in transport.calls] == ["token-1", "token-2"]


@pytest.mark.parametrize(
    "delivery_state",
    [_delivery_state(name) for name in _TRANSPORT_CASES["unconfirmed_delivery_states"]],
    ids=cast(list[str], _TRANSPORT_CASES["unconfirmed_delivery_states"]),
)
def test_create_rejects_unconfirmed_response_delivery(delivery_state: DeliveryState) -> None:
    transport = FakeTransport([HttpResponse(202, {"id": "task-1"}, delivery_state)])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id is None
    assert result.failure is not None
    assert result.failure.category == "logic_error"


def test_get_task_normalizes_state_without_retry() -> None:
    completed = cast(Mapping[str, object], _GET_TASK_FIXTURES["completed"])
    transport = FakeTransport([_delivered_response(cast(int, completed["status_code"]), completed["body"])])
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert isinstance(result, TaskState)
    assert result.state == "completed"
    assert result.failure is None
    assert result.metadata["task_id"] == "task-1"
    assert len(transport.calls) == 1
    assert transport.calls[0]["method"] == "GET"
    assert transport.calls[0]["url"].endswith("/tasks/task-1")


@pytest.mark.parametrize("task_id", ["", "../x", "a/b", "a b", None])
def test_get_task_rejects_unsafe_ids_before_transport(task_id: object) -> None:
    transport = FakeTransport([])
    provider = CopilotProvider(_config(transport))

    with pytest.raises(Exception):
        provider.get_task(task_id)  # type: ignore[arg-type]

    assert transport.calls == []


@pytest.mark.parametrize("task_id", ["../x", "a/b", "a b"])
def test_url_rejects_unsafe_ids_before_construction(task_id: str) -> None:
    provider = CopilotProvider(_config(FakeTransport([])))

    with pytest.raises(ValueError, match="task_id must be a safe non-empty path segment"):
        provider._url(task_id)


def test_malformed_creation_response_is_a_failure_without_retry() -> None:
    transport = FakeTransport([_delivered_response(202, {"status": "queued"})])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id is None
    assert result.failure is not None
    assert len(transport.calls) == 1


@pytest.mark.parametrize("field", ["state", "status"])
def test_creation_rejects_explicit_null_lifecycle_fields(field: str) -> None:
    transport = FakeTransport([_delivered_response(202, {field: None})])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id is None
    assert result.failure is not None
    assert result.failure.message == "Agent Task creation response contained an invalid lifecycle field"


def test_constructor_rejects_wrong_config_type_without_side_effects() -> None:
    with pytest.raises(ValueError, match="CopilotProviderConfig"):
        CopilotProvider(cast(CopilotProviderConfig, object()))


@pytest.mark.parametrize(
    "auth",
    [
        lambda: (_ for _ in ()).throw(RuntimeError("fixture secret")),
        lambda: ["not", "headers"],
        lambda: {"Header\nName": "value"},
        lambda: {"Bad Header": "value"},
        lambda: {"X:Y": "value"},
        lambda: {"": "value"},
        lambda: {"Authorization": "bad\x00token"},
        lambda: {"Authorization": " leading-space-token"},
        lambda: {"Authorization": "snowman \u2603"},
    ],
)
def test_auth_failures_are_local_and_do_not_dispatch(auth: object) -> None:
    transport = FakeTransport([])
    provider = CopilotProvider(_config(transport, auth=cast(Any, auth)))

    result = provider.create_task(_request())

    assert result.failure is not None
    assert transport.calls == []


def test_auth_exception_cause_does_not_retain_secret() -> None:
    secret = "auth-secret"
    transport = FakeTransport([])

    def auth() -> dict[str, str]:
        raise RuntimeError(secret)

    provider = CopilotProvider(_config(transport, auth=auth))

    with pytest.raises(ProviderError) as caught:
        provider._headers()

    assert secret not in str(caught.value)
    assert caught.value.__cause__ is None
    assert caught.value.__context__ is None


def test_auth_header_materialization_failures_are_local_and_do_not_dispatch() -> None:
    class RaisingMapping(Mapping[str, str]):
        def __getitem__(self, key: str) -> str:
            raise RuntimeError("unreadable")

        def __iter__(self):
            raise RuntimeError("unreadable")

        def __len__(self) -> int:
            return 1

        def items(self):
            raise RuntimeError("unreadable")

    transport = FakeTransport([])
    provider = CopilotProvider(_config(transport, auth=lambda: cast(Mapping[str, str], RaisingMapping())))

    result = provider.create_task(_request())

    assert result.failure is not None
    assert result.failure.category == "provider_error"
    assert result.failure.message == "auth_header_factory returned unreadable HTTP headers"
    assert transport.calls == []


def test_auth_header_materialization_exception_cause_does_not_retain_secret() -> None:
    secret = "header-secret"

    class RaisingMapping(Mapping[str, str]):
        def __getitem__(self, key: str) -> str:
            raise RuntimeError(secret)

        def __iter__(self):
            raise RuntimeError(secret)

        def __len__(self) -> int:
            return 1

        def items(self):
            raise RuntimeError(secret)

    provider = CopilotProvider(_config(FakeTransport([]), auth=lambda: RaisingMapping()))

    with pytest.raises(ProviderError) as caught:
        provider._headers()

    assert secret not in str(caught.value)
    assert caught.value.__cause__ is None
    assert caught.value.__context__ is None


def test_blank_bearer_token_does_not_corrupt_redacted_diagnostics() -> None:
    transport = FakeTransport([_delivered_response(500, {"message": "clean diagnostic"})])
    provider = CopilotProvider(_config(transport, auth=lambda: {"Authorization": "Bearer "}))

    result = provider.create_task(_request())

    assert result.failure is not None
    assert result.failure.details is not None
    response_details = cast(Mapping[str, object], result.failure.details["response"])
    assert response_details["message"] == "clean diagnostic"


def test_numeric_credential_payload_values_are_redacted_from_failure_details() -> None:
    transport = FakeTransport([_delivered_response(500, {"message": "credential 123456 leaked"})])
    provider = CopilotProvider(_config(transport))
    request = replace(_request(), parameters={"token": 123456})

    result = provider.create_task(request)

    assert result.failure is not None
    assert result.failure.details is not None
    response_details = cast(Mapping[str, object], result.failure.details["response"])
    assert response_details["message"] == "credential <redacted> leaked"


@pytest.mark.parametrize(
    "response",
    [
        object(),
        HttpResponse("bad", {}, DeliveryState.DELIVERED),  # type: ignore[arg-type]
        HttpResponse(True, {}, DeliveryState.DELIVERED),
        _delivered_response(202, "not json"),
        *[
            _delivered_response(cast(int, case["status_code"]), case["body"])
            for case in _CREATE_TASK_FIXTURES["failure_responses"]
        ],
    ],
)
def test_creation_failures_and_response_shapes_are_fail_closed(response: object) -> None:
    transport = FakeTransport([response])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id is None
    assert result.failure is not None
    assert len(transport.calls) == 1


def test_creation_accepts_nested_task_id() -> None:
    transport = FakeTransport([_delivered_response(202, {"task": {"id": "nested-task"}})])
    provider = CopilotProvider(_config(transport))

    assert provider.create_task(_request()).task_id == "nested-task"


def test_creation_preserves_none_context_and_metadata() -> None:
    transport = FakeTransport([_delivered_response(202, {"id": "minimal-task"})])
    provider = CopilotProvider(_config(transport))
    request = TaskRequest(
        model_id="model",
        prompt="prompt",
        context=None,
        parameters={},
        metadata=None,
    )

    assert provider.create_task(request).task_id == "minimal-task"


def test_creation_accepts_json_text_and_preserves_redacted_metadata() -> None:
    transport = FakeTransport([_delivered_response(202, '{"id": "text-task", "token": "secret"}')])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id == "text-task"
    assert result.metadata["token"] == "<redacted>"


def test_creation_accepts_json_text_with_non_finite_numbers() -> None:
    transport = FakeTransport([_delivered_response(202, '{"id":"text-task","score":NaN}')])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id == "text-task"
    assert result.metadata["score"] == "nan"


def test_creation_normalizes_non_string_mapping_keys_without_stringifying_them() -> None:
    class UnstringifiableKey:
        def __str__(self) -> str:
            raise AssertionError("arbitrary key stringification must not run")

    transport = FakeTransport([_delivered_response(202, {"id": "task-1", UnstringifiableKey(): "value"})])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id == "task-1"
    assert result.metadata["<UnstringifiableKey>"] == "value"


def test_base_url_root_slash_is_normalized() -> None:
    transport = FakeTransport([_delivered_response(202, {"id": "task-root"})])
    provider = CopilotProvider(replace(_config(transport), base_url="https://api.github.com/"))

    assert provider.create_task(_request()).task_id == "task-root"


def test_provider_owned_api_version_overrides_case_insensitive_factory_key() -> None:
    transport = FakeTransport([_delivered_response(202, {"id": "task-1"})])
    provider = CopilotProvider(
        _config(
            transport,
            auth=lambda: {
                "Authorization": "******",
                "x-github-api-version": "1970-01-01",
            },
        )
    )

    result = provider.create_task(_request())

    assert result.task_id == "task-1"
    headers = cast(Mapping[str, str], transport.calls[0]["headers"])
    assert headers["X-GitHub-Api-Version"] == "2026-03-10"
    assert "x-github-api-version" not in headers


def test_bearer_credentials_are_redacted_from_transport_errors() -> None:
    credential = "B" + "earer example-token"
    transport = FakeTransport([RuntimeError(credential)])
    provider = CopilotProvider(_config(transport, auth=lambda: {"Authorization": credential}))

    result = provider.create_task(_request())

    assert result.failure is not None
    assert result.failure.message == "Transport request raised an unexpected exception"
    assert credential not in str(result.failure.details)


def test_transport_error_details_credential_values_are_redacted_from_message() -> None:
    secret = "fixture-transport-token-xyz"
    transport = FakeTransport(
        [
            TransportError(
                "transport failed",
                details={"token": secret, "message": f"auth failed: {secret}"},
            )
        ]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.failure is not None
    assert result.failure.details is not None
    assert secret not in str(result.failure.details)


def test_redaction_replaces_overlapping_credentials_longest_first() -> None:
    transport = FakeTransport([_delivered_response(500, {"message": "abcdef"})])
    provider = CopilotProvider(
        _config(
            transport,
            auth=lambda: {"Authorization": "abc", "Proxy-Authorization": "abcdef"},
        )
    )

    result = provider.create_task(_request())

    assert result.failure is not None
    assert result.failure.details is not None
    response_details = cast(Mapping[str, object], result.failure.details["response"])
    assert response_details["message"] == "<redacted>"


def test_retrieval_converts_task_state_validation_error_to_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    transport = FakeTransport([_delivered_response(200, _fixture("task-completed.json"))])
    provider = CopilotProvider(_config(transport))
    original_task_state = copilot_module.TaskState
    calls = 0

    def raise_validation_error(**kwargs: object) -> Any:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise ValueError("invalid task state")
        return original_task_state(**cast(dict[str, Any], kwargs))

    monkeypatch.setattr(copilot_module, "TaskState", raise_validation_error)
    result = provider.get_task("task-1")

    assert result.state is None
    assert result.failure is not None
    assert result.failure.message == "invalid task state"


def test_retryable_transport_error_retries_once_then_returns_failure() -> None:
    transport = FakeTransport(
        [
            TransportError(
                "not delivered",
                delivery_state=DeliveryState.NOT_DELIVERED,
                retryable=True,
            ),
            object(),
        ]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.failure is not None
    assert len(transport.calls) == 2


def test_retrieval_rejects_conflicting_lifecycle_aliases() -> None:
    transport = FakeTransport(
        [
            _delivered_response(
                200,
                {
                    "state": "completed",
                    "status": "failed",
                    "created_at": "2026-01-01T00:00:00Z",
                },
            )
        ]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.state is None
    assert result.failure is not None
    assert result.failure.category == "provider_error"
    assert result.failure.message == "Agent Task response contained conflicting state fields"


def test_retrieval_rejects_conflicting_non_failed_state_with_error() -> None:
    transport = FakeTransport(
        [
            _delivered_response(
                200,
                {
                    "state": "completed",
                    "created_at": "2026-01-01T00:00:00Z",
                    "error": "should-not-be-present",
                },
            )
        ]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.state is None
    assert result.failure is not None
    assert result.failure.category == "provider_error"
    assert result.failure.message == "Agent Task response contained conflicting state and error fields"


@pytest.mark.parametrize("field", ["state", "status"])
def test_retrieval_rejects_explicit_null_lifecycle_fields(field: str) -> None:
    transport = FakeTransport(
        [
            _delivered_response(
                200,
                {
                    field: None,
                    "created_at": "2026-01-01T00:00:00Z",
                },
            )
        ]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.state is None
    assert result.failure is not None
    assert result.failure.message == "Agent Task response contained an invalid lifecycle field"


def test_retrieval_rejects_mismatched_task_id_aliases() -> None:
    transport = FakeTransport(
        [
            _delivered_response(
                200,
                {
                    "state": "completed",
                    "created_at": "2026-01-01T00:00:00Z",
                    "task_id": "other-task",
                },
            )
        ]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.state is None
    assert result.failure is not None
    assert result.failure.category == "provider_error"
    assert result.failure.message == "Agent Task response task id did not match requested task id"


def test_retrieval_rejects_conflicting_task_id_alias_values() -> None:
    transport = FakeTransport(
        [
            _delivered_response(
                200,
                {
                    "state": "completed",
                    "created_at": "2026-01-01T00:00:00Z",
                    "task_id": "task-a",
                    "id": "task-b",
                },
            )
        ]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.state is None
    assert result.failure is not None
    assert result.failure.category == "provider_error"
    assert result.failure.message == "Agent Task response contained conflicting task id fields"


@pytest.mark.parametrize("error_value", [None, " "])
def test_retrieval_allows_non_failed_state_with_empty_error_field(error_value: object) -> None:
    transport = FakeTransport(
        [
            _delivered_response(
                200,
                {
                    "state": "completed",
                    "created_at": "2026-01-01T00:00:00Z",
                    "error": error_value,
                },
            )
        ]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.state == "completed"
    assert result.failure is None


@pytest.mark.parametrize(
    "response",
    [
        object(),
        HttpResponse("bad", {}, DeliveryState.DELIVERED),  # type: ignore[arg-type]
        HttpResponse(True, {}, DeliveryState.DELIVERED),
        _delivered_response(200, "not json"),
        *[
            _delivered_response(cast(int, case["status_code"]), case["body"])
            for case in _GET_TASK_FIXTURES["failure_responses"]
        ],
    ],
)
def test_retrieval_failures_are_failure_backed_without_retry(response: object) -> None:
    transport = FakeTransport([response])
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.state is None
    assert result.failure is not None
    assert result.metadata["task_id"] == "task-1"
    assert len(transport.calls) == 1


def test_retrieval_supports_aliases_and_failed_lifecycle_state() -> None:
    transport = FakeTransport(
        [
            HttpResponse(
                200,
                {
                    "status": "failed",
                    "createdAt": "2026-01-01T00:00:00Z",
                    "message": "fixture failure",
                },
                DeliveryState.DELIVERED,
            )
        ]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.state == "failed"
    assert result.failure is not None
    assert result.failure.message == "fixture failure"


@pytest.mark.parametrize(
    ("provider_status", "expected_state"),
    [(case["provider_status"], case["expected_state"]) for case in _GET_TASK_FIXTURES["state_aliases"]],
    ids=[cast(str, case["provider_status"]) for case in _GET_TASK_FIXTURES["state_aliases"]],
)
def test_retrieval_normalizes_provider_native_active_statuses(provider_status: str, expected_state: str) -> None:
    transport = FakeTransport(
        [_delivered_response(200, {"status": provider_status, "created_at": "2026-01-01T00:00:00Z"})]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.state == expected_state


@pytest.mark.parametrize(
    "delivery_state",
    [_delivery_state(name) for name in _TRANSPORT_CASES["unconfirmed_delivery_states"]],
    ids=cast(list[str], _TRANSPORT_CASES["unconfirmed_delivery_states"]),
)
def test_retrieval_rejects_unconfirmed_response_delivery(delivery_state: DeliveryState) -> None:
    transport = FakeTransport(
        [HttpResponse(200, {"state": "completed", "created_at": "2026-01-01T00:00:00Z"}, delivery_state)]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.state is None
    assert result.failure is not None
    assert result.failure.category == "logic_error"


def test_failed_task_structured_error_is_not_stringified_into_message() -> None:
    transport = FakeTransport(
        [
            HttpResponse(
                200,
                {
                    "state": "failed",
                    "created_at": "2026-01-01T00:00:00Z",
                    "error": {"token": "remote-secret"},
                },
                DeliveryState.DELIVERED,
            )
        ]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.failure is not None
    assert result.failure.message == "Agent Task failed"
    assert result.failure.details is not None
    assert "remote-secret" not in str(result.failure.details)
    assert "<redacted>" in str(result.failure.details)


def test_failed_task_ignores_whitespace_error_and_uses_message_alias() -> None:
    transport = FakeTransport(
        [
            _delivered_response(
                200,
                {
                    "state": "failed",
                    "created_at": "2026-01-01T00:00:00Z",
                    "error": "   ",
                    "message": "fixture failure",
                },
            )
        ]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.failure is not None
    assert result.failure.message == "fixture failure"


@pytest.mark.parametrize("error", [TransportError("transport"), RuntimeError("unclassified")])
def test_retrieval_transport_failures_are_failure_backed(error: BaseException) -> None:
    transport = FakeTransport([error])
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.state is None
    assert result.failure is not None


def test_create_unclassified_transport_error_uses_stable_message() -> None:
    transport = FakeTransport([RuntimeError("payload-secret")])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.failure is not None
    assert result.failure.message == "Transport request raised an unexpected exception"
    assert result.failure.details == {"exception_type": "RuntimeError"}


def test_get_task_unclassified_transport_error_uses_stable_message() -> None:
    transport = FakeTransport([RuntimeError("payload-secret")])
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.failure is not None
    assert result.failure.message == "Transport request raised an unexpected exception"
    assert result.failure.details == {"exception_type": "RuntimeError"}


def test_retrieval_auth_failure_is_failure_backed() -> None:
    transport = FakeTransport([])
    provider = CopilotProvider(_config(transport, auth=lambda: 42))

    result = provider.get_task("task-1")

    assert result.state is None
    assert result.failure is not None
    assert transport.calls == []


def test_transport_failure_is_redacted() -> None:
    credential = "fixture-secret"
    transport = FakeTransport([TransportError(credential)])
    provider = CopilotProvider(_config(transport, auth=lambda: {"Authorization": credential}))

    result = provider.create_task(_request())

    assert result.failure is not None
    assert result.failure.message == "Transport request failed"
    assert credential not in result.failure.message


def test_retrieval_transport_failure_uses_stable_message_and_retains_task_id() -> None:
    transport = FakeTransport([TransportError("payload-secret")])
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.failure is not None
    assert result.failure.message == "Transport request failed"
    assert result.metadata["task_id"] == "task-1"


def test_response_diagnostics_redact_auth_values_in_ordinary_fields() -> None:
    credential = "fixture-secret"
    transport = FakeTransport([_delivered_response(500, {"message": credential})])
    provider = CopilotProvider(_config(transport, auth=lambda: {"Authorization": credential}))

    result = provider.create_task(_request())

    assert result.failure is not None
    assert result.failure.details is not None
    response_details = cast(Mapping[str, object], result.failure.details["response"])
    assert response_details["message"] == "<redacted>"


def test_response_diagnostics_redact_payload_credentials_echoed_by_provider() -> None:
    credential = "payload-secret"
    transport = FakeTransport([_delivered_response(500, {"message": f"invalid token {credential}"})])
    provider = CopilotProvider(_config(transport))
    request = replace(_request(), parameters={"token": credential})

    result = provider.create_task(request)

    assert result.failure is not None
    assert result.failure.details is not None
    response_details = cast(Mapping[str, object], result.failure.details["response"])
    assert response_details["message"] == "invalid token <redacted>"


def test_response_diagnostics_redact_response_credential_values_echoed_in_plain_fields() -> None:
    transport = FakeTransport([_delivered_response(500, {"token": "remote-secret", "message": "remote-secret"})])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.failure is not None
    assert result.failure.details is not None
    response_details = cast(Mapping[str, object], result.failure.details["response"])
    assert response_details["token"] == "<redacted>"
    assert response_details["message"] == "<redacted>"


def test_failed_task_metadata_redacts_auth_values_in_ordinary_fields() -> None:
    credential = "fixture-secret"
    transport = FakeTransport(
        [
            _delivered_response(
                200,
                {"state": "failed", "created_at": "2026-01-01T00:00:00Z", "message": credential},
            )
        ]
    )
    provider = CopilotProvider(_config(transport, auth=lambda: {"Authorization": credential}))

    result = provider.get_task("task-1")

    assert cast(Mapping[str, object], result.metadata)["message"] == "<redacted>"
    assert result.failure is not None
    assert result.failure.message == "<redacted>"


def test_failed_task_redacts_response_credential_values_echoed_in_plain_fields() -> None:
    transport = FakeTransport(
        [
            _delivered_response(
                200,
                {
                    "state": "failed",
                    "created_at": "2026-01-01T00:00:00Z",
                    "token": "remote-secret",
                    "message": "remote-secret",
                },
            )
        ]
    )
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.failure is not None
    assert result.failure.message == "<redacted>"
    metadata = cast(Mapping[str, object], result.metadata)
    assert metadata["token"] == "<redacted>"
    assert metadata["message"] == "<redacted>"


def test_retrieval_state_field_is_not_corrupted_by_auth_token_collision() -> None:
    # An auth token that equals a valid lifecycle state string must not corrupt
    # the state field via redaction.  Structural fields must be read from the
    # unredacted body before any redaction is applied.
    credential = "completed"
    transport = FakeTransport(
        [
            _delivered_response(
                200,
                {"state": credential, "created_at": "2026-01-01T00:00:00Z"},
            )
        ]
    )
    provider = CopilotProvider(_config(transport, auth=lambda: {"Authorization": credential}))

    result = provider.get_task("task-1")

    assert result.state == "completed"
    assert result.failure is None


def test_creation_task_id_field_is_not_corrupted_by_auth_token_collision() -> None:
    # An auth token that equals the returned task id must not corrupt the id
    # via redaction so that a successful creation is incorrectly rejected.
    credential = "task-1"
    transport = FakeTransport([_delivered_response(202, {"id": credential})])
    provider = CopilotProvider(_config(transport, auth=lambda: {"Authorization": credential}))

    result = provider.create_task(_request())

    assert result.task_id == "task-1"
    assert result.failure is None


def test_creation_failed_state_preserves_valid_remote_task_id() -> None:
    transport = FakeTransport([_delivered_response(202, {"state": "failed", "id": "task-1", "message": "boom"})])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id == "task-1"
    assert result.failure is not None
    assert result.failure.message == "boom"


def test_creation_metadata_redacts_auth_token_even_when_it_matches_task_id() -> None:
    credential = "task-1"
    transport = FakeTransport([_delivered_response(202, {"id": credential, "extra": credential})])
    provider = CopilotProvider(_config(transport, auth=lambda: {"Authorization": credential}))

    result = provider.create_task(_request())

    assert result.task_id == "task-1"
    assert cast(Mapping[str, object], result.metadata)["extra"] == "<redacted>"


def test_malformed_transport_details_are_safely_normalized() -> None:
    transport = FakeTransport([TransportError("transport", details={"value": object()})])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.failure is not None
    assert result.failure.details is not None
    assert isinstance(result.failure.details["value"], str)


def test_unreadable_nested_transport_details_are_failure_backed() -> None:
    class RaisingMapping(Mapping[str, object]):
        def __getitem__(self, key: str) -> object:
            raise RuntimeError("unreadable")

        def __iter__(self):
            raise RuntimeError("unreadable")

        def __len__(self) -> int:
            return 1

    transport = FakeTransport([TransportError("transport", details={"nested": RaisingMapping()})])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.failure is not None
    assert result.failure.details == {"value": "<unreadable>"}


def test_create_list_body_covers_parse_and_redact_list_branch() -> None:
    # A 500 response whose body is a JSON array covers the list branch of
    # _normalize_json_value and _redact_json_strings in the creation failure path.
    transport = FakeTransport([_delivered_response(500, [{"error": "provider error"}])])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id is None
    assert result.failure is not None


def test_create_non_finite_float_in_body_is_serialized_safely() -> None:
    # A response body containing float("inf") covers the non-finite repr branch
    # of _normalize_json_value in the creation success path.
    transport = FakeTransport([_delivered_response(202, {"id": "task-1", "score": float("inf")})])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id == "task-1"


def test_create_arbitrary_object_in_body_uses_stable_type_placeholder() -> None:
    # A response body containing an arbitrary non-serializable object covers the
    # fallback "<TypeName>" branch of _normalize_json_value and the False branch of
    # the list/tuple isinstance guard.  No __repr__ is executed, so a raising
    # or credential-leaking __repr__ cannot escape.
    class _BadRepr:
        def __repr__(self) -> str:
            raise RuntimeError("secret credential")

    transport = FakeTransport([_delivered_response(202, {"id": "task-1", "meta": _BadRepr()})])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id == "task-1"
    assert result.metadata.get("meta") == "<_BadRepr>"


@pytest.mark.parametrize("error", [ValueError("digit limit"), RecursionError()])
def test_malformed_json_text_response_body_falls_back_to_redacted_text(
    error: BaseException, monkeypatch: pytest.MonkeyPatch
) -> None:
    transport = FakeTransport([_delivered_response(500, '{"message":"******"}')])
    provider = CopilotProvider(_config(transport))

    def raise_error(*_args: object, **_kwargs: object) -> object:
        raise error

    monkeypatch.setattr(copilot_module.json, "loads", raise_error)
    result = provider.create_task(_request())

    assert result.failure is not None
    assert result.failure.details is not None
    assert result.failure.details["response"] == '{"message":"<redacted>"}'


def test_cyclic_dict_in_transport_details_returns_normalized_failure() -> None:
    # A TransportError whose details contains a self-referential dict must not
    # raise RecursionError.  create_task() must return a normalized failure.
    # TransportError makes a shallow copy of details, so the cycle is detected
    # at the second recursion level.
    cyclic: dict[str, object] = {}
    cyclic["self"] = cyclic
    transport = FakeTransport([TransportError("transport", details=cyclic)])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id is None
    assert result.failure is not None
    assert result.failure.details is not None
    inner = result.failure.details.get("self")
    assert isinstance(inner, Mapping)
    assert inner.get("self") == "<cycle>"


def test_cyclic_list_in_transport_details_returns_normalized_failure() -> None:
    # A TransportError whose details contains a self-referential list (wrapped
    # in a mapping) must not raise RecursionError.
    inner: list[object] = []
    inner.append(inner)
    transport = FakeTransport([TransportError("transport", details={"items": inner})])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id is None
    assert result.failure is not None
    assert result.failure.details is not None
    inner_result = result.failure.details.get("items")
    assert isinstance(inner_result, (list, tuple))
    assert inner_result[0] == "<cycle>"


def test_deep_transport_details_are_bounded_in_failure_diagnostics() -> None:
    nested: dict[str, object] = {"leaf": "value"}
    for _ in range(80):
        nested = {"child": nested}
    transport = FakeTransport([TransportError("transport", details=nested)])
    provider = CopilotProvider(_config(transport))

    result = provider.create_task(_request())

    assert result.task_id is None
    assert result.failure is not None
    assert result.failure.details is not None
    assert "<max-depth>" in str(result.failure.details)


def test_deep_retrieval_response_is_bounded_in_failure_metadata() -> None:
    nested: dict[str, object] = {"leaf": "value"}
    for _ in range(80):
        nested = {"child": nested}
    transport = FakeTransport([_delivered_response(500, nested)])
    provider = CopilotProvider(_config(transport))

    result = provider.get_task("task-1")

    assert result.state is None
    assert result.failure is not None
    assert "<max-depth>" in str(result.failure.details)
    assert "<max-depth>" in str(result.metadata)


def test_provider_error_from_discovery_is_delegated() -> None:
    class FailingDiscovery(ModelDiscovery):
        def _discover_models(self) -> list[ModelRecord]:
            raise ProviderError("discovery failed")

    provider = CopilotProvider(_config(FakeTransport([]), discovery=FailingDiscovery()))

    with pytest.raises(ProviderError, match="discovery failed"):
        provider.discover_models()
