"""SSH utilities for dev mode."""

from __future__ import annotations

import asyncio
import os
import subprocess
import tempfile
from pathlib import Path

from pydantic import BaseModel

from plato.utils.subprocess import SSH_OPTS

GATEWAY_HOST = os.getenv("PLATO_GATEWAY_HOST", "gateway.plato.so")


def _get_ssh_options(job_id: str, private_key_path: Path) -> list[tuple[str, str]]:
    """Get SSH options for connecting to a VM via the gateway.

    Returns:
        List of (option_name, option_value) pairs
    """
    sni = f"{job_id}--22.{GATEWAY_HOST}"
    proxy_cmd = f"openssl s_client -quiet -connect {GATEWAY_HOST}:443 -servername {sni} 2>/dev/null"

    return [*SSH_OPTS, ("ProxyCommand", proxy_cmd)]


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


def build_ssh_command(job_id: str, private_key_path: Path) -> list[str]:
    """Build SSH command with proxy for connecting to a VM.

    Args:
        job_id: The job ID for the VM
        private_key_path: Path to the SSH private key

    Returns:
        SSH command as list of strings
    """
    options = _get_ssh_options(job_id, private_key_path)

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
    options = _get_ssh_options(job_id, private_key_path)

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
            line = await process.stdout.readline()
            if not line:
                break
            print(line.decode("utf-8", errors="replace").rstrip())

    await process.wait()
    return process.returncode or 0
