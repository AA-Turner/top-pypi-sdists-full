import io
import json
import logging
import posixpath
import uuid
from typing import Dict, List, Optional

import polars as pl
import pyarrow.fs as pafs

from acryl_datahub_cloud.periodic_analytics import schema as pa_schema
from acryl_datahub_cloud.periodic_analytics.config import ObjectStorageConfig
from acryl_datahub_cloud.periodic_analytics.constants import Layer
from acryl_datahub_cloud.periodic_analytics.partitions import (
    DayPartition,
    HourPartition,
)

logger = logging.getLogger(__name__)

# RFC nests distinct sidecars under the bucket layer paths, so the sidecar
# layers share their parent bucket's subpath rather than getting their own.
_LAYER_SUBPATH: Dict[Layer, str] = {
    Layer.EVENTS: "events",
    Layer.HOURLY: "hourly_buckets",
    Layer.HOURLY_DISTINCT: "hourly_buckets",
    Layer.DAILY_ADDITIVE: "daily_buckets",
    Layer.DAILY_DISTINCT: "daily_buckets",
    Layer.MONTHLY: "monthly_buckets",
    Layer.BILLING_CLOSE: "billing_close",
}
_DISTINCT_LAYERS = {Layer.HOURLY_DISTINCT, Layer.DAILY_DISTINCT}


def _make_filesystem(config: ObjectStorageConfig) -> pafs.FileSystem:
    if config.provider == "s3":
        return pafs.S3FileSystem()  # credentials from pod identity / default chain
    if config.provider == "gcs":
        return pafs.GcsFileSystem()
    return pafs.LocalFileSystem()


