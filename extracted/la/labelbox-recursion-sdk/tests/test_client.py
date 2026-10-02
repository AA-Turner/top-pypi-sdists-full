"""Tests for the generated Python SDK and its hand-written entry point.

These run entirely offline against `httpx.MockTransport`, so they exercise the
real request pipeline — URL building, auth, serialization, deserialization —
without a backend. They are the check that the generated client is *usable*, not
merely that generation exited zero (which `yarn generate python-sdk` gates
separately).
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

import httpx
import pytest
from recursion import DEFAULT_BASE_URL, RecursionApiError, create_recursion_client
from recursion_sdk.client import AuthenticatedClient
from recursion_sdk.facade import Recursion

BASE_URL = "https://api.example.test"
ENV_ID = uuid.UUID("11111111-1111-4111-8111-111111111111")
SESSION_ID = uuid.UUID("22222222-2222-4222-8222-222222222222")

VERDICT_METRIC = {
    "delta_pp": None,
    "fail_count": 0,
    "not_applicable_count": 0,
    "pass_count": 0,
    "prior_rate": None,
    "rate": None,
}

#: A complete `EnvironmentDto`, built from the projection's own required-field
#: list — a partial fixture fails deserialization, which would make these tests
#: about the fixture rather than about the client.
FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures" / "environment_dto.json").read_text()
)


def client_with(handler) -> Recursion:
    """A namespaced client whose transport is `handler`."""
    inner = AuthenticatedClient(
        base_url=BASE_URL, token="test-key", raise_on_unexpected_status=False
    )
    inner.set_async_httpx_client(
        httpx.AsyncClient(
            base_url=BASE_URL,
            transport=httpx.MockTransport(handler),
            headers={"Authorization": "Bearer test-key"},
        )
    )
    return Recursion(inner)


def test_the_namespaces_mirror_the_typescript_sdk() -> None:
    """`@SdkRoute('synthesizers', 'create')` must yield `rl.synthesizers.create`
    in Python exactly as it yields `rl.synthesizers.create` in TypeScript."""
    rl = create_recursion_client(api_key="test-key")
    assert hasattr(rl, "synthesizers")
    assert hasattr(rl.synthesizers, "create")
    assert hasattr(rl.environments, "get")
    assert hasattr(rl.environments, "list")  # `list_` module, `list` on the facade
    assert hasattr(rl.sessions.handoff, "open")


@pytest.mark.asyncio
async def test_nested_handoff_access_uses_the_declared_public_path() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={
                "redemption_url": "http://127.0.0.1:6901/vnc.html",
                "redemption_url_expires_at": "2026-09-15T23:00:00Z",
            },
            headers={"Content-Type": "application/json", "Cache-Control": "no-store"},
        )

    access = await client_with(handler).sessions.handoff.open(SESSION_ID)

    assert seen["method"] == "POST"
    assert seen["url"] == (
        f"{BASE_URL}/managed-agents/v1/sessions/{SESSION_ID}/handoff/access"
    )
    assert access.redemption_url == "http://127.0.0.1:6901/vnc.html"


def test_default_client_targets_the_public_gateway() -> None:
    rl = create_recursion_client(api_key="test-key")
    assert str(rl._client._base_url) == DEFAULT_BASE_URL


def test_an_overridden_base_url_takes_effect() -> None:
    rl = create_recursion_client(api_key="test-key", base_url="http://localhost:4000")
    assert str(rl._client._base_url) == "http://localhost:4000"


def test_an_empty_api_key_is_rejected_at_construction() -> None:
    with pytest.raises(ValueError):
        create_recursion_client(api_key="")


def test_a_whitespace_only_api_key_is_rejected() -> None:
    with pytest.raises(ValueError):
        create_recursion_client(api_key="   ")


@pytest.mark.parametrize(
    "bad_base_url", ["api.example.com", "localhost:4000", "api.example.com/v1", ""]
)
def test_a_base_url_without_a_host_is_rejected(bad_base_url: str) -> None:
    """A schemeless `base_url` would otherwise produce a relative request URL, so
    fail closed at construction rather than at the first call."""
    with pytest.raises(ValueError):
        create_recursion_client(api_key="test-key", base_url=bad_base_url)


def test_a_caller_supplied_authorization_header_cannot_displace_the_api_key() -> None:
    """`create_recursion_client(headers=...)` is documented as unable to displace
    the auth header. That is a security-relevant claim resting on library
    internals and a *ranged* dependency (`httpx`), so pin it rather than trust the
    docstring: every other version-sensitive invariant here has a test."""
    rl = create_recursion_client(
        api_key="real-key",
        headers={
            "Authorization": "Bearer attacker",
            "X-Proxy-Target-Url": "https://preview",
        },
    )
    headers = rl._client.get_async_httpx_client().headers
    assert headers.get("authorization") == "Bearer real-key"
    assert headers.get("x-proxy-target-url") == "https://preview", (
        "other headers still pass through"
    )


def test_redirects_are_not_followed() -> None:
    """A followed cross-origin redirect would carry the Authorization header to
    another host. This is the generator's default; pin it so it stays true."""
    rl = create_recursion_client(api_key="test-key")
    assert rl._client._follow_redirects is False


