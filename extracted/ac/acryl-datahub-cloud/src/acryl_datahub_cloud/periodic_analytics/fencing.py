import logging
from typing import Dict, Iterable, List

import polars as pl

from acryl_datahub_cloud.periodic_analytics.watermark import WatermarkStore

logger = logging.getLogger(__name__)


class MissingAuthoritativeGenerationError(Exception):
    def __init__(self, layer_desc: str, missing_keys: List[str]) -> None:
        self.layer_desc = layer_desc
        self.missing_keys = missing_keys
        # A partition with output files on disk but no watermark job_run_id
        # on record is a data-integrity anomaly (mark_complete always writes
        # job_run_id together with the watermark entry) -- fail loud rather
        # than silently merging every generation ever written for it, which
        # is exactly the double-counting-on-lease-steal bug this fence
        # exists to close.
        super().__init__(
            f"cannot fence {layer_desc} merge read: {len(missing_keys)} "
            f"partition(s) have output files but no watermark job_run_id on "
            f"record ({missing_keys}); refusing to guess which generation "
            "is authoritative"
        )


def authoritative_job_run_ids(
    watermark: WatermarkStore, keys: Iterable[str], layer_desc: str
) -> Dict[str, str]:
    """Builds the {time_bucket: job_run_id} fencing map for every partition
    being merged, from the lower-grain watermark that was already checked
    complete before this partition was planned. Fails loud (rather than
    silently merging every generation on disk) if a key's job_run_id is
    missing -- see MissingAuthoritativeGenerationError."""
    mapping: Dict[str, str] = {}
    missing: List[str] = []
    for key in keys:
        job_run_id = watermark.job_run_id(key)
        if job_run_id is None:
            missing.append(key)
        else:
            mapping[key] = job_run_id
    if missing:
        raise MissingAuthoritativeGenerationError(layer_desc, sorted(missing))
    return mapping


def fence_by_job_run_id(
    lf: pl.LazyFrame, authoritative: Dict[str, str]
) -> pl.LazyFrame:
    """Keeps only rows whose (time_bucket, job_run_id) pair matches that
    partition's authoritative generation -- discards any stale/orphaned
    generation left behind by a lost run-lock lease race (a contender that
    loses the lock mid-write can still leave a bucket-<uuid>.parquet file
    sitting beside the winner's, since output filenames are unique per run;
    listing a directory's files alone is not enough to guarantee a
    single-generation read). Every bucket row already carries both
    `time_bucket` and `job_run_id` columns (see rollup.hourly._bucket_metadata),
    so this is a plain semi-join, harmless (and a no-op in practice) for
    layers that were never double-written."""
    fence_df = pl.DataFrame(
        {
            "time_bucket": list(authoritative.keys()),
            "job_run_id": list(authoritative.values()),
        }
    )
    return lf.join(fence_df.lazy(), on=["time_bucket", "job_run_id"], how="semi")
