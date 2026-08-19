# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Shared backfill-runner helpers used by expand / normalize / phash.

Centralizes fragment windowing, Table.backfill keyword mapping, the
cluster/manifest context, and the explicit rerun (overwrite / reuse / error)
semantics so every stage behaves identically.
"""

from __future__ import annotations

import contextlib
import logging
import os
from typing import TYPE_CHECKING, Any

import attrs

if TYPE_CHECKING:
    from loadtest.azure_scale_bench.benchmark_env import BenchConfig

_LOG = logging.getLogger(__name__)


def fragment_window_where(cfg: BenchConfig) -> str | None:
    """Build a row_index range clause for ``--num-frags``/``--skip-frags``.

    Source rows are sequential and packed ``cfg.rows_per_fragment`` per fragment,
    so a fragment window is a row_index range (no fragment-select API needed).
    Combined (AND) with any explicit repair ``--where``. Returns ``None`` when no
    window and no filter are set (so backfill uses its ``<col> IS NULL`` default).
    """
    clauses: list[str] = []
    if cfg.num_frags is not None or cfg.skip_frags is not None:
        skip = cfg.skip_frags or 0
        lo = skip * cfg.rows_per_fragment
        clauses.append(f"{cfg.row_index_col} >= {lo}")
        if cfg.num_frags is not None:
            hi = (skip + cfg.num_frags) * cfg.rows_per_fragment
            clauses.append(f"{cfg.row_index_col} < {hi}")
    if cfg.where:
        clauses.append(f"({cfg.where})")
    return " AND ".join(clauses) if clauses else None


def backfill_kwargs(
    cfg: BenchConfig,
    *,
    num_fragments: int | None = None,
    blob_read_strategy: str | None = None,
) -> dict:
    """Translate BenchConfig into Table.backfill keyword args."""
    kwargs: dict[str, Any] = {
        "concurrency": cfg.concurrency,
        "intra_applier_concurrency": cfg.intra_concurrency,
    }
    where = fragment_window_where(cfg)
    if where is not None:
        kwargs["where"] = where
    if blob_read_strategy is not None:
        kwargs["blob_read_strategy"] = blob_read_strategy
    if cfg.task_size is not None:
        kwargs["task_size"] = cfg.task_size
    if cfg.min_checkpoint_size is not None:
        kwargs["min_checkpoint_size"] = cfg.min_checkpoint_size
    if cfg.max_checkpoint_size is not None:
        kwargs["max_checkpoint_size"] = cfg.max_checkpoint_size
    if cfg.flush_interval_seconds is not None:
        kwargs["batch_checkpoint_flush_interval_seconds"] = cfg.flush_interval_seconds
    if cfg.commit_granularity_pct is not None and num_fragments:
        granularity = max(1, int(num_fragments * cfg.commit_granularity_pct / 100))
        kwargs["commit_granularity"] = granularity
    return kwargs


def sparse_update_kwargs(
    cfg: BenchConfig,
    *,
    num_fragments: int | None = None,
) -> dict:
    """Translate BenchConfig into run_ray_sparse_update keyword args.

    The sparse engine takes only ``concurrency`` (actor pool size), ``where``,
    and ``commit_granularity``; it has no checkpoint store or task sizing, so
    those knobs are meaningless there. Any that are set get one warning so a
    fragment-mode command line reused with ``--update-mode sparse_rows`` is not
    silently misleading. The row_index window from ``fragment_window_where`` is
    value-based, so it composes with sparse (which relocates repaired rows into
    appended fragments); window/fragment alignment is only physical before the
    first sparse pass.
    """
    kwargs: dict[str, Any] = {"concurrency": cfg.concurrency}
    where = fragment_window_where(cfg)
    if where is not None:
        kwargs["where"] = where
    if cfg.commit_granularity_pct is not None and num_fragments:
        granularity = max(1, int(num_fragments * cfg.commit_granularity_pct / 100))
        kwargs["commit_granularity"] = granularity
    elif num_fragments:
        # The engine chunks fragment ranges by commit granularity and sizes its
        # actor pool at min(concurrency, num_ranges); its own auto default
        # (>= num_fragments/20 per chunk) caps the pool at 20 actors. Size the
        # ranges to fill the requested pool instead; --commit-granularity-pct
        # overrides explicitly.
        kwargs["commit_granularity"] = max(1, num_fragments // max(1, cfg.concurrency))
    ignored = [
        name
        for name, value in (
            ("task_size", cfg.task_size),
            ("checkpoint_size", cfg.checkpoint_size),
            ("min_checkpoint_size", cfg.min_checkpoint_size),
            ("max_checkpoint_size", cfg.max_checkpoint_size),
            ("flush_interval_seconds", cfg.flush_interval_seconds),
            ("batch_size", cfg.batch_size),
        )
        if value is not None
    ]
    if cfg.intra_concurrency != 1:
        ignored.append("intra_concurrency")
    # Sparse actors schedule at Ray defaults (no udf.memory reservation), so a
    # non-default per-actor memory budget is a no-op there.
    default_memory = attrs.fields(type(cfg)).per_actor_memory_gib.default
    if cfg.per_actor_memory_gib != default_memory:
        ignored.append("per_actor_memory_gib")
    # Same story for the CPU reservation: the sparse repair UDF reserves no
    # resources, so --per-actor-cpus is a no-op under sparse update_mode.
    if cfg.per_actor_cpus is not None:
        ignored.append("per_actor_cpus")
    if ignored:
        _LOG.warning(
            "sparse update_mode has no checkpointing or task sizing; ignoring: %s",
            ", ".join(ignored),
        )
    return kwargs


def read_blob_bytes(value: Any) -> bytes | None:
    """Coerce a UDF blob argument to bytes.

    The range blob reader passes a file-like ``BufferBackedBlobFile`` (with a
    ``.read()``), not raw bytes; plain reads/tests pass ``bytes`` directly. Both
    are handled here. Returns ``None`` for null/unreadable input.
    """
    if value is None:
        return None
    if isinstance(value, bytes | bytearray | memoryview):
        return bytes(value)
    read = getattr(value, "read", None)
    if callable(read):
        data: Any = read()
        return bytes(data) if data else None
    return None


def scoped_row_count(cfg: BenchConfig, count_rows: Any) -> int:
    """Effective row count for a run — the rows actually being processed, used to
    size duplicate-injection groups to the run scope, not the whole clone.

    ``count_rows`` is a callable accepting an optional filter string.
      * pure ``--num-frags`` (no ``--where``): arithmetic from the fragment
        layout — exact window size, skip-independent, no query.
      * any other scope (``--skip-frags`` alone, ``--where``, window + where):
        count the rows matching the combined ``fragment_window_where`` filter
        (arbitrary predicates / open-ended skip windows can't be derived
        arithmetically).
      * no scope at all: the full table count.
    """
    where = fragment_window_where(cfg)
    if where is None:
        return count_rows()
    if cfg.num_frags is not None and not cfg.where:
        return cfg.num_frags * cfg.rows_per_fragment
    return count_rows(where)


def udf_size_kwargs(cfg: BenchConfig) -> dict[str, int]:
    """The non-None batch/checkpoint sizing kwargs for a @geneva.udf call."""
    return {
        key: value
        for key, value in (
            ("batch_size", cfg.batch_size),
            ("checkpoint_size", cfg.checkpoint_size),
            ("min_checkpoint_size", cfg.min_checkpoint_size),
            ("max_checkpoint_size", cfg.max_checkpoint_size),
        )
        if value is not None
    }


def udf_resource_kwargs(cfg: BenchConfig) -> dict[str, Any]:
    """Per-actor Ray resource kwargs for a @geneva.udf call.

    Always reserves per-actor memory; adds an explicit CPU reservation only when
    ``--per-actor-cpus`` is set. When unset, ``num_cpus`` is omitted so the geneva
    UDF default (1 CPU) stands and actor scheduling is unchanged.
    """
    kwargs: dict[str, Any] = {"memory": int(cfg.per_actor_memory_gib * 1024**3)}
    if cfg.per_actor_cpus is not None:
        kwargs["num_cpus"] = cfg.per_actor_cpus
    return kwargs


def apply_blob_read_buffer(cfg: BenchConfig) -> None:
    """Set the range blob-read buffer env. Driver-only — warn on a cluster.

    The env var only affects the process that reads it; KubeRay workers (which do
    the blob IO) inherit it only via the manifest env_vars, so on a real cluster
    it must also be set there.
    """
    if cfg.blob_read_buffer_size is None:
        return
    os.environ["GENEVA_RANGE_BLOB_READ_BUFFER_SIZE"] = str(cfg.blob_read_buffer_size)
    if cfg.cluster:
        _LOG.warning(
            "--blob-read-buffer set the DRIVER env only; on a cluster also set "
            "GENEVA_RANGE_BLOB_READ_BUFFER_SIZE in the manifest env_vars so workers "
            "honor it"
        )


def context(conn: Any, cfg: BenchConfig) -> Any:
    """Enter a Geneva cluster/manifest context only when a cluster is configured.

    ``conn.context`` requires a cluster, so ``--manifest`` without ``--cluster``
    is meaningless — warn and run locally rather than raising TypeError.
    """
    if not cfg.cluster:
        if cfg.manifest:
            _LOG.warning("--manifest %r ignored without --cluster", cfg.manifest)
        return contextlib.nullcontext()
    ctx_kwargs: dict[str, str] = {"cluster": cfg.cluster}
    if cfg.manifest:
        ctx_kwargs["manifest"] = cfg.manifest
    else:
        # Backfill UDFs import third-party deps worker-side (pillow / numpy /
        # imagehash / azure-storage-blob) that the base image may lack; without a
        # manifest the workers fail per-row with ModuleNotFoundError. Make that
        # actionable rather than cryptic.
        _LOG.warning(
            "running on cluster %r without --manifest: worker UDFs need their pip "
            "deps (pillow/numpy/imagehash/azure-storage-blob). Register one with "
            "`define-upload-manifest --manifest <name> --account-name <acct>` and pass "
            "--manifest <name> on every backfill stage.",
            cfg.cluster,
        )
    return conn.context(**ctx_kwargs)


def resolve_existing_columns(
    tbl: Any,
    cfg: BenchConfig,
    output_cols: list[str],
    *,
    stage: str,
    reapplies_udf: bool = False,
) -> None:
    """Apply explicit rerun semantics to a stage's existing output columns.

    On existing columns the caller must have set ``--overwrite`` (drop them) or
    ``--reuse-existing`` / ``--where`` (keep and continue filling). Otherwise we
    refuse, so a knob change can never silently reuse stale output.

    ``reapplies_udf`` tells the warning the truth for stages that pass a freshly
    built UDF to ``backfill(..., udf=...)`` on reuse (download/normalize/phash):
    changed knobs DO take effect on the reprocessed rows. Stages that reuse the
    column's stored UDF (e.g. expand) leave it ``False``.
    """
    existing = [c for c in output_cols if tbl.schema.get_field_index(c) >= 0]
    if not existing:
        return
    if cfg.overwrite:
        _LOG.info("[%s] overwrite: dropping existing columns: %s", stage, existing)
        tbl.drop_columns(existing)
    elif cfg.reuse_existing or cfg.where:
        if reapplies_udf:
            _LOG.warning(
                "[%s] reusing existing columns for suffix %r; backfill re-applies the "
                "CURRENT UDF to the selected rows, so changed knobs take effect on "
                "those rows (use --overwrite to rebuild every row, or a new --suffix)",
                stage,
                cfg.suffix,
            )
        else:
            _LOG.warning(
                "[%s] reusing existing columns for suffix %r; backfill continues with "
                "the column's ORIGINAL parameters (changed knobs are ignored — use "
                "--overwrite or a new --suffix to apply new ones)",
                stage,
                cfg.suffix,
            )
    else:
        raise RuntimeError(
            f"[{stage}] columns for suffix {cfg.suffix!r} already exist: {existing}. "
            "Pass --overwrite to drop and regenerate, --reuse-existing to continue "
            "filling, or choose a new --suffix."
        )
