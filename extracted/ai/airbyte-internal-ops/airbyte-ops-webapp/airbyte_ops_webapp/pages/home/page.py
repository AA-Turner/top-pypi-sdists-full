"""Ops Webapp home page."""

from fastmcp import FastMCP, FastMCPApp
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    H2,
    CardContent,
    CardHeader,
    Column,
    Div,
    Link,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.app_shell import build_ops_app
from airbyte_ops_webapp.auth.oauth import hydrate_oauth_action, oauth_config
from airbyte_ops_webapp.pages.connector_version_manager.defaults import (
    connector_version_manager_launch_path,
    default_connector_query,
)
from airbyte_ops_webapp.pages.shared_components.auth import render_auth_card
from airbyte_ops_webapp.pages.shared_components.layout import (
    render_mock_mode_banner,
    render_page_hero,
)
from airbyte_ops_webapp.state import mock_only_enabled
from airbyte_ops_webapp.theme import (
    AIRBYTE_PRIMARY,
    PAGE_CLASS,
    PANEL_CARD_CLASS,
    _card_style,
    _page_style,
)

OPS_HOME_TOOL_NAME = "ops_home"

home_app = FastMCPApp("Airbyte Ops Webapp Home")


@home_app.ui(name=OPS_HOME_TOOL_NAME, title="Airbyte Ops Webapp")
def open_ops_home(
    query: str = "",
    connector_name: str = "",
    connector: str = "",
) -> PrefabApp:
    """Open the Airbyte Ops Webapp home page."""
    current_oauth_config = oauth_config()
    explicit_default_connector = bool(
        query.strip() or connector_name.strip() or connector.strip()
    )
    connector_query = (
        default_connector_query(
            query=query,
            connector_name=connector_name,
            connector=connector,
        )
        if explicit_default_connector
        else ""
    )
    state = {
        "auth_bearer_token": "",
        "admin_user_email": "",
        "default_connector_from_args": explicit_default_connector,
        "is_mock_only": mock_only_enabled(),
        "oauth_config": current_oauth_config,
        "oauth_enabled": current_oauth_config["enabled"],
        "oauth_authenticated": False,
        "oauth_status": "",
        "oauth_user_email": "",
    }

    with (
        build_ops_app(
            title="Airbyte Ops Webapp",
            state=state,
            oauth_issuer=str(current_oauth_config["issuer"]),
        ) as app,
        Div(style=_page_style(), onMount=hydrate_oauth_action()),
        Column(gap=5, css_class=PAGE_CLASS),
    ):
        render_page_hero(
            title="Airbyte Ops Webapp",
            description=(
                "Sign in once, verify your authenticated Airbyte session, "
                "then open internal operations tools."
            ),
        )
        render_mock_mode_banner()
        render_auth_card()

        with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
            with CardHeader():
                H2("Connector Version Manager")
            with CardContent(), Column(gap=3):
                Text(
                    "Review connector state, stage scoped overrides, and "
                    "confirm payloads before applying production pin changes."
                )
                with If(~STATE.oauth_authenticated):
                    Text("Sign in above to unlock this tool.")
                with If(STATE.oauth_authenticated):
                    Link(
                        "Open Connector Version Manager",
                        href=connector_version_manager_launch_path(connector_query),
                        target="_self",
                        style={
                            "color": "#FFFFFF",
                            "background": AIRBYTE_PRIMARY,
                            "borderRadius": "0.5rem",
                            "display": "inline-flex",
                            "fontWeight": "600",
                            "padding": "0.625rem 1rem",
                            "textDecoration": "none",
                            "width": "fit-content",
                        },
                    )
    return app


def register_home_app(mcp: FastMCP) -> None:
    """Register the Ops Webapp home app with the MCP server."""
    mcp.add_provider(home_app)
