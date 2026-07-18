"""Customer Billing page.

Orchestrates the top-level layout. Each section is rendered by a dedicated
component module to keep the page definition readable and each component
individually maintainable.
"""

# ruff: noqa: SIM117

from __future__ import annotations

from fastmcp import FastMCP
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    CardContent,
    Column,
    Grid,
    Markdown,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.app_shell import build_ops_app
from airbyte_ops_webapp.auth.google_oauth import hydrate_google_oauth_action
from airbyte_ops_webapp.auth.oauth import hydrate_oauth_action, oauth_config
from airbyte_ops_webapp.pages.customer_billing._mcp_tools import (
    customer_billing_app,
)
from airbyte_ops_webapp.pages.customer_billing._state import (
    CustomerBillingPageState,
)
from airbyte_ops_webapp.pages.customer_billing.billing_actions import (
    render_billing_actions,
)
from airbyte_ops_webapp.pages.customer_billing.billing_overview import (
    render_billing_config,
    render_status_bar,
)
from airbyte_ops_webapp.pages.customer_billing.defaults import (
    CUSTOMER_BILLING_EMOJI,
    CUSTOMER_BILLING_TOOL_NAME,
)
from airbyte_ops_webapp.pages.customer_billing.org_lookup import (
    render_org_lookup,
)
from airbyte_ops_webapp.pages.customer_billing.result_modal import (
    render_result_modal,
)
from airbyte_ops_webapp.pages.shared_components.layout import (
    render_breadcrumb_nav,
    render_environment_banners,
    render_page_hero,
    render_version_footer,
)
from airbyte_ops_webapp.state import OAuthConfigState
from airbyte_ops_webapp.theme import (
    PAGE_CLASS,
    AbErrorCard,
    AbPage,
    AbPreviewCard,
)

# ---------------------------------------------------------------------------
# UI definition
# ---------------------------------------------------------------------------


@customer_billing_app.ui(
    name=CUSTOMER_BILLING_TOOL_NAME,
    title="Customer Billing",
    description="Manage organization payment status, grace periods, and billing waivers.",
)
def customer_billing() -> PrefabApp:
    """Open the Customer Billing page."""
    current_oauth_config = oauth_config()

    state = _build_initial_state(current_oauth_config=current_oauth_config)

    with build_ops_app(
        title=f"{CUSTOMER_BILLING_EMOJI} Customer Billing",
        state=state,
        oauth_issuer=current_oauth_config.issuer,
    ) as app:
        with AbPage(
            onMount=[hydrate_oauth_action(), hydrate_google_oauth_action()],
        ):
            with Column(gap=5, css_class=PAGE_CLASS):
                render_environment_banners()
                render_breadcrumb_nav(
                    current_page=f"{CUSTOMER_BILLING_EMOJI} Customer Billing",
                )
                render_page_hero(
                    title=f"{CUSTOMER_BILLING_EMOJI} Customer Billing",
                    description=(
                        "View and manage organization payment status, grace periods, "
                        "billing waivers, and Orb subscription plans."
                    ),
                    show_auth_controls=True,
                )
                _render_loading_banner()
                _render_error_banner()
                render_org_lookup()

                with If(STATE.org_loaded):
                    with Column(gap=4):
                        render_status_bar()
                        with Grid(columns=[3, 2], gap=4):
                            render_billing_config()
                            render_billing_actions()

                render_result_modal()
                render_version_footer()

    return app


# ---------------------------------------------------------------------------
# Small inline sections
# ---------------------------------------------------------------------------


def _render_loading_banner() -> None:
    with If(STATE.loading_message):
        with AbPreviewCard():
            with CardContent(), Column(gap=1):
                Markdown("**Loading**")
                Text(STATE.loading_message)


def _render_error_banner() -> None:
    with If(STATE.tool_error):
        with AbErrorCard():
            with CardContent(), Column(gap=1):
                Markdown("**Tool call failed**")
                Text(STATE.tool_error)


# ---------------------------------------------------------------------------
# State initialization
# ---------------------------------------------------------------------------


def _build_initial_state(
    *,
    current_oauth_config: OAuthConfigState,
) -> dict[str, object]:
    return CustomerBillingPageState.from_env(
        oauth_config=current_oauth_config
    ).to_prefab_state()


def register_customer_billing_app(mcp: FastMCP) -> None:
    """Register the customer billing app with the MCP server."""
    mcp.add_provider(customer_billing_app)
