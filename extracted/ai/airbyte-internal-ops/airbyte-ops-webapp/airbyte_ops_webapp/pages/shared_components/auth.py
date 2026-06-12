"""Shared authentication UI components."""

from prefab_ui.actions.custom import CallHandler
from prefab_ui.components import (
    H2,
    Badge,
    Button,
    CardContent,
    CardHeader,
    Column,
    Div,
    Input,
    Row,
    Small,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.auth.oauth import logout_oauth_action
from airbyte_ops_webapp.theme import PANEL_CARD_CLASS, _card_style


def render_auth_card() -> None:
    with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
        with CardHeader():
            H2("Auth")
        with CardContent(), Column(gap=2):
            with If(STATE.oauth_enabled):
                Text(
                    "Sign in with Keycloak to obtain a short-lived user bearer token. "
                    "The browser stores it in session storage and sends it to this "
                    "backend for Config API calls."
                )
                with Row(gap=2):
                    Button(
                        "Sign in with Airbyte",
                        variant="info",
                        onClick=CallHandler("startOAuth"),
                    )
                    Button(
                        "Sign out",
                        variant="outline",
                        onClick=logout_oauth_action(),
                    )
                with If(STATE.oauth_authenticated):
                    Badge("Authenticated", variant="success")
                    Text("Signed in as")
                    Text(content=STATE.oauth_user_email, bold=True)
                with If(STATE.oauth_status):
                    Text(STATE.oauth_status)
                Small(STATE.oauth_config.issuer)
                Small(STATE.oauth_config.redirect_uri)
            Input(
                name="auth_bearer_token",
                value=STATE.auth_bearer_token,
                placeholder="OAuth token is filled after sign-in; paste a bearer token only for local fallback",
                inputType="password",
            )


def render_compact_auth_controls() -> None:
    with Column(align="end", gap=2):
        with If(STATE.oauth_authenticated):
            Badge("Authenticated", variant="success")
            Text(content=STATE.oauth_user_email)
        with Row(gap=2):
            Button(
                "Sign in",
                variant="info",
                size="sm",
                onClick=CallHandler("startOAuth"),
            )
            Button(
                "Sign out",
                variant="outline",
                size="sm",
                onClick=logout_oauth_action(),
            )
