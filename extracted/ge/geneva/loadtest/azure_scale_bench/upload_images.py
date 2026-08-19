# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Upload a synthetic image dataset to Azure as loose objects + a Lance URL manifest.

Generates ``object_count`` real (synthetic) images following the Atlas size
distribution and uploads each as a loose blob, recording a Lance manifest table of
their URLs. Runs as a Geneva backfill over a small ``image_id`` table (so it
distributes across the KubeRay cluster and inherits windowing + checkpoint
resumability, exactly like the ``expand`` stage). The upload UDF is per-row
scalar by default; ``--upload-concurrency`` switches to a batched (Array-input)
UDF whose per-worker thread pool issues concurrent PUTs per batch, so fewer
actors sustain the same in-flight PUT count.

Deterministic + idempotent: the same ``(seed_run_id, image_id)`` always maps to the
same object key and the same bytes, and each upload does HEAD-then-decide, so a
resume re-runs cheaply. A plain resume (re)fills rows still missing manifest data;
to retry rows that FAILED a prior run, repair with ``--where "ok = false"``.
A ``SeedRunConfig`` JSON artifact is written alongside the manifest so later jobs
can re-derive URLs from config without scanning the full manifest.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any, NamedTuple, cast

import attrs
import pyarrow as pa

from loadtest.azure_scale_bench import (
    benchmark_env,
    clone,
    constants,
    image_distribution,
    object_writer,
    runner,
    synthetic_image,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from geneva.transformer import UDF
    from loadtest.azure_scale_bench.benchmark_env import BenchConfig
    from loadtest.azure_scale_bench.object_writer import ObjectWriter

_LOG = logging.getLogger(__name__)

MASK64 = constants.MASK64

# Manifest columns (struct field order == _row_to_tuple order). image_id is the
# table's existing input column, so it is not repeated here. ALL fields are
# nullable: add_columns materializes the columns all-null before backfill, and
# Lance rejects a non-nullable all-null column. Non-nullness of filled rows is
# implied by the ``ok``/``error`` columns after backfill. ``target_bucket`` is the
# assigned bucket; ``actual_bucket`` is the bucket of the actual encoded size.
_MANIFEST_FIELDS: list[tuple[str, pa.DataType]] = [
    ("url", pa.string()),
    ("account", pa.string()),
    ("container", pa.string()),
    ("object_key", pa.string()),
    ("prefix_id", pa.int32()),
    ("target_bucket", pa.string()),
    ("actual_bucket", pa.string()),
    ("target_bytes", pa.int64()),
    ("actual_bytes", pa.int64()),
    ("image_format", pa.string()),
    ("width", pa.int32()),
    ("height", pa.int32()),
    ("etag", pa.string()),
    ("ok", pa.bool_()),
    ("error", pa.string()),
]
MANIFEST_STRUCT = pa.struct(
    [pa.field(name, typ, nullable=True) for name, typ in _MANIFEST_FIELDS]
)
_ANCHOR_COLUMN = "url"

SEED_RUN_SCHEMA_VERSION = 1


# --- Seed-run config artifact ----------------------------------------------


@attrs.define(kw_only=True, frozen=True)
class SeedRunConfig:
    """The deterministic shape of one seed run (URL derivation + size + lifecycle).

    Persisted as JSON so later jobs re-derive object URLs from config alone.
    """

    schema_version: int
    generator_version: str
    distribution_version: str
    seed_run_id: str
    seed_run_salt: int
    object_count: int
    accounts: list[str]
    container: str
    base_prefix: str
    prefix_count: int
    image_format: str
    include_large_tail: bool
    max_image_bytes: int | None
    created_at: str
    delete_after: str
    manifest_uri: str


def _seed_run_salt(seed_run_id: str) -> int:
    """Deterministic 64-bit salt for a seed-run id (scatters account/prefix)."""
    return int.from_bytes(
        hashlib.blake2b(seed_run_id.encode(), digest_size=8).digest(), "big"
    )


def seed_run_artifact_uri(manifest_uri: str) -> str:
    """The JSON seed-run-config URI sitting beside the manifest table."""
    return f"{manifest_uri.removesuffix('.lance')}.seedrun.json"


def write_seed_run(
    uri: str, record: SeedRunConfig, storage_options: dict[str, str]
) -> None:
    """Write the seed-run config as JSON via the shared filesystem seam."""
    from geneva.utils.storage import filesystem_from_uri

    filesystem, path = filesystem_from_uri(uri, storage_options=storage_options)
    payload = json.dumps(attrs.asdict(record), indent=2).encode()
    with filesystem.open_output_stream(path) as stream:
        stream.write(payload)


def read_seed_run(uri: str, storage_options: dict[str, str]) -> SeedRunConfig:
    """Read the seed-run config JSON back into a ``SeedRunConfig``."""
    from geneva.utils.storage import filesystem_from_uri

    filesystem, path = filesystem_from_uri(uri, storage_options=storage_options)
    with filesystem.open_input_file(path) as stream:
        data = json.loads(stream.readall())
    return SeedRunConfig(**data)


# --- Worker manifest (deps the upload UDF needs on KubeRay workers) ---------


def build_upload_manifest(
    name: str, *, account_name: str, include_lance_deps: bool = True
) -> Any:
    """Build the standard upload-images worker ``GenevaManifest``.

    The upload UDF imports azure-storage-blob / azure-identity / pillow / numpy
    worker-side; this packages those (plus the validated lance/pylance pins + fury
    indexes and the ``./loadtest`` code) so a cluster run has them. Sets only
    ``AZURE_STORAGE_ACCOUNT_NAME`` — the account KEY stays in the worker env, never
    in the manifest.
    """
    from geneva.manifest import GenevaManifest

    pip_deps = list(constants.UPLOAD_WORKER_PIP_DEPS)
    if include_lance_deps:
        pip_deps += list(constants.UPLOAD_MANIFEST_LANCE_DEPS)
    builder = (
        GenevaManifest.create_pip(name)
        .add_py_module("./loadtest")
        .pip(pip_deps)
        .env_vars({benchmark_env.ACCOUNT_NAME_ENV: account_name})
    )
    for url in constants.UPLOAD_MANIFEST_EXTRA_INDEX_URLS:
        builder = builder.add_extra_index_url(url)
    return builder.build()


def define_upload_manifest(
    conn: Any, name: str, *, account_name: str, include_lance_deps: bool = True
) -> None:
    """Register the upload-images worker manifest under ``name`` on ``conn``.

    ``upload-images --manifest <name>`` then finds it via ``conn.context``.
    """
    manifest = build_upload_manifest(
        name, account_name=account_name, include_lance_deps=include_lance_deps
    )
    # define_manifest is deprecated upstream but is the path the workbench's
    # --manifest / conn.context(manifest=...) flow (and the validated smoke) use.
    conn.define_manifest(name, manifest)


def run_define_upload_manifest(cfg: BenchConfig) -> dict:
    """Build + register the upload-images manifest on the benchmark database."""
    if not cfg.manifest:
        raise ValueError("define-upload-manifest requires --manifest NAME")
    db_uri, _ = cfg.bench_db_and_table
    conn = benchmark_env.connect_geneva(db_uri, cfg.storage_options)
    define_upload_manifest(conn, cfg.manifest, account_name=cfg.account_name)
    metrics = {
        "stage": "define-upload-manifest",
        "manifest": cfg.manifest,
        "db_uri": db_uri,
        "account_name": cfg.account_name,
        "pip_deps": [
            *constants.UPLOAD_WORKER_PIP_DEPS,
            *constants.UPLOAD_MANIFEST_LANCE_DEPS,
        ],
    }
    _LOG.info("registered upload manifest: %s", metrics)
    return metrics


# --- Deterministic URL/key derivation --------------------------------------


class _UploadParams(NamedTuple):
    """Picklable per-run params captured by the upload UDF closure."""

    seed_run_id: str
    seed_run_salt: int
    accounts: tuple[str, ...]
    container: str
    base_prefix: str
    prefix_count: int
    image_format: str
    include_large_tail: bool
    max_bytes: int | None
    overwrite_objects: bool
    ext: str


def _params(cfg: BenchConfig, salt: int) -> _UploadParams:
    fmt = synthetic_image.normalize_format(cfg.image_format)
    return _UploadParams(
        seed_run_id=cast("str", cfg.seed_run_id),
        seed_run_salt=salt,
        accounts=tuple(cfg.accounts),
        container=cfg.loose_container,
        base_prefix=cfg.base_prefix,
        prefix_count=cfg.prefix_count,
        image_format=cfg.image_format,
        include_large_tail=cfg.include_large_tail,
        max_bytes=cfg.max_image_bytes,
        overwrite_objects=cfg.overwrite_objects,
        ext="jpg" if fmt == "jpeg" else "png",
    )


def params_from_seed_run(record: SeedRunConfig) -> _UploadParams:
    """Reconstruct the derivation params from a persisted seed-run config.

    The download stage uses this to re-derive object keys/URLs for a seed run
    WITHOUT scanning the manifest table — the same deterministic mapping that
    ``upload-images`` used to write the objects. ``overwrite_objects`` is irrelevant
    to reads, so it is left ``False``.
    """
    fmt = synthetic_image.normalize_format(record.image_format)
    return _UploadParams(
        seed_run_id=record.seed_run_id,
        seed_run_salt=record.seed_run_salt,
        accounts=tuple(record.accounts),
        container=record.container,
        base_prefix=record.base_prefix,
        prefix_count=record.prefix_count,
        image_format=record.image_format,
        include_large_tail=record.include_large_tail,
        max_bytes=record.max_image_bytes,
        overwrite_objects=False,
        ext="jpg" if fmt == "jpeg" else "png",
    )


def _scatter(image_id: int, salt: int, stream_salt: int) -> int:
    """A decorrelated 64-bit hash of image_id for this seed run + stream."""
    return image_distribution.row_hash((image_id ^ salt ^ stream_salt) & MASK64)


def account_for(image_id: int, params: _UploadParams) -> str:
    """The storage account this image is assigned to (round-robin by hash)."""
    idx = _scatter(image_id, params.seed_run_salt, constants.ACCOUNT_SALT)
    return params.accounts[idx % len(params.accounts)]


def prefix_id_for(image_id: int, params: _UploadParams) -> int:
    """The key-prefix bucket (spreads load across partitions)."""
    return (
        _scatter(image_id, params.seed_run_salt, constants.PREFIX_SALT)
        % params.prefix_count
    )


def object_key_for(image_id: int, prefix_id: int, params: _UploadParams) -> str:
    """Deterministic blob key: base/seed_run/p<prefix>/<image_id>.<ext>."""
    return (
        f"{params.base_prefix}/{params.seed_run_id}"
        f"/p{prefix_id:05d}/{image_id}.{params.ext}"
    )


def url_for(object_key: str, params: _UploadParams) -> str:
    """The full ``az://container/key`` URL."""
    return f"az://{params.container}/{object_key}"


# --- Per-image upload (idempotent) -----------------------------------------


def upload_one(
    image_id: int, get_writer: Callable[[str], ObjectWriter], params: _UploadParams
) -> dict[str, Any]:
    """Render + idempotently upload one image; return its manifest row.

    Derivation (account/key/url/size bucket) is computed first so a failed render
    or upload still records a correct row with ``ok=False`` and the error.
    """
    account = account_for(image_id, params)
    prefix_id = prefix_id_for(image_id, params)
    object_key = object_key_for(image_id, prefix_id, params)
    url = url_for(object_key, params)
    assignment = synthetic_image.target_assignment(
        image_id,
        include_large_tail=params.include_large_tail,
        max_bytes=params.max_bytes,
    )
    row: dict[str, Any] = {
        "url": url,
        "account": account,
        "container": params.container,
        "object_key": object_key,
        "prefix_id": prefix_id,
        "target_bucket": assignment.bucket,
        "actual_bucket": assignment.bucket,
        "target_bytes": assignment.target,
        "actual_bytes": 0,
        "image_format": synthetic_image.normalize_format(params.image_format),
        "width": 0,
        "height": 0,
        "etag": None,
        "ok": False,
        "error": None,
    }
    try:
        rendered = synthetic_image.render_sized_image(
            image_id,
            assignment.lo,
            assignment.hi,
            assignment.target,
            image_format=params.image_format,
        )
        row["actual_bytes"] = rendered.actual_bytes
        # The actual bucket can differ from the target (rare JPEG near-floor miss);
        # record both so the label never disagrees with actual_bytes.
        row["actual_bucket"] = synthetic_image.bucket_of(rendered.actual_bytes)
        row["image_format"] = rendered.image_format
        row["width"] = rendered.width
        row["height"] = rendered.height

        writer = get_writer(account)
        content_type = object_writer.content_type_for(params.image_format)
        expected_md5 = object_writer.md5_hex(rendered.image_bytes)
        if params.overwrite_objects:
            row["etag"] = writer.put(
                object_key,
                rendered.image_bytes,
                content_type=content_type,
                content_md5=expected_md5,
                overwrite=True,
            )
            row["ok"] = True
        else:
            # Conditional create: a single PUT on the common fresh path; HEAD only
            # on conflict, so a fresh seed is ~N storage ops, not 2N.
            try:
                row["etag"] = writer.put(
                    object_key,
                    rendered.image_bytes,
                    content_type=content_type,
                    content_md5=expected_md5,
                    overwrite=False,
                )
                row["ok"] = True
            except object_writer.ObjectExistsError:
                # Conflict-match verifies BOTH size and Content-MD5. A size-only match
                # with a missing MD5 (e.g. an object written by another tool) is NOT
                # trusted — fail so the run can't silently accept unverifiable content.
                stat = writer.head(object_key)
                row["etag"] = stat.etag if stat is not None else None
                if stat is None:
                    reason = "could not be read"
                elif stat.size_bytes != rendered.actual_bytes:
                    reason = f"has a different size ({stat.size_bytes})"
                elif stat.content_md5 is None:
                    reason = "cannot be verified (no checksum)"
                elif stat.content_md5 != expected_md5:
                    reason = "has different content"
                else:
                    reason = None
                    row["ok"] = True  # already present, size + MD5 match
                if reason is not None:
                    row["error"] = (
                        f"object exists but {reason}; pass --overwrite-objects "
                        "to replace"
                    )
    except Exception as exc:  # noqa: BLE001 - capture per-row failure in the manifest
        row["ok"] = False
        row["error"] = str(exc)
    # Mark successful rows with a non-null empty error so resume never re-selects
    # them: every manifest field is nullable, and geneva's unpacked-group default
    # predicate ORs `<col> IS NULL` across all fields (incl. the otherwise-null
    # `error`), which would re-touch every already-successful row.
    if row["ok"] and row["error"] is None:
        row["error"] = ""
    return row


def upload_ids(
    image_ids: list[int],
    get_writer: Callable[[str], ObjectWriter],
    params: _UploadParams,
    *,
    max_workers: int = 1,
    executor: ThreadPoolExecutor | None = None,
) -> list[dict[str, Any]]:
    """Upload a batch of image ids concurrently (order-preserving).

    The batched upload UDF's core: a thread pool issues many concurrent PUTs per
    batch (the sync Azure client releases the GIL during network IO), giving high
    in-flight density per worker without exploding actor/process count. Pass a
    long-lived ``executor`` (the batched UDF's per-worker pool) to avoid spinning up
    and tearing down threads every batch; it is reused, not shut down. With no
    ``executor``, ``max_workers <= 1`` runs serially and ``> 1`` uses a transient
    pool (the path tests/one-off calls take).
    """

    def _one(image_id: int) -> dict[str, Any]:
        return upload_one(image_id, get_writer, params)

    if executor is not None:
        return list(executor.map(_one, image_ids))
    if max_workers <= 1 or len(image_ids) <= 1:
        return [_one(i) for i in image_ids]
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(_one, image_ids))


