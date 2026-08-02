# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Utilities for building stable checkpoint keys.

This module centralizes the hashing and formatting logic so both UDFs and
map tasks can compose checkpoint keys consistently.
"""

import hashlib
from collections.abc import Iterable
from typing import Any, cast


def hash_string(value: str | None) -> str:
    """Return a stable md5 hex digest for the given string (or empty).

    The empty string is used for ``None`` values so that the hash is
    deterministic and safe for filesystem paths.
    """

    hasher = hashlib.md5()
    hasher.update((value or "").encode())
    return hasher.hexdigest()


def format_checkpoint_prefix(
    *,
    udf_name: str,
    udf_version: str,
    column: str,
    where: str | None,
    dataset_uri: str,
    src_files_hash: str | None = None,
) -> str:
    """Compose the prefix portion of a checkpoint key.

    The returned string follows the convention:
    ``udf-{name}_ver-{version}_col-{column}_where-{hash(where)}_uri-{hash(uri)}_srcfiles-{hash(srcfiles)}``
    """
    prefix = (
        f"udf-{udf_name}_ver-{udf_version}"
        f"_col-{column}_where-{hash_string(where)}"
        f"_uri-{hash_string(dataset_uri)}"
    )
    if src_files_hash is not None:
        prefix = f"{prefix}_srcfiles-{src_files_hash}"
    return prefix


def hash_source_files(files: Iterable[str] | None) -> str:
    """Return a stable hash for a set of source file paths."""
    if not files:
        return hash_string("")
    joined = "\n".join(sorted(files))
    return hash_string(joined)


def format_checkpoint_key(prefix: str, *, frag_id: int, start: int, end: int) -> str:
    """Attach fragment and range information to a checkpoint prefix."""

    return f"{prefix}_frag-{frag_id}_range-{start}-{end}"


# ---------------------------------------------------------------------------
# UDTF checkpoint key helpers
# ---------------------------------------------------------------------------


def format_udtf_checkpoint_prefix(
    *,
    udtf_name: str,
    udtf_version: str,
    source_version: int,
) -> str:
    """Top-level prefix: ``udtf_{name}_{version}_src-{source_version}``."""
    return f"udtf_{udtf_name}_{udtf_version}_src-{source_version}"


def format_udtf_partition_prefix(
    top_prefix: str,
    *,
    partition_col: str | None,
    partition_value: object,
) -> str:
    """Partition prefix within a UDTF checkpoint.

    Returns ``{top_prefix}___all__`` for unpartitioned UDTFs, or
    ``{top_prefix}_{col}={sanitized_value}`` for partitioned ones.
    """
    if partition_col is None:
        return f"{top_prefix}___all__"
    # Sanitize: replace _ with - to avoid collision with key separator
    sanitized = str(partition_value).replace("_", "-")
    return f"{top_prefix}_{partition_col}={sanitized}"


def format_udtf_batch_key(partition_prefix: str, batch_idx: int) -> str:
    """Full batch key: ``{partition_prefix}_batch-{idx:04d}``."""
    return f"{partition_prefix}_batch-{batch_idx:04d}"


def format_udtf_fragment_key(partition_prefix: str) -> str:
    """Checkpoint key for the FragmentMetadata of a completed partition."""
    return f"{partition_prefix}_fragment"


def parse_udtf_batch_index(key: str) -> int | None:
    """Extract the batch index from a UDTF batch key.

    Returns the integer batch index, or *None* if *key* is not a
    batch key (e.g. a done-marker).
    """
    if "_batch-" not in key:
        return None
    try:
        return int(key.rsplit("_batch-", 1)[1])
    except (ValueError, IndexError):
        return None


# ---------------------------------------------------------------------------
# Chunker checkpoint key helpers
# ---------------------------------------------------------------------------


def format_chunker_checkpoint_prefix(
    *,
    chunker_name: str,
    chunker_version: str,
    source_version: int,
) -> str:
    """Top-level prefix: ``chunker_{name}_{version}_src-{source_version}``."""
    return f"chunker_{chunker_name}_{chunker_version}_src-{source_version}"


def _normalize_row_id(row_id: object) -> int:
    if hasattr(row_id, "as_py"):
        row_id = cast("Any", row_id).as_py()
    if row_id is None:
        raise ValueError("row_ids must not contain None")
    return int(cast("Any", row_id))


def format_chunker_work_item_key(top_prefix: str, row_ids: Iterable[int]) -> str:
    """Checkpoint key for a chunker work item identified by row-id range."""
    iterator = iter(row_ids)
    try:
        first = _normalize_row_id(next(iterator))
    except StopIteration:
        raise ValueError("row_ids must not be empty") from None

    previous = first
    for row_id in iterator:
        current = _normalize_row_id(row_id)
        if current != previous + 1:
            raise ValueError("row_ids must be strictly ordered and contiguous by 1")
        previous = current
    return f"{top_prefix}_rowids-{first}-{previous}"


def format_chunker_fragment_key(work_item_key: str) -> str:
    """Checkpoint key for the FragmentMetadata of a completed chunker work item."""
    return f"{work_item_key}_fragment"
