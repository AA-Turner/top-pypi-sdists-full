"""Local files of `plato vault totp`, in the same pattern as :mod:`app_store`.

``~/.plato-creds/vault-totp/<login_key>/`` (directories 700, files 600, every
write an atomic replace) holds two files per account:

* ``<account>.backup-codes.json``: the vendor's backup codes. The login vault has
  no notes field, so they stay on this machine.
* ``<account>.pending-seed.json``: the seed between the code step and the vault
  write. It is deleted when the vault holds the seed. If the vault write fails, it
  is the only copy: ``plato vault edit <login_key> -a <account> --creds-stdin <
  <file>`` saves it (its JSON is exactly ``{"totp_seed": "..."}``).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from pydantic import ValidationError

from plato.chronos.login_vault import normalize_key
from plato.cli.vault.app_store import StoreError, atomic_write
from plato.cli.vault.totp_models import BackupCodesRecord, PendingSeedFile

STORE_DIR_ENV_VAR = "PLATO_VAULT_TOTP_DIR"
DEFAULT_STORE_DIR = Path.home() / ".plato-creds" / "vault-totp"


class TotpLocalStore:
    def __init__(self, root: Path | None = None) -> None:
        env = os.environ.get(STORE_DIR_ENV_VAR)
        self.root = root or (Path(env) if env else DEFAULT_STORE_DIR)

    def _dir(self, login_key: str) -> Path:
        lk = normalize_key(login_key)
        if not lk:
            raise StoreError("login_key must hold at least one letter or digit")
        return self.root / lk

    def _file(self, login_key: str, account: str, suffix: str) -> Path:
        ac = normalize_key(account)
        if not ac:
            raise StoreError("account must hold at least one letter or digit")
        return self._dir(login_key) / f"{ac}.{suffix}.json"

    def backup_codes_path(self, login_key: str, account: str) -> Path:
        return self._file(login_key, account, "backup-codes")

    def pending_seed_path(self, login_key: str, account: str) -> Path:
        return self._file(login_key, account, "pending-seed")

    def _ensure_dir(self, path: Path) -> None:
        """Make the root and the login_key directory, 700 whatever the umask says."""
        try:
            self.root.parent.mkdir(parents=True, exist_ok=True)
            for d in (self.root, path.parent):
                d.mkdir(mode=0o700, exist_ok=True)
                os.chmod(d, 0o700)
        except OSError as e:
            raise StoreError(f"cannot make {path.parent}: {e.strerror or type(e).__name__}") from None

    def save_backup_codes(self, record: BackupCodesRecord) -> Path:
        path = self.backup_codes_path(record.login_key, record.account)
        self._ensure_dir(path)
        atomic_write(path, json.dumps(record.model_dump(mode="json", context={"reveal": True}), indent=1))
        return path

    def load_backup_codes(self, login_key: str, account: str) -> BackupCodesRecord | None:
        path = self.backup_codes_path(login_key, account)
        try:
            raw = path.read_text()
        except FileNotFoundError:
            return None
        except OSError as e:
            raise StoreError(f"cannot read {path}: {e.strerror}") from None
        try:
            return BackupCodesRecord.model_validate(json.loads(raw))
        except (ValueError, ValidationError):
            # Never chain: pydantic and json quote the input, which holds the codes.
            raise StoreError(f"{path} is not a valid backup-codes record; fix or remove it by hand") from None

    def save_pending_seed(self, login_key: str, account: str, pending: PendingSeedFile) -> Path:
        path = self.pending_seed_path(login_key, account)
        self._ensure_dir(path)
        atomic_write(path, json.dumps(pending.model_dump(mode="json", context={"reveal": True})))
        return path

    def has_pending_seed(self, login_key: str, account: str) -> bool:
        return self.pending_seed_path(login_key, account).exists()

    def drop_pending_seed(self, login_key: str, account: str) -> None:
        try:
            self.pending_seed_path(login_key, account).unlink()
        except FileNotFoundError:
            pass
        except OSError as e:
            raise StoreError(f"cannot remove {self.pending_seed_path(login_key, account)}: {e.strerror}") from None


def default_totp_store() -> TotpLocalStore:
    """The store the CLI uses. Tests patch this (or set ``PLATO_VAULT_TOTP_DIR``)."""
    return TotpLocalStore()
