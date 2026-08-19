# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Environment, storage_options, connections, and the BenchConfig knob bag.

Auth: ``account_name`` (env ``AZURE_STORAGE_ACCOUNT_NAME``, default the benchmark
account) plus an optional ``account_key`` (env ``AZURE_STORAGE_ACCOUNT_KEY``).
The key is optional — when absent, account-name-only options are returned so
lance can fall back to Workload Identity / managed identity / public access.
"""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Any, overload

import attrs

from loadtest.azure_scale_bench import constants

if TYPE_CHECKING:
    import argparse

    import lance

_LOG = logging.getLogger(__name__)

ACCOUNT_NAME_ENV = "AZURE_STORAGE_ACCOUNT_NAME"
ACCOUNT_KEY_ENV = "AZURE_STORAGE_ACCOUNT_KEY"

SUPPORTED_IMAGE_MODES = frozenset({"physical_size"})
SUPPORTED_IMAGE_FORMATS = frozenset({"png", "jpeg", "jpg"})


def storage_options_from_env(
    *, account_name: str | None = None, account_key: str | None = None
) -> dict[str, str]:
    """Build Azure ``storage_options``, honoring an explicit key then the env.

    The account key is optional: when neither an explicit key nor the env key is
    present, account-name-only options are returned (no error), letting lance use
    Workload Identity / managed identity / public access.
    """
    name = account_name or os.environ.get(ACCOUNT_NAME_ENV) or constants.DEFAULT_ACCOUNT
    key = account_key or os.environ.get(ACCOUNT_KEY_ENV)
    options: dict[str, str] = {
        "account_name": name,
        "azure_storage_account_name": name,
    }
    if key:
        options["account_key"] = key
    return options


def split_source_uri(uri: str) -> tuple[str, str]:
    """Split an ``az://container/name.lance`` URI into (db_uri, table_name).

    Geneva opens tables as ``connect(db_uri).open_table(table_name)``; the
    benchmark datasets live as ``<container>/<name>.lance`` so the database URI
    is the parent and the table name is the final segment without the suffix.
    """
    cleaned = uri.rstrip("/")
    if cleaned.endswith(".lance"):
        cleaned = cleaned[: -len(".lance")]
    db_uri, sep, table = cleaned.rpartition("/")
    if not sep or not db_uri or not table:
        raise ValueError(f"cannot split source URI into (db, table): {uri!r}")
    return db_uri, table


@overload
def _env_str(name: str, default: str) -> str: ...
@overload
def _env_str(name: str, default: None = None) -> str | None: ...
def _env_str(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    return value if value not in (None, "") else default


@overload
def _env_int(name: str, default: int) -> int: ...
@overload
def _env_int(name: str, default: None = None) -> int | None: ...
def _env_int(name: str, default: int | None = None) -> int | None:
    value = os.environ.get(name)
    return int(value) if value not in (None, "") else default


@overload
def _env_float(name: str, default: float) -> float: ...
@overload
def _env_float(name: str, default: None = None) -> float | None: ...
def _env_float(name: str, default: float | None = None) -> float | None:
    value = os.environ.get(name)
    return float(value) if value not in (None, "") else default


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value in (None, ""):
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


def _to_str_tuple(value: Any) -> tuple[str, ...]:
    """Coerce None / a comma-string / a list to a tuple of non-empty strings.

    Lets ``accounts`` accept a ``BENCH_ACCOUNTS`` comma env, a CLI string, or a
    YAML list from a profile, normalized to a tuple on every set.
    """
    if value is None:
        return ()
    if isinstance(value, str):
        return tuple(part.strip() for part in value.split(",") if part.strip())
    return tuple(value)


@attrs.define(kw_only=True)
class BenchConfig:
    """Resolved benchmark knobs (env defaults overlaid with CLI args).

    Holds the full ``BENCH_*`` knob set; individual stages consume the subset
    they need. ``storage_options`` is derived from the account name/key.
    """

    # Identity / connection.
    source_uri: str = constants.SOURCE_URI
    bench_uri: str = constants.BENCH_URI
    account_name: str = constants.DEFAULT_ACCOUNT
    account_key: str | None = attrs.field(default=None, repr=False)
    suffix: str = "smoke1"
    summary_col: str = constants.SUMMARY_COL
    row_index_col: str = constants.ROW_INDEX_COL
    cluster: str | None = None
    manifest: str | None = None

    # Dataset shape (per-dataset; set via a profile for non-50B sizes).
    # rows_per_fragment is the logical windowing unit (shard == Lance fragment
    # here); expected_* are optional and only drive inventory warnings.
    rows_per_fragment: int = constants.DEFAULT_ROWS_PER_FRAGMENT
    expected_rows: int | None = None
    expected_fragments: int | None = None

    # Reference-table generator (build-ref-table): build M rows that reference
    # already-uploaded blobs, derived from the seed-run config. M = target_rows, or
    # object_count * expansion_factor when target_rows is unset. seed_run_config_uri
    # points at the seed run's .seedrun.json (else derived from manifest_uri).
    expansion_factor: int = constants.DEFAULT_EXPANSION_FACTOR
    seed_run_config_uri: str | None = None
    target_rows: int | None = None
    build_workers: int = constants.DEFAULT_BUILD_WORKERS
    commit_fragments: int = constants.DEFAULT_COMMIT_FRAGMENTS
    data_storage_version: str = constants.DATA_STORAGE_VERSION
    limit_fragments: int | None = None
    validate_build: bool = True

    # Multi-base reference table (build-ref-table): spread fragment DATA across
    # separate storage accounts (aggregate throughput) while the dataset root /
    # manifests stay in the primary account (--account-name). Empty = single-base
    # (current behavior). Base data lives at
    # ``<container>/<prefix>/<run-id>/<account>/base.lance``; see
    # ``build_ref_table.build_table_bases``.
    table_base_accounts: tuple[str, ...] = attrs.field(
        factory=tuple, converter=_to_str_tuple
    )
    table_base_prefix: str = constants.DEFAULT_TABLE_BASE_PREFIX
    table_base_run_id: str | None = None
    table_base_container: str | None = None

    # Backfill knobs.
    num_frags: int | None = None
    skip_frags: int | None = None
    concurrency: int = 8
    intra_concurrency: int = 1
    task_size: int | None = None
    checkpoint_size: int | None = None
    min_checkpoint_size: int | None = None
    max_checkpoint_size: int | None = None
    flush_interval_seconds: float | None = None
    flush_bytes_target: int | None = None
    commit_granularity_pct: float | None = None
    blob_read_buffer_size: int | None = None
    per_actor_memory_gib: float = 1.5
    # Ray CPU reservation per UDF actor (num_cpus). Unset keeps the geneva @udf
    # default of 1 CPU/actor; raise it when a batched UDF runs internal threads
    # (e.g. --normalize-concurrency) so Ray does not overpack actors onto a pod.
    per_actor_cpus: float | None = None
    batch_size: int | None = None
    skip_on_error: int | None = None
    where: str | None = None
    input_col: str | None = None

    # Expand rerun semantics (explicit; consumed by expand_images.run_expand).
    overwrite: bool = False
    reuse_existing: bool = False

    # Image-generation knobs.
    image_mode: str = "physical_size"
    max_image_bytes: int | None = None
    include_large_tail: bool = False
    image_width: int = 224
    image_height: int = 224
    image_format: str = "png"

    # Normalize / pHash / dedupe knobs.
    norm_size: int = 224
    # Per-actor image-transform threads per batch; set it to switch normalize to the
    # batched (Array-input) normalizer. None/unset uses the per-row scalar normalizer.
    # Pairs with a LOWER --concurrency to cut Ray actor pressure at fixed parallelism.
    normalize_concurrency: int | None = None
    # Per-actor hash-compute threads per batch; set it to switch phash to the batched
    # (Array-input) pHash UDF. None/unset uses the per-row scalar pHash UDF. Pairs with
    # a LOWER --concurrency to cut Ray actor pressure at fixed parallelism.
    phash_concurrency: int | None = None
    duplicate_pct: float = 0.0
    dup_avg_group_size: int = 5
    dup_bit_flips: int = 2
    dup_num_groups: int | None = None
    hamming_threshold: int = 4
    target_partition_size: int = 50_000

    # Validation knobs.
    max_error_rate: float = 0.5
    decode_sample_count: int = 8
    # Ground-truth dedupe validation loads row_index for every row on the driver;
    # skip it above this row count (it is a smoke/calibration check, not a 50B step).
    validation_max_rows: int = 10_000_000

    # Metrics / scaling context (GEN-626).
    num_nodes: int | None = None
    num_cpus: int | None = None
    azure_subscription_id: str | None = None
    azure_resource_group: str | None = None

    # Loose-object upload job (image-dataset seeding).
    object_count: int = constants.DEFAULT_OBJECT_COUNT
    seed_run_id: str | None = None
    accounts: tuple[str, ...] = attrs.field(factory=tuple, converter=_to_str_tuple)
    loose_container: str = constants.DEFAULT_LOOSE_CONTAINER
    base_prefix: str = constants.DEFAULT_BASE_PREFIX
    prefix_count: int = constants.DEFAULT_PREFIX_COUNT
    manifest_uri: str | None = None
    seed_rows_per_fragment: int = constants.DEFAULT_SEED_ROWS_PER_FRAGMENT
    overwrite_objects: bool = False
    delete_after_months: int = constants.DEFAULT_LIFECYCLE_MONTHS
    max_bucket_miss_rate: float = 0.01
    # Concurrent PUTs per batch; set it to switch upload-images to the batched
    # (Array-input) uploader. None/unset uses the per-row scalar uploader.
    upload_concurrency: int | None = None

    # Ingest/download job. The run table (--clone-target) is a build-ref-table
    # reference table; the download UDF reads each row's locator columns directly and
    # adds the ingest columns in place. shuffle_salt is the build-ref-table shuffle
    # (consumed there).
    shuffle_salt: int = 0
    driver_rows_per_fragment: int | None = None
    repair_errors: bool = False
    # Backfill write strategy: ``fragment`` (carry-forward column rewrite,
    # default) or ``sparse_rows`` (geneva's sparse row-update engine;
    # repair-only — see download_images for the convergence constraint).
    update_mode: str = constants.UPDATE_MODE_FRAGMENT
    # Concurrent GETs per batch; set it to switch download-images to the batched
    # (Array-input) downloader. None/unset uses the per-row scalar downloader.
    download_concurrency: int | None = None
    # Hard ceiling on estimated in-flight GETs (concurrency * intra_concurrency *
    # download_concurrency) for the batched downloader. Raise it to launch above the
    # default intentionally.
    max_in_flight: int = constants.DEFAULT_MAX_IN_FLIGHT

    # Deterministic row-wise failure injection (download/normalize/phash) — exercises
    # the resume/repair paths without real faults. Selected by row_index + seed.
    inject_failure_rate: float = 0.0
    inject_failure_seed: int = 0

    @property
    def storage_options(self) -> dict[str, str]:
        """Azure storage_options for this run.

        Honors an explicit ``account_key``, then the env key; when no key is
        available, returns account-name-only options (Workload Identity / public).
        """
        return storage_options_from_env(
            account_name=self.account_name, account_key=self.account_key
        )

    def validate(self) -> None:
        """Validate config invariants; raise ``ValueError`` on bad knobs."""
        constants.validate_suffix(self.suffix)
        if self.image_mode not in SUPPORTED_IMAGE_MODES:
            raise ValueError(
                f"unsupported image_mode {self.image_mode!r}; "
                f"supported: {sorted(SUPPORTED_IMAGE_MODES)}"
            )
        if self.image_format.lower() not in SUPPORTED_IMAGE_FORMATS:
            raise ValueError(
                f"unsupported image_format {self.image_format!r}; "
                f"supported: {sorted(SUPPORTED_IMAGE_FORMATS)}"
            )
        if self.overwrite and self.reuse_existing:
            raise ValueError("overwrite and reuse_existing are mutually exclusive")
        if self.update_mode not in constants.UPDATE_MODES:
            raise ValueError(
                f"update_mode must be one of {list(constants.UPDATE_MODES)}, "
                f"got {self.update_mode!r}"
            )
        if self.update_mode == constants.UPDATE_MODE_SPARSE:
            if self.overwrite:
                raise ValueError(
                    "update_mode='sparse_rows' repairs existing download columns; "
                    "--overwrite would drop them"
                )
            if not self.repair_errors and not self.where:
                raise ValueError(
                    "update_mode='sparse_rows' rewrites only the image struct, so "
                    "the default resume predicate (url IS NULL) can never "
                    "converge; pass --repair-errors or an explicit --where"
                )
        if not 0.0 <= self.duplicate_pct <= 1.0:
            raise ValueError(
                f"duplicate_pct must be in [0, 1], got {self.duplicate_pct}"
            )
        if self.dup_bit_flips * 2 > self.hamming_threshold:
            raise ValueError(
                f"dup_bit_flips*2 ({self.dup_bit_flips * 2}) exceeds hamming_threshold "
                f"({self.hamming_threshold}); injected duplicates would not cluster"
            )
        if self.num_frags is not None and self.num_frags < 1:
            raise ValueError(f"num_frags must be >= 1, got {self.num_frags}")
        if self.skip_frags is not None and self.skip_frags < 0:
            raise ValueError(f"skip_frags must be >= 0, got {self.skip_frags}")
        if not 0.0 <= self.max_error_rate <= 1.0:
            raise ValueError(
                f"max_error_rate must be in [0, 1], got {self.max_error_rate}"
            )
        if self.target_partition_size <= 0:
            raise ValueError(
                f"target_partition_size must be > 0, got {self.target_partition_size}"
            )
        if self.norm_size <= 0:
            raise ValueError(f"norm_size must be > 0, got {self.norm_size}")
        if self.per_actor_cpus is not None and self.per_actor_cpus <= 0:
            raise ValueError(f"per_actor_cpus must be > 0, got {self.per_actor_cpus}")
        if self.hamming_threshold < 0:
            raise ValueError(
                f"hamming_threshold must be >= 0, got {self.hamming_threshold}"
            )
        if self.dup_bit_flips < 0:
            raise ValueError(f"dup_bit_flips must be >= 0, got {self.dup_bit_flips}")
        if self.decode_sample_count <= 0:
            raise ValueError(
                f"decode_sample_count must be > 0, got {self.decode_sample_count}"
            )
        if self.rows_per_fragment <= 0:
            raise ValueError(
                f"rows_per_fragment must be > 0, got {self.rows_per_fragment}"
            )
        if self.expansion_factor < 1:
            raise ValueError(
                f"expansion_factor must be >= 1, got {self.expansion_factor}"
            )
        if self.build_workers < 1:
            raise ValueError(f"build_workers must be >= 1, got {self.build_workers}")
        if self.commit_fragments < 1:
            raise ValueError(
                f"commit_fragments must be >= 1, got {self.commit_fragments}"
            )
        if self.data_storage_version not in constants.DATA_STORAGE_VERSIONS:
            raise ValueError(
                "data_storage_version must be one of "
                f"{', '.join(constants.DATA_STORAGE_VERSIONS)}, "
                f"got {self.data_storage_version!r}"
            )
        if self.target_rows is not None and self.target_rows <= 0:
            raise ValueError(f"target_rows must be > 0, got {self.target_rows}")
        if self.limit_fragments is not None and self.limit_fragments < 1:
            raise ValueError(
                f"limit_fragments must be >= 1, got {self.limit_fragments}"
            )
        if self.table_base_accounts:
            if len(set(self.table_base_accounts)) != len(self.table_base_accounts):
                raise ValueError(
                    "table_base_accounts must be unique (each account backs a "
                    "distinct base path)"
                )
            if not self.table_base_prefix.strip("/"):
                raise ValueError("table_base_prefix must not be empty")
            if self.table_base_run_id is not None and (
                not self.table_base_run_id
                or not all(ch.isalnum() or ch in "_-." for ch in self.table_base_run_id)
            ):
                raise ValueError(
                    f"table_base_run_id {self.table_base_run_id!r} must be non-empty "
                    "and contain only letters, digits, '.', '_', or '-'"
                )
        if self.rows_per_fragment > constants.LANCE_MAX_ROWS_PER_FILE:
            raise ValueError(
                "rows_per_fragment must be <= "
                f"{constants.LANCE_MAX_ROWS_PER_FILE} (Lance per-file cap), got "
                f"{self.rows_per_fragment}"
            )
        if self.object_count <= 0:
            raise ValueError(f"object_count must be > 0, got {self.object_count}")
        if self.prefix_count <= 0:
            raise ValueError(f"prefix_count must be > 0, got {self.prefix_count}")
        if self.seed_rows_per_fragment <= 0:
            raise ValueError(
                f"seed_rows_per_fragment must be > 0, got {self.seed_rows_per_fragment}"
            )
        if self.seed_rows_per_fragment > 1_048_576:
            raise ValueError(
                "seed_rows_per_fragment must be <= 1048576 (Lance per-file cap), got "
                f"{self.seed_rows_per_fragment}"
            )
        if self.delete_after_months < constants.DEFAULT_LIFECYCLE_MONTHS:
            raise ValueError(
                f"delete_after_months must be >= {constants.DEFAULT_LIFECYCLE_MONTHS} "
                f"(lifecycle policy), got {self.delete_after_months}"
            )
        if self.seed_run_id is not None and (
            not self.seed_run_id
            or not all(ch.isalnum() or ch in "_-" for ch in self.seed_run_id)
        ):
            raise ValueError(
                f"seed_run_id {self.seed_run_id!r} must be non-empty and contain only "
                "letters, digits, '_', or '-'"
            )
        if not 0.0 <= self.max_bucket_miss_rate <= 1.0:
            raise ValueError(
                f"max_bucket_miss_rate must be in [0, 1], got "
                f"{self.max_bucket_miss_rate}"
            )
        if self.shuffle_salt < 0:
            raise ValueError(f"shuffle_salt must be >= 0, got {self.shuffle_salt}")
        if not 0.0 <= self.inject_failure_rate <= 1.0:
            raise ValueError(
                f"inject_failure_rate must be in [0, 1], got {self.inject_failure_rate}"
            )
        if self.inject_failure_seed < 0:
            raise ValueError(
                f"inject_failure_seed must be >= 0, got {self.inject_failure_seed}"
            )
        if self.max_in_flight < 1:
            raise ValueError(f"max_in_flight must be >= 1, got {self.max_in_flight}")
        if self.download_concurrency is not None:
            # Per-knob guard against typos (the useful band is single/double digits).
            if not (
                1 <= self.download_concurrency <= constants.MAX_DOWNLOAD_CONCURRENCY
            ):
                raise ValueError(
                    "download_concurrency must be in "
                    f"[1, {constants.MAX_DOWNLOAD_CONCURRENCY}], got "
                    f"{self.download_concurrency}"
                )
            # System guard: total in-flight GETs ~= the product of the three
            # concurrency knobs. Hard-fail above max_in_flight so a large launch is
            # always intentional (raise --max-in-flight to go higher).
            in_flight = (
                self.concurrency * self.intra_concurrency * self.download_concurrency
            )
            if in_flight > self.max_in_flight:
                raise ValueError(
                    f"estimated in-flight GETs {in_flight} exceeds --max-in-flight "
                    f"{self.max_in_flight}: concurrency({self.concurrency}) * "
                    f"intra_concurrency({self.intra_concurrency}) * "
                    f"download_concurrency({self.download_concurrency}). Lower a "
                    "factor or raise --max-in-flight to run intentionally."
                )
        if self.upload_concurrency is not None:
            # Same two guards for the batched uploader (in-flight PUTs).
            if not (1 <= self.upload_concurrency <= constants.MAX_UPLOAD_CONCURRENCY):
                raise ValueError(
                    "upload_concurrency must be in "
                    f"[1, {constants.MAX_UPLOAD_CONCURRENCY}], got "
                    f"{self.upload_concurrency}"
                )
            in_flight = (
                self.concurrency * self.intra_concurrency * self.upload_concurrency
            )
            if in_flight > self.max_in_flight:
                raise ValueError(
                    f"estimated in-flight PUTs {in_flight} exceeds --max-in-flight "
                    f"{self.max_in_flight}: concurrency({self.concurrency}) * "
                    f"intra_concurrency({self.intra_concurrency}) * "
                    f"upload_concurrency({self.upload_concurrency}). Lower a "
                    "factor or raise --max-in-flight to run intentionally."
                )
        if self.normalize_concurrency is not None:
            # Per-knob guard against typos (the useful band is single/double digits).
            if not (
                1 <= self.normalize_concurrency <= constants.MAX_NORMALIZE_CONCURRENCY
            ):
                raise ValueError(
                    "normalize_concurrency must be in "
                    f"[1, {constants.MAX_NORMALIZE_CONCURRENCY}], got "
                    f"{self.normalize_concurrency}"
                )
            # System guard: estimated concurrent CPU image transforms (decode/resize/
            # encode) ~= the product of the three concurrency knobs. These are CPU
            # transforms, NOT GET/PUT network requests. Hard-fail above max_in_flight so
            # a large launch is always intentional (raise --max-in-flight to go higher).
            in_flight = (
                self.concurrency * self.intra_concurrency * self.normalize_concurrency
            )
            if in_flight > self.max_in_flight:
                raise ValueError(
                    f"estimated concurrent image transforms {in_flight} exceeds "
                    f"--max-in-flight {self.max_in_flight}: "
                    f"concurrency({self.concurrency}) * "
                    f"intra_concurrency({self.intra_concurrency}) * "
                    f"normalize_concurrency({self.normalize_concurrency}). These are "
                    "CPU transforms, not network requests. Lower a factor or raise "
                    "--max-in-flight to run intentionally."
                )
        if self.phash_concurrency is not None:
            # Per-knob guard against typos (the useful band is single/double digits).
            if not (1 <= self.phash_concurrency <= constants.MAX_PHASH_CONCURRENCY):
                raise ValueError(
                    "phash_concurrency must be in "
                    f"[1, {constants.MAX_PHASH_CONCURRENCY}], got "
                    f"{self.phash_concurrency}"
                )
            # System guard: estimated concurrent CPU pHash computations (decode + DCT
            # hash) ~= the product of the three concurrency knobs. These are CPU
            # computations, NOT GET/PUT network requests. Hard-fail above max_in_flight
            # so a large launch is always intentional (raise --max-in-flight to go
            # higher).
            in_flight = (
                self.concurrency * self.intra_concurrency * self.phash_concurrency
            )
            if in_flight > self.max_in_flight:
                raise ValueError(
                    f"estimated concurrent pHash computations {in_flight} exceeds "
                    f"--max-in-flight {self.max_in_flight}: "
                    f"concurrency({self.concurrency}) * "
                    f"intra_concurrency({self.intra_concurrency}) * "
                    f"phash_concurrency({self.phash_concurrency}). These are CPU "
                    "computations, not network requests. Lower a factor or raise "
                    "--max-in-flight to run intentionally."
                )
        if self.driver_rows_per_fragment is not None:
            if self.driver_rows_per_fragment <= 0:
                raise ValueError(
                    "driver_rows_per_fragment must be > 0, got "
                    f"{self.driver_rows_per_fragment}"
                )
            if self.driver_rows_per_fragment > 1_048_576:
                raise ValueError(
                    "driver_rows_per_fragment must be <= 1048576 (Lance per-file "
                    f"cap), got {self.driver_rows_per_fragment}"
                )

    @property
    def source_db_and_table(self) -> tuple[str, str]:
        """(db_uri, table_name) for the source dataset."""
        return split_source_uri(self.source_uri)

    @property
    def bench_db_and_table(self) -> tuple[str, str]:
        """(db_uri, table_name) for the benchmark clone."""
        return split_source_uri(self.bench_uri)

    @classmethod
    def from_env_and_args(cls, args: argparse.Namespace | None = None) -> BenchConfig:
        """Build config from ``BENCH_*`` env defaults, overlaid with CLI args.

        Any CLI argument that is not ``None`` overrides the env/default value.
        Argument dest names must match this class's field names.
        """
        cfg = cls(
            source_uri=_env_str("BENCH_SOURCE_URI", constants.SOURCE_URI),
            bench_uri=_env_str("BENCH_CLONE_TARGET", constants.BENCH_URI),
            account_name=(_env_str(ACCOUNT_NAME_ENV, constants.DEFAULT_ACCOUNT)),
            account_key=_env_str(ACCOUNT_KEY_ENV),
            suffix=_env_str("BENCH_VARIANT_SUFFIX", "smoke1"),
            summary_col=_env_str("BENCH_SUMMARY_COL", constants.SUMMARY_COL),
            cluster=_env_str("BENCH_CLUSTER"),
            manifest=_env_str("BENCH_MANIFEST"),
            rows_per_fragment=_env_int(
                "BENCH_ROWS_PER_FRAGMENT", constants.DEFAULT_ROWS_PER_FRAGMENT
            ),
            expected_rows=_env_int("BENCH_EXPECTED_ROWS"),
            expected_fragments=_env_int("BENCH_EXPECTED_FRAGMENTS"),
            expansion_factor=_env_int(
                "BENCH_EXPANSION_FACTOR", constants.DEFAULT_EXPANSION_FACTOR
            ),
            seed_run_config_uri=_env_str("BENCH_SEED_RUN_CONFIG_URI"),
            target_rows=_env_int("BENCH_TARGET_ROWS"),
            build_workers=_env_int(
                "BENCH_BUILD_WORKERS", constants.DEFAULT_BUILD_WORKERS
            ),
            commit_fragments=_env_int(
                "BENCH_COMMIT_FRAGMENTS", constants.DEFAULT_COMMIT_FRAGMENTS
            ),
            data_storage_version=_env_str(
                "BENCH_DATA_STORAGE_VERSION", constants.DATA_STORAGE_VERSION
            ),
            limit_fragments=_env_int("BENCH_LIMIT_FRAGMENTS"),
            validate_build=_env_bool("BENCH_VALIDATE_BUILD", True),
            table_base_accounts=_env_str("BENCH_TABLE_BASE_ACCOUNTS"),
            table_base_prefix=_env_str(
                "BENCH_TABLE_BASE_PREFIX", constants.DEFAULT_TABLE_BASE_PREFIX
            ),
            table_base_run_id=_env_str("BENCH_TABLE_BASE_RUN_ID"),
            table_base_container=_env_str("BENCH_TABLE_BASE_CONTAINER"),
            num_frags=_env_int("BENCH_NUM_FRAGS"),
            skip_frags=_env_int("BENCH_SKIP_FRAGS"),
            concurrency=_env_int("BENCH_CONCURRENCY", 8),
            intra_concurrency=_env_int("BENCH_INTRA_CONCURRENCY", 1),
            task_size=_env_int("BENCH_TASK_SIZE"),
            checkpoint_size=_env_int("BENCH_CHECKPOINT_SIZE"),
            min_checkpoint_size=_env_int("BENCH_MIN_CHECKPOINT_SIZE"),
            max_checkpoint_size=_env_int("BENCH_MAX_CHECKPOINT_SIZE"),
            flush_interval_seconds=_env_float("BENCH_FLUSH_INTERVAL_SECONDS"),
            flush_bytes_target=_env_int("BENCH_FLUSH_BYTES_TARGET"),
            commit_granularity_pct=_env_float("BENCH_COMMIT_GRANULARITY_PCT"),
            blob_read_buffer_size=_env_int("BENCH_BLOB_READ_BUFFER_SIZE"),
            per_actor_memory_gib=_env_float("BENCH_PER_ACTOR_MEMORY_GIB", 1.5),
            per_actor_cpus=_env_float("BENCH_PER_ACTOR_CPUS"),
            batch_size=_env_int("BENCH_BATCH_SIZE"),
            skip_on_error=_env_int("BENCH_SKIP_ON_ERROR"),
            where=_env_str("BENCH_WHERE"),
            input_col=_env_str("BENCH_INPUT_COL"),
            overwrite=_env_bool("BENCH_OVERWRITE", False),
            reuse_existing=_env_bool("BENCH_REUSE_EXISTING", False),
            image_mode=_env_str("BENCH_IMAGE_MODE", "physical_size"),
            max_image_bytes=_env_int("BENCH_MAX_IMAGE_BYTES"),
            include_large_tail=_env_bool("BENCH_INCLUDE_LARGE_TAIL", False),
            image_width=_env_int("BENCH_IMAGE_WIDTH", 224),
            image_height=_env_int("BENCH_IMAGE_HEIGHT", 224),
            image_format=_env_str("BENCH_IMAGE_FORMAT", "png"),
            norm_size=_env_int("BENCH_NORM_SIZE", 224),
            duplicate_pct=_env_float("BENCH_DUPLICATE_PCT", 0.0),
            dup_avg_group_size=_env_int("BENCH_DUP_AVG_GROUP_SIZE", 5),
            dup_bit_flips=_env_int("BENCH_DUP_BIT_FLIPS", 2),
            dup_num_groups=_env_int("BENCH_DUP_NUM_GROUPS"),
            hamming_threshold=_env_int("BENCH_HAMMING_THRESHOLD", 4),
            target_partition_size=_env_int("BENCH_TARGET_PARTITION_SIZE", 50_000),
            max_error_rate=_env_float("BENCH_MAX_ERROR_RATE", 0.5),
            decode_sample_count=_env_int("BENCH_DECODE_SAMPLE_COUNT", 8),
            validation_max_rows=_env_int("BENCH_VALIDATION_MAX_ROWS", 10_000_000),
            num_nodes=_env_int("BENCH_NUM_NODES"),
            num_cpus=_env_int("BENCH_NUM_CPUS"),
            azure_subscription_id=_env_str("AZURE_SUBSCRIPTION_ID"),
            azure_resource_group=_env_str("BENCH_AZURE_RESOURCE_GROUP"),
            object_count=_env_int("BENCH_OBJECT_COUNT", constants.DEFAULT_OBJECT_COUNT),
            seed_run_id=_env_str("BENCH_SEED_RUN_ID"),
            accounts=_env_str("BENCH_ACCOUNTS"),
            loose_container=_env_str(
                "BENCH_LOOSE_CONTAINER", constants.DEFAULT_LOOSE_CONTAINER
            ),
            base_prefix=_env_str("BENCH_BASE_PREFIX", constants.DEFAULT_BASE_PREFIX),
            prefix_count=_env_int("BENCH_PREFIX_COUNT", constants.DEFAULT_PREFIX_COUNT),
            manifest_uri=_env_str("BENCH_MANIFEST_URI"),
            seed_rows_per_fragment=_env_int(
                "BENCH_SEED_ROWS_PER_FRAGMENT", constants.DEFAULT_SEED_ROWS_PER_FRAGMENT
            ),
            overwrite_objects=_env_bool("BENCH_OVERWRITE_OBJECTS", False),
            delete_after_months=_env_int(
                "BENCH_DELETE_AFTER_MONTHS", constants.DEFAULT_LIFECYCLE_MONTHS
            ),
            max_bucket_miss_rate=_env_float("BENCH_MAX_BUCKET_MISS_RATE", 0.01),
            upload_concurrency=_env_int("BENCH_UPLOAD_CONCURRENCY"),
            shuffle_salt=_env_int("BENCH_SHUFFLE_SALT", 0),
            driver_rows_per_fragment=_env_int("BENCH_DRIVER_ROWS_PER_FRAGMENT"),
            repair_errors=_env_bool("BENCH_REPAIR_ERRORS", False),
            update_mode=_env_str("BENCH_UPDATE_MODE", constants.UPDATE_MODE_FRAGMENT),
            download_concurrency=_env_int("BENCH_DOWNLOAD_CONCURRENCY"),
            normalize_concurrency=_env_int("BENCH_NORMALIZE_CONCURRENCY"),
            phash_concurrency=_env_int("BENCH_PHASH_CONCURRENCY"),
            max_in_flight=_env_int(
                "BENCH_MAX_IN_FLIGHT", constants.DEFAULT_MAX_IN_FLIGHT
            ),
            inject_failure_rate=_env_float("BENCH_INJECT_FAILURE_RATE", 0.0),
            inject_failure_seed=_env_int("BENCH_INJECT_FAILURE_SEED", 0),
        )
        if args is not None:
            cfg._overlay_args(args)
        return cfg

    def _overlay_args(self, args: argparse.Namespace) -> None:
        """Override fields from non-None CLI args matching field names."""
        for field in attrs.fields(type(self)):
            value = getattr(args, field.name, None)
            if value is not None:
                setattr(self, field.name, value)


def open_lance(
    uri: str,
    storage_options: dict[str, str],
    *,
    version: int | None = None,
) -> lance.LanceDataset:
    """Open a Lance dataset by raw URI (used for inventory and clone)."""
    import lance

    return lance.dataset(uri, storage_options=storage_options, version=version)


def table_exists(db_uri: str, name: str, storage_options: dict[str, str]) -> bool:
    """Whether ``name`` physically exists as a Lance dataset under ``db_uri``.

    Preferred over ``conn.table_names()``, which returns a single page (default
    limit 10) and so silently omits tables in a container holding more — the
    ``az://datasets`` container this benchmark targets holds well over ten.
    """
    try:
        open_lance(f"{db_uri}/{name}.lance", storage_options)
    except Exception as exc:  # noqa: BLE001 - absence is the expected path
        _LOG.debug("table %s not present under %s: %s", name, db_uri, exc)
        return False
    return True


def connect_geneva(db_uri: str, storage_options: dict[str, str]) -> Any:
    """Connect a Geneva database for backfill stages."""
    import geneva

    return geneva.connect(db_uri, storage_options=storage_options)
