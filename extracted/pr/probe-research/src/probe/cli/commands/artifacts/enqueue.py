"""queue an artifact write in the outbox: the presign intent ping, the journaled op, the async add, and settling queued uploads before a direct one."""

from __future__ import annotations

import contextlib
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ....sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

import typer

from .... import __version__
from ....foundation.request_identity.request_identity import client_version_headers
from ....sdk.artifact.anchors import Anchor
from ....sdk.settings.settings import resolve
from ....sdk.artifact.hashing import reference_fields
from ....foundation.request_identity.surface import Surface


def _ping_presign(
    anchor: Anchor,
    anchor_id: str | None,
    name: str,
    *,
    digest: str,
    size: int,
    content_type: str | None,
    kind: str | None,
    meta: dict | None,
    span_id: str | None,
    step_index: int | None,
    context: dict | None = None,
) -> str | None:
    """The 1A intent ping: a capped, best-effort presign at enqueue so the
    server's pending row (and its reaper) know this upload is coming. Never
    raises and never waits past the cap -- a dead network degrades to
    local-only enqueue, and the drainer re-presigns on every attempt anyway.
    """
    try:
        from ....sdk.delivery.transport.transport import Transport

        if context is not None:
            # Same principal as the drain will use (red team: an ambient env
            # token could register the intent row under a different tenant
            # than the one the op's pinned context delivers to).
            from ....sdk.delivery.outbox.drain.credentials import _settings_for_op

            settings = _settings_for_op(context)
        else:
            from ....sdk.settings.settings import resolve

            settings = resolve(base_url=_conn.base_url)
        if not settings.token:
            return None
        transport = Transport(
            settings,
            timeout=_PING_TIMEOUT_SECONDS,
            max_retries=_PING_MAX_RETRIES,
            surface=Surface.CLI.value,
            client_headers=client_version_headers("cli", __version__),
        )
        with _client_class()(settings=settings, transport=transport) as ping:
            presign = ping.presign_upload(
                anchor,
                anchor_id,
                name,
                digest=digest,
                size=size,
                content_type=content_type,
                kind=kind,
                meta=meta,
                span_id=span_id,
                step_index=step_index,
            )
        return presign.get("artifact_id")
    except Exception:  # noqa: BLE001 -- intent registration is best-effort by design
        return None


#: The 1A intent-ping cap. Load-bearing product behavior (CHANGELOG: "a
#: ~2s-capped presign ping") -- named so the documented cap and the code
#: cannot silently drift.
_PING_TIMEOUT_SECONDS = 2.0
_PING_MAX_RETRIES = 0


