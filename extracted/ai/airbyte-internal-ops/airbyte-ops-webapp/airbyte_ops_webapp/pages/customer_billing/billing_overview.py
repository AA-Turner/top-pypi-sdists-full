"""Billing overview components: status bar and current configuration panel."""

from __future__ import annotations

from prefab_ui.components import (
    Badge,
    CardContent,
    Column,
    Grid,
    Markdown,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.theme import (
    AbCard,
    AbCardLabel,
    AbCardMeta,
    AbCardValue,
    AbFieldLabel,
    AbFieldValue,
    AbSectionTitle,
    AbStatusCard,
)


def render_status_bar() -> None:
    """Render the 3-card status bar: Organization, Payment Status, Customer Tier."""
    with Grid(columns=3, gap=3):
        _render_org_card()
        _render_payment_status_card()
        _render_tier_card()


def _render_org_card() -> None:
    with (
        AbStatusCard(),
        CardContent(),
        Column(gap=1),
    ):
        AbCardLabel("Organization")
        AbCardValue(content=STATE.org_info.organization_name)
        AbCardMeta(content=STATE.org_info.organization_id)
        with If(STATE.org_info.email):
            AbCardMeta(content=STATE.org_info.email)


def _render_payment_status_card() -> None:
    with (
        AbStatusCard(),
        CardContent(),
        Column(gap=1),
    ):
        AbCardLabel("Payment Status")
        AbCardValue(content=STATE.payment_config.payment_status)
        with If(STATE.payment_config.grace_period_end_at):
            AbCardMeta(content=STATE.payment_config.grace_period_end_at)


def _render_tier_card() -> None:
    with (
        AbStatusCard(),
        CardContent(),
        Column(gap=1),
    ):
        AbCardLabel("Customer Tier")
        AbCardValue(content=STATE.payment_config.customer_tier)
        with If(STATE.payment_config.tier_warning):
            Badge(
                STATE.payment_config.tier_warning,
                css_class="w-fit bg-[#B42318] text-white",
            )


def render_billing_config() -> None:
    """Render the left-panel read-only billing configuration summary."""
    with (
        AbCard(),
        CardContent(),
        Column(gap=3),
    ):
        AbSectionTitle("Current Billing Configuration")
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
        AbFieldLabel(label)
        AbFieldValue(content=value)
