from typing import Protocol

from benchling_sdk.helpers.package_helpers import _required_packages_context, ExtrasPackage


class _KeyUnwrappingFunction(Protocol):
    """
    Key Unwrapping Function.

    A function which accepts a ciphertext with a wrapped key and returns the data encrypting key as bytes.
    """

    def __call__(self, wrapped_key: bytes) -> bytes:
        pass


@_required_packages_context(ExtrasPackage.PYTHON_JOSE)
def _create_key_type(unwrapping_function: _KeyUnwrappingFunction):
    """
    Create an unwrapping Jose Key.

    Only implements the unwrap function. This key should not be used or distributed for any other purpose.
    """
    from jose.backends.base import Key

    # Create function to inject into the key to unwrap
    def _unwrap(wrapped_key: bytes) -> bytes:
        return unwrapping_function(wrapped_key)

    # We explicitly don't want to implement any other part of the key... just the unwrap
    class _RSAKeyDelegatedUnwrapping(Key):
        def sign(self, msg):
            raise NotImplementedError()

        def verify(self, msg, sig):
            raise NotImplementedError()

        def public_key(self):
            raise NotImplementedError()

        def to_pem(self):
            raise NotImplementedError()

        def to_dict(self):
            raise NotImplementedError()

        def encrypt(self, plain_text, aad=None):
            raise NotImplementedError()

        def decrypt(self, cipher_text, iv=None, aad=None, tag=None):
            raise NotImplementedError()

        def wrap_key(self, key_data):
            raise NotImplementedError()

        # Intentionally implemented
        def unwrap_key(self, wrapped_key):
            return _unwrap(wrapped_key)

    return _RSAKeyDelegatedUnwrapping
