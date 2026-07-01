"""
cvc.security — Hard Apple-grade security layer for the CVC soul.

The soul is local-first, but "local" isn't the same as "private." This module
guarantees that even on the owner's own machine, an attacker without the
passphrase cannot read the soul. It also guarantees the owner can verify
their soul hasn't been tampered with.

Three primitives:
  - SoulVault      : AES-GCM encryption at rest (db, blobs, dreams)
  - AuditLog       : append-only, hash-chained record of every read/write
  - NetworkSentinel: blocks any outbound call not on the brain allowlist

Together they make the soul:
  * Confidential (vault — only the owner can read it)
  * Tamper-evident (audit — owner can verify nothing changed)
  * Network-quiet (sentinel — owner can prove CVC made no surprise calls)
"""

from .vault import SoulVault, VaultLocked, VaultUnlocked
from .audit import AuditLog, AuditEntry, AuditAction
from .sentinel import NetworkSentinel, OutboundBlocked

__all__ = [
    "SoulVault", "VaultLocked", "VaultUnlocked",
    "AuditLog", "AuditEntry", "AuditAction",
    "NetworkSentinel", "OutboundBlocked",
]