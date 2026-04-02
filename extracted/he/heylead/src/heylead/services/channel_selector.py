"""Channel selector — decide LinkedIn vs Email for each prospect.

Decision logic:
1. If no email account connected → LinkedIn only
2. If LinkedIn rate limits hit + prospect has email → Email overflow
3. If prospect has email + LinkedIn unanswered for 14 days → Email fallback
4. If campaign explicitly sets channel preference → respect it
5. Default: LinkedIn first (higher acceptance rate for warm outreach)
"""

from __future__ import annotations

import json
import logging
import time

from ..db.queries import get_outreach, get_setting

logger = logging.getLogger(__name__)

# Days before falling back to email after LinkedIn silence
EMAIL_FALLBACK_DAYS = 14
EMAIL_FALLBACK_SECONDS = EMAIL_FALLBACK_DAYS * 86400

# Channel constants
CHANNEL_LINKEDIN = "linkedin"
CHANNEL_EMAIL = "email"


def get_email_account_id() -> str:
    """Get the connected email account ID from settings."""
    return get_setting("email_account_id", "") or ""


def has_email_channel() -> bool:
    """Check if an email account is connected and available."""
    return bool(get_email_account_id())


def select_channel(
    outreach: dict | None = None,
    prospect: dict | None = None,
    campaign_config: dict | None = None,
    force_channel: str = "",
    linkedin_limit_hit: bool = False,
) -> str:
    """Select the best channel for this outreach.

    Args:
        outreach: Existing outreach record (if any).
        prospect: Prospect/contact data.
        campaign_config: Campaign config_json.
        force_channel: Override channel choice.
        linkedin_limit_hit: If True, LinkedIn daily/weekly limits are hit.
            Email will be preferred for prospects who have email addresses.

    Returns:
        "linkedin" or "email"
    """
    # Explicit override
    if force_channel == "dm":
        return "dm"  # Direct message to existing connection
    if force_channel in (CHANNEL_LINKEDIN, CHANNEL_EMAIL):
        if force_channel == CHANNEL_EMAIL and not has_email_channel():
            return CHANNEL_LINKEDIN
        return force_channel

    # Campaign-level preference
    if campaign_config:
        pref = campaign_config.get("channel", "")
        if pref == CHANNEL_EMAIL and has_email_channel():
            return CHANNEL_EMAIL
        if pref == CHANNEL_LINKEDIN and not linkedin_limit_hit:
            return CHANNEL_LINKEDIN

    # No email account → LinkedIn only (even if limited)
    if not has_email_channel():
        return CHANNEL_LINKEDIN

    # LinkedIn limit overflow → email for prospects with email addresses
    if linkedin_limit_hit:
        if prospect:
            email = _extract_email(prospect)
            if email:
                logger.info(
                    "LinkedIn limit hit — routing to email for %s",
                    prospect.get("name", "unknown"),
                )
                return CHANNEL_EMAIL
        # No email address available → LinkedIn (will be queued for later)
        return CHANNEL_LINKEDIN

    # If this outreach has been on LinkedIn for 14+ days with no reply → email
    if outreach:
        channel = outreach.get("channel") or CHANNEL_LINKEDIN
        if channel == CHANNEL_LINKEDIN:
            invited_at = outreach.get("invited_at") or 0
            status = outreach.get("status", "")
            # Only fall back if invited but never got reply/accept
            if (
                invited_at
                and status == "invited"
                and (time.time() - invited_at) > EMAIL_FALLBACK_SECONDS
            ):
                return CHANNEL_EMAIL

    # Check if prospect has a known email address
    if prospect:
        email = _extract_email(prospect)
        if not email:
            return CHANNEL_LINKEDIN

    # Default: LinkedIn first
    return CHANNEL_LINKEDIN


def should_email_fallback(outreach_id: str) -> bool:
    """Check if an outreach should fall back to email.

    Returns True if:
    - Email account is connected
    - Outreach was sent via LinkedIn 14+ days ago
    - No reply received
    """
    if not has_email_channel():
        return False

    outreach = get_outreach(outreach_id)
    if not outreach:
        return False

    channel = outreach.get("channel") or CHANNEL_LINKEDIN
    if channel != CHANNEL_LINKEDIN:
        return False

    invited_at = outreach.get("invited_at") or 0
    status = outreach.get("status", "")

    # Only fall back if invited but no response
    if invited_at and status == "invited":
        return (time.time() - invited_at) > EMAIL_FALLBACK_SECONDS

    return False


def _extract_email(prospect: dict) -> str:
    """Try to extract email from prospect profile data."""
    # Direct email field
    email = prospect.get("email") or ""
    if email:
        return email

    # From profile_json
    profile_json = prospect.get("profile_json") or ""
    if profile_json and isinstance(profile_json, str):
        try:
            profile = json.loads(profile_json)
            email = profile.get("email") or profile.get("email_address") or ""
            if email:
                return email
        except (json.JSONDecodeError, TypeError):
            pass

    return ""
