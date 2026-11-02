"""WebSocket tunnel relay — bridges agent TCP connections to Teleport apps.

Protocol (binary WebSocket frames):
- Frame format: [1 byte cmd][4 bytes stream_id][payload]
- Commands:
    0x01 CONNECT  — agent requests connection to an app (payload = app_name)
    0x02 DATA     — bidirectional TCP data relay
    0x03 CLOSE    — close a stream
    0x04 ERROR    — error message (payload = UTF-8 error text)
    0x05 CONNECTED — server confirms connection established

Flow:
1. Agent opens WebSocket to /tunnel
2. Agent sends CONNECT frame with app_name
3. Server generates app certs via tbot --oneshot
4. Server opens TLS connection to Teleport proxy using the app certs
5. Bidirectional DATA frames relay bytes between agent and app
6. Either side sends CLOSE to tear down the stream
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import shutil
import ssl
import struct
import tempfile
import time

from starlette.websockets import WebSocket, WebSocketDisconnect

from cube_cloud.teleport.tbot_manager import PROFILE_ROLE_MAP
from cube_cloud.tunnel.connection_manager import ConnectionManager

logger = logging.getLogger(__name__)

TELEPORT_PROXY = os.environ.get("TELEPORT_PROXY", "edgescaleai.teleport.sh:443")
TELEPORT_PROXY_HOST = TELEPORT_PROXY.split(":")[0]
TELEPORT_PROXY_PORT = int(TELEPORT_PROXY.split(":")[-1]) if ":" in TELEPORT_PROXY else 443

# tbot's default certificate_ttl is ~1h; without an explicit value the cache
# would happily reuse a long-dead cert. Match the cache TTL window.
APP_CERT_TTL = os.environ.get("APP_CERT_TTL", "24h")

# A Teleport app name is a DNS label (lowercase alphanumeric + hyphens, 1–63
# chars). `app_name` is user-derived — from the browser proxy's Host header
# (already regex-guarded upstream in browser_proxy/resolver.py) AND from the
# agent's /tunnel CONNECT frame (arbitrary, agent-supplied). Before it is ever
# used to build a filesystem path or the tbot config, we validate it against
# this at the choke points below (fail-closed) so neither entry can inject
# `..`/`/` into a cert-dir path (CodeQL py/path-injection; defense-in-depth).
_SAFE_APP_NAME = re.compile(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$")

# Frame commands
CMD_CONNECT = 0x01
CMD_DATA = 0x02
CMD_CLOSE = 0x03
CMD_ERROR = 0x04
CMD_CONNECTED = 0x05

# Frame header: 1 byte cmd + 4 byte stream_id
HEADER_SIZE = 5


def pack_frame(cmd: int, stream_id: int, payload: bytes = b"") -> bytes:
    """Pack a tunnel frame."""
    return struct.pack("!BI", cmd, stream_id) + payload


def unpack_frame(data: bytes) -> tuple[int, int, bytes]:
    """Unpack a tunnel frame. Returns (cmd, stream_id, payload)."""
    if len(data) < HEADER_SIZE:
        raise ValueError(f"Frame too short: {len(data)} bytes")
    cmd, stream_id = struct.unpack("!BI", data[:HEADER_SIZE])
    return cmd, stream_id, data[HEADER_SIZE:]


# ---------------------------------------------------------------------------
# App cert manager — generates certs on demand via tbot --oneshot
# ---------------------------------------------------------------------------


class AppCertManager:
    """Generates Teleport app certs on demand using tbot --oneshot.

    Caches certs per app with a TTL. Certs are explicitly issued for
    ``APP_CERT_TTL`` (24h by default) via tbot's ``certificate_ttl``,
    capped by the Teleport role's ``max_session_ttl``. The cache evicts
    after ``CERT_TTL_SECONDS`` (slightly less than the cert TTL) to
    ensure we never serve an expired cert.
    """

    CERT_TTL_SECONDS = 23 * 3600  # 23h cache, paired with 24h cert TTL above

    def __init__(self) -> None:
        # Keyed by (profile, app_name) tuple for per-role cert isolation
        self._certs: dict[tuple[str, str], str] = {}
        self._cert_times: dict[tuple[str, str], float] = {}
        # One lock per cache key so concurrent callers racing a cold/expired
        # entry for the SAME (profile, app_name) serialize onto a single
        # `tbot oneshot` generation instead of each spawning their own
        # subprocess (a browser's page load alone can fire a dozen+ parallel
        # requests against a not-yet-cached app on first visit).
        self._locks: dict[tuple[str, str], asyncio.Lock] = {}

    def _cached_if_fresh(
        self, cache_key: tuple[str, str], profile: str, app_name: str, log_expired: bool = True,
    ) -> str | None:
        """Return the cached cert dir for ``cache_key`` iff it's still valid."""
        cert_dir = self._certs.get(cache_key)
        cert_time = self._cert_times.get(cache_key, 0)
        if cert_dir and os.path.exists(cert_dir):
            age = time.time() - cert_time
            if age < self.CERT_TTL_SECONDS and os.path.exists(os.path.join(cert_dir, "tlscert")):
                logger.debug("Using cached cert for %s/%s (age=%.0fs)", profile, app_name, age)
                return cert_dir
            if log_expired:
                logger.info("Cert cache expired for %s/%s (age=%.0fs), regenerating", profile, app_name, age)
        return None

    async def get_cert_dir(self, app_name: str, profile: str = "admin") -> str:
        """Get or generate the cert directory for an app, scoped to the user's profile."""
        # Fail-closed before app_name reaches any filesystem path (see _SAFE_APP_NAME).
        if not _SAFE_APP_NAME.fullmatch(app_name):
            raise ValueError(f"invalid Teleport app name: {app_name!r}")
        cache_key = (profile, app_name)
        cached = self._cached_if_fresh(cache_key, profile, app_name)
        if cached:
            return cached

        lock = self._locks.setdefault(cache_key, asyncio.Lock())
        async with lock:
            # Re-check after acquiring the lock: a concurrent caller may have
            # already generated a fresh cert while we were waiting on it.
            # Don't re-log "expired" here -- that was already reported (if
            # applicable) by the check above.
            cached = self._cached_if_fresh(cache_key, profile, app_name, log_expired=False)
            if cached:
                return cached

            cert_dir = await self._generate_cert(app_name, profile=profile)
            self._certs[cache_key] = cert_dir
            self._cert_times[cache_key] = time.time()
            return cert_dir

    async def _generate_cert(self, app_name: str, profile: str = "admin") -> str:
        """Run tbot --oneshot to generate app-specific TLS certs.

        When a profile is specified, the output is scoped to that Teleport role
        so Teleport enforces per-role app access.
        """
        # app_name is validated fail-closed at the entries (get_cert_dir /
        # open_app_connection), but we also keep it OUT of the tempdir path so no
        # user-derived value ever reaches a path expression at all — the tempdir is
        # a fixed prefix + random suffix; app_name still appears in the config +
        # logs below for debuggability (CodeQL py/path-injection: no path taint).
        cert_dir = tempfile.mkdtemp(prefix="tbot-app-")

        # Read join token from the existing tbot config (loaded by the sidecar)
        join_token = os.environ.get("TBOT_JOIN_TOKEN", "cube-mcp-bot-iam")

        # Scope the app cert output to the user's Teleport role
        role = PROFILE_ROLE_MAP.get(profile, profile)
        roles_line = f"\n    roles: [{role}]"

        config_yaml = f"""version: v2
proxy_server: {TELEPORT_PROXY}
credential_ttl: {APP_CERT_TTL}
onboarding:
  join_method: iam
  token: {join_token}
storage:
  type: memory
outputs:
  - type: application
    destination:
      type: directory
      path: {cert_dir}
    app_name: {app_name}{roles_line}
"""
        config_path = os.path.join(cert_dir, "tbot-config.yaml")
        with open(config_path, "w") as f:
            f.write(config_yaml)

        cmd = [
            "tbot",
            "start",
            "--oneshot",
            f"--config={config_path}",
            f"--certificate-ttl={APP_CERT_TTL}",
        ]
        logger.info("Generating app cert: tbot oneshot for %s", app_name)

        # Pass AWS credential env vars (ECS Fargate uses container credentials,
        # not EC2 IMDS, so we must forward these for IAM join to work)
        tbot_env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/tmp"}
        for key in (
            "AWS_CONTAINER_CREDENTIALS_RELATIVE_URI",
            "AWS_CONTAINER_CREDENTIALS_FULL_URI",
            "AWS_CONTAINER_AUTHORIZATION_TOKEN",
            "AWS_DEFAULT_REGION",
            "AWS_REGION",
            "ECS_CONTAINER_METADATA_URI_V4",
        ):
            val = os.environ.get(key)
            if val:
                tbot_env[key] = val

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=tbot_env,
        )
        try:
            stdout_data, stderr_data = await asyncio.wait_for(
                proc.communicate(), timeout=30
            )
        except asyncio.TimeoutError:
            proc.kill()
            shutil.rmtree(cert_dir, ignore_errors=True)
            raise RuntimeError(f"tbot oneshot timed out for '{app_name}'")

        stderr_text = stderr_data.decode(errors="replace")
        logger.debug("tbot oneshot exit=%d stderr=%s", proc.returncode, stderr_text[-1000:])

        if proc.returncode != 0:
            shutil.rmtree(cert_dir, ignore_errors=True)
            raise RuntimeError(
                f"tbot oneshot failed (exit {proc.returncode}): {stderr_text[-500:]}"
            )

        cert_files = os.listdir(cert_dir)
        logger.debug("tbot generated files in %s: %s", cert_dir, cert_files)

        if "tlscert" not in cert_files:
            shutil.rmtree(cert_dir, ignore_errors=True)
            raise RuntimeError(f"tbot did not generate tlscert for '{app_name}': {cert_files}")

        return cert_dir

    def invalidate(self, app_name: str, profile: str = "admin") -> None:
        """Remove cached cert for an app/profile combination."""
        cache_key = (profile, app_name)
        cert_dir = self._certs.pop(cache_key, None)
        self._cert_times.pop(cache_key, None)
        if cert_dir:
            shutil.rmtree(cert_dir, ignore_errors=True)


