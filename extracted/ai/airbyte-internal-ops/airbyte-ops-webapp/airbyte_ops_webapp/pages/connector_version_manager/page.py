"""Connector Version Manager page."""

# ruff: noqa: SIM117

from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Any

from fastmcp import FastMCP, FastMCPApp
from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    H2,
    Button,
    CardContent,
    CardHeader,
    Column,
    DataTable,
    DataTableColumn,
    Div,
    Grid,
    Input,
    Markdown,
    Select,
    SelectOption,
    Switch,
    Text,
    Textarea,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import EVENT, RESULT, STATE

from airbyte_ops_webapp.app_shell import build_ops_app
from airbyte_ops_webapp.auth.oauth import hydrate_oauth_action, oauth_config
from airbyte_ops_webapp.models import OverridePlan, ScopeType
from airbyte_ops_webapp.pages.connector_version_manager.components import (
    render_recent_releases_and_rollout_context,
    render_status_cards,
)
from airbyte_ops_webapp.pages.connector_version_manager.defaults import (
    CONNECTOR_VERSION_MANAGER_TOOL_NAME,
    default_connector_query,
)
from airbyte_ops_webapp.pages.shared_components.layout import (
    render_mock_mode_banner,
    render_page_hero,
)
from airbyte_ops_webapp.services.connector_version_manager.adapter import (
    OpsMcpAdapter,
    operation_result_to_json,
    preview_to_json,
)
from airbyte_ops_webapp.services.connector_version_manager.demo_mode import (
    MockPinningAdapter,
)
from airbyte_ops_webapp.state import (
    AIRBYTE_BEARER_TOKEN_ENV_VAR,
    AIRBYTE_CLIENT_ID_ENV_VAR,
    AIRBYTE_CLIENT_SECRET_ENV_VAR,
    AIRBYTE_CONFIG_API_ROOT_ENV_VAR,
    mock_only_enabled,
)
from airbyte_ops_webapp.theme import (
    AIRBYTE_PRIMARY,
    AIRBYTE_SECONDARY,
    CODE_BLOCK_CLASS,
    PAGE_CLASS,
    PANEL_CARD_CLASS,
    PREVIEW_CARD_CLASS,
    SUCCESS_CARD_CLASS,
    _card_style,
    _code_surface_style,
    _page_style,
)

DEFAULT_ADMIN_USER_EMAIL = "devin-local@example.com"
DEFAULT_ADMIN_USER_ID = "00000000-0000-0000-0000-000000000000"

connector_version_manager_app = FastMCPApp("Connector Version Manager")


def _auth_available(bearer_token_override: str | None = None) -> bool:
    if mock_only_enabled():
        return True
    if bearer_token_override or os.getenv(AIRBYTE_BEARER_TOKEN_ENV_VAR):
        return True
    return bool(
        os.getenv(AIRBYTE_CLIENT_ID_ENV_VAR)
        and os.getenv(AIRBYTE_CLIENT_SECRET_ENV_VAR)
    )


def _adapter(bearer_token_override: str | None = None) -> OpsMcpAdapter:
    if mock_only_enabled():
        return MockPinningAdapter()
    return OpsMcpAdapter(
        bearer_token=bearer_token_override or os.getenv(AIRBYTE_BEARER_TOKEN_ENV_VAR),
        client_id=os.getenv(AIRBYTE_CLIENT_ID_ENV_VAR),
        client_secret=os.getenv(AIRBYTE_CLIENT_SECRET_ENV_VAR),
        config_api_root=os.getenv(AIRBYTE_CONFIG_API_ROOT_ENV_VAR)
        or "https://cloud.airbyte.com/api/v1",
    )


def _connector_rows(query: str) -> list[dict[str, str]]:
    return [asdict(connector) for connector in _adapter().search_connectors(query)]


def _connector_options(query: str) -> list[dict[str, str]]:
    return [
        {
            "label": f"{connector['name']} ({connector['latest_version']})",
            "value": connector["id"],
        }
        for connector in _connector_rows(query)
    ]


def _select_options(options: list[dict[str, str]]) -> None:
    for option in options:
        SelectOption(label=option["label"], value=option["value"])


