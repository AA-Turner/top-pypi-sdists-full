from abc import ABC, abstractmethod

from benchling_sdk.apps.config.cryptography_helpers import _create_key_type
from benchling_sdk.helpers.package_helpers import _required_packages_context, ExtrasPackage


class BaseDecryptionProvider(ABC):
    """
    Provides a way to decrypt encrypted messages.

    Various implementations might use AWS KMS, Azure, etc.
    """

    @abstractmethod
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt secrets.

        Receives encrypted cipher text and returns the decrypted plain text.
        """
        pass


class BaseKeyUnwrappingDecryptionProvider(BaseDecryptionProvider):
    """
    A decryption provider that will unwrap the key received from Benchling.

    Generally prefer extending this to BaseDecryptionProvider, unless you
    need to unwrap the key received from Benchling yourself.
    """

    _charset: str

    @_required_packages_context(ExtrasPackage.PYTHON_JOSE)
    def __init__(self, charset: str = "utf-8"):
        """Init BaseKeyUnwrappingDecryptionProvider."""
        self._charset = charset
        from jose import jwk
        from jose.constants import ALGORITHMS

        def _unwrapping_function(wrapped_key: bytes) -> bytes:
            return self.unwrap_key(wrapped_key)

        jwk.register_key(ALGORITHMS.RSA_OAEP_256, _create_key_type(_unwrapping_function))

    @_required_packages_context(ExtrasPackage.PYTHON_JOSE)
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt.

        Implement BaseDecryptionProvider's decrypt. Unwraps the encrypted payload from
        Benchling and will delegate to unwrap_key() to fetch the key decrypting key to
        then decrypt the secret.
        """
        from jose import jwe

        # Since we abstract key creation, the key name doesn't really matter
        return jwe.decrypt(ciphertext, "unused_key_id").decode(self._charset)

    @abstractmethod
    def unwrap_key(self, wrapped_key: bytes) -> bytes:
        """
        Unwrap Key.

        Accepts the wrapped key and decrypts the unwrapped key to use for data decryption
        from a provider such as AWS KMS, Azure, etc.
        """
        pass
