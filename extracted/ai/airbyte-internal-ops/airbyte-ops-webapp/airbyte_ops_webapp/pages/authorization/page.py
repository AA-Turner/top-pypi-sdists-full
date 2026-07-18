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
from airbyte_ops_webapp.state import OpsPageState, mock_only_enabled
from airbyte_ops_webapp.theme import (
    BUTTON_INFO_CLASS,
    BUTTON_OUTLINE_CLASS,
    PAGE_CLASS,
    AbCard,
    AbPage,
    AbPrimaryLink,
    AbSuccessCard,
    _airbyte_theme,
    _app_root_class,
)

authorization_app = FastMCPApp("Airbyte Ops Authorization")

_AUTH_CARD_CLASS = "max-w-[36rem] w-full"


def _render_airbyte_auth_card() -> None:
    """Render the Airbyte (Okta/Keycloak) auth status card."""
    with If(STATE.oauth_authenticated):
        with AbSuccessCard(css_class=_AUTH_CARD_CLASS):
            with CardHeader(), Row(align="center", gap=2):
                Icon("check-circle", size="default")
                H2("Airbyte")
            with CardContent(), Column(gap=2):
                with Row(align="center", gap=2):
                    Badge("Connected", css_class="bg-green-600 text-white")
                    Text(
                        STATE.oauth_user_email,
                        css_class="text-sm opacity-[0.85]",
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
        with AbCard(css_class=_AUTH_CARD_CLASS):
            with CardHeader(), Row(align="center", gap=2):
                Icon("lock", size="default")
                H2("Airbyte")
            with CardContent(), Column(gap=3):
                Text(
                    "Sign in with your Airbyte identity to access internal operations tools."
                )
                Small(
                    "Uses Keycloak → Okta. Required for Config API access.",
                    css_class="opacity-70",
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
        with AbSuccessCard(css_class=_AUTH_CARD_CLASS):
            with CardHeader(), Row(align="center", gap=2):
                Icon("check-circle", size="default")
                H2("Google")
            with CardContent(), Column(gap=2):
                with Row(align="center", gap=2):
                    Badge("Connected", css_class="bg-green-600 text-white")
                    Text(
                        STATE.google_user_email,
                        css_class="text-sm opacity-[0.85]",
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
        with AbCard(css_class=_AUTH_CARD_CLASS):
            with CardHeader(), Row(align="center", gap=2):
                Icon("lock", size="default")
                H2("Google")
            with CardContent(), Column(gap=3):
                Text("Sign in with your Google account for BigQuery access.")
                Small(
                    "Grants read-only BigQuery access using your @airbyte.io identity.",
                    css_class="opacity-70",
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
        **OpsPageState.from_env(oauth_config=current_oauth_config).to_prefab_state(),
        "google_oauth_config": current_google_config,
    }

    all_js_actions = {**OAUTH_JS_ACTIONS, **GOOGLE_OAUTH_JS_ACTIONS}

    with (
        PrefabApp(
            title="Airbyte Ops Authorization",
            css_class=_app_root_class(),
            state=state,
            theme=_airbyte_theme(),
            connect_domains=[
                current_oauth_config.issuer,
                "accounts.google.com",
            ],
            js_actions=all_js_actions,
            on_mount=hydrate_oauth_action(),
        ) as app,
        AbPage(
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
        with Div(css_class="flex flex-col items-center gap-6 w-full"):
            _render_airbyte_auth_card()
            _render_google_auth_card()
        with If(STATE.oauth_authenticated & STATE.google_authenticated):
            with Row(justify="center"):
                AbPrimaryLink(
                    "⚙️ Go Home",
                    href=OPS_HOME_PATH,
                    target="_top",
                )
        render_version_footer()
    return app


def register_authorization_app(mcp: FastMCP) -> None:
    """Register the Airbyte Ops authorization app with the MCP server."""
    mcp.add_provider(authorization_app)
