import os
import json
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

LEDGER_PATH = Path.home() / ".sage" / "offline_ledger.enc"
SALT = b"sage_offline_ledger_salt_v1"

class OfflineUsageLedger:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.key = self._derive_key(user_id)
        self.fernet = Fernet(self.key)
        self._ensure_ledger()

    def _derive_key(self, user_id: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=SALT,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(user_id.encode()))

    def _ensure_ledger(self):
        if not LEDGER_PATH.exists():
            self._write_ledger({"tokens_used": 0, "limit": 100000, "synced": True})

    def _read_ledger(self) -> dict:
        try:
            encrypted_data = LEDGER_PATH.read_bytes()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        except Exception:
            return {"tokens_used": 0, "limit": 100000, "synced": True}

    def _write_ledger(self, data: dict):
        encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        LEDGER_PATH.write_bytes(encrypted_data)

    def record_usage(self, tokens: int):
        data = self._read_ledger()
        if data["tokens_used"] + tokens > data["limit"]:
            raise Exception("Offline token limit exceeded. Please connect to WiFi or upgrade your plan to continue.")
        data["tokens_used"] += tokens
        data["synced"] = False
        self._write_ledger(data)

    def get_usage(self) -> int:
        return self._read_ledger().get("tokens_used", 0)

    def sync_limit(self, new_limit: int):
        data = self._read_ledger()
        data["limit"] = new_limit
        self._write_ledger(data)

    def sync_to_cloud_if_needed(self, sync_callback):
        """
        sync_callback should accept (tokens_used) and return True if successful.
        """
        data = self._read_ledger()
        if not data.get("synced", True) and data.get("tokens_used", 0) > 0:
            success = sync_callback(data["tokens_used"])
            if success:
                data["tokens_used"] = 0
                data["synced"] = True
                self._write_ledger(data)
