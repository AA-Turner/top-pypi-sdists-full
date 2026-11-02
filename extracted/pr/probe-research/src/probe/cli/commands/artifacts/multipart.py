"""files over the 64 MiB inspection limit, queued in parts: run-anchored and project/experiment/workspace-anchored."""

from __future__ import annotations
import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ....sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

import typer
from ....sdk.artifact.anchors import Anchor


def _artifact_enqueue_multipart(
    client: Client,
    run_ref: str | None,
    name: str,
    *,
    path: str,
    kind: str,
    step: int | None,
    span: str | None,
    content_type: str | None,
    meta: dict | None,
) -> dict | None:
    """A run file over the 64 MiB inspection limit, queued in parts.

    `_enqueue_upload` cannot take it: `check_upload` refuses anything over the
    limit, so before this the CLI handed a big file back to a synchronous upload
    and the daemon's 180 s call timed out under it. The run handle's own
    multipart door (`Run._maybe_multipart`) holds every gate -- the server
    advertising `artifact_multipart`, `PROBE_ARTIFACT_OPAQUE_POLICY=block`, an
    offline client -- so this only asks it to QUEUE (never upload in-process).

    None when the file is small or the door is shut (the caller's path stands);
    otherwise the same answer `_artifact_enqueue` gives: ``upload`` with the
    multipart op's id, or ``unstaged`` when the bytes could not be staged (the
    caller then uploads synchronously, as for any unstaged file).
    """
    from ....sdk.artifact.storage_handlers import multipart as _multipart
    from ....sdk.redaction import default_scrub, scrub_string
    from ....sdk.run.files.uploads import _NOT_QUEUED
    from ....sdk.secret_gate import CredentialInPath
    from ....sdk.secret_gate import _check_path as _check_upload_path

    if run_ref is None or not getattr(client, "async_writes", False) or not _multipart.over_threshold(path):
        return None  # an enqueue never uploads in-process
    if not _outbox_lasts(client):
        # An outbox on a throwaway disk (a pod without a volume, Modal, CI):
        # `run end` does not wait on parts, so the op would go with the box
        # and leave no record. The synchronous path uploads or points to it.
        return None
    try:
        _check_upload_path(path)
    except CredentialInPath:
        return None  # the single-PUT path refuses it, with its own message
    # What `Run.log_artifact` scrubs before its own multipart door, because the
    # op file outlives the command (a dead-lettered one stays in failed/).
    name = scrub_string(name)  # see `Client.upload`: a name is a path, not prose
    meta = default_scrub(dict(meta or {}))
    handle = _async_run(client, run_ref)
    reasons: list[str] = []

    def refused(reason: str) -> None:
        reasons.append(reason)

    handled = handle._maybe_multipart(
        name, path, kind=kind, content_type=content_type, span_id=span, step_index=step,
        meta=meta, strict=False, sync=False, refused=refused,
    )
    if handled is _NOT_QUEUED:
        return None
    if reasons:
        return {"mode": "unstaged", "op_id": None, "pinged": False, "unstaged_reason": reasons[0]}
    ops = getattr(handle, "_multipart_ops", None) or [None]
    return {"mode": "upload", "op_id": ops[-1], "pinged": False}


def _outbox_lasts(client: Client) -> bool:
    """Whether this client's outbox survives the process (not a throwaway
    disk), so a queued multipart op will be carried by the detached worker.
    Unknown storage counts as lasting, as `multipart.settle_reason` does."""
    try:
        from ....sdk.run.launch import ephemeral

        return bool(ephemeral.describe(str(client.journal.dir)).get("durable", True))
    except Exception:  # noqa: BLE001 -- unknown storage: trust the worker
        return True


def _goes_in_parts(anchor: Anchor, path: str | None, *, uri: str | None, reference: bool) -> bool:
    """A run-anchored upload of a regular file over the 64 MiB inspection limit."""
    if anchor is not Anchor.RUN or uri is not None or reference or not path:
        return False
    from ....sdk.artifact.storage_handlers import multipart as _multipart

    return os.path.isfile(path) and _multipart.over_threshold(path)


