"""log_dataset: identify, host, preview and register a dataset within a bounded wait; queue what cannot land now."""

from __future__ import annotations
import os
import tempfile
import threading
import time
from typing import TYPE_CHECKING, Any, Iterable, Mapping

from .. import errors
from .vocab import HashMode

if TYPE_CHECKING:  # pragma: no cover
    from ..client.client import Client
    from ..run.run import Run
from probe.sdk.artifact.record_formats.lines import _LINE_SUFFIXES, preview_sample
from probe.sdk.catalog.hosting import MANIFEST_SECONDS, host
from probe.sdk.catalog.identity import Prepared, registration_body, run_file_spec, to_display_path
from probe.sdk.catalog.catalog import _send
from probe.sdk.catalog.refs import DatasetRef, check_name, composition_parts, is_moving_ref
from probe.sdk.catalog.server import (
    _say,
    _warn_failure,
    _warn_once,
    catalog_available,
    could_succeed_later,
    old_server,
    warn_not_queued,
)
#: How long `log_dataset` waits for its registration before returning a pending ref (Q9; a slow server must not hold a training loop).
REGISTER_WAIT_SECONDS = 10.0
#: Bound on the registration's background retries, after which it is queued in the outbox.
REGISTER_DEADLINE_SECONDS = 60.0
#: Names reserved for Probe's own rows at the server (C8g).
PREVIEW_PREFIX = ".probe/previews/"


def _previewable(prepared: Prepared) -> str | None:
    """The file a preview is cut from: the dataset, or a folder's first line-record/Parquet file in path order."""
    if prepared.local is None:
        return None
    if prepared.manifest is None:
        return prepared.local
    for f in sorted(prepared.manifest.files, key=lambda f: f.relpath):
        ext = os.path.splitext(f.relpath)[1].lower()
        if ext in _LINE_SUFFIXES + (".parquet",):
            return f.full
    return None


def upload_preview(send: Any, prepared: Prepared, dataset_file_id: str) -> bool:
    """Upload a preview sample of a dataset kept outside Probe as run file
    `.probe/previews/<dataset file id><ext>` (`meta.preview_of`), saying so in one line.
    ``send(name, path, meta)`` uploads to the producing run (SDK `log_artifact`, CLI
    `upload_file`). True if uploaded. Never raises."""
    try:
        source_path = _previewable(prepared)
        if source_path is None:
            return False
        sample = preview_sample(source_path)
        if sample is None:
            return False
        data, records, ext = sample
        handle, tmp = tempfile.mkstemp(prefix="probe-preview-", suffix=ext)
        try:
            with os.fdopen(handle, "wb") as out:
                out.write(data)
            send(f"{PREVIEW_PREFIX}{dataset_file_id}{ext}", tmp, {"preview_of": dataset_file_id})
        finally:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        _say(
            f"probe: uploaded a {records}-row preview of {to_display_path(source_path)}; "
            "preview=False (--no-preview) to stop"
        )
        return True
    except Exception as exc:  # noqa: BLE001 - a preview is never worth a failure
        _warn_once(f"preview:{type(exc).__name__}", f"probe: no preview sample was uploaded ({exc})")
        return False


# log_dataset


def _run_sender(run: "Run") -> Any:
    def send(name: str, path: str, meta: dict) -> None:
        run.log_artifact(name, path=path, sync=True, meta=meta)

    return send


def log_dataset(
    run: "Run",
    path_or_uri: str | os.PathLike,
    name: str,
    *,
    register: bool = True,
    publish: bool = False,
    upload: bool = False,
    sources: Iterable[Any] = (),
    note: str | None = None,
    stats: Mapping[str, Any] | None = None,
    hash: str = HashMode.BUDGET.value,  # noqa: A002 - the plan's name
    composition: Mapping[Any, Any] | None = None,
    preview: bool = True,
    description: str | None = None,
    wait: float = REGISTER_WAIT_SECONDS,
) -> DatasetRef:
    """`Run.log_dataset`; see the module docstring. Never raises."""
    out = DatasetRef(name=name if isinstance(name, str) else None)
    what = f"log_dataset({name!r})"
    try:
        _log_dataset(
            run, out, path_or_uri, name, register=register, publish=publish, upload=upload, sources=sources,
            note=note, stats=stats, hash_mode=hash, composition=composition, preview=preview,
            description=description, wait=wait, what=what,
        )
    except Exception as exc:  # noqa: BLE001 - never into the job
        _warn_failure(exc, what)
        out._done.set()
    return out