def _row_to_tuple(row: dict[str, Any]) -> tuple:
    return tuple(row[name] for name, _ in _MANIFEST_FIELDS)


# --- The Geneva UDF + orchestration ----------------------------------------


def _udf_version(cfg: BenchConfig, salt: int, *, batched: bool = False) -> str:
    """UDF version embedding the seed shape, so a knob change re-keys checkpoints.

    The scalar knob string is unchanged by the batched mode (existing scalar
    checkpoints keep their keys); ``batched=True`` appends the mode and the upload
    concurrency, so scalar vs batched (and different concurrencies) re-key.
    """
    knobs = "|".join(
        str(x)
        for x in (
            constants.GENERATOR_VERSION,
            constants.DISTRIBUTION_VERSION,
            cfg.image_format,
            cfg.include_large_tail,
            cfg.max_image_bytes,
            cfg.prefix_count,
            cfg.base_prefix,
            salt,
            ",".join(cfg.accounts),
            *(("batched", cfg.upload_concurrency) if batched else ()),
        )
    )
    digest = hashlib.blake2b(knobs.encode(), digest_size=5).hexdigest()
    return f"0.1-{digest}"


def _writer_cache(
    container: str,
    writer_factory: Callable[[str], ObjectWriter] | None = None,
) -> Callable[[str], ObjectWriter]:
    """A per-worker ``account -> writer`` cache closure.

    Defaults to ``AzureBlobWriter``; ``writer_factory`` swaps the backing writer
    (the seam a local test writer plugs into). Each worker builds one client per
    account and reuses it across the fragment's rows.
    """
    cache: dict[str, ObjectWriter] = {}

    def get_writer(account: str) -> ObjectWriter:
        writer = cache.get(account)
        if writer is None:
            if writer_factory is not None:
                writer = writer_factory(account)
            else:
                writer = object_writer.AzureBlobWriter(account, container)
            cache[account] = writer
        return writer

    return get_writer


