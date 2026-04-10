"""Tool 1: setup_profile — Analyze your LinkedIn profile and generate a voice signature.

This is the #1 killer feature. Voice matching was the strongest positive
reaction in 7 of 12 customer discovery interviews. This is where users
think "OK, this AI actually gets me."

Supports two modes:

**Direct mode** (Unipile credentials in config):
  Call 1: setup_profile(llm_api_key="...") → auth link → user connects LinkedIn
  Call 2: setup_profile() → polls for account → profile fetch → voice analysis

**Backend mode** (backend_url + backend_jwt in config):
  Call 1: setup_profile(llm_api_key="...", backend_url="...", backend_jwt="...")
          → saves config → connects LinkedIn via backend proxy → profile + voice

If the account is already connected (re-run), skips straight to profile fetch.
"""

from __future__ import annotations

import logging

from ..ai.voice_analyzer import analyze_voice
from ..config import (
    get_backend_config,
    get_unipile_config,
    is_backend_mode,
    load_config,
    save_config,
    set_backend_config,
)
from ..constants import DEFAULT_BACKEND_URL, GEMINI_KEY_URL, LOGIN_URL_PATH
from ..db.queries import get_setting, save_setting
from ..formatter import format_voice_signature
from ..linkedin import (
    UnipileAuthError,
    UnipileError,
    get_account_id,
    get_linkedin_client,
)
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)


async def run_setup_profile(
    llm_api_key: str = "",
    llm_provider: str = "",
    backend_url: str = "",
    backend_jwt: str = "",
) -> str:
    """Set up the user's profile by analyzing their LinkedIn presence.

    Args:
        llm_api_key: API key for the LLM provider.
        llm_provider: Which LLM to use ("gemini", "claude", "openai").
        backend_url: HeyLead Backend API URL (enables backend mode).
        backend_jwt: JWT from Google OAuth (required for backend mode).

    Returns:
        Formatted string showing the voice analysis results or next-step instructions.
    """

    # ── Step 0: Save any provided credentials ──
    cfg = load_config()

    if llm_api_key:
        provider = llm_provider or "gemini"
        cfg.setdefault("api_keys", {})[provider] = llm_api_key
        save_config(cfg)

    if backend_url or backend_jwt:
        set_backend_config(
            backend_url or get_backend_config()[0],
            backend_jwt or get_backend_config()[1],
        )

    # ── Step 1: Check if we have any connection mode available ──
    # If neither backend JWT nor direct Unipile credentials exist, guide the user
    if not is_backend_mode():
        api_url, api_key = get_unipile_config()
        if not api_url or not api_key:
            login_url = f"{DEFAULT_BACKEND_URL}{LOGIN_URL_PATH}"
            return (
                "👋 Welcome to HeyLead! Let's get you set up (takes ~1 minute).\n\n"
                "**Step 1** — Sign in and connect LinkedIn:\n"
                f"  👉 {login_url}\n"
                "  Sign in with Google, click 'Connect LinkedIn Now', then copy your token.\n\n"
                "**Step 2** — Come back here and paste your token:\n"
                "  setup_profile(backend_jwt='YOUR_TOKEN')\n\n"
                "That's it! No API keys needed."
            )

    # ── Step 2: Check LLM key ──
    # In backend mode, LLM calls are proxied through the backend — no local key needed.
    # Only require a local key for direct mode (self-hosted Unipile).
    if not is_backend_mode():
        cfg = load_config()  # Reload in case we just saved
        has_llm_key = any(v for v in cfg.get("api_keys", {}).values() if v)
        if not has_llm_key:
            return (
                "❌ No LLM API key configured.\n\n"
                "Please provide an API key:\n"
                "  setup_profile(llm_api_key='YOUR_KEY', llm_provider='gemini')\n\n"
                f"Get a free Gemini key at: {GEMINI_KEY_URL}"
            )

    # ── Step 3: Route to appropriate mode ──
    if is_backend_mode():
        return await _setup_backend_mode()
    else:
        return await _setup_direct_mode()


