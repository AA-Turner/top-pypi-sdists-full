"""Exercise generated clients against their public HTTP boundary, without network I/O."""

from __future__ import annotations

import asyncio
import io
import json
import zipfile
from dataclasses import dataclass, field
from datetime import datetime
from email import policy
from email.message import EmailMessage
from email.parser import BytesParser
from uuid import UUID

import httpx
import pytest
from pydantic import JsonValue, TypeAdapter, ValidationError

from recursion_sdk import (
    AsyncRecursion,
    Recursion,
    RecursionAPIError,
    RecursionContractError,
    Upload,
    models,
)

HTTP_OK = 200
HTTP_NOT_MODIFIED = 304
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
UNDECLARED_HTTP_STATUS = 418
IDENTIFIER = "00000000-0000-4000-8000-000000000001"
OTHER_IDENTIFIER = "00000000-0000-4000-8000-000000000002"
RESOURCE_IDENTIFIER = UUID(IDENTIFIER)
TIMESTAMP = "2026-10-10T00:00:00Z"
QUERY_TIMESTAMP = "2026-10-10T12:34:56+05:30"
API_KEY_PAYLOAD_LENGTH = 43
API_KEY = "rma_" + "A" * API_KEY_PAYLOAD_LENGTH
BASE_URL = "https://sdk-tests.invalid"
CURRENT_ETAG = '"rev-1"'
UPDATED_ETAG = '"rev-2"'
MAX_SAFE_INTEGER = 9007199254740991
MINIMUM_CPU_MILLICORES = 250
INVALID_CPU_MILLICORES = 1
GZIP_CONTENT = bytes.fromhex("1f8b080000000000000303000000000000000000")
JSON_OBJECT = TypeAdapter(dict[str, JsonValue])
MEMORY_RESPONSE: dict[str, object] = {
    "enabled": False,
    "enabledEditable": True,
    "minNewEvidence": 0,
    "maxEvidencePerRun": 0,
    "cooldownSeconds": 0,
    "effectiveMinNewEvidence": 5,
    "effectiveMaxEvidencePerRun": 50,
    "effectiveCooldownSeconds": 3600,
}
ENVIRONMENT_RESPONSE: dict[str, object] = {
    "organization_id": IDENTIFIER,
    "environment_id": IDENTIFIER,
    "name": "sdk-test",
    "scope": "organization",
    "provider": "runs",
    "setup": {},
    "resources": {},
    "computer_use": False,
    "created_at": TIMESTAMP,
    "updated_at": TIMESTAMP,
}


@dataclass
class Wire:
    """Capture requests and supply one explicit server response."""

    body: object = field(default_factory=lambda: {"sessions": []})
    status: int = HTTP_OK
    content: bytes | None = None
    headers: dict[str, str] = field(default_factory=dict)
    requests: list[httpx.Request] = field(default_factory=list)

    def respond(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if self.content is not None:
            return httpx.Response(self.status, content=self.content, headers=self.headers)
        return httpx.Response(self.status, json=self.body, headers=self.headers)

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.respond)


def request_json(request: httpx.Request) -> dict[str, JsonValue]:
    return JSON_OBJECT.validate_json(request.content, strict=True)


@pytest.mark.parametrize("explicit_null", [False, True])
def test_patch_preserves_omission_null_and_request_scope(explicit_null: bool) -> None:
    payload: dict[str, object] = {"enabled": False}
    if explicit_null:
        payload["instructions"] = None
    body = models.RecursionLearningConfigRequest.model_validate(payload)
    wire = Wire(body=MEMORY_RESPONSE, headers={"ETag": UPDATED_ETAG})

    with Recursion(
        api_key=API_KEY,
        base_url=BASE_URL,
        organization_id=IDENTIFIER,
        tenant_id=IDENTIFIER,
        transport=wire.transport(),
    ) as recursion:
        result = recursion.managed_agents.update_agent_memory_settings(
            agent_id=RESOURCE_IDENTIFIER,
            if_match=CURRENT_ETAG,
            body=body,
            x_organization_id=IDENTIFIER,
            x_tenant_id=IDENTIFIER,
        )

    assert len(wire.requests) == 1
    request = wire.requests[0]
    assert request.method == "PATCH"
    assert request.url == f"{BASE_URL}/managed-agents/v1/agents/{IDENTIFIER}/memory/settings"
    assert request_json(request) == payload
    assert request.headers["authorization"] == f"Bearer {API_KEY}"
    assert request.headers["x-organization-id"] == IDENTIFIER
    assert request.headers["x-tenant-id"] == IDENTIFIER
    assert request.headers["if-match"] == CURRENT_ETAG
    assert isinstance(result.data, models.RecursionLearningConfig)
    assert result.data.model_dump(mode="json", by_alias=True, exclude_unset=True) == MEMORY_RESPONSE
    assert result.response.status_code == HTTP_OK
    assert result.response.headers["etag"] == UPDATED_ETAG


