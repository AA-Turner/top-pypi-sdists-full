"""Tests for the connector pinning adapter."""

import json
import urllib.parse
from types import SimpleNamespace

import google.auth.exceptions
import pytest
from airbyte.exceptions import PyAirbyteInputError
from airbyte_ops_mcp.connector_ops.rollouts._helpers import RolloutConfiguration

from airbyte_ops_webapp import state as state_module
from airbyte_ops_webapp.auth import mock_session as mock_session_module
from airbyte_ops_webapp.models import (
    ConnectorOption,
    ConnectorRollout,
    ConnectorVersion,
    OverridePlan,
    RolloutSyncSummary,
    TierPopulationFactors,
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
        "source-github",
        "source-postgres",
    ]
    assert [release.docker_image_tag for release in releases] == [
        "1.10.0-rc.1",
        "1.9.4",
        "3.7.2",
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


def test_mock_adapter_list_yanked_versions() -> None:
    adapter = MockPinningAdapter()

    yanked = adapter.list_yanked_versions()

    assert [(y.connector_name, y.docker_image_tag) for y in yanked] == [
        ("source-github", "1.9.3"),
        ("destination-snowflake", "3.2.0"),
    ]
    assert yanked[0].connector_id == "ef69ef6e-aa7f-4af1-a01d-ef775033524e"


@pytest.mark.parametrize(
    "connector_name, version, expect_marker",
    [
        pytest.param("source-github", "1.9.3", True, id="yanked-github"),
        pytest.param("destination-snowflake", "3.2.0", True, id="yanked-snowflake"),
        pytest.param("source-github", "1.9.4", False, id="not-yanked"),
    ],
)
def test_mock_adapter_get_yank_marker(
    connector_name: str,
    version: str,
    expect_marker: bool,
) -> None:
    adapter = MockPinningAdapter()

    marker = adapter.get_yank_marker(connector_name, version)

    if not expect_marker:
        assert marker is None
        return
    assert marker is not None
    assert marker.connector_name == connector_name
    assert marker.docker_image_tag == version
    assert marker.yanked_at
    # Raw marker text mirrors the version-yank.yml shape.
    assert "yanked: true" in marker.raw
    assert f"yanked_at: '{marker.yanked_at}'" in marker.raw


def test_mock_yanked_versions_are_not_active_rollout_versions() -> None:
    """Yanked mock versions must be mutually exclusive from rollout RC versions.

    Guards the demo guarantee that clicking a yanked version shows Version Yank
    Detail but not the Rollout Status detail (which gates on `rc == selected`).
    """
    adapter = MockPinningAdapter()

    rollout_rc_versions = {
        (rollout.connector_id, rollout.rc_docker_image_tag)
        for rollouts in adapter.rollouts.values()
        for rollout in rollouts
    }
    yanked_versions = {
        (row.connector_id, row.docker_image_tag)
        for row in adapter.list_yanked_versions()
    }

    assert yanked_versions.isdisjoint(rollout_rc_versions)


@pytest.mark.parametrize(
    "version_tag, expect_yanked",
    [
        pytest.param("1.9.3", True, id="yanked-version"),
        pytest.param("1.9.4", False, id="non-yanked-version"),
    ],
)
def test_load_connector_version_context_sets_yank_detail(
    monkeypatch: pytest.MonkeyPatch,
    version_tag: str,
    expect_yanked: bool,
) -> None:
    adapter = MockPinningAdapter()
    connector = adapter.search_connectors("source-github")[0]
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")
    monkeypatch.setattr(mock_session_module, "_oauth_authenticated", True)
    monkeypatch.setattr(tools_module, "get_adapter", lambda *_args: adapter)

    result = tools_module.load_connector_version_context(
        connector_id=connector.id,
        version_tag=version_tag,
    )

    assert result.selected_version_yanked is expect_yanked
    if expect_yanked:
        assert result.selected_version_yank_yanked_at
        assert result.selected_version_yank_yanked_at_display
        assert "yanked: true" in result.selected_version_yank_raw
    else:
        assert result.selected_version_yank_raw == ""
        assert result.selected_version_yank_yanked_at == ""


def test_unyank_connector_version_mock_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")

    result = tools_module.unyank_connector_version("source-github", "1.9.3")

    assert result.rollout_action_success is True
    assert "unyank" in result.rollout_action_result.lower()


def test_unyank_connector_version_dispatches_workflow(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(state_module.MOCK_ONLY_ENV_VAR, raising=False)
    captured: dict[str, object] = {}

    def fake_dispatch(**kwargs: object) -> object:
        captured.update(kwargs)
        return SimpleNamespace(run_url="https://run", workflow_url="https://wf")

    monkeypatch.setattr(
        tools_module, "resolve_ci_trigger_github_token", lambda: "token"
    )
    monkeypatch.setattr(tools_module, "trigger_workflow_dispatch", fake_dispatch)

    result = tools_module.unyank_connector_version("source-github", "1.9.3")

    assert result.rollout_action_success is True
    assert captured["inputs"] == {
        "connector-name": "source-github",
        "version": "1.9.3",
        "store": tools_module.YANK_STORE,
        "unyank": "true",
    }


def test_ops_adapter_list_yanked_versions_resolves_connector_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from airbyte_ops_mcp.registry.yank import YankedVersion as CoreYankedVersion

    def fake_list_yanked_versions(bucket_name: str) -> list[CoreYankedVersion]:
        return [
            CoreYankedVersion(
                connector_name="source-github",
                version="1.9.3",
                yanked_at="2026-06-18T14:30:00Z",
                reason="bad release",
            ),
            CoreYankedVersion(connector_name="source-missing", version="0.0.1"),
        ]

    def fake_resolve(name: str) -> str:
        if name == "source-missing":
            raise PyAirbyteInputError(message="not found")
        return "github-definition-id"

    monkeypatch.setattr(
        adapter_module, "list_yanked_versions", fake_list_yanked_versions
    )
    monkeypatch.setattr(
        adapter_module,
        "resolve_canonical_name_to_definition_id",
        fake_resolve,
    )
    adapter = OpsMcpAdapter()

    yanked = adapter.list_yanked_versions()

    assert yanked[0].connector_id == "github-definition-id"
    assert yanked[0].reason == "bad release"
    assert yanked[1].connector_id == ""


def test_yanked_version_rows_adds_display_date(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        helpers_module, "get_adapter", lambda *_args: MockPinningAdapter()
    )

    rows = helpers_module.yanked_version_rows()

    assert rows[0]["connector_name"] == "source-github"
    assert rows[0]["yanked_at_display"] == "2026-06-18 (Thu)"


def test_yanked_version_rows_empty_when_query_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FailingYankAdapter(MockPinningAdapter):
        def list_yanked_versions(self) -> object:
            raise RuntimeError("gcs unavailable")

    monkeypatch.setattr(
        helpers_module, "get_adapter", lambda *_args: FailingYankAdapter()
    )

    assert helpers_module.yanked_version_rows() == []


def test_load_yanked_versions_tab_returns_rows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        helpers_module, "get_adapter", lambda *_args: MockPinningAdapter()
    )

    result = tools_module.load_yanked_versions_tab()

    assert [row["connector_name"] for row in result.rows] == [
        "source-github",
        "destination-snowflake",
    ]


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
        # Selector tabs (default tab is active-rollouts)
        "load_active_rollouts_tab",
        "load_connector_version_context",
        "load_recent_releases_tab",
        "load_connector_version_context",
        "load_pinned_versions_tab",
        # Origin filter chips (4 chips x 2 serialized branches + initial)
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_pinned_versions_tab",
        "load_connector_version_context",
        # Yanked versions tab (lazy load + row-click context branches)
        "load_yanked_versions_tab",
        "load_connector_version_context",
        "load_connector_version_context",
        # Organization Pins tab: org search + two-step aggregate/detail loaders
        "search_orgs_workspaces",
        "load_org_pin_versions",
        "load_org_pins",
        # Rollout actions: advance, promote next stage, promote GA, cancel
        "advance_rollout",
        "load_connector_context",
        "promote_to_next_stage",
        "load_connector_context",
        "finalize_rollout",
        "load_connector_context",
        "finalize_rollout",
        "load_connector_context",
        # Yank action (shown only when no active rollout)
        "yank_connector_version",
        "load_connector_context",
        # Unyank action (shown when the selected version is yanked)
        "unyank_connector_version",
        "load_connector_context",
        # Pin actions
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

    assert "Default Versions" in serialized_app
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

    assert result.connector.name == "source-github"
    assert result.versions
    assert result.current_state["connector_name"] == "source-github"
    assert "rejected the scoped-configuration request" in result.context_error


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

    assert result.connector.name == "source-github"
    assert result.versions[0]["docker_image_tag"] == "1.9.4"
    assert result.versions[0]["last_published_display"] == "2026-04-26 (Sun)"
    assert result.current_state["active_version"] == "1.9.4"
    assert "Enter a Context GUID" in result.context_error


def test_load_recent_release_context_selects_connector_and_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")

    result = tools_module.load_recent_release_context(
        "ef69ef6e-aa7f-4af1-a01d-ef775033524e|1.9.4",
        context_guid="workspace_example",
    )

    assert result.selected_connector_id == "ef69ef6e-aa7f-4af1-a01d-ef775033524e"
    assert result.target_version == "1.9.4"
    assert result.connector.name == "source-github"


def test_load_progressive_rollout_context_selects_connector_and_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(state_module.MOCK_ONLY_ENV_VAR, "1")
    monkeypatch.setattr(mock_session_module, "_oauth_authenticated", True)

    result = tools_module.load_progressive_rollout_context(
        "b5ea17b1-f170-46dc-bc31-cc744ca984c1|3.8.0-rc.12",
        context_guid="workspace_example",
    )

    assert result.selected_connector_id == "b5ea17b1-f170-46dc-bc31-cc744ca984c1"
    assert result.target_version == "3.8.0-rc.12"
    assert result.connector.name == "source-postgres"
    assert result.resolved_context_label == '"Mock Workspace" Workspace'


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

    assert result.connector.name == "source-github"
    assert result.versions == []
    assert result.context_error == (
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


def _factors(
    *,
    pinned: int,
    gate_pass: int,
    off_version: int = 0,
    no_recent_sync: int = 0,
    failed: int = 0,
) -> TierPopulationFactors:
    """Build a self-consistent `TierPopulationFactors` for card tests.

    `active = pinned + off_version + unpinned` where `unpinned = gate_pass +
    no_recent_sync + failed`; `eligible = pinned + gate_pass` mirrors the
    backend's `nActorsEligibleOrAlreadyPinned`."""
    unpinned = gate_pass + no_recent_sync + failed
    active = pinned + off_version + unpinned
    return TierPopulationFactors(
        active=active,
        pinned_to_rollout=pinned,
        off_version_pinned=off_version,
        unpinned=unpinned,
        gate_pass=gate_pass,
        gate_excluded_failed=failed,
        gate_excluded_no_recent_sync=no_recent_sync,
        addressable=active,
        addressable_gated=pinned + gate_pass,
    )


def test_build_rollout_summary_uses_active_only_total_and_tier_eligible() -> None:
    """One active-only total up top; a started tier's realized `Pinned` coverage
    comes from the active-only population (`factors` / `pinned_by_tier`), NOT the
    inflated rollout-scan `num_pinned`/`num_eligible`. Not-started tiers still
    surface their gated-eligible count so future stages can be sized."""
    active_rollouts = [
        {
            "tier": "TIER_2",
            "rollout_id": "r-t2",
            "state": "in_progress",
            "current_target_rollout_pct": "100",
        }
    ]
    tier_summaries = {
        "TIER_2": RolloutSyncSummary(
            health="8 healthy | 0 unhealthy | 1 awaiting | 11 disabled",
            num_pinned=575,
            num_eligible=193,
            num_actors=893,
            num_healthy=8,
            num_unhealthy=0,
        )
    }
    summary = helpers_module.build_rollout_summary(
        active_rollouts,
        total_actors_display="280",
        tier_summaries=tier_summaries,
        eligible_by_tier={"TIER_2": 246, "TIER_1": 6, "TIER_0": 28},
        pinned_by_tier={"TIER_2": 157, "TIER_1": 0, "TIER_0": 0},
        factors_by_tier={"TIER_2": _factors(pinned=157, gate_pass=89)},
    )

    # Single connector-wide total reflects the active-only population, not 893.
    assert summary["total_actors_display"] == "280"

    cards = {c["tier_value"]: c for c in summary["tier_cards"]}
    t2 = cards["TIER_2"]
    assert t2["started"] is True
    assert t2["status_label"] == "Complete"
    # Realized coverage from active-only counts (157/246 = 64%), never the scan's
    # inflated 575/193.
    assert t2["pinned_summary"] == "157 of 246 eligible (64%)"
    assert t2["eligible_header"] == "246 Eligible Actors"
    # Health reconciles with the active-only pinned count: healthy + unhealthy +
    # awaiting = 157 (the pinned cohort). Awaiting absorbs the remainder.
    elig = [r["text"] for r in t2["eligible_rows"]]
    assert any("8 succeeding" in t for t in elig)
    assert any("0 failing" in t for t in elig)
    assert any("149 awaiting results" in t for t in elig)

    # Not-started tiers surface their eligible count for stage planning.
    assert cards["TIER_1"]["started"] is False
    assert cards["TIER_1"]["eligible_header"] == "6 Eligible Actors"
    assert cards["TIER_0"]["tier_label"] == "Tier 0"
    assert cards["TIER_0"]["eligible_header"] == "28 Eligible Actors"


def test_build_rollout_summary_pinned_never_exceeds_eligible() -> None:
    """Regression for source-faker: the rollout scan reported 575 pinned while
    only 73 actors were active/eligible. The card uses the active-only counts
    (`factors`) so the numerator can't exceed the denominator."""
    active_rollouts = [
        {
            "tier": "TIER_2",
            "rollout_id": "r-t2",
            "state": "in_progress",
            "current_target_rollout_pct": "50",
        }
    ]
    tier_summaries = {
        "TIER_2": RolloutSyncSummary(
            health="2 healthy | 0 unhealthy | 0 awaiting | 573 disabled",
            num_pinned=575,
            num_eligible=575,
            num_actors=575,
            num_healthy=2,
            num_unhealthy=0,
        )
    }
    summary = helpers_module.build_rollout_summary(
        active_rollouts,
        total_actors_display="73",
        tier_summaries=tier_summaries,
        eligible_by_tier={"TIER_2": 73, "TIER_1": 0, "TIER_0": 0},
        pinned_by_tier={"TIER_2": 36, "TIER_1": 0, "TIER_0": 0},
        factors_by_tier={"TIER_2": _factors(pinned=36, gate_pass=37)},
    )
    t2 = {c["tier_value"]: c for c in summary["tier_cards"]}["TIER_2"]
    assert t2["pinned_summary"] == "36 of 73 eligible (49%)"


def test_build_rollout_summary_health_reconciles_with_active_pinned() -> None:
    """Regression for source-faker: the health counts must be recomputed over the
    active-only pinned population, so succeeding + failing + awaiting == pinned.
    Awaiting absorbs the active-pinned actors with no result yet; dormant pinned
    actors are not shown."""
    active_rollouts = [
        {
            "tier": "TIER_2",
            "rollout_id": "r-t2",
            "state": "in_progress",
            "current_target_rollout_pct": "50",
        }
    ]
    tier_summaries = {
        "TIER_2": RolloutSyncSummary(
            health="2 healthy | 0 unhealthy | 0 awaiting | 573 disabled",
            num_pinned=575,
            num_eligible=575,
            num_actors=575,
            num_healthy=2,
            num_unhealthy=0,
        )
    }
    summary = helpers_module.build_rollout_summary(
        active_rollouts,
        total_actors_display="73",
        tier_summaries=tier_summaries,
        eligible_by_tier={"TIER_2": 73, "TIER_1": 0, "TIER_0": 0},
        pinned_by_tier={"TIER_2": 9, "TIER_1": 0, "TIER_0": 0},
        factors_by_tier={"TIER_2": _factors(pinned=9, gate_pass=64)},
    )
    t2 = {c["tier_value"]: c for c in summary["tier_cards"]}["TIER_2"]
    assert t2["pinned_summary"] == "9 of 73 eligible (12%)"
    # succeeding(2) + failing(0) + awaiting(7) = 9 = pinned.
    elig = [r["text"] for r in t2["eligible_rows"]]
    assert any("2 succeeding" in t for t in elig)
    assert any("0 failing" in t for t in elig)
    assert any("7 awaiting results" in t for t in elig)


def test_format_pinned_pct_uses_float_division_and_one_decimal() -> None:
    """The rollout percentage is the realized pinned/eligible ratio, computed
    with float division to one decimal place. Regression for `1 / 7` rendering a
    truncated `0%` (integer division) instead of `14.3%`; `0` eligible has no
    ratio, so it renders `N/A` rather than a misleading `0.0%`."""
    assert helpers_module.format_pinned_pct(1, 7) == "14.3%"
    assert helpers_module.format_pinned_pct(20, 20) == "100.0%"
    assert helpers_module.format_pinned_pct(0, 7) == "0.0%"
    assert helpers_module.format_pinned_pct(3, 0) == "N/A"


def test_build_rollout_summary_realized_coverage_is_pinned_over_eligible() -> None:
    """The compact `Pinned` line shows realized coverage — `1 of 7 eligible
    (14%)` — computed as pinned/eligible from the active-only population, distinct
    from the backend `Deployed` stage percentage."""
    active_rollouts = [
        {
            "tier": "TIER_2",
            "rollout_id": "r-t2",
            "state": "in_progress",
            "current_target_rollout_pct": "20",
        }
    ]
    tier_summaries = {
        "TIER_2": RolloutSyncSummary(
            health="1 healthy | 0 unhealthy | 0 awaiting | 6 disabled",
            num_pinned=7,
            num_eligible=7,
            num_actors=7,
            num_healthy=1,
            num_unhealthy=0,
        )
    }
    summary = helpers_module.build_rollout_summary(
        active_rollouts,
        total_actors_display="7",
        tier_summaries=tier_summaries,
        eligible_by_tier={"TIER_2": 7, "TIER_1": 0, "TIER_0": 0},
        pinned_by_tier={"TIER_2": 1, "TIER_1": 0, "TIER_0": 0},
        factors_by_tier={"TIER_2": _factors(pinned=1, gate_pass=6)},
    )
    t2 = {c["tier_value"]: c for c in summary["tier_cards"]}["TIER_2"]
    assert t2["deployed_display"] == "20%"
    assert t2["pinned_summary"] == "1 of 7 eligible (14%)"


@pytest.mark.parametrize(
    "config_dict,expected",
    [
        pytest.param(
            {
                "defaultRolloutMode": "autopilot",
                "autopilotConfig": {"strategy": "fast"},
            },
            "ON (Fast)",
            id="autopilot_fast",
        ),
        pytest.param(
            {
                "defaultRolloutMode": "autopilot",
                "autopilotConfig": {"strategy": "slow"},
            },
            "ON (Slow)",
            id="autopilot_slow",
        ),
        pytest.param(
            {
                "defaultRolloutMode": "autopilot",
                "autopilotConfig": {"strategy": "default"},
            },
            "ON (Fast)",
            id="autopilot_default_resolves_to_fast",
        ),
        pytest.param(
            {"defaultRolloutMode": "autopilot"},
            "ON (Fast)",
            id="autopilot_no_config_defaults_to_fast",
        ),
        pytest.param(
            {"defaultRolloutMode": "manual"},
            "OFF",
            id="manual_is_off",
        ),
    ],
)
def test_autopilot_display_includes_strategy(
    monkeypatch: pytest.MonkeyPatch,
    config_dict: dict[str, object],
    expected: str,
) -> None:
    """The Autopilot line shows the strategy suffix (`ON (Fast)` / `ON (Slow)`)
    when autopilot is enabled, and `OFF` (no suffix) otherwise. `default`
    strategy and a missing `autopilotConfig` both resolve to `Fast`."""
    config = RolloutConfiguration.model_validate(config_dict)
    monkeypatch.setattr(
        helpers_module, "get_connector_rollout_config", lambda *_a, **_k: config
    )
    assert helpers_module._autopilot_display("conn-id", "1.0.0") == expected


def test_autopilot_display_off_when_config_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A registry lookup failure degrades to `OFF` rather than raising."""

    def _raise(*_a: object, **_k: object) -> object:
        raise RuntimeError("registry unavailable")

    monkeypatch.setattr(helpers_module, "get_connector_rollout_config", _raise)
    assert helpers_module._autopilot_display("conn-id", "1.0.0") == "OFF"


def test_get_connector_population_propagates_tier_query_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A GCS tier-refresh `RuntimeError` during `summarize_population` must
    propagate as a hard failure rather than degrading to a zeroed per-tier
    breakdown that would misrepresent a real population as empty."""
    monkeypatch.setattr(
        adapter_module,
        "query_actor_population_by_org",
        lambda **_: [
            {"organization_id": "o1", "actor_count": 30, "pinned_actor_count": 0},
            {"organization_id": "o2", "actor_count": 12, "pinned_actor_count": 2},
        ],
    )

    monkeypatch.setattr(
        adapter_module,
        "get_gcp_credentials_for_tier_gcs_ro",
        object,
    )

    def _raise_tier_error(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("GCS tier refresh failed and no stale cache")

    monkeypatch.setattr(adapter_module, "summarize_population", _raise_tier_error)

    with pytest.raises(RuntimeError, match="GCS tier refresh failed"):
        OpsMcpAdapter().get_connector_population("def-id", is_destination=False)


def test_get_connector_population_maps_eligible_by_tier(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When tier data is available, each tier's eligible count is its
    job-status-*gated* audience (`addressable_gated_by_tier` = the backend's
    `nActorsEligibleOrAlreadyPinned`: gate_pass + pinned-to-rollout), and pinned
    is the active actors pinned to *this* RC (`pinned_to_version_active_by_tier`),
    so `pinned <= eligible` per tier. `total_eligible` is their sum."""
    captured: dict[str, object] = {}

    def _fake_query(**kwargs: object) -> list[dict[str, object]]:
        captured["target_version_id"] = kwargs.get("target_version_id")
        captured["rollout_created_at"] = kwargs.get("rollout_created_at")
        return [{"organization_id": "o1", "actor_count": 35, "pinned_actor_count": 7}]

    monkeypatch.setattr(adapter_module, "query_actor_population_by_org", _fake_query)
    sentinel_credentials = object()

    def _fake_creds() -> object:
        captured["creds_called"] = True
        return sentinel_credentials

    monkeypatch.setattr(
        adapter_module, "get_gcp_credentials_for_tier_gcs_ro", _fake_creds
    )

    # Active fleet is 35, but the eligible denominator is the gated audience
    # (`addressable_gated_by_tier` = gate_pass + pinned-to-rollout): Tier-2 = 13
    # (8 + 5), Tier-1 = 10, Tier-0 = 5. The per-tier eligibles therefore sum to
    # 28 (< total_active) — off-version pins, recent-failure, and no-recent-sync
    # actors are all excluded from the gated set.
    fake_summary = SimpleNamespace(
        active_by_tier=SimpleNamespace(
            tier_2_count=20, tier_1_count=10, tier_0_count=5
        ),
        eligible_by_tier=SimpleNamespace(
            tier_2_count=13, tier_1_count=10, tier_0_count=5
        ),
        pinned_any_by_tier=SimpleNamespace(
            tier_2_count=7, tier_1_count=0, tier_0_count=0
        ),
        addressable_by_tier=SimpleNamespace(
            tier_2_count=18, tier_1_count=10, tier_0_count=5
        ),
        pinned_to_version_active_by_tier=SimpleNamespace(
            tier_2_count=5, tier_1_count=0, tier_0_count=0
        ),
        off_version_pinned_by_tier=SimpleNamespace(
            tier_2_count=2, tier_1_count=0, tier_0_count=0
        ),
        gate_pass_by_tier=SimpleNamespace(
            tier_2_count=8, tier_1_count=10, tier_0_count=5
        ),
        gate_excluded_failed_by_tier=SimpleNamespace(
            tier_2_count=2, tier_1_count=0, tier_0_count=0
        ),
        gate_excluded_no_recent_sync_by_tier=SimpleNamespace(
            tier_2_count=3, tier_1_count=0, tier_0_count=0
        ),
        addressable_gated_by_tier=SimpleNamespace(
            tier_2_count=13, tier_1_count=10, tier_0_count=5
        ),
    )

    def _fake_summarize(*_args: object, **kwargs: object) -> object:
        captured["credentials"] = kwargs.get("credentials")
        return fake_summary

    monkeypatch.setattr(adapter_module, "summarize_population", _fake_summarize)

    population = OpsMcpAdapter().get_connector_population(
        "def-id",
        is_destination=False,
        target_version_id="rc-version-123",
    )

    assert population.total_active == 35
    # Eligible is the gated audience (gate_pass + pinned-to-rollout).
    assert population.eligible_tier_2 == 13
    assert population.eligible_tier_1 == 10
    assert population.eligible_tier_0 == 5
    # Pinned is the active actors pinned to *this* RC, a subset of eligible.
    assert population.pinned_tier_2 == 5
    assert population.pinned_tier_1 == 0
    assert population.pinned_tier_0 == 0
    assert population.pinned_tier_2 <= population.eligible_tier_2
    # The gated per-tier eligibles sum to less than the connector-wide active
    # total (that gap is off-version + failed + no-recent-sync actors), and the
    # headline `total_eligible` equals that sum so the cards reconcile.
    assert (
        population.eligible_tier_2
        + population.eligible_tier_1
        + population.eligible_tier_0
        == 28
    )
    assert population.total_eligible == 28
    assert population.tier_resolution_available is True
    # The full distinct-factor breakdown is surfaced per tier (nothing
    # collapsed). The gated eligible denominator is displayed; `addressable` is
    # still carried on the factors for the eligible fallback but is no longer
    # shown as its own row.
    t2 = population.factors_tier_2
    assert t2 is not None
    assert t2.active == 20
    assert t2.pinned_to_rollout == 5
    assert t2.off_version_pinned == 2
    # `active = pinned + off-version + unpinned`.
    assert t2.unpinned == 13
    # The job-status gate partitions the unpinned set exactly.
    assert (
        t2.gate_pass + t2.gate_excluded_failed + t2.gate_excluded_no_recent_sync
        == t2.unpinned
    )
    assert t2.gate_pass == 8
    assert t2.gate_excluded_failed == 2
    assert t2.gate_excluded_no_recent_sync == 3
    # The gated eligible denominator (gate_pass + pinned) is displayed; the raw
    # addressable value is still carried for the fallback.
    assert t2.addressable == 18
    assert t2.addressable_gated == 13
    # The rollout's RC version id is threaded through to the population query.
    assert captured["target_version_id"] == "rc-version-123"
    # Tier resolution runs under the runtime service-account (ADC) credentials.
    assert captured["creds_called"] is True
    assert captured["credentials"] is sentinel_credentials


@pytest.mark.parametrize(
    "error",
    [
        pytest.param(RuntimeError("gcs unavailable"), id="runtime-error"),
        pytest.param(
            google.auth.exceptions.GoogleAuthError("no ADC credentials"),
            id="google-auth-error",
        ),
    ],
)
def test_get_connector_population_propagates_tier_gcs_failure(
    monkeypatch, error: Exception
) -> None:
    """A GCS credential/read failure during tier resolution must propagate
    as a hard failure rather than degrading to a zeroed `0 of 0` breakdown that
    misrepresents a real population as empty."""

    def _fake_query(**_kwargs: object) -> list[dict[str, object]]:
        return [{"organization_id": "o1", "actor_count": 35, "pinned_actor_count": 7}]

    monkeypatch.setattr(adapter_module, "query_actor_population_by_org", _fake_query)

    def _raise_creds() -> object:
        raise error

    monkeypatch.setattr(
        adapter_module, "get_gcp_credentials_for_tier_gcs_ro", _raise_creds
    )

    with pytest.raises(type(error)):
        OpsMcpAdapter().get_connector_population(
            "def-id",
            is_destination=False,
            target_version_id="rc-version-123",
        )


def test_format_ratio_pct_rounds_and_handles_edges() -> None:
    """`format_ratio_pct` renders compact whole-number percentages and lets the
    caller choose the 0-of-0 convention (`100%` for started coverage, `0%` for a
    failure ratio). A non-zero sub-1% ratio never reads a misleading `0%`."""
    fr = helpers_module.format_ratio_pct
    assert fr(10, 14) == "71%"
    assert fr(6, 10) == "60%"
    assert fr(0, 10) == "0%"
    assert fr(1, 500) == "<1%"
    assert fr(0, 0) == "\u2014"
    assert fr(0, 0, empty="100%") == "100%"
    assert fr(0, 0, empty="0%") == "0%"


def test_tier_rollout_status_maps_state_to_glyph() -> None:
    """The status glyph reflects the rollout `state`: no/initialized rollout reads
    Not started, paused reads Paused, failures win over deployed %, 100%-clean
    reads Complete, otherwise In progress."""
    status = helpers_module.tier_rollout_status
    assert (
        status(has_rollout=False, state="", deployed_pct=0, failing=0)[1]
        == "Not started"
    )
    assert (
        status(has_rollout=True, state="initialized", deployed_pct=0, failing=0)[1]
        == "Not started"
    )
    assert (
        status(has_rollout=True, state="paused", deployed_pct=25, failing=0)[1]
        == "Paused"
    )
    assert (
        status(has_rollout=True, state="in_progress", deployed_pct=100, failing=1)[1]
        == "Attention"
    )
    assert (
        status(has_rollout=True, state="in_progress", deployed_pct=100, failing=0)[1]
        == "Complete"
    )
    assert (
        status(has_rollout=True, state="in_progress", deployed_pct=50, failing=0)[1]
        == "In progress"
    )


def test_build_breakdown_columns_two_columns_reconcile() -> None:
    """`build_breakdown_columns` splits actors into Eligible / Ineligible columns
    whose headers sum to `active`. Eligible subdivides into pinned (by health) and
    not-yet-pinned; Ineligible lists off-version pins first, then no-recent-sync
    and recent-failure. Percentages: pinned/not-yet-pinned share of eligible,
    health rows share of pinned."""
    factors = TierPopulationFactors(
        active=84,
        pinned_to_rollout=10,
        off_version_pinned=2,
        unpinned=72,
        gate_pass=4,
        gate_excluded_failed=1,
        gate_excluded_no_recent_sync=67,
        addressable=82,
        addressable_gated=14,
    )
    cols = helpers_module.build_breakdown_columns(
        factors, succeeding=6, failing=0, awaiting=4
    )
    assert cols["eligible_header"] == "14 Eligible Actors"
    assert cols["ineligible_header"] == "70 Ineligible"
    elig = [r["text"] for r in cols["eligible_rows"]]
    assert any("10 pinned (71%)" in t for t in elig)
    assert any("6 succeeding (60%)" in t for t in elig)
    assert any("0 failing (0%)" in t for t in elig)
    assert any("4 awaiting results (40%)" in t for t in elig)
    assert any("4 not yet pinned (29%)" in t for t in elig)
    inelig = [r["text"] for r in cols["ineligible_rows"]]
    assert "2 pinned to another version" in inelig[0]
    assert any("67 no recent sync" in t for t in inelig)
    assert any("1 recent failure" in t for t in inelig)


def test_build_breakdown_columns_omits_health_subgroup_when_absent() -> None:
    """Without post-pin health counts, the pinned row renders with no
    succeeding/failing/awaiting subrows."""
    factors = TierPopulationFactors(
        active=5,
        pinned_to_rollout=2,
        unpinned=3,
        gate_pass=3,
        addressable=5,
        addressable_gated=5,
    )
    cols = helpers_module.build_breakdown_columns(factors)
    elig = [r["text"] for r in cols["eligible_rows"]]
    assert any("2 pinned" in t for t in elig)
    assert not any("succeeding" in t for t in elig)


def test_build_rollout_summary_card_fields() -> None:
    """A started tier card exposes the status glyph, the compact Deployed/Pinned/
    Failed line values, and the two-column breakdown headers. A 100%-deployed,
    no-failure tier reads Complete."""
    factors = TierPopulationFactors(
        active=84,
        pinned_to_rollout=10,
        off_version_pinned=2,
        unpinned=72,
        gate_pass=4,
        gate_excluded_failed=1,
        gate_excluded_no_recent_sync=67,
        addressable=82,
        addressable_gated=14,
    )
    summary = helpers_module.build_rollout_summary(
        [
            {
                "tier": "TIER_2",
                "rollout_id": "r-t2",
                "state": "in_progress",
                "current_target_rollout_pct": "100",
            }
        ],
        tier_summaries={
            "TIER_2": RolloutSyncSummary(
                health="6 healthy | 0 unhealthy | 4 awaiting",
                num_healthy=6,
                num_unhealthy=0,
            )
        },
        pinned_by_tier={"TIER_2": 10},
        eligible_by_tier={"TIER_2": 14},
        factors_by_tier={"TIER_2": factors},
    )
    t2 = {c["tier_value"]: c for c in summary["tier_cards"]}["TIER_2"]
    assert t2["started"] is True
    assert t2["status_label"] == "Complete"
    assert t2["deployed_display"] == "100%"
    assert t2["pinned_summary"] == "10 of 14 eligible (71%)"
    assert t2["failed_summary"] == "0 of 10 pinned (0%)"
    assert t2["eligible_header"] == "14 Eligible Actors"
    assert t2["ineligible_header"] == "70 Ineligible"


def test_build_rollout_summary_not_started_tier_marked() -> None:
    """A tier with no rollout row reads Not started with `—` deployed, yet still
    surfaces its gated-eligible actor count so future stages can be sized."""
    factors = TierPopulationFactors(
        active=2,
        pinned_to_rollout=0,
        unpinned=2,
        gate_pass=1,
        gate_excluded_no_recent_sync=1,
        addressable=2,
        addressable_gated=1,
    )
    summary = helpers_module.build_rollout_summary(
        [
            {
                "tier": "TIER_2",
                "rollout_id": "r-t2",
                "state": "in_progress",
                "current_target_rollout_pct": "50",
            }
        ],
        eligible_by_tier={"TIER_0": 2},
        factors_by_tier={"TIER_0": factors},
    )
    t0 = {c["tier_value"]: c for c in summary["tier_cards"]}["TIER_0"]
    assert t0["started"] is False
    assert t0["status_label"] == "Not started"
    assert t0["deployed_display"] == "\u2014"
    assert t0["eligible_header"] == "1 Eligible Actors"


def test_build_rollout_summary_initialized_rollout_is_not_started() -> None:
    """A rollout row that exists but is `initialized` reads Not started (not In
    progress) — the ⚪ status prevents an unstarted tier from looking live."""
    summary = helpers_module.build_rollout_summary(
        [
            {
                "tier": "TIER_2",
                "rollout_id": "r-t2",
                "state": "in_progress",
                "current_target_rollout_pct": "50",
            },
            {
                "tier": "TIER_1",
                "rollout_id": "r-t1",
                "state": "initialized",
                "current_target_rollout_pct": "0",
            },
        ],
    )
    t1 = {c["tier_value"]: c for c in summary["tier_cards"]}["TIER_1"]
    assert t1["started"] is False
    assert t1["status_label"] == "Not started"


def test_build_rollout_summary_started_zero_eligible_reads_full_coverage() -> None:
    """A *started* tier with a 0-of-0 eligible audience reads `100%` coverage (all
    that will pin are pinned), while the failure ratio stays `0%`."""
    factors = TierPopulationFactors()
    summary = helpers_module.build_rollout_summary(
        [
            {
                "tier": "TIER_2",
                "rollout_id": "r-t2",
                "state": "in_progress",
                "current_target_rollout_pct": "100",
            }
        ],
        factors_by_tier={"TIER_2": factors},
    )
    t2 = {c["tier_value"]: c for c in summary["tier_cards"]}["TIER_2"]
    assert t2["pinned_summary"] == "0 of 0 eligible (100%)"
    assert t2["failed_summary"] == "0 of 0 pinned (0%)"


# Demo org IDs wired into the mock org-pin universe (mock_adapter._MOCK_ORG_PINS)
# and the org-lookup search mock (shared_components/org_search.py).
_ORG_ACME = "00000000-0000-0000-0000-000000000001"
_ORG_MOTHERDUCK = "00000000-0000-0000-0000-000000000002"
_ORG_AIRBYTE = "00000000-0000-0000-0000-000000000003"
_ORG_DATAFLOW = "00000000-0000-0000-0000-000000000004"


def test_org_pin_version_rows_maps_display_keys(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`org_pin_version_rows` adds the table's `_display` keys per version."""
    monkeypatch.setattr(
        helpers_module, "get_adapter", lambda *_args: MockPinningAdapter()
    )

    rows = helpers_module.org_pin_version_rows(_ORG_ACME)

    assert rows
    for row in rows:
        assert row["connector_id"] == row["connector_definition_id"]
        assert row["connector_name"]
        assert row["has_active_rollout_display"] in ("Yes", "")
        assert row["custom_pin_count_display"] == (
            row["actor_pins_display"]
            + row["workspace_pins_display"]
            + row["org_pins_display"]
        )


def test_org_pin_version_rows_are_org_specific(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Different orgs return different versions; unknown orgs return nothing."""
    monkeypatch.setattr(
        helpers_module, "get_adapter", lambda *_args: MockPinningAdapter()
    )

    acme = helpers_module.org_pin_version_rows(_ORG_ACME)
    motherduck = helpers_module.org_pin_version_rows(_ORG_MOTHERDUCK)

    acme_versions = {row["version_id"] for row in acme}
    motherduck_versions = {row["version_id"] for row in motherduck}
    assert acme_versions
    assert motherduck_versions
    assert acme_versions != motherduck_versions

    # Dataflow Labs has no pins -> empty result (exercises the empty state).
    assert helpers_module.org_pin_version_rows(_ORG_DATAFLOW) == []


def test_org_pin_version_rows_flags_active_rollout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """MotherDuck's rollout-backed version reports an active rollout; Acme's don't."""
    monkeypatch.setattr(
        helpers_module, "get_adapter", lambda *_args: MockPinningAdapter()
    )

    motherduck = helpers_module.org_pin_version_rows(_ORG_MOTHERDUCK)
    assert any(row["has_active_rollout_display"] == "Yes" for row in motherduck)

    acme = helpers_module.org_pin_version_rows(_ORG_ACME)
    assert all(row["has_active_rollout_display"] == "" for row in acme)


def test_org_pin_version_rows_empty_when_no_org() -> None:
    """No organization selected yields no rows (the tab's first step is empty)."""
    assert helpers_module.org_pin_version_rows("") == []
    assert helpers_module.org_pin_version_rows("   ") == []


def test_org_connector_pin_rows_classifies_pin_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`org_connector_pin_rows` labels each pin as Manual/Rollout/Breaking Change."""
    monkeypatch.setattr(
        helpers_module, "get_adapter", lambda *_args: MockPinningAdapter()
    )

    rows = helpers_module.org_connector_pin_rows(_ORG_ACME)

    assert rows
    for row in rows:
        assert row["scope_display"] == str(row["pin_scope_type"]).title()
        pin_type = row["pin_type_display"]
        assert pin_type == "Manual" or pin_type.startswith(
            ("Rollout", "Breaking Change")
        )
    assert any(row["pin_type_display"] == "Manual" for row in rows)


def test_org_connector_pin_rows_cover_all_pin_categories(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Across demo orgs the mock exercises manual, rollout, and breaking-change."""
    monkeypatch.setattr(
        helpers_module, "get_adapter", lambda *_args: MockPinningAdapter()
    )

    motherduck = helpers_module.org_connector_pin_rows(_ORG_MOTHERDUCK)
    airbyte = helpers_module.org_connector_pin_rows(_ORG_AIRBYTE)

    assert any(str(row["pin_type_display"]).startswith("Rollout") for row in motherduck)
    assert any(
        str(row["pin_type_display"]).startswith("Breaking Change") for row in airbyte
    )
    # An org-scoped pin is present for Airbyte (org/workspace/actor coverage).
    assert any(row["pin_scope_type"] == "organization" for row in airbyte)


def test_org_connector_pin_rows_version_filter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`pinned_version_id` narrows the detail rows to a single version."""
    monkeypatch.setattr(
        helpers_module, "get_adapter", lambda *_args: MockPinningAdapter()
    )

    all_rows = helpers_module.org_connector_pin_rows(_ORG_ACME)
    version_id = str(all_rows[0]["pinned_version_id"])
    filtered = helpers_module.org_connector_pin_rows(_ORG_ACME, version_id)

    assert filtered
    assert {row["pinned_version_id"] for row in filtered} == {version_id}
    assert len(filtered) < len(all_rows)


def test_org_connector_pin_rows_empty_when_no_org() -> None:
    assert helpers_module.org_connector_pin_rows("") == []
