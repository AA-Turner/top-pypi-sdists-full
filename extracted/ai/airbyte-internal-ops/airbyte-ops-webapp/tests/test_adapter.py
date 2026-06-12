"""Tests for the connector pinning adapter."""

import json
import urllib.parse

import pytest

from airbyte_ops_webapp import state as state_module
from airbyte_ops_webapp.models import OverridePlan
from airbyte_ops_webapp.pages.connector_version_manager import page as page_module
from airbyte_ops_webapp.pages.connector_version_manager.defaults import (
    DEFAULT_CONNECTOR_QUERY,
    connector_version_manager_launch_path,
    default_connector_query,
)
from airbyte_ops_webapp.services.connector_version_manager.adapter import (
    OpsMcpAdapter,
    operation_result_to_json,
    preview_to_json,
)
from airbyte_ops_webapp.services.connector_version_manager.demo_mode import (
    MockPinningAdapter,
)


def test_search_connectors_matches_name() -> None:
    adapter = MockPinningAdapter()

    results = adapter.search_connectors("github")

    assert len(results) == 1
    assert results[0].name == "source-github"


def test_default_connector_query_accepts_launch_arg_aliases() -> None:
    assert default_connector_query(query="destination-snowflake") == (
        "destination-snowflake"
    )
    assert default_connector_query(connector_name="source-postgres") == (
        "source-postgres"
    )
    assert default_connector_query(connector="source-github") == "source-github"
    assert default_connector_query() == DEFAULT_CONNECTOR_QUERY


def test_connector_version_manager_launch_path_encodes_default_query() -> None:
    path = connector_version_manager_launch_path("destination-snowflake")
    parsed = urllib.parse.urlparse(path)
    params = urllib.parse.parse_qs(parsed.query)

    assert parsed.path == "/launch"
    assert params["tool"] == ["manage_connector_versions"]
    assert json.loads(params["args"][0]) == {"query": "destination-snowflake"}


def test_connector_version_manager_prefills_connector_name_arg(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")

    app = page_module.connector_version_manager(connector_name="destination-snowflake")

    assert app.state["query"] == "destination-snowflake"
    assert app.state["default_connector_from_args"] is True
    assert app.state["selected_connector"]["name"] == "destination-snowflake"
    assert app.state["target_version"] == "3.3.1"
    assert app.state["versions"][0]["docker_image_tag"] == "3.3.1"


def test_workspace_preview_is_safe_and_targets_workspace_tool() -> None:
    adapter = MockPinningAdapter()
    plan = OverridePlan(
        action="set",
        connector_id="7e1aa9a0-8490-462e-8d5c-6a7906adf2f4",
        connector_name="source-github",
        connector_type="source",
        scope_type="workspace",
        organization_id="org_example",
        workspace_id="workspace_example",
        scope_id="workspace_example",
        version="2.4.0",
        override_reason="Customer support investigation",
        override_reason_reference_url="https://github.com/airbytehq/airbyte-ops-mcp/issues/750",
        approval_comment_url="https://airbytehq-team.slack.com/archives/C123/p123",
        user_email="devin-local@example.com",
        customer_tier_filter="TIER_2",
        force=False,
    )

    preview = adapter.stage_override(plan)

    assert preview.tool_name == "set_version_override"
    assert preview.mutating is False
    assert '"mode"' not in preview_to_json(preview)
    payload = preview.payload.model_dump()
    assert payload["target"]["scope"] == "workspace"
    assert payload["target"]["workspace_id"] == "workspace_example"
    assert payload["version"] == "2.4.0"
    assert payload["unset"] is False
    assert "approval_comment_url" in preview.required_approval_fields


def test_unset_preview_omits_version() -> None:
    adapter = MockPinningAdapter()
    plan = OverridePlan(
        action="unset",
        connector_id="7e1aa9a0-8490-462e-8d5c-6a7906adf2f4",
        connector_name="source-github",
        connector_type="source",
        scope_type="actor",
        organization_id="org_example",
        workspace_id="workspace_example",
        actor_id="source_example",
        scope_id="source_example",
        version=None,
        override_reason="Customer support investigation",
        override_reason_reference_url="https://github.com/airbytehq/airbyte-ops-mcp/issues/750",
        approval_comment_url="https://airbytehq-team.slack.com/archives/C123/p123",
        user_email="devin-local@example.com",
        customer_tier_filter="TIER_2",
        force=True,
    )

    preview = adapter.stage_override(plan)

    assert preview.tool_name == "set_version_override"
    payload = preview.payload.model_dump()
    assert payload["target"]["scope"] == "actor"
    assert payload["target"]["actor_id"] == "source_example"
    assert payload["version"] is None
    assert payload["unset"] is True
    assert payload["force"] is True


def test_mock_apply_is_successful_noop() -> None:
    adapter = MockPinningAdapter()
    plan = OverridePlan(
        action="set",
        connector_id="ef69ef6e-aa7f-4af1-a01d-ef775033524e",
        connector_name="source-github",
        connector_type="source",
        scope_type="organization",
        organization_id="org_example",
        scope_id="org_example",
        version="1.8.7",
        override_reason="Customer support investigation",
        override_reason_reference_url="https://github.com/airbytehq/airbyte-ops-mcp/issues/750",
        approval_comment_url="https://airbytehq-team.slack.com/archives/C123/p123",
        user_email="devin-local@example.com",
        customer_tier_filter="TIER_2",
        force=False,
    )

    result = adapter.apply_override(plan)

    assert result.success is True
    assert result.mutating is False
    assert result.mode == "mock"
    assert '"mode": "mock"' in operation_result_to_json(result)
    assert "no Airbyte Cloud change" in result.message


def test_mock_adapter_does_not_load_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")
    monkeypatch.setenv(state_module.AIRBYTE_BEARER_TOKEN_ENV_VAR, "should-not-load")
    monkeypatch.setenv(
        state_module.AIRBYTE_CONFIG_API_ROOT_ENV_VAR,
        "https://should-not-load.example",
    )

    adapter = page_module._adapter()

    assert isinstance(adapter, MockPinningAdapter)
    assert adapter.bearer_token is None
    assert adapter.config_api_root == "mock://config-api"


def test_local_definition_options_builds_bearer_header(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_headers = {}

    class FakeResponse:
        status_code = 200

        @staticmethod
        def json() -> dict[str, list[dict[str, str]]]:
            return {"sourceDefinitions": []}

    def fake_post(
        url: str,
        *,
        json: dict[str, str],
        headers: dict[str, str],
        timeout: int,
    ) -> FakeResponse:
        captured_headers.update(headers)
        return FakeResponse()

    monkeypatch.setattr(
        "airbyte_ops_webapp.services.connector_version_manager.adapter.api_client._get_access_token",
        lambda **kwargs: "local-token",
    )
    monkeypatch.setattr(
        "airbyte_ops_webapp.services.connector_version_manager.adapter.api_client.requests.post",
        fake_post,
    )

    adapter = OpsMcpAdapter(
        client_id="client-id",
        client_secret="client-secret",
        config_api_root="http://localhost:8000/api/v1",
    )

    assert adapter._local_definition_options("source") == ()
    assert captured_headers["Authorization"] == "Bearer local-token"