def test_operation_cannot_change_constructor_scope() -> None:
    wire = Wire()
    with Recursion(
        api_key=API_KEY,
        organization_id=IDENTIFIER,
        tenant_id=IDENTIFIER,
        transport=wire.transport(),
    ) as recursion:
        with pytest.raises(RecursionContractError, match="selector"):
            recursion.managed_agents.list_sessions(x_organization_id=OTHER_IDENTIFIER)
        with pytest.raises(RecursionContractError, match="selector"):
            recursion.managed_agents.list_sessions(x_tenant_id=OTHER_IDENTIFIER)
    assert wire.requests == []


def test_optional_null_parameters_are_omitted_and_preserve_constructor_scope() -> None:
    wire = Wire()
    with Recursion(
        api_key=API_KEY,
        organization_id=IDENTIFIER,
        tenant_id=IDENTIFIER,
        transport=wire.transport(),
    ) as recursion:
        recursion.managed_agents.list_sessions(
            metadata=None,
            root_only=None,
            x_organization_id=None,
            x_tenant_id=None,
        )
    assert len(wire.requests) == 1
    request = wire.requests[0]
    assert not request.url.query
    assert request.headers["x-organization-id"] == IDENTIFIER
    assert request.headers["x-tenant-id"] == IDENTIFIER


@pytest.mark.parametrize(
    "api_key",
    [
        "",
        "A" * API_KEY_PAYLOAD_LENGTH,
        "rma_short",
        "rma_" + "A" * (API_KEY_PAYLOAD_LENGTH + 1),
        "rma_" + "!" * API_KEY_PAYLOAD_LENGTH,
        " " + API_KEY,
        API_KEY + " ",
    ],
)
def test_constructor_rejects_invalid_api_key_shape(api_key: str) -> None:
    wire = Wire()
    with pytest.raises(ValueError, match="api_key"):
        Recursion(api_key=api_key, transport=wire.transport())
    assert wire.requests == []


@pytest.mark.parametrize("code", ["invalid_json", "invalid_request"])
def test_declared_api_error_retains_typed_envelope_status_and_headers(code: str) -> None:
    error_body = {"code": code, "message": "Invalid memory settings"}
    wire = Wire(
        body=error_body,
        status=HTTP_BAD_REQUEST,
        headers={"X-Request-Id": "sdk-error-receipt"},
    )
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        with pytest.raises(RecursionAPIError) as caught:
            recursion.managed_agents.update_agent_memory_settings(
                agent_id=RESOURCE_IDENTIFIER,
                if_match=CURRENT_ETAG,
                body=models.RecursionLearningConfigRequest.model_validate({"enabled": False}),
            )

    error = caught.value
    assert len(wire.requests) == 1
    assert error.status_code == HTTP_BAD_REQUEST
    assert error.code == code
    assert error.message == error_body["message"]
    assert isinstance(error.error, models.RecursionApiError)
    assert error.error.model_dump(mode="json", by_alias=True, exclude_unset=True) == error_body
    assert error.response.headers["x-request-id"] == "sdk-error-receipt"
    assert JSON_OBJECT.validate_json(error.response.content, strict=True) == error_body


def test_error_code_must_be_declared_for_its_http_status() -> None:
    # forbidden is a valid global API error, but it cannot inhabit this operation's 400.
    wire = Wire(body={"code": "forbidden", "message": "Wrong status"}, status=HTTP_BAD_REQUEST)
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        with pytest.raises(RecursionContractError) as caught:
            recursion.managed_agents.update_agent_memory_settings(
                agent_id=RESOURCE_IDENTIFIER,
                if_match=CURRENT_ETAG,
                body=models.RecursionLearningConfigRequest.model_validate({"enabled": False}),
            )
    assert len(wire.requests) == 1
    assert caught.value.response is not None
    assert caught.value.response.status_code == HTTP_BAD_REQUEST