async def _setup_backend_mode() -> str:
    """Setup flow via HeyLead Backend API proxy."""
    client = get_linkedin_client()
    try:
        stored_account_id = get_account_id()

        if stored_account_id:
            connected, status_msg = await client.verify_account(stored_account_id)
            if connected:
                return await _fetch_and_analyze(client, stored_account_id)
            else:
                logger.info(f"Stored account no longer connected: {status_msg}")
                await run_db(save_setting, "unipile_account_id", None)

        # ── Reconcile with backend ──
        # The webhook may have already bound an account on the backend
        # that we don't know about locally. Check before polling/auth-link.
        backend_account_id, _msg = await client.find_linkedin_account()
        if backend_account_id:
            connected, _status = await client.verify_account(backend_account_id)
            if connected:
                await run_db(save_setting, "unipile_account_id", backend_account_id)
                await run_db(save_setting, "auth_link_pending", False)
                await run_db(save_setting, "known_account_ids_before_auth", [])
                return await _fetch_and_analyze(client, backend_account_id)

        # Check if we're in "waiting for OAuth" state
        auth_link_pending = await run_db(get_setting, "auth_link_pending", False)

        if auth_link_pending:
            known_ids = set( await run_db(get_setting, "known_account_ids_before_auth", []))
            account_id, poll_msg = await client.poll_for_new_account(known_ids)

            if account_id:
                await run_db(save_setting, "unipile_account_id", account_id)
                await run_db(save_setting, "auth_link_pending", False)
                await run_db(save_setting, "known_account_ids_before_auth", [])
                return await _fetch_and_analyze(client, account_id)
            else:
                return (
                    f"⏳ {poll_msg}\n\n"
                    "Please make sure you:\n"
                    "1. Opened the auth link in your browser\n"
                    "2. Completed the LinkedIn login\n"
                    "3. Saw a success confirmation\n\n"
                    "Then run setup_profile() again to retry."
                )

        # Snapshot existing accounts, then create auth link via backend
        known_ids = await client.get_existing_account_ids()

        # Redirect user back to HeyLead after LinkedIn connects
        redirect_url = f"{DEFAULT_BACKEND_URL}/auth/linkedin-connected"

        try:
            auth_url = await client.create_hosted_auth_link(
                success_redirect_url=redirect_url,
            )
        except UnipileError as e:
            return f"❌ Failed to create LinkedIn auth link: {e}"

        await run_db(save_setting, "auth_link_pending", True)
        await run_db(save_setting, "known_account_ids_before_auth", list(known_ids))

        return (
            "🔗 Almost there! Open this link in your browser to connect LinkedIn:\n\n"
            f"  {auth_url}\n\n"
            "Steps:\n"
            "1. Click the link above (or copy-paste into your browser)\n"
            "2. Log in to LinkedIn when prompted\n"
            "3. Authorize the connection\n"
            "4. Come back here and run setup_profile() again\n\n"
            "⏱️ The link expires in 24 hours.\n"
            "🔒 Your credentials are handled securely by the HeyLead backend."
        )

    except UnipileError as e:
        return f"❌ Backend error: {e}"
    except Exception as e:
        logger.error(f"setup_profile (backend mode) failed: {e}", exc_info=True)
        return f"❌ Setup failed: {e}\n\nCheck ~/.heylead/logs/heylead.log for details."
    finally:
        await client.close()


