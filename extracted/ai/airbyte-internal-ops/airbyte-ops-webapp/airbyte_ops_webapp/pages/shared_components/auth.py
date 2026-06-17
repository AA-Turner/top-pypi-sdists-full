"""Shared authentication UI components."""

from prefab_ui.actions import SetState
from prefab_ui.actions.custom import CallHandler
from prefab_ui.components import (
    H2,
    Badge,
    Button,
    CardContent,
    CardHeader,
    Column,
    Div,
    Link,
    Popover,
    Row,
    Small,
    Text,
)
from prefab_ui.components.control_flow import ForEach, If
from prefab_ui.rx import ITEM, STATE

from airbyte_ops_webapp.auth.oauth import logout_oauth_action
from airbyte_ops_webapp.theme import (
    BUTTON_INFO_CLASS,
    BUTTON_OUTLINE_CLASS,
    PANEL_CARD_CLASS,
    _card_style,
    _primary_link_style,
)


def _login_card_style() -> dict[str, str]:
    style = _card_style()
    style.update({"maxWidth": "32rem", "width": "100%"})
    return style


def render_auth_status() -> None:
    with Row(align="center", gap=2):
        _render_notification_bell()
        with If(STATE.oauth_authenticated):
            with Row(align="center", gap=1):
                Link(
                    "🔒",
                    href="/authorization",
                    target="_top",
                    style={"textDecoration": "none", "fontSize": "0.9rem"},
                )
                Text(
                    STATE.oauth_user_email,
                    style={"fontSize": "0.8rem", "opacity": "0.85"},
                )
            Button(
                "Log out",
                variant="outline",
                size="sm",
                css_class=BUTTON_OUTLINE_CLASS,
                onClick=logout_oauth_action(),
            )
        with If(~STATE.oauth_authenticated):
            Link(
                "Log in",
                href="/authorization",
                target="_top",
                style=_primary_link_style(),
            )


def _render_notification_bell() -> None:
    """Bell icon with popover showing past notifications.

    Badge logic: the red "!" indicator appears only when there are
    *unviewed* notifications. Clicking the bell (which opens the popover)
    marks all current notifications as viewed. "Dismiss All" clears the
    notification list entirely.
    """
    with Popover(title="Notifications", side="bottom"):
        # --- trigger (first child) ---
        with Div(css_class="relative inline-flex"):
            Button(
                "",
                icon="bell",
                variant="ghost",
                size="icon-sm",
                on_click=[SetState("has_unviewed_notifications", False)],
            )
            with If(STATE.has_unviewed_notifications):
                Badge(
                    "!",
                    css_class=(
                        "absolute -top-1 -right-1 w-4 h-4 p-0 "
                        "flex items-center justify-center "
                        "text-[10px] bg-red-500 text-white rounded-full "
                        "pointer-events-none"
                    ),
                )
        # --- content ---
        with Column(
            gap=1,
            style={"maxHeight": "16rem", "overflowY": "auto", "minWidth": "18rem"},
        ):
            with (
                If(STATE.notifications.length() > 0),
                Row(
                    justify="end",
                    style={"marginBottom": "0.25rem"},
                ),
            ):
                Button(
                    "Dismiss All",
                    variant="ghost",
                    size="xs",
                    on_click=[
                        SetState("notifications", []),
                        SetState("has_unviewed_notifications", False),
                    ],
                )
            with If(~(STATE.notifications.length() > 0)):
                Small("No notifications.")
            with (
                ForEach(STATE.notifications),
                Div(
                    style={
                        "padding": "0.4rem 0.5rem",
                        "borderBottom": "1px solid rgba(255,255,255,0.1)",
                        "fontSize": "0.8rem",
                    },
                ),
            ):
                Text(ITEM)


def render_login_card() -> None:
    with Div(css_class=PANEL_CARD_CLASS, style=_login_card_style()):
        with CardHeader():
            H2("Log in with Airbyte")
        with CardContent(), Column(gap=3):
            with If(STATE.oauth_authenticated):
                Text("You are signed in and ready to use Airbyte Ops.")
                with Row(gap=2):
                    Link("Continue to Airbyte Ops", href="/home", target="_top")
                    Button(
                        "Log out",
                        variant="outline",
                        css_class=BUTTON_OUTLINE_CLASS,
                        onClick=logout_oauth_action(),
                    )
            with If(~STATE.oauth_authenticated):
                Text("Use your Airbyte identity to access internal operations tools.")
                Button(
                    "Log in with Airbyte",
                    variant="info",
                    css_class=BUTTON_INFO_CLASS,
                    onClick=CallHandler("startOAuth"),
                )
            with If(STATE.oauth_status):
                Text(STATE.oauth_status)
