"""Typed Prefab state model for the Customer Billing page.

`CustomerBillingPageState` is the single source of truth for the page's initial
state. It extends the shared `OpsPageState` (env / deploy / auth) and the shared
`OrgLookupModalState`, then adds the billing-specific fields. Building initial
state through this model means a mistyped, missing, or extra initial-state key
fails at page-build / type-check time instead of silently in the browser.

Runtime tool results (`RESULT.*`) may replace the nested fields (`org_info`,
`payment_config`, `apply_result`) wholesale with a richer shape; these models
describe the *initial* placeholder shape only.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from airbyte_ops_webapp.pages.shared_components.org_lookup_modal import (
    OrgLookupModalState,
)
from airbyte_ops_webapp.state import OpsPageState


class BillingOrgInfo(BaseModel):
    """Organization identity placeholder for the initial billing state."""

    model_config = ConfigDict(frozen=True)

    organization_id: str = ""
    organization_name: str = ""
    email: str = ""


class BillingPaymentConfig(BaseModel):
    """Payment-config placeholder for the initial billing state."""

    model_config = ConfigDict(frozen=True)

    organization_id: str = ""
    payment_status: str = ""
    subscription_status: str = ""
    payment_provider_id: str = ""
    grace_period_end_at: str = ""
    usage_category_overwrite: str = ""
    customer_tier: str = ""
    tier_warning: str = ""
    orb_subscription: object | None = None


class BillingApplyResult(BaseModel):
    """Apply-result placeholder for the initial billing state.

    A successful apply replaces this in state with the full tool result; the
    initial value only needs `success` and `message`.
    """

    model_config = ConfigDict(frozen=True)

    success: bool = False
    message: str = ""


class CustomerBillingPageState(OpsPageState, OrgLookupModalState):
    """Complete initial Prefab state for the Customer Billing page."""

    # Organization lookup
    org_query: str = ""
    org_info: BillingOrgInfo = Field(default_factory=BillingOrgInfo)
    payment_config: BillingPaymentConfig = Field(default_factory=BillingPaymentConfig)
    resolved_org_label: str = ""
    org_loaded: bool = False
    lookup_error: str = ""

    # Grace period form
    grace_period_value: str = ""
    grace_period_reason: str = ""

    # Permanent waiver form
    waiver_type: str = "free"
    waiver_reason: str = ""

    # Billing action tab
    billing_action_tab: str = "grace_period"

    # Confirmation dialogs
    grace_period_confirm_open: bool = False
    waiver_confirm_open: bool = False

    # Result modal
    apply_result: BillingApplyResult = Field(default_factory=BillingApplyResult)
    result_modal_open: bool = False
