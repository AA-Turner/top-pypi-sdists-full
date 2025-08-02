import secrets

class SecretKey:

    @staticmethod
    def random(length: int = 32) -> str:
        """
        Generates a cryptographically secure random key of the specified length (in bytes), returned as a hex string.

        Args:
            length (int): Length of the key in bytes. Default is 32.

        Returns:
            str: A random key as a hexadecimal string.
        """
        return secrets.token_hex(length)