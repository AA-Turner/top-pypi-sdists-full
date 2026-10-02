"""Optional W&B history through project attachments and server-owned jobs.

File receipts never cover this lane. The reviewed destination and request key
are committed before admission; a lost response must never mint a new import.
No credentials, metric writes, local snapshots or session associations belong
here. Background admission uses explicitly approved mappings and durable request keys.
"""

from __future__ import annotations

import copy
import hashlib
from dataclasses import asdict
from uuid import UUID, uuid4
from urllib.parse import urlsplit, urlunsplit

from ..sdk import errors
from ..sdk import agent_session
from . import tui
from .backfill_coverage import CoverageError

KEY = "wandb_history"
SOURCE_SCHEMA = "probe.wandb-source/1"
AUTOMATIC_APPROVAL_SCHEMA = "probe.wandb-import-approval/1"
MAX_IMPORTS = 16
MAX_ACCOUNTS = 20
MAX_OPTIONS = 200
JOB_STATES = {"queued", "running", "cancel_requested", "canceled", "completed", "failed"}


class HistoryResult(list[str]):
    """Status lines plus whether the selected source was reviewed or skipped."""

    def __init__(self, lines=(), *, source_resolved=False):
        super().__init__(lines)
        self.source_resolved = source_resolved


def _uuid(value):
    return str(UUID(str(value)))


def _text(value, limit=180):
    return " ".join(str(value).split())[:limit]


def _root(value):
    if not isinstance(value, str) or len(value) > 1024:
        raise CoverageError("Invalid W&B source identity.")
    parts = value.split("/")
    if len(parts) != 2 or any(
        not part or part in {".", ".."} or any(c.isspace() or ord(c) < 32 for c in part)
        for part in parts
    ):
        raise CoverageError("Expected an exact W&B entity/project source identity.")
    return value


def _projects(coverage):
    projects = {
        row["project_id"]: row.get("project_slug") or row["project_id"]
        for row in coverage.rows()
        if row["project_id"]
    }
    if coverage.scope.project_id:
        projects.setdefault(coverage.scope.project_id, coverage.scope.project_id)
    return projects


def _load(coverage, projects):
    identity = {
        "schema": 1,
        "scope": asdict(coverage.scope),
        "folder_source_id": coverage.source_id,
    }
    saved = coverage.meta(KEY)
    state = copy.deepcopy(saved) if saved is not None else {**identity, "imports": []}
    if any(state.get(key) != value for key, value in identity.items()):
        raise CoverageError("Saved W&B history belongs to a different source or destination scope.")
    items = state.get("imports")
    if not isinstance(items, list) or len(items) > MAX_IMPORTS:
        raise CoverageError("Saved W&B history has an invalid import list.")
    seen = set()
    for item in items:
        if item.get("project_id") not in projects:
            raise CoverageError(
                "Saved W&B destination is not one of this import's reviewed projects."
            )
        for key in ("project_id", "connection_id", "idempotency_key"):
            if _uuid(item[key]) != item[key]:
                raise CoverageError("Saved W&B history has an invalid identity.")
        root = _root(item["external_id"])
        if root in seen:
            raise CoverageError("Saved W&B source has more than one mapping.")
        seen.add(root)
        for key in ("attachment_id", "job_id", "retry_of", "experiment_id"):
            if item.get(key) and _uuid(item[key]) != item[key]:
                raise CoverageError("Saved W&B history has an invalid receipt.")
        if item.get("job_id") and not item.get("attachment_id"):
            raise CoverageError("Saved W&B job has no attachment identity.")
    return state


def _save(coverage, state):
    if coverage.meta(KEY) != state:
        coverage.put_meta(KEY, state)


def _attachment(row, item):
    if not isinstance(row, dict) or any(
        str(row.get(key)) != item[key] for key in ("project_id", "connection_id", "external_id")
    ):
        raise CoverageError(
            "W&B attachment response did not match the reviewed destination/source."
        )
    if row.get("experiment_id") != item.get("experiment_id"):
        raise CoverageError("W&B attachment response did not match the reviewed experiment destination.")
    ident = _uuid(row["id"])
    if item.get("attachment_id") and item["attachment_id"] != ident:
        raise CoverageError("W&B attachment identity changed; the saved intent was retained.")
    if row.get("state") != "active" or "backfill" not in row.get("features", []):
        raise CoverageError("W&B attachment needs review before history can start.")
    return ident


