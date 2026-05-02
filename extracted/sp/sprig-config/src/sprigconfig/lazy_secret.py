# src/sprigconfig/lazy_secret.py
"""
SprigConfig LazySecret - secure secret wrapper with global key management.

Adds public, documented APIs for managing the Fernet encryption key
(set_global_key, ensure_key_from_env, set_key_provider) to remove the
need for external modules to modify private state.
"""

from typing import Optional, Callable
import os
from cryptography.fernet import Fernet, InvalidToken
from .exceptions import ConfigLoadError

# ---------------------------------------------------------------------------
# Global key management (new public API)
# ---------------------------------------------------------------------------

_GLOBAL_KEY: Optional[str] = None
_KEY_PROVIDER: Optional[Callable[[], Optional[str]]] = None


def set_global_key(key: str) -> None:
    """
    Set the global Fernet key used by all LazySecret instances.

    Args:
        key: Base64-encoded Fernet key string.

    Raises:
        ConfigLoadError: If the key is empty or invalid.
    """
    global _GLOBAL_KEY
    if not key:
        raise ConfigLoadError("Cannot set empty Fernet key")

    # Validate key immediately
    try:
        Fernet(key)
    except Exception as e:
        raise ConfigLoadError(f"Invalid Fernet key format: {e}")

    _GLOBAL_KEY = key


def get_global_key() -> Optional[str]:
    """Return the current Fernet key (for diagnostics only)."""
    return _GLOBAL_KEY


def set_key_provider(provider: Callable[[], Optional[str]]) -> None:
    """
    Register a callable that can dynamically return a key when needed.

    Args:
        provider: Callable that returns a valid Fernet key string or None.
    """
    global _KEY_PROVIDER
    if not callable(provider):
        raise ConfigLoadError("Key provider must be callable")
    _KEY_PROVIDER = provider


def ensure_key_from_env() -> None:
    """
    Ensure that a global key is available.
    Loads APP_SECRET_KEY from environment if not already set.
    """
    global _GLOBAL_KEY
    if not _GLOBAL_KEY:
        key = os.getenv("APP_SECRET_KEY")
        if key:
            set_global_key(key)


def _resolve_key(explicit_key: Optional[str] = None) -> str:
    """
    Resolve which key to use for decryption.

    Priority:
      1. Explicit key passed to LazySecret
      2. Global key set via set_global_key()
      3. Dynamic provider registered via set_key_provider()
      4. Environment variable APP_SECRET_KEY

    Guards against recursive key resolution during nested config loads.
    """
    # --- recursion guard -----------------------------------------------------
    if getattr(_resolve_key, "_resolving", False):
        raise ConfigLoadError("Recursive key resolution detected")
    _resolve_key._resolving = True
    try:
        # 1. Explicit key
        if explicit_key:
            return explicit_key

        # 2. Global key
        if _GLOBAL_KEY:
            return _GLOBAL_KEY

        # 3. Provider
        if callable(_KEY_PROVIDER):
            key = _KEY_PROVIDER()
            if key:
                set_global_key(key)
                return key

        # 4. Environment
        env_key = os.getenv("APP_SECRET_KEY")
        if env_key:
            set_global_key(env_key)
            return env_key

        raise ConfigLoadError("No key provided to LazySecret.")
    finally:
        _resolve_key._resolving = False



# ---------------------------------------------------------------------------
# LazySecret implementation
# ---------------------------------------------------------------------------

class LazySecret:
    """
    Represents a value encrypted with ENC(...).
    Decrypts only when accessed via get() or __str__().
    """

    __slots__ = ("_encrypted_value", "_decrypted_value", "_key")

    def __init__(self, enc_value: str, key: Optional[str] = None):
        # Defensive: tolerate ENC(...) or raw value
        if isinstance(enc_value, str) and enc_value.startswith("ENC(") and enc_value.endswith(")"):
            self._encrypted_value = enc_value[4:-1]
        else:
            self._encrypted_value = enc_value
        self._decrypted_value = None
        self._key = key

    def _decrypt(self):
        if self._decrypted_value is not None:
            return self._decrypted_value

        key = _resolve_key(self._key)
        try:
            fernet = Fernet(key.encode() if isinstance(key, str) else key)
            self._decrypted_value = fernet.decrypt(self._encrypted_value.encode()).decode()
            return self._decrypted_value
        except InvalidToken as e:
            raise ConfigLoadError(f"Invalid Fernet key or ciphertext: {e}")

    def get(self) -> str:
        """Return the decrypted value."""
        return self._decrypt()

    def __str__(self) -> str:
        """Return the decrypted value when cast to string (use with care)."""
        return self._decrypt()

    def zeroize(self):
        """Overwrite decrypted value in memory (best effort)."""
        if self._decrypted_value is not None:
            self._decrypted_value = "\0" * len(self._decrypted_value)
            self._decrypted_value = None


# ---------------------------------------------------------------------------
# Backward compatibility
# ---------------------------------------------------------------------------

# Provide legacy _key_provider symbol for external code that references it
if "_key_provider" not in globals():
    def _key_provider() -> Optional[str]:
        return os.getenv("APP_SECRET_KEY")

    _KEY_PROVIDER = _key_provider