@pytest.mark.parametrize(
    ("content", "content_type", "status"),
    [
        (b"not-json", "application/json", HTTP_OK),
        (b'{"sessions":[],"unexpected":true}', "application/json", HTTP_OK),
        (b'{"sessions":[]}', "text/plain", HTTP_OK),
        (b'{"sessions":[]}', "application/json", UNDECLARED_HTTP_STATUS),
    ],
)
def test_malformed_or_undeclared_response_raises_contract_error(
    content: bytes, content_type: str, status: int
) -> None:
    wire = Wire(content=content, status=status, headers={"Content-Type": content_type})
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        with pytest.raises(RecursionContractError) as caught:
            recursion.managed_agents.list_sessions()
    assert len(wire.requests) == 1
    assert caught.value.response is not None
    assert caught.value.response.content == content


def test_sync_conditional_read_preserves_bodyless_304_and_etag() -> None:
    wire = Wire(content=b"", status=HTTP_NOT_MODIFIED, headers={"ETag": CURRENT_ETAG})
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        result = recursion.managed_agents.get_tag(
            tag_id=RESOURCE_IDENTIFIER, if_none_match=CURRENT_ETAG
        )
    assert result.data is None
    assert result.response.status_code == HTTP_NOT_MODIFIED
    assert result.response.content == b""
    assert result.response.headers["etag"] == CURRENT_ETAG
    assert wire.requests[0].headers["if-none-match"] == CURRENT_ETAG


def test_async_conditional_read_preserves_bodyless_304_and_etag() -> None:
    wire = Wire(content=b"", status=HTTP_NOT_MODIFIED, headers={"ETag": CURRENT_ETAG})

    async def read() -> None:
        async with AsyncRecursion(api_key=API_KEY, transport=wire.transport()) as recursion:
            result = await recursion.managed_agents.get_tag(
                tag_id=RESOURCE_IDENTIFIER, if_none_match=CURRENT_ETAG
            )
        assert result.data is None
        assert result.response.status_code == HTTP_NOT_MODIFIED
        assert result.response.content == b""
        assert result.response.headers["etag"] == CURRENT_ETAG

    asyncio.run(read())
    assert wire.requests[0].headers["if-none-match"] == CURRENT_ETAG


@pytest.mark.parametrize("content", [b"", b"unexpected-body"])
def test_304_requires_conditional_request_and_empty_body(content: bytes) -> None:
    wire = Wire(content=content, status=HTTP_NOT_MODIFIED)
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        with pytest.raises(RecursionContractError) as caught:
            recursion.managed_agents.get_tag(tag_id=RESOURCE_IDENTIFIER)
        if content:
            with pytest.raises(RecursionContractError, match="empty"):
                recursion.managed_agents.get_tag(
                    tag_id=RESOURCE_IDENTIFIER, if_none_match=CURRENT_ETAG
                )
    assert caught.value.response is not None
    assert caught.value.response.status_code == HTTP_NOT_MODIFIED


def test_multipart_preserves_boundary_file_identity_and_metadata_text() -> None:
    archive_buffer = io.BytesIO()
    with zipfile.ZipFile(archive_buffer, "w") as archive:
        archive.writestr(
            "SKILL.md", "---\nname: sdk-test\ndescription: SDK test.\n---\n# SDK test\n"
        )
    archive_content = archive_buffer.getvalue()
    metadata = '{"source":"sdk-test"}'
    skill: dict[str, object] = {
        "organization_id": IDENTIFIER,
        "skill_id": IDENTIFIER,
        "name": "sdk-test",
        "description": "SDK test.",
        "source": "organization",
        "created_at": TIMESTAMP,
        "updated_at": TIMESTAMP,
    }
    wire = Wire(body=skill)
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        result = recursion.managed_agents.publish_skill_bundle(
            bundle=Upload("sdk-test.zip", archive_content, "application/zip"), metadata=metadata
        )

    assert isinstance(result.data, models.Skill)
    assert len(wire.requests) == 1
    request = wire.requests[0]
    message = BytesParser(policy=policy.default).parsebytes(
        b"Content-Type: "
        + request.headers["content-type"].encode("ascii")
        + b"\r\nMIME-Version: 1.0\r\n\r\n"
        + request.content
    )
    assert isinstance(message, EmailMessage)
    assert message.is_multipart()
    parts = {
        part.get_param("name", header="content-disposition"): part for part in message.iter_parts()
    }
    assert set(parts) == {"bundle", "metadata"}
    bundle = parts["bundle"]
    assert bundle.get_filename() == "sdk-test.zip"
    assert bundle.get_content_type() == "application/zip"
    assert bundle.get_payload(decode=True) == archive_content
    assert parts["metadata"].get_payload(decode=True) == metadata.encode()


