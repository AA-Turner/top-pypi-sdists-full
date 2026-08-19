# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Stable configuration and naming conventions for the Azure 50B workbench.

This module is the single source of truth for URIs, the target blob-size
distribution, hash salts, and output-column naming, so that every stage
(clone / expand / normalize / phash / validate / cleanup) agrees on names.
No I/O happens here.
"""

from __future__ import annotations

from typing import Literal, get_args

# --- Source (read-only) and benchmark (writable clone) datasets ------------

DEFAULT_ACCOUNT = "oailancepub"

SOURCE_URI = (
    "az://datasets/mmlb_50b_default_text_embedding_50000shard_20260601053941.lance"
)
BENCH_URI = "az://datasets/mmlb_50b_azure_scale_bench.lance"

SOURCE_TABLE = "mmlb_50b_default_text_embedding_50000shard_20260601053941"
BENCH_TABLE = "mmlb_50b_azure_scale_bench"

# Default logical windowing unit (rows per shard == Lance fragment for these
# datasets; sequential row_index, fragment-aligned). Overridable per dataset via
# a profile's rows_per_fragment. Used to translate --num-frags/--skip-frags into
# row_index ranges.
DEFAULT_ROWS_PER_FRAGMENT = 1_000_000

# Lance hard cap on rows per data file; a fragment build must not exceed it.
LANCE_MAX_ROWS_PER_FILE = 1_048_576

# Source columns consumed across stages.
ROW_INDEX_COL = "row_index"
SUMMARY_COL = "summary"

# --- Reference-table generator (build-ref-table) ----------------------------

# Columns of the standalone shuffled reference table. Every column is a pure
# function of (image_id, seed-run config): a Feistel permutation over [0, M)
# yields ``logical``, then image_id = logical % N and expansion_index = logical // N,
# and the storage-locator + size columns are derived exactly as upload-images placed
# the blobs. No source-table scan and no Azure upload, so the table can be built while
# the upload is still in progress.
IMAGE_ID_COL = "image_id"
EXPANSION_INDEX_COL = "expansion_index"
URL_COL = "url"
ACCOUNT_COL = "account"
CONTAINER_COL = "container"
OBJECT_KEY_COL = "object_key"
PREFIX_ID_COL = "prefix_id"
TARGET_BUCKET_COL = "target_bucket"
TARGET_BYTES_COL = "target_bytes"
IMAGE_FORMAT_COL = "image_format"

# Default logical rows per source image (10 logical rows per object → 5B→50B).
DEFAULT_EXPANSION_FACTOR = 10

# Reference-table build defaults (local multiprocessing on one large pod).
DEFAULT_BUILD_WORKERS = 16
DEFAULT_COMMIT_FRAGMENTS = 500
# Lance data-storage format version the reference table is written in. Mirrors
# the literal accepted by ``lance.write_dataset``, so an unsupported --data-
# storage-version fails at config time instead of mid-build.
DataStorageVersion = Literal[
    "stable", "2.0", "2.1", "2.2", "2.3", "next", "legacy", "0.1"
]
DATA_STORAGE_VERSIONS: tuple[str, ...] = get_args(DataStorageVersion)
DATA_STORAGE_VERSION: DataStorageVersion = "2.1"

# Multi-base reference tables (build-ref-table --table-base-accounts). Fragment
# DATA is spread across separate storage accounts for aggregate throughput while
# the dataset root / manifests stay in the primary account. Bases are named
# ``base_1``, ``base_2``, ... in account order, and each base dataset lives at
# ``<container>/<prefix>/<run-id>/<account>/base.lance``. Empty accounts list =
# single-base (default). Requires a pylance build with the multi-base write API
# (>= 9.0.0-beta.15).
DEFAULT_TABLE_BASE_PREFIX = "loadtest/table-bases"

# Sanity ceiling for download-images --download-concurrency (threads per batch in the
# batched downloader). A secondary per-knob guard against typos; the real protection is
# the in-flight product guard below. The useful band is single/double digits.
MAX_DOWNLOAD_CONCURRENCY = 512

# Same ceiling for upload-images --upload-concurrency (threads per batch in the
# batched uploader).
MAX_UPLOAD_CONCURRENCY = 512

# Same ceiling for normalize --normalize-concurrency (per-actor image-transform threads
# per batch in the batched normalizer). These are CPU transforms, not network requests;
# the real protection is the in-flight product guard below.
MAX_NORMALIZE_CONCURRENCY = 512

# Same ceiling for phash --phash-concurrency (per-actor hash-compute threads per batch
# in the batched pHash UDF). These are CPU computations, not network requests; the real
# protection is the in-flight product guard below.
MAX_PHASH_CONCURRENCY = 512

# Default hard ceiling on estimated in-flight GETs for the batched downloader:
# concurrency * intra_concurrency * download_concurrency. ~100K IOPS needs only a few
# thousand in-flight (IOPS * latency), so this is generous headroom; raise
# --max-in-flight to launch above it intentionally.
DEFAULT_MAX_IN_FLIGHT = 50_000

# download-images backfill write strategies. ``fragment`` is geneva's default
# carry-forward path (whole-fragment column rewrite). ``sparse_rows`` is the
# sparse row-update engine (delete-by-address + append; repair-only — see
# download_images). Plain strings so this module never imports geneva at parse
# time; a unit test asserts UPDATE_MODE_SPARSE matches geneva's
# SPARSE_UPDATE_MODE constant.
UPDATE_MODE_FRAGMENT = "fragment"
UPDATE_MODE_SPARSE = "sparse_rows"
UPDATE_MODES: tuple[str, ...] = (UPDATE_MODE_FRAGMENT, UPDATE_MODE_SPARSE)

# --- Blob encoding ----------------------------------------------------------

# Lance blob marker. Must live inside the struct's own ``image_bytes`` field
# (see plan: single-struct add_columns adds ``pa.field(col, udf.data_type)``
# directly, so nested field metadata is what carries the marker).
BLOB_ENCODING_KEY = "lance-encoding:blob"
MMLB_BLOB_META = {BLOB_ENCODING_KEY: "true"}

# --- Target blob-size distribution -----------------------------------------

# (bucket_name, lo_bytes_inclusive, hi_bytes_exclusive, weight). Verbatim from
# the benchmark spec; the extrapolated >64 MiB tail is ~100k rows at 50B and is
# disabled by default for smoke runs (see image_distribution.clamp_target).
SIZE_BUCKETS: list[tuple[str, int, int, float]] = [
    ("lt_1kib", 1, 1 << 10, 0.0227),
    ("1_4kib", 1 << 10, 4 << 10, 0.0686),
    ("4_16kib", 4 << 10, 16 << 10, 0.1849),
    ("16_64kib", 16 << 10, 64 << 10, 0.3344),
    ("64_256kib", 64 << 10, 256 << 10, 0.2736),
    ("256kib_1mib", 256 << 10, 1 << 20, 0.0929),
    ("1_4mib", 1 << 20, 4 << 20, 0.0200),
    ("4_16mib", 4 << 20, 16 << 20, 0.0027),
    ("16_64mib", 16 << 20, 64 << 20, 0.0002),
    ("gt_64mib", 64 << 20, 128 << 20, 0.000002),
]

# Largest bucket whose hi <= 64 MiB; the >64 MiB tail is folded here when
# BENCH_INCLUDE_LARGE_TAIL is false.
LARGE_TAIL_THRESHOLD = 64 << 20

# --- Deterministic hash streams --------------------------------------------

# Fixed 64-bit salts xor'd with row_index before hashing to decorrelate the
# bucket choice, in-bucket target size, image format, padding, account, prefix,
# and reference-table shuffle streams (so e.g. a large object is not
# preferentially on one account, and the shuffle is independent of placement).
MASK64 = (1 << 64) - 1
BUCKET_SALT = 0xA5A5_A5A5_A5A5_A5A5
TARGET_SALT = 0x5A5A_5A5A_5A5A_5A5A
FORMAT_SALT = 0x3C3C_3C3C_3C3C_3C3C
PAD_SALT = 0xC3C3_C3C3_C3C3_C3C3
ACCOUNT_SALT = 0x1F1F_1F1F_1F1F_1F1F
PREFIX_SALT = 0xE1E1_E1E1_E1E1_E1E1
# Reference-table Feistel round-function salt (fresh byte pattern; the taken
# patterns are A5,5A,3C,C3,1F,E1 here plus 66/11/22/33/44 in the inject modules).
SHUFFLE_SALT = 0x9D9D_9D9D_9D9D_9D9D

# --- MMLB-compatible image attributes --------------------------------------

# Ported verbatim from mmlb/rust/mmlb/src/{config,generator,image_gen}.rs so the
# derived text/font/background are deterministic and consistent with MMLB. Note
# fidelity here is byte-size only; exact pixels do not matter for the benchmark.
FONTS: tuple[str, ...] = ("Helvetica", "Times New Roman")

BACKGROUND_COLORS: list[tuple[str, tuple[int, int, int]]] = [
    ("white", (255, 255, 255)),
    ("green", (144, 238, 144)),
    ("red", (255, 182, 193)),
    ("blue", (173, 216, 230)),
    ("yellow", (255, 255, 224)),
]

MAX_SUMMARY_END_TRIM_WORD_COUNT = 5

# Pillow font-file mapping. The directory is overridable via BENCH_FONT_DIR;
# rendering falls back to Pillow's default font when a file is unavailable.
DEFAULT_FONT_DIR: str | None = None
FONT_FILE_MAP: dict[str, str] = {
    "Helvetica": "DejaVuSans.ttf",
    "Times New Roman": "DejaVuSerif.ttf",
    "Courier New": "DejaVuSansMono.ttf",
}

# Rendering constants (mmlb image_gen.rs): base sizes are calibrated at 224px.
DEFAULT_IMAGE_SIZE = 224
BASE_FONT_SIZE = 32.0
BASE_LINE_HEIGHT = 40
WORDS_PER_LINE = 6
TEXT_COLOR = (0, 0, 0)

# --- Output-column naming (suffix-based) ------------------------------------

# Scalar metadata fields emitted (via UnpackedUDF) alongside the image struct.
META_FIELDS: tuple[str, ...] = (
    "summary_in_image",
    "font",
    "background_color",
    "image_size_bucket",
    "image_target_bytes",
    "image_actual_bytes",
    "image_format",
)


def validate_suffix(suffix: str) -> str:
    """Return ``suffix`` if it is safe for column/identifier construction.

    The metadata prefix ``img_meta_{suffix}_`` must be a valid Python
    identifier (UnpackedUDF requires it), so the suffix is restricted to
    ``[A-Za-z0-9_]`` and must not be empty.
    """
    if not suffix:
        raise ValueError("benchmark suffix must not be empty")
    if not suffix.replace("_", "").isalnum() or not suffix.isascii():
        raise ValueError(
            f"benchmark suffix {suffix!r} must contain only letters, digits, and "
            "underscores"
        )
    if not f"img_meta_{suffix}_".isidentifier():
        raise ValueError(f"benchmark suffix {suffix!r} is not identifier-safe")
    return suffix


def struct_col(suffix: str) -> str:
    """Nested image-struct column name. Blob input path is ``<col>.image_bytes``."""
    return f"summary_image_nested_{validate_suffix(suffix)}"


def meta_prefix(suffix: str) -> str:
    """Identifier prefix for the unpacked scalar metadata columns."""
    return f"img_meta_{validate_suffix(suffix)}_"


def meta_cols(suffix: str) -> list[str]:
    """All scalar metadata column names for a suffix."""
    prefix = meta_prefix(suffix)
    return [f"{prefix}{field}" for field in META_FIELDS]


def actual_bytes_col(suffix: str) -> str:
    """Convenience accessor for the ``image_actual_bytes`` scalar column."""
    return f"{meta_prefix(suffix)}image_actual_bytes"


def target_bytes_col(suffix: str) -> str:
    """Convenience accessor for the ``image_target_bytes`` scalar column."""
    return f"{meta_prefix(suffix)}image_target_bytes"


def ingest_seed_id_col(suffix: str) -> str:
    """Downloaded-image seed-image-id column (the compact source reference)."""
    return f"ingest_seed_image_id_{validate_suffix(suffix)}"


def ingest_url_col(suffix: str) -> str:
    """Downloaded-image source-URL column (also the ingest resume anchor)."""
    return f"ingest_source_url_{validate_suffix(suffix)}"


def norm_col(suffix: str) -> str:
    """Normalized-image struct column name."""
    return f"image_norm_{validate_suffix(suffix)}"


def phash_col(suffix: str) -> str:
    """Perceptual-hash column name."""
    return f"phash_{validate_suffix(suffix)}"


def manifest_name(suffix: str) -> str:
    """Geneva manifest name for a benchmark variant."""
    return f"azure_scale_bench_{validate_suffix(suffix)}"


def edge_table(suffix: str) -> str:
    """Dedupe edge-list view name."""
    return f"dedupe_edges_{validate_suffix(suffix)}"


def cluster_table(suffix: str) -> str:
    """Dedupe clusters (representative + duplicates) view name."""
    return f"dedupe_clusters_{validate_suffix(suffix)}"


def groups_table(suffix: str) -> str:
    """Exploded per-row dedupe-groups table name."""
    return f"dedupe_groups_{validate_suffix(suffix)}"


def curated_table(suffix: str) -> str:
    """Curated (post-dedupe) output table name."""
    return f"curated_{validate_suffix(suffix)}"


def dedupe_table_names(suffix: str) -> list[str]:
    """All dedupe/curate view/table names a suffix may have produced."""
    return [
        edge_table(suffix),
        cluster_table(suffix),
        groups_table(suffix),
        curated_table(suffix),
    ]


def all_suffix_columns(
    suffix: str, *, include_norm: bool = True, include_phash: bool = True
) -> list[str]:
    """Every output column a suffix may have produced (for cleanup)."""
    cols = [struct_col(suffix), *meta_cols(suffix)]
    if include_norm:
        cols.append(norm_col(suffix))
    if include_phash:
        cols.append(phash_col(suffix))
    return cols


# --- Loose-object upload job (image-dataset seeding) ------------------------

# Stamped into the seed-run config + the upload UDF version, so a generator or
# distribution change is detectable and never silently reuses old output.
# v2: structured procedural images (gradient + shapes + lines) replacing the
# original white-noise pixels, for pHash/dedupe realism.
GENERATOR_VERSION = "2"
DISTRIBUTION_VERSION = "1"

DEFAULT_OBJECT_COUNT = 100_000_000
DEFAULT_PREFIX_COUNT = 8192
# Smaller-than-data fragmenting so 100M objects shard into ~1000 fragments for
# scheduling granularity across a large worker fleet (1M/frag is too coarse).
DEFAULT_SEED_ROWS_PER_FRAGMENT = 100_000
DEFAULT_LIFECYCLE_MONTHS = 6
DEFAULT_LOOSE_CONTAINER = "datasets"
DEFAULT_BASE_PREFIX = "loadtest/images"

# Pip deps the benchmark UDFs import WORKER-side, registered once via the
# `define-upload-manifest` subcommand so a single manifest serves the whole pipeline
# on a cluster (else a backfill fails per-row with ModuleNotFoundError):
#   upload render + Azure PUT -> azure-storage-blob, azure-identity, pillow, numpy
#   download GET              -> azure-storage-blob, azure-identity
#   normalize / phash         -> pillow, numpy, imagehash
# Per-stage extras are harmless; one superset manifest keeps the runbook simple.
UPLOAD_WORKER_PIP_DEPS: tuple[str, ...] = (
    "azure-storage-blob",
    "azure-identity",
    "pillow",
    "numpy",
    "imagehash",
)

# Lance/Geneva worker pins + extra indexes matching the validated cluster smoke.
UPLOAD_MANIFEST_LANCE_DEPS: tuple[str, ...] = (
    "pyarrow",
    "lancedb==0.34.0b4",
    "pylance==9.0.0b21",
)
UPLOAD_MANIFEST_EXTRA_INDEX_URLS: tuple[str, ...] = (
    "https://pypi.fury.io/lancedb/",
    "https://pypi.fury.io/lance-format/",
)
