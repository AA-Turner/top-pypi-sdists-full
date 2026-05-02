"""NAT traversal using Cloudflare Tunnel (cloudflared).

Provides a public URL to access the MJPEG viewer from anywhere,
even behind NAT/firewalls. Uses free quick tunnels (no account needed).

On Windows, auto-downloads cloudflared.exe on first use (~30MB).
Fallback: detect local IP and provide LAN-accessible URL.
"""

from __future__ import annotations

import asyncio
import logging
import re
import shutil
import socket
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

_CLOUDFLARED_VERSION = "2026.2.0"
_CLOUDFLARED_URL = (
    f"https://github.com/cloudflare/cloudflared/releases/download/"
    f"{_CLOUDFLARED_VERSION}/cloudflared-windows-amd64.exe"
)


def _get_cloudflared_path() -> Path:
    """Return the expected path for the bundled cloudflared binary."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent / "cloudflared.exe"
    from ghost_pc.config.schema import GHOST_HOME

    return GHOST_HOME / "cloudflared.exe"


def _find_cloudflared() -> str | None:
    """Find cloudflared: bundled location → PATH → auto-download."""
    # 1. Check bundled/cached location
    cached = _get_cloudflared_path()
    if cached.is_file():
        return str(cached)

    # 2. Check system PATH
    system = shutil.which("cloudflared")
    if system:
        return system

    return None


async def _download_cloudflared() -> str | None:
    """Download cloudflared.exe to the local cache (Windows only)."""
    if sys.platform != "win32":
        return None

    dest = _get_cloudflared_path()
    dest.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Downloading cloudflared for remote access (~30MB)...")
    try:
        proc = await asyncio.create_subprocess_exec(
            "powershell",
            "-Command",
            f'Invoke-WebRequest -Uri "{_CLOUDFLARED_URL}" -OutFile "{dest}" -UseBasicParsing',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await asyncio.wait_for(proc.communicate(), timeout=120)
        if dest.is_file() and dest.stat().st_size > 1_000_000:
            logger.info("cloudflared downloaded to %s", dest)
            return str(dest)
        else:
            logger.warning("cloudflared download failed or file too small")
            if dest.exists():
                dest.unlink()
            return None
    except Exception as e:
        logger.warning("cloudflared download error: %s", e)
        if dest.exists():
            dest.unlink()
        return None


async def start_tunnel(port: int) -> str | None:
    """Start a Cloudflare quick tunnel pointing at the given local port.

    Returns the public URL (e.g., https://xyz.trycloudflare.com) or None if failed.
    Auto-downloads cloudflared on Windows if not found.
    """
    cloudflared = _find_cloudflared()
    if not cloudflared:
        cloudflared = await _download_cloudflared()
    if not cloudflared:
        logger.warning("cloudflared not available. Remote access disabled.")
        return None

    try:
        proc = await asyncio.create_subprocess_exec(
            cloudflared,
            "tunnel",
            "--url",
            f"http://localhost:{port}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # cloudflared prints the public URL to stderr
        url: str | None = None
        start = asyncio.get_event_loop().time()
        timeout = 30.0

        while proc.stderr:
            try:
                line_bytes = await asyncio.wait_for(proc.stderr.readline(), timeout=5.0)
            except TimeoutError:
                if asyncio.get_event_loop().time() - start > timeout:
                    break
                continue

            if not line_bytes:
                break

            line = line_bytes.decode("utf-8", errors="replace")
            logger.debug("[cloudflared] %s", line.strip())

            # Look for the tunnel URL in the output
            match = re.search(r"(https://[a-z0-9-]+\.trycloudflare\.com)", line)
            if match:
                url = match.group(1)
                logger.info("Cloudflare tunnel active: %s", url)
                return url

        logger.warning("Failed to start Cloudflare tunnel within %ds", timeout)
        proc.terminate()
        return None

    except Exception as e:
        logger.error("Cloudflare tunnel error: %s", e)
        return None


def get_local_ip() -> str:
    """Get the machine's LAN IP address."""
    try:
        # Connect to an external address to determine the local IP
        # (doesn't actually send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_viewer_url(port: int, token: str, tunnel_url: str | None = None) -> str:
    """Build the best available viewer URL.

    Prefers tunnel URL if available, falls back to LAN IP.
    """
    if tunnel_url:
        return f"{tunnel_url}/view?token={token}"
    local_ip = get_local_ip()
    return f"http://{local_ip}:{port}/view?token={token}"
