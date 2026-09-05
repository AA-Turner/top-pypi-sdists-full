"""Plato SDK v2 - Synchronous Sandbox Client.

The SandboxClient provides methods for sandbox development workflows:
creating sandboxes, managing SSH, syncing files, running flows, etc.
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
import shutil
import subprocess
import tempfile
import time
import uuid
from contextlib import suppress
from pathlib import Path
from typing import Literal, cast
from urllib.parse import quote

import httpx
import yaml
from pydantic import BaseModel
from rich.console import Console

from plato._generated.api.v1.cluster import prefetch_snapshot
from plato._generated.api.v1.env import cleanup as env_cleanup
from plato._generated.api.v1.env import get_simulator_by_name as env_get_simulator_by_name
from plato._generated.api.v1.gitea import (
    create_simulator_repository,
    get_accessible_simulators,
    get_gitea_credentials,
    get_simulator_repository,
)
from plato._generated.api.v1.sandbox import start_worker
from plato._generated.api.v1.simulator import get_env_flows as simulator_get_env_flows
from plato._generated.api.v1.simulator import get_plato_config as simulator_get_plato_config
from plato._generated.api.v1.simulator import get_simulator_versions as simulator_get_simulator_versions
from plato._generated.api.v2.jobs import add_ssh_key as jobs_add_ssh_key
from plato._generated.api.v2.jobs import checkpoint as jobs_checkpoint
from plato._generated.api.v2.jobs import get_flows as jobs_get_flows
from plato._generated.api.v2.jobs import get_job_info as jobs_get_job_info
from plato._generated.api.v2.jobs import public_url as jobs_public_url
from plato._generated.api.v2.jobs import rdp_url as jobs_rdp_url
from plato._generated.api.v2.jobs import reset as jobs_reset
from plato._generated.api.v2.jobs import snapshot as jobs_snapshot
from plato._generated.api.v2.jobs import state as jobs_state
from plato._generated.api.v2.jobs import wait_for_ready as jobs_wait_for_ready
from plato._generated.api.v2.sessions import add_job as sessions_add_job
from plato._generated.api.v2.sessions import add_ssh_key as sessions_add_ssh_key
from plato._generated.api.v2.sessions import close as sessions_close
from plato._generated.api.v2.sessions import connect_network as sessions_connect_network
from plato._generated.api.v2.sessions import get_public_url as sessions_get_public_url
from plato._generated.api.v2.sessions import get_session_details
from plato._generated.api.v2.sessions import remove_job as sessions_remove_job
from plato._generated.api.v2.sessions import reset as sessions_reset
from plato._generated.api.v2.sessions import snapshot as sessions_snapshot
from plato._generated.api.v2.sessions import state as sessions_state
from plato._generated.models import (
    AddJobRequest,
    AddSSHKeyRequest,
    AppApiV2SchemasSessionCreateSnapshotRequest,
    AppApiV2SchemasSessionCreateSnapshotResponse,
    AppSchemasBuildModelsSimConfigDataset,
    ArtifactCredential,
    ArtifactCredentials,
    ArtifactMcpConfig,
    CloseSessionResponse,
    CreateCheckpointRequest,
    CreateCheckpointResult,
    CreateSnapshotResult,
    DatabaseMutationListenerConfig,
    EnvCleanupResponse,
    Flow,
    Kind,
    PrefetchRequest,
    RemoveJobRequest,
    RemoveJobResponse,
    ResetJobResult,
    ResetSessionRequest,
    ResetSessionResponse,
    ResolvedMcpConfig,
    SessionDetailsResponse,
    SessionStateResponse,
    SessionStateResult,
    VMManagementRequest,
)
from plato.chronos.api.sessions import get_session_envs as chronos_get_session_envs
from plato.utils.ssh import gateway_proxy_command
from plato.utils.subprocess import ssh_user_for_provider
from plato.v1.models.sandbox import PlatoConfig
from plato.v2._wait_for_ready import is_terminal_status, poll_until_ready_sync
from plato.v2.async_.flow_executor import FlowExecutor
from plato.v2.models import SandboxState
from plato.v2.sandbox_store import (
    HEARTBEAT_PROC_MARKER,
    SandboxStore,
    heartbeat_log_path,
    slugify,
    stop_heartbeat,
)
from plato.v2.sync.artifact import ArtifactManager
from plato.v2.types import Env, EnvFromArtifact, EnvFromResource, EnvFromSimulator, SimConfigCompute

logger = logging.getLogger(__name__)


SSH_CACHE_DIR = Path.home() / ".cache" / "plato" / "ssh"
DEFAULT_BASE_URL = "https://plato.so"
DEFAULT_TIMEOUT = 600.0
VALID_PROVIDERS = {"firecracker", "qemu"}


def _get_plato_dir(working_dir: Path | None = None) -> Path:
    """Get the .plato directory path."""
    base = working_dir or Path.cwd()
    return base / ".plato"


def _generate_ssh_key_pair(prefix: str, working_dir: Path | None = None) -> tuple[str, str]:
    """Generate an SSH key pair and save to .plato/ directory.

    Args:
        prefix: Prefix for key filename.
        working_dir: Working directory for .plato/.

    Returns:
        Tuple of (public_key_content, private_key_path).
    """
    plato_dir = _get_plato_dir(working_dir)
    plato_dir.mkdir(mode=0o700, exist_ok=True)

    key_name = f"ssh_key_{prefix}"
    private_key_path = plato_dir / key_name
    public_key_path = plato_dir / f"{key_name}.pub"

    # Remove existing keys
    if private_key_path.exists():
        private_key_path.unlink()
    if public_key_path.exists():
        public_key_path.unlink()

    # Generate key pair
    subprocess.run(
        [
            "ssh-keygen",
            "-t",
            "ed25519",
            "-f",
            str(private_key_path),
            "-N",
            "",
            "-q",
        ],
        check=True,
    )

    # Read public key
    public_key = public_key_path.read_text().strip()

    return public_key, str(private_key_path)


def _generate_ssh_config(
    job_id: str,
    private_key_path: str,
    working_dir: Path | None = None,
    ssh_host: str = "sandbox",
    provider: str | None = None,
    mesh_ip: str | None = None,
    name: str | None = None,
) -> str:
    """Generate SSH config file for easy access via gateway.

    Args:
        job_id: The job ID for routing.
        private_key_path: Path to private key (absolute or relative).
        mesh_ip: WireGuard mesh IP of the VM. When set (attached sandboxes,
            where the caller runs on a VM inside the same session mesh), the
            config connects to it directly — in-VPC, no gateway ProxyCommand,
            no NAT round-trip.
        working_dir: Working directory for .plato/.
        ssh_host: Host alias in config.
        name: Sandbox slot name. When given, the config is written to
            ``.plato/ssh_config_<name>`` (so sibling sandboxes in one working
            directory don't overwrite each other's) and ``.plato/ssh_config``
            is pointed at it, keeping the documented
            ``ssh -F .plato/ssh_config sandbox`` working for the current slot.
        provider: Hypervisor backing the job ("firecracker", "qemu", or None
            when unknown). Determines the ``User`` line — see
            :func:`~plato.utils.subprocess.ssh_user_for_provider`. ``None`` falls back to ``root``.

    Returns:
        Path to the generated SSH config file (relative to working_dir).

    Note:
        The IdentityFile in the config uses a path relative to working_dir.
        SSH commands must be run from the workspace root for paths to resolve.
    """
    gateway_host = os.getenv("PLATO_GATEWAY_HOST", "gateway.plato.so")

    # Convert private key path to be relative to working_dir
    # This ensures the config is portable if the workspace moves
    base = working_dir or Path.cwd()
    try:
        relative_key_path = Path(private_key_path).relative_to(base)
    except ValueError:
        # If not relative to working_dir, keep as-is (shouldn't happen normally)
        relative_key_path = Path(private_key_path)

    # SNI format: {job_id}--{port}.{gateway_host} (matches v1 proxy.py)
    ssh_port = 22
    sni = f"{job_id}--{ssh_port}.{gateway_host}"
    ssh_user = ssh_user_for_provider(provider)
    # Both aliases resolve to the same VM, so `ssh -F .plato/ssh_config sandbox`
    # (documented everywhere) and `ssh -F .plato/ssh_config_<name> <name>` work.
    host_aliases = f"{ssh_host} {name}" if name and name != ssh_host else ssh_host

    if mesh_ip:
        config_content = f"""# Plato Sandbox SSH Config (mesh-direct)
# Generated for job: {job_id}
# Connects to the VM's WireGuard mesh IP directly (same-session mesh).
# NOTE: Run SSH commands from workspace root for relative paths to resolve

Host {host_aliases}
    HostName {mesh_ip}
    Port {ssh_port}
    User {ssh_user}
    IdentityFile {relative_key_path}
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
"""
    else:
        config_content = f"""# Plato Sandbox SSH Config
# Generated for job: {job_id}
# NOTE: Run SSH commands from workspace root for relative paths to resolve

Host {host_aliases}
    HostName {job_id}
    User {ssh_user}
    IdentityFile {relative_key_path}
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
    ProxyCommand {gateway_proxy_command(gateway_host, sni)}
"""

    store = SandboxStore(working_dir or Path.cwd())
    store.plato_dir.mkdir(mode=0o700, parents=True, exist_ok=True)

    # Per-slot file; `.plato/ssh_config` is a symlink the store repoints at
    # whichever slot is current (on save, on `use`, and on stop), so it never
    # drifts to a sandbox you did not select or one that is gone.
    config_path = store.ssh_config_path(name) if name else store.ssh_config_file
    config_path.write_text(config_content)

    return str(config_path)


def _run_ssh_command(
    ssh_config_path: str,
    ssh_host: str,
    command: str,
    cwd: Path | str | None = None,
) -> tuple[int, str, str]:
    """Run a command via SSH.

    Args:
        ssh_config_path: Path to SSH config file (can be relative).
        ssh_host: SSH host alias from config.
        command: Command to execute on remote.
        cwd: Working directory to run SSH from. Required when ssh_config_path
             contains relative paths (e.g., for IdentityFile).

    Returns:
        Tuple of (returncode, stdout, stderr).
    """
    result = subprocess.run(
        ["ssh", "-F", ssh_config_path, ssh_host, command],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    return result.returncode, result.stdout, result.stderr


#: PowerShell run on Windows guests by ``SandboxClient.enable_manual_control``.
#: Clears Winlogon ``ForceAutoLogon`` (the console auto-logon reclaim that
#: bounces human RDP sessions) and verifies the write; ``AutoAdminLogon`` is
#: left untouched so the agent user still auto-logs on at boot. Sent via
#: ``powershell -EncodedCommand`` so no quoting survives the ssh → cmd.exe →
#: powershell chain.
_MANUAL_CONTROL_PS = """
$winlogon = 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon'
Set-ItemProperty -Path $winlogon -Name ForceAutoLogon -Value '0' -Type String
$value = (Get-ItemProperty -Path $winlogon).ForceAutoLogon
if ($value -ne '0') { Write-Error "ForceAutoLogon is '$value' after update"; exit 1 }
Write-Output 'ForceAutoLogon=0'
""".strip()


# =============================================================================
# HEARTBEAT UTILITIES
# =============================================================================


#: A session that answers 404/410 is gone for good, so the heartbeat exits
#: instead of POSTing into the void forever. Small enough that a clobbered or
#: crashed CLI leaks a process for minutes rather than days, large enough to
#: ride out a backend blip.
_HEARTBEAT_GONE_STREAK = 5
#: Failures of any other kind (network down, 5xx) get a much longer rope —
#: killing a heartbeat over a flaky wifi hop would take the VM down with it.
_HEARTBEAT_ERROR_STREAK = 120
#: Seconds between beats. The backend expires a session after ~2 minutes
#: without one, so this only ever wants shortening (tests do exactly that).
_HEARTBEAT_INTERVAL_ENV = "PLATO_HEARTBEAT_INTERVAL_SECONDS"
_HEARTBEAT_INTERVAL_DEFAULT = 30.0


def _start_heartbeat_process(session_id: str, api_key: str, slot_path: str | Path) -> int | None:
    """Start a background process that sends heartbeats.

    Uses only stdlib (urllib) to work on any machine without dependencies.

    The process is detached (survives the terminal) but it is *owned by its
    slot file*, which it re-reads before every beat, and it exits on its own
    when any of these say the sandbox is over:

    - the slot file is gone or records ``stopped_at`` (a ``stop``, a
      ``--remove``, even an ``rm -rf`` of the working directory)
    - the slot's ``session_id`` changed (the name was reused)
    - the slot's ``expires_at`` has passed — the idle lease. Commands that use
      the sandbox push ``expires_at`` forward, so an actively-used sandbox
      stays alive and an abandoned one dies at most ``--timeout`` after the
      last touch. An immortal orphan is impossible by construction.
    - the backend answers 404/410 repeatedly (the session is already gone)

    Because the slot file is the kill switch, stopping a sandbox never
    requires *finding* this process; the recorded pid is only used to kill it
    a beat sooner than it would exit anyway.

    Returns:
        PID of the background process, or None if failed.
    """
    log_file = str(heartbeat_log_path(session_id))
    base_url = os.getenv("PLATO_BASE_URL", "https://plato.so")
    # Strip trailing /api if present to avoid double /api/api in URL
    if base_url.endswith("/api"):
        base_url = base_url[:-4]
    base_url = base_url.rstrip("/")
    try:
        interval = float(os.getenv(_HEARTBEAT_INTERVAL_ENV, _HEARTBEAT_INTERVAL_DEFAULT))
    except ValueError:
        interval = _HEARTBEAT_INTERVAL_DEFAULT

    # Use only stdlib - no external dependencies
    heartbeat_script = f"""
