"""
nx_autoconnect.py — Zero-friction integration connection.
User says "connect shopify" or just "shopify" in context.
NX installs, authenticates, connects automatically.
No /integrations menu needed.
"""

import os
import getpass
import webbrowser
from typing import Optional

import httpx

from nx_obfuscate import HUB

GOLD  = "\033[38;2;200;164;74m"
GREEN = "\033[38;2;80;200;100m"
RED   = "\033[38;2;220;80;70m"
DIM   = "\033[38;2;146;140;122m"
RESET = "\033[0m"


# Natural language triggers for each integration. ONLY high-signal phrases —
# short stems like "pr" or generic words like "code" / "db" caused false-positive
# autoconnect prompts on ordinary speech (e.g. "pretend" matched "pr").
INTEGRATION_TRIGGERS = {
    "shopify":       ["shopify", "my store", "my shopify"],
    "github":        ["github", "my repo", "pull request", "my repository", "open a pr"],
    "notion":        ["notion", "my notion"],
    "hubspot":       ["hubspot"],
    "slack":         ["slack", "my slack", "in slack"],
    "stripe":        ["stripe", "my stripe"],
    "google-drive":  ["google drive", "gdocs", "google docs"],
    "salesforce":    ["salesforce"],
    "linear":        ["linear", "my linear"],
    "jira":          ["jira", "my jira"],
    "supabase":      ["supabase", "my supabase"],
    "quickbooks":    ["quickbooks"],
}


import re as _re_ac

def detect_needed_integrations(user_message: str) -> list[str]:
    """Detect which integrations a user message *clearly* needs.

    Uses word-boundary matching so short stems don't trigger on substrings
    of unrelated words. The triggers above are intentionally narrow — false
    positives interrupt the user with token prompts on ordinary speech.
    """
    msg = (user_message or "").lower()
    needed = []
    for integration, triggers in INTEGRATION_TRIGGERS.items():
        for t in triggers:
            # Multi-word phrases match literally; single tokens require word boundaries.
            if " " in t:
                if t in msg:
                    needed.append(integration)
                    break
            else:
                if _re_ac.search(rf"(?<![A-Za-z0-9_]){_re_ac.escape(t)}(?![A-Za-z0-9_])", msg):
                    needed.append(integration)
                    break
    return needed


def _retry(fn, attempts: int = 3, base_delay: float = 0.3):
    """Audit-N: retry-with-backoff for autoconnect's HTTP calls."""
    import random as _rand, time as _t
    last_exc = None
    for i in range(max(1, attempts)):
        try:
            resp = fn()
            code = getattr(resp, "status_code", None)
            if code is None or (code < 500 and code != 429):
                return resp
            last_exc = RuntimeError(f"HTTP {code}")
        except Exception as exc:
            last_exc = exc
        if i + 1 < attempts:
            _t.sleep(base_delay * (2 ** i) * (1.0 + (_rand.random() - 0.5) * 0.5))
    if last_exc:
        raise last_exc
    return None


def get_connected_integrations(user_id: str) -> list[str]:
    """Already-connected integrations — across BOTH connection systems:
      - the new MCP OAuth sign-ins (Notion, Linear, GoHighLevel, … — a Keychain
        token), and
      - the old hub servers (npx).
    Unified at the ROOT so no path (auto-connect, /connected, autoconnect's own
    check) ever treats an MCP-signed-in service as "not connected" and tries to
    re-set it up. Names are returned in BOTH slug and display form so any caller's
    membership test matches."""
    out = []
    # MCP OAuth sign-ins — the serverless connects
    try:
        import nx_mcp_oauth as _mcpo
        for slug in _mcpo.all_servers():
            if _mcpo.is_connected(slug):
                out.append(slug)
                name = (_mcpo.get_server(slug) or {}).get("name", "")
                if name:
                    out.append(name)
    except Exception:
        pass
    # old hub servers
    try:
        hub_url = os.environ.get("NX_MCP_HUB_URL", HUB["default"])
        r = _retry(lambda: httpx.get(
            f"{hub_url}/api/user/{user_id}/servers",
            timeout=5,
        ))
        if r.status_code == 200:
            servers = r.json().get("servers", [])
            out.extend(s["name"] for s in servers if s.get("status") == "connected")
    except Exception:
        pass
    return out


