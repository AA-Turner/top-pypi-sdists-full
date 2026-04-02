"""Tool 1b: switch_account — List connected LinkedIn accounts and switch between them.

Fetches all LinkedIn accounts from Unipile, shows them with profile info
(name, headline, LinkedIn URL), and lets the user pick which one to use.
Then re-runs profile fetch + voice analysis for the selected account.
"""

from __future__ import annotations

import logging

from ..ai.voice_analyzer import analyze_voice
from ..config import is_backend_mode
from ..db.queries import get_setting, save_setting
from ..formatter import format_voice_signature
from ..linkedin import UnipileError, get_account_id, get_linkedin_client
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)


def _extract_linkedin_url(acc: dict) -> str:
    """Extract LinkedIn profile URL from an account's connection_params.

    Unipile stores the public identifier in connection_params.im.publicIdentifier.
    This is the user's real LinkedIn vanity slug (e.g., 'johndoe').
    """
    cp = acc.get("connection_params") or {}
    im = cp.get("im") or {}
    pub_id = im.get("publicIdentifier") or im.get("public_identifier") or ""
    if pub_id:
        return f"https://www.linkedin.com/in/{pub_id}"
    return ""


def _parse_linkedin_accounts(accounts: list[dict]) -> list[dict]:
    """Filter and normalize account list to LinkedIn accounts with profile URLs."""
    linkedin_accounts = []
    for acc in accounts:
        provider = (
            acc.get("provider")
            or acc.get("provider_type")
            or acc.get("type")
            or ""
        )
        if "LINKEDIN" not in str(provider).upper():
            continue
        acc_id = (
            acc.get("id")
            or acc.get("account_id")
            or acc.get("accountId")
            or acc.get("uuid")
        )
        if not acc_id:
            continue
        linkedin_accounts.append(
            {
                "id": str(acc_id),
                "name": acc.get("name") or "",
                "linkedin_url": _extract_linkedin_url(acc),
            }
        )
    return linkedin_accounts


async def run_switch_account() -> str:
    """List all LinkedIn accounts and let the user pick one."""
    if not is_backend_mode():
        from ..config import get_unipile_config

        api_url, api_key = get_unipile_config()
        if not api_url or not api_key:
            return "❌ Not connected. Run setup_profile first."

    client = get_linkedin_client()
    try:
        accounts = await client.list_accounts()
        linkedin_accounts = _parse_linkedin_accounts(accounts)

        if not linkedin_accounts:
            return (
                "❌ No LinkedIn accounts found.\n\n"
                "Run setup_profile() to connect your LinkedIn account."
            )

        current_id = get_account_id()

        lines = ["**Connected LinkedIn accounts:**\n"]
        for i, acc in enumerate(linkedin_accounts, 1):
            marker = " ← current" if acc["id"] == current_id else ""
            display = acc["name"] or acc["id"]
            lines.append(f"{i}. `{acc['id']}` — {display}{marker}")
            if acc["linkedin_url"]:
                lines.append(f"   🔗 {acc['linkedin_url']}")

        lines.append("")
        lines.append(
            "To switch, tell me which account number you want to use "
            "and I'll call `switch_account_to(account_id='...')`."
        )

        return "\n".join(lines)

    except Exception as e:
        logger.error(f"switch_account failed: {e}", exc_info=True)
        return f"❌ Failed to list accounts: {e}"
    finally:
        await client.close()


