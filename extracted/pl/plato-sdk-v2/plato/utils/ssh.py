import os
import sys
from pathlib import Path
from tempfile import mkdtemp

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

_SYSTEM_LIBRESSL = "/usr/bin/openssl"


def gateway_openssl_binary() -> str:
    """OpenSSL binary used for the SSH gateway ProxyCommand.

    Homebrew OpenSSL 3.6.x `s_client` drops gateway TLS tunnels under bulk
    bidirectional traffic: rsync/scp connections die within seconds
    ("connection unexpectedly closed" / broken pipe) while small probe
    commands succeed, so it masquerades as VM flakiness. `-nocommands` does
    not help. On macOS prefer the system LibreSSL at /usr/bin/openssl, which
    is unaffected; everywhere else keep resolving `openssl` from PATH.

    Set PLATO_SSH_OPENSSL_BIN to override the binary explicitly.
    """
    override = os.getenv("PLATO_SSH_OPENSSL_BIN")
    if override:
        return override
    if sys.platform == "darwin" and Path(_SYSTEM_LIBRESSL).exists():
        return _SYSTEM_LIBRESSL
    return "openssl"


def gateway_proxy_command(gateway_host: str, sni: str, *, port: int = 443, verify_flag: str = "") -> str:
    """Build the `openssl s_client` ProxyCommand for reaching a VM via the gateway."""
    flag = f" {verify_flag}" if verify_flag else ""
    return (
        f"{gateway_openssl_binary()} s_client -quiet -connect {gateway_host}:{port} -servername {sni}{flag} 2>/dev/null"
    )


def generate_ssh_key(*, directory: Path | None = None, prefix: str = "plato-ssh-") -> Path:
    """Generate a unique Ed25519 SSH key pair for VM access.

    Returns the private key path. The matching public key is written to the
    sibling ``.pub`` path. Each call gets its own temporary directory so
    concurrent callers cannot overwrite one another's keypair.
    """
    temp_dir = Path(mkdtemp(prefix=prefix, dir=str(directory) if directory is not None else None))
    temp_dir.chmod(0o700)

    key_path = temp_dir / "id_ed25519"
    pub_path = key_path.with_suffix(".pub")

    private_key = Ed25519PrivateKey.generate()

    key_path.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.OpenSSH,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    key_path.chmod(0o600)

    pub_path.write_bytes(
        private_key.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH,
        )
        + b"\n"
    )
    pub_path.chmod(0o644)

    return key_path