def _job(row, item, coverage):
    expected = {
        "source": "wandb",
        "connection_id": item["connection_id"],
        "project_id": item["project_id"],
        "attachment_id": item["attachment_id"],
        "workspace_id": coverage.scope.workspace_id,
    }
    if not isinstance(row, dict) or any(str(row.get(k)) != v for k, v in expected.items()):
        raise CoverageError("W&B job response did not match the saved source/destination.")
    if row.get("experiment_id") != item.get("experiment_id"):
        raise CoverageError("W&B job response did not match the saved experiment destination.")
    scope = row.get("scope")
    if (
        not isinstance(scope, list)
        or len(scope) != 1
        or scope[0].get("external_id") != item["external_id"]
    ):
        raise CoverageError("W&B job returned a different source selection.")
    ident = _uuid(row["id"])
    if item.get("job_id") and item["job_id"] != ident:
        raise CoverageError("W&B job identity changed; the saved receipt was retained.")
    if row.get("state") not in JOB_STATES:
        raise CoverageError("W&B job returned an unknown state.")
    return {
        "id": ident,
        "state": row["state"],
        "processed_count": row.get("processed_count", 0),
        "counts": row.get("counts", {}),
        "warnings": row.get("warnings", [])[:10],
        "last_error": row.get("last_error"),
    }


def _advance(client, coverage, state, item, *, admit):
    # GET reconciliation is permitted even while disconnected or paused. A
    # completed history receipt says what ran; it cannot promise current access.
    if item.get("job_id"):
        row = client.get_project_wandb_backfill(
            item["project_id"], item["attachment_id"], item["job_id"]
        )
    elif not admit:
        return
    else:
        _save(coverage, state)
        if not item.get("attachment_id"):
            if item.get("experiment_id"):
                row = client.attach_experiment_wandb_source(
                    item["experiment_id"], connection_id=item["connection_id"],
                    external_id=item["external_id"],
                )
            else:
                row = client.attach_project_wandb_source(
                    item["project_id"], connection_id=item["connection_id"],
                    external_id=item["external_id"],
                )
            item["attachment_id"] = _attachment(row, item)
            _save(coverage, state)
        if item.get("retry_of"):
            row = client.retry_project_wandb_backfill(
                item["project_id"],
                item["attachment_id"],
                item["retry_of"],
                idempotency_key=item["idempotency_key"],
            )
        else:
            row = client.launch_project_wandb_backfill(
                item["project_id"],
                item["attachment_id"],
                idempotency_key=item["idempotency_key"],
            )
    receipt = _job(row, item, coverage)
    item.update(job_id=receipt["id"], receipt=receipt, error=None)
    _save(coverage, state)


def record_reviewed_selection(coverage, *, project_id, connection_id, external_id, experiment_id=None):
    """Commit an explicitly reviewed mapping; return its immutable request key.

    Programmatic callers own review just as the CLI picker does. This function
    does no HTTP, and never changes a prior source's destination or request key.
    """
    projects = _projects(coverage)
    state = _load(coverage, projects)
    project_id, connection_id = _uuid(project_id), _uuid(connection_id)
    experiment_id = _uuid(experiment_id) if experiment_id is not None else None
    external_id = _root(external_id)
    if project_id not in projects:
        raise CoverageError("W&B destination must be one of this folder's reviewed projects.")
    for item in state["imports"]:
        if item["external_id"] == external_id:
            if (item["project_id"] != project_id or item["connection_id"] != connection_id
                    or item.get("experiment_id") != experiment_id):
                raise CoverageError("This W&B source already has a different saved mapping.")
            return copy.deepcopy(item)
    if len(state["imports"]) >= MAX_IMPORTS:
        raise CoverageError("This folder already has the maximum number of W&B selections.")
    item = {
        "project_id": project_id,
        **({"experiment_id": experiment_id} if experiment_id else {}),
        "connection_id": connection_id,
        "external_id": external_id,
        "attachment_id": None,
        "job_id": None,
        "idempotency_key": str(uuid4()),
        "receipt": None,
        "error": None,
    }
    state["imports"].append(item)
    _save(coverage, state)
    return copy.deepcopy(item)