def _log_dataset(
    run: "Run",
    out: DatasetRef,
    path_or_uri: str | os.PathLike,
    name: str,
    *,
    register: bool,
    publish: bool,
    upload: bool,
    sources: Iterable[Any],
    note: str | None,
    stats: Mapping[str, Any] | None,
    hash_mode: str,
    composition: Mapping[Any, Any] | None,
    preview: bool,
    description: str | None,
    wait: float,
    what: str,
) -> None:
    client = run._client
    check_name(name)
    parts = composition_parts(composition) if composition else None
    # A registration naming a moving ref is never queued: a replay would resolve it later (D17).
    sources = list(sources or ())
    queue = not any(is_moving_ref(ref) for ref in [*(p["target"] for p in parts or ()), *sources])
    if catalog_available(client) is False:
        raise errors.NotFoundError("Not Found", status=404, detail="Not Found")
    from ..capture import lineage as inputs

    # The run's ONE hashing budget (reads, outputs, datasets).
    budget = inputs.run_hash_budget(run.id)
    before = budget[0]
    try:
        from probe.sdk.catalog.identity import prepare  # call time: one binding, in identity, for tests to patch

        prepared = prepare(path_or_uri, hash_mode=hash_mode, budget=budget, upload=upload)
    finally:
        inputs.charge_run_hash(run.id, before - budget[0])
    out.content_hash, out.identity = prepared.content_hash, prepared.identity
    common = dict(note=note, stats=stats, sources=sources, publish=publish, description=description,
                  composition=parts)
    if upload:
        host(client, name, prepared, say=lambda line: _say(f"probe: {what}: {line}"))
        # The run produced this version: the server records it as the step.
        body = registration_body(
            name, hosted={"manifest_hash": prepared.content_hash, "run_id": run.id}, **common
        )
        _register_bounded(client, body, out, wait=wait, what=what, after=None, queue=queue)
        return
    queued = prepared.manifest is not None and not _ship_manifest(client, prepared)
    if not register:
        row = _record_run_file(run, name, prepared)
        if row and row.get("id"):
            out.artifact_id = str(row["id"])
            out.ref = f"artifact:{row['id']}"
            if preview:
                upload_preview(_run_sender(run), prepared, out.artifact_id)
        out._done.set()
        return
    body = registration_body(name, run_file=run_file_spec(run.id, name, prepared), **common)
    if queued:
        if not queue:
            out.pending = False
            out._done.set()
            warn_not_queued(client, what)
            return
        # The manifest waits in the outbox; the registration waits right behind it.
        _queue_registration(client, body, out, what=what)
        return

    def after() -> None:
        if not preview or prepared.local is None:
            return
        row = run.reconcile_artifact(name, prepared.content_hash)
        if row and row.get("id") and row.get("state") != "queued":
            out.artifact_id = str(row["id"])
            upload_preview(_run_sender(run), prepared, out.artifact_id)

    _register_bounded(client, body, out, wait=wait, what=what, after=after, queue=queue)


def _ship_manifest(client: "Client", prepared: Prepared) -> bool:
    """PUT the manifest within `MANIFEST_SECONDS`. True if it landed; False if it was queued in the
    outbox (the caller queues the registration behind it). A refusal raises."""
    from ..delivery.ops.classify import classify
    from ..delivery.transport.deadlines import deadline_scope

    manifest = prepared.manifest
    assert manifest is not None
    gz = manifest.gz()
    try:
        with deadline_scope(time.monotonic() + MANIFEST_SECONDS):
            client.put_manifest(prepared.content_hash, gz)
        return True
    except errors.RosError as exc:
        if old_server(exc) or classify(exc) in ("permanent", "idempotent"):
            raise
    client.journal.append_catalog_manifest(prepared.content_hash, gz)
    return False


def _queue_registration(client: "Client", body: dict, out: DatasetRef, *, what: str) -> None:
    """Queue the registration behind its queued manifest; ``out`` stays pending."""
    landed = client._enqueue("POST", "/v1/catalog/datasets", body)
    if landed:
        client._after_enqueue()
    out.pending = bool(landed)
    out._done.set()
    _warn_once(
        "log_dataset:queued",
        f"probe: {what}: Probe could not take the dataset's manifest now"
        + (", so it and the registration are queued in the outbox and go when Probe answers."
           if landed else "; the outbox could not hold the registration either, so it was not recorded."),
    )


def _record_run_file(run: "Run", name: str, prepared: Prepared) -> dict | None:
    """`register=False`: the run's dataset file alone, as a reference row (the manifest names its files)."""
    from ..artifact.kinds import ArtifactKind

    body = {
        "kind": ArtifactKind.DATASET.value,
        "name": name,
        "uri": prepared.uri,
        "content_hash": prepared.content_hash,
        "size_bytes": prepared.size_bytes,
        "is_reference": True,
        "meta": dict(prepared.meta),
    }
    return _send(run._client, f"/v1/runs/{run.id}/artifacts", body, what=f"log_dataset({name!r}, register=False)")


def _register_bounded(
    client: "Client", body: dict, out: DatasetRef, *, wait: float, what: str, after: Any, queue: bool = True
) -> None:
    """Send the registration on a thread, waiting at most ``wait`` seconds; past that ``out`` returns
    pending and fills when it lands. A failure that could succeed later is queued unless
    ``queue`` is False (moving ref, D17)."""

    def work() -> None:
        from ..delivery.transport.deadlines import deadline_scope

        try:
            # One bound for the registration AND what follows (finding the run file, the preview).
            with deadline_scope(time.monotonic() + REGISTER_DEADLINE_SECONDS):
                if queue:
                    answer = client.send("POST", "/v1/catalog/datasets", body, raise_permanent=True)
                else:
                    answer = client.send("POST", "/v1/catalog/datasets", body, strict=True)
                if isinstance(answer, dict):
                    out._fill(answer)
                    if callable(after):
                        after()
                else:
                    out.pending = True  # queued in the outbox: delivered later, never filled here
        except Exception as exc:  # noqa: BLE001
            out.pending = False
            if not queue and could_succeed_later(exc):
                warn_not_queued(client, what, exc)
            else:
                _warn_failure(exc, what)
        finally:
            out._done.set()

    out.pending = True
    worker = threading.Thread(target=work, name="probe-log-dataset", daemon=False)
    worker.start()
    if not out._done.wait(max(0.0, float(wait))):
        _warn_once(
            "log_dataset:pending",
            f"probe: {what}: Probe has not answered within {wait:g}s; the registration goes on in "
            "the background (the returned ref fills in when it lands; DatasetRef.wait() waits for it).",
        )
