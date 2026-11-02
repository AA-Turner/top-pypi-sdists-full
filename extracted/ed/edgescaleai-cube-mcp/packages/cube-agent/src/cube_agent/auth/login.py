"""Login flow for cube-agent — saves API key locally."""

from __future__ import annotations

import asyncio
import logging
import secrets
import ssl
import webbrowser

import httpx
import truststore

from cube_agent.auth.keystore import save_key, delete_key, has_key
from cube_agent.config import get_cloud_url

logger = logging.getLogger(__name__)


def _is_ssl_cert_error(exc: Exception) -> bool:
    """Return True if exc or its direct cause is an SSL certificate verification error."""
    cause = exc.__cause__ or exc.__context__
    return isinstance(exc, ssl.SSLCertVerificationError) or isinstance(cause, ssl.SSLCertVerificationError)


async def login_browser() -> str:
    """Browser-based login: open sign-in page, poll for API key.

    1. Generate a random session_id
    2. Open browser to {cloud_url}/auth/login?session_id={session_id}
    3. Poll {cloud_url}/auth/session/{session_id} with exponential backoff
       (0.5s → 2s, up to 2 minutes total)
    4. On success: save the API key locally
    """
    cloud_url = get_cloud_url().rstrip("/")
    session_id = secrets.token_urlsafe(32)

    login_url = f"{cloud_url}/auth/login?session_id={session_id}"
    poll_url = f"{cloud_url}/auth/session/{session_id}"

    # Open the browser
    webbrowser.open(login_url)

    # Delegate TLS verification to the OS trust store (macOS Keychain, Windows
    # CryptoAPI, Linux OpenSSL paths) so corporate/firewall CAs are trusted
    # without manual cert-bundle patching.
    ssl_ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    # Poll for the API key with exponential backoff:
    # Start at 0.5s, increase to max 2s — keeps response snappy while
    # avoiding excessive requests during the longer password-entry phase.
    async with httpx.AsyncClient(verify=ssl_ctx) as client:
        poll_interval = 0.5
        elapsed = 0.0
        max_wait = 120.0  # 2 minutes
        last_error: Exception | None = None

        while elapsed < max_wait:
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval
            try:
                resp = await client.get(poll_url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("status") == "ready":
                        api_key = data["api_key"]
                        save_key(api_key)
                        return "Login successful! API key saved."
            except Exception as e:
                if _is_ssl_cert_error(e):
                    # Cert errors won't clear up with retries — fail fast so
                    # the user sees the real cause instead of a 2-minute hang.
                    logger.error("TLS certificate verification failed: %s", e)
                    return (
                        "Login failed: TLS certificate verification error. "
                        "Your network may use a TLS-inspecting proxy whose CA is not "
                        "in your OS trust store. Install the proxy CA into your system "
                        "trust store and try again, or set CUBE_API_KEY with a pre-issued key."
                    )
                last_error = e
                logger.debug("Poll error (will retry): %s", e)

            # Ramp up: 0.5 → 0.75 → 1.0 → 1.25 → … → 2.0 (cap)
            poll_interval = min(poll_interval + 0.25, 2.0)

    if last_error is not None:
        logger.warning("Login timed out after poll errors. Last error: %s", last_error)
    return "Login timed out. Try again, or set the CUBE_API_KEY environment variable with a pre-issued key."


def logout() -> str:
    """Remove the stored API key."""
    if delete_key():
        return "API key removed."
    return "No API key was stored."


def status() -> str:
    """Check authentication status."""
    if has_key():
        return "Authenticated (API key stored)."
    return "Not authenticated. Run cube-agent login <api-key> to configure."
