"""Tests for the connector pinning adapter."""

import json
import urllib.parse
from types import SimpleNamespace

import pytest
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_webapp import state as state_module
from airbyte_ops_webapp.auth import mock_session as mock_session_module
from airbyte_ops_webapp.models import (
    ConnectorOption,
    ConnectorRollout,
    ConnectorVersion,
    OverridePlan,
)
from airbyte_ops_webapp.pages.connector_version_manager import (
    _helpers as helpers_module,
)
from airbyte_ops_webapp.pages.connector_version_manager import (
    _mcp_tools as tools_module,
)
from airbyte_ops_webapp.pages.connector_version_manager import (
    page as page_module,
)
from airbyte_ops_webapp.pages.connector_version_manager.defaults import (
    CONNECTOR_VERSION_MANAGER_PATH,
    DEFAULT_CONNECTOR_QUERY,
    connector_version_manager_path,
    default_connector_query,
)
from airbyte_ops_webapp.services.connector_version_manager import (
    adapter as adapter_module,
)
from airbyte_ops_webapp.services.connector_version_manager.adapter import (
    OpsMcpAdapter,
    _cloud_scope_url,
    operation_result_to_json,
    preview_to_json,
)
from airbyte_ops_webapp.services.connector_version_manager.demo_mode import (
    MockPinningAdapter,
)


class FakeResponse:
    def __init__(
        self, status_code: int, payload: dict[str, object] | None = None
    ) -> None:
        self.status_code = status_code
        self.payload = payload or {}
        self.text = str(self.payload)

    def json(self) -> dict[str, object]:
        return self.payload


def test_search_connectors_matches_name() -> None:
    adapter = MockPinningAdapter()

    results = adapter.search_connectors("github")

    assert len(results) == 1
    assert results[0].name == "source-github"


def test_mock_recent_releases_are_sorted_newest_first() -> None:
    adapter = MockPinningAdapter()

    releases = adapter.list_recent_releases(limit=3)

    assert [release.connector_name for release in releases] == [
        "source-github",
        "source-postgres",
        "destination-snowflake",
    ]
    assert [release.docker_image_tag for release in releases] == [
        "1.9.4",
        "3.7.2",
        "3.3.1",
    ]


def test_ops_recent_releases_use_30_days_with_no_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict[str, object]] = []

    def fake_query_new_connector_releases(
        *,
        days: int,
        limit: int | None,
    ) -> list[dict[str, object]]:
        calls.append({"days": days, "limit": limit})
        return [
            {
                "version_id": "version-id",
                "actor_definition_id": "definition-id",
                "docker_repository": "airbyte/source-github",
                "docker_image_tag": "1.9.4",
                "release_stage": "generally_available",
                "last_published": "2026-06-10T00:00:00Z",
            }
        ]

    monkeypatch.setattr(
        adapter_module,
        "query_new_connector_releases",
        fake_query_new_connector_releases,
    )
    adapter = OpsMcpAdapter()

    releases = adapter.list_recent_releases()

    assert calls == [{"days": 30, "limit": None}]
    assert releases[0].connector_id == "definition-id"
    assert releases[0].connector_name == "source-github"


def test_ops_progressive_rollouts_use_no_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict[str, object]] = []

    def fake_query_connector_rollouts(
        *,
        active_only: bool,
        limit: int | None,
    ) -> list[dict[str, object]]:
        calls.append({"active_only": active_only, "limit": limit})
        return [
            {
                "rollout_id": "rollout-id",
                "actor_definition_id": "definition-id",
                "state": "initialized",
                "rc_docker_image_tag": "3.8.0-rc.12",
                "rc_docker_repository": "airbyte/source-postgres",
                "initial_docker_image_tag": "3.8.0",
                "current_target_rollout_pct": "50",
                "final_target_rollout_pct": "50",
                "created_at": "2026-06-10T00:00:00Z",
                "updated_at": "2026-06-11T00:00:00Z",
            }
        ]

    monkeypatch.setattr(
        adapter_module,
        "query_connector_rollouts",
        fake_query_connector_rollouts,
    )
    adapter = OpsMcpAdapter()

    rollouts = adapter.list_progressive_rollouts()

    assert calls == [{"active_only": True, "limit": None}]
    assert rollouts[0].connector_id == "definition-id"
    assert rollouts[0].connector_name == "source-postgres"