def _artifact_enqueue(
    client: Client,
    anchor: Anchor,
    anchor_id: str | None,
    name: str,
    *,
    path: str | None,
    uri: str | None,
    reference: bool,
    hash_content: bool,
    allow_missing: bool,
    kind: str,
    step: int | None,
    span: str | None,
    content_type: str | None,
    meta: dict | None,
    ping: bool = True,
    require_staged: bool = False,
    in_parts: bool = True,
) -> dict:
    """Journal ONE artifact operation on an already-open async client.

    Split out of :func:`_artifact_add_async` so `--from-manifest` can drive it per
    row: the manifest's whole reason to exist is that opening a client, resolving
    an anchor and starting a process per file is what makes a bulk import cost
    CPU-hours. This function opens nothing, prints nothing, and kicks nothing --
    the caller owns the client and decides when to wake the drainer.

    ``ping=False`` skips the capped presign ping. Intent registration is
    best-effort by contract (the drainer re-presigns on every attempt), and at
    manifest scale a per-row round trip capped at 2s is the very cost the bulk
    path exists to avoid.

    ``require_staged`` refuses to queue an op whose bytes could not be staged,
    returning ``mode="unstaged"`` so the caller can upload synchronously instead.
    Default False keeps the manifest path on its documented trade: at bulk scale
    an unstaged reference is the point, and 200k synchronous fallbacks are not.

    Returns ``{"mode": "reference"|"upload"|"unstaged"|"refused", "op_id":
    str|None, "pinged": bool}``. ``unstaged`` means staging was refused and
    nothing was queued; ``refused`` means the outbox itself could not be written
    and nothing was queued -- both hand the write back to the caller.
    """
    run_ref = anchor_id if anchor is Anchor.RUN else None
    if reference or uri is not None:
        if anchor is Anchor.RUN:
            _async_run(client, anchor_id).log_artifact(
                name,
                path=path,
                uri=uri,
                reference=reference,
                hash_content=hash_content,
                allow_missing=allow_missing,
                kind=kind,
                step_index=step,
                span_id=span,
                content_type=content_type,
                meta=meta,
            )
        else:
            if reference:
                fields = reference_fields(
                    path, hash_content=hash_content, allow_missing=allow_missing
                )
                body = {"name": name, "is_reference": True, **fields}
            else:
                body = {"name": name, "uri": uri, "is_reference": True}
            if content_type:
                body["content_type"] = content_type
            # Literal paths, one per anchor: tests/test_parity.py reads call
            # sites statically, and a table lookup hid this one from it while it
            # still named the leaf door. An experiment's reference is queued by
            # the experiment alone and placed under its project when it drains
            # (`journal._placed`, X21): no network here, and a move before
            # delivery cannot dead-letter it.
            if anchor is Anchor.EXPERIMENT:
                from ....sdk.routes import UNPLACED_PROJECT

                path = f"/v1/projects/{UNPLACED_PROJECT}/experiments/{anchor_id}/artifacts"
            elif anchor is Anchor.PROJECT:
                path = f"/v1/projects/{anchor_id}/artifacts"
            else:
                raise typer.BadParameter(f"a {anchor.value} anchor has no reference form")
            # `_enqueue`, not `journal.append_http`: this was the last bypass of
            # the never-raises rule the upload path adopted.
            if not client._enqueue("POST", path, body):
                return {"mode": "refused", "op_id": None, "pinged": False}
        return {"mode": "reference", "op_id": None, "pinged": False}

    if not path:
        raise typer.BadParameter("needs a file path (--reference, or --uri)")
    if not os.path.isfile(path):
        # A FIFO, device, or procfs stream would block fingerprint/snapshot
        # forever -- async promises bounded enqueue time (codex).
        raise typer.BadParameter(f"{path} is not a regular file")
    from ....sdk.delivery.journal.headroom import INLINE_HASH_MAX_BYTES

    run_only = anchor is Anchor.RUN
    if run_only and in_parts:
        sent = _artifact_enqueue_multipart(
            client, anchor_id, name, path=path, kind=kind, step=step, span=span,
            content_type=content_type, meta=meta,
        )
        if sent is not None:
            return sent
    # Snapshot first, hash the snapshot (inside append_upload): hashing
    # the live file and copying it later would let a same-size rewrite
    # in between poison the content address (codex TOCTOU).
    # `_enqueue_upload`, not `journal.append_upload`: the journal raises on a full
    # or read-only spool (ENOSPC, flock ENOSYS on Lustre/FUSE), and this call site
    # is exactly the one the http-path guard never covered. It also scrubs
    # meta before it reaches the ops file, where a failed op keeps it.
    queued = client._enqueue_upload(
        anchor=anchor.value,
        anchor_id=anchor_id,
        name=name,
        src_path=path,
        inline_hash=os.path.getsize(path) <= INLINE_HASH_MAX_BYTES,
        content_type=content_type,
        kind=kind if run_only else None,
        meta=meta if run_only else None,
        span_id=span,
        step_index=step,
        run_ref=run_ref,
        require_staged=require_staged,
    )
    if queued is None:
        # The outbox refused the write and said so in a warning. Hand it back
        # rather than reporting a queue that does not hold it.
        return {"mode": "refused", "op_id": None, "pinged": False}
    if queued["op_id"] is None:
        # require_staged and no headroom: nothing was appended, so the caller's
        # synchronous upload is the only writer. Leaving an op queued here is
        # what would upload the file twice, with the drainer's later read of a
        # rotated src_path winning.
        return {
            "mode": "unstaged",
            "op_id": None,
            "pinged": False,
            "unstaged_reason": queued.get("unstaged_reason"),
        }
    is_pinged = False
    if ping and queued["blob"] is not None:
        is_pinged = (
            _ping_presign(
                anchor,
                anchor_id,
                name,
                digest=queued["blob"],
                size=queued["size_bytes"],
                content_type=content_type,
                kind=kind if run_only else None,
                meta=meta if run_only else None,
                span_id=span,
                step_index=step,
                context=client.journal.context,
            )
            is not None
        )
    return {"mode": "upload", "op_id": queued["op_id"], "pinged": is_pinged}


def _queue_is_deliverable() -> bool:
    """What `_async_client` insists on: a credential the background drainer can
    use. Without one the synchronous path stands."""
    from ....sdk.settings.settings import resolve

    settings = resolve(base_url=_conn.base_url)
    return bool(settings.token or settings.ingest_token)


