"""Airbyte Ops login page."""

from fastmcp import FastMCP, FastMCPApp
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Div, Link, Row
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.app_shell import build_ops_app
from airbyte_ops_webapp.auth.oauth import hydrate_oauth_action, oauth_config
from airbyte_ops_webapp.pages.shared_components.auth import render_login_card
from airbyte_ops_webapp.pages.shared_components.layout import (
    OPS_HOME_PATH,
    render_breadcrumb_nav,
    render_environment_banners,
    render_page_hero,
)
from airbyte_ops_webapp.state import (
    mock_only_enabled,
    preview_deploy_enabled,
    preview_pr_number,
    preview_pr_url,
)
from airbyte_ops_webapp.theme import PAGE_CLASS, _page_style, _primary_link_style

OPS_LOGIN_PATH = "/login"
OPS_LOGIN_TOOL_NAME = "ops_login"

login_app = FastMCPApp("Airbyte Ops Login")


def _login_card_container_style() -> dict[str, str]:
    return {
        "display": "flex",
        "justifyContent": "center",
        "width": "100%",
    }


@login_app.ui(name=OPS_LOGIN_TOOL_NAME, title="Airbyte Ops Login")
def open_ops_login() -> PrefabApp:
    """Open the Airbyte Ops login page."""
    current_oauth_config = oauth_config()
    state = {
        "auth_bearer_token": "",
        "admin_user_email": "",
        "is_mock_only": mock_only_enabled(),
        "is_preview_deploy": preview_deploy_enabled(),
        "preview_pr_number": preview_pr_number(),
        "preview_pr_url": preview_pr_url(),
        "oauth_config": current_oauth_config,
        "oauth_enabled": current_oauth_config["enabled"],
        "oauth_authenticated": False,
        "oauth_status": "",
        "oauth_user_email": "",
    }

    with (
        build_ops_app(
            title="Airbyte Ops Login",
            state=state,
            oauth_issuer=str(current_oauth_config["issuer"]),
        ) as app,
        Div(style=_page_style(), onMount=hydrate_oauth_action()),
        Column(gap=5, css_class=PAGE_CLASS),
    ):
        render_environment_banners()
        render_breadcrumb_nav(current_page="Login")
        render_page_hero(
            title="Airbyte Ops",
            description="Sign in once to use internal operations tools.",
            show_auth_controls=True,
        )
        with Div(style=_login_card_container_style()):
            render_login_card()
        with If(STATE.oauth_authenticated), Row(justify="center"):
            Link(
                "⚙️ Go Home",
                href=OPS_HOME_PATH,
                target="_top",
                style=_primary_link_style(),
            )
    return app


def register_login_app(mcp: FastMCP) -> None:
    """Register the Airbyte Ops login app with the MCP server."""
    mcp.add_provider(login_app)
