from pathlib import Path
from tempfile import mkdtemp

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


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
