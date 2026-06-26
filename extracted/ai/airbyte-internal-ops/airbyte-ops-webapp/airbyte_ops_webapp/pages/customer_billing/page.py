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
    Div,
    Grid,
    Markdown,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.app_shell import build_ops_app
from airbyte_ops_webapp.auth.google_oauth import hydrate_google_oauth_action
from airbyte_ops_webapp.auth.oauth import hydrate_oauth_action, oauth_config
from airbyte_ops_webapp.pages.customer_billing._helpers import (
    empty_org_state,
    empty_payment_config,
)
from airbyte_ops_webapp.pages.customer_billing._mcp_tools import (
    customer_billing_app,
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
)
from airbyte_ops_webapp.pages.shared_components.org_lookup_modal import (
    org_lookup_modal_state,
)
from airbyte_ops_webapp.state import (
    mock_only_enabled,
    preview_deploy_enabled,
    preview_pr_number,
    preview_pr_url,
)
from airbyte_ops_webapp.theme import (
    AIRBYTE_PRIMARY,
    ERROR_CARD_CLASS,
    PAGE_CLASS,
    PREVIEW_CARD_CLASS,
    _card_style,
    _page_style,
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
        oauth_issuer=str(current_oauth_config["issuer"]),
    ) as app:
        with Div(
            style=_page_style(),
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

    return app


# ---------------------------------------------------------------------------
# Small inline sections
# ---------------------------------------------------------------------------


def _render_loading_banner() -> None:
    with If(STATE.loading_message):
        with Div(
            css_class=PREVIEW_CARD_CLASS,
            style=_card_style(accent=AIRBYTE_PRIMARY),
        ):
            with CardContent(), Column(gap=1):
                Markdown("**Loading**")
                Text(STATE.loading_message)


def _render_error_banner() -> None:
    with If(STATE.tool_error):
        with Div(
            css_class=ERROR_CARD_CLASS,
            style=_card_style(accent="#ff6b6b"),
        ):
            with CardContent(), Column(gap=1):
                Markdown("**Tool call failed**")
                Text(STATE.tool_error)


# ---------------------------------------------------------------------------
# State initialization
# ---------------------------------------------------------------------------


def _build_initial_state(
    *,
    current_oauth_config: dict[str, object],
) -> dict[str, object]:
    return {
        **org_lookup_modal_state(),
        # Organization lookup
        "org_query": "",
        "org_info": empty_org_state(),
        "payment_config": empty_payment_config(),
        "resolved_org_label": "",
        "org_loaded": False,
        "lookup_error": "",
        # Grace period form
        "grace_period_value": "",
        "grace_period_reason": "",
        # Permanent waiver form
        "waiver_type": "free",
        "waiver_reason": "",
        # Billing action tab
        "billing_action_tab": "grace_period",
        # Confirmation dialogs
        "grace_period_confirm_open": False,
        "waiver_confirm_open": False,
        # Result modal
        "apply_result": {"success": False, "message": ""},
        "result_modal_open": False,
        # Loading / error
        "is_loading": False,
        "loading_message": "",
        "tool_error": "",
        # Auth (Airbyte)
        "auth_bearer_token": "",
        "is_mock_only": mock_only_enabled(),
        "is_preview_deploy": preview_deploy_enabled(),
        "preview_pr_number": preview_pr_number(),
        "preview_pr_url": preview_pr_url(),
        "oauth_config": current_oauth_config,
        "oauth_enabled": current_oauth_config["enabled"],
        "oauth_authenticated": False,
        "oauth_status": "",
        "oauth_user_email": "",
        # Auth (Google)
        "google_authenticated": False,
        "google_user_email": "",
        "google_access_token": "",
        "google_status": "",
    }


def register_customer_billing_app(mcp: FastMCP) -> None:
    """Register the customer billing app with the MCP server."""
    mcp.add_provider(customer_billing_app)
