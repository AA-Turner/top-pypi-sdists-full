"""SSH utilities for Plato CLI."""

from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


def get_plato_dir(working_dir: Path | str | None = None) -> Path:
    """Get the directory for plato config/SSH files.

    Args:
        working_dir: If provided, returns working_dir/.plato (for container/agent use).
                     If None, returns ~/.plato (local development).
    """
    if working_dir is not None:
        return Path(working_dir) / ".plato"
    return Path.home() / ".plato"


def generate_ssh_key_pair(identifier: str, working_dir: Path | str | None = None) -> tuple[str, str]:
    """
    Generate a new ed25519 SSH key pair.

    Args:
        identifier: A unique identifier for naming the key files (e.g., session_id prefix)
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