def build_upload_udf(
    cfg: BenchConfig,
    salt: int,
    writer_factory: Callable[[str], ObjectWriter] | None = None,
) -> UDF:
    """A per-row upload UDF (one Azure HEAD/PUT per image) bound to ``image_id``.

    A per-worker writer cache lives in the closure so each KubeRay worker builds
    one client per account and reuses it across the fragment's rows.
    """
    import geneva

    params = _params(cfg, salt)
    get_writer = _writer_cache(params.container, writer_factory)

    udf_kwargs: dict[str, Any] = {
        "data_type": MANIFEST_STRUCT,
        "version": _udf_version(cfg, salt),
        **runner.udf_resource_kwargs(cfg),
        **runner.udf_size_kwargs(cfg),
    }

    @geneva.udf(**udf_kwargs)
    def upload_image(image_id: int) -> tuple:
        return _row_to_tuple(upload_one(image_id, get_writer, params))

    return cast("UDF", attrs.evolve(upload_image, input_columns=["image_id"]))


def build_upload_udf_batched(
    cfg: BenchConfig,
    salt: int,
    writer_factory: Callable[[str], ObjectWriter] | None = None,
) -> UDF:
    """A batched (Array-input) upload UDF: concurrent PUTs per batch.

    A thread pool of ``cfg.upload_concurrency`` renders + uploads across the
    batch's rows, giving high in-flight PUT density per worker so seeding needs
    far fewer actors than one-PUT-per-actor scalar mode. The pool is created
    lazily per worker and reused across batches (not one pool per batch). The
    output is the same manifest struct (unpacked from ``data_type``, so the
    sibling columns are identical to the scalar path), and each row goes through
    the same ``upload_one`` — derivation and object bytes are identical.

    Note: batched UDFs are not multi-output, so an EXISTING manifest column
    resumes with its stored UDF regardless of this flag — switching modes
    requires ``--overwrite`` (safe either way: same derived data).
    """
    import geneva

    params = _params(cfg, salt)
    max_workers = cfg.upload_concurrency or 1
    get_writer = _writer_cache(params.container, writer_factory)
    # A one-slot holder for the per-worker pool: built lazily on the worker (a live
    # ThreadPoolExecutor is unpicklable, so it must not exist at ship time) and
    # reused across batches to avoid per-batch thread churn.
    pool_box: list[ThreadPoolExecutor | None] = [None]

    udf_kwargs: dict[str, Any] = {
        "data_type": MANIFEST_STRUCT,
        "version": _udf_version(cfg, salt, batched=True),
        **runner.udf_resource_kwargs(cfg),
        **runner.udf_size_kwargs(cfg),
    }

    @geneva.udf(**udf_kwargs)
    def upload_image_batch(image_id: pa.Array) -> pa.Array:
        ids: list[int] = []
        for i in image_id.to_pylist():
            if i is None:
                # never expected (the id table is a dense range); guard rather
                # than silently drop a row and misalign the returned batch
                raise ValueError("image_id must be non-null")
            ids.append(int(i))
        if max_workers > 1 and pool_box[0] is None:
            pool_box[0] = ThreadPoolExecutor(
                max_workers=max_workers, thread_name_prefix="img-upload"
            )
        out = upload_ids(
            ids,
            get_writer,
            params,
            max_workers=max_workers,
            executor=pool_box[0],
        )
        return pa.array([_row_to_tuple(r) for r in out], type=MANIFEST_STRUCT)

    return cast("UDF", attrs.evolve(upload_image_batch, input_columns=["image_id"]))


