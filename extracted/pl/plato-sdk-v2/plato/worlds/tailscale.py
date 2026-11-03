"""Tailscale VPN helpers for Plato worlds."""

from __future__ import annotations

import asyncio
import json
import logging
import shutil
from pathlib import Path
from typing import Any

import httpx

from plato.worlds.config import TailscaleConfig

logger = logging.getLogger(__name__)


async def generate_tailscale_auth_key(api_key: str) -> str:
    """Generate a short-lived, single-use auth key via the Tailscale API."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.tailscale.com/api/v2/tailnet/-/keys",
            auth=("", api_key),
            json={
                "capabilities": {
                    "devices": {
                        "create": {
                            "reusable": False,
                            "ephemeral": True,
                            "preauthorized": True,
                        }
                    }
                },
                "expirySeconds": 300,
            },
        )
        if resp.status_code != 200:
            raise RuntimeError(f"Tailscale API key generation failed (HTTP {resp.status_code}): {resp.text}")
        return resp.json()["key"]


async def setup_tailscale(
    ts: TailscaleConfig,
    *,
    log: logging.Logger = logger,
) -> asyncio.subprocess.Process | None:
    """Join a Tailscale tailnet using the API key to generate an auth key.

    Returns the ``tailscaled`` process if one was started (so the caller can
    clean it up later), or ``None`` if the daemon was already running.

    Raises RuntimeError if any step fails.
    """
    if not ts.enabled:
        return None

    if shutil.which("tailscale") is None or shutil.which("tailscaled") is None:
        log.info("Installing Tailscale...")
        proc = await asyncio.create_subprocess_shell(
            "curl -fsSL https://tailscale.com/install.sh | sh",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(f"Tailscale install failed (rc={proc.returncode}): {stderr.decode().strip()}")
    else:
        log.info("Tailscale already installed, skipping install")

    async def _tailscale_status() -> dict[str, Any] | None:
        proc = await asyncio.create_subprocess_exec(
            "sudo",
            "tailscale",
            "status",
            "--json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _stderr = await proc.communicate()
        if proc.returncode != 0:
            return None
        return json.loads(stdout.decode())

    status = await _tailscale_status()
    is_online = bool(status and status.get("Self", {}).get("Online"))

    tailscaled_proc: asyncio.subprocess.Process | None = None

    if not is_online:
        # Containers don't have systemd, so start tailscaled manually if needed.
        log.info("Starting tailscaled daemon...")
        tailscaled_proc = await asyncio.create_subprocess_exec(
            "sudo",
            "tailscaled",
            "--state=/var/lib/tailscale/tailscaled.state",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await asyncio.sleep(2)

        if not ts.api_key:
            raise RuntimeError(
                "tailscale.enabled is True but tailscale.api_key is not set "
                "and no existing tailnet connection was found"
            )

        # Generate a short-lived auth key via the Tailscale API only when reconnecting.
        log.info("Generating Tailscale auth key...")
        auth_key = await generate_tailscale_auth_key(ts.api_key)

        log.info("Connecting to tailnet...")
        proc = await asyncio.create_subprocess_exec(
            "sudo",
            "tailscale",
            "up",
            f"--auth-key={auth_key}",
            "--accept-dns=false",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(f"'tailscale up' failed (rc={proc.returncode}): {stderr.decode().strip()}")

        status = await _tailscale_status()
        if status is None:
            raise RuntimeError("'tailscale status' failed after connect")
    else:
        log.info("Tailscale already connected, skipping auth/up")

    assert status is not None
    self_name = status.get("Self", {}).get("HostName", "unknown")
    peers = status.get("Peer", {})
    peer_names = [p.get("HostName", "?") for p in peers.values()]
    log.info(
        "Tailscale connected as '%s', %d peer(s) visible",
        self_name,
        len(peer_names),
    )
    log.debug("Tailscale peers: %s", ", ".join(peer_names) or "(none)")

    # MagicDNS doesn't reliably configure the system resolver in
    # containers, so write /etc/hosts entries for all tailscale peers.
    hosts_lines = []
    for peer in peers.values():
        # DNSName is the tailscale MagicDNS name (e.g. "plato-a100.tail1234.ts.net.")
        # HostName is the OS hostname (e.g. "instance-20260226-193911")
        dns_name = peer.get("DNSName", "").rstrip(".")
        os_hostname = peer.get("HostName", "")
        # Extract short name from DNS (e.g. "plato-a100" from "plato-a100.tail1234.ts.net")
        short_name = dns_name.split(".")[0] if dns_name else ""
        addrs = peer.get("TailscaleIPs", [])
        if addrs:
            ipv4 = next((a for a in addrs if "." in a), None)
            if ipv4:
                names = []
                if short_name:
                    names.append(short_name)
                if os_hostname and os_hostname != short_name:
                    names.append(os_hostname)
                if names:
                    hosts_lines.append(f"{ipv4}\t{' '.join(names)}")
    if hosts_lines:
        try:
            hosts_block = "\n# Tailscale peers\n" + "\n".join(hosts_lines) + "\n"
            hosts_path = Path("/etc/hosts")
            existing = hosts_path.read_text()
            hosts_path.write_text(existing + hosts_block)
            log.info("Added %d tailscale peer(s) to /etc/hosts", len(hosts_lines))
            log.debug("Tailscale /etc/hosts entries: %s", ", ".join(hosts_lines))
        except Exception as e:
            log.warning(f"Failed to update /etc/hosts: {e}")

    return tailscaled_proc


async def cleanup_tailscale(
    proc: asyncio.subprocess.Process | None,
    *,
    log: logging.Logger = logger,
) -> None:
    """Terminate tailscaled if it was started by us."""
    if proc is None:
        return

    try:
        if proc.returncode is None:
            proc.terminate()
            try:
                await asyncio.wait_for(proc.wait(), timeout=5)
            except TimeoutError:
                log.warning("tailscaled did not exit after SIGTERM, sending SIGKILL")
                proc.kill()
                await proc.wait()
        else:
            await proc.wait()
    except ProcessLookupError:
        return
    except Exception as e:
        log.warning(f"Failed to cleanup tailscaled process: {e}")
