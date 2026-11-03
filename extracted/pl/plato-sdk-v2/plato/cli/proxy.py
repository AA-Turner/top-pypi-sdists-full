"""SSH and gateway utilities for Plato CLI.

This module provides:
- SSH key generation and config file management
- TLS connection utilities for port forwarding via TLS + SNI gateway

The CLI commands (ssh, tunnel) are in sandbox.py.
"""

import os
import socket
import ssl
import subprocess
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

# Default gateway configuration
DEFAULT_GATEWAY_HOST = "gateway.plato.so"
DEFAULT_GATEWAY_PORT = 443


def get_gateway_config() -> tuple[str, int]:
    """Get gateway host and port from environment or defaults."""
    host = os.environ.get("PLATO_GATEWAY_HOST", DEFAULT_GATEWAY_HOST)
    port = int(os.environ.get("PLATO_GATEWAY_PORT", str(DEFAULT_GATEWAY_PORT)))
    return host, port


def get_plato_dir(working_dir: Path | str | None = None) -> Path:
    """Get the .plato directory for config/SSH files.

    Args:
        working_dir: If provided, returns working_dir/.plato.
                     If None, returns cwd/.plato (workspace-based).
    """
    if working_dir is not None:
        return Path(working_dir) / ".plato"
    return Path.cwd() / ".plato"


def generate_ssh_key_pair(identifier: str, working_dir: Path | str | None = None) -> tuple[str, str]:
    """Generate a new ed25519 SSH key pair.

    Args:
        identifier: A unique identifier for naming the key files (e.g., job_id prefix)
        working_dir: Optional working directory for the .plato folder

    Returns:
        Tuple of (public_key_str, private_key_path)
    """
    plato_dir = get_plato_dir(working_dir)
    plato_dir.mkdir(mode=0o700, exist_ok=True)

    private_key_path = plato_dir / f"ssh_{identifier}_key"
    public_key_path = plato_dir / f"ssh_{identifier}_key.pub"

    # Remove existing keys if they exist
    private_key_path.unlink(missing_ok=True)
    public_key_path.unlink(missing_ok=True)

    # Generate ed25519 key pair
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Serialize private key in OpenSSH format
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Serialize public key in OpenSSH format
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH,
    )

    # Add comment to public key
    comment = f"plato-sandbox-{identifier}"
    public_key_str = f"{public_key_bytes.decode('utf-8')} {comment}"

    # Write private key with 0600 permissions
    private_key_path.write_bytes(private_key_bytes)
    private_key_path.chmod(0o600)

    # Write public key with 0644 permissions
    public_key_path.write_text(public_key_str + "\n")
    public_key_path.chmod(0o644)

    return public_key_str, str(private_key_path)


def generate_ssh_config(
    job_id: str,
    private_key_path: str,
    gateway_host: str | None = None,
    gateway_port: int | None = None,
    working_dir: Path | str | None = None,
) -> str:
    """Generate .plato/ssh_config file for easy SSH access.

    Args:
        job_id: The job ID for the sandbox VM.
        private_key_path: Path to the SSH private key file.
        gateway_host: Gateway hostname (default: from env or gateway.plato.so).
        gateway_port: Gateway port (default: from env or 443).
        working_dir: Working directory for .plato folder.

    Returns:
        Absolute path to the generated ssh_config file.
    """
    if gateway_host is None:
        gateway_host = os.environ.get("PLATO_GATEWAY_HOST", DEFAULT_GATEWAY_HOST)
    if gateway_port is None:
        gateway_port = int(os.environ.get("PLATO_GATEWAY_PORT", str(DEFAULT_GATEWAY_PORT)))

    plato_dir = get_plato_dir(working_dir)
    plato_dir.mkdir(mode=0o700, exist_ok=True)

    ssh_config_path = plato_dir / "ssh_config"

    config_content = f"""# Plato SSH Config
# Usage: ssh -F .plato/ssh_config sandbox

Host *.plato
    User root
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    ProxyCommand openssl s_client -quiet -connect {gateway_host}:{gateway_port} -servername %h--22.{gateway_host} 2>/dev/null

Host sandbox
    HostName {job_id}.plato
    IdentityFile {private_key_path}
"""

    ssh_config_path.write_text(config_content)
    ssh_config_path.chmod(0o600)

    return str(ssh_config_path)


def run_ssh_command(ssh_config_path: str, ssh_host: str, command: str) -> tuple[int, str, str]:
    """Run a command on the remote VM via SSH.

    Args:
        ssh_config_path: Path to SSH config file.
        ssh_host: SSH host alias (e.g., "sandbox").
        command: Shell command to execute.

    Returns:
        Tuple of (returncode, stdout, stderr).
    """
    result = subprocess.run(
        ["ssh", "-F", ssh_config_path, ssh_host, command],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def create_tls_connection(
    gateway_host: str,
    gateway_port: int,
    sni: str,
    verify_ssl: bool = True,
) -> ssl.SSLSocket:
    """Create a TLS connection to the gateway with the specified SNI.

    Args:
        gateway_host: The gateway hostname.
        gateway_port: The gateway port.
        sni: The SNI (Server Name Indication) for routing.
        verify_ssl: Whether to verify SSL certificates.

    Returns:
        An SSL socket connected to the gateway.
    """
    # Create SSL context
    context = ssl.create_default_context()
    if not verify_ssl:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    # Create socket and wrap with TLS
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)

    # Wrap with TLS, using SNI for routing
    ssl_sock = context.wrap_socket(sock, server_hostname=sni)

    try:
        ssl_sock.connect((gateway_host, gateway_port))
    except Exception as e:
        ssl_sock.close()
        raise ConnectionError(f"Failed to connect to gateway: {e}") from e

    return ssl_sock


def forward_data(src: socket.socket, dst: socket.socket, name: str = "") -> None:
    """Forward data between two sockets until one closes.

    Args:
        src: Source socket to read from.
        dst: Destination socket to write to.
        name: Optional name for debugging.
    """
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
