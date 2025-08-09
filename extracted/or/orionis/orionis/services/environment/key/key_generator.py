import os

class SecureKeyGenerator:
    """
    Static utility class for generating cryptographically secure random keys.

    This class provides a static method to generate a secure random key,
    encoded as a hexadecimal string, suitable for use in security-sensitive
    applications such as cryptographic secrets or tokens.
    """

    @staticmethod
    def generate() -> str:
        """
        Generate a cryptographically secure random key encoded in hexadecimal.

        Returns
        -------
        str
            A 64-character hexadecimal string representing a 32-byte
            cryptographically secure random key.
        """

        # Generate 32 random bytes using a cryptographically secure RNG
        # Encode the bytes as a hexadecimal string and return
        return os.urandom(32).hex()