async def run_list_linkedin_accounts() -> str:
    """List connected LinkedIn accounts with LinkedIn profile URLs and Sales Nav badge.

    Extracts the public identifier directly from the account data
    (connection_params.im.publicIdentifier) — no extra API calls needed.
    Also shows which account is used for premium search.
    """
    if not is_backend_mode():
        from ..config import get_unipile_config

        api_url, api_key = get_unipile_config()
        if not api_url or not api_key:
            return "❌ Not connected. Run setup_profile first."

    client = get_linkedin_client()
    try:
        accounts = await client.list_accounts()
        linkedin_accounts = _parse_linkedin_accounts(accounts)

        if not linkedin_accounts:
            return (
                "No LinkedIn accounts connected.\n\n"
                "Run setup_profile() to connect your LinkedIn account."
            )

        current_id = get_account_id()

        # Check for cached premium search account
        from ..services.search_account_resolver import get_cached_search_account
        search_acct = await run_db(get_cached_search_account)

        # Try to get Sales Nav status for all accounts
        from ..linkedin.backend_client import BackendClient
        sales_nav_map: dict[str, bool] = {}
        if isinstance(client, BackendClient):
            try:
                sn_results = await client.check_sales_nav_all()
                for r in sn_results:
                    sales_nav_map[r.get("account_id", "")] = r.get("has_sales_navigator", False)
            except Exception:
                pass  # Non-critical, skip badge

        # Check connectivity status for each account
        connectivity_map: dict[str, tuple[bool, str]] = {}
        for acc in linkedin_accounts:
            try:
                connected, msg = await client.verify_account(acc["id"])
                connectivity_map[acc["id"]] = (connected, msg)
            except Exception:
                connectivity_map[acc["id"]] = (True, "")  # Assume OK on error

        lines = ["**Connected LinkedIn accounts:**\n"]
        for i, acc in enumerate(linkedin_accounts, 1):
            markers = []
            if acc["id"] == current_id:
                markers.append("current")
            if search_acct and acc["id"] == search_acct and search_acct != current_id:
                markers.append("search")
            if sales_nav_map.get(acc["id"]):
                markers.append("Sales Nav")

            # Connectivity badge
            is_connected, conn_msg = connectivity_map.get(acc["id"], (True, ""))
            if not is_connected:
                markers.append("Disconnected")

            marker_str = f" ← {', '.join(markers)}" if markers else ""

            display = acc["name"] or acc["id"]
            lines.append(f"{i}. `{acc['id']}` — {display}{marker_str}")
            if not is_connected:
                lines.append(f"   ⚠️ {conn_msg}")
            if acc["linkedin_url"]:
                lines.append(f"   LinkedIn: {acc['linkedin_url']}")

        lines.append("")
        lines.append("Use switch_account_to(account_id='...') to switch.")
        lines.append("Use set_search_account(account_id='...') to pin a premium search account.")
        return "\n".join(lines)
    except Exception as e:
        logger.error(f"list_linkedin_accounts failed: {e}", exc_info=True)
        return f"❌ Failed to list accounts: {e}"
    finally:
        await client.close()


async def run_switch_account_to(account_id: str) -> str:
    """Switch to a specific LinkedIn account, re-fetch profile, re-analyze voice."""
    if not account_id or not account_id.strip():
        return "❌ Please provide an account_id."

    try:
        client = get_linkedin_client()
    except UnipileError as e:
        return f"❌ Not connected. {e}\n\nRun setup_profile first."
    try:
        # Verify the account exists and is connected
        connected, status_msg = await client.verify_account(account_id)
        if not connected:
            return f"❌ Account `{account_id}` is not connected: {status_msg}"

        # Store the new account ID
        await run_db(save_setting, "unipile_account_id", account_id)
        from ..linkedin.unipile import invalidate_account_id_cache
        invalidate_account_id_cache()

        # Bind on backend too (if backend mode)
        if is_backend_mode():
            try:
                await client.bind_account(account_id)
            except Exception:
                pass  # 409 = already bound, which is fine

        # Fetch profile
        try:
            profile = await client.get_own_profile(account_id)
        except Exception as e:
            await run_db(save_setting, "unipile_account_id", account_id)  # keep it stored anyway
            return (
                f"✅ Switched to account `{account_id}` but couldn't fetch profile: {e}\n"
                "Run setup_profile() to retry."
            )

        if not profile.get("name"):
            return (
                f"✅ Switched to account `{account_id}` but profile is empty.\n"
                "The connection might need time to sync. Try setup_profile() in a minute."
            )

        # Fetch posts
        try:
            provider_id = profile.get("provider_id", "")
            posts = await client.get_posts(account_id, provider_id=provider_id)
            profile["posts"] = posts
        except Exception:
            profile["posts"] = []

        # Re-analyze voice
        try:
            analysis = await analyze_voice(profile)
        except Exception as e:
            # Store profile even if voice analysis fails
            await run_db(save_setting, "profile", profile)
            return (
                f"✅ Switched to account `{account_id}` — {profile['name']}\n"
                f"⚠️ Voice analysis failed: {e}\n"
                "Run setup_profile() to retry."
            )

        voice = analysis.get("voice", {})
        expertise = analysis.get("expertise", {})

        # Store everything
        await run_db(save_setting, "profile", profile)
        await run_db(save_setting, "voice_signature", voice)
        await run_db(save_setting, "expertise_map", expertise)
        await run_db(save_setting, "setup_complete", True)

        # Format output
        output = format_voice_signature(voice, expertise)

        header = (
            f"✅ Switched to: **{profile['name']}**"
            + (f" — {profile['title']}" if profile.get("title") else "")
            + (f" at {profile['company']}" if profile.get("company") else "")
            + "\n"
            + (f"🔗 {profile['profile_url']}\n" if profile.get("profile_url") else "")
            + f"📝 {len(profile.get('posts', []))} recent posts analyzed\n"
            + "\n"
        )

        return header + output

    except Exception as e:
        logger.error(f"switch_account_to failed: {e}", exc_info=True)
        return f"❌ Switch failed: {e}"
    finally:
        await client.close()