def _default_manifest_uri(cfg: BenchConfig, seed_run_id: str) -> str:
    """Default manifest table next to the benchmark clone's database."""
    db_uri, _ = cfg.bench_db_and_table
    return f"{db_uri}/img_manifest_{seed_run_id}.lance"


def _ensure_id_table(
    conn: Any,
    table_name: str,
    uri: str,
    storage_options: dict[str, str],
    object_count: int,
    rows_per_frag: int,
) -> Any:
    """Create (or open) the ``image_id`` table, one fragment per ``rows_per_frag``.

    Existence is decided by a PHYSICAL Lance check (``clone._exists``), NOT
    ``conn.table_names()``: the namespace listing is paginated, so an upload resume in
    a busy container could miss the existing manifest table and wrongly try to create
    it again. ``conn.create_table`` registers the table, so ``open_table`` then finds
    it on resume.
    """
    if clone._exists(uri, storage_options):
        tbl = conn.open_table(table_name)
        current = tbl.count_rows()
        if current != object_count:
            raise RuntimeError(
                f"id table {table_name!r} has {current} rows, expected {object_count} "
                "(a partial or mismatched prior build); drop the table and rerun, or "
                "use a different --seed-run-id"
            )
        return tbl
    tbl = None
    for start in range(0, object_count, rows_per_frag):
        end = min(start + rows_per_frag, object_count)
        batch = pa.table({"image_id": pa.array(range(start, end), pa.int64())})
        if tbl is None:
            tbl = conn.create_table(table_name, batch)
        else:
            tbl.add(batch, mode="append")
    if tbl is None:  # object_count == 0 guard (validation forbids it, but be safe)
        tbl = conn.create_table(
            table_name, pa.table({"image_id": pa.array([], pa.int64())})
        )
    return tbl


