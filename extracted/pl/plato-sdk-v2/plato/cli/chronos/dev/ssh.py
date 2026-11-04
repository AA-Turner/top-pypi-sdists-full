"""SSH utilities for dev mode."""

from __future__ import annotations

import asyncio
import logging
import os
import signal
import subprocess
import tempfile
from pathlib import Path

from pydantic import BaseModel

from plato.utils.ssh import gateway_proxy_command
from plato.utils.subprocess import SSH_OPTS

logger = logging.getLogger(__name__)


def _run_shell_with_timeout(
    cmd: str,
    timeout: int,
) -> subprocess.CompletedProcess[str]:
    """Run a shell command, killing the entire process group on timeout.

    Unlike subprocess.run(shell=True, timeout=...) which only kills the
    top-level shell, this kills all child processes (ssh, openssl, etc.)
    by placing them in a new session and sending SIGKILL to the group.
    """
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        return subprocess.CompletedProcess(cmd, proc.returncode, stdout, stderr)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()
        raise


GATEWAY_HOST = os.getenv("PLATO_GATEWAY_HOST", "gateway.plato.so")


def get_vm_ssh_options(job_id: str, private_key_path: Path) -> list[tuple[str, str]]:
    """Get SSH options for connecting to a VM via the gateway.

    Returns:
        List of (option_name, option_value) pairs
    """
    sni = f"{job_id}--22.{GATEWAY_HOST}"
    proxy_cmd = gateway_proxy_command(GATEWAY_HOST, sni)

    return [
        *SSH_OPTS,
        ("ProxyCommand", proxy_cmd),
        ("ControlMaster", "auto"),
        ("ControlPath", f"/tmp/plato-ssh-{job_id}"),
        ("ControlPersist", "600"),
    ]


class SSHKeyPair(BaseModel):
    """SSH key pair for VM access."""

    private_key_path: Path
    public_key: str

    model_config = {"arbitrary_types_allowed": True}

    @classmethod
    def generate(cls, key_dir: Path | None = None) -> SSHKeyPair:
        """Generate an ED25519 SSH keypair.

        Args:
            key_dir: Directory to store keys. Creates temp dir if None.

        Returns:
            SSHKeyPair with paths to generated keys.
        """
        if key_dir is None:
            key_dir = Path(tempfile.mkdtemp(prefix="plato_ssh_"))

        key_dir.mkdir(parents=True, exist_ok=True)
        private_key_path = key_dir / "id_ed25519"
        public_key_path = key_dir / "id_ed25519.pub"

        # Generate key pair
        subprocess.run(
            ["ssh-keygen", "-t", "ed25519", "-f", str(private_key_path), "-N", "", "-q"],
            check=True,
        )

        public_key = public_key_path.read_text().strip()
        return cls(private_key_path=private_key_path, public_key=public_key)


async def wait_for_ssh_reachable(
    job_id: str,
    private_key_path: Path,
    retries: int = 10,
    delay: float = 3.0,
    timeout: int = 10,
) -> bool:
    """Wait until the VM is reachable via the SSH gateway tunnel.

    The gateway uses NATS events to register WireGuard peers. There can be
    a brief window after connect_network returns where the gateway hasn't
    processed the peer-add event yet, causing SSH connections to time out
    during banner exchange. This probe retries until the tunnel works.

    Returns True if SSH became reachable, False if all retries exhausted.
    """
    loop = asyncio.get_event_loop()
    ssh_cmd = build_ssh_command_string(job_id, private_key_path)
    cmd = f"{ssh_cmd} root@{job_id}.plato true"
    proc_timeout = timeout + 5  # margin over SSH ConnectTimeout

    for attempt in range(1, retries + 1):
        try:
            result = await loop.run_in_executor(
                None,
                lambda: _run_shell_with_timeout(cmd, proc_timeout),
            )
            if result.returncode == 0:
                if attempt > 1:
                    logger.info("SSH gateway reachable for %s after %d attempts", job_id, attempt)
                else:
                    logger.debug("SSH gateway reachable for %s on first attempt", job_id)
                return True
            logger.debug(
                "SSH probe %d/%d for %s: exit %d — %s",
                attempt,
                retries,
                job_id,
                result.returncode,
                result.stderr.strip()[:100],
            )
        except subprocess.TimeoutExpired:
            logger.debug("SSH probe %d/%d for %s: timed out", attempt, retries, job_id)

        if attempt < retries:
            await asyncio.sleep(delay)

    logger.warning("SSH gateway not reachable for %s after %d attempts", job_id, retries)
    return False


def ensure_master_connection(job_id: str, private_key_path: Path, timeout: int = 30) -> bool:
    """Pre-establish an SSH ControlMaster connection.

    Must be called before parallel rsyncs to avoid ControlMaster race
    conditions where multiple processes compete to create the master socket.

    Returns True if the master was established successfully.
    """
    ssh_cmd = build_ssh_command_string(job_id, private_key_path)
    cmd = f"{ssh_cmd} root@{job_id}.plato true"
    try:
        result = _run_shell_with_timeout(cmd, timeout)
        if result.returncode != 0:
            logger.warning("Failed to pre-establish SSH master for %s: %s", job_id, result.stderr.strip())
            return False
        logger.debug("SSH ControlMaster established for %s", job_id)
        return True
    except subprocess.TimeoutExpired:
        logger.warning("SSH master connection timed out for %s after %ds", job_id, timeout)
        return False


def build_ssh_command(job_id: str, private_key_path: Path) -> list[str]:
    """Build SSH command with proxy for connecting to a VM.

    Args:
        job_id: The job ID for the VM
        private_key_path: Path to the SSH private key

    Returns:
        SSH command as list of strings
    """
    options = get_vm_ssh_options(job_id, private_key_path)

    cmd = ["ssh", "-i", str(private_key_path)]
    for name, value in options:
        cmd.extend(["-o", f"{name}={value}"])
    cmd.append(f"root@{job_id}.plato")

    return cmd


def build_ssh_command_string(job_id: str, private_key_path: Path) -> str:
    """Build SSH command string for use with rsync -e.

    Args:
        job_id: The job ID for the VM
        private_key_path: Path to the SSH private key

    Returns:
        SSH command string suitable for rsync -e option
    """
    options = get_vm_ssh_options(job_id, private_key_path)

    parts = [f"ssh -i {private_key_path}"]
    for name, value in options:
        # Quote values containing spaces
        if " " in value:
            parts.append(f"-o '{name}={value}'")
        else:
            parts.append(f"-o {name}={value}")

    return " ".join(parts)


async def run_ssh_command(
    job_id: str,
    private_key_path: Path,
    command: str,
    stream_output: bool = True,
) -> int:
    """Run a command via SSH and optionally stream output.

    Args:
        job_id: The job ID for the VM
        private_key_path: Path to the SSH private key
        command: Command to run on the VM
        stream_output: If True, print output in real-time

    Returns:
        Exit code of the command
    """
    ssh_cmd = build_ssh_command(job_id, private_key_path)
    ssh_cmd.append(command)

    process = await asyncio.create_subprocess_exec(
        *ssh_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    if stream_output and process.stdout:
        while True:
            try:
                line = await process.stdout.readline()
            except ValueError:
                line = await process.stdout.read(2**16)
                if not line:
                    break
            if not line:
                break
            print(line.decode("utf-8", errors="replace").rstrip())

    await process.wait()
    return process.returncode or 0
