"""CreateRunHandler (OpHandler): deliver an offline run's create under its on_conflict policy and record local key -> server id."""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING, Any

from .... import errors
from .....foundation.safe_warn import safe_warn as _diagnostics
from probe.sdk.routes import WriteOp, path_for

if TYPE_CHECKING:
    from ....client.client import Client
    from ...journal.journal import Journal


# -- the drain's half (called from journal._execute) ----------------------------
def bind_local_refs(journal: Journal, op: dict) -> None:
    """Rewrite ``local:<key>`` to the run's server id in the op's path, body and upload
    anchor. ``run_ref`` keeps the key (the run's lane identity)."""
    ref = str(op.get("run_ref") or "")
    key = ref[len(LOCAL_PREFIX) :]
    entry = read_mapping(journal.dir).get(key)
    if not entry or not entry.get("id"):
        raise errors.OfflineRunNotCreated(
            f"offline run {ref} is not on the server yet: its create has not been "
            "delivered (still queued, or refused: its own error says why and names the "
            "fix). `probe sync --list` shows it."
        )
    run_id = str(entry["id"])
    if isinstance(op.get("path"), str):
        op["path"] = op["path"].replace(ref, run_id)
    if op.get("body") is not None:
        op["body"] = _replace(op["body"], ref, run_id)
    upload = op.get("upload")
    if isinstance(upload, dict) and upload.get("anchor_id") == ref:
        upload["anchor_id"] = run_id


def _replace(value: Any, old: str, new: str) -> Any:
    if isinstance(value, str):
        return value.replace(old, new) if old in value else value
    if isinstance(value, list):
        return [_replace(v, old, new) for v in value]
    if isinstance(value, dict):
        return {k: _replace(v, old, new) for k, v in value.items()}
    return value


def deliver_create(journal: Journal, client: Client, op: dict) -> dict:
    """Deliver an offline run's create and record ``key -> id`` before the op is
    dequeued. Idempotent by creation key: a crash between create and mapping replays the
    create and gets the same run.

    The OFFLINE create always goes first. A create the init fallback kept a sent request
    for (``create["request"]``) replays it verbatim only when the server answers that the
    key already made a run (422 ``creation_key_reused``: the online create landed, its
    answer was lost). Never on a client-side guess."""
    create = op.get("create") or {}
    key = str(create.get("creation_key") or "")
    if not key:
        raise errors.ValidationError(f"offline create op {op.get('op_id')} has no creation_key", status=422)
    known = read_mapping(journal.dir).get(key)
    if known and known.get("id"):
        return {"id": known["id"]}
    kept = create.get("request")
    via = "offline"
    try:
        path = create.get("path") or _home_path(client, create, key)
        if path == UNFILED_CREATE_PATH:
            raise _no_home(key)
        try:
            row = _create_with_policy(client, path, create)
        except errors.RosError as gone:
            # The fallback's create carries the home init resolved (project or experiment
            # id); deleted or trashed since, the POST is a 404/410. Name the fix instead
            # of dead-lettering a bare "not found".
            if not (isinstance(gone, errors.NotFoundError) or gone.status == 410):
                raise
            raise errors.ValidationError(
                f"offline run {local_ref(key)} was recorded for a project or experiment "
                f"that is gone from this server ({gone}). File it somewhere that exists: "
                "`probe sync <its folder> --project <slug>` (and `--experiment <slug>`).",
                status=422,
            ) from gone
    except errors.ValidationError as exc:
        if kept is None or not _key_made_a_run(exc):
            raise
        try:
            row = _post(client, kept["path"], kept["body"])
        except errors.ValidationError as again:
            if not _key_made_a_run(again):
                raise
            raise errors.ValidationError(
                f"offline run {local_ref(key)}: the create init sent online before the "
                "outage made a run under this key, but this login cannot replay it (only "
                "the user who sent it can). Sync this folder logged in as that user.",
                status=422,
            ) from again
        via = "online"
    _write_mapping(journal.dir, key, row["id"], via=via)
    return row


def _key_made_a_run(exc: errors.RosError) -> bool:
    detail = exc.detail if isinstance(exc.detail, dict) else {}
    return exc.status == 422 and detail.get("code") == "creation_key_reused"


def _post(client: Client, path: str, body: dict) -> dict:
    # The server declares run_creation_key (checked before a sync starts), so a create
    # whose answer is lost is safe to re-send: retried like a read.
    return client.transport.request("POST", path, json_body=body, idempotent=True).json()


#: Where an older CLI sent a run with no home. Never sent again: every run has a project.
UNFILED_CREATE_PATH = "/v1/runs"


def _no_home(key: str) -> errors.ValidationError:
    """An older CLI queued this create with no project: refused here, refiled by the researcher."""
    return errors.ValidationError(
        f"offline run {local_ref(key)} was recorded with no project, and every run needs one. "
        "File it: `probe sync <its folder> --project <slug>` (and `--experiment <slug>`).",
        status=422,
    )


