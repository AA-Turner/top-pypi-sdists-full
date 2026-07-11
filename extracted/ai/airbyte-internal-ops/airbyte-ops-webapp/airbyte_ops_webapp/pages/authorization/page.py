"""Airbyte Ops authorization page with dual auth status cards."""

# ruff: noqa: SIM117

from fastmcp import FastMCP, FastMCPApp
from prefab_ui.actions.custom import CallHandler
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    H2,
    Badge,
    Button,
    CardContent,
    CardHeader,
    Column,
    Div,
    Icon,
    Link,
    Row,
    Small,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.auth.google_oauth import (
    GOOGLE_OAUTH_JS_ACTIONS,
    google_oauth_config,
    hydrate_google_oauth_action,
    logout_google_oauth_action,
    mock_login_google_oauth_action,
    mock_logout_google_oauth_action,
)
from airbyte_ops_webapp.auth.oauth import (
    OAUTH_JS_ACTIONS,
    hydrate_oauth_action,
    logout_oauth_action,
    mock_login_oauth_action,
    mock_logout_oauth_action,
    oauth_config,
)
from airbyte_ops_webapp.pages.authorization.defaults import (
    OPS_AUTHORIZATION_TOOL_NAME,
)
from airbyte_ops_webapp.pages.shared_components.layout import (
    OPS_HOME_PATH,
    render_breadcrumb_nav,
    render_environment_banners,
    render_page_hero,
    render_version_footer,
)
from airbyte_ops_webapp.state import (
    deploy_sha,
    deploy_sha_url,
    mock_only_enabled,
    ops_package_version,
    preview_deploy_enabled,
    preview_pr_number,
    preview_pr_url,
)
from airbyte_ops_webapp.theme import (
    BUTTON_INFO_CLASS,
    BUTTON_OUTLINE_CLASS,
    PAGE_CLASS,
    PANEL_CARD_CLASS,
    SUCCESS_CARD_CLASS,
    _airbyte_theme,
    _app_root_class,
    _card_style,
    _page_style,
    _primary_link_style,
)

authorization_app = FastMCPApp("Airbyte Ops Authorization")


def _auth_card_style() -> dict[str, str]:
    style = _card_style()
    style.update({"maxWidth": "36rem", "width": "100%"})
    return style


def _cards_container_style() -> dict[str, str]:
    return {
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "gap": "1.5rem",
        "width": "100%",
    }


def _render_airbyte_auth_card() -> None:
    """Render the Airbyte (Okta/Keycloak) auth status card."""
    with If(STATE.oauth_authenticated):
        with Div(
            css_class=f"{PANEL_CARD_CLASS} {SUCCESS_CARD_CLASS}",
            style=_auth_card_style(),
        ):
            with CardHeader(), Row(align="center", gap=2):
                Icon("check-circle", size="default")
                H2("Airbyte")
            with CardContent(), Column(gap=2):
                with Row(align="center", gap=2):
                    Badge("Connected", css_class="bg-green-600 text-white")
                    Text(
                        STATE.oauth_user_email,
                        style={"fontSize": "0.875rem", "opacity": "0.85"},
                    )
                Button(
                    "Log out of Airbyte",
                    variant="outline",
                    size="sm",
                    css_class=BUTTON_OUTLINE_CLASS,
                    onClick=mock_logout_oauth_action()
                    if mock_only_enabled()
                    else logout_oauth_action(),
                )

    with If(~STATE.oauth_authenticated):
        with Div(css_class=PANEL_CARD_CLASS, style=_auth_card_style()):
            with CardHeader(), Row(align="center", gap=2):
                Icon("lock", size="default")
                H2("Airbyte")
            with CardContent(), Column(gap=3):
                Text(
                    "Sign in with your Airbyte identity to access internal operations tools."
                )
                Small(
                    "Uses Keycloak → Okta. Required for Config API access.",
                    style={"opacity": "0.7"},
                )
                Button(
                    "Log in with Airbyte",
                    variant="info",
                    css_class=BUTTON_INFO_CLASS,
                    onClick=mock_login_oauth_action()
                    if mock_only_enabled()
                    else CallHandler("startOAuth"),
                )