def _admin_user_options() -> list[dict[str, str]]:
    if mock_only_enabled():
        return [{"label": DEFAULT_ADMIN_USER_EMAIL, "value": DEFAULT_ADMIN_USER_EMAIL}]
    try:
        admin_users = list(_adapter().list_instance_admin_users())
    except Exception:
        admin_users = []
    if not admin_users:
        admin_users = [
            {
                "email": DEFAULT_ADMIN_USER_EMAIL,
                "userId": DEFAULT_ADMIN_USER_ID,
            }
        ]
    return [
        {
            "label": f"{admin_user['email']} ({admin_user['userId']})",
            "value": admin_user["email"],
        }
        for admin_user in admin_users
    ]


def _first_admin_user_email() -> str:
    options = _admin_user_options()
    return options[0]["value"] if options else DEFAULT_ADMIN_USER_EMAIL


def _rows_from_dataclasses(rows: Any) -> list[dict[str, Any]]:
    return [asdict(row) for row in rows]


def _json_text(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True)


def _empty_connector() -> dict[str, str]:
    return {
        "id": "",
        "name": "",
        "connector_type": "source",
        "latest_version": "",
        "docker_repository": "",
    }


def _connector_context_placeholder(message: str) -> dict[str, Any]:
    current_state = {"message": message}
    return {
        "connector": _empty_connector(),
        "versions": [],
        "current_state": current_state,
        "current_state_markdown": _json_text(current_state),
        "ancestor_configs": [],
        "descendant_configs": [],
    }


def _target_ids(
    *,
    adapter: OpsMcpAdapter,
    scope_type: ScopeType,
    scope_id: str,
    actor_workspace_id: str,
) -> tuple[str, str | None, str | None]:
    if scope_type == "organization":
        return scope_id, None, None
    if scope_type == "actor":
        organization_id = (
            adapter.resolve_organization_id("workspace", actor_workspace_id)
            if actor_workspace_id
            else ""
        )
        return organization_id, actor_workspace_id or None, scope_id
    return adapter.resolve_organization_id("workspace", scope_id), scope_id, None


@connector_version_manager_app.tool()
def search_connectors(query: str = "") -> dict[str, Any]:
    """Search connector definitions by name, definition ID, or Docker repository."""
    connectors = _connector_rows(query)
    return {
        "connectors": connectors,
        "connector_options": _connector_options(query),
        "selected_connector_id": connectors[0]["id"] if connectors else "",
    }


@connector_version_manager_app.tool()
def load_connector_context(
    connector_id: str,
    scope_type: ScopeType = "workspace",
    scope_id: str = "",
    actor_workspace_id: str = "",
    auth_bearer_token: str = "",
) -> dict[str, Any]:
    """Load connector versions and scoped pin context."""
    if not connector_id:
        return _connector_context_placeholder(
            "Search for and select a connector before loading scope context."
        )
    adapter = _adapter(auth_bearer_token or None)
    try:
        connector = adapter.get_connector(connector_id)
    except ValueError:
        return _connector_context_placeholder(f"Unknown connector ID: {connector_id}")
    if not _auth_available(auth_bearer_token or None):
        current_state = {
            "message": "Enter a bearer token or set Airbyte Cloud client credentials to load scope context.",
        }
        return {
            "connector": asdict(connector),
            "versions": [],
            "current_state": current_state,
            "current_state_markdown": _json_text(current_state),
            "ancestor_configs": [],
            "descendant_configs": [],
        }
    workspace_id = scope_id if scope_type == "workspace" else actor_workspace_id
    if isinstance(adapter, MockPinningAdapter):
        current_state = adapter.get_current_context(
            connector_id=connector.id,
            scope_type=scope_type,
            scope_id=scope_id,
        )
    else:
        current_state = adapter.get_current_context(
            connector_id=connector.id,
            scope_type=scope_type,
            scope_id=scope_id,
            workspace_id=workspace_id,
        )
    return {
        "connector": asdict(connector),
        "versions": _rows_from_dataclasses(adapter.list_versions(connector.id)),
        "current_state": asdict(current_state),
        "current_state_markdown": _json_text(asdict(current_state)),
        "ancestor_configs": _rows_from_dataclasses(
            current_state.ancestor_configurations
        ),
        "descendant_configs": _rows_from_dataclasses(
            current_state.descendant_configurations
        ),
    }


