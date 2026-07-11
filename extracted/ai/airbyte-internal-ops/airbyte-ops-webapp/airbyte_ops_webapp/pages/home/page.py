"""Airbyte Ops home page."""

from fastmcp import FastMCP, FastMCPApp
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    H3,
    Badge,
    CardContent,
    Column,
    Div,
    Grid,
    Link,
    Svg,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.app_shell import build_ops_app
from airbyte_ops_webapp.auth.oauth import hydrate_oauth_action, oauth_config
from airbyte_ops_webapp.pages.authorization.defaults import OPS_AUTHORIZATION_PATH
from airbyte_ops_webapp.pages.connector_version_manager.defaults import (
    CONNECTOR_VERSION_MANAGER_EMOJI,
    connector_version_manager_path,
    default_connector_query,
)
from airbyte_ops_webapp.pages.customer_billing.defaults import (
    CUSTOMER_BILLING_EMOJI,
    CUSTOMER_BILLING_PATH,
)
from airbyte_ops_webapp.pages.shared_components.layout import (
    OPS_HOME_LABEL,
    render_breadcrumb_nav,
    render_environment_banners,
    render_page_hero,
    render_version_footer,
)
from airbyte_ops_webapp.state import (
    OpsPageState,
    deploy_sha,
    deploy_sha_url,
    mock_only_enabled,
    ops_package_version,
    preview_deploy_enabled,
    preview_pr_number,
    preview_pr_url,
)
from airbyte_ops_webapp.theme import (
    AIRBYTE_LAVENDER,
    AIRBYTE_PRIMARY,
    AIRBYTE_SECONDARY,
    PAGE_CLASS,
    PANEL_CARD_CLASS,
    _more_tools_icon_svg,
    _page_style,
    _primary_link_style,
    _tool_card_style,
    _tool_icon_style,
)

OPS_HOME_TOOL_NAME = "ops_home"

home_app = FastMCPApp("Airbyte Ops Home")


def _render_tool_icon(icon_svg: str, *, accent: str = AIRBYTE_PRIMARY) -> None:
    with Div(style=_tool_icon_style(accent=accent)):
        Svg(icon_svg, width="1.5rem", height="1.5rem")


def _render_emoji_icon(emoji: str, *, accent: str = AIRBYTE_PRIMARY) -> None:
    """Render an emoji inside the same styled container as SVG tool icons."""
    Text(
        emoji,
        style={
            **_tool_icon_style(accent=accent),
            "fontSize": "1.5rem",
            "lineHeight": "1",
        },
    )


def _render_connector_version_manager_card(connector_query: str) -> None:
    with (
        Div(css_class=PANEL_CARD_CLASS, style=_tool_card_style(accent=AIRBYTE_PRIMARY)),
        CardContent(),
        Column(gap=3),
    ):
        _render_emoji_icon(CONNECTOR_VERSION_MANAGER_EMOJI)
        H3("Connector Version Manager")
        Text(
            "Manage connector rollout versions, scoped pins, and safe previews "
            "before applying production changes."
        )
        with If(~STATE.oauth_authenticated):
            Badge(
                "Sign-in required",
                css_class="w-fit bg-[#CECBF2] text-[#140F43]",
            )
            Link(
                "Log in with Airbyte",
                href=OPS_AUTHORIZATION_PATH,
                target="_top",
                style=_primary_link_style(),
            )
        with If(STATE.oauth_authenticated):
            Badge("Ready", variant="success")
            Link(
                "Open tool",
                href=connector_version_manager_path(connector_query),
                target="_top",
                style=_primary_link_style(),
            )


def _render_customer_billing_card() -> None:
    with (
        Div(css_class=PANEL_CARD_CLASS, style=_tool_card_style(accent=AIRBYTE_PRIMARY)),
        CardContent(),
        Column(gap=3),
    ):
        _render_emoji_icon(CUSTOMER_BILLING_EMOJI)
        H3("Customer Billing")
        Text(
            "Manage grace periods, billing waivers, and usage category overrides "
            "for organizations."
        )
        with If(~STATE.oauth_authenticated):
            Badge(
                "Sign-in required",
                css_class="w-fit bg-[#CECBF2] text-[#140F43]",
            )
            Link(
                "Log in with Airbyte",
                href=OPS_AUTHORIZATION_PATH,
                target="_top",
                style=_primary_link_style(),
            )
        with If(STATE.oauth_authenticated):
            Badge("Ready", variant="success")
            Link(
                "Open tool",
                href=CUSTOMER_BILLING_PATH,
                target="_top",
                style=_primary_link_style(),
            )


def _render_more_tools_card() -> None:
    with (
        Div(
            css_class=PANEL_CARD_CLASS, style=_tool_card_style(accent=AIRBYTE_LAVENDER)
        ),
        CardContent(),
        Column(gap=3),
    ):
        _render_tool_icon(_more_tools_icon_svg(), accent=AIRBYTE_SECONDARY)
        H3("More Tools Coming Soon")
        Text(
            "This home will expand as more internal operations workflows move into "
            "Airbyte Ops."
        )
        Badge("Coming soon", css_class="w-fit bg-[#CECBF2] text-[#140F43]")


@home_app.ui(name=OPS_HOME_TOOL_NAME, title="Airbyte Ops")
def open_ops_home(
    query: str = "",
    connector_name: str = "",
    connector: str = "",
) -> PrefabApp:
    """Open the Airbyte Ops home page."""
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
    state = OpsPageState(
        default_connector_from_args=explicit_default_connector,
        is_mock_only=mock_only_enabled(),
        is_preview_deploy=preview_deploy_enabled(),
        preview_pr_number=preview_pr_number(),
        preview_pr_url=preview_pr_url(),
        deploy_sha=deploy_sha(),
        deploy_sha_url=deploy_sha_url(),
        ops_package_version=ops_package_version(),
        oauth_config=current_oauth_config,
        oauth_enabled=bool(current_oauth_config["enabled"]),
    ).to_prefab_state()

    with (
        build_ops_app(
            title="Airbyte Ops",
            state=state,
            oauth_issuer=str(current_oauth_config["issuer"]),
        ) as app,
        Div(style=_page_style(), onMount=hydrate_oauth_action()),
        Column(gap=5, css_class=PAGE_CLASS),
    ):
        render_environment_banners()
        render_breadcrumb_nav(current_page=OPS_HOME_LABEL)
        render_page_hero(
            title="Airbyte Ops",
            description=(
                "A focused internal home for Airbyte operational workflows, "
                "safe previews, and controlled production changes."
            ),
            show_auth_controls=True,
        )

        with Grid(columns=3, gap=4):
            _render_connector_version_manager_card(connector_query)
            _render_customer_billing_card()
            _render_more_tools_card()
        render_version_footer()
    return app


def register_home_app(mcp: FastMCP) -> None:
    """Register the Airbyte Ops home app with the MCP server."""
    mcp.add_provider(home_app)