def admit_reviewed_history(client, coverage, *, project_id, connection_id, external_id, experiment_id=None):
    """Admit/recover one explicit mapping through the same durable CLI boundary.

    Exact request replay recovers lost acknowledgments; a known job is only
    read. Failed jobs are never retried by this entrypoint.
    """
    selected = record_reviewed_selection(
        coverage, project_id=project_id, connection_id=connection_id, external_id=external_id,
        experiment_id=experiment_id,
    )
    state = _load(coverage, _projects(coverage))
    item = next(
        item for item in state["imports"] if item["idempotency_key"] == selected["idempotency_key"]
    )
    _advance(client, coverage, state, item, admit=True)
    return copy.deepcopy(item)


def _review(title, lines, choices, *, default=None):
    options = {"default": default} if default is not None else {}
    answer = tui.review(title, lines, choices, **options)
    if answer is None:
        raise KeyboardInterrupt
    return answer


def _pick(title, rows, *, lines=(), default=None):
    if not rows:
        return None
    answer = _review(
        title, lines,
        [("Skip W&B history", tui.SKIP), *[(_text(label), value) for label, value in rows]],
        default=default if any(value == default for _, value in rows) else None,
    )
    return None if answer is tui.SKIP else answer


def eligible_connections(client):
    """List connected W&B accounts that support explicitly attached history."""
    accounts = client.list_mirror_connections()
    if not isinstance(accounts, list):
        raise CoverageError("W&B accounts could not be listed.")
    return [row for row in accounts
            if isinstance(row, dict) and row.get("source") == "wandb"
            and row.get("status") == "active" and row.get("has_credential")
            and "project_attachments" in row.get("features", [])][:MAX_ACCOUNTS]


def _selection_identity(client):
    identity = client.me()
    parsed = urlsplit(client.settings.base_url)
    if (not identity.get("customer_id") or not identity.get("user_id")
            or not parsed.hostname or parsed.username or parsed.password):
        raise CoverageError("The account for this W&B selection could not be verified.")
    return {
        "backend": urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip("/"), "", "")),
        "customer_id": str(identity["customer_id"]), "user_id": str(identity["user_id"]),
    }


def choose_source(client, *, accounts=None, default=None):
    """Choose a source now; no destination is approved and no import is launched.

    The folder plan supplies destinations before import. Returning BACK revisits the
    caller's upfront offer; None skips W&B, while Ctrl+C remains interruption.
    """
    accounts = eligible_connections(client) if accounts is None else accounts
    if not accounts:
        return None
    connection = next((row for row in accounts if default and row.get("id") == default.get("connection_id")), None)
    selected = None
    while True:
        picked = _pick(
            "Choose a W&B account",
            [(f"{row.get('label') or row.get('name') or 'W&B'} · {row['id']}", row) for row in accounts],
            lines=["Choose the connected account containing the project you want to import."],
            default=connection,
        )
        if picked is tui.BACK or picked is None:
            return picked
        if picked != connection:
            selected = None
        connection = picked
        options = client.list_mirror_scope_options(_uuid(connection["id"]))
        if not isinstance(options, list):
            raise CoverageError("W&B projects could not be listed.")
        choices = [(_root(row["external_id"]), row) for row in options[:MAX_OPTIONS]]
        if selected is None:
            selected = next((row for _, row in choices if default and row["external_id"] == default.get("external_id")), None)
        picked = _pick(
            "Choose W&B history", choices,
            lines=["Choose a W&B project. You'll review its Probe destination after the folder plan is ready."],
            default=selected,
        )
        if picked is tui.BACK:
            continue
        if picked is None:
            return None
        return {"schema": SOURCE_SCHEMA, **_selection_identity(client),
                "connection_id": _uuid(connection["id"]), "external_id": _root(picked["external_id"])}


