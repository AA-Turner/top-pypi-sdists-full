"""Billing overview components: status bar and current configuration panel."""

from __future__ import annotations

from prefab_ui.components import (
    Badge,
    CardContent,
    Column,
    Div,
    Grid,
    Markdown,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.theme import (
    PANEL_CARD_CLASS,
    STATUS_CARD_CLASS,
    _card_style,
)


def render_status_bar() -> None:
    """Render the 3-card status bar: Organization, Payment Status, Customer Tier."""
    with Grid(columns=3, gap=3):
        _render_org_card()
        _render_payment_status_card()
        _render_tier_card()


def _render_org_card() -> None:
    with (
        Div(css_class=STATUS_CARD_CLASS, style=_card_style()),
        CardContent(),
        Column(gap=1),
    ):
        Text(
            "Organization",
            style={"fontSize": "0.75rem", "opacity": "0.7", "fontWeight": "600"},
        )
        Text(
            content=STATE.org_info.organization_name,
            style={"fontSize": "1.25rem", "fontWeight": "700"},
        )
        Text(
            content=STATE.org_info.organization_id,
            style={"fontSize": "0.75rem", "opacity": "0.6"},
        )
        with If(STATE.org_info.email):
            Text(
                content=STATE.org_info.email,
                style={"fontSize": "0.75rem", "opacity": "0.6"},
            )


def _render_payment_status_card() -> None:
    with (
        Div(css_class=STATUS_CARD_CLASS, style=_card_style()),
        CardContent(),
        Column(gap=1),
    ):
        Text(
            "Payment Status",
            style={"fontSize": "0.75rem", "opacity": "0.7", "fontWeight": "600"},
        )
        Text(
            content=STATE.payment_config.payment_status,
            style={"fontSize": "1.25rem", "fontWeight": "700"},
        )
        with If(STATE.payment_config.grace_period_end_at):
            Text(
                content=STATE.payment_config.grace_period_end_at,
                style={"fontSize": "0.75rem", "opacity": "0.6"},
            )


def _render_tier_card() -> None:
    with (
        Div(css_class=STATUS_CARD_CLASS, style=_card_style()),
        CardContent(),
        Column(gap=1),
    ):
        Text(
            "Customer Tier",
            style={"fontSize": "0.75rem", "opacity": "0.7", "fontWeight": "600"},
        )
        Text(
            content=STATE.payment_config.customer_tier,
            style={"fontSize": "1.25rem", "fontWeight": "700"},
        )
        with If(STATE.payment_config.tier_warning):
            Badge(
                STATE.payment_config.tier_warning,
                css_class="w-fit bg-[#B42318] text-white",
            )


def render_billing_config() -> None:
    """Render the left-panel read-only billing configuration summary."""
    with (
        Div(css_class=PANEL_CARD_CLASS, style=_card_style()),
        CardContent(),
        Column(gap=3),
    ):
        Text(
            "Current Billing Configuration",
            style={"fontWeight": "700", "fontSize": "1.125rem"},
        )
        _render_config_field("Payment Status", STATE.payment_config.payment_status)
        _render_config_field(
            "Subscription Status", STATE.payment_config.subscription_status
        )
        _render_config_field(
            "Grace Period Ends", STATE.payment_config.grace_period_end_at
        )
        _render_config_field(
            "Usage Category", STATE.payment_config.usage_category_overwrite
        )
        _render_config_field(
            "Payment Provider", STATE.payment_config.payment_provider_id
        )

        with If(STATE.payment_config.orb_subscription):
            Markdown("**Orb Subscription**")
            _render_config_field(
                "Plan", STATE.payment_config.orb_subscription.plan_name
            )
            _render_config_field("Status", STATE.payment_config.orb_subscription.status)
            _render_config_field(
                "Start", STATE.payment_config.orb_subscription.start_date
            )
            _render_config_field("End", STATE.payment_config.orb_subscription.end_date)
            _render_config_field(
                "Orb Customer", STATE.payment_config.orb_subscription.orb_customer_id
            )


def _render_config_field(label: str, value: object) -> None:
    """Render a single label-value row."""
    with Grid(columns=2, gap=2):
        Text(
            label,
            style={"fontSize": "0.875rem", "opacity": "0.7"},
        )
        Text(
            content=value,
            style={"fontSize": "0.875rem", "fontWeight": "500"},
        )
