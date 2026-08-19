# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Create and validate the shallow-clone benchmark table.

A shallow clone copies only dataset metadata and references — no data files are
rewritten — so benchmark writes never touch the read-only source. Implemented
with ``lance.LanceDataset.shallow_clone``.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import attrs

from loadtest.azure_scale_bench import benchmark_env, inventory

if TYPE_CHECKING:
    import lance

_LOG = logging.getLogger(__name__)


@attrs.define
class CloneResult:
    """Outcome of a clone operation."""

    source_uri: str
    target_uri: str
    created: bool
    source_version: int
    target_version: int
    rows_match: bool
    fragments_match: bool


def _exists(uri: str, storage_options: dict[str, str]) -> bool:
    """Return True if a Lance dataset can be opened at ``uri``."""
    try:
        benchmark_env.open_lance(uri, storage_options)
    except Exception as exc:  # noqa: BLE001 - absence is the expected path
        _LOG.debug("target %s not present: %s", uri, exc)
        return False
    return True


def clone_table(
    source_uri: str,
    target_uri: str,
    storage_options: dict[str, str],
    *,
    reference: tuple[str | None, int | None] = (None, None),
    recreate: bool = False,
) -> CloneResult:
    """Create the benchmark clone if absent, then validate source vs clone.

    The source is never modified. If the target already exists and ``recreate``
    is False, the existing clone is validated and returned (idempotent). The
    ``reference`` selects the source version to clone; ``(None, None)`` is the
    latest version on the main branch.
    """
    if recreate and _exists(target_uri, storage_options):
        raise RuntimeError(
            f"refusing to recreate existing clone {target_uri}; drop it manually "
            "first to avoid accidental data loss"
        )

    created = False
    if not _exists(target_uri, storage_options):
        src: lance.LanceDataset = benchmark_env.open_lance(source_uri, storage_options)
        _LOG.info(
            "creating shallow clone %s <- %s (version %s)",
            target_uri,
            source_uri,
            src.version,
        )
        src.shallow_clone(target_uri, reference, storage_options=storage_options)
        created = True
    else:
        _LOG.info("clone already exists: %s", target_uri)

    return _validate(source_uri, target_uri, storage_options, created=created)


def _validate(
    source_uri: str,
    target_uri: str,
    storage_options: dict[str, str],
    *,
    created: bool,
) -> CloneResult:
    """Open source and clone, compare row/fragment counts, log versions."""
    src_inv = inventory.describe(source_uri, storage_options)
    dst_inv = inventory.describe(target_uri, storage_options)
    if not src_inv.exists:
        raise RuntimeError(f"source dataset not openable after clone: {source_uri}")
    if not dst_inv.exists:
        raise RuntimeError(f"clone not openable after creation: {target_uri}")

    assert src_inv.version is not None
    assert dst_inv.version is not None
    rows_match = src_inv.num_rows == dst_inv.num_rows
    fragments_match = src_inv.num_fragments == dst_inv.num_fragments
    _LOG.info(
        "clone validated: source v%s (%s rows, %s frags) | clone v%s "
        "(%s rows, %s frags) | rows_match=%s fragments_match=%s",
        src_inv.version,
        f"{src_inv.num_rows:,}",
        f"{src_inv.num_fragments:,}",
        dst_inv.version,
        f"{dst_inv.num_rows:,}",
        f"{dst_inv.num_fragments:,}",
        rows_match,
        fragments_match,
    )
    if not (rows_match and fragments_match):
        _LOG.warning("clone row/fragment counts do not match source")

    return CloneResult(
        source_uri=source_uri,
        target_uri=target_uri,
        created=created,
        source_version=src_inv.version,
        target_version=dst_inv.version,
        rows_match=rows_match,
        fragments_match=fragments_match,
    )
