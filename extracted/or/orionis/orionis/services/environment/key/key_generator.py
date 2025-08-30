import os
import base64

class SecureKeyGenerator:
    """
    Utility class for generating Laravel-compatible APP_KEY values.

    Laravel expects keys in Base64 format, prefixed with 'base64:'.
    Supported ciphers: AES-128-CBC, AES-256-CBC, AES-128-GCM, AES-256-GCM.
    """

    KEY_SIZES = {
        "AES-128-CBC": 16,
        "AES-256-CBC": 32,
        "AES-128-GCM": 16,
        "AES-256-GCM": 32,
    }

    @staticmethod
    def generate(cipher: str = "AES-256-CBC") -> str:
        """
        Generate a Laravel-compatible APP_KEY.

        Parameters
        ----------
        cipher : str
            The cipher algorithm. Options: AES-128-CBC, AES-256-CBC,
            AES-128-GCM, AES-256-GCM. Default is AES-256-CBC.

        Returns
        -------
        str
            A string formatted like Laravel's APP_KEY (e.g., base64:xxxx).
        """
        if cipher not in SecureKeyGenerator.KEY_SIZES:
            raise ValueError(
                f"Cipher '{cipher}' no soportado. "
                f"Opciones: {', '.join(SecureKeyGenerator.KEY_SIZES.keys())}"
            )

        key_length = SecureKeyGenerator.KEY_SIZES[cipher]

        # Generate secure random bytes
        key = os.urandom(key_length)

        # Encode in Base64 and prepend 'base64:'
        return "base64:" + base64.b64encode(key).decode("utf-8")