_cert_mgr = AppCertManager()


# ---------------------------------------------------------------------------
# Direct TLS connection to Teleport proxy
# ---------------------------------------------------------------------------


async def open_app_connection(
    app_name: str, profile: str = "admin",
) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
    """Open a TLS connection to a Teleport app using tbot-generated certs.

    The connection goes to <app_name>.<teleport_proxy_host>:443 with mTLS.
    """
    # Fail-closed before app_name reaches any filesystem path (see _SAFE_APP_NAME).
    if not _SAFE_APP_NAME.fullmatch(app_name):
        raise ValueError(f"invalid Teleport app name: {app_name!r}")
    cert_dir = await _cert_mgr.get_cert_dir(app_name, profile=profile)

    # Build SSL context with app-specific client cert
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.load_cert_chain(
        certfile=os.path.join(cert_dir, "tlscert"),
        keyfile=os.path.join(cert_dir, "key"),
    )

    # Load Teleport CA for server verification
    teleport_cas = os.path.join(cert_dir, "teleport-database-ca.pem")
    teleport_host_cas = os.path.join(cert_dir, "teleport-host-ca.pem")
    teleport_user_cas = os.path.join(cert_dir, "teleport-user-ca.pem")

    # Try loading available CA files; fall back to not verifying if none found
    loaded_ca = False
    for ca_file in [teleport_cas, teleport_host_cas, teleport_user_cas]:
        if os.path.exists(ca_file):
            try:
                ctx.load_verify_locations(cafile=ca_file)
                loaded_ca = True
            except Exception:
                pass

    if not loaded_ca:
        # Fall back to system CAs or skip verification
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        logger.warning("No Teleport CA found, disabling server cert verification")

    # Set ALPN protocol for TCP apps so Teleport routes to the TCP proxy
    # instead of defaulting to HTTP reverse proxy (which breaks MQTT etc.)
    from cube_cloud.teleport.tbot_manager import tbot

    app_type = await tbot.get_app_type(app_name, profile=profile)
    if app_type == "TCP":
        ctx.set_alpn_protocols(["teleport-tcp"])
        logger.debug("Setting ALPN=teleport-tcp for TCP app %s", app_name)

    # Connect to the Teleport proxy
    # For app access, connect to the proxy host (apps are routed via SNI/ALPN)
    app_host = f"{app_name}.{TELEPORT_PROXY_HOST}"
    logger.debug("Connecting TLS to %s:%d (SNI=%s, type=%s)", TELEPORT_PROXY_HOST, TELEPORT_PROXY_PORT, app_host, app_type)

    reader, writer = await asyncio.open_connection(
        TELEPORT_PROXY_HOST,
        TELEPORT_PROXY_PORT,
        ssl=ctx,
        server_hostname=app_host,
    )

    logger.debug("TLS connection established to %s", app_name)
    return reader, writer