def _selected_source(client, selection):
    """Resolve the unapproved source afresh before presenting any destination."""
    identity = _selection_identity(client)
    if (not isinstance(selection, dict) or selection.get("schema") != SOURCE_SCHEMA
            or any(selection.get(key) != value for key, value in identity.items())):
        raise CoverageError("This W&B selection belongs to a different account or Probe backend.")
    connection_id, external_id = _uuid(selection["connection_id"]), _root(selection["external_id"])
    connection = next((row for row in eligible_connections(client) if row.get("id") == connection_id), None)
    if connection is None:
        raise CoverageError("The selected W&B account is unavailable. Reconnect it in Integrations, then retry.")
    options = client.list_mirror_scope_options(connection_id)
    if not isinstance(options, list):
        raise CoverageError("W&B projects could not be listed.")
    selected = next((row for row in options if _root(row["external_id"]) == external_id), None)
    if selected is None:
        raise CoverageError("The selected W&B project is no longer available from this account.")
    return connection, selected


def _destination_project(client, ident, scope):
    row = client.get_project(_uuid(ident))
    if (str(row.get("id")) != _uuid(ident)
            or row.get("customer_id") != scope.customer_id
            or str(row.get("workspace_id")) != scope.workspace_id):
        raise CoverageError("The W&B destination is outside this import's workspace.")
    return row


def choose_automatic_destination(client, *, folder, wandb_source, project=None):
    """Approve one destination for files and W&B before automatic scanning.

    Only explicit project creation writes here. History admission belongs to
    the durable worker; Back/Skip never starts it or scans the folder.
    """
    from pathlib import Path
    from . import backfill
    from .backfill_coverage import Scope

    scope = Scope.resolve(client, project)
    _, selected = _selected_source(client, wandb_source)
    if selected.get("project_id"):
        bound = _destination_project(client, selected["project_id"], scope)
        if scope.project_id and bound["id"] != scope.project_id:
            raise CoverageError("This W&B source is already attached to another Probe project.")
        destinations = [bound]
    elif scope.project_id:
        destinations = [_destination_project(client, scope.project_id, scope)]
    else:
        page = client.list_projects(workspace_id=scope.workspace_id, limit=MAX_OPTIONS)
        rows = page if isinstance(page, list) else page.items
        destinations = [row for row in rows
                        if row.get("customer_id") == scope.customer_id
                        and str(row.get("workspace_id")) == scope.workspace_id]
    choices = [(f"{row.get('name') or row['slug']} · {row['id']}", row) for row in destinations]
    if not selected.get("project_id") and not scope.project_id:
        slug = backfill.slug_for(Path(folder))
        found = client.resolve_project(slug)
        if found is not None and (found.get("customer_id") != scope.customer_id
                                  or str(found.get("workspace_id")) != scope.workspace_id):
            suffix = hashlib.sha256(f"{scope.key}:{Path(folder).resolve()}".encode()).hexdigest()[:8]
            slug = f"{slug[:90]}-{suffix}"
            found = client.resolve_project(slug)
        if found is None:
            choices.append((f"Create project {Path(folder).name}", {"create": slug}))
        elif (found.get("customer_id") == scope.customer_id
                and str(found.get("workspace_id")) == scope.workspace_id
                and all(row["id"] != found["id"] for row in destinations)):
            choices.append((f"{found.get('name') or slug} · {found['id']}", found))
    if not choices:
        raise CoverageError("No project is available in this workspace. Create a Probe project, then retry.")
    destination = None
    while True:
        destination = _pick(
            "Choose a destination for files and W&B", choices,
            lines=[
                "Both this folder's files and the selected W&B history will go to one Probe project.",
                "Scanning and file import run in the background without another plan review.",
            ], default=destination,
        )
        if destination is None or destination is tui.BACK:
            return destination
        name = (f"Create project {Path(folder).name}" if "create" in destination
                else f"{destination.get('name') or destination['slug']} · {destination['id']}")
        answer = _review(
            "Start automatic import",
            [f"Folder: {folder}", f"W&B source: {wandb_source['external_id']}",
             f"Destination for files and W&B: {name}",
             "The agent will scan and import this folder automatically into this project.",
             "W&B history starts in the background using this approved destination. Live sync is unchanged."],
            [("Skip W&B history", "skip"), ("Import files and W&B history", "import")],
        )
        if answer is tui.BACK:
            continue
        if answer != "import":
            return None
        # A long review must not carry an old account/source into admission.
        _, selected = _selected_source(client, wandb_source)
        if "create" in destination:
            slug = destination["create"]
            found = client.resolve_project(slug)
            if found is None:
                try:
                    found = client.create_project(
                        slug,
                        Path(folder).name,
                        kind="general",
                        workspace_id=scope.workspace_id,
                        # A directory basename is a PATH COMPONENT, not a title
                        # somebody chose. Pinned rather than left to the
                        # environment so a backfill run from a bare terminal
                        # does not lock it: `authorship.py` calls this exact
                        # case a template, and a template is enhanceable.
                        authored_by=agent_session.AUTHORSHIP_AGENT,
                    )
                except errors.ConflictError:
                    found = client.resolve_project(slug)
                    if found is None:
                        raise
            if found.get("slug") != slug:
                raise CoverageError("The created project did not match the approved project name.")
            destination = _destination_project(client, found["id"], scope)
        else:
            destination = _destination_project(client, destination["id"], scope)
        approval = {
            **wandb_source, "schema": AUTOMATIC_APPROVAL_SCHEMA,
            "workspace_id": scope.workspace_id, "project_id": _uuid(destination["id"]),
            **({"experiment_id": _uuid(selected["experiment_id"])} if selected.get("experiment_id") else {}),
        }
        return validate_automatic_approval(client, approval)


