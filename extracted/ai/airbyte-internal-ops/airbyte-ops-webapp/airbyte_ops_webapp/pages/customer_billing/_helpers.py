"""Shared helpers for the Customer Billing page."""

from __future__ import annotations

import json
import os
from typing import Any

from prefab_ui.actions import SetState, ShowToast
from prefab_ui.components import SelectOption
from prefab_ui.rx import RESULT

from airbyte_ops_webapp.state import (
    AIRBYTE_BEARER_TOKEN_ENV_VAR,
    AIRBYTE_CONFIG_API_ROOT_ENV_VAR,
    mock_only_enabled,
)

DEFAULT_ADMIN_USER_EMAIL = "devin-local@example.com"


# ---------------------------------------------------------------------------
# Auth / config helpers
# ---------------------------------------------------------------------------


def auth_available(bearer_token_override: str | None = None) -> bool:
    """Return `True` when Cloud API credentials are available."""
    if mock_only_enabled():
        return True
    if os.getenv(AIRBYTE_BEARER_TOKEN_ENV_VAR):
        return True
    return bool(bearer_token_override)


def resolved_config_api_root() -> str:
    """Return the Config API root URL from env or the Cloud default."""
    return (
        os.getenv(AIRBYTE_CONFIG_API_ROOT_ENV_VAR) or "https://cloud.airbyte.com/api/v1"
    )


def resolved_bearer_token(override: str | None = None) -> str | None:
    """Return the bearer token from override or env."""
    return override or os.getenv(AIRBYTE_BEARER_TOKEN_ENV_VAR) or None


# ---------------------------------------------------------------------------
# Data formatting
# ---------------------------------------------------------------------------


def json_text(value: Any) -> str:
    """Pretty-print a value as JSON."""
    return json.dumps(value, indent=2, sort_keys=True)


def empty_org_state() -> dict[str, str]:
    """Empty org placeholder for state initialization."""
    return {
        "organization_id": "",
        "organization_name": "",
        "email": "",
    }


def empty_payment_config() -> dict[str, Any]:
    """Empty payment config placeholder for state initialization."""
    return {
        "organization_id": "",
        "payment_status": "",
        "subscription_status": "",
        "payment_provider_id": "",
        "grace_period_end_at": "",
        "usage_category_overwrite": "",
        "customer_tier": "",
        "tier_warning": "",
        "orb_subscription": None,
    }


# ---------------------------------------------------------------------------
# UI option renderers
# ---------------------------------------------------------------------------


def render_select_options(options: list[dict[str, str]]) -> None:
    """Render a list of `SelectOption` components."""
    for option in options:
        SelectOption(label=option["label"], value=option["value"])


# ---------------------------------------------------------------------------
# State action builders
# ---------------------------------------------------------------------------


def start_tool_call(message: str) -> list[SetState]:
    """Set loading state before a tool call."""
    return [
        SetState("is_loading", True),
        SetState("loading_message", message),
        SetState("tool_error", ""),
    ]


def finish_tool_call() -> list[SetState]:
    """Clear loading state after a successful tool call."""
    return [
        SetState("is_loading", False),
        SetState("loading_message", ""),
        SetState("tool_error", ""),
    ]


def fail_tool_call(message: Any) -> list[Any]:
    """Set error state after a failed tool call."""
    return [
        SetState("is_loading", False),
        SetState("loading_message", ""),
        SetState("tool_error", message),
        ShowToast("Tool call failed", description=message, variant="error"),
    ]


def lookup_success_actions() -> list[SetState]:
    """State updates after a successful org lookup."""
    return [
        *finish_tool_call(),
        SetState("org_info", RESULT.org_info),
        SetState("payment_config", RESULT.payment_config),
        SetState("resolved_org_label", RESULT.resolved_org_label),
        SetState("org_loaded", RESULT.org_loaded),
        SetState("lookup_error", RESULT.lookup_error),
    ]


# Static error messages for on_error handlers (transport-level failures).
# Tool functions handle application errors internally via on_success path.
LOOKUP_ERROR = "Organization lookup failed. Please try again."
APPLY_ERROR = "Apply operation failed. Please try again."


def lookup_fail_actions() -> list[Any]:
    """State updates after a failed org lookup."""
    return [
        *fail_tool_call(LOOKUP_ERROR),
        SetState("org_loaded", False),
        SetState("lookup_error", LOOKUP_ERROR),
    ]


def apply_success_actions() -> list[Any]:
    """State updates after a successful apply operation."""
    return [
        *finish_tool_call(),
        SetState("apply_result", RESULT),
        SetState("result_modal_open", True),
    ]


def apply_fail_actions() -> list[Any]:
    """State updates after a failed apply operation."""
    return [
        *fail_tool_call(APPLY_ERROR),
        SetState("apply_result", {"success": False, "message": APPLY_ERROR}),
        SetState("result_modal_open", True),
    ]
