"""
cvc.core.will — Soul Will & Executor Protocol.

This is the load-bearing missing piece of the digital-parents arc. The
soul can outlive its owner — but only if there's a plan for what
happens next. Without a will, the .cvc/ folder rots on a hard drive
and the soul disappears with its owner.

The Will is:
  - **A free-form message** from the owner to whoever inherits the soul.
    "If you are reading this, I have passed. Here is what I want you
    to know about me, about the people I cared about, about what I
    built..."
  - **A list of executors** — people the owner trusts to receive the
    soul. Each has a public key stored with their executor record.
  - **A release condition** — currently `manual` only. The owner
    must explicitly trigger the release. v2 will add `time_locked`
    and `death_verified`.

Crypto design:
  - The **will_text** is encrypted via the existing soul vault
    (AES-256-GCM, scrypt-derived key). This inherits all the security
    guarantees from cvc.security.vault — same crypto as every other
    soul blob.
  - **Executor public keys** are RSA-4096, PEM-encoded. Generated on
    demand via ``WillStore.generate_executor_keypair()``. The private
    key is shown to the owner **once** with a "save this somewhere
    safe" warning. The vault never stores private keys.
  - v1 release = the owner's manual action. The release artifact is a
    single ``.soul`` file containing will_text + metadata. In v2 the
    release will require M-of-N executor signatures (Shamir + RSA).

Storage:
  - Metadata (executors, release_condition, timestamps, blob name):
    ``~/.cvc/will.json`` — unencrypted, audit-friendly.
  - Will text: ``~/.cvc/vault/blobs/will_<will_id>.cvcv`` — encrypted.

Forward compatibility:
  - v1 manual release works today.
  - v2 will add: time_locked (release on date), death_verified (oracle
    attestation), Shamir M-of-N key release. The data structures are
    designed to accommodate these without breaking v1 records.

Privacy invariants (enforced at the API layer in cvc.gateway.soul):
  - ``will_text`` is NEVER returned by any endpoint except ``release``.
  - Private keys are NEVER stored. Never logged. Never echoed back.
"""

from __future__ import annotations

import json
import logging
import os
import secrets
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.will")

WILL_METADATA_FILENAME = "will.json"
WILL_VAULT_BLOB_PREFIX = "will_"
EXECUTOR_KEY_SIZE = 4096  # RSA


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@dataclass
class Executor:
    """One person the owner trusts to inherit the soul.

    Each executor gets a public key at creation time. The private key
    is generated and returned ONCE to the owner (who must save it
    somewhere safe and share it with the executor out-of-band). v1
    release does not yet require executor signatures — that lands in
    v2 with Shamir M-of-N. The public keys are stored for forward
    compatibility.
    """

    executor_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str = ""
    relationship: str = ""  # "wife", "son", "lawyer", "best friend"
    contact: str = ""  # email or phone — for the owner to coordinate release
    role: str = "primary"  # "primary" | "witness" | "backup"
    public_key_pem: str = ""  # RSA-4096 public key, PEM-encoded
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SoulWill:
    """The owner's will for their soul.

    Append-only metadata. The will_text lives encrypted in the vault;
    only the blob name is referenced here.

    A second ``version`` increments on every update. The old will_text
    blob is retained (not deleted) so audit can verify evolution.
    """

    will_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    owner_name: str = ""
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    version: int = 1
    release_condition: str = "manual"  # "manual" | "time_locked" (v2) | "death_verified" (v2)
    executors: list[Executor] = field(default_factory=list)
    # Vault blob name holding the encrypted will_text. None until
    # the first create() call. Older blobs are kept on update for audit.
    current_blob_name: str = ""
    blob_history: list[str] = field(default_factory=list)
    # Total releases (audit). Each release creates an artifact.
    release_count: int = 0
    last_released_at: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "will_id": self.will_id,
            "owner_name": self.owner_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
            "release_condition": self.release_condition,
            "executors": [e.to_dict() for e in self.executors],
            "current_blob_name": self.current_blob_name,
            "blob_history": self.blob_history,
            "release_count": self.release_count,
            "last_released_at": self.last_released_at,
        }


# ---------------------------------------------------------------------------
# Key generation
# ---------------------------------------------------------------------------