def validate_automatic_approval(client, approval):
    """Revalidate the exact approved source and destination; never select one."""
    from .backfill_coverage import Scope

    required = {"schema", "backend", "customer_id", "user_id", "connection_id", "external_id",
                "workspace_id", "project_id"}
    if (not isinstance(approval, dict) or approval.get("schema") != AUTOMATIC_APPROVAL_SCHEMA
            or not required <= approval.keys() or set(approval) - required - {"experiment_id"}):
        raise CoverageError("The automatic import has no valid W&B destination approval.")
    _, source = _selected_source(client, {**approval, "schema": SOURCE_SCHEMA})
    project_id = _uuid(approval["project_id"])
    scope = Scope.resolve(client, f"id:{project_id}", workspace_id=approval["workspace_id"])
    if (scope.backend != approval["backend"] or scope.customer_id != approval["customer_id"]
            or scope.project_id != project_id):
        raise CoverageError("The W&B destination belongs to another account or backend.")
    if source.get("project_id") and str(source["project_id"]) != project_id:
        raise CoverageError("This W&B source is already attached to another Probe project.")
    experiment = str(source["experiment_id"]) if source.get("experiment_id") else None
    if experiment and not source.get("project_id"):
        raise CoverageError("The attached W&B experiment has no verified parent project.")
    if experiment != approval.get("experiment_id"):
        raise CoverageError("The W&B experiment destination changed after review.")
    return copy.deepcopy(approval)


def admit_automatic_history(client, coverage, approval):
    """Replay only the destination approved before this automatic job started."""
    approval = validate_automatic_approval(client, approval)
    if (coverage.scope.project_id != approval["project_id"]
            or coverage.scope.workspace_id != approval["workspace_id"]):
        raise CoverageError("The automatic folder and W&B destinations do not match.")
    history = admit_reviewed_history(
        client, coverage, project_id=approval["project_id"], connection_id=approval["connection_id"],
        external_id=approval["external_id"], experiment_id=approval.get("experiment_id"),
    )
    state = history["receipt"]["state"]
    if state in {"failed", "canceled", "cancel_requested"}:
        raise CoverageError(
            f"W&B history {approval['external_id']} is {state}. Review this history on the dashboard. "
            "Its receipt and the file plan are saved; this request will not restart W&B history."
        )
    return history