def _assert_seed_run_compatible(
    existing: SeedRunConfig, cfg: BenchConfig, salt: int
) -> None:
    """Raise if a resume's knobs differ from the persisted seed-run config.

    On resume the manifest column already exists, so backfill fills remaining rows
    with the column's ORIGINAL UDF (original knobs). A changed derivation knob would
    make the uploaded objects and the ``.seedrun.json`` disagree — refuse instead.
    """
    drift = [
        f"{field}: config={was!r} != current={now!r}"
        for field, was, now in (
            ("seed_run_salt", existing.seed_run_salt, salt),
            ("object_count", existing.object_count, cfg.object_count),
            ("accounts", list(existing.accounts), list(cfg.accounts)),
            ("container", existing.container, cfg.loose_container),
            ("base_prefix", existing.base_prefix, cfg.base_prefix),
            ("prefix_count", existing.prefix_count, cfg.prefix_count),
            ("image_format", existing.image_format, cfg.image_format),
            ("include_large_tail", existing.include_large_tail, cfg.include_large_tail),
            ("max_image_bytes", existing.max_image_bytes, cfg.max_image_bytes),
        )
        if was != now
    ]
    if drift:
        raise RuntimeError(
            f"upload-images resume aborted: knobs differ from the persisted seed-run "
            f"config for {existing.seed_run_id!r}: {'; '.join(drift)}. Use --overwrite "
            "to rebuild, or a new --seed-run-id."
        )