def _override_plan(
    *,
    adapter: OpsMcpAdapter,
    connector_id: str,
    connector_name: str,
    connector_type: str,
    scope_type: ScopeType,
    scope_id: str,
    actor_workspace_id: str,
    action: str,
    version: str,
    override_reason: str,
    reference_url: str,
    approval_comment_url: str,
    user_email: str | None,
    customer_tier_filter: str,
    force: bool,
) -> OverridePlan:
    organization_id, workspace_id, actor_id = _target_ids(
        adapter=adapter,
        scope_type=scope_type,
        scope_id=scope_id,
        actor_workspace_id=actor_workspace_id,
    )
    return OverridePlan(
        action=action,
        connector_id=connector_id,
        connector_name=connector_name,
        connector_type=connector_type,
        scope_type=scope_type,
        organization_id=organization_id,
        workspace_id=workspace_id or None,
        actor_id=actor_id or None,
        scope_id=scope_id,
        version=None if action == "unset" else version,
        override_reason=override_reason,
        override_reason_reference_url=reference_url,
        approval_comment_url=approval_comment_url,
        user_email=user_email,
        customer_tier_filter=customer_tier_filter,
        force=force,
    )


@connector_version_manager_app.tool()
def stage_override(
    connector_id: str,
    connector_name: str,
    connector_type: str,
    scope_type: ScopeType,
    scope_id: str,
    action: str,
    version: str,
    override_reason: str,
    reference_url: str,
    approval_comment_url: str,
    user_email: str | None,
    auth_bearer_token: str = "",
    actor_workspace_id: str = "",
    customer_tier_filter: str = "TIER_2",
    force: bool = False,
) -> dict[str, Any]:
    """Stage a safe preview for a connector version override."""
    adapter = _adapter(auth_bearer_token or None)
    preview = adapter.stage_override(
        _override_plan(
            adapter=adapter,
            connector_id=connector_id,
            connector_name=connector_name,
            connector_type=connector_type,
            scope_type=scope_type,
            scope_id=scope_id,
            actor_workspace_id=actor_workspace_id,
            action=action,
            version=version,
            override_reason=override_reason,
            reference_url=reference_url,
            approval_comment_url=approval_comment_url,
            user_email=user_email,
            customer_tier_filter=customer_tier_filter,
            force=force,
        )
    )
    return {
        "preview_json": preview_to_json(preview),
        "warnings": list(preview.warnings),
    }


@connector_version_manager_app.tool()
def apply_override(
    connector_id: str,
    connector_name: str,
    connector_type: str,
    scope_type: ScopeType,
    scope_id: str,
    action: str,
    version: str,
    override_reason: str,
    reference_url: str,
    approval_comment_url: str,
    user_email: str | None,
    auth_bearer_token: str = "",
    actor_workspace_id: str = "",
    customer_tier_filter: str = "TIER_2",
    force: bool = False,
) -> dict[str, Any]:
    """Apply a connector version override after user confirmation."""
    adapter = _adapter(auth_bearer_token or None)
    result = adapter.apply_override(
        _override_plan(
            adapter=adapter,
            connector_id=connector_id,
            connector_name=connector_name,
            connector_type=connector_type,
            scope_type=scope_type,
            scope_id=scope_id,
            actor_workspace_id=actor_workspace_id,
            action=action,
            version=version,
            override_reason=override_reason,
            reference_url=reference_url,
            approval_comment_url=approval_comment_url,
            user_email=user_email,
            customer_tier_filter=customer_tier_filter,
            force=force,
        )
    )
    return {
        "apply_result_json": operation_result_to_json(result),
        "apply_message": result.message,
        "apply_success": result.success,
    }


