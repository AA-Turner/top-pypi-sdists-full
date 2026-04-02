"""Search Account Resolver — find the best LinkedIn account for search operations.

Automatically detects Sales Navigator accounts from the Unipile workspace
and returns the optimal account for searching, separate from the user's
sending account.

Priority:
1. Cached premium search account from settings (re-detect every 7 days)
2. Auto-detected Sales Nav account from workspace (prefer non-sending)
3. Fallback: user's own active account
"""

from __future__ import annotations

import logging
import time
from typing import Any

from ..db.async_bridge import run_db
from ..db.queries import get_setting, save_setting

logger = logging.getLogger(__name__)

# Re-detect Sales Nav accounts every 7 days
_CACHE_TTL_SECONDS = 7 * 24 * 3600


async def resolve_search_account(
    client: Any,
    sending_account_id: str,
) -> tuple[str, bool]:
    """Resolve the best account for LinkedIn search.

    Checks for a cached premium search account, then auto-detects by
    scanning all workspace accounts for Sales Navigator access.

    Args:
        client: BackendClient or UnipileClient instance.
        sending_account_id: The user's active account used for sending.

    Returns:
        (search_account_id, has_sales_nav) tuple.
        search_account_id may equal sending_account_id if no premium found.
    """
    # 1. Check cache
    cached_id = await run_db(get_setting, "premium_search_account_id", "")
    cached_at = await run_db(get_setting, "premium_search_detected_at", 0)

    if cached_id and cached_at:
        age = time.time() - cached_at
        if age < _CACHE_TTL_SECONDS:
            logger.info(
                "Using cached premium search account %s (age: %dd)",
                cached_id[:8], int(age / 86400),
            )
            return cached_id, True

    # 2. Auto-detect: scan all accounts for Sales Navigator
    logger.info("Auto-detecting Sales Navigator accounts...")

    from ..linkedin.backend_client import BackendClient

    if isinstance(client, BackendClient):
        # Backend mode: use the dedicated endpoint that checks all pool accounts
        try:
            results = await client.check_sales_nav_all()
            sales_nav_accounts = [
                r for r in results if r.get("has_sales_navigator")
            ]
        except Exception as e:
            logger.warning("check_sales_nav_all failed: %s", e)
            sales_nav_accounts = []
    else:
        # Direct Unipile mode: iterate all accounts manually
        sales_nav_accounts = []
        try:
            accounts = await client.list_accounts()
            for acc in accounts:
                acc_id = acc.get("id") or acc.get("account_id") or ""
                if not acc_id:
                    continue
                provider = acc.get("provider") or acc.get("provider_type") or ""
                if "LINKEDIN" not in str(provider).upper():
                    continue
                try:
                    has_sn = await client.detect_sales_navigator(acc_id)
                    if has_sn:
                        sales_nav_accounts.append({
                            "account_id": acc_id,
                            "name": acc.get("name", ""),
                            "has_sales_navigator": True,
                        })
                except Exception:
                    continue
        except Exception as e:
            logger.warning("Failed to list accounts for Sales Nav detection: %s", e)

    if not sales_nav_accounts:
        logger.info("No Sales Navigator accounts found — using sending account")
        # Check if sending account itself has Sales Nav
        try:
            own_sn = await client.detect_sales_navigator(sending_account_id)
        except Exception:
            own_sn = False
        # Cache the negative result too (avoid re-scanning every campaign)
        await run_db(save_setting, "premium_search_account_id", "")
        await run_db(save_setting, "premium_search_detected_at", int(time.time()))
        return sending_account_id, own_sn

    # 3. Pick the best one: prefer non-sending account to avoid rate limit conflicts
    best = None
    for acc in sales_nav_accounts:
        aid = acc.get("account_id", "")
        if aid != sending_account_id:
            best = aid
            break

    # If all Sales Nav accounts are the sending account, use it
    if not best:
        best = sales_nav_accounts[0].get("account_id", sending_account_id)

    # 4. Cache result
    await run_db(save_setting, "premium_search_account_id", best)
    await run_db(save_setting, "premium_search_detected_at", int(time.time()))

    logger.info(
        "Premium search account resolved: %s (from %d Sales Nav accounts)",
        best[:8], len(sales_nav_accounts),
    )
    return best, True


def get_cached_search_account() -> str:
    """Return the cached premium search account ID, or empty string if none.

    Used by ICP enrichment to route LinkedIn code lookups through the
    premium account without re-running the full detection flow.
    """
    cached_id = get_setting("premium_search_account_id", "")
    cached_at = get_setting("premium_search_detected_at", 0)
    if cached_id and cached_at and (time.time() - cached_at < _CACHE_TTL_SECONDS):
        return cached_id
    return ""


def invalidate_search_account_cache() -> None:
    """Clear the cached premium search account (e.g., after auth failure)."""
    save_setting("premium_search_account_id", "")
    save_setting("premium_search_detected_at", 0)
    logger.info("Premium search account cache invalidated")
