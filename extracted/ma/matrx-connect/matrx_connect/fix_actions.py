"""THE ONE VOCABULARY of ``fix_action`` — the machine-readable way through a refusal.

Law: ``common-docs/policies/no-unapproved-restrictions.md`` + ``no-dead-ends.md`` rule 16 —
every block a person can get past carries its way through. The server's refusals say it as
DATA (``fix_action``: one token below) so a client opens the right door (a sign-in sheet, the
organization picker, the age dialog, the plan page ...) without parsing a sentence.

Status codes and wording of a refusal never change because of this token; it is metadata only.
The client side keys on the same strings (``apps/matrx-frontend/lib/diagnostics/errorTierRules.ts``).

Lives in matrx-connect because it is the bottom of the graph every refusing package already
imports (pure: no I/O, no aidream import).
"""

from __future__ import annotations

from typing import Any, Final

FIX_SIGN_IN: Final = "sign_in"
FIX_SIGN_UP: Final = "sign_up"
FIX_PICK_ORGANIZATION: Final = "pick_organization"
FIX_DECLARE_AGE: Final = "declare_age"
FIX_GUARDIAN_CONSENT: Final = "guardian_consent"
FIX_UPGRADE_PLAN: Final = "upgrade_plan"
FIX_ADD_POINTS: Final = "add_points"
FIX_CONNECT_INTEGRATION: Final = "connect_integration"
FIX_GRANT_PERMISSION: Final = "grant_permission"
FIX_OPEN_SETTINGS: Final = "open_settings"

#: Every token the platform-wide vocabulary names. Domain-specific tokens that predate it
#: (``approve_run``, ``connect_mailbox``, ``open_device`` ...) stay with their own domain.
PLATFORM_FIX_TOKENS: Final[frozenset[str]] = frozenset({
    FIX_SIGN_IN, FIX_SIGN_UP, FIX_PICK_ORGANIZATION, FIX_DECLARE_AGE, FIX_GUARDIAN_CONSENT,
    FIX_UPGRADE_PLAN, FIX_ADD_POINTS, FIX_CONNECT_INTEGRATION, FIX_GRANT_PERMISSION,
    FIX_OPEN_SETTINGS,
})

#: Refusal code -> the token a person can use to get past it. Only codes whose cause the
#: person can fix in the product belong here.
FIX_ACTION_BY_CODE: Final[dict[str, str]] = {
    "organization_required": FIX_PICK_ORGANIZATION,
    "organization_context_required": FIX_PICK_ORGANIZATION,  # the client transport kernel's own code
    "education_age_declaration_required": FIX_DECLARE_AGE,
    "education_coppa_consent_required": FIX_GUARDIAN_CONSENT,
    "not_signed_in": FIX_SIGN_IN,
    "sign_in_required": FIX_SIGN_IN,
    "session_required": FIX_SIGN_IN,
    "unauthorized": FIX_SIGN_IN,
    "guest_identity_rate_limited": FIX_SIGN_IN,
    "points_exhausted": FIX_UPGRADE_PLAN,  # what the client usage-gate opens today (usageGate.ts upgrade_plan)
    "not_connected": FIX_CONNECT_INTEGRATION,
    "connection_needs_attention": FIX_CONNECT_INTEGRATION,
    "usage_limit_reached": FIX_UPGRADE_PLAN,
    "free_tier_model_refused": FIX_UPGRADE_PLAN,
    "missing_permission": FIX_GRANT_PERMISSION,
    "missing_api_key": FIX_OPEN_SETTINGS,
}


def fix_action_for(code: str | None) -> str | None:
    """The fix token for a refusal ``code``, or ``None`` when the person cannot fix it."""
    return FIX_ACTION_BY_CODE.get(code or "")


def with_fix_action(body: dict[str, Any], code: str | None = None) -> dict[str, Any]:
    """Return ``body`` carrying ``fix_action`` for ``code`` (or ``body['code']``), never overwriting one already set."""
    token = fix_action_for(code or body.get("code") or body.get("error"))
    if token and not body.get("fix_action"):
        body = {**body, "fix_action": token}
    return body


__all__ = [
    "FIX_ACTION_BY_CODE", "FIX_ADD_POINTS", "FIX_CONNECT_INTEGRATION", "FIX_DECLARE_AGE",
    "FIX_GRANT_PERMISSION", "FIX_GUARDIAN_CONSENT", "FIX_OPEN_SETTINGS", "FIX_PICK_ORGANIZATION",
    "FIX_SIGN_IN", "FIX_SIGN_UP", "FIX_UPGRADE_PLAN", "PLATFORM_FIX_TOKENS",
    "fix_action_for", "with_fix_action",
]