async def _setup_direct_mode() -> str:
    """Setup flow with direct Unipile credentials (original behavior)."""
    from ..config import get_unipile_config
    from ..linkedin.unipile import UnipileClient

    api_url, api_key = get_unipile_config()

    if not api_url or not api_key:
        login_url = f"{DEFAULT_BACKEND_URL}{LOGIN_URL_PATH}"
        return (
            "No Unipile credentials found for direct mode.\n\n"
            "Recommended: Use backend mode instead (easier setup):\n"
            f"  1. Sign in at: {login_url}\n"
            "  2. Copy your token from the page\n"
            "  3. Run: setup_profile(backend_jwt='YOUR_TOKEN')\n\n"
            "Advanced: For self-hosted Unipile, add to ~/.heylead/config.json:\n"
            '  "unipile_api_url": "https://apiXX.unipile.com:XXXXX"\n'
            '  "unipile_api_key": "YOUR_UNIPILE_API_KEY"'
        )

    client = UnipileClient(api_url, api_key)
    try:
        stored_account_id = get_account_id()

        if stored_account_id:
            connected, status_msg = await client.verify_account(stored_account_id)
            if connected:
                return await _fetch_and_analyze(client, stored_account_id)
            else:
                logger.info(f"Stored account no longer connected: {status_msg}")
                await run_db(save_setting, "unipile_account_id", None)

        # Check if we're in "waiting for OAuth" state
        auth_link_pending = await run_db(get_setting, "auth_link_pending", False)

        if auth_link_pending:
            known_ids = set( await run_db(get_setting, "known_account_ids_before_auth", []))
            account_id, poll_msg = await client.poll_for_new_account(known_ids)

            if account_id:
                await run_db(save_setting, "unipile_account_id", account_id)
                await run_db(save_setting, "auth_link_pending", False)
                await run_db(save_setting, "known_account_ids_before_auth", [])
                return await _fetch_and_analyze(client, account_id)
            else:
                return (
                    f"⏳ {poll_msg}\n\n"
                    "Please make sure you:\n"
                    "1. Opened the auth link in your browser\n"
                    "2. Completed the LinkedIn login\n"
                    "3. Saw a success confirmation\n\n"
                    "Then run setup_profile() again to retry."
                )

        # Snapshot existing accounts, then create auth link
        known_ids = await client.get_existing_account_ids()

        # Redirect user back to HeyLead after LinkedIn connects
        redirect_url = f"{DEFAULT_BACKEND_URL}/auth/linkedin-connected"

        try:
            auth_url = await client.create_hosted_auth_link(
                success_redirect_url=redirect_url,
            )
        except UnipileError as e:
            return f"❌ Failed to create LinkedIn auth link: {e}"

        await run_db(save_setting, "auth_link_pending", True)
        await run_db(save_setting, "known_account_ids_before_auth", list(known_ids))

        return (
            "🔗 Almost there! Open this link in your browser to connect LinkedIn:\n\n"
            f"  {auth_url}\n\n"
            "Steps:\n"
            "1. Click the link above (or copy-paste into your browser)\n"
            "2. Log in to LinkedIn when prompted\n"
            "3. Authorize the connection\n"
            "4. Come back here and run setup_profile() again\n\n"
            "⏱️ The link expires in 24 hours.\n"
            "🔒 Your credentials are handled by Unipile — nothing stored locally."
        )

    except UnipileError as e:
        return f"❌ Unipile error: {e}"
    except Exception as e:
        logger.error(f"setup_profile failed: {e}", exc_info=True)
        return f"❌ Setup failed: {e}\n\nCheck ~/.heylead/logs/heylead.log for details."
    finally:
        await client.close()


