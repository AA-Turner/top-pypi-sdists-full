"""Cross-process and cross-host reader/writer lock over a generation log of immutable snapshots."""

from __future__ import annotations

__lazy_modules__ = ["contrast_vendor.filelock._soft_rw._async"]

from contrast_vendor.filelock._soft_rw._async import AsyncAcquireSoftReadWriteReturnProxy, AsyncSoftReadWriteLock
from contrast_vendor.filelock._soft_rw._sync import SoftReadWriteLock

__all__ = [
    "AsyncAcquireSoftReadWriteReturnProxy",
    "AsyncSoftReadWriteLock",
    "SoftReadWriteLock",
]