def _artifact_add_async(
    client: Client,
    anchor: Anchor,
    anchor_id: str | None,
    name: str,
    *,
    path: str | None,
    uri: str | None,
    reference: bool,
    hash_content: bool,
    allow_missing: bool,
    kind: str,
    step: int | None,
    span: str | None,
    content_type: str | None,
    meta: dict | None,
) -> bool:
    """Queue an artifact operation and return immediately.

    Returns True when the write is queued, False when the caller must upload it
    SYNCHRONOUSLY instead -- staging was refused, or the outbox could not be
    written. False is not an error: it means nothing was enqueued, so the caller
    is now the only writer and must actually do the write.

    Reference/uri forms are pure JSON writes and journal as http ops -- zero
    staging, the fastest path. Byte uploads snapshot into the blob store;
    files at or under the 11A threshold fingerprint inline and fire the capped
    presign ping so the server registers intent, bigger files defer hashing to
    the drainer so return time stays flat.

    Takes the caller's client rather than opening its own: the caller already
    resolved the write mode and holds a client that agrees with it, and opening
    a second one here could disagree with that decision.
    """
    result = _artifact_enqueue(
        client,
        anchor,
        anchor_id,
        name,
        path=path,
        uri=uri,
        reference=reference,
        hash_content=hash_content,
        allow_missing=allow_missing,
        kind=kind,
        step=step,
        span=span,
        content_type=content_type,
        meta=meta,
        # The single-file path REFUSES an unstaged op. An unstaged op records
        # src_path and the drainer reads the live file at delivery, so a bare
        # `probe artifact add ckpt.pt` beside a rotating training loop would
        # upload step-1100 bytes under the step-1000 name. Nobody asked for that
        # by typing a bare command. The manifest path keeps the old trade.
        require_staged=True,
    )
    if result["mode"] in ("unstaged", "refused"):
        return False
    _kick_drainer()
    if result["mode"] == "reference":
        print(f"added reference {name!r} (queued)")
        _say_where_the_kind_went(kind)
        return True
    registered = "intent registered" if result["pinged"] else "intent deferred to drain"
    print(f"added upload {name!r} op={result['op_id']} ({registered}) (queued)")
    _say_where_the_kind_went(kind)
    return True


@contextlib.contextmanager
def _queue_client_if_possible(explicit: bool | None):
    """Yield a client for the queue path, or None when there is no queue path.

    `explicit is False` means the caller has already ruled queueing out --
    `--sync`, or a non-run anchor taking the synchronous default. Constructing a
    client to ask it a question whose answer is known, and then closing it, is
    pure cost; the synchronous path below opens its own.
    """
    if explicit is False:
        yield None
        return
    client = _default_client(explicit)
    try:
        yield client
    finally:
        client.close()


def _drain_colliding_uploads(anchor: Anchor, anchor_id: str | None, name: str) -> None:
    """Deliver any QUEUED upload for this same (anchor, name) before a direct one.

    A direct upload carries no journal sequence number, so it can land ahead of a
    queued write that was made EARLIER for the same name -- and which of two
    same-name artifacts a later lookup returns is decided by recency at the
    server, not by the order you logged them. Delivering the queued one first
    restores the order the caller actually wrote in.

    Runs before EVERY direct upload, not only the low-disk fallback: `--sync` and
    a credential-degraded session reach the server the same way and invert the
    same order. It is still free on the hot path, because a QUEUED add never gets
    here -- which is what keeps the per-append O(N^2) listdir curve that
    b820e9c8 removed from coming back.

    Best-effort by contract: this improves ordering, it is not a lock. A failure
    to drain must never stop the upload the user asked for.
    """
    # RUN ANCHORS ONLY. Only run-anchored uploads queue by default, only their
    # ops carry the `run_ref` that `drain` scopes on, and only their `anchor_id`
    # is already resolved -- a project or workspace anchor_id here is still a
    # SLUG (`_anchor_id_for` runs later) while the queued op stored a uuid, so
    # the comparison could never match and bought a full queue parse to find
    # nothing, on exactly the anchors this change made always-synchronous.
    if anchor is not Anchor.RUN or not anchor_id:
        return
    try:
        journal = _journal()
        colliding = [
            op
            for queue in journal.namespaces()
            for _, op in queue.pending()
            if (op.get("upload") or {}).get("name") == name
            and (op.get("upload") or {}).get("anchor") == anchor.value
            and (op.get("upload") or {}).get("anchor_id") == anchor_id
            and op.get("run_ref")
        ]
        if not colliding:
            return
        # Scope the drain to the runs those ops belong to. Machine-wide flush is
        # deliberately not used: 747d2a46 removed it from this very path because
        # it dragged a neighbour's whole backlog through one artifact upload.
        from ....sdk.delivery.outbox.drain.drain import drain

        # wait_for_lock=False: the default BLOCKS on the drain flock until the
        # background worker finishes its whole pass, and a blocked wait is not an
        # exception, so the `except` below would never see it -- an ordering
        # courtesy could hang the upload it exists to precede. Under
        # async-by-default a run's queue routinely holds thousands of ops.
        for run_scope in {op["run_ref"] for op in colliding}:
            drain(journal, run_ref=run_scope, wait_for_lock=False)
    except Exception:  # noqa: BLE001 -- ordering is a courtesy, the upload is the job
        pass
from probe.cli.commands.artifacts.multipart import _artifact_enqueue_multipart  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.artifacts.row_checks import _say_where_the_kind_went  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.refs import run_ref  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.run_handle import _async_run  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client_class, _conn, _default_client, _journal, _kick_drainer  # noqa: E402 -- pieces need each other; the front door loads this one first