# {HEARTBEAT_PROC_MARKER}: identifies this process as a Plato sandbox heartbeat.
import os
import sys
import time
import json
import urllib.request
import urllib.error
from datetime import datetime

session_id = "{session_id}"
# Read from the environment rather than the script body: argv is world-readable
# in `ps`, and this key would otherwise be printed to every user on the box.
api_key = os.environ.pop("PLATO_HEARTBEAT_API_KEY", "")
base_url = "{base_url}"
log_file = "{log_file}"
slot_path = {json.dumps(str(slot_path))}
GONE_STREAK = {_HEARTBEAT_GONE_STREAK}
ERROR_STREAK = {_HEARTBEAT_ERROR_STREAK}
INTERVAL = {interval}

def log(msg):
    timestamp = datetime.now().isoformat()
    with open(log_file, "a") as f:
        f.write(f"[{{timestamp}}] {{msg}}\\n")
        f.flush()

def slot_verdict(missing_streak):
    # The slot file owns this process. Only a *definitive* signal may end it:
    # the file being gone twice in a row (writes are atomic renames, but be
    # cheap insurance against an unlink+rewrite editor), a recorded stop, the
    # name now holding a different session, or the lease running out. An
    # unreadable or corrupt file keeps the sandbox alive — never kill a VM
    # over a parse error.
    try:
        with open(slot_path) as f:
            data = json.load(f)
    except FileNotFoundError:
        return ("slot file gone" if missing_streak + 1 >= 2 else None), missing_streak + 1
    except Exception:
        return None, 0
    if not isinstance(data, dict):
        return None, 0
    if data.get("stopped_at"):
        return "slot stopped", 0
    sid = data.get("session_id")
    if sid and sid != session_id:
        return "slot reused for another session", 0
    expires_at = data.get("expires_at")
    if expires_at and time.time() >= float(expires_at):
        return "lease expired (idle past --timeout; any sandbox command renews it)", 0
    return None, 0

log(f"Heartbeat process started for session {{session_id}}")
log(f"URL: {{base_url}}/api/v2/sessions/{{session_id}}/heartbeat")
log(f"Owned by slot file: {{slot_path}}")