def generate_executor_keypair() -> tuple[str, str]:
    """Generate an RSA-4096 keypair for a new executor.

    Returns:
        (public_key_pem, private_key_pem) — both as UTF-8 strings.

    The caller MUST surface the private key to the owner exactly once
    with an explicit warning to save it. The WillStore never stores
    the private key — it returns the keypair to the caller, who is
    responsible for delivery.
    """
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=EXECUTOR_KEY_SIZE)
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    return public_pem, private_pem


def validate_public_key_pem(pem: str) -> bool:
    """Sanity-check a public-key PEM. Returns True if loadable + RSA."""
    try:
        from cryptography.hazmat.primitives import serialization
        key = serialization.load_pem_public_key(pem.encode("utf-8"))
        # RSA only for v1 (so v2 Shamir can use the same key material).
        from cryptography.hazmat.primitives.asymmetric import rsa
        return isinstance(key, rsa.RSAPublicKey)
    except Exception:
        return False


# ---------------------------------------------------------------------------
# WillStore — load / save / encrypt / release
# ---------------------------------------------------------------------------


class WillStore:
    """Manages the soul will on disk.

    Owns:
      - ``will.json`` — unencrypted metadata (executors, timestamps, blob names).
      - ``<vault>/blobs/will_<id>.cvcv`` — encrypted will_text via SoulVault.
    """

    def __init__(
        self,
        cvc_root: Path,
        vault: Any | None = None,
    ) -> None:
        """WillStore constructor.

        Args:
            cvc_root: Path to the active CVC root (where ``will.json`` lives).
            vault: Optional pre-constructed ``SoulVault`` instance. When
                provided, this is used directly — avoids the per-call
                instance that would always be locked. The gateway should
                pass its session's unlocked vault here.
        """
        self.cvc_root = Path(cvc_root)
        self.will_path = self.cvc_root / WILL_METADATA_FILENAME
        self._injected_vault = vault

    # -- locate helpers ----------------------------------------------------

    @staticmethod
    def vault_dir() -> Path:
        """Find the soul vault dir (same lookup as cvc.gateway.security)."""
        candidates = [
            Path.cwd() / ".cvc" / "vault",
            Path.home() / ".cvc" / "vault",
        ]
        for p in candidates:
            if p.exists():
                return p
        return candidates[-1]

    def _vault(self) -> Any:
        """Lazily import + construct the SoulVault.

        If an unlocked vault was injected via the constructor, returns
        that. Otherwise constructs a fresh instance — which will be
        locked if the process hasn't unlocked the vault yet.
        """
        if self._injected_vault is not None:
            return self._injected_vault
        from cvc.security.vault import SoulVault
        return SoulVault(self.vault_dir())

    def _audit(self) -> Any:
        """Hash-chained audit log, same one the security gateway uses."""
        from cvc.security.audit import AuditLog
        return AuditLog(self.vault_dir() / "audit.log")

    # -- load / save metadata ---------------------------------------------

    def load(self) -> SoulWill | None:
        """Load the will metadata from disk. Returns None if no will yet."""
        if not self.will_path.exists():
            return None
        try:
            data = json.loads(self.will_path.read_text(encoding="utf-8"))
            executors = [Executor(**e) for e in data.get("executors", [])]
            return SoulWill(
                will_id=data["will_id"],
                owner_name=data.get("owner_name", ""),
                created_at=float(data.get("created_at", 0.0)),
                updated_at=float(data.get("updated_at", 0.0)),
                version=int(data.get("version", 1)),
                release_condition=data.get("release_condition", "manual"),
                executors=executors,
                current_blob_name=data.get("current_blob_name", ""),
                blob_history=data.get("blob_history", []),
                release_count=int(data.get("release_count", 0)),
                last_released_at=float(data.get("last_released_at", 0.0)),
            )
        except Exception as exc:
            logger.exception("failed to load will: %s", exc)
            return None

    def _save_metadata(self, will: SoulWill) -> Path:
        self.will_path.write_text(
            json.dumps(will.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return self.will_path

    # -- create / update ---------------------------------------------------

    def create_will(
        self,
        owner_name: str,
        will_text: str,
        executors: list[Executor] | None = None,
        release_condition: str = "manual",
    ) -> SoulWill:
        """Create or replace the will.

        Encrypts the will_text into the vault. If a will already exists,
        its blob is kept in ``blob_history`` (audit) and a new version
        replaces it. Same will_id, incremented version.

        Args:
            owner_name: For display in the executor UI / release artifact.
            will_text: The free-form message. Encrypted via vault.
            executors: Initial executor list (optional, can add later).
            release_condition: v1 = "manual".

        Returns the persisted SoulWill.
        """
        if release_condition != "manual":
            raise ValueError(
                f"release_condition='{release_condition}' is not supported in v1; "
                "only 'manual' is available"
            )

        existing = self.load()
        if existing is None:
            will = SoulWill(
                owner_name=owner_name,
                release_condition=release_condition,
                executors=list(executors or []),
            )
        else:
            # Update path: bump version, preserve will_id + executors if not given
            will = existing
            will.owner_name = owner_name
            will.release_condition = release_condition
            if executors is not None:
                will.executors = list(executors)
            will.version += 1
            if will.current_blob_name:
                will.blob_history.append(will.current_blob_name)

        will.updated_at = time.time()

        # Encrypt the new will_text into a fresh vault blob
        vault = self._vault()
        if not vault.is_initialized:
            raise RuntimeError(
                "soul vault is not initialized. "
                "Call cvc security initialize (or POST /api/security/initialize) first. "
                "The will_text is encrypted via the same vault that protects the rest of the soul."
            )
        # Ensure unlocked so write_blob works; raise a clear error otherwise.
        if not vault.is_unlocked:
            raise RuntimeError(
                "soul vault is locked. "
                "Call cvc security unlock (or POST /api/security/unlock) before writing the will."
            )

        blob_name = f"{WILL_VAULT_BLOB_PREFIX}{will.will_id}_v{will.version}"
        vault.write_blob(blob_name, will_text.encode("utf-8"))
        will.current_blob_name = blob_name

        self._save_metadata(will)

        # Audit
        try:
            audit = self._audit()
            audit.append(
                "will.create" if existing is None else "will.update",
                actor="owner",
                target=blob_name,
                detail={"version": will.version, "executors": len(will.executors)},
            )
        except Exception:
            # Audit failure shouldn't block the write — the will is already saved.
            logger.debug("audit append failed (non-fatal)")

        logger.info(
            "will: %s v%d (%d bytes encrypted) → blob=%s",
            "created" if existing is None else "updated",
            will.version,
            len(will_text),
            blob_name,
        )

        # C4: spine capture (best-effort, never raises)
        try:
            from cvc.events.spine import capture
            capture(
                kind="soul.will_created" if existing is None else "soul.will_updated",
                workspace=str(self.cvc_root),
                channel="soul",
                actor="owner",
                summary=f"will v{will.version} ({len(will.executors)} executors)",
                data={
                    "will_id": will.will_id,
                    "version": will.version,
                    "executors": len(will.executors),
                    "encrypted_bytes": len(will_text),
                },
                tags=["will", "digital-parents"],
            )
        except Exception:
            pass

        return will

    # -- executors ---------------------------------------------------------

    def add_executor(
        self,
        name: str,
        relationship: str,
        contact: str,
        role: str = "primary",
        public_key_pem: str = "",
    ) -> tuple[SoulWill, str | None]:
        """Add an executor to the will.

        If ``public_key_pem`` is empty, a fresh RSA-4096 keypair is
        generated. The private key is returned (once) — the caller must
        show it to the owner immediately with a save warning. The
        WillStore never persists private keys.

        Returns:
            (will, private_key_pem_or_None)
              - ``will``: the updated SoulWill metadata
              - ``private_key_pem``: the one-time private key (PEM),
                or None if the caller supplied a public_key_pem
        """
        will = self.load()
        if will is None:
            raise RuntimeError("no will exists yet — call create_will() first")

        private_key_pem: str | None = None
        if not public_key_pem:
            public_key_pem, private_key_pem = generate_executor_keypair()
        elif not validate_public_key_pem(public_key_pem):
            raise ValueError("provided public_key_pem is not a valid RSA PEM")

        executor = Executor(
            name=name,
            relationship=relationship,
            contact=contact,
            role=role if role in ("primary", "witness", "backup") else "primary",
            public_key_pem=public_key_pem,
        )
        will.executors.append(executor)
        will.updated_at = time.time()
        self._save_metadata(will)

        try:
            self._audit().append(
                "will.executor.add",
                actor="owner",
                target=executor.executor_id,
                detail={"name": name, "role": role},
            )
        except Exception:
            logger.debug("audit append failed (non-fatal)")

        logger.info("will: executor added name=%s role=%s id=%s", name, role, executor.executor_id)
        return will, private_key_pem

    def remove_executor(self, executor_id: str) -> SoulWill:
        """Remove an executor by id. Idempotent — no error if not found."""
        will = self.load()
        if will is None:
            raise RuntimeError("no will exists yet")
        before = len(will.executors)
        will.executors = [e for e in will.executors if e.executor_id != executor_id]
        if len(will.executors) != before:
            will.updated_at = time.time()
            self._save_metadata(will)
            try:
                self._audit().append(
                    "will.executor.remove",
                    actor="owner",
                    target=executor_id,
                )
            except Exception:
                logger.debug("audit append failed (non-fatal)")
        return will

    # -- release -----------------------------------------------------------

    def release(self, actor: str = "owner", reason: str = "") -> dict[str, Any]:
        """Build a release artifact.

        v1 release is always manual (the owner clicking a button). The
        artifact is a dict containing the will_text + metadata + audit
        trail — ready to be written as a single ``.soul`` JSON file by
        the gateway.

        Returns:
            {
              "will_id": ...,
              "owner_name": ...,
              "version": N,
              "released_at": unix_ts,
              "released_at_iso": "YYYY-MM-DD HH:MM:SS",
              "released_by": "owner",
              "reason": "manual release",
              "executors": [...],     # public-key material only
              "will_text": "...",     # decrypted plaintext
              "audit_chain_hash": "..."  # last hash of the audit log
            }

        Raises:
            RuntimeError if no will exists, or if the vault is locked.
        """
        will = self.load()
        if will is None:
            raise RuntimeError("no will exists to release")
        if not will.current_blob_name:
            raise RuntimeError("will has no current text blob — create the will first")

        vault = self._vault()
        if not vault.is_initialized:
            raise RuntimeError("soul vault is not initialized")
        if not vault.is_unlocked:
            raise RuntimeError("soul vault is locked — unlock before releasing")

        will_text_bytes = vault.read_blob(will.current_blob_name)
        will_text = will_text_bytes.decode("utf-8", errors="replace")

        released_at = time.time()
        will.release_count += 1
        will.last_released_at = released_at
        self._save_metadata(will)

        # Audit
        try:
            audit = self._audit()
            audit.append(
                "will.release",
                actor=actor,
                target=will.current_blob_name,
                detail={
                    "version": will.version,
                    "reason": reason or "manual release",
                },
            )
            # Pull the last chain_hash for the artifact — proof-of-trail.
            try:
                last_hash = audit._last_chain_hash()
            except Exception:
                last_hash = ""
        except Exception:
            last_hash = ""
            logger.debug("audit append failed (non-fatal)")

        artifact = {
            "will_id": will.will_id,
            "owner_name": will.owner_name,
            "version": will.version,
            "released_at": released_at,
            "released_at_iso": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(released_at)),
            "released_by": actor,
            "reason": reason or "manual release",
            "release_condition": will.release_condition,
            "executors": [e.to_dict() for e in will.executors],
            "will_text": will_text,
            "audit_chain_hash": last_hash,
            "schema": "cvc.soul.v1",
        }
        logger.info(
            "will: released (count=%d) will_id=%s v%d by %s",
            will.release_count,
            will.will_id,
            will.version,
            actor,
        )

        # C4: spine capture (best-effort)
        try:
            from cvc.events.spine import capture
            capture(
                kind="soul.will_released",
                workspace=str(self.cvc_root),
                channel="soul",
                actor=actor,
                summary=f"will v{will.version} released (count={will.release_count})",
                data={
                    "will_id": will.will_id,
                    "version": will.version,
                    "release_count": will.release_count,
                    "reason": reason or "",
                },
                tags=["will", "release", "digital-parents"],
            )
        except Exception:
            pass

        return artifact

    # -- status helpers ----------------------------------------------------

    def status(self) -> dict[str, Any]:
        """Return a status dict for the dashboard (no plaintext)."""
        will = self.load()
        if will is None:
            return {
                "exists": False,
                "release_condition": None,
                "executors": 0,
                "version": 0,
                "release_count": 0,
            }
        return {
            "exists": True,
            "will_id": will.will_id,
            "owner_name": will.owner_name,
            "version": will.version,
            "created_at": will.created_at,
            "updated_at": will.updated_at,
            "release_condition": will.release_condition,
            "executors": len(will.executors),
            "current_blob_name": will.current_blob_name,
            "blob_history_count": len(will.blob_history),
            "release_count": will.release_count,
            "last_released_at": will.last_released_at,
        }
