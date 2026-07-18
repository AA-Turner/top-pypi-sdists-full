"""Airbyte Ops login page."""

from fastmcp import FastMCP, FastMCPApp
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Div, Row
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
    render_version_footer,
)
from airbyte_ops_webapp.state import OpsPageState
from airbyte_ops_webapp.theme import PAGE_CLASS, AbPage, AbPrimaryLink

OPS_LOGIN_PATH = "/login"
OPS_LOGIN_TOOL_NAME = "ops_login"

login_app = FastMCPApp("Airbyte Ops Login")


@login_app.ui(name=OPS_LOGIN_TOOL_NAME, title="Airbyte Ops Login")
def open_ops_login() -> PrefabApp:
    """Open the Airbyte Ops login page."""
    current_oauth_config = oauth_config()
    state = OpsPageState.from_env(oauth_config=current_oauth_config).to_prefab_state()

    with (
        build_ops_app(
            title="Airbyte Ops Login",
            state=state,
            oauth_issuer=current_oauth_config.issuer,
        ) as app,
        AbPage(onMount=hydrate_oauth_action()),
        Column(gap=5, css_class=PAGE_CLASS),
    ):
        render_environment_banners()
        render_breadcrumb_nav(current_page="Login")
        render_page_hero(
            title="Airbyte Ops",
            description="Sign in once to use internal operations tools.",
            show_auth_controls=True,
        )
        with Div(css_class="flex justify-center w-full"):
            render_login_card()
        with If(STATE.oauth_authenticated), Row(justify="center"):
            AbPrimaryLink(
                "⚙️ Go Home",
                href=OPS_HOME_PATH,
                target="_top",
            )
        render_version_footer()
    return app


def register_login_app(mcp: FastMCP) -> None:
    """Register the Airbyte Ops login app with the MCP server."""
    mcp.add_provider(login_app)
