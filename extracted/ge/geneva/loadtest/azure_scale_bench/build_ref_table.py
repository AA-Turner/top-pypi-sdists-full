# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Single-pass, shuffled reference-table generator (``build-ref-table``).

Builds a standalone Lance table of ``M`` rows that *reference* already-uploaded
Azure blobs, without scanning a source table or uploading anything. Every column
is a pure function of ``image_id`` plus the seed-run config, so the table can be
built while the upload is still in progress.

Mapping (the shuffle):

    logical         = feistel(row_index, M, shuffle_salt)  # bijection on [0, M)
    image_id        = logical % N                           # N = object_count
    expansion_index = logical // N

A Feistel permutation gives a true (non-block) distribution: each image appears
``M / N`` times (exactly, when ``M % N == 0``; otherwise ±1), every
``(image_id, expansion_index)`` pair is unique, and consecutive rows hold
unrelated image ids (effectively no adjacent duplicates).

Derivation matches ``upload_images`` byte-for-byte (the correctness boundary): the
locator columns (``url`` / ``account`` / ``object_key`` / ``prefix_id``) are pure
64-bit integer hashing + string templates and are vectorized exactly; the size
columns (``target_bucket`` / ``target_bytes``) use the float distribution in
``image_distribution`` and are informational (the download stage never reads them).

The build runs locally on one large pod: a ``spawn`` ``ProcessPoolExecutor`` whose
workers each generate one fragment and write it with ``LanceFragment.create`` (no
commit); the driver consumes fragments in index order and batch-commits them via
``LanceOperation.Append``. Resume is driven by the dataset's row count (in-order
contiguous-prefix commits make it unambiguous); a ``<output>.progress.json`` sidecar
is written for operator clarity only.