class ObjectStore:
    """All Hive-layout path construction for periodic_analytics lives here.

    The layout is a cross-team contract:
    ``<bucket>/<prefix>/customer_id=<cid>/instance_id=<iid>/metric_family=<mf>/<layer>/dt=YYYY-MM-DD[/hour=HH]``
    """

    def __init__(
        self,
        config: ObjectStorageConfig,
        filesystem: Optional[pafs.FileSystem] = None,
    ) -> None:
        self.config = config
        self.filesystem: Optional[pafs.FileSystem] = filesystem or _make_filesystem(
            config
        )
        self.bucket_name = config.bucket.split("://", 1)[-1].rstrip("/")

    def close(self) -> None:
        # Drop the live pyarrow FileSystem before interpreter shutdown.
        # Holding S3FileSystem across Py_Finalize deadlocks in pyarrow>=24
        # (apache/arrow#50188). `del` of the Python ref is required;
        # finalize_s3() alone still hangs.
        fs = self.filesystem
        self.filesystem = None
        del fs

    def _require_filesystem(self) -> pafs.FileSystem:
        if self.filesystem is None:
            raise RuntimeError("ObjectStore.close() already called")
        return self.filesystem

    def tenant_prefix(self) -> str:
        # Bucket-relative (no bucket name) — run_lock.py talks to S3/GCS
        # directly via each provider's SDK (for conditional put/get/delete),
        # which needs a raw key, unlike every other ObjectStore method below
        # that returns a pyarrow-filesystem path with the bucket baked in.
        return posixpath.join(
            self.config.prefix,
            f"customer_id={self.config.customer_id}",
            f"instance_id={self.config.instance_id}",
        )

    def lock_key(self, source_kind: str, metric_family: str) -> str:
        # Keyed on source KIND ("rollup"/"billing-sync") + tenant +
        # metric_family, not the ingestion-source entity name, so a restate
        # recipe and the scheduled source for the same layer contend for the
        # SAME lock. metric_family is included because recipes are scoped
        # per-family (see family_root) — without it, two recipes for the
        # same tenant + source_kind but different metric_family would
        # over-lock each other despite touching disjoint storage roots.
        return posixpath.join(
            self.tenant_prefix(),
            f"metric_family={metric_family}",
            "_locks",
            f"{source_kind}.lock",
        )

    def family_root(self, metric_family: str) -> str:
        return posixpath.join(
            self.bucket_name, self.tenant_prefix(), f"metric_family={metric_family}"
        )

    def layer_dir(self, metric_family: str, layer: Layer) -> str:
        return posixpath.join(self.family_root(metric_family), _LAYER_SUBPATH[layer])

    def hour_dir(self, metric_family: str, layer: Layer, hour: HourPartition) -> str:
        path = posixpath.join(
            self.layer_dir(metric_family, layer),
            f"dt={hour.dt}",
            f"hour={hour.hour:02d}",
        )
        return (
            posixpath.join(path, "distinct_sets") if layer in _DISTINCT_LAYERS else path
        )

    def day_dir(self, metric_family: str, layer: Layer, day: DayPartition) -> str:
        path = posixpath.join(self.layer_dir(metric_family, layer), f"dt={day.dt}")
        return (
            posixpath.join(path, "distinct_sets") if layer in _DISTINCT_LAYERS else path
        )

    def day_has_event_files(self, metric_family: str, day: DayPartition) -> bool:
        """True when the events layer has at least one parquet under ``dt=<day>``."""
        events_dir = posixpath.join(
            self.layer_dir(metric_family, Layer.EVENTS), f"dt={day.dt}"
        )
        return bool(self.list_parquet_files(events_dir))

    def period_dir(self, metric_family: str, layer: Layer, period: str) -> str:
        return posixpath.join(self.layer_dir(metric_family, layer), f"period={period}")

    def delete_dir_contents(self, dir_path: str) -> None:
        # Restate re-runs a watermarked hour and must overwrite cleanly rather
        # than appending a second generation of bucket-*.parquet files
        # alongside the stale ones; missing_dir_ok covers first-time hours.
        self._require_filesystem().delete_dir_contents(dir_path, missing_dir_ok=True)

    def list_parquet_files(self, dir_path: str) -> List[str]:
        selector = pafs.FileSelector(dir_path, recursive=False, allow_not_found=True)
        infos = self._require_filesystem().get_file_info(selector)
        return sorted(
            info.path
            for info in infos
            if info.type == pafs.FileType.File and info.path.endswith(".parquet")
        )

    def read_json(self, path: str) -> Optional[dict]:
        fs = self._require_filesystem()
        info = fs.get_file_info(path)
        if info.type != pafs.FileType.File:
            return None
        with fs.open_input_stream(path) as stream:
            return json.loads(stream.read().decode("utf-8"))

    def write_json(self, path: str, payload: dict) -> None:
        fs = self._require_filesystem()
        fs.create_dir(posixpath.dirname(path), recursive=True)
        # Write-temp-then-rename so a crash mid-write can't leave a truncated
        # manifest.json (I2) — a partial local write would otherwise corrupt
        # the whole layer's watermarks, forcing a full recompute. On S3/GCS
        # `filesystem.move` is copy+delete, not a POSIX atomic rename — but
        # what matters here is object-granular visibility (readers only ever
        # see the old object or the fully-written new one, never a partial
        # write), which copy+delete preserves. The temp name carries a random
        # suffix rather than a fixed `{path}.tmp` — two concurrent writers to
        # the same manifest would otherwise stomp each other's temp object
        # before either gets to `move`, corrupting whichever one loses.
        # TODO: a writer that dies between open_output_stream and move now
        # leaks a uniquely-named orphan `*.tmp` object with no cleanup path
        # (the old fixed name was at least overwritten next run). Add a
        # periodic sweep or a lifecycle rule on `*.tmp` before this
        # accumulates unbounded in long-lived buckets.
        tmp_path = f"{path}.{uuid.uuid4().hex[:8]}.tmp"
        with fs.open_output_stream(tmp_path) as stream:
            stream.write(json.dumps(payload, indent=2, sort_keys=True).encode("utf-8"))
        fs.move(tmp_path, path)

    def write_parquet(self, df: pl.DataFrame, dir_path: str, filename: str) -> str:
        fs = self._require_filesystem()
        fs.create_dir(dir_path, recursive=True)
        path = posixpath.join(dir_path, filename)
        # pyarrow's NativeFile isn't typed as IO[bytes], so buffer in memory first
        # rather than passing the stream straight to polars.
        buffer = io.BytesIO()
        df.write_parquet(buffer)
        with fs.open_output_stream(path) as stream:
            stream.write(buffer.getvalue())
        logger.debug("wrote %d rows to %s", df.height, path)
        return path

    def scan_parquet(
        self,
        files: List[str],
        *,
        schema: Optional[Dict[str, pl.DataType]] = None,
    ) -> pl.LazyFrame:
        # provider=local wants plain paths; s3/gcs need the scheme prefixed so
        # polars picks its native cloud reader with the same default credentials.
        scheme = {"s3": "s3://", "gcs": "gs://", "local": ""}[self.config.provider]
        kwargs: Dict = {
            "low_memory": True,
            "missing_columns": "insert",
            "extra_columns": "ignore",
        }
        if schema is not None:
            # Explicit schema required when files may differ (additive vs latest
            # buckets): without it Polars locks onto the first file's columns.
            kwargs["schema"] = schema
        return pl.scan_parquet([f"{scheme}{f}" for f in files], **kwargs)

    def scan_bucket_parquet(self, files: List[str]) -> pl.LazyFrame:
        """Scan additive/latest bucket parquet with the union column schema."""
        return self.scan_parquet(files, schema=pa_schema.BUCKET_SCAN_SCHEMA)

    @staticmethod
    def new_file_name(kind: str) -> str:
        return f"{kind}-{uuid.uuid4().hex[:12]}.parquet"