def _offer(client, coverage, state, projects, *, back_to_selection=False, wandb_source=None):
    step = 0
    accounts = None
    connection = selected = destination = None
    choices = None
    if wandb_source is not None:
        connection, selected = _selected_source(client, wandb_source)
        previous = next((item for item in state["imports"] if item["external_id"] == selected["external_id"]), None)
        if previous is not None:
            if previous["connection_id"] != _uuid(connection["id"]):
                raise CoverageError("This W&B source already has a different saved account mapping.")
            return "reviewed"  # Reuse its existing reviewed destination and request key.
        step = 3
    if len(state["imports"]) >= MAX_IMPORTS:
        if wandb_source is not None:
            raise CoverageError("This folder already has the maximum number of W&B selections.")
        return
    while True:
        if step == 0:
            answer = _review(
                "Add W&B history",
                [
                    "Optionally add W&B history to a project from this folder.",
                    "Choose an existing account from Integrations, then review its exact project destination.",
                    "Live sync keeps its current setting; new attachments start paused. File delivery is separate.",
                ],
                [("Continue with files", "skip"), ("Choose W&B history", "wandb")],
            )
            if answer is tui.BACK and back_to_selection:
                return tui.BACK
            if answer != "wandb":
                return
            step = 1

        if step == 1:
            if accounts is None:
                accounts = eligible_connections(client)
            picked = _pick(
                "Choose a W&B account",
                [
                    (f"{row.get('label') or row.get('name') or 'W&B'} · {row['id']}", row)
                    for row in accounts[:MAX_ACCOUNTS]
                ],
                lines=[f"Showing the first {MAX_ACCOUNTS} eligible accounts. Manage credentials in Integrations."],
                default=connection,
            )
            if picked is tui.BACK:
                if not back_to_selection:
                    return
                step = 0
                continue
            if picked is None:
                if not accounts:
                    raise CoverageError(
                        "No eligible W&B account. Connect W&B in the dashboard's Integrations page, "
                        "then try linking again."
                    )
                return
            if picked != connection:
                choices = selected = None
            connection = picked
            step = 2

        if step == 2:
            if choices is None:
                options = client.list_mirror_scope_options(_uuid(connection["id"]))
                if not isinstance(options, list):
                    raise CoverageError("W&B projects could not be listed.")
                mapped = {item["external_id"] for item in state["imports"]}
                choices = []
                for row in options[:MAX_OPTIONS]:
                    external = _root(row["external_id"])
                    if external in mapped:
                        continue
                    bound = row.get("project_id")
                    experiment = row.get("experiment_id")
                    suffix = (f" (already attached to experiment {experiment} in project {bound})" if experiment else
                              f" (already attached to {bound})" if bound else "")
                    choices.append((external + suffix, row))
            picked = _pick(
                "Choose W&B history", choices,
                lines=[f"Select a source project. Showing the first {MAX_OPTIONS} W&B projects."],
                default=selected,
            )
            if picked is tui.BACK:
                if not back_to_selection:
                    return
                step = 1
                continue
            if picked is None:
                return
            selected = picked
            step = 3

        if step == 3:
            picked = _pick(
                "Choose a Probe destination",
                [(f"{slug} · {ident}", ident) for ident, slug in sorted(projects.items())],
                lines=["Choose one of this folder's reviewed Probe projects."],
                default=destination,
            )
            if picked is tui.BACK:
                if wandb_source is not None:
                    return tui.BACK
                if not back_to_selection:
                    return
                step = 2
                continue
            if picked is None:
                return tui.SKIP if wandb_source is not None else None
            destination = picked
            if selected.get("project_id") and str(selected["project_id"]) != destination:
                raise CoverageError(
                    "This W&B source is already attached to Probe project "
                    f"{selected['project_id']}; its history was not duplicated or moved."
                )
            external = _root(selected["external_id"])
            experiment_id = _uuid(selected["experiment_id"]) if selected.get("experiment_id") else None
            if experiment_id is not None and not selected.get("project_id"):
                raise CoverageError("The attached W&B experiment has no verified parent project.")
            step = 4

        answer = _review(
            "Review W&B history import",
            [
                f"W&B source: {external}",
                f"Probe destination: {projects[destination]} · {destination}",
                *([f"Reuse its existing experiment: {experiment_id}"] if experiment_id else []),
                "Existing source identities are reused. History runs on the server; metrics stay source-backed.",
                "This does not enable live sync or associate coding sessions.",
            ],
            [("Skip W&B history", "skip"), ("Import this W&B history", "import")],
        )
        if answer is tui.BACK and (back_to_selection or wandb_source is not None):
            step = 3
            continue
        if answer != "import":
            return tui.SKIP if wandb_source is not None else None
        record_reviewed_selection(
            coverage, project_id=destination, connection_id=_uuid(connection["id"]),
            external_id=external, experiment_id=experiment_id,
        )  # SQLite FULL commit precedes BOTH admission calls.
        return "reviewed"


