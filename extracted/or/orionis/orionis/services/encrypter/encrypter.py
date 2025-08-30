import base64
import json
import os
from typing import Optional
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Encrypter:

    SUPPORTED_CIPHERS = ["AES-128-CBC", "AES-256-CBC", "AES-128-GCM", "AES-256-GCM"]

    def __init__(self, app_key: str, cipher: str = "AES-256-CBC"):
        # Decodificar APP_KEY de Laravel
        if app_key.startswith("base64:"):
            key_bytes = base64.b64decode(app_key[7:])
        else:
            key_bytes = app_key.encode()

        self.key = key_bytes
        self.cipher = cipher

        # Validar cipher
        if cipher not in self.SUPPORTED_CIPHERS:
            raise ValueError(f"Cipher '{cipher}' no soportado. Usa uno de: {self.SUPPORTED_CIPHERS}")

        # Validar longitud de clave según el cipher
        key_len = len(self.key)
        if cipher.startswith("AES-128") and key_len != 16:
            raise ValueError("La clave debe ser de 16 bytes para AES-128")
        if cipher.startswith("AES-256") and key_len != 32:
            raise ValueError("La clave debe ser de 32 bytes para AES-256")

    def encrypt(self, plaintext: str) -> str:
        data = plaintext.encode()

        if "GCM" in self.cipher:
            return self._encrypt_gcm(data)
        else:
            return self._encrypt_cbc(data)

    def decrypt(self, payload: str) -> str:
        # Decodificar base64 -> JSON
        decoded = base64.b64decode(payload).decode()
        data = json.loads(decoded)

        cipher = data.get("cipher")
        iv = base64.b64decode(data["iv"])
        value = base64.b64decode(data["value"])
        tag = base64.b64decode(data["tag"]) if data.get("tag") else None

        if cipher != self.cipher:
            raise ValueError(f"El cipher del payload '{cipher}' no coincide con el configurado '{self.cipher}'")

        if "GCM" in cipher:
            return self._decrypt_gcm(value, iv, tag).decode()
        else:
            return self._decrypt_cbc(value, iv).decode()

    # -------------------
    # Métodos privados CBC
    # -------------------
    def _encrypt_cbc(self, data: bytes) -> str:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # PKCS7 padding
        pad_len = 16 - (len(data) % 16)
        data += bytes([pad_len]) * pad_len

        ct = encryptor.update(data) + encryptor.finalize()

        payload = {
            "iv": base64.b64encode(iv).decode(),
            "value": base64.b64encode(ct).decode(),
            "tag": None,
            "cipher": self.cipher,
        }

        return base64.b64encode(json.dumps(payload).encode()).decode()

    def _decrypt_cbc(self, ct: bytes, iv: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        data = decryptor.update(ct) + decryptor.finalize()

        # Unpad PKCS7
        pad_len = data[-1]
        return data[:-pad_len]

    # -------------------
    # Métodos privados GCM
    # -------------------
    def _encrypt_gcm(self, data: bytes) -> str:
        iv = os.urandom(12)
        aesgcm = AESGCM(self.key)
        ct = aesgcm.encrypt(iv, data, None)

        # separar ciphertext y tag (últimos 16 bytes)
        value, tag = ct[:-16], ct[-16:]

        payload = {
            "iv": base64.b64encode(iv).decode(),
            "value": base64.b64encode(value).decode(),
            "tag": base64.b64encode(tag).decode(),
            "cipher": self.cipher,
        }

        return base64.b64encode(json.dumps(payload).encode()).decode()

    def _decrypt_gcm(self, value: bytes, iv: bytes, tag: Optional[bytes]) -> bytes:
        aesgcm = AESGCM(self.key)
        return aesgcm.decrypt(iv, value + tag, None)