def _artifact_add_anchored_multipart(
    anchor: Anchor,
    anchor_id: str | None,
    name: str,
    path: str,
    *,
    content_type: str | None,
    write_mode: bool | None,
) -> bool:
    """A file over 64 MiB for a project, experiment, workspace or the team
    Shared folder, in parts (0333; bigger-uploads plan D5).

    The single presigned PUT these anchors have cannot take it: the credential
    gate's 64 MiB inspection limit refuses it before the request. So it goes
    the way a run's big file goes (`sdk/artifact/storage_handlers/multipart/multipart.py`): STAGED into the outbox
    and queued, returning at once, the worker sending the parts later -- or,
    under an explicit ``--sync``, or with no queue to carry it (a client that
    cannot drain), or bytes that cannot be staged, sent in parts now.

    Only for a regular file over the threshold, on a server that declares
    ``artifact_multipart_anchored``, and never under
    ``PROBE_ARTIFACT_OPAQUE_POLICY=block`` (multipart bytes reach storage
    before anything reads them). False leaves the write to today's path.
    """
    from ....sdk.artifact.storage_handlers import multipart as _multipart
    from ....sdk import secret_gate as _gate

    if not os.path.isfile(path) or not _multipart.over_threshold(path):
        return False
    if not _gate.policy().allow_opaque:
        return False
    explicit = _resolve_write_mode(write_mode)
    # Queued unless --sync says otherwise, even under PROBE_ASYNC=0 (the Probe
    # daemon's setting, with a 180 s call), as for a run's big file; a client
    # with no credential the drainer could use keeps the in-process path.
    client = _async_client() if explicit is not False and _queue_is_deliverable() else _default_client(explicit)
    try:
        try:
            is_supported = client.supports_feature(_multipart.ANCHORED_FEATURE) is True
        except Exception:  # noqa: BLE001 -- a probe that failed is not a declaration
            is_supported = False
        if not is_supported:
            return False
        with _client() as lookup:
            anchor_id = _anchor_id_for(lookup, anchor, anchor_id)
        fields: dict[str, Any] = {
            "anchor": anchor.value,
            "anchor_id": anchor_id,
            "name": name,
            "src": path,
            "kind": None,
            "content_type": content_type,
            "meta": None,
            "span_id": None,
            "step_index": None,
        }
        if explicit is not False and client.async_writes and _outbox_lasts(client):
            journal = client.journal
            try:
                op = _multipart.build_op(journal, **fields)
            except (_multipart.StageRefused, OSError) as exc:
                refusal = str(exc) or type(exc).__name__
            else:
                try:
                    _multipart.enqueue(journal, op)
                except Exception as exc:  # noqa: BLE001 -- a full outbox: send it now instead
                    _multipart.release_staged(op["multipart"])
                    refusal = f"the outbox could not take it ({exc})"
                else:
                    client._after_enqueue()
                    _kick_drainer()
                    mib = os.path.getsize(path) // (1 << 20)
                    print(f"added upload {name!r} op={op['op_id']} (in parts, {mib} MiB) (queued)")
                    return True
            # Nothing is queued, so this process is the only writer: send it
            # now, as `_artifact_add_async` hands a run's back when staging is
            # refused.
            typer.echo(f"probe: {name!r} was not queued: {refusal}; uploading it in parts now", err=True)
        _print_json(_multipart.upload_now(client, **fields))
        return True
    finally:
        client.close()
from probe.cli.commands.artifacts.anchors import _anchor_id_for  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.artifacts.enqueue import _queue_is_deliverable  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.refs import run_ref  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.run_handle import _async_run  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _async_client,
    _client,
    _default_client,
    _kick_drainer,
    _resolve_write_mode,
)