def test_binary_download_returns_exact_gzip_bytes() -> None:
    wire = Wire(content=GZIP_CONTENT, headers={"Content-Type": "application/gzip"})
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        result = recursion.managed_agents.get_skill_version_content(
            skill_id=RESOURCE_IDENTIFIER, skill_version_id=RESOURCE_IDENTIFIER
        )
    assert result.data == GZIP_CONTENT
    assert result.response.content == GZIP_CONTENT


def test_recursive_json_preserves_booleans_numbers_and_nulls() -> None:
    metadata: dict[str, object] = {
        "nested": [None, True, False, 0, -1, 1.25, "x", [], {}, [MAX_SAFE_INTEGER]]
    }
    skill_group: dict[str, object] = {
        "organization_id": IDENTIFIER,
        "skill_group_id": IDENTIFIER,
        "name": "sdk-test",
        "skill_count": 0,
        "created_at": TIMESTAMP,
        "updated_at": TIMESTAMP,
        "metadata": metadata,
    }
    wire = Wire(body=skill_group)
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        result = recursion.managed_agents.update_skill_group(
            skill_group_id=RESOURCE_IDENTIFIER,
            body=models.SkillGroupPatchRequest.model_validate({"metadata": metadata}),
        )
    expected = json.dumps(metadata, sort_keys=True)
    # JSON serialization distinguishes true from 1, unlike Python equality.
    assert json.dumps(request_json(wire.requests[0])["metadata"], sort_keys=True) == expected
    decoded = result.data.model_dump(mode="json", by_alias=True, exclude_unset=True)
    assert json.dumps(decoded["metadata"], sort_keys=True) == expected


def test_closed_response_union_rejects_mixed_delivery_variant() -> None:
    delivery: dict[str, object] = {"kind": "webhook", "webhookUrl": "/sdk-test"}
    event_source: dict[str, object] = {
        "eventSourceId": IDENTIFIER,
        "displayName": "sdk-test",
        "type": "custom_webhook",
        "status": "active",
        "delivery": delivery,
        "revision": 1,
        "createdAt": TIMESTAMP,
        "updatedAt": TIMESTAMP,
        "health": "never_received",
        "triggerCount": 0,
        "lastDelivery": None,
    }
    wire = Wire(body={"items": [event_source], "nextCursor": None, "total": 1})
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        result = recursion.managed_agents.list_event_sources()
        assert result.data.model_dump(mode="json", by_alias=True, exclude_unset=True) == wire.body
        delivery["connectionId"] = IDENTIFIER
        with pytest.raises(RecursionContractError) as caught:
            recursion.managed_agents.list_event_sources()
    assert len(wire.requests) == 2
    assert caught.value.response is not None


def test_canonical_provider_conditional_rejects_before_transport() -> None:
    wire = Wire(body=ENVIRONMENT_RESPONSE)
    valid = {
        "name": "sdk-test",
        "provider": "runs",
        "resources": {"cpu_milli": MINIMUM_CPU_MILLICORES},
    }
    invalid = {**valid, "provider": "docker"}
    # The model covers field types; the canonical if/then covers their relationship.
    invalid_body = models.CreateEnvironmentRequest.model_validate(invalid)
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        recursion.managed_agents.create_environment(
            body=models.CreateEnvironmentRequest.model_validate(valid)
        )
        with pytest.raises(RecursionContractError):
            recursion.managed_agents.create_environment(body=invalid_body)
    assert len(wire.requests) == 1
    assert request_json(wire.requests[0]) == valid


def test_invalid_numeric_union_rejects_before_transport() -> None:
    wire = Wire(body=ENVIRONMENT_RESPONSE)
    payload = {
        "name": "sdk-test",
        "provider": "runs",
        "resources": {"cpu_milli": INVALID_CPU_MILLICORES},
    }
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        with pytest.raises((ValidationError, RecursionContractError)):
            recursion.managed_agents.create_environment(
                body=models.CreateEnvironmentRequest.model_validate(payload)
            )
    assert wire.requests == []


def test_unsafe_nested_json_integer_rejects_before_transport() -> None:
    wire = Wire()
    payload = {"metadata": {"nested": [MAX_SAFE_INTEGER + 1]}}
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        with pytest.raises((ValidationError, RecursionContractError)):
            recursion.managed_agents.update_skill_group(
                skill_group_id=RESOURCE_IDENTIFIER,
                body=models.SkillGroupPatchRequest.model_validate(payload),
            )
    assert wire.requests == []