Failure semantics: this is a SINGLE-WRITER build — do not run two builds against the
same output concurrently (their commits would race on ``read_version``). Committed
fragments are durable; on any mid-build failure, rerun the same command to resume
from the committed prefix (generation is deterministic, so the regenerated fragments
are identical). Fragment data files written but not yet committed when a build dies
are left untracked on storage and are harmless; reclaim them by rebuilding once with
``--overwrite``.
"""

from __future__ import annotations

import json
import logging
import os
import time
from concurrent.futures import Future, ProcessPoolExecutor
from multiprocessing import get_context
from typing import TYPE_CHECKING, Any, NamedTuple, cast

import numpy as np
import pyarrow as pa

from loadtest.azure_scale_bench import (
    constants,
    image_distribution,
    synthetic_image,
    upload_images,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from loadtest.azure_scale_bench.benchmark_env import BenchConfig

_LOG = logging.getLogger(__name__)

# --- Vectorized splitmix64 (must match image_distribution.row_hash exactly) ---
# All arithmetic is numpy uint64, which wraps mod 2**64; constants are cast to
# uint64 so a stray Python int can never promote an expression to float64.

_GOLDEN = np.uint64(0x9E3779B97F4A7C15)
_MIX_C1 = np.uint64(0xBF58476D1CE4E5B9)
_MIX_C2 = np.uint64(0x94D049BB133111EB)
_S30 = np.uint64(30)
_S27 = np.uint64(27)
_S31 = np.uint64(31)
_TWO64 = 2.0**64
_FEISTEL_ROUNDS = 4
_INT32_MAX = (1 << 31) - 1
# Per-fragment write retries (deterministic generation makes a retry safe).
_FRAGMENT_WRITE_ATTEMPTS = 3


def _vec_row_hash(x: np.ndarray) -> np.ndarray:
    """splitmix64 finalizer over a uint64 array (vectorized ``row_hash``)."""
    x = x.astype(np.uint64, copy=True)
    x = x + _GOLDEN
    x = (x ^ (x >> _S30)) * _MIX_C1
    x = (x ^ (x >> _S27)) * _MIX_C2
    return x ^ (x >> _S31)


def _vec_scatter(
    image_id: np.ndarray, seed_run_salt: int, stream_salt: int
) -> np.ndarray:
    """Vectorized ``upload_images._scatter``: row_hash(id ^ run_salt ^ stream)."""
    salt = np.uint64(seed_run_salt & constants.MASK64) ^ np.uint64(
        stream_salt & constants.MASK64
    )
    return _vec_row_hash(image_id.astype(np.uint64, copy=False) ^ salt)


def _vec_stream(image_id: np.ndarray, salt: int) -> np.ndarray:
    """Vectorized ``image_distribution._stream``: row_hash(id ^ salt)."""
    return _vec_row_hash(image_id.astype(np.uint64, copy=False) ^ np.uint64(salt))


def _vec_uniform01(h: np.ndarray) -> np.ndarray:
    """Map a uint64 hash array to float64 in [0, 1) (matches ``_uniform01``)."""
    return h.astype(np.float64) / _TWO64


# --- Feistel permutation over [0, M) with cycle-walking ---------------------


def _feistel_params(m: int) -> tuple[int, int]:
    """Half-width ``hbits`` and ``half_mask`` for a domain ``2**(2*hbits) >= m``."""
    bits = (m - 1).bit_length() if m > 1 else 0  # smallest b with 2**b >= m
    hbits = (bits + 1) // 2
    return hbits, (1 << hbits) - 1


def _round_keys(salt: int) -> list[np.uint64]:
    """Per-round Feistel keys, decorrelated by the shuffle salt and round index.

    Computed in Python ints (exact, masked) then cast to uint64 so the per-round
    multiply never trips a numpy scalar-overflow warning.
    """
    golden = 0x9E3779B97F4A7C15
    base = (constants.SHUFFLE_SALT ^ (salt & constants.MASK64)) & constants.MASK64
    return [
        np.uint64((base ^ ((i * golden) & constants.MASK64)) & constants.MASK64)
        for i in range(_FEISTEL_ROUNDS)
    ]


def _feistel_once(
    x: np.ndarray, *, hbits: int, half_mask: int, round_keys: list[np.uint64]
) -> np.ndarray:
    """One balanced Feistel permutation pass over the power-of-two domain."""
    if hbits == 0:  # domain size 1 (m == 1): identity
        return x
    hb = np.uint64(hbits)
    hm = np.uint64(half_mask)
    left = (x >> hb) & hm
    right = x & hm
    for key in round_keys:
        f = _vec_row_hash(right ^ key) & hm
        left, right = right, left ^ f
    return (left << hb) | right


def feistel(row_index: np.ndarray, *, m: int, salt: int) -> np.ndarray:
    """Bijective shuffle of ``[0, m)`` (Feistel network + cycle-walking).

    Returns a uint64 array; ``row_index`` values must lie in ``[0, m)``.
    """
    if m <= 0:
        raise ValueError(f"m must be > 0, got {m}")
    hbits, half_mask = _feistel_params(m)
    keys = _round_keys(salt)
    m_u = np.uint64(m)
    y = _feistel_once(
        row_index.astype(np.uint64, copy=False),
        hbits=hbits,
        half_mask=half_mask,
        round_keys=keys,
    )
    mask = y >= m_u  # walk values that fell outside [0, m) back in
    while mask.any():
        y[mask] = _feistel_once(
            y[mask], hbits=hbits, half_mask=half_mask, round_keys=keys
        )
        mask = y >= m_u
    return y


def map_rows(
    row_index: np.ndarray, *, n: int, m: int, salt: int
) -> tuple[np.ndarray, np.ndarray]:
    """Map ``row_index`` -> (``image_id``, ``expansion_index``) via the shuffle."""
    logical = feistel(row_index, m=m, salt=salt)
    n_u = np.uint64(n)
    return logical % n_u, logical // n_u


# --- Column derivation (locators exact; sizes informational) ----------------


def build_schema() -> pa.Schema:
    """The fixed reference-table schema (stable field order)."""
    return pa.schema(
        [
            pa.field(constants.ROW_INDEX_COL, pa.int64()),
            pa.field(constants.IMAGE_ID_COL, pa.int64()),
            pa.field(constants.EXPANSION_INDEX_COL, pa.int32()),
            pa.field(constants.URL_COL, pa.string()),
            pa.field(constants.ACCOUNT_COL, pa.string()),
            pa.field(constants.CONTAINER_COL, pa.string()),
            pa.field(constants.OBJECT_KEY_COL, pa.string()),
            pa.field(constants.PREFIX_ID_COL, pa.int32()),
            pa.field(constants.TARGET_BUCKET_COL, pa.string()),
            pa.field(constants.TARGET_BYTES_COL, pa.int64()),
            pa.field(constants.IMAGE_FORMAT_COL, pa.string()),
        ]
    )


def _format_keys(
    image_id: np.ndarray, prefix_id: np.ndarray, params: Any
) -> tuple[pa.Array, pa.Array]:
    """Build the ``object_key`` and ``url`` strings (the isolated, swappable seam).

    This is the likely bottleneck. It is deliberately the single place that formats
    strings so a faster path (pyarrow ``compute`` / numpy ``char``) can replace this
    v1 Python-list implementation without touching the rest of the generator. The
    templates match ``upload_images.object_key_for`` / ``url_for`` exactly.
    """
    base = params.base_prefix
    seed = params.seed_run_id
    ext = params.ext
    container = params.container
    ids = image_id.tolist()
    prefixes = prefix_id.tolist()
    object_keys = [
        f"{base}/{seed}/p{p:05d}/{i}.{ext}" for i, p in zip(ids, prefixes, strict=True)
    ]
    urls = [f"az://{container}/{k}" for k in object_keys]
    return pa.array(object_keys, pa.string()), pa.array(urls, pa.string())


def _derive_sizes(
    image_id: np.ndarray, *, include_large_tail: bool, max_bytes: int | None
) -> tuple[pa.Array, pa.Array]:
    """Vectorized ``image_distribution.assign``: (target_bucket, target_bytes).

    Bucket selection replicates the scalar running-sum compare exactly (same float
    op sequence); ``target_bytes`` uses log-uniform float math (``np.rint`` is
    round-half-to-even, matching Python ``round``) and is informational only.
    """
    if max_bytes is not None:
        buckets = image_distribution._capped_buckets(
            include_large_tail=include_large_tail, max_bytes=max_bytes
        )
    else:
        buckets = list(constants.SIZE_BUCKETS)

    u = _vec_uniform01(_vec_stream(image_id, constants.BUCKET_SALT))
    total = sum(weight for *_, weight in buckets)
    chosen = np.full(image_id.shape, len(buckets) - 1, dtype=np.int64)
    assigned = np.zeros(image_id.shape, dtype=bool)
    acc = 0.0
    for bi, (_name, _lo, _hi, weight) in enumerate(buckets):
        acc += weight / total
        sel = (~assigned) & (u < acc)
        chosen[sel] = bi
        assigned |= sel

    names = np.array([b[0] for b in buckets], dtype=object)
    los = np.array([b[1] for b in buckets], dtype=np.int64)
    his = np.array([b[2] for b in buckets], dtype=np.int64)
    name_arr = names[chosen]
    row_lo = los[chosen]
    row_hi = his[chosen]

    if max_bytes is None and not include_large_tail:
        tail = row_hi > constants.LARGE_TAIL_THRESHOLD
        if tail.any():
            t_name, t_lo, t_hi = image_distribution._largest_non_tail_bucket()
            name_arr = name_arr.copy()
            name_arr[tail] = t_name
            row_lo = row_lo.copy()
            row_hi = row_hi.copy()
            row_lo[tail] = t_lo
            row_hi[tail] = t_hi

    v = _vec_uniform01(_vec_stream(image_id, constants.TARGET_SALT))
    lo_eff = np.maximum(row_lo, 1).astype(np.float64)
    hi_f = row_hi.astype(np.float64)
    target = np.rint(np.exp(np.log(lo_eff) + v * (np.log(hi_f) - np.log(lo_eff))))
    target = np.minimum(np.maximum(target, lo_eff), hi_f - 1.0)

    return (
        pa.array(name_arr, pa.string()),
        pa.array(target.astype(np.int64), pa.int64()),
    )


def generate_fragment(start_row: int, num_rows: int, plan: _BuildPlan) -> pa.Table:
    """Generate one fragment of ``num_rows`` rows starting at ``start_row``.

    Pure and independent per row, so fragments can be built in any order/process.
    """
    params = plan.params
    r = np.arange(start_row, start_row + num_rows, dtype=np.uint64)
    image_id, expansion_index = map_rows(r, n=plan.n, m=plan.m, salt=plan.salt)

    salt = params.seed_run_salt
    acct_idx = (
        _vec_scatter(image_id, salt, constants.ACCOUNT_SALT)
        % np.uint64(len(params.accounts))
    ).astype(np.int64)
    prefix_id = (
        _vec_scatter(image_id, salt, constants.PREFIX_SALT)
        % np.uint64(params.prefix_count)
    ).astype(np.int64)

    accounts = np.array(list(params.accounts), dtype=object)
    object_key, url = _format_keys(image_id, prefix_id, params)
    target_bucket, target_bytes = _derive_sizes(
        image_id,
        include_large_tail=plan.include_large_tail,
        max_bytes=plan.max_bytes,
    )

    return pa.table(
        {
            constants.ROW_INDEX_COL: pa.array(r.astype(np.int64), pa.int64()),
            constants.IMAGE_ID_COL: pa.array(image_id.astype(np.int64), pa.int64()),
            constants.EXPANSION_INDEX_COL: pa.array(
                expansion_index.astype(np.int32), pa.int32()
            ),
            constants.URL_COL: url,
            constants.ACCOUNT_COL: pa.array(accounts[acct_idx], pa.string()),
            constants.CONTAINER_COL: pa.array(
                np.full(num_rows, params.container, dtype=object), pa.string()
            ),
            constants.OBJECT_KEY_COL: object_key,
            constants.PREFIX_ID_COL: pa.array(prefix_id.astype(np.int32), pa.int32()),
            constants.TARGET_BUCKET_COL: target_bucket,
            constants.TARGET_BYTES_COL: target_bytes,
            constants.IMAGE_FORMAT_COL: pa.array(
                np.full(num_rows, plan.image_format, dtype=object), pa.string()
            ),
        },
        schema=plan.schema,
    )


# --- Multi-base placement (spread fragment data across storage accounts) -----
#
# Optional (``--table-base-accounts``): the dataset root / manifests stay in the
# primary account (``cfg.storage_options``) while fragment DATA is round-robined
# across separate per-account Lance "bases" for aggregate write throughput. Bases
# are named ``base_1``, ``base_2``, ... in account order; each base dataset lives
# at ``<container>/<prefix>/<run-id>/<account>/base.lance``. These helpers are
# pure (no Lance import) so the specs are picklable into worker processes and
# unit-testable without infrastructure.


class _TableBase(NamedTuple):
    """One table-base target: stable name, dataset path, and backing account."""

    name: str
    path: str
    account: str


def _split_uri_scheme(uri: str) -> tuple[str | None, str | None, str]:
    """Split ``scheme://netloc/rest`` -> (scheme, netloc, rest).

    A local path (no ``://``) returns ``(None, None, uri)``.
    """
    if "://" not in uri:
        return None, None, uri
    scheme, rest = uri.split("://", 1)
    netloc, _sep, tail = rest.partition("/")
    return scheme, netloc, tail


def default_table_base_run_id(output_uri: str) -> str:
    """Default base-path run id: the output table name with ``.lance`` stripped."""
    tail = output_uri.rstrip("/").rsplit("/", 1)[-1]
    return tail.removesuffix(".lance")


def build_table_bases(
    *,
    output_uri: str,
    accounts: Sequence[str],
    prefix: str,
    run_id: str | None = None,
    container: str | None = None,
) -> tuple[_TableBase, ...]:
    """Ordered table-base specs (``base_1``..``base_N``) for ``accounts``.

    For a cloud output URI each base is an **account-qualified** ADLS-Gen2 URI
    ``abfss://<container>@<account>.dfs.core.windows.net/<prefix>/<run-id>/
    <account>/base.lance``: Lance resolves the base's storage account from the
    URI authority, so cross-account reads and writes need no ``base_store_params``
    (they work with managed identity / Entra ID) — this is what lets a Geneva
    backfill read and spread writes across the bases without any Geneva change.
    The account is repeated as a path segment for readability and base↔account
    reconciliation on resume. Local paths (tests) use the output table's parent
    directory. An empty ``accounts`` yields an empty tuple (single-base mode).
    """
    if not accounts:
        return ()
    prefix = prefix.strip("/")
    rid = run_id or default_table_base_run_id(output_uri)
    scheme, netloc, _tail = _split_uri_scheme(output_uri)
    if scheme is not None:
        # Container is the output URI's netloc (az://<container>/…) or the
        # authority's filesystem segment (abfss://<container>@<account>…).
        cont = container or (netloc.split("@", 1)[0] if netloc else "")
        if not cont:
            raise ValueError(
                f"cannot derive a container for table bases from {output_uri!r}; "
                "pass --table-base-container"
            )
        bases: list[_TableBase] = []
        for i, account in enumerate(accounts, start=1):
            path = (
                f"abfss://{cont}@{account}.dfs.core.windows.net"
                f"/{prefix}/{rid}/{account}/base.lance"
            )
            bases.append(_TableBase(name=f"base_{i}", path=path, account=account))
        return tuple(bases)

    parent = os.path.dirname(os.path.abspath(output_uri))
    root = os.path.join(parent, *prefix.split("/"), rid)
    return tuple(
        _TableBase(
            name=f"base_{i}",
            path=os.path.join(root, account, "base.lance"),
            account=account,
        )
        for i, account in enumerate(accounts, start=1)
    )


def table_base_store_params(
    bases: Sequence[_TableBase],
) -> dict[str, dict[str, str]]:
    """Per-base Azure ``storage_options`` keyed by the base-path URI.

    Lance matches ``base_store_params`` by the exact base-path URI (``BasePath.
    path``), NOT by base name — a key that doesn't match a registered base path
    silently falls back to the root account. So the key MUST be ``base.path``
    (the URI passed to ``DatasetBasePath``), not ``base.name``. Each base
    authenticates to its own account by name only (Entra ID / managed identity —
    account keys cannot span accounts). Local-path bases (tests) get no options,
    so an all-local layout returns an empty mapping.
    """
    params: dict[str, dict[str, str]] = {}
    for base in bases:
        if "://" in base.path:
            params[base.path] = {
                "account_name": base.account,
                "azure_storage_account_name": base.account,
            }
    return params


def _canonical_base_store_params(
    dataset,  # noqa: ANN001
    bases: Sequence[_TableBase],
) -> dict[str, dict[str, str]]:
    """Per-base store params keyed by the base path Lance recorded in the manifest.

    Matches each spec to its manifest base by name, then keys the params by the
    manifest's *stored* base path (not the locally constructed one) so any path
    normalization Lance applied can't reintroduce the key mismatch that silently
    routes writes/reads to the root account.
    """
    registered = {
        bp.name: str(bp.path)
        for bp in dataset._ds.base_paths().values()
        if not bp.is_dataset_root
    }
    params: dict[str, dict[str, str]] = {}
    for base in bases:
        stored = registered.get(base.name)
        if stored and "://" in stored:
            params[stored] = {
                "account_name": base.account,
                "azure_storage_account_name": base.account,
            }
    return params


def base_name_for_fragment(index: int, base_count: int) -> str:
    """Round-robin base name for fragment ``index`` (``base_1``..``base_N``)."""
    return f"base_{index % base_count + 1}"


def resolve_table_bases(cfg: BenchConfig) -> tuple[_TableBase, ...]:
    """Resolve the configured table-base specs (empty tuple = single-base)."""
    return build_table_bases(
        output_uri=cfg.bench_uri,
        accounts=cfg.table_base_accounts,
        prefix=cfg.table_base_prefix,
        run_id=cfg.table_base_run_id,
        container=cfg.table_base_container,
    )


def _initial_bases(bases: Sequence[_TableBase]) -> list:
    """Construct Lance ``DatasetBasePath`` objects for dataset bootstrap."""
    from lance import DatasetBasePath

    return [DatasetBasePath(path=base.path, name=base.name) for base in bases]


def _require_multi_base_api() -> None:
    """Fail fast (before any write) if pylance lacks the multi-base write API."""
    import inspect

    import lance

    if "initial_bases" not in inspect.signature(lance.write_dataset).parameters:
        raise RuntimeError(
            "multi-base build (--table-base-accounts) requires a pylance build with "
            "the multi-base write API (>= 9.0.0-beta.15); install pylance==9.0.0b15"
        )


# --- Build plan (shared by run / estimate / validate) -----------------------


class _BuildPlan(NamedTuple):
    """Resolved, picklable build parameters (one source of truth)."""

    params: Any  # upload_images._UploadParams
    seed_uri: str
    n: int
    m: int
    salt: int
    include_large_tail: bool
    max_bytes: int | None
    image_format: str
    rows_per_fragment: int
    num_fragments: int
    schema: pa.Schema
    uri: str
    storage_options: dict[str, str]
    data_storage_version: constants.DataStorageVersion
    # Empty tuple = single-base; otherwise fragment data is round-robined across
    # these per-account bases (base_1..base_N in order).
    base_specs: tuple[_TableBase, ...] = ()
    # Per-base store params keyed by the EXACT base-path URI Lance registered in
    # the manifest (Lance matches base_store_params by path, not name). Resolved
    # post-bootstrap in run_build_ref_table; None until then / for single-base.
    base_store_params: dict[str, dict[str, str]] | None = None


def _plan_from_cfg(cfg: BenchConfig) -> _BuildPlan:
    """Read the seed-run config and resolve the full build plan."""
    storage_options = cfg.storage_options
    seed_uri = cfg.seed_run_config_uri
    if not seed_uri and cfg.manifest_uri:
        seed_uri = upload_images.seed_run_artifact_uri(cfg.manifest_uri)
    if not seed_uri:
        raise ValueError(
            "build-ref-table requires --seed-run-config-uri (or --manifest-uri to "
            "derive it)"
        )

    record = upload_images.read_seed_run(seed_uri, storage_options)
    params = upload_images.params_from_seed_run(record)
    n = record.object_count
    if n <= 0:
        raise ValueError(f"seed-run object_count must be > 0, got {n}")

    m = cfg.target_rows if cfg.target_rows is not None else n * cfg.expansion_factor
    if m <= 0:
        raise ValueError(f"target row count must be > 0, got {m}")

    rpf = cfg.rows_per_fragment
    num_fragments = -(-m // rpf)
    if cfg.limit_fragments is not None:
        num_fragments = min(num_fragments, cfg.limit_fragments)

    if -(-m // n) > _INT32_MAX:
        raise ValueError(
            "expansion_index would overflow int32 (target_rows / object_count too "
            "large); raise object_count or lower target_rows"
        )

    return _BuildPlan(
        params=params,
        seed_uri=seed_uri,
        n=n,
        m=m,
        salt=cfg.shuffle_salt,
        include_large_tail=params.include_large_tail,
        max_bytes=params.max_bytes,
        image_format=synthetic_image.normalize_format(record.image_format),
        rows_per_fragment=rpf,
        num_fragments=num_fragments,
        schema=build_schema(),
        uri=cfg.bench_uri,
        storage_options=storage_options,
        # BenchConfig validation guarantees membership in DATA_STORAGE_VERSIONS.
        data_storage_version=cast(
            "constants.DataStorageVersion", cfg.data_storage_version
        ),
        base_specs=resolve_table_bases(cfg),
    )


# --- Worker (runs in a spawned child process) -------------------------------

_WORKER: dict[str, Any] = {}


def _init_worker(plan: _BuildPlan) -> None:
    """Pool initializer: import Lance/PyArrow and cache the plan in the child."""
    import lance  # noqa: F401  ensure the Lance/Arrow stack is loaded child-side

    _WORKER["plan"] = plan


def _write_fragment_metas(index: int, plan: _BuildPlan, batches: list) -> list[str]:
    """Write fragment ``index``'s data file(s) (no commit); return meta JSON blobs.

    Single-base uses ``LanceFragment.create``; multi-base routes the data file to
    the round-robin target base via ``write_fragments`` (base decided at write
    time). Both return one fragment here (num rows <= the Lance per-file cap).
    """
    reader = pa.RecordBatchReader.from_batches(plan.schema, batches)
    if plan.base_specs:
        from lance.fragment import write_fragments

        # Fragment 0 bootstraps the durable primary/root dataset; subsequent
        # fragments are spread across bases starting at base_1.
        target = base_name_for_fragment(index - 1, len(plan.base_specs))
        dataset = _WORKER.get("dataset")
        if dataset is None:
            dataset = _open_dataset(plan)
            _WORKER["dataset"] = dataset
        metas = write_fragments(
            reader,
            dataset,
            schema=plan.schema,
            mode="append",
            data_storage_version=plan.data_storage_version,
            target_bases=[target],
            base_store_params=plan.base_store_params
            or table_base_store_params(plan.base_specs)
            or None,
        )
        return [json.dumps(meta.to_json()) for meta in metas]

    from lance.fragment import LanceFragment

    frag_meta = LanceFragment.create(
        plan.uri,
        reader,
        schema=plan.schema,
        mode="append",
        storage_options=plan.storage_options or {},
        data_storage_version=plan.data_storage_version,
    )
    return [json.dumps(frag_meta.to_json())]


def _build_and_write_fragment(index: int) -> tuple[int, list[str], int]:
    """Generate fragment ``index`` and write its data file (no commit).

    Generation is deterministic, so the write is retried a few times on transient
    cloud errors (expected over a multi-hour 50B build); a retry may leave an
    orphaned data file, which is harmless (never committed, reclaimed on rebuild).
    """
    plan: _BuildPlan = _WORKER["plan"]
    start = index * plan.rows_per_fragment
    num = min(plan.rows_per_fragment, plan.m - start)
    batches = generate_fragment(start, num, plan).to_batches()

    last_exc: Exception | None = None
    for attempt in range(_FRAGMENT_WRITE_ATTEMPTS):
        try:
            return index, _write_fragment_metas(index, plan, batches), num
        except Exception as exc:  # noqa: BLE001, PERF203 - retry transient writes
            last_exc = exc
            time.sleep(min(2**attempt, 5))
    raise RuntimeError(
        f"fragment {index} failed after {_FRAGMENT_WRITE_ATTEMPTS} attempts"
    ) from last_exc


# --- Driver: bootstrap / resume / batch-commit ------------------------------


def _open_dataset(
    plan: _BuildPlan, *, version: int | None = None, with_bases: bool = True
) -> Any:
    """Open the dataset with root credentials + per-base store params (multi-base).

    Reading fragment data files across bases (validation) needs each base's
    credentials; manifest/root reads (existence, schema, row counts, base
    registry) only need ``plan.storage_options``, so ``with_bases=False`` skips
    the per-base credentials — avoiding threading credentials for bases that may
    not be registered yet (e.g. reconciling a resume).
    """
    import lance

    kwargs: dict[str, Any] = {
        "storage_options": plan.storage_options,
        "version": version,
    }
    if with_bases and plan.base_specs:
        store_params = plan.base_store_params or table_base_store_params(
            plan.base_specs
        )
        if store_params:
            kwargs["base_store_params"] = store_params
    last_exc: Exception | None = None
    for attempt in range(6):
        try:
            return lance.dataset(plan.uri, **kwargs)
        except (FileNotFoundError, OSError, ValueError) as exc:  # noqa: PERF203
            last_exc = exc
            if attempt == 5:
                break
            time.sleep(min(2**attempt, 5))
    if last_exc is not None:
        raise last_exc
    raise RuntimeError(f"failed to open dataset {plan.uri}")


def _dataset_exists(plan: _BuildPlan) -> bool:
    """Whether a Lance dataset physically exists at ``plan.uri``."""
    from pyarrow.fs import FileType

    from geneva.utils.storage import filesystem_from_uri

    # Avoid probing through lance.dataset() here. With pylance 9.0.0-beta.15 on
    # Azure, a failed open immediately before write_dataset(initial_bases=...) can
    # poison the following create: write_dataset returns a dataset object but no
    # durable root _versions directory is left behind.
    versions_uri = plan.uri.rstrip("/") + "/_versions"
    try:
        filesystem, path = filesystem_from_uri(
            versions_uri, storage_options=plan.storage_options
        )
        return filesystem.get_file_info(path).type != FileType.NotFound
    except (FileNotFoundError, ValueError, OSError):
        return False


def _base_account(path: str) -> str:
    """Backing account of a base path (the ``.../<account>/base.lance`` segment)."""
    parts = path.rstrip("/").rsplit("/", 2)
    return parts[-2] if len(parts) >= 2 else path


def _check_base_consistency(dataset, plan: _BuildPlan) -> None:  # noqa: ANN001
    """Refuse to resume when the requested bases don't match the registered ones.

    The base name→account binding (and single- vs multi-base itself) is frozen in
    the manifest at bootstrap. On resume, appends target bases by name and
    authenticate each by account via ``base_store_params``, so a changed
    ``--table-base-accounts`` set/order — or toggling multi-base on or off — would
    crash mid-build (unregistered base) or silently scatter data into the wrong
    accounts. Fail fast up front, the same way a schema/version mismatch does.
    Base *path* prefix/run-id differences are harmless on resume (appends follow
    the manifest-registered path), so only the name→account mapping is compared.
    """
    registered = {
        bp.name: _base_account(bp.path)
        for bp in dataset._ds.base_paths().values()
        if not bp.is_dataset_root
    }
    requested = {base.name: base.account for base in plan.base_specs}
    if registered == requested:
        return
    if not plan.base_specs:
        raise RuntimeError(
            "existing reference table is multi-base but --table-base-accounts was "
            "not given; pass the same table-base flags to resume it, or --overwrite "
            "to rebuild it single-base"
        )
    if not registered:
        raise RuntimeError(
            "existing reference table is single-base but --table-base-accounts was "
            "given; omit the flag to resume it, or --overwrite to rebuild it "
            "multi-base"
        )
    raise RuntimeError(
        "requested table bases do not match the existing reference table's "
        "registered bases (the accounts or their order differ); pass the same "
        "--table-base-accounts used to create it, or --overwrite to rebuild"
    )


def _commit_append(plan: _BuildPlan, metas: list, read_version: int) -> int:
    """Append fragments in one commit; return the new dataset version."""
    import lance

    op = lance.LanceOperation.Append(metas)
    dataset = _open_dataset(plan)
    committed = lance.LanceDataset.commit(
        dataset,
        op,
        read_version=read_version,
        storage_options=plan.storage_options or None,
        base_store_params=table_base_store_params(plan.base_specs) or None,
    )
    return committed.version


def _write_progress(
    uri: str,
    storage_options: dict[str, str],
    *,
    committed_fragments: int,
    total_fragments: int,
    committed_rows: int,
) -> None:
    """Write a best-effort progress sidecar (operator clarity; never authoritative)."""
    try:
        from geneva.utils.storage import filesystem_from_uri

        progress_uri = uri.removesuffix(".lance") + ".progress.json"
        filesystem, path = filesystem_from_uri(
            progress_uri, storage_options=storage_options
        )
        payload = json.dumps(
            {
                "output_uri": uri,
                "committed_fragments": committed_fragments,
                "total_fragments": total_fragments,
                "committed_rows": committed_rows,
            },
            indent=2,
        ).encode()
        with filesystem.open_output_stream(path) as stream:
            stream.write(payload)
    except Exception as exc:  # noqa: BLE001 - sidecar is advisory; never fail the build
        _LOG.debug("progress sidecar write skipped: %s", exc)


def _bootstrap_or_resume(plan: _BuildPlan, *, overwrite: bool) -> tuple[int, int, int]:
    """Create the dataset (fresh) or open it (resume).

    Returns ``(start_index, read_version, committed_rows)``: the first fragment
    index still to build, the current dataset version, and rows already committed.
    """
    import lance

    exists = False if overwrite else _dataset_exists(plan)
    if exists and not overwrite:
        dataset = _open_dataset(plan, with_bases=False)
        if dataset.schema.names != plan.schema.names:
            raise RuntimeError(
                "existing reference table schema does not match; drop it or pass "
                "--overwrite"
            )
        if dataset.data_storage_version != plan.data_storage_version:
            raise RuntimeError(
                f"existing reference table uses data_storage_version "
                f"{dataset.data_storage_version!r}, expected "
                f"{plan.data_storage_version!r}; pass --overwrite to rebuild"
            )
        # Resume appends target bases by name and authenticate them by account, so
        # the requested bases must match the ones frozen in the manifest.
        _check_base_consistency(dataset, plan)
        committed_rows = dataset.count_rows()
        if committed_rows >= plan.m:
            return plan.num_fragments, dataset.version, committed_rows
        if committed_rows % plan.rows_per_fragment != 0:
            # A clean build leaves only fragment-aligned prefixes (the one partial
            # fragment is the global last, committed only when the build completes). A
            # non-aligned, incomplete count means a foreign/corrupt/partial table;
            # resuming from the floored index would re-append an overlapping fragment
            # and duplicate rows, so refuse rather than corrupt it.
            raise RuntimeError(
                f"existing reference table has {committed_rows} rows, not a multiple "
                f"of rows_per_fragment ({plan.rows_per_fragment}); it is partial or "
                "inconsistent — pass --overwrite to rebuild"
            )
        start_index = committed_rows // plan.rows_per_fragment
        if start_index > 0:
            _LOG.info(
                "resuming build of %s at fragment %d (%d rows committed)",
                plan.uri,
                start_index,
                committed_rows,
            )
            return start_index, dataset.version, committed_rows
        # committed_rows == 0: an empty dataset; fall through to a clean bootstrap.

    # Fresh build (or --overwrite, or an empty existing dataset): bootstrap with a
    # real first fragment, matching the proven high-fragment-count pattern. In
    # multi-base mode the bootstrap fragment intentionally lands in the primary
    # root while ``initial_bases`` registers every side base in the manifest.
    # On Azure/pylance 9.0.0-beta.15, bootstrapping directly into target_bases can
    # return a dataset object without leaving a reopenable root behind; primary
    # bootstrap + base registration keeps the root durable.
    num0 = min(plan.rows_per_fragment, plan.m)
    base_kwargs: dict[str, Any] = {}
    if plan.base_specs:
        base_kwargs = {
            "initial_bases": _initial_bases(plan.base_specs),
            "base_store_params": table_base_store_params(plan.base_specs) or None,
        }
    dataset = lance.write_dataset(
        generate_fragment(0, num0, plan),
        plan.uri,
        schema=plan.schema,
        mode="overwrite",
        storage_options=plan.storage_options,
        data_storage_version=plan.data_storage_version,
        **base_kwargs,
    )
    return 1, dataset.version, num0


def run_build_ref_table(cfg: BenchConfig) -> dict:
    """Build (or resume) the shuffled reference table; return a metrics dict."""
    plan = _plan_from_cfg(cfg)
    workers = cfg.build_workers
    commit_batch = cfg.commit_fragments

    _LOG.info(
        "build-ref-table: object_count=%d target_rows=%d fragments=%d rpf=%d "
        "workers=%d commit_every=%d output=%s",
        plan.n,
        plan.m,
        plan.num_fragments,
        plan.rows_per_fragment,
        workers,
        commit_batch,
        plan.uri,
    )
    if plan.base_specs:
        _require_multi_base_api()
        _LOG.info(
            "multi-base: spreading fragment data round-robin across %d bases "
            "(accounts=%s, run_id=%s)",
            len(plan.base_specs),
            [base.account for base in plan.base_specs],
            cfg.table_base_run_id or default_table_base_run_id(plan.uri),
        )

    start_index, read_version, committed_rows = _bootstrap_or_resume(
        plan, overwrite=cfg.overwrite
    )
    if plan.base_specs:
        # Lance matches base_store_params by the exact registered base-path URI, so
        # re-key from the manifest's stored paths (read back post-bootstrap) before
        # any worker append/commit; a name-keyed miss silently routes data to the
        # root account. This resolved plan is what the worker pool is seeded with.
        canonical = _canonical_base_store_params(
            _open_dataset(plan, with_bases=False), plan.base_specs
        )
        plan = plan._replace(base_store_params=canonical)
        _LOG.info(
            "multi-base store params keyed by %d registered base paths", len(canonical)
        )
    rows_at_start = committed_rows
    started = time.time()

    if start_index < plan.num_fragments:
        max_inflight = max(commit_batch, 2 * workers)
        from lance.fragment import FragmentMetadata

        pending: dict[int, Future] = {}
        metas: list = []
        next_submit = start_index
        next_collect = start_index
        ctx = get_context("spawn")
        try:
            with ProcessPoolExecutor(
                max_workers=workers,
                mp_context=ctx,
                initializer=_init_worker,
                initargs=(plan,),
            ) as pool:
                while next_collect < plan.num_fragments:
                    while (
                        next_submit < plan.num_fragments and len(pending) < max_inflight
                    ):
                        pending[next_submit] = pool.submit(
                            _build_and_write_fragment, next_submit
                        )
                        next_submit += 1
                    _index, frag_jsons, num = pending.pop(next_collect).result()
                    metas.extend(FragmentMetadata.from_json(j) for j in frag_jsons)
                    next_collect += 1
                    committed_rows += num
                    if len(metas) >= commit_batch or next_collect >= plan.num_fragments:
                        read_version = _commit_append(plan, metas, read_version)
                        _LOG.info(
                            "committed fragments [%d, %d) -> v%d (%d rows)",
                            next_collect - len(metas),
                            next_collect,
                            read_version,
                            committed_rows,
                        )
                        _write_progress(
                            plan.uri,
                            plan.storage_options,
                            committed_fragments=next_collect,
                            total_fragments=plan.num_fragments,
                            committed_rows=committed_rows,
                        )
                        metas = []
        except Exception:  # noqa: BLE001 - log actionable context, then re-raise
            _LOG.error(
                "build-ref-table failed mid-build (reached fragment %d of %d); "
                "committed fragments are durable — rerun the same command to resume "
                "from the committed prefix. Uncommitted fragment files may remain on "
                "storage; rebuild once with --overwrite to reclaim them.",
                next_collect,
                plan.num_fragments,
            )
            raise

    elapsed = time.time() - started
    rows_built = committed_rows - rows_at_start
    fragments_built = plan.num_fragments - start_index

    metrics: dict[str, Any] = {
        "stage": "build-ref-table",
        "seed_run_config_uri": plan.seed_uri,
        "output_uri": plan.uri,
        "object_count": plan.n,
        "target_rows": plan.m,
        "rows_per_fragment": plan.rows_per_fragment,
        "data_storage_version": plan.data_storage_version,
        "num_fragments": plan.num_fragments,
        "workers": workers,
        "shuffle_salt": plan.salt,
        "start_fragment": start_index,
        "fragments_built": fragments_built,
        "rows_built": rows_built,
        "total_rows": committed_rows,
        "elapsed_seconds": round(elapsed, 2),
        "rows_per_second": round(rows_built / elapsed, 1) if elapsed > 0 else None,
        "fragments_per_second": round(fragments_built / elapsed, 2)
        if elapsed > 0
        else None,
        "ok": True,
    }

    if plan.base_specs:
        metrics["multi_base"] = {
            "base_count": len(plan.base_specs),
            "accounts": [base.account for base in plan.base_specs],
            "prefix": cfg.table_base_prefix,
            "run_id": cfg.table_base_run_id or default_table_base_run_id(plan.uri),
            "bases": [
                {"name": base.name, "path": base.path} for base in plan.base_specs
            ],
        }

    if cfg.validate_build:
        metrics["validation"] = validate_ref_table(cfg, plan=plan)
        metrics["ok"] = metrics["validation"]["ok"]

    _LOG.info("build-ref-table complete: %s", metrics)
    return metrics


# --- Validation -------------------------------------------------------------


def validate_ref_table(
    cfg: BenchConfig,
    *,
    sample_rows: int = 256,
    head_check: bool = False,
    plan: _BuildPlan | None = None,
) -> dict:
    """Sample-check the built table: schema, row/fragment counts, and that derived
    locators match the scalar ``upload_images`` helpers (the correctness boundary).

    ``head_check`` (off by default; the upload may still be in progress) HEADs a few
    URLs to confirm the referenced blobs resolve.
    """
    if plan is None:
        plan = _plan_from_cfg(cfg)
    params = plan.params
    dataset = _open_dataset(plan)

    schema_ok = dataset.schema.names == plan.schema.names
    total_rows = dataset.count_rows()
    fragments = dataset.get_fragments()
    num_fragments = len(fragments)

    sample = dataset.to_table(
        columns=[
            constants.ROW_INDEX_COL,
            constants.IMAGE_ID_COL,
            constants.URL_COL,
            constants.OBJECT_KEY_COL,
            constants.ACCOUNT_COL,
            constants.PREFIX_ID_COL,
        ],
        limit=sample_rows,
    ).to_pydict()

    order = list(np.argsort(sample[constants.ROW_INDEX_COL]))
    image_ids = [sample[constants.IMAGE_ID_COL][i] for i in order]
    adjacent = sum(1 for a, b in zip(image_ids, image_ids[1:], strict=False) if a == b)

    mismatches = 0
    for i in range(len(sample[constants.IMAGE_ID_COL])):
        iid = int(sample[constants.IMAGE_ID_COL][i])
        prefix_id = upload_images.prefix_id_for(iid, params)
        object_key = upload_images.object_key_for(iid, prefix_id, params)
        url = upload_images.url_for(object_key, params)
        if (
            url != sample[constants.URL_COL][i]
            or object_key != sample[constants.OBJECT_KEY_COL][i]
            or prefix_id != sample[constants.PREFIX_ID_COL][i]
            or upload_images.account_for(iid, params)
            != sample[constants.ACCOUNT_COL][i]
        ):
            mismatches += 1

    # Rows the run intended to produce: the full target for a normal build, or the
    # limited count for a --limit-fragments canary. Exact-match gives real "done"
    # confidence (not just "non-empty").
    expected_rows = min(plan.num_fragments * plan.rows_per_fragment, plan.m)
    result: dict[str, Any] = {
        "schema_ok": schema_ok,
        "total_rows": total_rows,
        "expected_rows": expected_rows,
        "complete": total_rows == expected_rows,
        "num_fragments": num_fragments,
        "sampled_rows": len(image_ids),
        "derivation_mismatches": mismatches,
        "adjacent_image_ids": adjacent,
        "ok": schema_ok and mismatches == 0 and total_rows == expected_rows,
    }

    if plan.base_specs:
        placement = _validate_base_placement(dataset, fragments, plan)
        result["base_distribution"] = placement
        result["ok"] = result["ok"] and placement["ok"]

    if head_check:
        result["head_check"] = _head_sample(
            sample[constants.URL_COL], plan.storage_options
        )
    return result


def _validate_base_placement(dataset, fragments: list, plan: _BuildPlan) -> dict:  # noqa: ANN001
    """Count data files per base and assert the round-robin spread was applied.

    Fragment 0 bootstraps the durable primary/root dataset. Every later fragment
    should land on ``base_{(i - 1) % base_count + 1}``, so a full build touches
    root plus every configured base; a tiny build touches root plus the leading
    prefix. Reports the per-base file distribution and whether the expected
    placements (no more, no fewer) were used.
    """
    base_names = {
        bid: (bp.name or f"base_id_{bid}")
        for bid, bp in dataset._ds.base_paths().items()
    }
    distribution: dict[str, int] = {}
    for frag in fragments:
        for data_file in frag.data_files():
            # Root/single-base data files report base_id None (or 0); anything not
            # in the registered set surfaces as an (unexpected) placement below.
            bid = getattr(data_file, "base_id", None) or 0
            name = base_names.get(bid, "root" if bid == 0 else f"base_id_{bid}")
            distribution[name] = distribution.get(name, 0) + 1

    base_count = len(plan.base_specs)
    expected = {"root"}
    expected.update(
        base_name_for_fragment(i - 1, base_count) for i in range(1, len(fragments))
    )
    used = set(distribution)
    unexpected = sorted(used - expected)
    missing = sorted(expected - used)
    return {
        "distribution": distribution,
        "expected_bases": sorted(expected),
        "unexpected_bases": unexpected,
        "missing_bases": missing,
        "ok": not unexpected and not missing,
    }


def _head_sample(
    urls: list[str], storage_options: dict[str, str], *, limit: int = 8
) -> dict:
    """HEAD a few URLs to confirm the referenced blobs resolve (best-effort)."""
    from pyarrow.fs import FileType

    from geneva.utils.storage import filesystem_from_uri

    checked = 0
    missing = 0
    for url in urls[:limit]:
        filesystem, path = filesystem_from_uri(url, storage_options=storage_options)
        info = filesystem.get_file_info(path)
        checked += 1
        if info.type == FileType.NotFound:
            missing += 1
    return {"checked": checked, "missing": missing}


# --- Estimate (sizing/runtime sanity, no full write) ------------------------


def estimate_ref_table(cfg: BenchConfig) -> dict:
    """Generate + locally write one fragment to project size and runtime; no Azure."""
    import shutil
    import tempfile

    import lance

    plan = _plan_from_cfg(cfg)
    num0 = min(plan.rows_per_fragment, plan.m)

    t0 = time.time()
    table = generate_fragment(0, num0, plan)
    gen_seconds = time.time() - t0
    arrow_bytes = table.nbytes

    tmp_dir = tempfile.mkdtemp(prefix="ref_estimate_")
    try:
        local_uri = os.path.join(tmp_dir, "estimate.lance")
        lance.write_dataset(
            table,
            local_uri,
            schema=plan.schema,
            data_storage_version=plan.data_storage_version,
        )
        on_disk = sum(
            os.path.getsize(os.path.join(root, name))
            for root, _dirs, files in os.walk(local_uri)
            for name in files
        )
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    compressed_bpr = on_disk / num0
    rows_per_sec_core = num0 / gen_seconds if gen_seconds > 0 else float("nan")
    rows_per_sec = rows_per_sec_core * cfg.build_workers

    def _projection(rows: int) -> dict:
        return {
            "rows": rows,
            "compressed_bytes": int(compressed_bpr * rows),
            "est_seconds": round(rows / rows_per_sec, 1) if rows_per_sec else None,
        }

    estimate = {
        "stage": "build-ref-table-estimate",
        "seed_run_config_uri": plan.seed_uri,
        "object_count": plan.n,
        "target_rows": plan.m,
        "num_fragments": plan.num_fragments,
        "rows_per_fragment": plan.rows_per_fragment,
        "workers": cfg.build_workers,
        "arrow_bytes_per_row": round(arrow_bytes / num0, 1),
        "compressed_bytes_per_row": round(compressed_bpr, 1),
        "gen_rows_per_second_per_core": round(rows_per_sec_core, 1),
        "gen_rows_per_second_total": round(rows_per_sec, 1),
        "target": _projection(plan.m),
        "projections": {
            "10b": _projection(10_000_000_000),
            "30b": _projection(30_000_000_000),
            "50b": _projection(50_000_000_000),
        },
        "ok": True,
    }
    _LOG.info("build-ref-table estimate: %s", estimate)
    return estimate
