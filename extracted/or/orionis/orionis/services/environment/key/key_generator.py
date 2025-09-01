import os
import base64
from orionis.foundation.config.app.enums.ciphers import Cipher

class SecureKeyGenerator:

    # Mapping of cipher modes to their respective key sizes in bytes
    KEY_SIZES = {
        Cipher.AES_128_CBC: 16,
        Cipher.AES_256_CBC: 32,
        Cipher.AES_128_GCM: 16,
        Cipher.AES_256_GCM: 32
    }

    @staticmethod
    def generate(cipher: str | Cipher = Cipher.AES_256_CBC) -> str:
        """
        Generate a Laravel-compatible APP_KEY.

        Parameters
        ----------
        cipher : str | Cipher
            The cipher algorithm. Options: AES-128-CBC, AES-256-CBC,
            AES-128-GCM, AES-256-GCM. Default is AES-256-CBC.

        Returns
        -------
        str
            A string formatted like Laravel's APP_KEY (e.g., base64:xxxx).
        """
        # Normalize cipher input to Cipher enum if string is provided
        if isinstance(cipher, str):
            try:
                cipher_enum = Cipher(cipher)
            except ValueError:
                raise ValueError(
                    f"Cipher '{cipher}' is not supported. "
                    f"Options: {', '.join(c.value for c in SecureKeyGenerator.KEY_SIZES.keys())}"
                )
        else:
            cipher_enum = cipher

        if cipher_enum not in SecureKeyGenerator.KEY_SIZES:
            raise ValueError(
                f"Cipher '{cipher_enum}' is not supported. "
                f"Options: {', '.join(c.value for c in SecureKeyGenerator.KEY_SIZES.keys())}"
            )

        key_length = SecureKeyGenerator.KEY_SIZES[cipher_enum]
        key = os.urandom(key_length)
        return f"base64:{base64.b64encode(key).decode('utf-8')}"
