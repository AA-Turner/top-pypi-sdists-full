"""Tool: account — Manage LinkedIn accounts (list, switch, unlink, search account).

Thin dispatcher that routes to existing run_* functions based on the action parameter.
"""

from __future__ import annotations

import logging
from ..db.async_bridge import run_db


logger = logging.getLogger(__name__)


async def run_account(
    action: str = "list",
    account_id: str = "",
) -> str:
    """Manage LinkedIn accounts.

    Actions:
      list               — Show all connected LinkedIn accounts (with Sales Nav badge)
      switch             — List accounts and pick one to switch to
      switch_to          — Switch to a specific account by ID
      unlink             — Disconnect the current LinkedIn account
      set_search_account — Pin a specific account for premium search
      get_search_account — Show current premium search account

    Args:
        action: What to do.
        account_id: The Unipile account ID (required for 'switch_to', 'set_search_account').
    """
    action = action.lower().strip()

    if action == "list":
        from .switch_account import run_list_linkedin_accounts
        return await run_list_linkedin_accounts()

    if action == "switch":
        from .switch_account import run_switch_account
        return await run_switch_account()

    if action == "switch_to":
        if not account_id:
            return "Error: 'account_id' is required for action='switch_to'. Use account(action='list') to see IDs."
        from .switch_account import run_switch_account_to
        return await run_switch_account_to(account_id)

    if action == "unlink":
        from .unlink_account import run_unlink_account
        return await run_unlink_account()

    if action == "set_search_account":
        if not account_id:
            return "Error: 'account_id' required. Use account(action='list') to see IDs."
        return await _set_search_account(account_id)

    if action in ("get_search_account", "search_account"):
        return _get_search_account()

    return (
        f"Unknown action: '{action}'. Use 'list', 'switch', 'switch_to', "
        "'unlink', 'set_search_account', or 'get_search_account'."
    )


async def _set_search_account(account_id: str) -> str:
    """Validate and pin a specific account for premium search."""
    from ..db.queries import save_setting
    from ..linkedin import get_linkedin_client, UnipileError

    try:
        client = get_linkedin_client()
    except UnipileError as e:
        return f"❌ {e}"

    try:
        # Verify the account exists
        connected, status_msg = await client.verify_account(account_id)
        if not connected:
            return f"❌ Account `{account_id}` is not connected: {status_msg}"

        # Check Sales Navigator
        has_sn = await client.detect_sales_navigator(account_id)

        import time
        await run_db(save_setting, "premium_search_account_id", account_id)
        await run_db(save_setting, "premium_search_detected_at", int(time.time()))

        sn_badge = " (Sales Navigator)" if has_sn else " (no Sales Navigator)"
        return (
            f"✅ Search account set to `{account_id}`{sn_badge}\n\n"
            "All future campaign searches and ICP enrichment will use this account.\n"
            "Use `account(action='get_search_account')` to verify."
        )
    except Exception as e:
        return f"❌ Failed to set search account: {e}"
    finally:
        await client.close()


def _get_search_account() -> str:
    """Show the current premium search account."""
    from ..services.search_account_resolver import get_cached_search_account
    from ..db.queries import get_setting

    cached = get_cached_search_account()
    own = get_setting("unipile_account_id", "")

    if cached and cached != own:
        return (
            f"**Premium search account:** `{cached}`\n"
            f"**Sending account:** `{own}`\n\n"
            "Campaign searches and ICP enrichment route through the premium account.\n"
            "Use `account(action='set_search_account', account_id='...')` to change."
        )
    if cached == own:
        return (
            f"**Search & sending account:** `{own}` (same account, has Sales Navigator)\n\n"
            "Use `account(action='set_search_account', account_id='...')` to use a different account for search."
        )
    return (
        "No premium search account configured. Auto-detection runs on next campaign creation.\n\n"
        "Use `account(action='set_search_account', account_id='...')` to pin one manually."
    )