def test_required_nullable_model_reference_deserializes_none() -> None:
    """A required property may still be explicitly null on the wire."""
    from recursion_sdk.models.managed_agents_session_list_item import (
        ManagedAgentsSessionListItem,
    )

    session = ManagedAgentsSessionListItem.from_dict(
        {
            "computer_use": False,
            "config": None,
            "created_at": "2026-09-18T12:00:00Z",
            "credential_refs": None,
            "credential_refs_configured": True,
            "evaluation_eligibility": {"eligible": False},
            "kind": "api_call",
            "latest_evaluation": None,
            "organization_id": "dev-org",
            "root_session_id": str(SESSION_ID),
            "session_id": str(SESSION_ID),
            "session_path": "/",
            "status": "completed",
            "updated_at": "2026-09-18T12:00:00Z",
        }
    )

    assert session.latest_evaluation is None
    assert session.to_dict()["latest_evaluation"] is None


def test_required_nullable_overview_reference_deserializes_none() -> None:
    from recursion_sdk.models.managed_agents_evaluation_overview_tiles import (
        ManagedAgentsEvaluationOverviewTiles,
    )

    tiles = ManagedAgentsEvaluationOverviewTiles.from_dict(
        {
            "coverage": {
                "delta_pp": None,
                "eligible_session_count": 0,
                "evaluated_eligible_session_count": 0,
                "evaluation_snapshot_count": 0,
                "history_status": "complete",
                "prior_rate": None,
                "rate": None,
            },
            "evaluation_cost": {
                "complete_count": 0,
                "completeness": None,
                "delta_usd": None,
                "evaluation_count": 0,
                "per_evaluation_usd": None,
                "prior_per_evaluation_usd": None,
                "total_usd": None,
            },
            "lowest_criterion": None,
            "overall_pass": VERDICT_METRIC,
        }
    )

    assert tiles.lowest_criterion is None
    assert tiles.to_dict()["lowest_criterion"] is None


def test_nullable_overview_array_item_deserializes_none() -> None:
    from recursion_sdk.models.managed_agents_agent_row import ManagedAgentsAgentRow

    row = ManagedAgentsAgentRow.from_dict(
        {
            "criterion_metrics": [None],
            "evaluation_count": 0,
            "newest_failures": [],
            "overall_pass": VERDICT_METRIC,
            "target_agent_id": str(ENV_ID),
        }
    )

    assert row.criterion_metrics == [None]
    assert row.to_dict()["criterion_metrics"] == [None]


def test_nullable_optional_patch_field_distinguishes_null_from_omission() -> None:
    """Patch models must preserve all three states: value, null, and omitted."""
    from recursion_sdk.models.update_environment_settings_dto import (
        UpdateEnvironmentSettingsDto,
    )
    from recursion_sdk.types import UNSET

    omitted = UpdateEnvironmentSettingsDto()
    cleared = UpdateEnvironmentSettingsDto(problem_editor_instructions=None)

    assert omitted.problem_editor_instructions is UNSET
    assert "problemEditorInstructions" not in omitted.to_dict()
    assert cleared.problem_editor_instructions is None
    assert cleared.to_dict()["problemEditorInstructions"] is None
    assert (
        UpdateEnvironmentSettingsDto.from_dict(
            {"problemEditorInstructions": None}
        ).problem_editor_instructions
        is None
    )


@pytest.mark.asyncio
async def test_a_read_sends_a_bearer_token_and_deserializes_the_response() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["url"] = str(request.url)
        seen["auth"] = request.headers.get("Authorization")
        return httpx.Response(
            200, json=FIXTURE, headers={"Content-Type": "application/json"}
        )

    environment = await client_with(handler).environments.get(ENV_ID)

    assert seen["method"] == "GET"
    assert seen["url"] == f"{BASE_URL}/v1/environments/{ENV_ID}"
    assert seen["auth"] == "Bearer test-key", "the API key is sent as a bearer token"
    assert environment.name == FIXTURE["name"], (
        "the response deserialized into a typed model"
    )