async def _fetch_and_analyze(client, account_id: str) -> str:
    """Fetch profile, analyze voice, store results, return formatted output.

    Works with both UnipileClient and BackendClient.
    """

    # ── Fetch LinkedIn profile ──
    try:
        profile = await client.get_own_profile(account_id)
    except UnipileAuthError:
        await run_db(save_setting, "unipile_account_id", None)
        return (
            "❌ LinkedIn account disconnected.\n\n"
            "Run setup_profile() again to reconnect."
        )
    except Exception as e:
        logger.error(f"Failed to fetch LinkedIn profile: {e}")
        return (
            f"❌ Failed to fetch your LinkedIn profile: {e}\n\n"
            "This might be a temporary issue. Try again in a minute."
        )

    if not profile.get("name"):
        return (
            "❌ Could not read your LinkedIn profile.\n"
            "The connection might need to be refreshed. Run setup_profile() again."
        )

    # ── Fetch posts ──
    try:
        provider_id = profile.get("provider_id", "")
        posts = await client.get_posts(account_id, provider_id=provider_id)
        profile["posts"] = posts
    except Exception as e:
        logger.warning(f"Failed to fetch posts (non-fatal): {e}")
        profile["posts"] = []

    # ── Analyze voice with LLM ──
    try:
        analysis = await analyze_voice(profile)
    except Exception as e:
        logger.error(f"Voice analysis failed: {e}")
        return (
            f"❌ Voice analysis failed: {e}\n\n"
            "Check your LLM API key in ~/.heylead/config.json\n"
            "Get a free Gemini key at: https://aistudio.google.com/apikey"
        )

    voice = analysis.get("voice", {})
    expertise = analysis.get("expertise", {})

    # ── Store in database ──
    await run_db(save_setting, "profile", profile)
    await run_db(save_setting, "voice_signature", voice)
    await run_db(save_setting, "expertise_map", expertise)

    # ── Generate Hume AI voice config from voice signature ──
    try:
        from ..ai.hume_voice import create_voice_config
        hume_voice_config = create_voice_config(voice)
        await run_db(save_setting, "hume_voice_config", hume_voice_config)
        logger.info("Hume voice config generated and saved")
    except Exception as e:
        logger.warning("Hume voice config generation failed (non-fatal): %s", e)

    await run_db(save_setting, "setup_complete", True)

    # ── Auto-create company watchlist for user's own company page ──
    try:
        own_company_name = profile.get("company", "")
        own_company_url = ""
        experience = profile.get("experience", [])
        if experience and isinstance(experience, list):
            current = experience[0] if experience else {}
            own_company_url = current.get("company_url", "") or current.get("company_linkedin_url", "")
            if not own_company_name:
                own_company_name = current.get("company", "")

        if own_company_name:
            from ..db.signal_queries import list_watchlists, save_watchlist
            import re as _re
            company_identifier = ""
            if own_company_url:
                _match = _re.search(r"linkedin\.com/company/([^/?#]+)", own_company_url)
                company_identifier = _match.group(1) if _match else ""
            if not company_identifier:
                company_identifier = own_company_name

            existing_company_wl = [
                w for w in await run_db(list_watchlists, is_active=True)
                if w.get("watch_type") == "company"
                and company_identifier in (w.get("keywords_list") or [])
            ]
            if not existing_company_wl:
                await run_db(save_watchlist, name=f"{own_company_name} (Your Company)",
                    watch_type="company",
                    keywords=[company_identifier],)
                logger.info("Auto-created company watchlist for %s", own_company_name)
    except Exception as e:
        logger.debug("Auto company watchlist creation failed (non-fatal): %s", e)

    # ── Auto-create keyword watchlists from user expertise ──
    try:
        from ..db.signal_queries import list_watchlists as _list_wl, save_watchlist as _save_wl

        existing_kws: set[str] = set()
        for wl in await run_db(_list_wl, is_active=True):
            for kw in wl.get("keywords_list", []):
                existing_kws.add(kw.lower().strip())

        # Core expertise → keyword watchlist
        core_raw = expertise.get("core", "")
        if core_raw:
            core_topics = [t.strip() for t in core_raw.split(",") if t.strip()]
            new_core = [t for t in core_topics if t.lower() not in existing_kws]
            if new_core:
                await run_db(
                    _save_wl,
                    name="My Expertise — Core Topics",
                    watch_type="keyword",
                    keywords=new_core[:10],
                )
                existing_kws.update(t.lower() for t in new_core)
                logger.info("Auto-created core expertise watchlist: %d keywords", len(new_core))

        # Credible topics → keyword watchlist
        credible_raw = expertise.get("credible_topics", "")
        if credible_raw:
            credible_topics = [t.strip() for t in credible_raw.split(",") if t.strip()]
            new_credible = [t for t in credible_topics if t.lower() not in existing_kws]
            if new_credible:
                await run_db(
                    _save_wl,
                    name="My Expertise — Industry Topics",
                    watch_type="keyword",
                    keywords=new_credible[:10],
                )
                logger.info("Auto-created industry topics watchlist: %d keywords", len(new_credible))
    except Exception as e:
        logger.debug("Auto expertise watchlist creation failed (non-fatal): %s", e)

    # ── Auto-analyze brand & generate improvement plan ──
    brand_summary = ""
    try:
        from .brand_strategy import _handle_analyze, _handle_plan

        account_id_for_brand = await run_db(get_setting, "unipile_account_id", "")
        if account_id_for_brand:
            await _handle_analyze(account_id_for_brand, "")
            await _handle_plan(account_id_for_brand, "")

            from ..services.brand_service import load_brand_analysis

            ba = await run_db(load_brand_analysis)
            score = ba.get("overall_score", 0) if ba else 0
            brand_summary = (
                f"\n\n Brand Audit: {score}/100\n"
                "A 4-week improvement plan has been auto-generated and will execute automatically.\n"
                "Run brand_strategy(action='progress') anytime to check progress."
            )
            logger.info("Auto brand analysis complete: score=%d", score)
    except Exception as e:
        logger.warning("Auto brand analysis failed (non-fatal): %s", e)

    # ── Detect Sales Navigator license ──
    has_sales_nav = False
    try:
        has_sales_nav = await client.detect_sales_navigator(account_id)
        await run_db(save_setting, "has_sales_navigator", has_sales_nav)
        if has_sales_nav:
            logger.info("Sales Navigator detected on this account")
    except Exception as e:
        await run_db(save_setting, "has_sales_navigator", False)
        logger.debug("Sales Nav detection skipped: %s", e)

    # ── Auto-register webhook for real-time events ──
    try:
        from ..config import is_backend_mode
        from ..constants import DEFAULT_BACKEND_URL
        if is_backend_mode():
            webhook_url = f"{DEFAULT_BACKEND_URL}/webhooks/unipile-webhook"
            result = await client.register_webhook(
                account_id,
                webhook_url,
                events=["new_message", "new_relation", "account_disconnected", "message_seen"],
            )
            if result.get("success"):
                logger.info("Auto-registered webhook for real-time events")
            else:
                logger.debug("Webhook registration skipped: %s", result.get("error", ""))
    except Exception as e:
        logger.debug("Webhook auto-registration failed (non-critical): %s", e)

    # ── Sync email_account_id from backend ──
    email_status = ""
    try:
        from ..config import is_backend_mode
        if is_backend_mode() and hasattr(client, "get_user_info"):
            user_info = await client.get_user_info()
            email_acct = user_info.get("email_account_id", "")
            if email_acct:
                await run_db(save_setting, "email_account_id", email_acct)
                email_status = "\n📧 Email account connected — email fallback enabled."
                logger.info("Synced email_account_id from backend: %s", email_acct[:8])
    except Exception as e:
        logger.debug("Email account sync skipped: %s", e)

    # ── Format and return ──
    output = format_voice_signature(voice, expertise)

    header = (
        f"👤 {profile['name']}"
        + (f" — {profile['title']}" if profile.get("title") else "")
        + (f" at {profile['company']}" if profile.get("company") else "")
        + "\n"
        + (f"📍 {profile['location']}\n" if profile.get("location") else "")
        + (f"🔗 {profile['profile_url']}\n" if profile.get("profile_url") else "")
        + f"📝 {len(profile.get('posts', []))} recent posts analyzed\n"
        + "\n"
    )

    serper_hint = (
        "\n💡 Optional: Add a SERPER API key for news-enhanced messages:\n"
        "   Add \"serper\" to api_keys in ~/.heylead/config.json\n"
        "   Get a free key at: https://serper.dev"
    )

    website_hint = (
        "\n💡 **Tip:** Set up website tracking with `signals(action='website_setup')` "
        "to detect when target companies visit your site."
    )

    next_hint = (
        "\n\n**Next:** create_campaign(...) → generate_and_send → check_replies."
    )

    return header + output + email_status + brand_summary + serper_hint + website_hint + next_hint