def test_ops_adapter_resolves_actor_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    connector = ConnectorOption(
        id="source-definition-id",
        name="source-github",
        connector_type="source",
        latest_version="1.9.4",
        docker_repository="airbyte/source-github",
    )

    def fake_post(
        url: str,
        *,
        json: dict[str, str],
        headers: dict[str, str],
        timeout: int,
    ) -> FakeResponse:
        if url.endswith("/sources/get"):
            return FakeResponse(
                200,
                {
                    "sourceDefinitionId": connector.id,
                    "workspaceId": "workspace-id",
                    "name": "My Source",
                },
            )
        if url.endswith("/workspaces/get"):
            return FakeResponse(
                200,
                {"organizationId": "organization-id", "name": "Test Workspace"},
            )
        raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(
        adapter_module.api_client, "_get_access_token", lambda **_: "token"
    )
    monkeypatch.setattr(adapter_module.api_client.requests, "post", fake_post)
    monkeypatch.setattr(
        adapter_module,
        "get_organization_info",
        lambda **_: SimpleNamespace(
            organization_name="Test Org",
            organization_id="organization-id",
        ),
    )

    resolution = OpsMcpAdapter(bearer_token="token").resolve_context_guid(
        connector=connector,
        context_guid="actor-id",
    )

    assert resolution.scope_type == "actor"
    assert resolution.scope_id == "actor-id"
    assert resolution.workspace_id == "workspace-id"
    assert resolution.organization_id == "organization-id"
    assert resolution.scope_name == "My Source"
    assert resolution.workspace_name == "Test Workspace"
    assert resolution.organization_name == "Test Org"
    assert resolution.actor_type == "source"


def test_ops_adapter_context_resolution_falls_through_validation_misses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    connector = ConnectorOption(
        id="source-definition-id",
        name="source-github",
        connector_type="source",
        latest_version="1.9.4",
        docker_repository="airbyte/source-github",
    )
    statuses_by_path = {
        "/sources/get": 404,
        "/workspaces/get": 422,
    }

    def fake_post(
        url: str,
        *,
        json: dict[str, str],
        headers: dict[str, str],
        timeout: int,
    ) -> FakeResponse:
        for path, status_code in statuses_by_path.items():
            if url.endswith(path):
                return FakeResponse(status_code)
        raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(
        adapter_module.api_client, "_get_access_token", lambda **_: "token"
    )
    monkeypatch.setattr(adapter_module.api_client.requests, "post", fake_post)
    monkeypatch.setattr(
        adapter_module,
        "get_organization_info",
        lambda **_: SimpleNamespace(
            organization_name="Fallthrough Org",
            organization_id="organization-id",
        ),
    )

    resolution = OpsMcpAdapter(bearer_token="token").resolve_context_guid(
        connector=connector,
        context_guid="organization-id",
    )

    assert resolution.scope_type == "organization"
    assert resolution.scope_id == "organization-id"
    assert resolution.organization_id == "organization-id"
    assert resolution.organization_name == "Fallthrough Org"


def test_default_connector_query_accepts_launch_arg_aliases() -> None:
    assert default_connector_query(query="destination-snowflake") == (
        "destination-snowflake"
    )
    assert default_connector_query(connector_name="source-postgres") == (
        "source-postgres"
    )
    assert default_connector_query(connector="source-github") == "source-github"
    assert default_connector_query() == DEFAULT_CONNECTOR_QUERY


def test_connector_version_manager_path_encodes_default_query() -> None:
    path = connector_version_manager_path("destination-snowflake")
    parsed = urllib.parse.urlparse(path)
    params = urllib.parse.parse_qs(parsed.query)

    assert parsed.path == CONNECTOR_VERSION_MANAGER_PATH
    assert params["query"] == ["destination-snowflake"]


def test_connector_version_manager_path_omits_query_when_empty() -> None:
    assert connector_version_manager_path() == CONNECTOR_VERSION_MANAGER_PATH


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