@pytest.mark.asyncio
async def test_a_mutation_serializes_the_request_body() -> None:
    from recursion_sdk.models.create_environment_dto import CreateEnvironmentDto

    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["url"] = str(request.url)
        seen["body"] = json.loads(request.content)
        return httpx.Response(
            201, json=FIXTURE, headers={"Content-Type": "application/json"}
        )

    body = CreateEnvironmentDto(
        external_id="ticketing",
        name="Ticketing agent",
        organization_id=uuid.UUID(FIXTURE["organizationId"]),
    )
    created = await client_with(handler).environments.upsert(body=body)

    assert seen["method"] == "POST"
    assert seen["url"] == f"{BASE_URL}/v1/environments"
    assert seen["body"]["name"] == "Ticketing agent"
    assert seen["body"]["externalId"] == "ticketing", (
        "fields are camelCased on the wire"
    )
    assert created is not None


@pytest.mark.asyncio
async def test_create_agent_propagates_idempotency_key_without_changing_the_body() -> (
    None
):
    from recursion_sdk.models.managed_agents_create_agent_request import (
        ManagedAgentsCreateAgentRequest,
    )

    seen_headers: list[str | None] = []
    seen_bodies: list[object] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_headers.append(request.headers.get("Idempotency-Key"))
        seen_bodies.append(json.loads(request.content))
        # The request contract is the subject; a non-success response avoids a
        # large unrelated Agent fixture while still exercising the real wire.
        return httpx.Response(
            503,
            json={"code": "service_unavailable", "message": "Unavailable"},
            headers={"Content-Type": "application/json"},
        )

    body = ManagedAgentsCreateAgentRequest(
        model="mock:echo", name="Recipe agent", system="Follow the instructions."
    )
    rl = client_with(handler)
    with pytest.raises(RecursionApiError):
        await rl.managed_agents.create_agent(body=body)
    with pytest.raises(RecursionApiError):
        await rl.managed_agents.create_agent(
            body=body, idempotency_key="stable-logical-create-key"
        )

    assert seen_headers == [None, "stable-logical-create-key"]
    assert seen_bodies[0] == seen_bodies[1], (
        "adding the header must not alter the request body"
    )


@pytest.mark.asyncio
async def test_a_non_2xx_response_raises_rather_than_returning_a_value() -> None:
    """The generator returns `None` for an undocumented status and the parsed
    *error body* for a documented one — both easy to use by accident. The facade
    raises instead, matching the TypeScript client's `throwOnError: true`."""

    error_body = {
        "code": "not_found",
        "message": "Environment not found",
        "details": {"resource": "environment"},
    }

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404,
            json=error_body,
            headers={"Content-Type": "application/json"},
        )

    with pytest.raises(RecursionApiError) as raised:
        await client_with(handler).environments.get(ENV_ID)
    assert raised.value.status_code == 404
    assert raised.value.parsed.to_dict() == error_body
    assert json.loads(raised.value.content) == error_body


@pytest.mark.parametrize(
    ("status_code", "error_code"),
    [
        (400, "invalid_request"),
        (401, "unauthorized"),
        (403, "forbidden"),
        (429, "rate_limit_exceeded"),
        (500, "internal_error"),
        (503, "service_unavailable"),
    ],
)
@pytest.mark.asyncio
async def test_list_models_deserializes_flat_gateway_errors(
    status_code: int, error_code: str
) -> None:
    """Every documented Managed Agents error deserializes as the flat envelope."""

    error_body = {"code": error_code, "message": "Gateway rejected the request"}

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code,
            json=error_body,
            headers={"Content-Type": "application/json"},
        )

    with pytest.raises(RecursionApiError) as raised:
        await client_with(handler).managed_agents.list_models()
    assert raised.value.status_code == status_code
    assert raised.value.parsed.to_dict() == error_body


@pytest.mark.asyncio
async def test_an_undocumented_status_also_raises_recursion_api_error() -> None:
    """The documented contract is "every non-2xx raises `RecursionApiError`", so
    a status the spec never mentions must not escape as the generator's own
    `UnexpectedStatus`. That is what `raise_on_unexpected_status=False` buys: it
    keeps the generated code from raising before the facade can normalise."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            418, json={"weird": True}, headers={"Content-Type": "application/json"}
        )

    with pytest.raises(RecursionApiError) as raised:
        await client_with(handler).environments.get(ENV_ID)
    assert raised.value.status_code == 418


@pytest.mark.asyncio
async def test_query_parameters_reach_the_wire() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={"items": [], "nextCursor": None, "total": 0},
            headers={"Content-Type": "application/json"},
        )

    await client_with(handler).environments.list(limit=25, search="ticket")
    assert "limit=25" in str(seen["url"])
    assert "search=ticket" in str(seen["url"])
