"""SSH-as-bootloader: bring an agent VM's daemon up, once.

The only SSH the RPC path keeps. One idempotent command installs the session
token and starts the daemon; the world then polls for readiness and caches the
handshake. Everything after this rides the daemon.

Bootstrap NEVER fails the session — on any failure the host is demoted to
``ssh_only`` and every call site falls back to its legacy SSH body.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from plato.rpc.client.manager import (
    close_agent_client,
    get_agent_client,
    get_host_state,
    session_token,
)
from plato.rpc.client.stubs import HealthStub
from plato.rpc.errors import AgentRpcError
from plato.rpc.protocol import (
    BOOTSTRAP_NO_DAEMON_RC,
    DEFAULT_PORT,
    LOG_FILE,
    STATE_DIR,
    TOKEN_FILE,
)
from plato.utils.subprocess import VM_PATH_EXPORT, run_ssh, scp_content_to_vm

logger = logging.getLogger(__name__)

_TOKEN_UPLOAD_PATH = "/tmp/.plato-agent-token"  # noqa: S108 - transient, 0600, moved server-side
_READINESS_BUDGET_S = 15.0
# exit-42 ("daemon binary absent") is retried within this budget rather than
# demoted on the first probe. The daemon arrives ~4s after boot via the runtime
# SDK upgrade in install_agent_code, which runs CONCURRENTLY with this probe
# (task.py's gather) — so "not installed" almost always means "not installed
# YET". The wait overlaps that install. A genuinely stale image (daemon never
# arrives) still demotes to SSH after the budget. This is also exactly what the
# no-ssh branch needs: with no fallback, waiting is the only correct behavior.
_NO_DAEMON_RETRY_BUDGET_S = 10.0
_NO_DAEMON_RETRY_DELAY_S = 2.0


def _bootstrap_command() -> str:
    # Idempotent: install token 0600, verify the daemon entry point exists
    # (exit 42 = stale baked SDK), then serve --daemonize (a no-op if already
    # running). Kept to plain, quoting-free shell — no payloads interpolated.
    return (
        # The shared export, NOT a hand-copy: the daemon's environ seeds every
        # job/exec spawn env, so a missing dir here (an early copy dropped
        # /usr/local/bin) breaks tool resolution for everything the daemon runs.
        f"{VM_PATH_EXPORT}; "
        f"install -d -m 0700 {STATE_DIR}; "
        f"install -m 0600 {_TOKEN_UPLOAD_PATH} {TOKEN_FILE} && rm -f {_TOKEN_UPLOAD_PATH}; "
        f"command -v plato-agent-daemon >/dev/null || exit {BOOTSTRAP_NO_DAEMON_RC}; "
        f"plato-agent-daemon serve --port {DEFAULT_PORT} "
        f"--token-file {TOKEN_FILE} --state-dir {STATE_DIR} "
        f"--log-file {LOG_FILE} --daemonize"
    )


async def ensure_daemon(
    hostname: str,
    ssh_key_path: Path,
    *,
    port: int = DEFAULT_PORT,
) -> bool:
    """Ensure the daemon is up on ``hostname`` and cache its handshake.

    Returns True if the host is now in ``rpc`` mode, False if it was demoted to
    ``ssh_only`` (caller then uses SSH). Never raises.
    """
    state = get_host_state(hostname)
    if state.mode == "rpc":
        return True
    if state.mode == "ssh_only":
        return False

    token = session_token()
    state.token = token
    loop = asyncio.get_running_loop()
    bootstrap_start = loop.time()
    no_daemon_deadline = bootstrap_start + _NO_DAEMON_RETRY_BUDGET_S
    probes = 0
    while True:
        probes += 1
        try:
            await scp_content_to_vm(ssh_key_path, hostname, _TOKEN_UPLOAD_PATH, token.encode())
            rc, _out, err = await run_ssh(ssh_key_path, hostname, _bootstrap_command(), timeout=60)
        except Exception as exc:  # noqa: BLE001 - bootstrap failures are non-fatal
            logger.warning("agentd bootstrap on %s failed pre-readiness: %s", hostname, exc)
            return _demote(hostname)

        if rc == BOOTSTRAP_NO_DAEMON_RC:
            # Daemon binary not present YET — the concurrent SDK upgrade is
            # likely still installing it. Retry within budget before demoting.
            if loop.time() < no_daemon_deadline:
                logger.info("agentd not yet installed on %s; retrying (SDK upgrade may still be in flight)", hostname)
                await asyncio.sleep(_NO_DAEMON_RETRY_DELAY_S)
                continue
            logger.info(
                "agentd still not installed on %s after %.0fs (stale image); using SSH",
                hostname,
                _NO_DAEMON_RETRY_BUDGET_S,
            )
            return _demote(hostname)
        if rc != 0:
            logger.warning("agentd bootstrap on %s exited %d: %s", hostname, rc, err.strip()[:400])
            return _demote(hostname)
        break

    if await _await_ready(hostname, token, port=port):
        # The happy-path duration: first probe -> armed. This is the number to
        # watch against _NO_DAEMON_RETRY_BUDGET_S — if it creeps toward the
        # budget, the wait is too tight (agents about to arm are demoting).
        logger.info(
            "agentd armed on %s after %.1fs (%d probe%s)",
            hostname,
            loop.time() - bootstrap_start,
            probes,
            "" if probes == 1 else "s",
        )
        return True
    await _log_remote_daemon_tail(ssh_key_path, hostname)
    return _demote(hostname)


async def _await_ready(hostname: str, token: str, *, port: int) -> bool:
    client = get_agent_client(hostname, token, port=port)
    loop = asyncio.get_running_loop()
    deadline = loop.time() + _READINESS_BUDGET_S
    delay = 0.2
    while loop.time() < deadline:
        try:
            handshake = await HealthStub(client).handshake(deadline_s=3.0)
        except AgentRpcError:
            await asyncio.sleep(delay)
            delay = min(delay * 2, 2.0)
            continue
        state = get_host_state(hostname)
        state.mode = "rpc"
        state.handshake = handshake
        logger.info(
            "agentd ready on %s: v%d caps=%s",
            hostname,
            handshake.protocol_version,
            ",".join(handshake.capabilities),
        )
        return True
    return False


async def _log_remote_daemon_tail(ssh_key_path: Path, hostname: str) -> None:
    try:
        _rc, out, _err = await run_ssh(ssh_key_path, hostname, f"tail -50 {LOG_FILE} 2>/dev/null", timeout=15)
        if out.strip():
            logger.warning("agentd log tail from %s:\n%s", hostname, out.strip()[-2000:])
    except Exception:  # noqa: BLE001 - diagnostics only
        pass


def _demote(hostname: str) -> bool:
    state = get_host_state(hostname)
    if state.mode == "rpc":
        # A concurrent bootstrap on this host already SUCCEEDED — overwriting
        # its verdict wedges a healthy daemon into ssh_only for the session
        # (the audit-M8 clobber). Keep the success and let this loser's op
        # proceed against the armed daemon; the tripwire log measures how
        # often the race actually fires in production.
        logger.warning(
            "Bootstrap race on %s: refusing to demote a host that already armed (concurrent bootstrap clobber)",
            hostname,
        )
        return True
    state.mode = "ssh_only"
    return False


async def teardown_host(hostname: str) -> None:
    """Drop client + state for a hostname (VM destroyed / mesh IP retired)."""
    await close_agent_client(hostname)