def test_connector_version_manager_does_not_prefill_without_args(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")

    app = page_module.connector_version_manager()

    assert app.state["query"] == ""
    assert app.state["default_connector_from_args"] is False
    assert app.state["selected_connector"]["id"] == ""
    assert app.state["versions"] == []


def test_connector_version_manager_auth_requires_bearer_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(state_module.MOCK_ONLY_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.AIRBYTE_BEARER_TOKEN_ENV_VAR, raising=False)
    monkeypatch.setenv(state_module.AIRBYTE_CLIENT_ID_ENV_VAR, "client-id")
    monkeypatch.setenv(state_module.AIRBYTE_CLIENT_SECRET_ENV_VAR, "client-secret")

    assert helpers_module.auth_available() is False
    assert helpers_module.auth_available("browser-oauth-token") is True


def test_connector_version_manager_adapter_prefers_browser_oauth_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(state_module.MOCK_ONLY_ENV_VAR, raising=False)
    monkeypatch.setenv(state_module.AIRBYTE_BEARER_TOKEN_ENV_VAR, "env-token")
    monkeypatch.setenv(state_module.AIRBYTE_CLIENT_ID_ENV_VAR, "client-id")
    monkeypatch.setenv(state_module.AIRBYTE_CLIENT_SECRET_ENV_VAR, "client-secret")

    adapter = helpers_module.get_adapter("browser-oauth-token")

    assert adapter.bearer_token == "browser-oauth-token"
    assert adapter.client_id is None
    assert adapter.client_secret is None


def test_recent_release_options_fall_back_when_query_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FailingReleasesAdapter(MockPinningAdapter):
        def list_recent_releases(self, **_kwargs: object) -> object:
            raise RuntimeError("database unavailable")

    monkeypatch.setattr(
        helpers_module, "get_adapter", lambda *_args: FailingReleasesAdapter()
    )

    assert helpers_module.recent_release_options() == [
        {"label": "Recent releases unavailable", "value": ""}
    ]


def test_progressive_rollout_options_fall_back_when_query_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FailingRolloutsAdapter(MockPinningAdapter):
        def list_progressive_rollouts(self, **_kwargs: object) -> object:
            raise RuntimeError("database unavailable")

    monkeypatch.setattr(
        helpers_module, "get_adapter", lambda *_args: FailingRolloutsAdapter()
    )

    assert helpers_module.progressive_rollout_options() == [
        {"label": "Progressive rollouts unavailable", "value": ""}
    ]


def test_admin_user_options_fall_back_when_query_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FailingAdminUsersAdapter(MockPinningAdapter):
        def list_instance_admin_users(self) -> object:
            raise RuntimeError("config api unavailable")

    monkeypatch.delenv(state_module.MOCK_ONLY_ENV_VAR, raising=False)
    monkeypatch.setattr(
        helpers_module, "get_adapter", lambda *_args: FailingAdminUsersAdapter()
    )

    options = helpers_module.admin_user_options()

    assert len(options) == 1
    assert options[0]["value"] == helpers_module.DEFAULT_ADMIN_USER_EMAIL


def test_rollout_rows_fall_back_when_query_fails() -> None:
    connector = ConnectorOption(
        id="source-postgres-id",
        name="source-postgres",
        connector_type="source",
        latest_version="3.8.0",
        docker_repository="airbyte/source-postgres",
    )

    class FailingRolloutsAdapter(MockPinningAdapter):
        def list_active_rollouts(self, _connector_id: str) -> object:
            raise RuntimeError("database unavailable")

    rows, error = helpers_module.rollout_rows_or_empty(
        FailingRolloutsAdapter(),
        connector,
    )

    assert rows == []
    assert error == "Progressive rollout status could not be loaded."


def test_connector_version_manager_initial_state_uses_resolved_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")
    monkeypatch.setattr(mock_session_module, "_oauth_authenticated", True)

    app = page_module.connector_version_manager(
        connector_name="source-github",
        scope_type="workspace",
        scope_id="actor_example",
    )

    assert app.state["scope_type"] == "actor"
    assert app.state["scope_id"] == "actor_example"
    assert app.state["actor_workspace_id"] == "workspace_example"
    assert app.state["resolved_context_label"] == '"Mock Source" Actor'


def test_connector_version_manager_tool_calls_have_error_handlers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")
    app_json = page_module.connector_version_manager(
        connector_name="source-github"
    ).to_json()
    tool_calls = []

    def collect_tool_calls(value) -> None:
        if isinstance(value, dict):
            if value.get("action") == "toolCall":
                tool_calls.append(value)
            for child in value.values():
                collect_tool_calls(child)
        elif isinstance(value, list):
            for child in value:
                collect_tool_calls(child)

    collect_tool_calls(app_json)

    assert [call["tool"] for call in tool_calls] == [
        "load_connector_version_context",
        "load_recent_releases_tab",
        "load_connector_version_context",
        "load_active_rollouts_tab",
        "load_connector_version_context",
        "load_pinned_versions_tab",
        # Filter chips (4 chips x 2 serialized branches + initial = 8 extra)
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_connector_version_context",
        # Rollout actions: advance, promote next stage, promote GA, cancel
        "advance_rollout",
        "load_connector_context",
        "promote_to_next_stage",
        "load_connector_context",
        "finalize_rollout",
        "load_connector_context",
        "finalize_rollout",
        "load_connector_context",
        "resolve_scope_guid",
        "remove_selected_pins",
        "load_version_pins",
        "resolve_scope_guid",
        "apply_override",
        "load_version_pins",
    ]
    for call in tool_calls:
        error_actions = call["onError"]
        assert {"action": "setState", "key": "is_loading", "value": False} in (
            error_actions
        )
        assert {"action": "setState", "key": "loading_message", "value": ""} in (
            error_actions
        )
        assert any(
            action["action"] == "setState"
            and action["key"] == "tool_error"
            and action["value"]
            for action in error_actions
        )
        assert any(action["action"] == "showToast" for action in error_actions)


def test_connector_version_manager_selector_has_four_tabs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")
    app_json = page_module.connector_version_manager(
        connector_name="source-github"
    ).to_json()
    serialized_app = json.dumps(app_json)

    assert "Latest Versions" in serialized_app
    assert "Recent Releases" in serialized_app
    assert "Active Rollouts" in serialized_app
    assert "Pinned Versions" in serialized_app


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
    assert "override_reason" in preview.required_approval_fields


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

    adapter = helpers_module.get_adapter()

    assert isinstance(adapter, MockPinningAdapter)
    assert adapter.bearer_token is None
    assert adapter.config_api_root == "mock://config-api"


def test_connector_version_manager_adapter_uses_env_bearer_token_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(state_module.MOCK_ONLY_ENV_VAR, raising=False)
    monkeypatch.setenv(state_module.AIRBYTE_CLIENT_ID_ENV_VAR, "client-id")
    monkeypatch.setenv(state_module.AIRBYTE_CLIENT_SECRET_ENV_VAR, "client-secret")
    monkeypatch.setenv(state_module.AIRBYTE_BEARER_TOKEN_ENV_VAR, "env-oauth-token")

    adapter = helpers_module.get_adapter()

    assert adapter.bearer_token == "env-oauth-token"
    assert adapter.client_id is None
    assert adapter.client_secret is None


def test_load_connector_context_returns_connector_when_scope_context_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FailingContextAdapter(MockPinningAdapter):
        def get_current_context(self, **_kwargs: object) -> object:
            raise PyAirbyteInputError(message="Unauthorized")

    adapter = FailingContextAdapter()
    connector = adapter.search_connectors("source-github")[0]
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")
    monkeypatch.setattr(mock_session_module, "_oauth_authenticated", True)
    monkeypatch.setattr(tools_module, "get_adapter", lambda *_args: adapter)

    result = tools_module.load_connector_context(connector.id)

    assert result["connector"]["name"] == "source-github"
    assert result["versions"]
    assert result["current_state"]["connector_name"] == "source-github"
    assert "rejected the scoped-configuration request" in result["context_error"]


def test_load_connector_context_skips_scoped_api_without_real_scope(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    connector = ConnectorOption(
        id="b4c5d105-31fd-4817-96b6-cb923bfc04cb",
        name="source-github",
        connector_type="source",
        latest_version="1.9.4",
        docker_repository="airbyte/source-github",
    )
    versions = (
        ConnectorVersion(
            version_id="github-194",
            docker_image_tag="1.9.4",
            docker_repository="airbyte/source-github",
            release_stage="generally_available",
            support_level="certified",
            cdk_version="python:6.44.1",
            language="python",
            last_published="2026-04-26T14:12:00Z",
        ),
    )

    class RealAdapterWithoutScope(OpsMcpAdapter):
        def get_connector(self, connector_id: str) -> ConnectorOption:
            assert connector_id == connector.id
            return connector

        def list_versions(self, connector_id: str) -> tuple[ConnectorVersion, ...]:
            assert connector_id == connector.id
            return versions

        def list_active_rollouts(
            self, connector_id: str
        ) -> tuple[ConnectorRollout, ...]:
            assert connector_id == connector.id
            return ()

        def get_current_context(self, **_kwargs: object) -> object:
            raise AssertionError("scoped Config API should not be called")

    monkeypatch.delenv(state_module.MOCK_ONLY_ENV_VAR, raising=False)
    monkeypatch.setattr(
        tools_module, "get_adapter", lambda *_args: RealAdapterWithoutScope()
    )

    result = tools_module.load_connector_context(
        connector.id,
        scope_id="workspace_example",
        auth_bearer_token="oauth-token",
    )

    assert result["connector"]["name"] == "source-github"
    assert result["versions"][0]["docker_image_tag"] == "1.9.4"
    assert result["versions"][0]["last_published_display"] == "2026-04-26 (Sun)"
    assert result["current_state"]["active_version"] == "1.9.4"
    assert "Enter a Context GUID" in result["context_error"]


def test_load_recent_release_context_selects_connector_and_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")

    result = tools_module.load_recent_release_context(
        "ef69ef6e-aa7f-4af1-a01d-ef775033524e|1.9.4",
        context_guid="workspace_example",
    )

    assert result["selected_connector_id"] == "ef69ef6e-aa7f-4af1-a01d-ef775033524e"
    assert result["target_version"] == "1.9.4"
    assert result["connector"]["name"] == "source-github"


def test_load_progressive_rollout_context_selects_connector_and_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")
    monkeypatch.setattr(mock_session_module, "_oauth_authenticated", True)

    result = tools_module.load_progressive_rollout_context(
        "b5ea17b1-f170-46dc-bc31-cc744ca984c1|3.8.0-rc.12",
        context_guid="workspace_example",
    )

    assert result["selected_connector_id"] == "b5ea17b1-f170-46dc-bc31-cc744ca984c1"
    assert result["target_version"] == "3.8.0-rc.12"
    assert result["connector"]["name"] == "source-postgres"
    assert result["resolved_context_label"] == '"Mock Workspace" Workspace'


def test_load_connector_context_returns_connector_when_versions_need_auth(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FailingVersionsAdapter(MockPinningAdapter):
        def list_versions(self, _connector_id: str) -> object:
            raise PyAirbyteInputError(message="Unauthorized")

    adapter = FailingVersionsAdapter()
    connector = adapter.search_connectors("source-github")[0]
    monkeypatch.delenv(state_module.MOCK_ONLY_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.AIRBYTE_BEARER_TOKEN_ENV_VAR, raising=False)
    monkeypatch.setattr(tools_module, "get_adapter", lambda *_args: adapter)

    result = tools_module.load_connector_context(connector.id)

    assert result["connector"]["name"] == "source-github"
    assert result["versions"] == []
    assert result["context_error"] == (
        "Sign in with Airbyte to load scoped configuration context."
    )


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


@pytest.mark.parametrize(
    "scope_type, scope_id, workspace_id, actor_type, expected_url",
    [
        pytest.param(
            "organization",
            "664c690e-5263-49ba-b01f-4a6759b3330a",
            "",
            "",
            "https://cloud.airbyte.com/organization/664c690e-5263-49ba-b01f-4a6759b3330a/settings/organization",
            id="organization",
        ),
        pytest.param(
            "workspace",
            "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "",
            "",
            "https://cloud.airbyte.com/workspaces/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            id="workspace",
        ),
        pytest.param(
            "actor",
            "11111111-2222-3333-4444-555555555555",
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "source",
            "https://cloud.airbyte.com/workspaces/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/source/11111111-2222-3333-4444-555555555555",
            id="actor-source",
        ),
        pytest.param(
            "actor",
            "11111111-2222-3333-4444-555555555555",
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "destination",
            "https://cloud.airbyte.com/workspaces/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/destination/11111111-2222-3333-4444-555555555555",
            id="actor-destination",
        ),
    ],
)
def test_cloud_scope_url(
    scope_type: str,
    scope_id: str,
    workspace_id: str,
    actor_type: str,
    expected_url: str,
) -> None:
    assert (
        _cloud_scope_url(
            scope_type=scope_type,
            scope_id=scope_id,
            workspace_id=workspace_id,
            actor_type=actor_type,
        )
        == expected_url
    )


@pytest.mark.parametrize(
    "scope_type, scope_id, workspace_id, actor_type, error_match",
    [
        pytest.param(
            "actor",
            "11111111-2222-3333-4444-555555555555",
            "",
            "source",
            "requires workspace_id",
            id="actor-missing-workspace",
        ),
        pytest.param(
            "actor",
            "11111111-2222-3333-4444-555555555555",
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "widget",
            "requires actor_type",
            id="actor-invalid-type",
        ),
        pytest.param(
            "actor",
            "11111111-2222-3333-4444-555555555555",
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "",
            "requires actor_type",
            id="actor-empty-type",
        ),
        pytest.param(
            "unknown",
            "11111111-2222-3333-4444-555555555555",
            "",
            "",
            "Unknown scope_type",
            id="unknown-scope-type",
        ),
    ],
)
def test_cloud_scope_url_errors(
    scope_type: str,
    scope_id: str,
    workspace_id: str,
    actor_type: str,
    error_match: str,
) -> None:
    with pytest.raises(ValueError, match=error_match):
        _cloud_scope_url(
            scope_type=scope_type,
            scope_id=scope_id,
            workspace_id=workspace_id,
            actor_type=actor_type,
        )
