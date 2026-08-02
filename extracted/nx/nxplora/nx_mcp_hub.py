"""
nx_mcp_hub.py - NX MCP Hub (corrected from validation).

Real package: mcp-hub (not mcphub)
Real health: /api/servers (not /health)
Real tools: /api/servers -> servers[].capabilities.tools[]
Registry: ravitemer.github.io/mcp-registry/registry.json (not TensorBlock)
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Optional

import httpx
from nx_obfuscate import HUB

NX_HUB_URL = os.environ.get("NX_MCP_HUB_URL", HUB["default"])
NX_HUB_CONFIG = Path.home() / ".nx" / "mcp_hub_config.json"
MCP_REGISTRY_URL = HUB["registry"]
_registry_cache: list[dict] = []


def _load_registry() -> list[dict]:
    """Load the real mcp-hub marketplace registry."""
    global _registry_cache
    if _registry_cache:
        return _registry_cache
    try:
        response = httpx.get(MCP_REGISTRY_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            _registry_cache = data if isinstance(data, list) else data.get("servers", [])
            return _registry_cache
    except Exception:
        pass
    return []


def _hub_url(path: str) -> str:
    return f"{NX_HUB_URL}{path}"


def search_registry(query: str, limit: int = 10) -> list[dict]:
    """Search the real mcp-hub marketplace registry."""
    servers = _load_registry()
    query_lower = query.lower()
    results = [
        server
        for server in servers
        if query_lower in server.get("name", "").lower()
        or query_lower in server.get("description", "").lower()
    ]
    return results[:limit]


def hub_health() -> dict:
    """
    Real health check - /api/servers returns 200 when hub is running.
    /health returns 404 and must not be used.
    """
    try:
        response = httpx.get(_hub_url(HUB["servers_api"]), timeout=3)
        if response.status_code == 200:
            data = response.json()
            servers = data.get("servers", [])
            connected = [server for server in servers if server.get("status") == "connected"]
            return {
                "running": True,
                "total_servers": len(servers),
                "connected": len(connected),
                "timestamp": data.get("timestamp"),
            }
    except Exception:
        pass
    return {"running": False}


def hub_start(config_path: Optional[Path] = None) -> dict:
    """Start mcp-hub if not already running."""
    status = hub_health()
    if status["running"]:
        return {"status": "already_running", **status}

    config = config_path or NX_HUB_CONFIG
    if not config.exists():
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(json.dumps({"mcpServers": {}}, indent=2))

    # Port resolution order:
    #   1) explicit NX_MCP_HUB_PORT (advanced users / CI)
    #   2) auto-allocate a free port and persist it for this nx process
    # Hard-coded 37373 was a collision vector for concurrent nx instances
    # and dev sessions.
    port_env = os.environ.get("NX_MCP_HUB_PORT")
    if port_env:
        port = port_env
    else:
        import socket as _sk
        try:
            with _sk.socket(_sk.AF_INET, _sk.SOCK_STREAM) as _s:
                _s.bind(("127.0.0.1", 0))
                port = str(_s.getsockname()[1])
        except OSError:
            port = "37373"

    # Capture stderr so spawn / bind failures surface to the caller instead
    # of being silently swallowed by /dev/null.
    log_dir = Path.home() / ".nx" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    stderr_log = log_dir / "mcp_hub.stderr.log"
    # Record which mcp-hub binary + version we're about to spawn, so a swapped
    # or unexpected binary on PATH is visible after the fact (supply-chain
    # hygiene — the binary is third-party and unpinned).
    try:
        import shutil as _shutil
        _resolved = _shutil.which("mcp-hub") or "mcp-hub"
        _ver = subprocess.run(["mcp-hub", "--version"], capture_output=True,
                              text=True, timeout=5)
        with open(stderr_log, "a") as _f:
            _f.write(f"[mcp-hub spawn] path={_resolved} "
                     f"version={(_ver.stdout or _ver.stderr).strip()[:60]}\n")
    except Exception:
        pass
    try:
        proc = subprocess.Popen(
            ["mcp-hub", "--port", str(port), "--config", str(config)],
            stdout=subprocess.DEVNULL,
            stderr=open(stderr_log, "a"),
        )
        time.sleep(3)
        # Confirm the process actually came up — Popen returns immediately even
        # when the spawned binary exits with an error.
        if proc.poll() is not None and proc.returncode != 0:
            tail = ""
            try:
                tail = stderr_log.read_text(errors="replace")[-400:]
            except Exception:
                pass
            return {
                "status": "spawn_failed",
                "error": f"mcp-hub exited with code {proc.returncode}",
                "stderr_tail": tail,
                "port": port,
            }
        return {"status": "started", "port": port, **hub_health()}
    except FileNotFoundError:
        return {
            "status": "not_installed",
            "error": "Run: npm install -g mcp-hub",
        }


def hub_list_tools(server_name: Optional[str] = None) -> list[dict]:
    """
    Real tool discovery via /api/servers.
    Returns servers[].capabilities.tools[].
    """
    try:
        response = httpx.get(_hub_url(HUB["servers_api"]), timeout=10)
        if response.status_code != 200:
            return []
        servers = response.json().get("servers", [])
        tools = []
        for server in servers:
            if server_name and server.get("name") != server_name:
                continue
            if server.get("status") != "connected":
                continue
            for tool in server.get("capabilities", {}).get("tools", []):
                tools.append(
                    {
                        **tool,
                        "server": server.get("name"),
                        "server_version": server.get("serverInfo", {}).get("version"),
                    }
                )
        return tools
    except Exception:
        return []


def hub_add_server(name: str, command: str, args: list[str], env: dict = {}) -> dict:
    """
    Add a server to mcp-hub config.
    Config shape validated from real boot output.
    """
    try:
        config = {}
        if NX_HUB_CONFIG.exists():
            config = json.loads(NX_HUB_CONFIG.read_text())

        if "mcpServers" not in config:
            config["mcpServers"] = {}

        config["mcpServers"][name] = {
            "command": command,
            "args": args,
            "env": env,
        }

        NX_HUB_CONFIG.parent.mkdir(exist_ok=True)
        NX_HUB_CONFIG.write_text(json.dumps(config, indent=2))
        return {"success": True, "name": name}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def hub_status() -> dict:
    """Hub status including per-server tool counts."""
    health = hub_health()
    if not health["running"]:
        return health

    tools = hub_list_tools()
    by_server: dict[str, int] = {}
    for tool in tools:
        server = tool["server"]
        by_server[server] = by_server.get(server, 0) + 1
    return {
        **health,
        "tools_total": len(tools),
        "tools_by_server": by_server,
    }