@connector_version_manager_app.ui(
    name=CONNECTOR_VERSION_MANAGER_TOOL_NAME,
    title="Connector Version Manager",
    description="Open the Airbyte Connector Version Manager app.",
)
def connector_version_manager(
    query: str = "",
    connector_name: str = "",
    connector: str = "",
    connector_id: str | None = None,
    scope_type: ScopeType = "workspace",
    scope_id: str = "workspace_example",
    actor_workspace_id: str = "",
) -> PrefabApp:
    """Open the connector version manager."""
    adapter = _adapter()
    current_oauth_config = oauth_config()
    connector_query = default_connector_query(
        query=query,
        connector_name=connector_name,
        connector=connector,
    )
    connectors = _connector_rows(connector_query)
    selected_connector_id = connector_id or (connectors[0]["id"] if connectors else "")
    selected_connector = _empty_connector()
    if selected_connector_id:
        try:
            selected_connector = asdict(adapter.get_connector(selected_connector_id))
        except ValueError:
            selected_connector = _empty_connector()
    context = load_connector_context(
        selected_connector["id"],
        scope_type,
        scope_id,
        actor_workspace_id,
    )
    state = {
        "accepts_default_connector": True,
        "default_connector_from_args": bool(
            query.strip()
            or connector_name.strip()
            or connector.strip()
            or (connector_id or "").strip()
        ),
        "query": connector_query,
        "connectors": connectors,
        "connector_options": _connector_options(connector_query),
        "selected_connector_id": selected_connector["id"],
        "selected_connector": selected_connector,
        "scope_type": scope_type,
        "scope_id": scope_id,
        "actor_workspace_id": actor_workspace_id,
        "action": "set",
        "target_version": selected_connector["latest_version"],
        "override_reason": "",
        "reference_url": "",
        "approval_comment_url": "",
        "customer_tier_filter": "TIER_2",
        "force": False,
        "auth_bearer_token": "",
        "admin_user_email": _first_admin_user_email(),
        "admin_user_options": _admin_user_options(),
        "versions": context["versions"],
        "current_state": context["current_state"],
        "current_state_markdown": context["current_state_markdown"],
        "ancestor_configs": context["ancestor_configs"],
        "descendant_configs": context["descendant_configs"],
        "preview_json": "",
        "preview_warnings": [],
        "apply_result_json": "",
        "apply_message": "",
        "apply_success": False,
        "is_mock_only": mock_only_enabled(),
        "oauth_config": current_oauth_config,
        "oauth_enabled": current_oauth_config["enabled"],
        "oauth_authenticated": False,
        "oauth_status": "",
        "oauth_user_email": "",
    }

    with build_ops_app(
        title="Connector Version Manager",
        state=state,
        oauth_issuer=str(current_oauth_config["issuer"]),
    ) as app:
        with Div(style=_page_style(), onMount=hydrate_oauth_action()):
            with Column(gap=5, css_class=PAGE_CLASS):
                render_page_hero(
                    title="Connector Version Manager",
                    description=(
                        "Review connector state, stage scoped overrides, and confirm "
                        "payloads before applying production pin changes."
                    ),
                    show_auth_controls=True,
                )
                render_mock_mode_banner()

                with Grid(columns=[1, 2], gap=4):
                    with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
                        with CardHeader():
                            H2("1. Select connector")
                        with CardContent(), Column(gap=3):
                            Input(
                                name="query",
                                value=STATE.query,
                                placeholder="Search connector name, ID, or Docker repo",
                            )
                            Button(
                                "Search",
                                variant="info",
                                on_click=CallTool(
                                    search_connectors,
                                    arguments={"query": STATE.query},
                                    on_success=[
                                        SetState("connectors", RESULT.connectors),
                                        SetState(
                                            "connector_options",
                                            RESULT.connector_options,
                                        ),
                                        SetState(
                                            "selected_connector_id",
                                            RESULT.selected_connector_id,
                                        ),
                                    ],
                                ),
                            )
                            Select(
                                name="selected_connector_id",
                                value=state["selected_connector_id"],
                                onChange=[
                                    SetState(
                                        "selected_connector_id", EVENT.target.value
                                    ),
                                    CallTool(
                                        load_connector_context,
                                        arguments={
                                            "connector_id": EVENT.target.value,
                                            "scope_type": STATE.scope_type,
                                            "scope_id": STATE.scope_id,
                                            "actor_workspace_id": STATE.actor_workspace_id,
                                            "auth_bearer_token": STATE.auth_bearer_token,
                                        },
                                        on_success=[
                                            SetState(
                                                "selected_connector",
                                                RESULT.connector,
                                            ),
                                            SetState(
                                                "target_version",
                                                RESULT.connector.latest_version,
                                            ),
                                            SetState("versions", RESULT.versions),
                                            SetState(
                                                "current_state",
                                                RESULT.current_state,
                                            ),
                                            SetState(
                                                "current_state_markdown",
                                                RESULT.current_state_markdown,
                                            ),
                                            SetState(
                                                "ancestor_configs",
                                                RESULT.ancestor_configs,
                                            ),
                                            SetState(
                                                "descendant_configs",
                                                RESULT.descendant_configs,
                                            ),
                                        ],
                                    ),
                                ],
                            )
                            _select_options(state["connector_options"])
                            DataTable(
                                columns=[
                                    DataTableColumn(
                                        key="name", header="Connector", sortable=True
                                    ),
                                    DataTableColumn(
                                        key="latest_version", header="Latest"
                                    ),
                                    DataTableColumn(
                                        key="connector_type", header="Type"
                                    ),
                                ],
                                rows=STATE.connectors,
                                search=True,
                                paginated=True,
                                pageSize=8,
                            )
                    with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
                        with CardHeader():
                            H2("2. Target scope")
                        with CardContent(), Column(gap=3):
                            Select(
                                name="scope_type",
                                value=state["scope_type"],
                                onChange=SetState("scope_type", EVENT.target.value),
                            )
                            _select_options(
                                [
                                    {"label": value.title(), "value": value}
                                    for value in [
                                        "actor",
                                        "workspace",
                                        "organization",
                                    ]
                                ]
                            )
                            Input(
                                name="scope_id",
                                value=STATE.scope_id,
                                placeholder="Actor, workspace, or organization ID",
                            )
                            Input(
                                name="actor_workspace_id",
                                value=STATE.actor_workspace_id,
                                placeholder="Workspace ID for actor scope",
                            )
                            Button(
                                "Refresh context",
                                variant="info",
                                on_click=CallTool(
                                    load_connector_context,
                                    arguments={
                                        "connector_id": STATE.selected_connector_id,
                                        "scope_type": STATE.scope_type,
                                        "scope_id": STATE.scope_id,
                                        "actor_workspace_id": STATE.actor_workspace_id,
                                        "auth_bearer_token": STATE.auth_bearer_token,
                                    },
                                    on_success=[
                                        SetState(
                                            "selected_connector", RESULT.connector
                                        ),
                                        SetState("versions", RESULT.versions),
                                        SetState("current_state", RESULT.current_state),
                                        SetState(
                                            "current_state_markdown",
                                            RESULT.current_state_markdown,
                                        ),
                                        SetState(
                                            "ancestor_configs",
                                            RESULT.ancestor_configs,
                                        ),
                                        SetState(
                                            "descendant_configs",
                                            RESULT.descendant_configs,
                                        ),
                                    ],
                                ),
                            )
                            render_status_cards()

                render_recent_releases_and_rollout_context()

                with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
                    with CardHeader():
                        H2("3. Configure version change")
                    with CardContent(), Column(gap=4):
                        with Grid(columns=2, gap=3):
                            Select(
                                name="action",
                                value=state["action"],
                                onChange=SetState("action", EVENT.target.value),
                            )
                            _select_options(
                                [
                                    {"label": value.title(), "value": value}
                                    for value in ["set", "unset"]
                                ]
                            )
                            Input(
                                name="target_version",
                                value=STATE.target_version,
                                placeholder="1.2.3",
                            )
                        Textarea(
                            name="override_reason",
                            value=STATE.override_reason,
                            placeholder="Required justification for set/unset operation",
                            rows=3,
                        )
                        Input(
                            name="reference_url",
                            value=STATE.reference_url,
                            placeholder="GitHub issue URL for audit context",
                        )
                        Input(
                            name="approval_comment_url",
                            value=STATE.approval_comment_url,
                            placeholder="Slack approval record URL for real applies",
                        )
                        with Grid(columns=3, gap=3):
                            Select(
                                name="customer_tier_filter",
                                value=state["customer_tier_filter"],
                                onChange=SetState(
                                    "customer_tier_filter", EVENT.target.value
                                ),
                            )
                            _select_options(
                                [
                                    {"label": value, "value": value}
                                    for value in ["TIER_2", "TIER_1", "TIER_0", "ALL"]
                                ]
                            )
                            Select(
                                name="admin_user_email",
                                value=state["admin_user_email"],
                                onChange=SetState(
                                    "admin_user_email", EVENT.target.value
                                ),
                            )
                            _select_options(state["admin_user_options"])
                            Switch(
                                label="Force existing override replacement",
                                name="force",
                            )
                        Button(
                            "Stage preview",
                            variant="info",
                            on_click=CallTool(
                                stage_override,
                                arguments={
                                    "connector_id": STATE.selected_connector.id,
                                    "connector_name": STATE.selected_connector.name,
                                    "connector_type": STATE.selected_connector.connector_type,
                                    "scope_type": STATE.scope_type,
                                    "scope_id": STATE.scope_id,
                                    "actor_workspace_id": STATE.actor_workspace_id,
                                    "action": STATE.action,
                                    "version": STATE.target_version,
                                    "override_reason": STATE.override_reason,
                                    "reference_url": STATE.reference_url,
                                    "approval_comment_url": STATE.approval_comment_url,
                                    "user_email": STATE.admin_user_email,
                                    "auth_bearer_token": STATE.auth_bearer_token,
                                    "customer_tier_filter": STATE.customer_tier_filter,
                                    "force": STATE.force,
                                },
                                on_success=[
                                    SetState("preview_json", RESULT.preview_json),
                                    SetState("preview_warnings", RESULT.warnings),
                                ],
                            ),
                        )
                        with If(STATE.preview_json):
                            with Div(
                                css_class=PREVIEW_CARD_CLASS,
                                style=_card_style(accent=AIRBYTE_PRIMARY),
                            ):
                                with CardContent(), Column(gap=3):
                                    Markdown("**Preview payload**")
                                    Markdown(STATE.preview_warnings)
                                    with Div(style=_code_surface_style()):
                                        Text(
                                            STATE.preview_json,
                                            css_class=CODE_BLOCK_CLASS,
                                        )
                                    Button(
                                        "Apply change",
                                        variant="destructive",
                                        on_click=CallTool(
                                            apply_override,
                                            arguments={
                                                "connector_id": STATE.selected_connector.id,
                                                "connector_name": STATE.selected_connector.name,
                                                "connector_type": STATE.selected_connector.connector_type,
                                                "scope_type": STATE.scope_type,
                                                "scope_id": STATE.scope_id,
                                                "actor_workspace_id": STATE.actor_workspace_id,
                                                "action": STATE.action,
                                                "version": STATE.target_version,
                                                "override_reason": STATE.override_reason,
                                                "reference_url": STATE.reference_url,
                                                "approval_comment_url": STATE.approval_comment_url,
                                                "user_email": STATE.admin_user_email,
                                                "auth_bearer_token": STATE.auth_bearer_token,
                                                "customer_tier_filter": STATE.customer_tier_filter,
                                                "force": STATE.force,
                                            },
                                            on_success=[
                                                SetState(
                                                    "apply_result_json",
                                                    RESULT.apply_result_json,
                                                ),
                                                SetState(
                                                    "apply_message",
                                                    RESULT.apply_message,
                                                ),
                                                SetState(
                                                    "apply_success",
                                                    RESULT.apply_success,
                                                ),
                                            ],
                                        ),
                                    )
                        with If(STATE.apply_message):
                            with Div(
                                css_class=SUCCESS_CARD_CLASS,
                                style=_card_style(accent=AIRBYTE_SECONDARY),
                            ):
                                with CardContent(), Column(gap=2):
                                    Markdown(STATE.apply_message)
                                    with Div(style=_code_surface_style()):
                                        Text(
                                            STATE.apply_result_json,
                                            css_class=CODE_BLOCK_CLASS,
                                        )

    return app


def register_connector_version_manager_app(mcp: FastMCP) -> None:
    """Register the connector version manager app with the MCP server."""
    mcp.add_provider(connector_version_manager_app)
