import posixpath
from datetime import datetime, timezone
from typing import Dict, Iterable, Optional, Set

from acryl_datahub_cloud.periodic_analytics.constants import MANIFESTS_DIR, Layer
from acryl_datahub_cloud.periodic_analytics.storage import ObjectStore


class WatermarkStore:
    """Per-layer completed-partition manifest (RFC R11: per-layer watermarks)."""

    def __init__(self, store: ObjectStore, metric_family: str, layer: Layer) -> None:
        self._store = store
        self._layer = layer
        self._path = posixpath.join(
            store.family_root(metric_family),
            MANIFESTS_DIR,
            layer.value,
            "manifest.json",
        )
        self._cache: Optional[Dict[str, dict]] = None

    def _partitions(self) -> Dict[str, dict]:
        if self._cache is None:
            manifest = self._store.read_json(self._path) or {}
            self._cache = dict(manifest.get("partitions", {}))
        return self._cache

    def completed_keys(self) -> Set[str]:
        return set(self._partitions())

    def is_complete(self, key: str) -> bool:
        return key in self._partitions()

    def job_run_id(self, key: str) -> Optional[str]:
        # The authoritative generation for a completed partition -- callers
        # merging this layer's output (the next grain up, or MTD) must fence
        # their read to rows carrying this job_run_id, so a stale/orphaned
        # generation left behind by a lost lease race (see run_lock.py)
        # never gets summed alongside the winner's.
        entry = self._partitions().get(key)
        return entry.get("job_run_id") if entry is not None else None

    def mark_complete(self, key: str, job_run_id: str) -> None:
        self.mark_complete_many([key], job_run_id)

    def mark_complete_many(self, keys: Iterable[str], job_run_id: str) -> None:
        """Batch-complete partitions with a single manifest write."""
        key_list = list(keys)
        if not key_list:
            return
        partitions = self._partitions()
        computed_at = datetime.now(timezone.utc).isoformat()
        for key in key_list:
            partitions[key] = {
                "job_run_id": job_run_id,
                "computed_at": computed_at,
            }
        self._store.write_json(
            self._path, {"layer": self._layer.value, "partitions": partitions}
        )
