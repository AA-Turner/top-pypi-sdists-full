import base64
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from fivetran_connector_sdk_common.constants import CONFIG_ENCRYPTION_KEY_FILE, ENCRYPTED_VALUE_PREFIX, UTF_8
from fivetran_connector_sdk_common.helpers import config_root_dir

NONCE_LENGTH_BYTES = 12
KEY_SIZE_BYTES = 32  # AES-256


def _key_file_path() -> str:
    return os.path.join(config_root_dir(), CONFIG_ENCRYPTION_KEY_FILE)


def _load_key() -> bytes:
    """Loads the persisted encryption key, raising a clear error if it does not exist.

    This is the read-only path used when decrypting configuration.json; it never creates a key.
    """
    key_path = _key_file_path()
    if not os.path.exists(key_path):
        raise ValueError(
            f"configuration.json contains encrypted values but the encryption key was not found at "
            f"{key_path}; re-run 'fivetran configuration' to regenerate configuration.json"
        )

    try:
        with open(key_path, "r", encoding=UTF_8) as f:
            key = base64.b64decode(f.read().strip())
    except (OSError, ValueError) as e:
        raise ValueError(
            f"failed to read the encryption key at {key_path}; re-run 'fivetran configuration' to "
            f"regenerate configuration.json"
        ) from e

    if len(key) != KEY_SIZE_BYTES:
        raise ValueError(
            f"invalid key length: expected {KEY_SIZE_BYTES} bytes, got {len(key)}"
        )
    return key


def _decrypt_value(value: str | None, field_name: str, key: bytes) -> str | None:
    """Decrypts value if it carries ENCRYPTED_VALUE_PREFIX; otherwise returns it unchanged."""
    if value is None or not value.startswith(ENCRYPTED_VALUE_PREFIX):
        return value

    try:
        combined = base64.b64decode(value[len(ENCRYPTED_VALUE_PREFIX):])
        if len(combined) < NONCE_LENGTH_BYTES:
            raise ValueError("ciphertext shorter than nonce length")
        nonce, ciphertext = combined[:NONCE_LENGTH_BYTES], combined[NONCE_LENGTH_BYTES:]
        plaintext = AESGCM(key).decrypt(nonce, ciphertext, field_name.encode(UTF_8))
        return plaintext.decode(UTF_8)
    except (ValueError, InvalidTag) as e:
        raise ValueError(
            f"failed to decrypt configuration field '{field_name}'; the value contains the "
            f"'{ENCRYPTED_VALUE_PREFIX}' prefix, so Fivetran attempted to decrypt it, but the encryption key "
            f"is missing or invalid, or the encrypted value is corrupted. Re-run "
            f"'fivetran configuration' to regenerate configuration.json."
        ) from e


def _key_directory_permissions_ok(directory: str) -> bool:
    return os.access(directory, os.R_OK | os.W_OK | os.X_OK)


def get_or_create_key() -> bytes:
    """Returns the persisted encryption key, generating and persisting a new one if none exists yet."""
    key_path = _key_file_path()
    if os.path.exists(key_path):
        return _load_key()
    key = os.urandom(KEY_SIZE_BYTES)
    directory = os.path.dirname(key_path)
    os.makedirs(directory, mode=0o700, exist_ok=True)
    if not _key_directory_permissions_ok(directory):
        raise ValueError(f"Not enough permissions for directory: {directory}. "
                         "The owner must have read, write, and execute permissions.")
    temp_path = key_path + ".tmp"
    if os.path.exists(temp_path):
        os.unlink(temp_path)
    fd = os.open(temp_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding=UTF_8) as f:
        f.write(base64.b64encode(key).decode("ascii"))
    os.replace(temp_path, key_path)
    return key


def encrypt_value(plaintext: str, field_name: str, key: bytes) -> str:
    """Encrypts `plaintext` bound to `field_name`, so a ciphertext cannot be copied to a different field."""
    nonce = os.urandom(NONCE_LENGTH_BYTES)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext.encode(UTF_8), field_name.encode(UTF_8))
    return ENCRYPTED_VALUE_PREFIX + base64.b64encode(nonce + ciphertext).decode("ascii")


def decrypt_configuration_values(configuration: dict) -> dict:
    """Decrypts every password field in configuration that carries ENCRYPTED_VALUE_PREFIX.

    The key is loaded lazily, only if at least one value in configuration is encrypted.
    """
    if not any(isinstance(value, str) and value.startswith(ENCRYPTED_VALUE_PREFIX)
               for value in configuration.values()):
        return configuration

    key = _load_key()
    return {field_name: _decrypt_value(value, field_name, key) for field_name, value in configuration.items()}
