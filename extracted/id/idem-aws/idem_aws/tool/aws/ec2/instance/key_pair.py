import contextlib
import os
import pathlib
import stat
import tempfile
from typing import Tuple

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import NoEncryption
from cryptography.hazmat.primitives.serialization import PrivateFormat
from cryptography.hazmat.primitives.serialization import PublicFormat


@contextlib.contextmanager
def verify(
    hub, *, ssh_public_key: str = None, ssh_private_key: str = None
) -> Tuple[str, str]:
    """
    Validate the ssh keypair, generate a keypair if necessary

    Args:
        hub:
        ssh_public_key(Text, Optional): A public ssh key or path to send to the instance
        ssh_private_key(Text, Optional): A private ssh key or path to send to the instance

    Yields:
        A tuple containing the bytes of the public ssh key and the file path of the private ssh key as a tuple

    Examples:
        # Create a new keypair
        with hub.tool.aws.ec2.instance.key_pair.verify() as key_pair:
            verified_public_key, private_key_file = key_pair

        # Validate an existing keypair
        ssh_public_key = "ssh-rsa XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX username@host"
        ssh_private_key = "~/.ssh/id_rsa"
        with hub.tool.aws.ec2.instance.key_pair.verify(ssh_public_key=ssh_public_key, ssh_private_key=ssh_private_key) as key_pair:
            verified_public_key, private_key_file = key_pair
    """
    if bool(ssh_public_key) != bool(ssh_private_key):
        raise ValueError(
            "Both a private ssh key and a public ssh key must be specified"
        )

    # Create a keypair if none were passed
    if not (ssh_public_key and ssh_private_key):
        hub.log.debug(f"Creating an ssh keypair")
        private_key = rsa.generate_private_key(65537, 2048)
        ssh_private_key = private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption(),
        )
        ssh_public_key = private_key.public_key().public_bytes(
            encoding=Encoding.OpenSSH, format=PublicFormat.OpenSSH
        )

    # Verify the public key
    if isinstance(ssh_public_key, bytes):
        ssh_public_key = ssh_public_key.decode()

    # If the ssh_public_key was a path, then read the contents of that path into a variable
    try:
        public_key_path = pathlib.Path(ssh_public_key)
        if public_key_path.exists():
            ssh_public_key = public_key_path.read_text()
    except:
        # It's OK, the public key is a string not a file path
        ...

    try:
        # Verify the private key
        private_key_path = pathlib.Path(
            ssh_private_key.decode()
            if isinstance(ssh_private_key, bytes)
            else ssh_private_key
        )
        file_exists = private_key_path.exists()
    except:
        file_exists = False

    if file_exists:
        st_mode = os.stat(private_key_path).st_mode
        if stat.S_ISREG(st_mode) and ((st_mode & 0o777) == 0o600):
            yield ssh_public_key, private_key_path.absolute()
        else:
            raise PermissionError(
                f"Private key has invalid permissions, should be 0o600"
            )
    else:
        with tempfile.NamedTemporaryFile(
            mode="wb+", prefix="id-rsa-", suffix=".pem", delete=True
        ) as private_key_file:
            if isinstance(ssh_private_key, str):
                ssh_private_key = ssh_private_key.encode()
            # Write private_key to file and chmod 400
            private_key_file.write(ssh_private_key)
            private_key_file.flush()
            os.chmod(private_key_file.name, 0o600)
            yield ssh_public_key, private_key_file.name
