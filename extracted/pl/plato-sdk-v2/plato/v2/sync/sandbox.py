"""Plato SDK v2 - Synchronous Sandbox Client.

The SandboxClient provides methods for sandbox development workflows:
creating sandboxes, managing SSH, syncing files, running flows, etc.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import shutil
import signal
import subprocess
import tempfile
import time
from pathlib import Path
from urllib.parse import quote

import httpx
import yaml
from pydantic import BaseModel
from rich.console import Console

from plato._generated.api.v1.cluster import prefetch_snapshot
from plato._generated.api.v1.env import cleanup as env_cleanup
from plato._generated.api.v1.gitea import (
    create_simulator_repository,
    get_accessible_simulators,
    get_gitea_credentials,
    get_simulator_repository,
)
from plato._generated.api.v1.sandbox import start_worker
from plato._generated.api.v2.jobs import get_flows as jobs_get_flows
from plato._generated.api.v2.jobs import state as jobs_state
from plato._generated.api.v2.sessions import add_ssh_key as sessions_add_ssh_key
from plato._generated.api.v2.sessions import close as sessions_close
from plato._generated.api.v2.sessions import connect_network as sessions_connect_network
from plato._generated.api.v2.sessions import get_public_url as sessions_get_public_url
from plato._generated.api.v2.sessions import get_session_details
from plato._generated.api.v2.sessions import snapshot as sessions_snapshot
from plato._generated.api.v2.sessions import state as sessions_state
from plato._generated.models import (
    AddSSHKeyRequest,
    AppApiV2SchemasSessionCreateSnapshotResponse,
    AppSchemasBuildModelsSimConfigDataset,
    CloseSessionResponse,
    CreateCheckpointRequest,
    DatabaseMutationListenerConfig,
    EnvCleanupResponse,
    Flow,
    PlatoConfig,
    PrefetchRequest,
    SessionDetailsResponse,
    SessionStateResponse,
    VMManagementRequest,
)
from plato.v2.async_.flow_executor import FlowExecutor
from plato.v2.models import SandboxState
from plato.v2.types import Env, EnvFromArtifact, EnvFromResource, EnvFromSimulator, SimConfigCompute

logger = logging.getLogger(__name__)


SSH_CACHE_DIR = Path.home() / ".cache" / "plato" / "ssh"
DEFAULT_BASE_URL = "https://plato.so"
DEFAULT_TIMEOUT = 600.0


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
) -> str:
    """Generate SSH config file for easy access via gateway.

    Args:
        job_id: The job ID for routing.
        private_key_path: Path to private key (absolute or relative).
        working_dir: Working directory for .plato/.
        ssh_host: Host alias in config.

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

    config_content = f"""# Plato Sandbox SSH Config
# Generated for job: {job_id}
# NOTE: Run SSH commands from workspace root for relative paths to resolve

Host {ssh_host}
    HostName {job_id}
    User root
    IdentityFile {relative_key_path}
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
    ProxyCommand openssl s_client -quiet -connect {gateway_host}:443 -servername {sni} 2>/dev/null
"""

    plato_dir = _get_plato_dir(working_dir)
    plato_dir.mkdir(mode=0o700, exist_ok=True)

    config_path = plato_dir / "ssh_config"
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


# =============================================================================
# HEARTBEAT UTILITIES
# =============================================================================