def run(
    client, coverage, *, interactive=False, yes=False, offer=False, back_to_selection=False,
    wandb_source=None,
):
    """Return status lines, or BACK when the caller owns pre-delivery navigation.

    Back preserves approved history and returns before any further admissions.
    Provider failures remain optional; Ctrl+C stays a distinct interruption.
    """
    try:
        return _run(
            client, coverage, interactive=interactive, yes=yes, offer=offer,
            back_to_selection=back_to_selection, wandb_source=wandb_source,
        )
    except Exception as exc:
        return HistoryResult([_failure(exc)])


def _run(client, coverage, *, interactive, yes, offer, back_to_selection=False, wandb_source=None):
    lines = HistoryResult()
    source_reviewed = False
    projects = _projects(coverage)
    if not projects or (coverage.meta(KEY) is None and not (offer and interactive and not yes)):
        return lines
    try:
        state = _load(coverage, projects)
    except (CoverageError, KeyError, TypeError, ValueError) as exc:
        return [f"W&B history needs review ({type(exc).__name__}); saved state was retained."]
    admit = offer and interactive and not yes
    if admit:
        try:
            navigation = _offer(
                client, coverage, state, projects, back_to_selection=back_to_selection,
                wandb_source=wandb_source,
            )
            if navigation is tui.BACK:
                return tui.BACK
            lines.source_resolved = navigation is tui.SKIP
            source_reviewed = navigation == "reviewed"
        except Exception as exc:
            lines.append(_failure(exc))
        # Only a successfully committed selection can authorize admission. A
        # failed SQLite commit must not leave an in-memory selection sendable.
        state = _load(coverage, projects)
    for item in state["imports"]:
        try:
            _advance(client, coverage, state, item, admit=admit)
            receipt = item.get("receipt") or {}
            if admit and receipt.get("state") in {"failed", "canceled"}:
                answer = _review(
                    "Retry W&B history",
                    [
                        f"W&B history for {item['external_id']}: {receipt['state']}.",
                        "The previous job and its history are retained.",
                    ],
                    [("Leave this history as it is", "skip"), ("Retry this W&B history", "retry")],
                )
                if answer is tui.BACK and back_to_selection:
                    return tui.BACK
                if answer == "retry":
                    item.setdefault("previous_jobs", []).append(
                        {
                            "idempotency_key": item["idempotency_key"],
                            "receipt": receipt,
                        }
                    )
                    item.update(
                        retry_of=item["job_id"],
                        job_id=None,
                        receipt=None,
                        idempotency_key=str(uuid4()),
                        error=None,
                    )
                    _save(coverage, state)
                    _advance(client, coverage, state, item, admit=True)
        except Exception as exc:
            item["error"] = _failure(exc)
            _save(coverage, state)
        receipt = item.get("receipt") or {}
        status = receipt.get("state", "admission pending; rerun interactively to reconcile")
        destination = projects[item['project_id']]
        if item.get('experiment_id'):
            destination += f" / experiment {item['experiment_id']}"
        lines.append(f"W&B history {item['external_id']} → {destination}: {status}.")
        if status == "completed":
            lines.append("History discovery completed; metric reads use the connected W&B source.")
        if item.get("error"):
            lines.append(item["error"])
        if receipt.get("warnings"):
            lines.append(
                f"W&B reported {len(receipt['warnings'])} warning(s); inspect the history job."
            )
    if wandb_source is not None and source_reviewed:
        selected = next((item for item in state["imports"]
                         if item["external_id"] == wandb_source["external_id"]), None)
        lines.source_resolved = bool(selected and selected.get("job_id") and not selected.get("error"))
    return lines


def _failure(exc):
    detail = (
        f": {_text(exc, 400)}" if isinstance(exc, (CoverageError, errors.ConflictError)) else ""
    )
    return f"W&B history pending ({type(exc).__name__}){detail}. File delivery continues."