def _build_seed_run_config(
    cfg: BenchConfig, seed_run_id: str, salt: int, manifest_uri: str
) -> SeedRunConfig:
    created = datetime.now(timezone.utc)
    delete_after = created + timedelta(days=30 * cfg.delete_after_months)
    return SeedRunConfig(
        schema_version=SEED_RUN_SCHEMA_VERSION,
        generator_version=constants.GENERATOR_VERSION,
        distribution_version=constants.DISTRIBUTION_VERSION,
        seed_run_id=seed_run_id,
        seed_run_salt=salt,
        object_count=cfg.object_count,
        accounts=list(cfg.accounts),
        container=cfg.loose_container,
        base_prefix=cfg.base_prefix,
        prefix_count=cfg.prefix_count,
        image_format=cfg.image_format,
        include_large_tail=cfg.include_large_tail,
        max_image_bytes=cfg.max_image_bytes,
        created_at=created.isoformat(),
        delete_after=delete_after.isoformat(),
        manifest_uri=manifest_uri,
    )


def run_upload_images(cfg: BenchConfig) -> dict:
    """Create the id table, upload the image dataset, and write the URL manifest."""
    if not cfg.seed_run_id:
        raise ValueError("upload-images requires --seed-run-id")
    if not cfg.accounts:
        raise ValueError("upload-images requires at least one --accounts entry")

    seed_run_id = cfg.seed_run_id
    salt = _seed_run_salt(seed_run_id)
    manifest_uri = cfg.manifest_uri or _default_manifest_uri(cfg, seed_run_id)
    artifact_uri = seed_run_artifact_uri(manifest_uri)
    db_uri, table = benchmark_env.split_source_uri(manifest_uri)
    storage_options = cfg.storage_options
    conn = benchmark_env.connect_geneva(db_uri, storage_options)

    if cfg.cluster:
        # The UDF imports these worker-side; they must be in the manifest env, else
        # the backfill fails per-row with ModuleNotFoundError on the workers.
        _LOG.warning(
            "upload-images on cluster %r: the worker env must include %s (driver "
            "having them is not enough). Register a manifest first with: "
            "`run define-upload-manifest --manifest <name> --account-name %s`, then "
            "pass --manifest <name>.",
            cfg.cluster,
            ", ".join(constants.UPLOAD_WORKER_PIP_DEPS),
            cfg.account_name,
        )

    tbl = _ensure_id_table(
        conn,
        table,
        manifest_uri,
        storage_options,
        cfg.object_count,
        cfg.seed_rows_per_fragment,
    )

    # Rerun safety (mirrors expand/normalize/phash): refuse to silently reuse a
    # manifest built with different knobs. --overwrite drops the columns so the UDF
    # is rebuilt with the new knobs; --reuse-existing/--where continues filling with
    # the column's ORIGINAL parameters.
    output_cols = [name for name, _ in _MANIFEST_FIELDS]
    runner.resolve_existing_columns(tbl, cfg, output_cols, stage="upload-images")

    if _ANCHOR_COLUMN not in tbl.schema.names:
        from geneva.transformer import UnpackedUDF

        # Fresh (or --overwrite-recreated) columns: stamp the seed-run config and
        # register the UDF whose knob-hash version keys its checkpoints.
        record = _build_seed_run_config(cfg, seed_run_id, salt, manifest_uri)
        write_seed_run(artifact_uri, record, storage_options)
        _LOG.info("wrote seed-run config: %s", artifact_uri)
        if cfg.upload_concurrency:
            udf = build_upload_udf_batched(cfg, salt)
        else:
            udf = build_upload_udf(cfg, salt)
        tbl.add_columns(UnpackedUDF(udf, prefix=""))
        _LOG.info("added manifest columns to %s", manifest_uri)
    else:
        # Resume: remaining rows fill via the stored (original-knob) UDF, so the
        # persisted config must still match the current knobs (else they diverge).
        _assert_seed_run_compatible(
            read_seed_run(artifact_uri, storage_options), cfg, salt
        )
        if cfg.upload_concurrency:
            # Execution shape only (same derived data), so this is a warning, not
            # a compat failure like the derivation knobs above.
            _LOG.warning(
                "--upload-concurrency has no effect on a resume: the existing "
                "manifest columns re-run their stored UDF; use --overwrite to "
                "rebuild with the batched uploader"
            )
        _LOG.info("resuming seed run %s (config unchanged)", seed_run_id)

    num_fragments = len(tbl.get_fragments())
    # Window on image_id (not row_index) with the seed-specific fragment size.
    window_cfg = attrs.evolve(
        cfg, row_index_col="image_id", rows_per_fragment=cfg.seed_rows_per_fragment
    )
    kwargs = runner.backfill_kwargs(window_cfg, num_fragments=num_fragments)
    if not cfg.where:
        # Default resume: only process rows not yet attempted. The anchor `url` is
        # written for EVERY processed row (success or failure), so `url IS NULL`
        # selects exactly the unprocessed rows. This overrides geneva's unpacked-group
        # default (an OR of `<col> IS NULL` that includes the always-null-on-success
        # `error` column), which would otherwise re-touch every already-successful
        # row on resume — a full conflict/HEAD pass at 100M. Repair failed rows
        # explicitly with `--where "ok = false"`.
        window_where = kwargs.get("where")
        resume = f"{_ANCHOR_COLUMN} IS NULL"
        kwargs["where"] = f"({window_where}) AND {resume}" if window_where else resume
    _LOG.info(
        "upload backfill: object_count=%s fragments=%s where=%s concurrency=%s "
        "upload_concurrency=%s",
        cfg.object_count,
        num_fragments,
        kwargs.get("where", "<unfilled manifest rows>"),
        cfg.concurrency,
        cfg.upload_concurrency,
    )

    started = time.time()
    with runner.context(conn, cfg):
        tbl.backfill(_ANCHOR_COLUMN, **kwargs)
    elapsed = time.time() - started
    tbl.checkout_latest()

    total = tbl.count_rows()
    filled = tbl.count_rows(filter=f"{_ANCHOR_COLUMN} IS NOT NULL")
    uploaded_ok = tbl.count_rows(filter="ok = true")
    errors = filled - uploaded_ok
    error_rate = (errors / filled) if filled else 0.0
    # Size-fidelity (distinct from upload success): rows whose actual encoded size
    # missed the assigned Atlas bucket. Warned, not failed — ok tracks upload only.
    bucket_misses = tbl.count_rows(
        filter="ok = true AND target_bucket != actual_bucket"
    )
    miss_rate = (bucket_misses / uploaded_ok) if uploaded_ok else 0.0
    if miss_rate > cfg.max_bucket_miss_rate:
        _LOG.warning(
            "bucket_miss_rate %.4f exceeds max %.4f (%d/%d rows landed outside their "
            "assigned size bucket); the recorded distribution is in actual_bucket",
            miss_rate,
            cfg.max_bucket_miss_rate,
            bucket_misses,
            uploaded_ok,
        )
    metrics = {
        "stage": "upload-images",
        "seed_run_id": seed_run_id,
        "manifest_uri": manifest_uri,
        "seed_run_config_uri": seed_run_artifact_uri(manifest_uri),
        "object_count": cfg.object_count,
        "upload_concurrency": cfg.upload_concurrency,
        "num_fragments": num_fragments,
        "total_rows": total,
        "rows_filled": filled,
        "uploaded_ok": uploaded_ok,
        "errors": errors,
        "error_rate": round(error_rate, 6),
        "bucket_misses": bucket_misses,
        "bucket_miss_rate": round(miss_rate, 6),
        "elapsed_seconds": round(elapsed, 2),
        "ok": (
            error_rate <= cfg.max_error_rate and miss_rate <= cfg.max_bucket_miss_rate
        ),
    }
    _LOG.info("upload-images complete: %s", metrics)
    return metrics