def _home_path(client: Client, create: dict, key: str) -> str:
    project, experiment = create.get("project"), create.get("experiment")
    question = create.get("question")
    if not project and not experiment:
        raise _no_home(key)
    try:
        project_id = None
        if project:
            # `workspace=` (kept as given) files a NEW project; without it, the
            # syncing computer's workspace (`Client.create_project`).
            workspace = create.get("workspace")
            # An id-shaped project is resolved, never created (`Client._project_named`).
            by_id, slug = client._project_named(project)
            project_id = (
                by_id["id"]
                if by_id is not None
                else client.ensure_project(slug, **({"workspace_id": workspace} if workspace else {}))["id"]
                if question is not None
                else client.resolve_or_raise("project", slug)["id"]
            )
        if experiment:
            if question is not None:
                exp = client.ensure_experiment(
                    experiment, create.get("experiment_name"), question=question, project_id=project_id
                )
            else:
                exp = client.resolve_or_raise("experiment", experiment, project_id=project_id)
            if project_id and exp.get("project_id") not in (None, project_id):
                # As online (`_resolve_run_experiment`): never filed in another project unsaid.
                raise errors.ValidationError(
                    f"offline run {local_ref(key)} was recorded for experiment {experiment!r} in project "
                    f"{project!r}, but that experiment is in another project. File it: "
                    "`probe sync --project <slug>` (and `--experiment <slug>`).",
                    status=422,
                )
            # The experiment API's run create: under the project it is filed
            # in (an experiment row always names it).
            return f"/v1/projects/{exp['project_id']}/experiments/{exp['id']}/runs"
        return f"/v1/projects/{project_id}/runs"
    except errors.NotFoundError as exc:
        where = f"project {project!r}" + (f", experiment {experiment!r}" if experiment else "")
        raise errors.ValidationError(
            f"offline run {local_ref(key)} was recorded for {where}, which does not exist "
            f"on this server ({exc}). File it somewhere that does: "
            "`probe sync --project <slug>` (and `--experiment <slug>`).",
            status=422,
        ) from exc


def _create_with_policy(client: Client, path: str, create: dict) -> dict:
    body = create["body"]
    ref = local_ref(str(create.get("creation_key")))
    try:
        return _post(client, path, body)
    except errors.ConflictError as conflict:
        base = body.get("external_id")
        if create.get("on_conflict") == "supersede" and base is not None:
            incumbent = conflict.existing_id
        else:
            # Re-raised WITHOUT `existing_id`: the drain reads a 409 naming one on a retried
            # op as its own earlier delivery and would drop this create with no mapping,
            # stranding every write behind it.
            raise errors.ConflictError(_conflict_message(client, ref, base, conflict)) from conflict
    # SUPERSEDE: a fresh run as <external_id>-rN with retry lineage, each slot
    # under a key DERIVED from the run's own, so a re-sync replays the same one.
    for n in range(2, 7):
        retry = dict(
            body,
            external_id=f"{base}-r{n}",
            creation_key=hashlib.sha256(f"{create['creation_key']}:r{n}".encode()).hexdigest()[:32],
        )
        if incumbent:
            retry.update(
                parent_run_id=str(incumbent), parent_relation="retry", parent_provenance="observed_call"
            )
        try:
            row = _post(client, path, retry)
        except errors.ConflictError:
            continue
        _mark_supersede(client, row, incumbent, n)
        return row
    raise errors.ConflictError(f"{ref}: no free retry slot for {base!r} after 5 attempts")


def _conflict_message(client: Client, ref: str, base: str | None, conflict: errors.ConflictError) -> str:
    if base is None:
        return f"offline run {ref}: {conflict}"
    holder = conflict.existing_id
    status = None
    if holder:
        try:
            status = (client.transport.get(f"/v1/runs/{holder}") or {}).get("status")
        except errors.RosError:
            status = None  # only for the message
    held = f"run {holder}" + (f" ({status})" if status else "") if holder else "another run"
    return (
        f"offline run {ref} was recorded with external_id {base!r}, which {held} already "
        "has on this server. An offline recording cannot resume that run; deliver it as "
        f"a retry of it with `probe sync <its folder> --on-conflict supersede` (it opens as "
        f"{base}-r2, linked to it)."
    )


def _mark_supersede(client: Client, row: dict, incumbent: str | None, attempt: int) -> None:
    """What an online supersede records (`Client._create_run_with_policy`): the new run's
    ``retry_of``/``retry_attempt`` foreign keys and a dead incumbent tagged
    ``superseded``. Both idempotent (per-key merge, a set), so a re-synced slot repeats
    them harmlessly. Best effort: the run and its data matter more than lineage tags."""
    if not incumbent:
        return
    try:
        client.transport.request(
            "PATCH",
            path_for(WriteOp.RUN_PATCH, row['id']),
            json_body={"foreign_keys": {"retry_of": str(incumbent), "retry_attempt": attempt}},
            idempotent=True,
        )
        old = client.transport.get(f"/v1/runs/{incumbent}") or {}
        if old.get("status") in client._DEAD_RUN_STATUSES:
            tags = sorted({*(old.get("tags") or []), "superseded"})
            client.transport.request(
                "PATCH", path_for(WriteOp.RUN_PATCH, incumbent), json_body={"tags": tags}, idempotent=True
            )
    except errors.RosError as exc:
        _diagnostics.warn(
            f"probe sync: run {row.get('id')} superseded {incumbent}, but its retry lineage "
            f"(retry_of, the incumbent's `superseded` tag) was not recorded: {exc}"
        )
from probe.sdk.delivery.offline.offline import LOCAL_PREFIX, local_ref  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.offline.queue import _write_mapping, read_mapping  # noqa: E402 -- pieces need each other; the front door loads this one first
