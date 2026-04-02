"""Tool: unlink_account — Disconnect LinkedIn from HeyLead.

In backend mode: calls backend DELETE /accounts/unlink and clears local account_id.
In direct mode: clears local account_id only (no Unipile API to unlink).
User can reconnect later via setup_profile.
"""

from __future__ import annotations

import logging

from ..config import is_backend_mode
from ..db.queries import delete_setting
from ..linkedin import get_account_id, get_linkedin_client
from ..linkedin.backend_client import BackendClient
from ..db.async_bridge import run_db

logger = logging.getLogger(__name__)


async def run_unlink_account() -> str:
    """Disconnect the current LinkedIn account from HeyLead.

    Backend mode: unlinks on the server and clears local account_id.
    Direct mode: clears local account_id only.
    """
    account_id = get_account_id()
    if not account_id:
        return (
            "No LinkedIn account is connected.\n\n"
            "Run setup_profile() to connect an account."
        )

    if is_backend_mode():
        try:
            client = get_linkedin_client()
            if isinstance(client, BackendClient):
                await client.unlink_account()
        except Exception as e:
            logger.warning(f"Backend unlink failed (clearing local anyway): {e}")
            # Still clear local so user isn't stuck

    await run_db(delete_setting, "unipile_account_id")
    logger.info("Unlinked LinkedIn account (local account_id cleared)")

    return (
        "✅ LinkedIn account disconnected.\n\n"
        "Your campaigns and data are still in HeyLead. "
        "To connect again (same or different LinkedIn), run setup_profile()."
    )
