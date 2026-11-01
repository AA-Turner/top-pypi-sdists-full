"""the sqlite receipt index: commit receipt identities in one transaction and compact it in bounded batches."""

from __future__ import annotations
RECEIPT_INDEX_VERSION = 1
RECEIPT_COMPACTION_BATCH = 256