def _render_google_auth_card() -> None:
    """Render the Google OAuth status card for BigQuery access."""
    with If(STATE.google_authenticated):
        with Div(
            css_class=f"{PANEL_CARD_CLASS} {SUCCESS_CARD_CLASS}",
            style=_auth_card_style(),
        ):
            with CardHeader(), Row(align="center", gap=2):
                Icon("check-circle", size="default")
                H2("Google")
            with CardContent(), Column(gap=2):
                with Row(align="center", gap=2):
                    Badge("Connected", css_class="bg-green-600 text-white")
                    Text(
                        STATE.google_user_email,
                        style={"fontSize": "0.875rem", "opacity": "0.85"},
                    )
                Button(
                    "Log out of Google",
                    variant="outline",
                    size="sm",
                    css_class=BUTTON_OUTLINE_CLASS,
                    on_click=mock_logout_google_oauth_action()
                    if mock_only_enabled()
                    else logout_google_oauth_action(),
                )

    with If(~STATE.google_authenticated):
        with Div(css_class=PANEL_CARD_CLASS, style=_auth_card_style()):
            with CardHeader(), Row(align="center", gap=2):
                Icon("lock", size="default")
                H2("Google")
            with CardContent(), Column(gap=3):
                Text("Sign in with your Google account for BigQuery access.")
                Small(
                    "Grants read-only BigQuery access using your @airbyte.io identity.",
                    style={"opacity": "0.7"},
                )
                Button(
                    "Log in with Google",
                    variant="info",
                    css_class=BUTTON_INFO_CLASS,
                    onClick=mock_login_google_oauth_action()
                    if mock_only_enabled()
                    else CallHandler("startGoogleOAuth"),
                )


@authorization_app.ui(
    name=OPS_AUTHORIZATION_TOOL_NAME, title="Airbyte Ops Authorization"
)
def open_ops_authorization() -> PrefabApp:
    """Open the Airbyte Ops authorization page."""
    current_oauth_config = oauth_config()
    current_google_config = google_oauth_config()
    state = {
        "auth_bearer_token": "",
        "admin_user_email": "",
        "is_mock_only": mock_only_enabled(),
        "is_preview_deploy": preview_deploy_enabled(),
        "preview_pr_number": preview_pr_number(),
        "preview_pr_url": preview_pr_url(),
        "deploy_sha": deploy_sha(),
        "deploy_sha_url": deploy_sha_url(),
        "ops_package_version": ops_package_version(),
        "oauth_config": current_oauth_config,
        "oauth_enabled": current_oauth_config["enabled"],
        "oauth_authenticated": False,
        "oauth_status": "",
        "oauth_user_email": "",
        "google_oauth_config": current_google_config,
        "google_authenticated": False,
        "google_user_email": "",
        "google_access_token": "",
        "google_status": "",
    }

    all_js_actions = {**OAUTH_JS_ACTIONS, **GOOGLE_OAUTH_JS_ACTIONS}

    with (
        PrefabApp(
            title="Airbyte Ops Authorization",
            css_class=_app_root_class(),
            state=state,
            theme=_airbyte_theme(),
            connect_domains=[
                str(current_oauth_config["issuer"]),
                "accounts.google.com",
            ],
            js_actions=all_js_actions,
            on_mount=hydrate_oauth_action(),
        ) as app,
        Div(
            style=_page_style(),
            onMount=hydrate_google_oauth_action(),
        ),
        Column(gap=5, css_class=PAGE_CLASS),
    ):
        render_environment_banners()
        render_breadcrumb_nav(current_page="Authorization")
        render_page_hero(
            title="Authorization",
            description="Manage your authentication for Airbyte internal tools.",
            show_auth_controls=True,
        )
        with Div(style=_cards_container_style()):
            _render_airbyte_auth_card()
            _render_google_auth_card()
        with If(STATE.oauth_authenticated & STATE.google_authenticated):
            with Row(justify="center"):
                Link(
                    "⚙️ Go Home",
                    href=OPS_HOME_PATH,
                    target="_top",
                    style=_primary_link_style(),
                )
        render_version_footer()
    return app


def register_authorization_app(mcp: FastMCP) -> None:
    """Register the Airbyte Ops authorization app with the MCP server."""
    mcp.add_provider(authorization_app)
