import os
import keyring
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


KEY_BYTES = 32
_BLOCK_SIZE = 16


class KeyringEncrypter:
    def __init__(self, service_name="Agilicus", username="encryption.key"):
        self.service_name = service_name
        self.username = username
        self.init_key()

    def init_key(self):
        encoded_key = keyring.get_password(self.service_name, self.username)
        if encoded_key is not None:
            key = base64.b64decode(encoded_key.encode("utf-8"))
        else:
            key = os.urandom(KEY_BYTES)
            encoded_key = base64.b64encode(key).decode("utf-8")
            keyring.set_password(self.service_name, self.username, encoded_key)
        self.key = key

    def encrypt(self, raw: str) -> bytes:
        try:
            iv = os.urandom(_BLOCK_SIZE)
            cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv))
            encryptor = cipher.encryptor()
            return (
                iv
                + encryptor.update(raw.encode("utf-8"))
                + encryptor.finalize()
                + encryptor.tag
            )
        except Exception as exc:
            raise ValueError(f"failed to encrypt: {str(exc)}")

    def decrypt(self, enc: bytes) -> str:
        try:
            tagStart = len(enc) - _BLOCK_SIZE
            tag = enc[tagStart:]
            iv = enc[:_BLOCK_SIZE]
            enc = enc[_BLOCK_SIZE:tagStart]
            cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv, tag))
            decryptor = cipher.decryptor()
            raw = decryptor.update(enc) + decryptor.finalize()
            return raw.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"failed to decrypt: {str(exc)}")
