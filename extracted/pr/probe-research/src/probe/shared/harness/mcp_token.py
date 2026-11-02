"""the read token this device holds and the API its stored credentials belong to, which every McpSlot syncs against."""

from __future__ import annotations


def current_mcp_token() -> str | None:
    """The read token this device holds, or None."""
    from probe.sdk.settings.settings import load_context

    try:
        return (load_context() or {}).get("mcp_token") or None
    except Exception:  # noqa: BLE001 - an unreadable config is "no token", not a crash
        return None


def _context_base_url() -> str:
    """The API this device's stored credentials belong to.

    Read from the SAME context as `mcp_token`, which is what makes it the right
    thing to compare the Codex endpoint against: the two values were written by
    one `save_context` call and describe one account.
    """
    from probe.sdk.settings.settings import DEFAULT_BASE_URL, load_context

    try:
        return str((load_context() or {}).get("base_url") or DEFAULT_BASE_URL)
    except Exception:  # noqa: BLE001 - an unreadable config is "the default"
        return DEFAULT_BASE_URL