# ---------------------------------------------------------------------------
# Tunnel relay
# ---------------------------------------------------------------------------


class TunnelRelay:
    """Handles a single WebSocket tunnel connection from a cube-agent.

    Each WebSocket can multiplex multiple streams (one per app connection).
    """

    def __init__(self, ws: WebSocket, conn_mgr: ConnectionManager, profile: str = "admin") -> None:
        self.ws = ws
        self.conn_mgr = conn_mgr
        self.profile = profile
        # stream_id -> (reader, writer) asyncio TCP connection
        self._streams: dict[int, tuple[asyncio.StreamReader, asyncio.StreamWriter]] = {}
        self._relay_tasks: dict[int, asyncio.Task] = {}

    async def run(self) -> None:
        """Main loop: read WebSocket frames, dispatch by command."""
        logger.info("Tunnel relay run() started")
        try:
            while True:
                raw = await self.ws.receive_bytes()
                cmd, stream_id, payload = unpack_frame(raw)

                if cmd == CMD_CONNECT:
                    asyncio.create_task(self._handle_connect(stream_id, payload))
                elif cmd == CMD_DATA:
                    await self._handle_data(stream_id, payload)
                elif cmd == CMD_CLOSE:
                    await self._handle_close(stream_id)
                else:
                    logger.warning("Unknown tunnel command: 0x%02x", cmd)

        except WebSocketDisconnect:
            logger.info("Tunnel WebSocket disconnected")
        except Exception as e:
            logger.error("Tunnel relay error: %s", e)
        finally:
            await self._cleanup()

    async def _handle_connect(self, stream_id: int, payload: bytes) -> None:
        """Handle CONNECT: open TLS connection to Teleport app."""
        app_name = payload.decode("utf-8")
        logger.info("Tunnel CONNECT stream=%d app=%s", stream_id, app_name)

        try:
            reader, writer = await asyncio.wait_for(
                open_app_connection(app_name, profile=self.profile),
                timeout=45,  # tbot oneshot + TLS connect
            )
        except asyncio.TimeoutError:
            await self._send_error(stream_id, f"Connection to {app_name} timed out")
            return
        except Exception as e:
            logger.error("CONNECT failed for %s: %s", app_name, e)
            await self._send_error(stream_id, f"Failed to connect to '{app_name}': {e}")
            return

        self._streams[stream_id] = (reader, writer)
        self.conn_mgr.add_stream(stream_id, app_name)

        # Send CONNECTED confirmation
        await self.ws.send_bytes(pack_frame(CMD_CONNECTED, stream_id))
        logger.info("Stream %d connected to %s", stream_id, app_name)

        # Start background task to relay TCP→WebSocket
        task = asyncio.create_task(self._relay_tcp_to_ws(stream_id, reader))
        self._relay_tasks[stream_id] = task

    async def _handle_data(self, stream_id: int, payload: bytes) -> None:
        """Handle DATA: forward bytes from WebSocket to TCP."""
        stream = self._streams.get(stream_id)
        if not stream:
            return
        _, writer = stream
        try:
            writer.write(payload)
            await writer.drain()
        except Exception as e:
            logger.warning("TCP write error stream=%d: %s", stream_id, e)
            await self._close_stream(stream_id)

    async def _handle_close(self, stream_id: int) -> None:
        """Handle CLOSE: tear down a stream."""
        await self._close_stream(stream_id)

    async def _relay_tcp_to_ws(self, stream_id: int, reader: asyncio.StreamReader) -> None:
        """Background task: relay TCP data → WebSocket DATA frames."""
        try:
            while True:
                data = await reader.read(32768)
                if not data:
                    break
                await self.ws.send_bytes(pack_frame(CMD_DATA, stream_id, data))
        except Exception as e:
            logger.debug("TCP read done stream=%d: %s", stream_id, e)
        finally:
            # Notify agent that stream is closed
            try:
                await self.ws.send_bytes(pack_frame(CMD_CLOSE, stream_id))
            except Exception:
                pass
            await self._close_stream(stream_id)

    async def _send_error(self, stream_id: int, message: str) -> None:
        """Send an ERROR frame to the agent."""
        try:
            await self.ws.send_bytes(pack_frame(CMD_ERROR, stream_id, message.encode("utf-8")))
        except Exception:
            pass

    async def _close_stream(self, stream_id: int) -> None:
        """Close a single stream."""
        # Cancel relay task
        task = self._relay_tasks.pop(stream_id, None)
        if task and not task.done():
            task.cancel()

        # Close TCP connection
        stream = self._streams.pop(stream_id, None)
        if stream:
            _, writer = stream
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

        self.conn_mgr.remove_stream(stream_id)

    async def _cleanup(self) -> None:
        """Close all streams on disconnect."""
        for stream_id in list(self._streams):
            await self._close_stream(stream_id)