def autoconnect(
    integration: str,
    user_id: str,
    canvas=None,
) -> dict:
    """
    Auto-connect an integration.
    Shows progress on canvas.
    Prompts for credentials only when needed.
    """
    from nx_mcp import MCP_REGISTRY

    mcp = MCP_REGISTRY.get(integration)
    if not mcp:
        return {"error": f"Unknown integration: {integration}"}

    if canvas:
        canvas.step(f"Connecting {integration}...", "working")

    auth_type = mcp.get("auth", "api_key")
    env_key   = mcp.get("env_key")

    # Check if already connected (case-insensitive, across both systems)
    connected = get_connected_integrations(user_id)
    if integration.strip().lower() in {c.strip().lower() for c in connected}:
        if canvas:
            canvas.complete_step(f"Connecting {integration}...", "done")
        return {"success": True, "already_connected": True}

    # Get credentials
    token = ""
    if auth_type == "none" or not env_key:
        token = "none"

    elif auth_type == "oauth":
        # Open OAuth URL
        oauth_urls = {
            "shopify":      "https://partners.shopify.com/",
            "slack":        "https://api.slack.com/apps",
            "salesforce":   "https://login.salesforce.com",
            "google-drive": "https://console.cloud.google.com/apis/credentials",
            "hubspot":      "https://app.hubspot.com/oauth/authorize",
        }
        url = oauth_urls.get(integration)
        if not url:
            # Never fabricate https://{integration}.com/settings/api (dead domain).
            print(f"\n  {GOLD}✦ {integration}{RESET}")
            print(f"  {DIM}Connect it with /integrations {integration} — the real login.{RESET}")
            return {"ok": False, "detail": "no_verified_oauth_url", "integration": integration}
        print(f"\n  {GOLD}✦ {integration} requires OAuth authorization{RESET}")
        print(f"  {DIM}Opening browser...{RESET}")
        webbrowser.open(url)
        print(f"  {DIM}After authorizing, paste your access token:{RESET}")

        try:
            token = getpass.getpass(f"  {GOLD}{env_key} › {RESET}")
        except (KeyboardInterrupt, EOFError):
            return {"error": "cancelled"}

    else:
        # API key
        print(f"\n  {GOLD}✦ Connect {integration}{RESET}")
        print(f"  {DIM}{mcp.get('description', '')}{RESET}")

        try:
            token = getpass.getpass(
                f"  {GOLD}{env_key} › {RESET}"
            )
        except (KeyboardInterrupt, EOFError):
            return {"error": "cancelled"}

    if not token:
        return {"error": "No credentials provided"}

    # Connect via hub
    try:
        hub_url = os.environ.get("NX_MCP_HUB_URL", HUB["default"])
        # Use shlex so quoted args (e.g. `--label "thing two"`) survive intact.
        import shlex
        try:
            install_parts = shlex.split(mcp.get("install", "") or "")
        except ValueError:
            install_parts = (mcp.get("install", "") or "").split()
        args = install_parts[2:] if len(install_parts) > 2 else install_parts
        r = _retry(lambda: httpx.post(
            f"{hub_url}/api/connect",
            json={
                "user_id": user_id,
                "server_name": integration,
                "command": install_parts[0] if install_parts else "npx",
                "args": ["-y"] + args,
                "env": {env_key: token} if env_key and token != "none" else {},
            },
            timeout=60,
        ))
        result = r.json()
        if result.get("success"):
            tools = result.get("tools_count", 0)
            if canvas:
                canvas.complete_step(f"Connecting {integration}...", "done")
            print(f"\n  {GREEN}✦ {integration} connected — {tools} tools ready{RESET}\n")
            return {"success": True, "tools": tools}
        else:
            return {"error": result.get("error", "Connection failed")}
    except Exception as e:
        return {"error": str(e)}


def maybe_autoconnect(user_message: str, user_id: str, canvas=None) -> list[dict]:
    """
    High-level helper: detect needed integrations and connect missing ones.
    Returns a list of result dicts.
    """
    needed = detect_needed_integrations(user_message)
    if not needed:
        return []

    connected = get_connected_integrations(user_id)
    connected_low = {c.lower() for c in connected}
    # Also treat servers connected via the new MCP OAuth sign-in (Keychain token)
    # as connected — otherwise we'd try to re-set-up an already-connected service
    # the OLD way (e.g. prompt for NOTION_API_KEY when Notion is signed in).
    try:
        import nx_mcp_oauth as _mcpo
    except Exception:
        _mcpo = None

    def _already(n):
        nl = n.strip().lower()
        if n in connected or nl in connected_low:
            return True
        if _mcpo:
            for cand in (nl, n):
                try:
                    if _mcpo.is_connected(cand):
                        return True
                except Exception:
                    pass
        return False

    missing = [n for n in needed if not _already(n)]

    results = []
    for integration in missing:
        print(f"\n  {GOLD}✦ {integration} not connected — setting it up{RESET}")
        result = autoconnect(integration, user_id, canvas=canvas)
        results.append({"integration": integration, **result})
        if not result.get("success"):
            print(f"  {RED}· Could not connect {integration}: {result.get('error')}{RESET}")

    return results
