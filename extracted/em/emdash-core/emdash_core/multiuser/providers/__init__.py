"""Sync providers for multiuser sessions.

This package contains implementations of the SyncProvider protocol
for different backends.

Available providers:
- LocalFileSyncProvider: File-based, single machine (dev/testing)
- FirebaseSyncProvider: Firebase Realtime Database (multi-machine)
"""

from .local import LocalFileSyncProvider
from .firebase import FirebaseSyncProvider

__all__ = ["LocalFileSyncProvider", "FirebaseSyncProvider"]
