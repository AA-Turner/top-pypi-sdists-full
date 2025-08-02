import os

class SecureKeyGenerator:
    """
    Provides static methods for generating secure random keys in base64 format.

    Methods
    -------
    generate_key() : str
        Generates a secure random key encoded in base64.
    """

    @staticmethod
    def generate() -> str:
        """
        Generates a cryptographically secure random key and encodes it in hexadecimal format.

        This method uses the operating system's cryptographic random number generator to
        produce a 32-byte random value, which is then encoded as a hexadecimal string.

        Returns
        -------
        str
            A 64-character hexadecimal string representing a 32-byte secure random key.
        """

        # Generate 32 random bytes using a cryptographically secure RNG
        # Encode the bytes as a hexadecimal string and return
        return os.urandom(32).hex()