@pytest.mark.parametrize(
    "number",
    [str(MAX_SAFE_INTEGER + 1), "NaN", "Infinity", "-Infinity", "1e400"],
    ids=["unsafe_integer", "nan", "positive_infinity", "negative_infinity", "float_overflow"],
)
def test_unsafe_or_nonfinite_response_json_rejects_before_model_coercion(number: str) -> None:
    skill_group: dict[str, object] = {
        "organization_id": IDENTIFIER,
        "skill_group_id": IDENTIFIER,
        "name": "sdk-test",
        "skill_count": 0,
        "created_at": TIMESTAMP,
        "updated_at": TIMESTAMP,
    }
    # Supply raw JSON: reserializing through a model could round an unsafe integer.
    content = (json.dumps(skill_group)[:-1] + ',"metadata":{"nested":[' + number + "]}}").encode()
    wire = Wire(content=content, headers={"Content-Type": "application/json"})
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        with pytest.raises(RecursionContractError) as caught:
            recursion.managed_agents.update_skill_group(
                skill_group_id=RESOURCE_IDENTIFIER,
                body=models.SkillGroupPatchRequest.model_validate({"name": "sdk-test"}),
            )
    assert len(wire.requests) == 1
    assert caught.value.response is not None
    assert caught.value.response.content == content


def test_path_segments_and_repeated_query_values_are_encoded() -> None:
    thread_id = "imported /?#é"
    wire = Wire(body={"code": "not_found", "message": "Unknown thread"}, status=HTTP_NOT_FOUND)
    with Recursion(api_key=API_KEY, base_url=BASE_URL, transport=wire.transport()) as recursion:
        with pytest.raises(RecursionAPIError):
            recursion.managed_agents.get_session_thread(
                session_id=RESOURCE_IDENTIFIER, thread_id=thread_id
            )
    assert wire.requests[0].url.raw_path == (
        f"/managed-agents/v1/sessions/{IDENTIFIER}/threads/imported%20%2F%3F%23%C3%A9".encode()
    )

    metadata = ["label:with spaces", "source:a/b?c#d", "unicode:é"]
    wire = Wire()
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        recursion.managed_agents.list_sessions(metadata=metadata, root_only=True)
    assert wire.requests[0].url.params.get_list("metadata") == metadata
    assert wire.requests[0].url.params["root_only"] == "true"


def test_datetime_query_preserves_offset_and_rejects_naive_datetime() -> None:
    timestamp = datetime.fromisoformat(QUERY_TIMESTAMP)
    wire = Wire(
        body={"code": "invalid_request", "message": "Invalid automation run filter"},
        status=HTTP_BAD_REQUEST,
    )
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        with pytest.raises(RecursionAPIError):
            recursion.managed_agents.list_automation_runs(created_at_gte=timestamp)
        with pytest.raises(RecursionContractError):
            recursion.managed_agents.list_automation_runs(
                created_at_gte=timestamp.replace(tzinfo=None)
            )
    assert len(wire.requests) == 1
    assert wire.requests[0].url.params["createdAtGte"] == timestamp.isoformat()


def test_sync_context_manager_closes_connections() -> None:
    wire = Wire()
    with Recursion(api_key=API_KEY, transport=wire.transport()) as recursion:
        recursion.managed_agents.list_sessions()
    with pytest.raises(RuntimeError, match="closed"):
        recursion.managed_agents.list_sessions()
    assert len(wire.requests) == 1


def test_async_context_manager_closes_connections() -> None:
    wire = Wire()

    async def use_client() -> None:
        async with AsyncRecursion(api_key=API_KEY, transport=wire.transport()) as recursion:
            await recursion.managed_agents.list_sessions()
        with pytest.raises(RuntimeError, match="closed"):
            await recursion.managed_agents.list_sessions()

    asyncio.run(use_client())
    assert len(wire.requests) == 1


def test_transport_errors_propagate_without_automatic_retry() -> None:
    requests: list[httpx.Request] = []

    def unavailable(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        raise httpx.ConnectError("No connection", request=request)

    with Recursion(api_key=API_KEY, transport=httpx.MockTransport(unavailable)) as recursion:
        with pytest.raises(httpx.ConnectError, match="No connection"):
            recursion.managed_agents.list_sessions()
    assert len(requests) == 1
