"""
nx_mcp_manager.py — NX MCP control-plane client.

The CLI no longer spawns local mcp-hub processes. It talks to the NX control
plane API, which manages a single hub subprocess remotely.
"""

from __future__ import annotations

import os
import random
import time
from typing import Optional
from urllib.parse import quote

import httpx
from nx_obfuscate import HUB


def _retry(fn, attempts: int = 3, base_delay: float = 0.3):
    """Audit-N: retry-with-backoff for the MCP control-plane HTTP calls.
    Retries on connection errors, timeouts, 5xx, and 429. Returns the last
    response or raises the last exception."""
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
            time.sleep(base_delay * (2 ** i) * (1.0 + (random.random() - 0.5) * 0.5))
    if last_exc:
        raise last_exc
    return None

NX_CONTROL_PLANE = os.environ.get("NX_MCP_HUB_URL", HUB["default"]).rstrip("/")
REGISTRY_URL = HUB["registry"]


def _user_path(user_id: str) -> str:
    return quote(str(user_id), safe="")


def _control_url(path: str) -> str:
    return f"{NX_CONTROL_PLANE}{path}"


def start_user_hub(user_id: str, servers: Optional[dict] = None) -> dict:
    """
    Ensure the remote control plane is reachable.

    `servers` is accepted for backward compatibility with earlier local-hub
    call sites but is no longer used by the client.
    """
    _ = servers
    try:
        response = _retry(lambda: httpx.get(_control_url(HUB["health"]), timeout=10))
        if response.status_code != 200:
            return {
                "status": "unavailable",
                "user_id": user_id,
                "error": f"control plane returned {response.status_code}",
            }
        payload = response.json()
        return {
            "status": "ready",
            "user_id": user_id,
            "hub_alive": bool(payload.get("hub_alive")),
            "hub_port": payload.get("hub_port"),
            "control_plane": NX_CONTROL_PLANE,
        }
    except Exception as exc:
        return {
            "status": "unavailable",
            "user_id": user_id,
            "error": str(exc),
            "control_plane": NX_CONTROL_PLANE,
        }


def stop_user_hub(user_id: str) -> dict:
    """
    Disconnect every server registered for the user from the remote hub.
    Distinguishes a real "no servers" state from "control plane unreachable".
    """
    try:
        ping = _retry(lambda: httpx.get(_control_url(HUB.get("health", "/health")), timeout=10))
        if ping.status_code >= 500:
            return {
                "status": "unavailable",
                "user_id": user_id,
                "removed": [],
                "error": f"control plane returned {ping.status_code}",
            }
    except Exception as exc:
        return {
            "status": "unavailable",
            "user_id": user_id,
            "removed": [],
            "error": f"control plane unreachable: {exc}",
        }

    servers = get_user_servers(user_id)
    removed = []
    for server in servers:
        name = server.get("name")
        if not name:
            continue
        try:
            response = _retry(lambda: httpx.post(
                _control_url(HUB["disconnect"]),
                json={"user_id": user_id, "server_name": name},
                timeout=30,
            ))
            payload = response.json()
        except Exception as exc:
            return {
                "status": "failed",
                "user_id": user_id,
                "removed": removed,
                "error": str(exc),
            }
        if payload.get("success"):
            removed.append(name)
    return {"status": "stopped", "user_id": user_id, "removed": removed}


def get_user_port(user_id: str) -> Optional[int]:
    """
    Compatibility shim for older callers that expected a local hub port.
    """
    _ = user_id
    return None


def add_server_for_user(
    user_id: str,
    server_name: str,
    command: str,
    args: list[str],
    env: Optional[dict] = None,
) -> dict:
    """
    Register a user-scoped MCP server through the control plane.
    """
    try:
        response = _retry(lambda: httpx.post(
            _control_url(HUB["connect"]),
            json={
                "user_id": user_id,
                "server_name": server_name,
                "command": command,
                "args": args,
                "env": dict(env or {}),
            },
            timeout=60,
        ))
        return response.json()
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def get_user_tools(user_id: str) -> list[dict]:
    """
    Read tool metadata from the control plane's user-scoped tools endpoint.
    """
    try:
        response = _retry(lambda: httpx.get(
            f"{_control_url(HUB['user_api'])}{_user_path(user_id)}{HUB['tools_suffix']}",
            timeout=10,
        ))
        if response.status_code == 200:
            return response.json().get("tools", [])
    except Exception:
        pass
    return []


def get_user_servers(user_id: str) -> list[dict]:
    """
    Read user-scoped server status from the control plane.
    """
    try:
        response = _retry(lambda: httpx.get(
            f"{_control_url(HUB['user_api'])}{_user_path(user_id)}{HUB['servers_suffix']}",
            timeout=10,
        ))
        if response.status_code == 200:
            return response.json().get("servers", [])
    except Exception:
        pass
    return []


def list_active_sessions() -> list[dict]:
    """
    Surface the control plane's current server view in a session-like shape.
    """
    try:
        response = _retry(lambda: httpx.get(_control_url(HUB["servers_api"]), timeout=10))
        if response.status_code != 200:
            return []
        active = []
        for server in response.json().get("servers", []):
            name = server.get("name", "")
            user_id, _, server_name = name.partition("__")
            active.append(
                {
                    "user_id": user_id or None,
                    "server": server_name or name,
                    "alive": server.get("status") == "connected",
                    "status": server.get("status"),
                }
            )
        return active
    except Exception:
        return []


def cleanup_dead_sessions() -> int:
    """
    Session cleanup is owned by the remote control plane.
    """
    return 0


def search_marketplace(query: str, limit: int = 10) -> list[dict]:
    """
    Search the validated mcp-hub marketplace registry.
    """
    try:
        response = _retry(lambda: httpx.get(REGISTRY_URL, timeout=10))
        if response.status_code != 200:
            return []
        servers = response.json().get("servers", [])
        query_lower = query.lower()
        matches = [
            server
            for server in servers
            if query_lower in server.get("name", "").lower()
            or query_lower in server.get("description", "").lower()
            or any(query_lower in tag.lower() for tag in server.get("tags", []))
        ]
        return matches[:limit]
    except Exception:
        return []