heartbeat_count = 0
gone_streak = 0
error_streak = 0
missing_streak = 0
while True:
    reason, missing_streak = slot_verdict(missing_streak)
    if reason:
        log(f"{{reason}} - exiting; the backend reaps the session on heartbeat loss")
        sys.exit(0)
    heartbeat_count += 1
    try:
        url = f"{{base_url}}/api/v2/sessions/{{session_id}}/heartbeat"
        req = urllib.request.Request(
            url,
            method="POST",
            headers={{"X-API-Key": api_key, "Content-Type": "application/json"}},
            data=b"{{}}",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
            result = json.loads(body)
            success = result.get("success", False)
            log(f"Heartbeat #{{heartbeat_count}}: status={{status}}, success={{success}}")
        gone_streak = 0
        error_streak = 0
    except urllib.error.HTTPError as e:
        log(f"Heartbeat #{{heartbeat_count}}: HTTP {{e.code}} - {{e.reason}}")
        error_streak += 1
        # 404/410 mean the session no longer exists: nothing left to keep
        # alive, so exit instead of outliving the sandbox forever.
        if e.code in (404, 410):
            gone_streak += 1
            if gone_streak >= GONE_STREAK:
                log(f"Session gone ({{e.code}}) {{gone_streak}}x in a row - exiting")
                sys.exit(0)
        else:
            gone_streak = 0
    except Exception as e:
        log(f"Heartbeat #{{heartbeat_count}} EXCEPTION: {{type(e).__name__}}: {{e}}")
        error_streak += 1
    if error_streak >= ERROR_STREAK:
        log(f"{{error_streak}} consecutive failures - exiting")
        sys.exit(0)
    time.sleep(INTERVAL)
"""

    try:
        process = subprocess.Popen(
            ["python3", "-c", heartbeat_script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
            env={**os.environ, "PLATO_HEARTBEAT_API_KEY": api_key},
        )
        return process.pid
    except Exception:
        return None


#: Killing a heartbeat is :func:`plato.v2.sandbox_store.stop_heartbeat` — a
#: verified SIGTERM (the pid must carry the heartbeat marker in its argv, so a
#: recycled pid is never killed). It is a courtesy for immediacy only: the
#: heartbeat's slot file is its kill switch and it exits on its own within a
#: beat of the slot being stopped or removed.


class SyncResult(BaseModel):
    files_synced: int
    bytes_synced: int


class SSHConfigInfo(BaseModel):
    """SSH config information for connecting to a job."""

    config_content: str
    private_key_path: str
    job_id: str
    gateway_host: str


def _generate_temp_ssh_key_pair() -> tuple[str, str]:
    """Generate a temporary SSH key pair.

    Returns:
        Tuple of (public_key_content, private_key_path).
    """
    # Create temp directory for keys
    temp_dir = tempfile.mkdtemp(prefix="plato_ssh_")
    private_key_path = os.path.join(temp_dir, "id_ed25519")

    # Generate key pair
    subprocess.run(
        [
            "ssh-keygen",
            "-t",
            "ed25519",
            "-f",
            private_key_path,
            "-N",
            "",
            "-q",
        ],
        check=True,
    )

    # Read public key
    public_key = Path(f"{private_key_path}.pub").read_text().strip()

    return public_key, private_key_path


def _get_or_create_cached_ssh_key_pair() -> tuple[str, str]:
    """Get or create a cached SSH key pair at ~/.cache/plato/ssh/.

    Returns:
        Tuple of (public_key_content, private_key_path).
    """
    SSH_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    private_key_path = SSH_CACHE_DIR / "id_ed25519"
    public_key_path = SSH_CACHE_DIR / "id_ed25519.pub"

    if private_key_path.exists() and public_key_path.exists():
        private_key_path.chmod(0o600)
        logger.debug("Reusing cached SSH key pair at %s", private_key_path)
        return public_key_path.read_text().strip(), str(private_key_path)

    # Clean partial state + stale session cache before regenerating
    for p in (private_key_path, public_key_path, SSH_CACHE_DIR / "authorized_sessions"):
        p.unlink(missing_ok=True)

    logger.debug("Generating new SSH key pair at %s", private_key_path)
    subprocess.run(
        ["ssh-keygen", "-t", "ed25519", "-f", str(private_key_path), "-N", "", "-q"],
        check=True,
    )

    return public_key_path.read_text().strip(), str(private_key_path)


def _generate_ssh_config_content(job_id: str, private_key_path: str, provider: str | None = None) -> str:
    """Generate SSH config content for a job.

    Args:
        job_id: The job ID for routing.
        private_key_path: Path to private key.
        provider: Hypervisor backing the job ("firecracker", "qemu", or None
            when unknown). Determines the ``User`` line — see
            :func:`~plato.utils.subprocess.ssh_user_for_provider`. ``None`` falls back to ``root``
            for backwards compatibility with older job-info responses.

    Returns:
        SSH config content as a string.
    """
    gateway_host = os.getenv("PLATO_GATEWAY_HOST", "gateway.plato.so")

    # SNI format: {job_id}--{port}.{gateway_host}
    ssh_port = 22
    sni = f"{job_id}--{ssh_port}.{gateway_host}"
    ssh_user = ssh_user_for_provider(provider)

    config_content = f"""# Plato SSH Config for job: {job_id}
# Generated dynamically for -J/--job-id option

Host sandbox
    HostName {job_id}
    User {ssh_user}
    IdentityFile {private_key_path}
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
    ProxyCommand {gateway_proxy_command(gateway_host, sni)}
"""
    return config_content


# =============================================================================
# TUNNEL
# =============================================================================

DEFAULT_GATEWAY_HOST = "gateway.plato.so"
DEFAULT_GATEWAY_PORT = 443


def _get_gateway_config() -> tuple[str, int]:
    """Get gateway host and port from environment or defaults."""
    host = os.environ.get("PLATO_GATEWAY_HOST", DEFAULT_GATEWAY_HOST)
    port = int(os.environ.get("PLATO_GATEWAY_PORT", str(DEFAULT_GATEWAY_PORT)))
    return host, port


def _create_tls_connection(
    gateway_host: str,
    gateway_port: int,
    sni: str,
    verify_ssl: bool = True,
):
    """Create a TLS connection to the gateway with the specified SNI."""
    import socket
    import ssl

    context = ssl.create_default_context()
    if not verify_ssl:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)
    ssl_sock = context.wrap_socket(sock, server_hostname=sni)

    try:
        ssl_sock.connect((gateway_host, gateway_port))
    except Exception as e:
        ssl_sock.close()
        raise ConnectionError(f"Failed to connect to gateway: {e}") from e

    return ssl_sock


def _forward_data(src, dst, name: str = "") -> None:
    """Forward data between two sockets until one closes."""
    import socket

    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        try:
            dst.shutdown(socket.SHUT_WR)
        except OSError:
            pass


#: How long ``Tunnel``'s accept loop blocks before re-checking ``_running``.
#: This is what bounds ``Tunnel.stop()``: a blocked ``accept()`` does not wake
#: when the listening socket is closed from another thread, so stop() waits out
#: at most one poll interval.
_TUNNEL_ACCEPT_POLL_S = 0.2


class Tunnel:
    """A TCP tunnel to a remote port on a sandbox VM.

    Goes via the TLS gateway by default; when ``mesh_ip`` is set (attached
    sandboxes, caller on a VM inside the same session mesh) it forwards
    directly to the mesh IP — in-VPC, no gateway NAT round-trip.
    """

    def __init__(
        self,
        job_id: str,
        remote_port: int,
        local_port: int | None = None,
        bind_address: str = "127.0.0.1",
        verify_ssl: bool = True,
        mesh_ip: str | None = None,
    ):
        self.job_id = job_id
        self.remote_port = remote_port
        self.local_port = local_port or remote_port
        self.bind_address = bind_address
        self.verify_ssl = verify_ssl
        self.mesh_ip = mesh_ip

        self._server = None
        self._thread = None
        self._running = False

    def start(self) -> int:
        """Start the tunnel. Returns the local port."""
        import socket
        import threading

        gateway_host, gateway_port = _get_gateway_config()
        sni = f"{self.job_id}--{self.remote_port}.{gateway_host}"

        # Create local listener
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self._server.bind((self.bind_address, self.local_port))
            self._server.listen(5)
        except OSError as e:
            raise ValueError(f"Could not bind to {self.bind_address}:{self.local_port}: {e}") from e

        self._running = True

        def handle_client(client_sock, client_addr):
            try:
                if self.mesh_ip:
                    upstream_sock = socket.create_connection((self.mesh_ip, self.remote_port), timeout=30)
                else:
                    upstream_sock = _create_tls_connection(gateway_host, gateway_port, sni, verify_ssl=self.verify_ssl)
                t1 = threading.Thread(
                    target=_forward_data,
                    args=(client_sock, upstream_sock, "client->upstream"),
                    daemon=True,
                )
                t2 = threading.Thread(
                    target=_forward_data,
                    args=(upstream_sock, client_sock, "upstream->client"),
                    daemon=True,
                )
                t1.start()
                t2.start()
                t1.join()
                t2.join()
            except Exception:
                pass
            finally:
                try:
                    client_sock.close()
                except OSError:
                    pass

        def accept_loop():
            server = self._server
            assert server is not None, "Server must be initialized before accept_loop"
            while self._running:
                try:
                    server.settimeout(_TUNNEL_ACCEPT_POLL_S)
                    client_sock, client_addr = server.accept()
                    threading.Thread(
                        target=handle_client,
                        args=(client_sock, client_addr),
                        daemon=True,
                    ).start()
                except TimeoutError:
                    continue
                except OSError:
                    break

        self._thread = threading.Thread(target=accept_loop, daemon=True)
        self._thread.start()

        return self.local_port

    def stop(self) -> None:
        """Stop the tunnel."""
        self._running = False
        if self._server:
            try:
                self._server.close()
            except OSError:
                pass
        if self._thread:
            self._thread.join(timeout=2.0)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False


# =============================================================================
# SANDBOX CLIENT
# =============================================================================

DEFAULT_CHRONOS_URL = "https://chronos.plato.so"


def resolve_chronos_plato_session_id(
    chronos_session_id: str,
    api_key: str,
    chronos_url: str | None = None,
) -> str:
    """Resolve a Chronos session public id to its backing Plato session id.

    Chronos tracks envs by reading them off the Plato session it launched
    (``GET /api/sessions/{id}/envs`` joins on ``plato_session_id``), so
    attaching a sandbox to a Chronos session means adding its job to that
    Plato session.
    """
    base = (chronos_url or os.environ.get("CHRONOS_URL") or DEFAULT_CHRONOS_URL).rstrip("/")
    with httpx.Client(base_url=base, timeout=httpx.Timeout(30)) as client:
        envs_response = chronos_get_session_envs.sync(
            client,
            public_id=chronos_session_id,
            x_api_key=api_key,
        )
    if not envs_response.plato_session_id:
        raise RuntimeError(f"Chronos session {chronos_session_id} has no backing Plato session to attach envs to")
    return envs_response.plato_session_id


def dataset_config_from_plato_config(
    plato_config: object, dataset: str, *, source: str
) -> AppSchemasBuildModelsSimConfigDataset:
    """Validate one dataset of a plato-config through the generated backend-schema model.

    This is the model to use whenever the config is *serialised* (config-mode
    snapshots, start-worker): it is regenerated from the backend's
    ``SimConfigDataset`` and therefore carries every field the backend knows —
    ``audit_ignore_tables``, ``native_worker``, ... The hand-maintained
    :class:`plato.v1.models.sandbox.PlatoConfig` declares neither and silently
    dropped both from the ``plato_config`` stored on every config-mode snapshot.
    """
    if not isinstance(plato_config, dict):
        raise ValueError(f"Invalid plato config in {source}: expected a top-level mapping")
    config = cast(dict[str, object], plato_config)
    datasets = config.get("datasets")
    if isinstance(datasets, dict):
        datasets = cast(dict[str, object], datasets)
        dataset_config = datasets.get(dataset)
        if dataset_config is None:
            available_datasets = sorted(str(name) for name in datasets.keys())
            raise ValueError(f"Dataset '{dataset}' not found in {source}. Available datasets: {available_datasets}")
    else:
        # Config without a datasets wrapper — treat the top-level mapping as the
        # dataset config directly (some artifacts store it this way).
        dataset_config = config
    return AppSchemasBuildModelsSimConfigDataset.model_validate(dataset_config)


# Variable names (metadata.variables[].name) that identify the login credential.
_USER_VARIABLES = ("username", "user", "email", "login")
_PASSWORD_VARIABLES = ("password", "pass")
_TOKEN_VARIABLES = ("token", "api_key", "api_token", "secret")


def credentials_from_dataset_config(
    dataset_config: AppSchemasBuildModelsSimConfigDataset,
) -> ArtifactCredentials | None:
    """Login credentials to store on the artifact, read from plato-config metadata.

    The artifact stores structured credentials next to its flows so consumers
    (task cards, ``Session.login``) never have to parse ``flows.yml``. Two
    sources, explicit first:

    * ``metadata.credentials`` — the API shape verbatim (``primary`` plus
      optional ``roles``); use it for role accounts or non-password kinds.
    * ``metadata.variables`` — the login variables the flows fill:
      ``username``/``user``/``email``/``login`` + ``password`` → a password
      credential; a user alone → ``email_only``; a token/secret alone →
      ``token``.

    Returns None when neither is declared — the backend then carries the parent
    artifact's credentials forward, and a first snapshot stores none.
    """
    metadata = dataset_config.metadata
    if metadata is None:
        return None
    explicit = (metadata.model_extra or {}).get("credentials")
    if explicit is not None:
        if not isinstance(explicit, dict):
            raise ValueError("metadata.credentials must be a mapping with 'primary' and optional 'roles'")
        return ArtifactCredentials.model_validate(explicit)

    values: dict[str, str] = {}
    for variable in metadata.variables or []:
        name = str(variable.get("name", "")).strip().lower()
        value = variable.get("value")
        if name and value is not None:
            values[name] = str(value)
    user = next((values[n] for n in _USER_VARIABLES if n in values), None)
    password = next((values[n] for n in _PASSWORD_VARIABLES if n in values), None)
    token = next((values[n] for n in _TOKEN_VARIABLES if n in values), None)
    if user and password is not None:
        primary = ArtifactCredential(kind=Kind.password, user=user, password=password)
    elif user:
        primary = ArtifactCredential(kind=Kind.email_only, user=user)
    elif token:
        primary = ArtifactCredential(kind=Kind.token, secret=token)
    else:
        return None
    return ArtifactCredentials(primary=primary)


def describe_credentials(credentials: ArtifactCredentials | None) -> str:
    """One-line, secret-free summary for console output (``user=admin kind=password``)."""
    if credentials is None or credentials.primary is None:
        return "none"
    primary = credentials.primary
    kind = primary.kind.value if primary.kind is not None else "password"
    parts = [f"kind={kind}"]
    if primary.user:
        parts.insert(0, f"user={primary.user}")
    if credentials.roles:
        parts.append(f"roles={','.join(sorted(credentials.roles))}")
    return " ".join(parts)


def describe_mcp_config(mcp: ArtifactMcpConfig | ResolvedMcpConfig | None) -> str:
    """One-line summary for console output (``enabled=True port=3000 path=/mcp``).

    ``none`` = nothing stored on the artifact; ``inherit`` = a config whose
    every field is unset — :meth:`SandboxClient._build_checkpoint_request` drops
    such a config from the request, so the backend inherits the parent
    artifact's rather than being handed an empty override.
    """
    if mcp is None:
        return "none"
    # port/path are root models on the stored config, plain scalars on the resolved one
    parts = [
        f"{name}={getattr(value, 'root', value)}"
        for name, value in (("enabled", mcp.enabled), ("port", mcp.port), ("path", mcp.path))
        if value is not None
    ]
    return " ".join(parts) or "inherit"


class SandboxClient:
    """Synchronous client for sandbox development workflows.

    Supports two modes:
    1. Stateless (working_dir=None): Pure operations, no file I/O
    2. Stateful (working_dir=Path): Persists state to .plato/state.yaml

    Usage (stateless):
        client = SandboxClient(api_key="...")
        result = client.start(mode="blank", service="myservice")
        client.stop(result.session_id)
        client.close()

    Usage (stateful - recommended for CLI/scripts):
        client = SandboxClient(api_key="...", working_dir=Path("."))
        client.start(mode="blank", service="myservice")  # Saves state
        # Later...
        client = SandboxClient(api_key="...", working_dir=Path("."))  # Loads state
        client.stop()  # Uses saved session_id
    """

    # State file paths
    PLATO_DIR = ".plato"

    def __init__(
        self,
        working_dir: Path,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        console: Console = Console(),
        sandbox_name: str | None = None,
    ):
        self.api_key = api_key or os.environ.get("PLATO_API_KEY")
        if not self.api_key:
            raise ValueError("API key required. Set PLATO_API_KEY or pass api_key=")

        url = base_url or os.environ.get("PLATO_BASE_URL", DEFAULT_BASE_URL)
        if url.endswith("/api"):
            url = url[:-4]
        self.base_url = url.rstrip("/")
        self.console = console
        self.working_dir = working_dir
        self.store = SandboxStore(working_dir)
        # Slot these operations act on (``--name`` / ``$PLATO_SANDBOX``);
        # None means whichever slot ``.plato/current`` points at.
        self.sandbox_name = sandbox_name

        self._http = httpx.Client(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout),
        )
        self.artifacts = ArtifactManager(self._http, self.api_key)

    def _get_plato_dir(self) -> Path:
        return Path(self.working_dir) / self.PLATO_DIR

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    # -------------------------------------------------------------------------
    # START
    # -------------------------------------------------------------------------

    def start(
        self,
        simulator_name: str | None = None,
        mode: str = "blank",
        # artifact or simulator mode
        artifact_id: str | None = None,
        dataset: str = "base",
        tag: str | None = None,
        # blankl or plato-config mode
        cpus: int = 1,
        memory: int = 2048,
        disk: int = 10240,
        app_port: int | None = None,
        messaging_port: int | None = None,
        # common
        connect_network: bool = True,
        timeout: int = 1800,
        provider: str | None = None,
        chronos_session_id: str | None = None,
        attach_strict: bool = True,
        name: str | None = None,
    ) -> SandboxState:
        """Start a sandbox environment.

        Uses Plato SDK v2 internally for session creation.

        Args:
            name: Slot to store this sandbox under in ``.plato/sandboxes/``.
                Defaults to the simulator name, suffixed if that slot is taken,
                so a second start in the same working directory gets its own
                slot instead of overwriting the first one.
            mode: Start mode - "blank", "simulator", or "artifact".
            simulator_name: Simulator name.
            artifact_id: Artifact UUID.
            dataset: Dataset name.
            tag: Artifact tag.
            cpus: Number of CPUs.
            memory: Memory in MB.
            disk: Disk in MB.
            app_port: App port.
            messaging_port: Messaging port.
            connect_network: Whether to connect WireGuard network.
            provider: VM provider for blank/config resource VMs. Use "qemu" for Windows VMs.
            chronos_session_id: When set, attach the sandbox to this Chronos
                session instead of creating a standalone Plato session: the env
                is added as a job on the session's backing Plato session, so
                Chronos tracks it and its lifetime is bound to that session.
            attach_strict: When False, a failure to resolve the Chronos
                session's backing Plato session falls back to a standalone
                sandbox with a warning instead of raising. The CLI uses this
                for the ambient env-var default so legacy flows on sessions
                without a plato_session_id keep working; explicit
                --chronos-session stays strict.

        Returns:
            SandboxState with sandbox info.
        """

        assert self.api_key is not None
        provider_literal: Literal["firecracker", "qemu"] | None = None
        if provider is not None:
            if provider not in VALID_PROVIDERS:
                raise ValueError(
                    f"Invalid provider '{provider}'. Expected one of: {', '.join(sorted(VALID_PROVIDERS))}"
                )
            if mode not in {"blank", "config"}:
                raise ValueError("--provider is only supported for blank and config sandbox modes")
            provider_literal = cast(Literal["firecracker", "qemu"], provider)

        # Build environment config using Env factory
        env_config: EnvFromSimulator | EnvFromArtifact | EnvFromResource
        config_cpus: int | None = None
        config_memory: int | None = None
        config_disk: int | None = None
        config_app_port: int | None = None
        config_messaging_port: int | None = None

        if mode == "artifact" and artifact_id:
            self.console.print(f"[cyan]Mode:[/cyan] artifact ({artifact_id})")
            env_config = Env.artifact(artifact_id)
        elif mode == "simulator" and simulator_name:
            self.console.print(f"[cyan]Mode:[/cyan] simulator ({simulator_name}:{tag})")
            env_config = Env.simulator(simulator_name, tag=tag, dataset=dataset)
        elif mode == "blank":
            # Use provided simulator_name or default to "sandbox"
            sim_name = simulator_name or "sandbox"
            self.console.print(f"[cyan]Mode:[/cyan] blank VM ({sim_name})")
            self.console.print(f"[dim]  cpus={cpus}, memory={memory}MB, disk={disk}MB[/dim]")
            sim_config = SimConfigCompute(
                cpus=cpus, memory=memory, disk=disk, app_port=app_port, plato_messaging_port=messaging_port
            )
            env_config = Env.resource(sim_name, sim_config, provider=provider_literal)
        elif mode == "config":
            self.console.print("[cyan]Mode:[/cyan] config (plato-config.yml)")
            # read plato-config.yml
            plato_config_path = self.working_dir / "plato-config.yml"
            with open(plato_config_path, "rb") as f:
                plato_config = yaml.safe_load(f)
            plato_config_model = PlatoConfig.model_validate(plato_config)
            dataset_config = plato_config_model.datasets[dataset]
            simulator_name = plato_config_model.service
            if not simulator_name:
                raise ValueError("Service name is required in plato-config.yml")
            if not dataset_config.compute:
                raise ValueError(f"Compute configuration is required for dataset '{dataset}'")
            self.console.print(f"simulator_name: {simulator_name}")
            # Save compute values for state (will be used later when saving state.json)
            config_cpus = dataset_config.compute.cpus
            config_memory = dataset_config.compute.memory
            config_disk = dataset_config.compute.disk
            config_app_port = dataset_config.compute.app_port
            config_messaging_port = dataset_config.compute.plato_messaging_port
            sim_config = SimConfigCompute(
                cpus=config_cpus,
                memory=config_memory,
                disk=config_disk,
                app_port=config_app_port,
                plato_messaging_port=config_messaging_port,
            )
            env_config = Env.resource(simulator_name, sim_config, provider=provider_literal)
        else:
            raise ValueError(f"Invalid mode '{mode}' or missing required parameter")

        # Track total time
        total_start = time.time()

        # We do each step separately to show progress:
        # 1. Create session, 2. Wait for ready, 3. Setup SSH
        from plato._generated.api.v2.sessions import make as sessions_make
        from plato._generated.api.v2.sessions import wait_for_ready as sessions_wait_for_ready
        from plato._generated.models import CreateSessionFromEnvs, Envs, RunSessionSource

        attached = chronos_session_id is not None
        attach_plato_session_id: str | None = None
        sandbox_mesh_ip: str | None = None
        if attached:
            assert chronos_session_id is not None
            self.console.print(f"[cyan]Attaching to Chronos session:[/cyan] {chronos_session_id}")
            try:
                attach_plato_session_id = resolve_chronos_plato_session_id(chronos_session_id, self.api_key)
            except Exception as exc:
                if attach_strict:
                    raise
                self.console.print(
                    f"[yellow]Could not attach to Chronos session {chronos_session_id} ({exc}); "
                    "starting a standalone sandbox instead[/yellow]"
                )
                attached = False

        if attached:
            assert attach_plato_session_id is not None
            # Step 1 (attached): add the env as a job on the Plato session
            # backing the Chronos session, so Chronos tracks and manages it.
            session_id = attach_plato_session_id
            if env_config.alias is None:
                env_config.alias = f"sandbox-{simulator_name or mode}-{uuid.uuid4().hex[:8]}"
            self.console.print("[yellow]Adding env to session...[/yellow]")
            step_start = time.time()
            add_response = sessions_add_job.sync(
                client=self._http,
                session_id=session_id,
                body=AddJobRequest(env=env_config, timeout=timeout),
                x_api_key=self.api_key,
            )
            if not add_response.env.success:
                raise RuntimeError(f"Failed to add environment to session {session_id}: {add_response.env.error}")
            if not add_response.env.job_id:
                raise ValueError("No job ID found")
            # Dedicated str-typed local: `job_id` is also assigned in the other
            # branch, which voids narrowing inside the wait lambda's closure.
            added_job_id: str = add_response.env.job_id
            job_id = added_job_id
            if not simulator_name:
                simulator_name = add_response.env.simulator
            elapsed = time.time() - step_start
            self.console.print(
                f"[green]Env added:[/green] {job_id} (alias={env_config.alias}) [dim]({elapsed:.1f}s)[/dim]"
            )
        else:
            # Step 1: Create session
            self.console.print("[yellow]Creating session...[/yellow]")
            step_start = time.time()
            request_body = CreateSessionFromEnvs(
                envs=[Envs(root=env_config)],
                timeout=timeout,
                source=RunSessionSource.SDK,
            )
            response = sessions_make.sync(
                client=self._http,
                body=request_body,
                x_api_key=self.api_key,
            )
            session_id = response.session_id
            elapsed = time.time() - step_start
            self.console.print(f"[green]Session created:[/green] {session_id} [dim]({elapsed:.1f}s)[/dim]")

            # Check if any envs failed to create
            if response.envs:
                for env_result in response.envs:
                    if not env_result.success:
                        raise RuntimeError(f"Failed to create environment: {env_result.error}")
                    if env_result.job_id:
                        self.console.print(f"[dim]  Job: {env_result.job_id}[/dim]")
            else:
                raise RuntimeError("No environments created in session")

            job_id = response.envs[0].job_id if response.envs else None
            if not job_id:
                raise ValueError("No job ID found")

        # The session (and its job) now exists remotely — record it locally
        # *before* the long wait for the VM. The slot is a write-ahead intent
        # record: from this point there is no window in which a running VM has
        # no local trace, so a crash anywhere below leaves a slot that `list`
        # shows, `stop -n` tears down, and whose heartbeat exits on its own.
        # Failure handling collapses to the one shared teardown path.
        slot_name: str | None = None
        heartbeat_pid: int | None = None
        try:
            if not simulator_name and mode == "artifact":
                # Best-effort, purely for a friendlier slot name: the job
                # record carries its service from creation, but if the lookup
                # fails the slot is just named after the mode.
                with suppress(Exception):
                    simulator_name = self._lookup_simulator_name(session_id, job_id, attached)
            slot_name = self.store.claim(slugify(name) if name else slugify(simulator_name or mode))
            if name and slot_name != slugify(name):
                self.console.print(
                    f"[yellow]Slot '{slugify(name)}' was claimed by a concurrent start; using '{slot_name}'[/yellow]"
                )
            started_at = time.time()
            # make_current=False: the slot must be findable (list, stop -n,
            # the heartbeat) from the moment the session exists, but `current`
            # — what another terminal's bare `ssh`/`stop`/`status` acts on —
            # must keep meaning the previous, *usable* sandbox until this one
            # is ready. The final save below flips it.
            self.store.save(
                slot_name,
                {
                    "session_id": session_id,
                    "job_id": job_id,
                    "mode": mode,
                    "simulator_name": simulator_name,
                    "dataset": dataset,
                    "attached": attached,
                    "chronos_session_id": chronos_session_id if attached else None,
                    "created_at": started_at,
                    "expires_at": started_at + timeout,
                    "timeout": timeout,
                },
                make_current=False,
            )

            # Start the heartbeat now, so even the boot wait is covered.
            # Attached sandboxes skip it: the Chronos runtime already
            # heartbeats the shared session, and their lifetime should be
            # bound to that session, not to a local process.
            if attached:
                self.console.print("[dim]Skipping local heartbeat — lifecycle owned by the Chronos session[/dim]")
            else:
                heartbeat_pid = _start_heartbeat_process(session_id, self.api_key, self.store.path(slot_name))
                if heartbeat_pid:
                    self.store.update(slot_name, heartbeat_pid=heartbeat_pid)
                    self.console.print(f"[green]Heartbeat started[/green] (pid={heartbeat_pid})")
                else:
                    self.console.print("[dim]Heartbeat failed to start[/dim]")

            # Step 2: wait for the VM. Attached waits on just our job — the
            # shared session's other envs are none of our business.
            self.console.print("[yellow]Waiting for VM to start...[/yellow]")
            step_start = time.time()
            if attached:
                # Dedicated str-typed local: `job_id` is assigned in both
                # branches, which voids narrowing inside the lambda's closure.
                wait_job_id: str = str(job_id)
                job_ready_response = poll_until_ready_sync(
                    lambda per_call: jobs_wait_for_ready.sync(
                        client=self._http,
                        job_id=wait_job_id,
                        timeout=per_call,
                        x_api_key=self.api_key,
                    ),
                    timeout=timeout,
                )
                if not job_ready_response.ready:
                    reason = job_ready_response.error or (
                        "terminal status" if is_terminal_status(job_ready_response) else "timeout"
                    )
                    raise RuntimeError(f"VM failed to start: {reason}")
                # The backend adds the job to the session mesh and ready-wait
                # blocks until it has joined, so the mesh IP is usable now.
                sandbox_mesh_ip = job_ready_response.mesh_ip
            else:
                ready_response = poll_until_ready_sync(
                    lambda per_call: sessions_wait_for_ready.sync(
                        client=self._http,
                        session_id=session_id,
                        timeout=per_call,
                        x_api_key=self.api_key,
                    ),
                    timeout=timeout,
                )
                if not ready_response.ready:
                    errors = []
                    if ready_response.results:
                        for jid, result in ready_response.results.items():
                            if not result.ready:
                                errors.append(f"{jid}: {result.error or 'Unknown error'}")
                    reason = (
                        ", ".join(errors)
                        if errors
                        else ("terminal status" if is_terminal_status(ready_response) else "timeout")
                    )
                    raise RuntimeError(f"VM failed to start: {reason}")

            elapsed = time.time() - step_start
            self.console.print(f"[green]VM ready:[/green] {job_id} [dim]({elapsed:.1f}s)[/dim]")

            # Step 3: Connect network
            network_connected = False
            if attached:
                # The backend auto-joined the job to the session's WireGuard mesh
                # (Chronos sessions always have one); a session-level connect here
                # would mutate network state for every env in the shared session.
                network_connected = sandbox_mesh_ip is not None
                if sandbox_mesh_ip:
                    self.console.print(f"[green]Joined session mesh:[/green] {sandbox_mesh_ip}")
                else:
                    self.console.print("[dim]No mesh IP reported; session network may be absent[/dim]")
            elif connect_network:
                self.console.print("[yellow]Connecting network...[/yellow]")
                step_start = time.time()
                connect_response = sessions_connect_network.sync(
                    client=self._http,
                    session_id=session_id,
                    x_api_key=self.api_key,
                )
                network_connected = connect_response.get("success", False)
                elapsed = time.time() - step_start
                self.console.print(f"[green]Network connected:[/green] {network_connected} [dim]({elapsed:.1f}s)[/dim]")
            else:
                self.console.print("[dim]Skipping network connection (--no-network)[/dim]")

            # Artifact mode needs simulator_name for the public URL; required
            # from here even if the best-effort lookup above was skipped.
            if not simulator_name:
                simulator_name = self._lookup_simulator_name(session_id, job_id, attached)
                if not simulator_name:
                    raise ValueError(f"No simulator name found in session details for job ID {job_id}")

            # Get public URL with router target formatting (logic inlined)
            public_url = None
            try:
                urls: list[str | None] = []
                if attached:
                    job_url_response = jobs_public_url.sync(
                        client=self._http,
                        job_id=job_id,
                        x_api_key=self.api_key,
                    )
                    if job_url_response:
                        urls.append(job_url_response.url)
                else:
                    url_response = sessions_get_public_url.sync(
                        client=self._http,
                        session_id=session_id,
                        x_api_key=self.api_key,
                    )
                    if url_response and url_response.results:
                        urls.extend(
                            result.url if hasattr(result, "url") else str(result)
                            for result in url_response.results.values()
                        )
                for url in urls:
                    if not url:
                        raise ValueError(f"No public URL found in result dict for job ID {job_id}")
                    if "_plato_router_target=" not in url and simulator_name:
                        target_param = f"_plato_router_target={simulator_name}.web.plato.so"
                        if "?" in url:
                            url = f"{url}&{target_param}"
                        else:
                            url = f"{url}?{target_param}"
                    public_url = url
                elapsed = time.time() - step_start
                self.console.print(f"[green]Public URL:[/green] {public_url} [dim]({elapsed:.1f}s)[/dim]")
            except Exception as e:
                self.console.print(f"[dim]Public URL not available: {e}[/dim]")

            # Setup SSH. Look up provider so the generated ssh_config uses the
            # right User — root for firecracker/Linux, plato for QEMU/Windows.
            # Falls back to root when the field is missing (older API rollouts),
            # which keeps the legacy firecracker path working.
            # If the caller passed --provider explicitly, use that; otherwise look
            # it up from job info (covers artifact/simulator modes where the
            # provider is determined by the backend).
            private_key_path: str | None = None
            ssh_config_path: str | None = None
            self.console.print("[yellow]Setting up SSH...[/yellow]")
            step_start = time.time()
            try:
                if provider is None:
                    try:
                        job_info = jobs_get_job_info.sync(
                            client=self._http,
                            job_id=job_id,
                            x_api_key=self.api_key,
                        )
                        provider = getattr(job_info, "provider", None) or (
                            job_info.model_dump().get("provider") if hasattr(job_info, "model_dump") else None
                        )
                    except Exception as e:
                        # Non-fatal: provider lookup failure → fall through with root user.
                        self.console.print(f"[dim]Provider lookup failed (defaulting to firecracker): {e}[/dim]")

                install_user = ssh_user_for_provider(provider)
                public_key, private_key_path = _generate_ssh_key_pair(
                    f"{slot_name}_{job_id[:8]}", Path(self.working_dir)
                )

                # ``username`` is advisory — the v2 add_ssh_key endpoint enforces
                # the correct user server-side, but we send the right value so
                # audit logs match what actually gets provisioned on the guest.
                add_key_request = AddSSHKeyRequest(public_key=public_key, username=install_user)
                if attached:
                    # Job-scoped: the session-level endpoint would install the key
                    # on every VM in the shared session.
                    key_response = jobs_add_ssh_key.sync(
                        client=self._http,
                        job_id=job_id,
                        body=add_key_request,
                        x_api_key=self.api_key,
                    )
                    key_added = key_response.success
                else:
                    add_response = sessions_add_ssh_key.sync(
                        client=self._http,
                        session_id=session_id,
                        body=add_key_request,
                        x_api_key=self.api_key,
                    )
                    key_added = add_response.success

                if key_added:
                    ssh_config_path = _generate_ssh_config(
                        job_id,
                        private_key_path,
                        Path(self.working_dir),
                        provider=provider,
                        mesh_ip=sandbox_mesh_ip,
                        name=slot_name,
                    )
                    elapsed = time.time() - step_start
                    self.console.print(
                        f"[green]SSH configured:[/green] ssh -F .plato/ssh_config {slot_name} [dim]({elapsed:.1f}s)[/dim]"
                    )
                else:
                    self.console.print("[dim]SSH key upload failed[/dim]")
            except Exception as e:
                self.console.print(f"[dim]SSH setup failed: {e}[/dim]")

            # Convert absolute paths to relative for state storage
            def _to_relative(abs_path: str | None) -> str | None:
                if not abs_path or not self.working_dir:
                    return abs_path
                try:
                    return str(Path(abs_path).relative_to(self.working_dir))
                except ValueError:
                    return abs_path  # Keep absolute if not relative to working_dir

            # Update internal state. created_at/expires_at come from the intent
            # record written before the boot wait, so the lease starts counting
            # from creation — using commands push expires_at forward from here.
            rel_ssh_config = _to_relative(ssh_config_path)
            ssh_host = "sandbox" if ssh_config_path else None
            sandbox_state = SandboxState(
                name=slot_name,
                session_id=session_id,
                job_id=job_id,
                public_url=public_url,
                mode=mode,
                ssh_config_path=rel_ssh_config,
                ssh_host=ssh_host,
                ssh_command=f"ssh -F {rel_ssh_config} {ssh_host}" if rel_ssh_config else None,
                ssh_key_path=_to_relative(private_key_path),
                heartbeat_pid=heartbeat_pid,
                simulator_name=simulator_name,
                dataset=dataset,
                provider=provider,
                network_connected=network_connected,
                attached=attached,
                chronos_session_id=chronos_session_id if attached else None,
                mesh_ip=sandbox_mesh_ip,
                created_at=started_at,
                expires_at=started_at + timeout,
                timeout=timeout,
            )
            if mode == "artifact":
                sandbox_state.artifact_id = artifact_id
            elif mode == "simulator":
                sandbox_state.tag = tag
            elif mode == "blank":
                sandbox_state.cpus = cpus
                sandbox_state.memory = memory
                sandbox_state.disk = disk
                sandbox_state.app_port = app_port
                sandbox_state.messaging_port = messaging_port
            elif mode == "config":
                assert config_cpus is not None
                assert config_memory is not None
                assert config_disk is not None
                assert config_app_port is not None
                assert config_messaging_port is not None
                sandbox_state.cpus = config_cpus
                sandbox_state.memory = config_memory
                sandbox_state.disk = config_disk
                sandbox_state.app_port = config_app_port
                sandbox_state.messaging_port = config_messaging_port

            # Save into the named slot; this also repoints .plato/state.json at
            # it and keeps this directory in the machine-wide index so
            # `list --all` and `gc` can find it from anywhere.
            self.store.save(slot_name, sandbox_state.model_dump())

            total_elapsed = time.time() - total_start
            self.console.print("")
            self.console.print(
                f"[bold green]Sandbox ready![/bold green] [dim](slot: {slot_name}, total: {total_elapsed:.1f}s)[/dim]"
            )

            return sandbox_state
        except BaseException:
            self._teardown_failed_start(slot_name, session_id, job_id, attached)
            raise

    def _teardown_failed_start(
        self,
        slot_name: str | None,
        session_id: str | None,
        job_id: str | None,
        attached: bool,
    ) -> None:
        """Undo a start that failed (or was Ctrl-C'd) after the session existed.

        Because the slot was written before anything slow happened, this is
        just the ordinary teardown: close the remote half, then run the same
        local cleanup `stop` uses. Best-effort throughout — a cleanup error
        must not replace the failure the caller actually needs to see — and
        anything it misses self-resolves: the heartbeat exits on its own once
        the slot is gone (or its lease runs out), and the next command's
        reconcile clears the rest.
        """
        self.console.print("[yellow]Start failed — cleaning up the partially created sandbox[/yellow]")
        if session_id:
            try:
                if attached and job_id:
                    # Closing the shared session would take the owning Chronos
                    # session's other envs down with it.
                    self.remove_env(session_id=session_id, job_id=job_id)
                elif not attached:
                    sessions_close.sync(client=self._http, session_id=session_id, x_api_key=self.api_key)
            except Exception as exc:
                self.console.print(
                    f"[red]Could not close session {session_id}: {exc}. "
                    f"Stop it with `plato sandbox stop --session-id {session_id}`[/red]"
                )
        if slot_name:
            with suppress(Exception):
                self.store.stop_local(slot_name, remove=True)

    def _lookup_simulator_name(self, session_id: str, job_id: str | None, attached: bool) -> str | None:
        """Our job's service name from session details (artifact mode learns it late)."""
        # Note: get_session_details returns a dict, not a Pydantic model
        session_details = get_session_details.sync(
            client=self._http,
            session_id=session_id,
            x_api_key=self.api_key,
        )
        jobs = (
            session_details.get("jobs") if isinstance(session_details, dict) else getattr(session_details, "jobs", None)
        )
        for j in jobs or []:
            if isinstance(j, dict):
                jid = j.get("job_id") or j.get("public_id")
                service = j.get("service")
            else:
                jid = getattr(j, "job_id", None) or getattr(j, "public_id", None)
                service = getattr(j, "service", None)
            if attached:
                # A shared session has other envs, so "first job with a
                # service" would pick someone else's — match ours by id.
                if jid == job_id and service:
                    return str(service)
            elif service:
                return str(service)
        return None

    def enable_manual_control(self, state: SandboxState, wait_seconds: int = 300) -> str:
        """Prepare a Windows (qemu) sandbox for a human RDP session.

        Windows sandbox images auto-logon the agent user at the console with
        Winlogon ``ForceAutoLogon=1`` so the desktop agent always has a live
        interactive session. On a client-SKU guest (one active session), that
        same setting re-logs the console back on the moment an RDP client
        takes over the session — bouncing the human off seconds after the
        "Welcome" screen. This waits until the guest is SSH-reachable, clears
        ``ForceAutoLogon`` (``AutoAdminLogon`` stays on, so boot behavior is
        unchanged), then resolves and returns the browser RDP viewer URL.

        Args:
            state: The started sandbox's state (needs SSH configured and
                provider ``qemu``).
            wait_seconds: How long to keep retrying SSH before giving up —
                snapshot-resumed Windows guests can take a while to accept
                connections.

        Returns:
            The browser RDP viewer URL for the sandbox's job.

        Raises:
            ValueError: If the sandbox is not a qemu (Windows) VM.
            RuntimeError: If SSH was never configured, the registry update
                fails on the guest, or the RDP URL lookup fails.
            TimeoutError: If the guest is not SSH-reachable in time.
        """
        assert self.api_key is not None
        if state.provider != "qemu":
            raise ValueError(
                f"--manual-control needs a Windows (qemu) VM; this sandbox's provider is {state.provider or 'unknown'}"
            )
        if not state.ssh_config_path or not state.ssh_host:
            raise RuntimeError("--manual-control needs SSH, but SSH setup did not complete for this sandbox")

        encoded = base64.b64encode(_MANUAL_CONTROL_PS.encode("utf-16-le")).decode("ascii")
        remote_cmd = f"powershell -NoProfile -EncodedCommand {encoded}"

        self.console.print("[yellow]Enabling manual control (waiting for guest SSH)...[/yellow]")
        step_start = time.time()
        deadline = step_start + wait_seconds
        while True:
            returncode, stdout, stderr = _run_ssh_command(
                state.ssh_config_path, state.ssh_host, remote_cmd, cwd=self.working_dir
            )
            if returncode == 0:
                break
            # 255 is ssh's own "could not connect / transport failed" code;
            # anything else means the command ran on the guest and failed.
            if returncode != 255:
                raise RuntimeError(
                    f"manual-control registry update failed on the guest (exit {returncode}): "
                    f"{stderr.strip() or stdout.strip()}"
                )
            if time.time() >= deadline:
                raise TimeoutError(f"guest not SSH-reachable within {wait_seconds}s; last ssh error: {stderr.strip()}")
            time.sleep(5)

        elapsed = time.time() - step_start
        self.console.print(
            f"[green]Manual control enabled:[/green] console auto-logon reclaim disabled "
            f"(ForceAutoLogon=0) [dim]({elapsed:.1f}s)[/dim]"
        )

        rdp_response = jobs_rdp_url.sync(client=self._http, job_id=state.job_id, x_api_key=self.api_key)
        if not rdp_response.success or not rdp_response.url:
            raise RuntimeError(f"RDP URL lookup failed for job {state.job_id}: {rdp_response.error}")
        state.rdp_url = rdp_response.url
        if state.name:
            with suppress(Exception):
                self.store.update(state.name, rdp_url=rdp_response.url)
        self.console.print(f"[bold green]RDP URL:[/bold green] {rdp_response.url}")
        return rdp_response.url

    def pull_config(self, artifact_id: str, dataset: str) -> dict[str, bool]:
        """Download plato-config.yml and flows.yml from the artifact API.

        Fetches the config files stored in the artifact so they can be
        edited locally and applied via start-worker / sandbox flow.

        Returns:
            Dict with ``plato_config_written`` and ``flows_written`` booleans.
        """
        result = {"plato_config_written": False, "flows_written": False}

        # Pull plato-config.yml
        try:
            plato_config_resp = simulator_get_plato_config.sync(
                client=self._http,
                artifact_id=artifact_id,
                x_api_key=self.api_key,
            )
            if plato_config_resp.plato_config:
                config_path = self.working_dir / "plato-config.yml"
                config_path.write_text(plato_config_resp.plato_config)
                self.console.print("[green]Downloaded:[/green] plato-config.yml")
                result["plato_config_written"] = True
            else:
                self.console.print("[dim]No plato-config found in artifact[/dim]")
        except Exception as e:
            self.console.print(f"[dim]Failed to download plato-config.yml: {e}[/dim]")

        # Pull flows.yml
        try:
            flows_resp = simulator_get_env_flows.sync(
                client=self._http,
                artifact_id=artifact_id,
                x_api_key=self.api_key,
            )
            if flows_resp:
                # Read flows_path from plato-config to determine where to write
                flows_path = "base/flows.yml"
                config_path = self.working_dir / "plato-config.yml"
                if config_path.exists():
                    try:
                        with open(config_path) as f:
                            pc = yaml.safe_load(f)
                        ds = pc.get("datasets", {}).get(dataset, {})
                        meta = ds.get("metadata", {})
                        if meta.get("flows_path"):
                            flows_path = meta["flows_path"]
                    except Exception:
                        pass

                # Sanitize flows_path to prevent writing outside working_dir
                candidate = (self.working_dir / flows_path).resolve()
                working_dir_resolved = self.working_dir.resolve()
                if not (candidate == working_dir_resolved or working_dir_resolved in candidate.parents):
                    self.console.print(
                        f"[yellow]Warning:[/yellow] flows_path {flows_path!r} resolves outside working_dir, "
                        "using default 'base/flows.yml'"
                    )
                    flows_path = "base/flows.yml"
                    candidate = (self.working_dir / flows_path).resolve()

                candidate.parent.mkdir(parents=True, exist_ok=True)

                # Normalize API response to {"flows": [list of flow dicts]}
                # API may return a list of flows or a dict with a "flows" key
                if isinstance(flows_resp, list):
                    flows_data = {"flows": flows_resp}
                elif isinstance(flows_resp, dict) and "flows" in flows_resp:
                    flows_data = flows_resp
                else:
                    flows_data = {"flows": [flows_resp] if isinstance(flows_resp, dict) else flows_resp}

                flows_yaml = yaml.dump(flows_data, default_flow_style=False, sort_keys=False)
                candidate.write_text(flows_yaml)
                self.console.print(f"[green]Downloaded:[/green] {flows_path}")
                result["flows_written"] = True
            else:
                self.console.print("[dim]No flows found in artifact[/dim]")
        except Exception as e:
            self.console.print(f"[dim]Failed to download flows: {e}[/dim]")

        return result

    def reset(self, session_id: str) -> ResetSessionResponse:
        """Reset all jobs in a session to initial state."""
        return sessions_reset.sync(
            client=self._http,
            session_id=session_id,
            body=ResetSessionRequest(),
            x_api_key=self.api_key,
        )

    def reset_job(self, job_id: str) -> ResetJobResult:
        """Reset a single job (attached sandboxes — leaves the shared session's other envs alone)."""
        return jobs_reset.sync(
            client=self._http,
            job_id=job_id,
            body=ResetSessionRequest(),
            x_api_key=self.api_key,
        )

    # CHECKED
    def stop(
        self,
        session_id: str,
        heartbeat_pid: int | None = None,
    ) -> CloseSessionResponse:
        """Close the session, then stop its heartbeat.

        In that order: killing the heartbeat first means a transient failure to
        close leaves a VM that is still running with nothing keeping it alive,
        so it dies ~2 minutes later for reasons the caller never sees.
        """
        response = sessions_close.sync(
            client=self._http,
            session_id=session_id,
            x_api_key=self.api_key,
        )
        if heartbeat_pid:
            stop_heartbeat(heartbeat_pid)
        return response

    def remove_env(self, session_id: str, job_id: str) -> RemoveJobResponse:
        """Remove one env's job from a shared session without closing it.

        This is the stop path for attached sandboxes — closing the session
        would take down the owning Chronos session's other envs.
        """
        return sessions_remove_job.sync(
            client=self._http,
            session_id=session_id,
            body=RemoveJobRequest(job_id=job_id),
            x_api_key=self.api_key,
        )

    def cleanup_slot(self, name: str, remove: bool = False) -> dict[str, bool]:
        """Local teardown after a sandbox has been stopped remotely.

        Delegates to :meth:`SandboxStore.stop_local` — the one local-teardown
        path shared by ``stop``, ``--force``, slot reuse, failed starts and
        ``gc``.
        """
        return self.store.stop_local(name, remove=remove)

    # CHECKED
    def status(self, session_id: str) -> SessionDetailsResponse:
        return get_session_details.sync(
            client=self._http,
            session_id=session_id,
            x_api_key=self.api_key,
        )

    def _build_checkpoint_request(
        self,
        mode: str | None,
        dataset: str | None,
        target: str | None = None,
        mcp: ArtifactMcpConfig | None = None,
    ) -> CreateCheckpointRequest:
        """Build the checkpoint payload; config mode packs local plato-config.yml + flows.

        ``target`` is the routing domain stored on the artifact (e.g.
        ``grist.web.plato.so``); the proxy serves the artifact under it instead
        of the sims.plato.so fallback. Independent of ``mode``; when omitted the
        backend inherits the parent artifact's target.

        ``mcp`` is the artifact-level MCP endpoint config (enabled/port/path),
        which overrides the simulator's field by field. Also independent of
        ``mode``; when omitted — or when every one of its fields is unset — it
        is left off the request and the backend inherits the parent artifact's.
        """
        checkpoint_request = CreateCheckpointRequest()
        if target:
            checkpoint_request.target = target
            self.console.print(f"[dim]Artifact target: {target}[/dim]")

        if mcp is not None:
            # An all-unset config is not an override: omit it so the backend inherits the
            # parent artifact's, matching what mcp_config_from_flags returns for no flags.
            if mcp.model_dump(exclude_none=True):
                checkpoint_request.mcp_config = mcp
            self.console.print(f"[dim]Artifact MCP: {describe_mcp_config(mcp)}[/dim]")

        if mode == "config":
            if not dataset:
                raise ValueError("dataset is required for config-mode snapshots")
            # read plato-config.yml - need parsed for extracting values
            plato_config_path = self.working_dir / "plato-config.yml"
            plato_config_raw = plato_config_path.read_text()
            plato_config = yaml.safe_load(plato_config_raw)

            # Validate through the generated backend-schema model, not the v1 PlatoConfig
            # (see dataset_config_from_plato_config). exclude_unset stores exactly what
            # the file says, without the generated model's defaults leaking in.
            dataset_config = dataset_config_from_plato_config(plato_config, dataset, source=str(plato_config_path))
            dataset_dict = dataset_config.model_dump(exclude_unset=True, by_alias=True, mode="json")
            checkpoint_request.plato_config = yaml.dump(dataset_dict, default_flow_style=False)

            dataset_compute = dataset_config.compute
            checkpoint_request.internal_app_port = dataset_compute.app_port
            checkpoint_request.messaging_port = dataset_compute.plato_messaging_port
            # we dont set target

            # Override service name if specified in plato-config.yml
            service_name = plato_config.get("service") if isinstance(plato_config, dict) else None
            if service_name:
                checkpoint_request.override_service = str(service_name)

            # Read flows from the path specified in plato-config metadata
            # API expects YAML string, not parsed dict
            # Only set flows if file exists AND has content, otherwise leave as None to inherit from parent
            dataset_metadata = dataset_config.metadata
            flows_file_path = dataset_metadata.flows_path if dataset_metadata else None
            if flows_file_path:
                # flows_path is relative to working_dir
                flows_path = self.working_dir / flows_file_path
                if flows_path.exists():
                    flows_content = flows_path.read_text().strip()
                    if flows_content:
                        checkpoint_request.flows = flows_content
                else:
                    self.console.print(f"[yellow]Warning: flows file not found at {flows_path}[/yellow]")

            # Structured login credentials travel with the flows they belong to.
            checkpoint_request.credentials = credentials_from_dataset_config(dataset_config)
            self.console.print(
                f"[dim]Artifact credentials: {describe_credentials(checkpoint_request.credentials)}[/dim]"
            )

        return checkpoint_request

    # CHECKED
    def snapshot(
        self,
        session_id: str,
        mode: str,
        dataset: str,
        target: str | None = None,
        mcp: ArtifactMcpConfig | None = None,
    ) -> AppApiV2SchemasSessionCreateSnapshotResponse:
        checkpoint_request = self._build_checkpoint_request(mode, dataset, target, mcp)

        response = sessions_snapshot.sync(
            client=self._http,
            session_id=session_id,
            body=checkpoint_request,
            x_api_key=self.api_key,
        )

        # Save artifact_id to the sandbox slot so it can be retrieved via `plato sandbox status`
        if response.results:
            # Get the first successful artifact_id from results
            for job_id, result in response.results.items():
                if result.success and result.artifact_id:
                    self._record_artifact_id(result.artifact_id)

                    # Prefetch snapshot to all workers so VMs can boot from it immediately
                    self.console.print("[cyan]Prefetching snapshot to workers...[/cyan]")
                    try:
                        prefetch_snapshot.sync(
                            client=self._http,
                            body=PrefetchRequest(artifact_id=result.artifact_id),
                            x_api_key=self.api_key,
                        )
                        self.console.print("[green]Prefetch dispatched to workers[/green]")
                    except Exception as e:
                        self.console.print(f"[yellow]Prefetch failed (non-fatal): {e}[/yellow]")

                    break

        return response

    def _record_artifact_id(self, artifact_id: str) -> None:
        """Record a fresh artifact on the sandbox slot this client is driving."""
        name = self.store.resolve(self.sandbox_name)
        if name and self.store.load(name) is not None:
            self.store.update(name, artifact_id=artifact_id)

    def _record_and_prefetch_artifact(self, artifact_id: str) -> None:
        """Save artifact_id to the sandbox slot and prefetch it to workers."""
        self._record_artifact_id(artifact_id)

        self.console.print("[cyan]Prefetching snapshot to workers...[/cyan]")
        try:
            prefetch_snapshot.sync(
                client=self._http,
                body=PrefetchRequest(artifact_id=artifact_id),
                x_api_key=self.api_key,
            )
            self.console.print("[green]Prefetch dispatched to workers[/green]")
        except Exception as e:
            self.console.print(f"[yellow]Prefetch failed (non-fatal): {e}[/yellow]")

    def snapshot_job_full(
        self,
        job_id: str,
        mode: str | None = None,
        dataset: str | None = None,
        target: str | None = None,
        mcp: ArtifactMcpConfig | None = None,
    ) -> CreateSnapshotResult:
        """Full snapshot (disk + memory) of a single job — the per-job
        analog of the session-level snapshot.

        This is what attached sandboxes use: it creates a base artifact even
        for from-scratch (config/blank) VMs, without snapshotting the shared
        session's other envs. Contrast with :meth:`snapshot_job`, which is a
        lightweight *checkpoint* and requires an artifact-resumed VM.
        ``mode="config"`` packs the local plato-config.yml + flows just like
        the session-level snapshot.
        """
        checkpoint_request = self._build_checkpoint_request(mode, dataset, target, mcp)
        snapshot_request = AppApiV2SchemasSessionCreateSnapshotRequest(
            **checkpoint_request.model_dump(exclude_none=True)
        )
        response = jobs_snapshot.sync(
            client=self._http,
            job_id=job_id,
            body=snapshot_request,
            x_api_key=self.api_key,
        )

        if response.success and response.artifact_id:
            self._record_and_prefetch_artifact(response.artifact_id)

        return response

    def snapshot_job(
        self,
        job_id: str,
        mode: str | None = None,
        dataset: str | None = None,
        target: str | None = None,
        mcp: ArtifactMcpConfig | None = None,
    ) -> CreateCheckpointResult:
        """Checkpoint a single job (one env in a multi-env session).

        Lightweight diff snapshot — the backend requires the VM to have been
        resumed from a base artifact (unified datagen's per-env case). For
        from-scratch VMs use :meth:`snapshot_job_full`. ``mode="config"``
        packs the local plato-config.yml + flows just like the session-level
        snapshot.
        """
        response = jobs_checkpoint.sync(
            client=self._http,
            job_id=job_id,
            body=self._build_checkpoint_request(mode, dataset, target, mcp),
            x_api_key=self.api_key,
        )

        if response.success and response.artifact_id:
            self._record_and_prefetch_artifact(response.artifact_id)

        return response

    # CHECKED
    def connect_network(self, session_id: str) -> dict:
        return sessions_connect_network.sync(
            client=self._http,
            session_id=session_id,
            x_api_key=self.api_key,
        )

    # CHECKED
    def start_worker(
        self,
        job_id: str,
        simulator: str,
        dataset: str,
        wait_timeout: int = 300,  # 5 minutes
        use_api: bool = False,
    ) -> None:
        dataset_config = self._load_start_worker_dataset_config(
            simulator=simulator,
            dataset=dataset,
            use_api=use_api,
        )

        _ = start_worker.sync(
            client=self._http,
            public_id=job_id,
            body=VMManagementRequest(
                service=simulator,
                dataset=dataset,
                plato_dataset_config=dataset_config,
            ),
            x_api_key=self.api_key,
        )

        if wait_timeout > 0:
            # Wait before first state poll to allow worker to initialize
            time.sleep(15)
            start_time = time.time()
            poll_interval = 10

            while time.time() - start_time < wait_timeout:
                try:
                    state_response = jobs_state.sync(
                        client=self._http,
                        job_id=job_id,
                        x_api_key=self.api_key,
                    )
                    if state_response:
                        state_dict = (
                            state_response.model_dump() if hasattr(state_response, "model_dump") else state_response
                        )
                        if isinstance(state_dict, dict) and "error" not in state_dict.get("state", {}):
                            return
                except Exception:
                    pass

                time.sleep(poll_interval)

    def _load_start_worker_dataset_config(
        self,
        simulator: str,
        dataset: str,
        use_api: bool,
    ) -> AppSchemasBuildModelsSimConfigDataset:
        raw_plato_config: object
        config_source: str

        if use_api:
            self.console.print("[cyan]Config source: API[/cyan]")
            # Use v1 simulator artifact APIs to resolve the correct simulator artifact,
            # then fetch its plato-config.yml.
            sim_info = env_get_simulator_by_name.sync(
                client=self._http,
                name=simulator,
                x_api_key=self.api_key,
            )

            versions = simulator_get_simulator_versions.sync(
                client=self._http,
                simulator_name=simulator,
                include_checkpoints=False,
                x_api_key=self.api_key,
            )

            dataset_versions = [v for v in versions.versions if v.dataset == dataset]
            if not dataset_versions:
                available_datasets = sorted({v.dataset for v in versions.versions})
                raise ValueError(
                    f"No simulator versions found for simulator='{simulator}' dataset='{dataset}'. "
                    f"Available datasets: {available_datasets}"
                )

            tag = sim_info.versionTag
            tagged_versions = [v for v in dataset_versions if tag in (v.tags or [])] if tag else []

            selected = max((tagged_versions or dataset_versions), key=lambda v: v.created_at)
            plato_config_resp = simulator_get_plato_config.sync(
                client=self._http,
                artifact_id=selected.artifact_id,
                x_api_key=self.api_key,
            )
            if not plato_config_resp.plato_config:
                raise ValueError(f"No plato_config returned for artifact_id='{selected.artifact_id}'")

            config_source = f"artifact '{selected.artifact_id}'"
            raw_plato_config = yaml.safe_load(plato_config_resp.plato_config) or {}
        else:
            config_path = self.working_dir / "plato-config.yml"
            if not config_path.exists():
                config_path = self.working_dir / "plato-config.yaml"
            if not config_path.exists():
                raise ValueError("plato-config.yml / plato-config.yaml not found in working directory")

            config_source = str(config_path)
            with open(config_path, "rb") as f:
                raw_plato_config = yaml.safe_load(f) or {}

        return dataset_config_from_plato_config(raw_plato_config, dataset, source=config_source)

    # CHECKED
    def sync(
        self,
        session_id: str,
        simulator: str,
        timeout: int = 120,
    ) -> SyncResult:
        """Sync local files to sandbox using rsync over SSH.

        Uses the SSH config from .plato/ssh_config for fast, reliable file transfer.
        """
        local_path = self.working_dir
        remote_path = f"/home/plato/worktree/{simulator}"

        # Load SSH config from state
        state = self.store.load(self.store.resolve(self.sandbox_name))
        if state is None:
            raise ValueError("No sandbox state found - run 'plato sandbox start' first")

        ssh_config_path = state.get("ssh_config_path")
        ssh_host = state.get("ssh_host", "sandbox")

        if not ssh_config_path:
            raise ValueError("No SSH config in state - run 'plato sandbox start' first")

        exclude_patterns = [
            "__pycache__",
            "*.pyc",
            ".git",
            ".venv",
            "venv",
            "node_modules",
            ".sandbox.yaml",
            "*.egg-info",
            ".pytest_cache",
            ".mypy_cache",
            ".DS_Store",
            "*.swp",
            "*.swo",
            ".plato",
        ]

        # Build rsync command
        rsync_cmd = [
            "rsync",
            "-avz",
            "--delete",
            "-e",
            f"ssh -F {ssh_config_path}",
        ]

        # Add excludes
        for pattern in exclude_patterns:
            rsync_cmd.extend(["--exclude", pattern])

        # Source and destination
        rsync_cmd.append(f"{local_path}/")
        rsync_cmd.append(f"{ssh_host}:{remote_path}/")

        self.console.print(f"[dim]rsync -> {ssh_host}:{remote_path}/[/dim]")

        # Ensure rsync is installed on the VM and create remote directory
        setup_result = subprocess.run(
            [
                "ssh",
                "-F",
                ssh_config_path,
                ssh_host,
                f"which rsync >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq rsync) && mkdir -p {remote_path}",
            ],
            capture_output=True,
            text=True,
            cwd=self.working_dir,
        )
        if setup_result.returncode != 0:
            raise ValueError(f"Failed to setup remote: {setup_result.stderr}")

        # Run rsync
        result = subprocess.run(
            rsync_cmd,
            capture_output=True,
            text=True,
            cwd=self.working_dir,
            timeout=timeout,
        )

        if result.returncode != 0:
            raise ValueError(f"rsync failed: {result.stderr}")

        # Count synced files from rsync output
        lines = result.stdout.strip().split("\n") if result.stdout else []
        file_count = len(
            [
                line
                for line in lines
                if line
                and not line.startswith("sending")
                and not line.startswith("sent")
                and not line.startswith("total")
            ]
        )

        # Get bytes from rsync output (e.g., "sent 1,234 bytes")
        bytes_synced = 0
        for line in lines:
            if "sent" in line and "bytes" in line:
                import re

                match = re.search(r"sent ([\d,]+) bytes", line)
                if match:
                    bytes_synced = int(match.group(1).replace(",", ""))
                    break

        return SyncResult(
            files_synced=file_count,
            bytes_synced=bytes_synced,
        )

    def tunnel(
        self,
        job_id: str,
        remote_port: int,
        local_port: int | None = None,
        bind_address: str = "127.0.0.1",
        mesh_ip: str | None = None,
    ) -> Tunnel:
        return Tunnel(
            job_id=job_id,
            remote_port=remote_port,
            local_port=local_port,
            bind_address=bind_address,
            mesh_ip=mesh_ip,
        )

    def get_ssh_config_for_job(self, job_id: str) -> SSHConfigInfo:
        """Get SSH config for connecting to a specific job.

        Uses a cached SSH key pair from ~/.cache/plato/ssh/, adds the
        public key to the VM via the session add_ssh_key API, and returns
        an SSH config that routes through the Plato gateway.

        Args:
            job_id: The job public ID to connect to.

        Returns:
            SSHConfigInfo with the config content, private key path, and metadata.
        """
        gateway_host = os.getenv("PLATO_GATEWAY_HOST", "gateway.plato.so")

        # Get or create cached SSH key pair
        public_key, private_key_path = _get_or_create_cached_ssh_key_pair()

        # Look up session ID + provider from job, then add SSH key via the
        # session API. ``provider`` decides the ssh User on the generated
        # config — root for firecracker/Linux, plato for QEMU/Windows.
        try:
            job_info = jobs_get_job_info.sync(
                client=self._http,
                job_id=job_id,
                x_api_key=self.api_key,
            )
            if not job_info.session_id:
                raise RuntimeError(f"Job {job_id} has no associated session")

            # ``provider`` is recent on the API. Read defensively so older
            # API rollouts still return a usable config (falls back to
            # ``root`` user, which is correct for the firecracker default).
            provider = getattr(job_info, "provider", None) or (
                job_info.model_dump().get("provider") if hasattr(job_info, "model_dump") else None
            )
            install_user = ssh_user_for_provider(provider)

            auth_path = SSH_CACHE_DIR / "authorized_sessions"
            authorized = set(auth_path.read_text().splitlines()) if auth_path.exists() else set()

            if job_info.session_id in authorized:
                logger.debug("SSH key already added to session %s, skipping", job_info.session_id)
            else:
                # ``username`` is advisory — the v2 add_ssh_key endpoint
                # ignores it for QEMU and forces ``plato`` server-side. We
                # send the right value anyway so audit logs are accurate.
                add_key_request = AddSSHKeyRequest(public_key=public_key, username=install_user)
                add_response = sessions_add_ssh_key.sync(
                    client=self._http,
                    session_id=job_info.session_id,
                    body=add_key_request,
                    x_api_key=self.api_key,
                )
                if not add_response.success:
                    raise RuntimeError("SSH key upload was not successful")
                authorized.add(job_info.session_id)
                auth_path.write_text("\n".join(authorized) + "\n")
        except Exception as e:
            raise RuntimeError(f"Failed to add SSH key to job {job_id}: {e}") from e

        # Generate SSH config keyed off the provider we discovered above.
        config_content = _generate_ssh_config_content(job_id, private_key_path, provider=provider)

        return SSHConfigInfo(
            config_content=config_content,
            private_key_path=private_key_path,
            job_id=job_id,
            gateway_host=gateway_host,
        )

    def run_audit_ui(
        self,
        job_id: str | None = None,
        dataset: str = "base",
        no_tunnel: bool = False,
        mesh_ip: str | None = None,
    ) -> None:
        import shutil

        if not shutil.which("streamlit"):
            raise ValueError("streamlit not installed. Run: pip install streamlit psycopg2-binary pymysql")

        ui_file = Path(__file__).resolve().parent.parent.parent / "cli" / "audit_ui.py"
        if not ui_file.exists():
            raise ValueError(f"UI file not found: {ui_file}")

        # Get DB listener from plato-config.yml
        db_listener: DatabaseMutationListenerConfig | None = None
        for config_path in [self.working_dir / "plato-config.yml", self.working_dir / "plato-config.yaml"]:
            if config_path.exists():
                with open(config_path) as f:
                    plato_config = PlatoConfig.model_validate(yaml.safe_load(f))
                dataset_config = plato_config.datasets.get(dataset)
                if dataset_config and dataset_config.listeners:
                    for listener in dataset_config.listeners.values():
                        if isinstance(listener, DatabaseMutationListenerConfig):
                            db_listener = listener
                            break
                break
        tunnel = None

        if db_listener and job_id and not no_tunnel:
            self.console.print(f"Starting tunnel to {db_listener.db_type} on port {db_listener.db_port}...")
            tunnel = self.tunnel(job_id, db_listener.db_port or 0, mesh_ip=mesh_ip)
            tunnel.start()
            time.sleep(1)  # Let tunnel stabilize
            self.console.print(
                f"[green]Tunnel open:[/green] localhost:{db_listener.db_port} -> VM:{db_listener.db_port}"
            )

        # Pass db config via environment variables
        env = os.environ.copy()
        if db_listener:
            env["PLATO_DB_HOST"] = "127.0.0.1"
            env["PLATO_DB_PORT"] = str(db_listener.db_port)
            env["PLATO_DB_USER"] = db_listener.db_user or ""
            env["PLATO_DB_PASSWORD"] = db_listener.db_password or ""
            env["PLATO_DB_NAME"] = db_listener.db_database or ""
            env["PLATO_DB_TYPE"] = str(db_listener.db_type)
            self.console.print(
                f"[dim]DB config: {db_listener.db_user}@127.0.0.1:{db_listener.db_port}/{db_listener.db_database}[/dim]"
            )

        try:
            subprocess.run(["streamlit", "run", str(ui_file)], env=env)
        finally:
            if tunnel:
                tunnel.stop()
                self.console.print("[yellow]Tunnel closed[/yellow]")

    def run_flow(
        self,
        url: str,
        flow_name: str,
        dataset: str,
        use_api: bool = False,
        job_id: str | None = None,
        headless: bool = False,
        keep_browser_open: bool = False,
    ) -> None:
        flow_obj: Flow | None = None
        screenshots_dir = self.working_dir / "screenshots"

        if use_api:
            # Fetch from API
            if not job_id:
                raise ValueError("job_id required when use_api=True")

            self.console.print("[cyan]Flow source: API[/cyan]")
            flows_response = jobs_get_flows.sync(
                client=self._http,
                job_id=job_id,
                x_api_key=self.api_key,
            )

            if flows_response:
                for flow_data in flows_response:
                    if isinstance(flow_data, dict):
                        if flow_data.get("name") == flow_name:
                            flow_obj = Flow.model_validate(flow_data)
                            break
                    elif hasattr(flow_data, "name") and flow_data.name == flow_name:
                        flow_obj = (
                            flow_data if isinstance(flow_data, Flow) else Flow.model_validate(flow_data.model_dump())
                        )
                        break

            if not flow_obj:
                available = [
                    f.get("name") if isinstance(f, dict) else getattr(f, "name", "?") for f in (flows_response or [])
                ]
                raise ValueError(f"Flow '{flow_name}' not found in API. Available: {available}")
        else:
            # Use local flows
            config_paths = [
                self.working_dir / "plato-config.yml",
                self.working_dir / "plato-config.yaml",
            ]

            for config_path in config_paths:
                if config_path.exists():
                    with open(config_path) as f:
                        plato_config = PlatoConfig.model_validate(yaml.safe_load(f))

                    dataset_config = plato_config.datasets.get(dataset)
                    if dataset_config and dataset_config.metadata:
                        flows_path = dataset_config.metadata.flows_path

                        if flows_path:
                            flow_file = (
                                config_path.parent / flows_path
                                if not Path(flows_path).is_absolute()
                                else Path(flows_path)
                            )

                            if flow_file.exists():
                                with open(flow_file) as f:
                                    flow_dict = yaml.safe_load(f)
                                flow_obj = next(
                                    (
                                        Flow.model_validate(fl)
                                        for fl in flow_dict.get("flows", [])
                                        if fl.get("name") == flow_name
                                    ),
                                    None,
                                )
                                if flow_obj:
                                    screenshots_dir = flow_file.parent / "screenshots"
                                    self.console.print(f"[cyan]Flow source: local ({flow_file})[/cyan]")
                                    break

            if not flow_obj:
                raise ValueError(f"Flow '{flow_name}' not found in local config")

        # Assert for type narrowing in nested function (checked above in both branches)
        assert flow_obj is not None
        validated_flow: Flow = flow_obj

        # Run the flow with Playwright
        async def _run_flow():
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=headless)
                try:
                    page = await browser.new_page()
                    await page.goto(url)
                    executor = FlowExecutor(page, validated_flow, screenshots_dir)
                    await executor.execute()
                    if keep_browser_open:
                        self.console.print("[yellow]Browser kept open. Press Ctrl+C to close.[/yellow]")
                        try:
                            while True:
                                await asyncio.sleep(1)
                        except KeyboardInterrupt:
                            pass
                finally:
                    await browser.close()

        asyncio.get_event_loop().run_until_complete(_run_flow())

    # CHECKED
    def state(self, session_id: str) -> SessionStateResponse:
        response = sessions_state.sync(
            client=self._http,
            session_id=session_id,
            merge_mutations=True,
            x_api_key=self.api_key,
        )
        return response

    def state_job(self, job_id: str) -> SessionStateResult:
        """Get one job's state (attached sandboxes — the session-level call
        would return every env's mutations in the shared session)."""
        return jobs_state.sync(
            client=self._http,
            job_id=job_id,
            merge_mutations=True,
            x_api_key=self.api_key,
        )

    def clear_audit(
        self,
        job_group_id: str,
        job_id: str | None = None,
        simulator_name: str | None = None,
        job_scoped: bool = False,
        mesh_ip: str | None = None,
    ) -> EnvCleanupResponse:
        """Clear audit_log tables in the sandbox database(s).

        Tries POST /api/v1/env/{id}/cleanup first. That endpoint requires a
        simulator attached to the job_group; chronos-managed sessions
        (datagen) restore envs from artifacts via EnvFromArtifact and never
        attach one, so the call returns 404 "Simulator not found". When that
        happens, fall back to opening a TCP tunnel to each env's DB and
        TRUNCATE'ing audit_log directly via DatabaseCleaner — which only
        needs job_id + artifact-derived db_config, no server-side simulator
        lookup.

        Args:
            job_group_id: Session id (same as job_group_id for v2 sessions).
            job_id: Per-env job id, used for the tunnel fallback.
            simulator_name: Used to resolve the artifact for db_config lookup.
            job_scoped: Skip the job-group cleanup and go straight to the
                per-job tunnel path. Attached sandboxes must set this — their
                job_group is the shared session, and the group cleanup would
                truncate audit_log on every sibling env.
            mesh_ip: Mesh IP of the env's VM; when set the DB cleanup tunnel
                goes mesh-direct instead of via the TLS gateway.
        """
        if job_scoped:
            server_err = "job-group cleanup skipped (attached sandbox — group is the shared session)"
        else:
            try:
                resp = env_cleanup.sync(
                    client=self._http,
                    job_group_id=job_group_id,
                    x_api_key=self.api_key,
                )
                if resp.success:
                    return resp
                server_err = resp.error or "env_cleanup returned success=false"
            except Exception as e:
                server_err = str(e)

        if not job_id or not simulator_name:
            return EnvCleanupResponse(
                success=False,
                error=f"server cleanup failed ({server_err}); job_id/simulator_name required for tunnel fallback",
            )

        from plato._generated.api.v1.simulator import get_db_config
        from plato._generated.api.v1.simulator.get_simulator_by_name import (
            sync as get_sim_sync,
        )
        from plato.v2.utils.db_cleanup import DatabaseCleaner
        from plato.v2.utils.models import EnvironmentInfo

        sim = get_sim_sync(client=self._http, simulator_name=simulator_name, x_api_key=self.api_key)
        sim_config = (sim or {}).get("config", {}) if isinstance(sim, dict) else {}
        artifact_id = sim_config.get("base_artifact_id") or sim_config.get("data_artifact_id")
        if not artifact_id:
            return EnvCleanupResponse(
                success=False,
                error=f"no base_artifact_id/data_artifact_id on simulator '{simulator_name}'",
            )

        db_configs = get_db_config.sync(
            client=self._http,
            artifact_id=artifact_id,
            x_api_key=self.api_key,
        )
        if not db_configs:
            return EnvCleanupResponse(
                success=False,
                error=f"no db configs returned for artifact {artifact_id}",
            )

        async def _noop():
            return None

        env_info = EnvironmentInfo(
            job_id=job_id,
            alias=simulator_name,
            artifact_id=artifact_id,
            mesh_ip=mesh_ip,
            get_state_fn=_noop,
        )

        assert self.api_key is not None
        api_key: str = self.api_key

        async def _run():
            async with httpx.AsyncClient(
                base_url=self._http.base_url,
                timeout=httpx.Timeout(120.0),
            ) as ac:
                return await DatabaseCleaner().cleanup_session(
                    envs=[env_info],
                    http_client=ac,
                    api_key=api_key,
                )

        result = asyncio.run(_run())
        failures = []
        for alias, env_result in (result.environments or {}).items():
            for db_name, db_result in (env_result.databases or {}).items():
                if not db_result.success:
                    failures.append(f"{alias}/{db_name}: {db_result.error}")
        if failures:
            return EnvCleanupResponse(success=False, error="; ".join(failures))
        return EnvCleanupResponse(success=True)

    # CHECKED
    def start_services(
        self,
        simulator_name: str,
        ssh_config_path: str,
        ssh_host: str,
        dataset: str,
    ) -> list[dict[str, str]]:
        # Get Gitea credentials
        creds = get_gitea_credentials.sync(client=self._http, x_api_key=self.api_key)

        # Get accessible simulators
        simulators = get_accessible_simulators.sync(client=self._http, x_api_key=self.api_key)
        simulator = None
        for sim in simulators:
            sim_name = sim.get("name") if isinstance(sim, dict) else getattr(sim, "name", None)
            if sim_name and sim_name.lower() == simulator_name.lower():
                simulator = sim
                break
        if not simulator:
            raise ValueError(f"Simulator '{simulator_name}' not found in gitea accessible simulators")

        # Get or create repo
        sim_id = simulator.get("id") if isinstance(simulator, dict) else getattr(simulator, "id", None)
        has_repo = simulator.get("has_repo") if isinstance(simulator, dict) else getattr(simulator, "has_repo", False)
        if has_repo:
            repo = get_simulator_repository.sync(client=self._http, simulator_id=sim_id, x_api_key=self.api_key)  # type: ignore
        else:
            repo = create_simulator_repository.sync(client=self._http, simulator_id=sim_id, x_api_key=self.api_key)  # type: ignore

        clone_url = repo.clone_url
        if not clone_url:
            raise ValueError("No clone URL available for gitea repository")

        # Build authenticated URL
        encoded_username = quote(creds.username, safe="")
        encoded_password = quote(creds.password, safe="")
        auth_clone_url = clone_url.replace("https://", f"https://{encoded_username}:{encoded_password}@", 1)

        repo_dir = f"/home/plato/worktree/{simulator_name}"
        branch_name = f"workspace-{int(time.time())}"

        # Clone, copy, push
        with tempfile.TemporaryDirectory(prefix="plato-hub-") as temp_dir:
            temp_repo = Path(temp_dir) / "repo"
            git_env = os.environ.copy()
            git_env["GIT_TERMINAL_PROMPT"] = "0"
            git_env["GIT_ASKPASS"] = ""

            subprocess.run(
                ["git", "clone", auth_clone_url, str(temp_repo)], capture_output=True, env=git_env, check=True
            )
            subprocess.run(
                ["git", "checkout", "-b", branch_name], cwd=temp_repo, capture_output=True, env=git_env, check=True
            )

            # Copy files
            current_dir = Path(self.working_dir)

            def _copy_files(src_dir: Path, dst_dir: Path) -> None:
                """Copy files, skipping .git/ and .plato-hub.json."""
                for src_path in src_dir.rglob("*"):
                    rel_path = src_path.relative_to(src_dir)
                    if ".git" in rel_path.parts or rel_path.name == ".plato-hub.json":
                        continue
                    dst_path = dst_dir / rel_path
                    if src_path.is_dir():
                        dst_path.mkdir(parents=True, exist_ok=True)
                    else:
                        dst_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_path, dst_path)

            _copy_files(current_dir, temp_repo)

            subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True, env=git_env)
            result = subprocess.run(
                ["git", "status", "--porcelain"], cwd=temp_repo, capture_output=True, text=True, env=git_env
            )

            if result.stdout.strip():
                subprocess.run(
                    ["git", "commit", "-m", "Sync from local workspace"],
                    cwd=temp_repo,
                    capture_output=True,
                    env=git_env,
                )

            subprocess.run(
                ["git", "remote", "set-url", "origin", auth_clone_url],
                cwd=temp_repo,
                capture_output=True,
                env=git_env,
            )
            subprocess.run(
                ["git", "push", "-u", "origin", branch_name],
                cwd=temp_repo,
                capture_output=True,
                env=git_env,
                check=True,
            )

        # Clone on VM - first verify SSH works
        # Debug: show SSH config being used
        ssh_config_full_path = (
            Path(self.working_dir) / ssh_config_path
            if not Path(ssh_config_path).is_absolute()
            else Path(ssh_config_path)
        )
        if not ssh_config_full_path.exists():
            raise ValueError(f"SSH config file not found: {ssh_config_full_path}")

        self.console.print(f"[dim]SSH config: {ssh_config_full_path}[/dim]")
        self.console.print(f"[dim]SSH host: {ssh_host}[/dim]")

        # Run SSH with verbose to see what's happening
        ssh_cmd = ["ssh", "-v", "-F", ssh_config_path, ssh_host, "echo 'SSH connection OK'"]
        self.console.print(f"[dim]Running: {' '.join(ssh_cmd)}[/dim]")
        self.console.print(f"[dim]Working dir: {self.working_dir}[/dim]")

        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            cwd=self.working_dir,
        )
        ret, stdout, stderr = result.returncode, result.stdout, result.stderr

        if ret != 0:
            # Show SSH config contents for debugging
            try:
                config_content = ssh_config_full_path.read_text()
                self.console.print(f"[yellow]SSH config contents:[/yellow]\n{config_content}")
            except Exception:
                pass
            # Show SSH verbose output
            self.console.print(f"[yellow]SSH stderr (verbose):[/yellow]\n{stderr}")
            error_output = stderr or stdout or "(no output)"
            raise ValueError(f"SSH connection failed (exit {ret})")

        _run_ssh_command(ssh_config_path, ssh_host, "mkdir -p /home/plato/worktree", cwd=self.working_dir)
        _run_ssh_command(ssh_config_path, ssh_host, f"rm -rf {repo_dir}", cwd=self.working_dir)

        # Clone repo - mask credentials in error output
        ret, stdout, stderr = _run_ssh_command(
            ssh_config_path,
            ssh_host,
            f"git clone -b {branch_name} {auth_clone_url} {repo_dir}",
            cwd=self.working_dir,
        )
        if ret != 0:
            # Mask credentials in error output
            safe_url = clone_url  # Use non-authenticated URL in error
            error_output = stderr or stdout or "(no output)"
            error_output = error_output.replace(creds.username, "***").replace(creds.password, "***")
            raise ValueError(f"Clone failed (exit {ret}) for {safe_url} branch {branch_name}: {error_output}")

        # ECR auth (optional - skip if aws CLI unavailable)
        try:
            ecr_result = subprocess.run(
                ["aws", "ecr", "get-login-password", "--region", "us-west-1"], capture_output=True, text=True
            )
        except (PermissionError, FileNotFoundError):
            ecr_result = None
        if ecr_result and ecr_result.returncode == 0:
            ecr_token = ecr_result.stdout.strip()
            ecr_registry = "383806609161.dkr.ecr.us-west-1.amazonaws.com"
            _run_ssh_command(
                ssh_config_path,
                ssh_host,
                f"echo '{ecr_token}' | docker login --username AWS --password-stdin {ecr_registry}",
                cwd=self.working_dir,
            )

        # Start services
        services_started = []
        with open(self.working_dir / "plato-config.yml", "rb") as f:
            plato_config = yaml.safe_load(f)
        plato_config_model = PlatoConfig.model_validate(plato_config)
        services_config = plato_config_model.datasets[dataset].services
        if not services_config:
            self.console.print("[yellow]No services configured, skipping service startup[/yellow]")
            return services_started
        for svc_name, svc_config in services_config.items():
            # svc_config is a Pydantic model (DockerComposeServiceConfig), use getattr
            svc_type = getattr(svc_config, "type", "")
            if svc_type == "docker-compose":
                compose_file = getattr(svc_config, "file", "docker-compose.yml")
                compose_cmd = f"cd {repo_dir} && docker compose -f {compose_file} up -d"
                ret, _, stderr = _run_ssh_command(ssh_config_path, ssh_host, compose_cmd, cwd=self.working_dir)
                if ret != 0:
                    raise ValueError(f"Failed to start {svc_name}: {stderr}")
                services_started.append({"name": svc_name, "type": "docker-compose", "file": compose_file})
            else:
                raise ValueError(f"Unsupported service type: {svc_type}")

        return services_started

    # # -------------------------------------------------------------------------
    # # RUN FLOW
    # # -------------------------------------------------------------------------

    # def clear_audit(
    #     self,
    #     job_id: str,
    #     session_id: str | None = None,
    #     db_listeners: list[tuple[str, dict]] | None = None,
    # ) -> ClearAuditResult:
    #     """Clear audit_log tables in sandbox databases.

    #     Args:
    #         job_id: Job ID for the sandbox.
    #         session_id: Session ID for refreshing state cache.
    #         db_listeners: List of (name, config) tuples for database listeners.

    #     Returns:
    #         ClearAuditResult with cleanup status.
    #     """
    #     if not db_listeners:
    #         return ClearAuditResult(success=False, error="No database listeners provided")

    #     def _execute_db_cleanup(name: str, db_config: dict, local_port: int) -> dict:
    #         """Execute DB cleanup using sync SQLAlchemy."""
    #         db_type = db_config.get("db_type", "postgresql").lower()
    #         db_user = db_config.get("db_user", "postgres" if db_type == "postgresql" else "root")
    #         db_password = db_config.get("db_password", "")
    #         db_database = db_config.get("db_database", "postgres")

    #         user = quote_plus(db_user)
    #         password = quote_plus(db_password)
    #         database = quote_plus(db_database)

    #         if db_type == "postgresql":
    #             db_url = f"postgresql+psycopg2://{user}:{password}@127.0.0.1:{local_port}/{database}"
    #         elif db_type in ("mysql", "mariadb"):
    #             db_url = f"mysql+pymysql://{user}:{password}@127.0.0.1:{local_port}/{database}"
    #         else:
    #             return {"listener": name, "success": False, "error": f"Unsupported db_type: {db_type}"}

    #         engine = create_engine(db_url, pool_pre_ping=True)
    #         tables_truncated = []

    #         with engine.begin() as conn:
    #             if db_type == "postgresql":
    #                 result = conn.execute(
    #                     text("SELECT schemaname, tablename FROM pg_tables WHERE tablename = 'audit_log'")
    #                 )
    #                 tables = result.fetchall()
    #                 for schema, table in tables:
    #                     conn.execute(text(f"TRUNCATE TABLE {schema}.{table} RESTART IDENTITY CASCADE"))
    #                     tables_truncated.append(f"{schema}.{table}")
    #             elif db_type in ("mysql", "mariadb"):
    #                 result = conn.execute(
    #                     text(
    #                         "SELECT table_schema, table_name FROM information_schema.tables "
    #                         "WHERE table_name = 'audit_log' AND table_schema = DATABASE()"
    #                     )
    #                 )
    #                 tables = result.fetchall()
    #                 conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    #                 for schema, table in tables:
    #                     conn.execute(text(f"DELETE FROM `{table}`"))
    #                     tables_truncated.append(table)
    #                 conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    #         engine.dispose()
    #         return {"listener": name, "success": True, "tables_truncated": tables_truncated}

    #     async def clear_audit_via_tunnel(name: str, db_config: dict) -> dict:
    #         """Clear audit_log by connecting via proxy tunnel."""
    #         db_type = db_config.get("db_type", "postgresql").lower()
    #         db_port = db_config.get("db_port", 5432 if db_type == "postgresql" else 3306)

    #         local_port = find_free_port()
    #         tunnel = ProxyTunnel(
    #             env_id=job_id,
    #             db_port=db_port,
    #             temp_password="newpass",
    #             host_port=local_port,
    #         )

    #         try:
    #             await tunnel.start()
    #             result = await asyncio.to_thread(_execute_db_cleanup, name, db_config, local_port)
    #             return result
    #         except Exception as e:
    #             return {"listener": name, "success": False, "error": str(e)}
    #         finally:
    #             await tunnel.stop()

    #     async def run_all():
    #         tasks = [clear_audit_via_tunnel(name, db_config) for name, db_config in db_listeners]
    #         return await asyncio.gather(*tasks)

    #     try:
    #         results = asyncio.run(run_all())

    #         # Refresh state cache
    #         if session_id:
    #             try:
    #                 sessions_state.sync(
    #                     client=self._http,
    #                     session_id=session_id,
    #                     x_api_key=self.api_key,
    #                 )
    #             except Exception:
    #                 pass

    #         all_success = all(r["success"] for r in results)
    #         return ClearAuditResult(success=all_success, results=list(results))

    #     except Exception as e:
    #         return ClearAuditResult(success=False, error=str(e))