def _start_heartbeat_process(session_id: str, api_key: str) -> int | None:
    """Start a background process that sends heartbeats.

    Uses only stdlib (urllib) to work on any machine without dependencies.

    Returns:
        PID of the background process, or None if failed.
    """
    log_file = f"/tmp/plato_heartbeat_{session_id}.log"
    base_url = os.getenv("PLATO_BASE_URL", "https://plato.so")
    # Strip trailing /api if present to avoid double /api/api in URL
    if base_url.endswith("/api"):
        base_url = base_url[:-4]
    base_url = base_url.rstrip("/")

    # Use only stdlib - no external dependencies
    heartbeat_script = f'''
import time
import json
import urllib.request
import urllib.error
from datetime import datetime

session_id = "{session_id}"
api_key = "{api_key}"
base_url = "{base_url}"
log_file = "{log_file}"

def log(msg):
    timestamp = datetime.now().isoformat()
    with open(log_file, "a") as f:
        f.write(f"[{{timestamp}}] {{msg}}\\n")
        f.flush()

log(f"Heartbeat process started for session {{session_id}}")
log(f"URL: {{base_url}}/api/v2/sessions/{{session_id}}/heartbeat")

heartbeat_count = 0
while True:
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
    except urllib.error.HTTPError as e:
        log(f"Heartbeat #{{heartbeat_count}}: HTTP {{e.code}} - {{e.reason}}")
    except Exception as e:
        log(f"Heartbeat #{{heartbeat_count}} EXCEPTION: {{type(e).__name__}}: {{e}}")
    time.sleep(30)
'''

    try:
        process = subprocess.Popen(
            ["python3", "-c", heartbeat_script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
        return process.pid
    except Exception:
        return None


def _stop_heartbeat_process(pid: int) -> bool:
    """Stop the heartbeat process.

    Returns:
        True if stopped successfully.
    """
    try:
        os.kill(pid, signal.SIGTERM)
        return True
    except ProcessLookupError:
        return True
    except Exception:
        return False


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
        logger.info("Reusing cached SSH key pair at %s", private_key_path)
        return public_key_path.read_text().strip(), str(private_key_path)

    # Clean partial state + stale session cache before regenerating
    for p in (private_key_path, public_key_path, SSH_CACHE_DIR / "authorized_sessions"):
        p.unlink(missing_ok=True)

    logger.info("Generating new SSH key pair at %s", private_key_path)
    subprocess.run(
        ["ssh-keygen", "-t", "ed25519", "-f", str(private_key_path), "-N", "", "-q"],
        check=True,
    )

    return public_key_path.read_text().strip(), str(private_key_path)


def _generate_ssh_config_content(job_id: str, private_key_path: str) -> str:
    """Generate SSH config content for a job.

    Args:
        job_id: The job ID for routing.
        private_key_path: Path to private key.

    Returns:
        SSH config content as a string.
    """
    gateway_host = os.getenv("PLATO_GATEWAY_HOST", "gateway.plato.so")

    # SNI format: {job_id}--{port}.{gateway_host}
    ssh_port = 22
    sni = f"{job_id}--{ssh_port}.{gateway_host}"

    config_content = f"""# Plato SSH Config for job: {job_id}
# Generated dynamically for -J/--job-id option

Host sandbox
    HostName {job_id}
    User root
    IdentityFile {private_key_path}
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
    ProxyCommand openssl s_client -quiet -connect {gateway_host}:443 -servername {sni} 2>/dev/null
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


class Tunnel:
    """A TCP tunnel to a remote port on a sandbox VM via the TLS gateway."""

    def __init__(
        self,
        job_id: str,
        remote_port: int,
        local_port: int | None = None,
        bind_address: str = "127.0.0.1",
        verify_ssl: bool = True,
    ):
        self.job_id = job_id
        self.remote_port = remote_port
        self.local_port = local_port or remote_port
        self.bind_address = bind_address
        self.verify_ssl = verify_ssl

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
                gateway_sock = _create_tls_connection(gateway_host, gateway_port, sni, verify_ssl=self.verify_ssl)
                t1 = threading.Thread(
                    target=_forward_data,
                    args=(client_sock, gateway_sock, "client->gateway"),
                    daemon=True,
                )
                t2 = threading.Thread(
                    target=_forward_data,
                    args=(gateway_sock, client_sock, "gateway->client"),
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
                    server.settimeout(1.0)
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

        self._http = httpx.Client(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout),
        )

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
    ) -> SandboxState:
        """Start a sandbox environment.

        Uses Plato SDK v2 internally for session creation.

        Args:
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

        Returns:
            SandboxState with sandbox info.
        """

        assert self.api_key is not None

        # Build environment config using Env factory
        env_config: EnvFromSimulator | EnvFromArtifact | EnvFromResource

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
            env_config = Env.resource(sim_name, sim_config)
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
            env_config = Env.resource(simulator_name, sim_config)
        else:
            raise ValueError(f"Invalid mode '{mode}' or missing required parameter")

        # Track total time
        total_start = time.time()

        # We do each step separately to show progress:
        # 1. Create session, 2. Wait for ready, 3. Setup SSH
        from plato._generated.api.v2.sessions import make as sessions_make
        from plato._generated.api.v2.sessions import wait_for_ready as sessions_wait_for_ready
        from plato._generated.models import CreateSessionFromEnvs, Envs, RunSessionSource

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

        # Step 2: Wait for VM
        self.console.print("[yellow]Waiting for VM to start...[/yellow]")
        step_start = time.time()
        ready_response = sessions_wait_for_ready.sync(
            client=self._http,
            session_id=session_id,
            timeout=timeout,
            x_api_key=self.api_key,
        )
        if not ready_response.ready:
            errors = []
            if ready_response.results:
                for jid, result in ready_response.results.items():
                    if not result.ready:
                        errors.append(f"{jid}: {result.error or 'Unknown error'}")
            raise RuntimeError(f"VM failed to start: {', '.join(errors) if errors else 'timeout'}")

        job_id = response.envs[0].job_id if response.envs else None
        if not job_id:
            raise ValueError("No job ID found")
        elapsed = time.time() - step_start
        self.console.print(f"[green]VM ready:[/green] {job_id} [dim]({elapsed:.1f}s)[/dim]")

        # Step 3: Connect network
        network_connected = False
        if connect_network:
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

        # For artifact mode, we need to get simulator_name from session details BEFORE generating public URL
        # Note: get_session_details returns a dict, not a Pydantic model
        if not simulator_name:
            session_details = get_session_details.sync(
                client=self._http,
                session_id=session_id,
                x_api_key=self.api_key,
            )
            jobs = (
                session_details.get("jobs")
                if isinstance(session_details, dict)
                else getattr(session_details, "jobs", None)
            )
            if jobs:
                for j in jobs:
                    service = j.get("service") if isinstance(j, dict) else getattr(j, "service", None)
                    if service:
                        simulator_name = service
                        break
            if not simulator_name:
                raise ValueError(f"No simulator name found in session details for job ID {job_id}")

        # Get public URL with router target formatting (logic inlined)
        public_url = None
        try:
            url_response = sessions_get_public_url.sync(
                client=self._http,
                session_id=session_id,
                x_api_key=self.api_key,
            )
            if url_response and url_response.results:
                for result in url_response.results.values():
                    url = result.url if hasattr(result, "url") else str(result)
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

        # Setup SSH
        self.console.print("[yellow]Setting up SSH...[/yellow]")
        step_start = time.time()
        ssh_config_path = None
        try:
            public_key, private_key_path = _generate_ssh_key_pair(session_id[:8], Path(self.working_dir))

            add_key_request = AddSSHKeyRequest(public_key=public_key, username="root")
            add_response = sessions_add_ssh_key.sync(
                client=self._http,
                session_id=session_id,
                body=add_key_request,
                x_api_key=self.api_key,
            )

            if add_response.success:
                ssh_config_path = _generate_ssh_config(job_id, private_key_path, Path(self.working_dir))
                elapsed = time.time() - step_start
                self.console.print(
                    f"[green]SSH configured:[/green] ssh -F .plato/ssh_config sandbox [dim]({elapsed:.1f}s)[/dim]"
                )
            else:
                self.console.print("[dim]SSH key upload failed[/dim]")
        except Exception as e:
            self.console.print(f"[dim]SSH setup failed: {e}[/dim]")

        # Start heartbeat
        self.console.print("[yellow]Starting heartbeat...[/yellow]")
        step_start = time.time()
        heartbeat_pid = _start_heartbeat_process(session_id, self.api_key)
        elapsed = time.time() - step_start
        if heartbeat_pid:
            self.console.print(f"[green]Heartbeat started[/green] (pid={heartbeat_pid}) [dim]({elapsed:.1f}s)[/dim]")
        else:
            self.console.print("[dim]Heartbeat failed to start[/dim]")

        # Convert absolute paths to relative for state storage
        def _to_relative(abs_path: str | None) -> str | None:
            if not abs_path or not self.working_dir:
                return abs_path
            try:
                return str(Path(abs_path).relative_to(self.working_dir))
            except ValueError:
                return abs_path  # Keep absolute if not relative to working_dir

        # Update internal state
        rel_ssh_config = _to_relative(ssh_config_path)
        ssh_host = "sandbox" if ssh_config_path else None
        sandbox_state = SandboxState(
            session_id=session_id,
            job_id=job_id,
            public_url=public_url,
            mode=mode,
            ssh_config_path=rel_ssh_config,
            ssh_host=ssh_host,
            ssh_command=f"ssh -F {rel_ssh_config} {ssh_host}" if rel_ssh_config else None,
            heartbeat_pid=heartbeat_pid,
            simulator_name=simulator_name,
            dataset=dataset,
            network_connected=network_connected,
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
            sandbox_state.cpus = config_cpus
            sandbox_state.memory = config_memory
            sandbox_state.disk = config_disk
            sandbox_state.app_port = config_app_port
            sandbox_state.messaging_port = config_messaging_port

        # Save state to working_dir/.plato/state.json
        with open(self.working_dir / self.PLATO_DIR / "state.json", "w") as f:
            json.dump(sandbox_state.model_dump(), f)

        total_elapsed = time.time() - total_start
        self.console.print("")
        self.console.print(f"[bold green]Sandbox ready![/bold green] [dim](total: {total_elapsed:.1f}s)[/dim]")

        return sandbox_state

    # CHECKED
    def stop(
        self,
        session_id: str,
        heartbeat_pid: int | None = None,
    ) -> CloseSessionResponse:
        if heartbeat_pid:
            _stop_heartbeat_process(heartbeat_pid)

        return sessions_close.sync(
            client=self._http,
            session_id=session_id,
            x_api_key=self.api_key,
        )

    # CHECKED
    def status(self, session_id: str) -> SessionDetailsResponse:
        return get_session_details.sync(
            client=self._http,
            session_id=session_id,
            x_api_key=self.api_key,
        )

    # CHECKED
    def snapshot(
        self,
        session_id: str,
        mode: str,
        dataset: str,
    ) -> AppApiV2SchemasSessionCreateSnapshotResponse:
        checkpoint_request = CreateCheckpointRequest()

        if mode == "config":
            # read plato-config.yml - need parsed for extracting values
            plato_config_path = self.working_dir / "plato-config.yml"
            plato_config_raw = plato_config_path.read_text()
            plato_config = yaml.safe_load(plato_config_raw)

            # New format - extract just the dataset portion
            plato_config_model = PlatoConfig.model_validate(plato_config)
            dataset_config = plato_config_model.datasets[dataset]
            # Convert dataset config back to dict for YAML serialization
            dataset_dict = dataset_config.model_dump(exclude_none=True, by_alias=True, mode="json")
            checkpoint_request.plato_config = yaml.dump(dataset_dict, default_flow_style=False)

            dataset_compute = dataset_config.compute
            if not dataset_compute:
                raise ValueError(f"Compute configuration is required for dataset '{dataset}'")
            checkpoint_request.internal_app_port = dataset_compute.app_port
            checkpoint_request.messaging_port = dataset_compute.plato_messaging_port
            # we dont set target

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

        response = sessions_snapshot.sync(
            client=self._http,
            session_id=session_id,
            body=checkpoint_request,
            x_api_key=self.api_key,
        )

        # Save artifact_id to local state.json so it can be retrieved via `plato sandbox status`
        if response.results:
            # Get the first successful artifact_id from results
            for job_id, result in response.results.items():
                if result.success and result.artifact_id:
                    state_path = self.working_dir / self.PLATO_DIR / "state.json"
                    if state_path.exists():
                        with open(state_path) as f:
                            state = json.load(f)
                        state["artifact_id"] = result.artifact_id
                        with open(state_path, "w") as f:
                            json.dump(state, f)

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
    ) -> None:
        with open(self.working_dir / "plato-config.yml", "rb") as f:
            plato_config = yaml.safe_load(f)
        plato_config_model = PlatoConfig.model_validate(plato_config)
        dataset_config = plato_config_model.datasets[dataset]

        # Convert AppApiV2SchemasArtifactSimConfigDataset to AppSchemasBuildModelsSimConfigDataset
        # They have compatible fields but different nested types
        dataset_config_dict = dataset_config.model_dump(exclude_none=True, mode="json")

        _ = start_worker.sync(
            client=self._http,
            public_id=job_id,
            body=VMManagementRequest(
                service=simulator,
                dataset=dataset,
                plato_dataset_config=AppSchemasBuildModelsSimConfigDataset.model_validate(dataset_config_dict),
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
        state_file = self.working_dir / ".plato" / "state.json"
        if not state_file.exists():
            raise ValueError("No state file found - run 'plato sandbox start' first")

        with open(state_file) as f:
            state = json.load(f)

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
    ) -> Tunnel:
        return Tunnel(
            job_id=job_id,
            remote_port=remote_port,
            local_port=local_port,
            bind_address=bind_address,
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
        from plato._generated.api.v2.jobs import get_job_info

        gateway_host = os.getenv("PLATO_GATEWAY_HOST", "gateway.plato.so")

        # Get or create cached SSH key pair
        public_key, private_key_path = _get_or_create_cached_ssh_key_pair()

        # Look up session ID from job, then add SSH key via the session API
        try:
            job_info = get_job_info.sync(
                client=self._http,
                job_id=job_id,
                x_api_key=self.api_key,
            )
            if not job_info.session_id:
                raise RuntimeError(f"Job {job_id} has no associated session")

            auth_path = SSH_CACHE_DIR / "authorized_sessions"
            authorized = set(auth_path.read_text().splitlines()) if auth_path.exists() else set()

            if job_info.session_id in authorized:
                logger.info("SSH key already added to session %s, skipping", job_info.session_id)
            else:
                add_key_request = AddSSHKeyRequest(public_key=public_key, username="root")
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

        # Generate SSH config
        config_content = _generate_ssh_config_content(job_id, private_key_path)

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
            tunnel = self.tunnel(job_id, db_listener.db_port)
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
            env["PLATO_DB_USER"] = db_listener.db_user
            env["PLATO_DB_PASSWORD"] = db_listener.db_password or ""
            env["PLATO_DB_NAME"] = db_listener.db_database
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

    def clear_audit(self, job_group_id: str) -> EnvCleanupResponse:
        """Clear audit logs for a sandbox.

        This clears the audit_log table(s) in the sandbox's database,
        which tracks database mutations. Useful for resetting audit
        state between test runs.

        Args:
            job_group_id: The job group ID (same as session_id for v2 sessions)

        Returns:
            EnvCleanupResponse with success status
        """
        response = env_cleanup.sync(
            client=self._http,
            job_group_id=job_group_id,
            x_api_key=self.api_key,
        )
        return response

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
