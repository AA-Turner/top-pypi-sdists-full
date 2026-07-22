"""Airbyte Ops home page."""

from fastmcp import FastMCP, FastMCPApp
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    H3,
    Badge,
    CardContent,
    Column,
    Grid,
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
from airbyte_ops_webapp.pages.home.agents import (
    HOME_AGENTS_CALLOUT,
)
from airbyte_ops_webapp.pages.motherduck_diagnostics.defaults import (
    MOTHERDUCK_DIAGNOSTICS_EMOJI,
    MOTHERDUCK_DIAGNOSTICS_PATH,
)
from airbyte_ops_webapp.pages.shared_components.layout import (
    OPS_HOME_LABEL,
    render_breadcrumb_nav,
    render_environment_banners,
    render_page_hero,
    render_version_footer,
)
from airbyte_ops_webapp.state import OpsPageState
from airbyte_ops_webapp.theme import (
    AIRBYTE_LAVENDER,
    AIRBYTE_PRIMARY,
    AIRBYTE_SECONDARY,
    PAGE_CLASS,
    AbPage,
    AbPrimaryLink,
    AbToolCard,
    AbToolIcon,
    _more_tools_icon_svg,
)

OPS_HOME_TOOL_NAME = "ops_home"

home_app = FastMCPApp("Airbyte Ops Home")


def _render_tool_icon(icon_svg: str, *, accent: str = AIRBYTE_PRIMARY) -> None:
    with AbToolIcon(accent=accent):
        Svg(icon_svg, width="1.5rem", height="1.5rem")


def _render_emoji_icon(emoji: str, *, accent: str = AIRBYTE_PRIMARY) -> None:
    """Render an emoji inside the same styled container as SVG tool icons."""
    with AbToolIcon(accent=accent):
        Text(emoji, css_class="text-2xl leading-none")


def _render_connector_version_manager_card(connector_query: str) -> None:
    with (
        AbToolCard(),
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
            AbPrimaryLink(
                "Log in with Airbyte",
                href=OPS_AUTHORIZATION_PATH,
                target="_top",
            )
        with If(STATE.oauth_authenticated):
            Badge("Ready", variant="success")
            AbPrimaryLink(
                "Open tool",
                href=connector_version_manager_path(connector_query),
                target="_top",
            )


def _render_customer_billing_card() -> None:
    with (
        AbToolCard(),
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
            AbPrimaryLink(
                "Log in with Airbyte",
                href=OPS_AUTHORIZATION_PATH,
                target="_top",
            )
        with If(STATE.oauth_authenticated):
            Badge("Ready", variant="success")
            AbPrimaryLink(
                "Open tool",
                href=CUSTOMER_BILLING_PATH,
                target="_top",
            )


def _render_motherduck_diagnostics_card() -> None:
    with (
        AbToolCard(),
        CardContent(),
        Column(gap=3),
    ):
        _render_emoji_icon(MOTHERDUCK_DIAGNOSTICS_EMOJI)
        H3("MotherDuck Diagnostics")
        Text(
            "Compute-usage analytics, recent query outcomes, and live server "
            "connections for MotherDuck."
        )
        with If(~STATE.oauth_authenticated):
            Badge(
                "Sign-in required",
                css_class="w-fit bg-[#CECBF2] text-[#140F43]",
            )
            AbPrimaryLink(
                "Log in with Airbyte",
                href=OPS_AUTHORIZATION_PATH,
                target="_top",
            )
        with If(STATE.oauth_authenticated):
            Badge("Ready", variant="success")
            AbPrimaryLink(
                "Open tool",
                href=MOTHERDUCK_DIAGNOSTICS_PATH,
                target="_top",
            )


def _render_more_tools_card() -> None:
    with (
        AbToolCard(accent=AIRBYTE_LAVENDER),
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
    state = OpsPageState.from_env(
        oauth_config=current_oauth_config,
        default_connector_from_args=explicit_default_connector,
    ).to_prefab_state()

    with (
        build_ops_app(
            title="Airbyte Ops",
            state=state,
            oauth_issuer=current_oauth_config.issuer,
        ) as app,
        AbPage(onMount=hydrate_oauth_action()),
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
            agents_callout=HOME_AGENTS_CALLOUT,
        )

        with Grid(columns=3, gap=4):
            _render_connector_version_manager_card(connector_query)
            _render_customer_billing_card()
            _render_motherduck_diagnostics_card()
            _render_more_tools_card()
        render_version_footer()
    return app


def register_home_app(mcp: FastMCP) -> None:
    """Register the Airbyte Ops home app with the MCP server."""
    mcp.add_provider(home_app)
