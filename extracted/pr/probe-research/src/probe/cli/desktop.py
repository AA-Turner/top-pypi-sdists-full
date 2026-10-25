"""Bounded desktop JSON adapter over the existing import engine.

No credentials or raw import payloads cross this boundary. A review pins the
account, exact transcript prefixes and selected folder identities. Only its
opaque id can start the durable, detached jobs after explicit user approval.
"""
from __future__ import annotations

from dataclasses import asdict
import base64
import hashlib
import json
from pathlib import Path
import sys
import time
import uuid

import typer

from probe.sdk.durable import file_lock, write_text_atomic

app = typer.Typer(help="Desktop app's versioned JSON interface.")
MAX_INPUT = 1024 * 1024
PREVIEW_TTL = 30 * 60
HISTORY_PAGE_SIZE = 50
REPORT_LINES = 200
REPORT_LINE_CHARS = 2000
SOURCE_IDS = 32


def _closed_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("Desktop request contains a repeated field.")
        value[key] = item
    return value


def _client():
    from probe.sdk.client import Client
    from probe.sdk.config import current_context_name, resolve
    # Explicit settings prevent ambient credential refresh from adopting a new
    # login halfway through one response. Pin the context name at the same time.
    context = current_context_name()
    client = Client(settings=resolve(context=context), async_writes=False, fail_open=False,
                    auto_drain=False, attribution="backfill")
    client._desktop_context = context
    return client


def _identity(client):
    from .backfill_transcripts import _background_identity
    identity = _background_identity(client)
    identity["context"] = getattr(client, "_desktop_context", identity["context"])
    return identity


def _scope(identity):
    return {"userId": identity["user_id"], "customerId": identity["customer_id"]}


def _backend(value):
    from urllib.parse import urlsplit, urlunsplit
    parsed = urlsplit(value)
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(),
                       parsed.path.rstrip("/"), "", ""))


def _same_account(left, right):
    return ({**left, "base_url": _backend(left.get("base_url", ""))}
            == {**right, "base_url": _backend(right.get("base_url", ""))})


def _sources():
    from . import backfill_transcripts as t, capabilities
    census = t.discover(agents=t.IMPORTABLE, tracked=set(), plugin_dirs={
        source: capabilities.tap_plugin_dir(source) for source in t.IMPORTABLE
    })
    return census


def _source_row(t):
    return {"id": f"{t.agent}:{t.session_id}", "harness": t.agent,
            "title": Path(t.cwd).name if t.cwd else t.path.stem,
            "path": str(t.path), "mtime": t.mtime, "size": t.size}


def _preview_dir():
    from .import_jobs import default_dir
    path = default_dir().parent / "desktop-previews"
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    return path


def _preview_path(value):
    try:
        key = uuid.UUID(value).hex
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError("Invalid backfill review id.") from exc
    return _preview_dir() / f"{key}.json"


def _job_matches(job, identity):
    payload = job.get("payload") or {}
    account = payload.get("account")
    if account is not None:
        return _same_account(account, identity)
    scope = payload.get("scope") or {}
    return (scope.get("customer_id") == identity["customer_id"]
            and _backend(scope.get("backend", "")) == _backend(identity["base_url"])
            and payload.get("user_id") == identity["user_id"]
            and payload.get("context") == identity["context"])


def _job_sources(job):
    """Display the approved transcript producers, never a label or folder worker."""
    from probe.harness import get_registry
    if job.get("kind") != "transcripts":
        return []
    files = (job.get("payload") or {}).get("files")
    if not isinstance(files, list):
        return []
    sources = []
    for row in files:
        source = row.get("agent") if isinstance(row, dict) else None
        if (not isinstance(source, str) or not source or len(source) > 64
                or not all(c in "abcdefghijklmnopqrstuvwxyz0123456789_" for c in source)):
            continue
        harness = get_registry().find(source)  # an alias (`claude`) names its producer id
        source = harness.id if harness else source
        if source not in sources:
            sources.append(source)
        if len(sources) == SOURCE_IDS:
            break
    return sources


def _job_activity(job):
    """A bounded safe progress stream, including an older worker's current snapshot."""
    from ..sdk.redaction import scrub_string
    from . import import_jobs
    def display(value, limit):
        # Inspect credential/URL context before the display clip. Keep even a
        # malformed saved record bounded; encoded nesting fails closed.
        try:
            return import_jobs._clean(scrub_string(value[:8192]), limit)
        except (ValueError, RecursionError):
            return "Activity text omitted."
    raw = job.get("activity")
    raw = raw if isinstance(raw, list) else []
    events = []
    truncated = bool(job.get("activity_truncated")) or len(raw) > REPORT_LINES
    states = {state.value for state in import_jobs.State}
    for row in raw[-REPORT_LINES:]:
        if (not isinstance(row, dict) or not isinstance(row.get("state"), str)
                or row["state"] not in states):
            continue
        message, stamp = row.get("message"), row.get("at")
        if not isinstance(message, str) or not isinstance(stamp, str):
            continue
        if len(message) > REPORT_LINE_CHARS or len(stamp) > 100:
            truncated = True
        clean = display(message, REPORT_LINE_CHARS)
        events.append({"at": display(stamp, 100), "state": row["state"], "message": clean})
    current = (job.get("progress") or {}).get("message")
    if isinstance(current, str) and current:
        if len(current) > REPORT_LINE_CHARS:
            truncated = True
        message = display(current, REPORT_LINE_CHARS)
        latest = events[-1] if events else {}
        if latest.get("message") != message or latest.get("state") != job["state"]:
            events.append({"at": display(str(job["updated_at"]), 100), "state": job["state"], "message": message})
    if len(events) > REPORT_LINES:
        truncated = True
    lines = [f"{row['at']} {row['state']}: {row['message']}" for row in events[-REPORT_LINES:]]
    truncated = truncated or any(len(line) > REPORT_LINE_CHARS for line in lines)
    return ([line[:REPORT_LINE_CHARS] for line in lines], truncated)


def _public_job(job, *, identity=None, summary=False):
    from . import import_progress
    done, total = import_progress.counts(job)
    report = job.get("report", [])
    activity, activity_truncated = ([], False) if summary else _job_activity(job)
    return {"id": job["id"], "kind": job.get("kind"), "label": str(job["label"])[:512],
            "state": job["state"], "createdAt": str(job["created_at"])[:100],
            "updatedAt": str(job["updated_at"])[:100],
            "completed": done if import_progress.completion_known(job) else None,
            "total": total, "unit": "sessions" if job.get("kind") == "transcripts" else "files",
            "partial": import_progress.is_partial(job),
            "sources": _job_sources(job),
            "message": str((job.get("progress") or {}).get("message") or "")[:2000],
            "error": str(job["error"])[:2000] if job.get("error") else None,
            "report": [] if summary else [str(x)[:REPORT_LINE_CHARS] for x in report[-REPORT_LINES:]],
            "reportTruncated": not summary and (len(report) > REPORT_LINES or any(
                len(str(x)) > REPORT_LINE_CHARS for x in report[-REPORT_LINES:])),
            "activity": activity, "activityTruncated": activity_truncated,
            **({"scope": _scope(identity)} if identity is not None else {})}


def _history(identity, cursor=None):
    """Bound the IPC response, with a creation/id cursor pinned to this authority."""
    from . import import_jobs
    stamp = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    after = None
    if cursor is not None:
        try:
            if not cursor or len(cursor) > 256:
                raise ValueError()
            decoded = base64.b64decode(cursor + "=" * (-len(cursor) % 4), altchars=b"-_", validate=True)
            point = json.loads(decoded)
            if (not isinstance(point, list) or len(point) != 3
                    or not all(isinstance(x, str) for x in point) or point[2] != stamp):
                raise ValueError()
            after = tuple(point[:2])
        except (ValueError, TypeError, UnicodeError) as exc:
            raise ValueError("Backfill history changed or its cursor is invalid. Refresh the history.") from exc
    def key(job):
        return (job["created_at"], job["id"])
    owned = sorted((job for job in import_jobs.list_jobs() if _job_matches(job, identity)), key=key, reverse=True)
    active = [job for job in owned if job["state"] in (import_jobs.State.QUEUED, import_jobs.State.RUNNING)]
    remaining = [job for job in owned if after is None or key(job) < after]
    page = remaining[:HISTORY_PAGE_SIZE]
    more = len(remaining) > len(page)
    next_cursor = base64.urlsafe_b64encode(json.dumps([*key(page[-1]), stamp],
        separators=(",", ":")).encode()).decode().rstrip("=") if more else None
    return {"jobs": [_public_job(job, summary=True) for job in page], "total": len(owned),
            "activeJobs": [_public_job(job, summary=True) for job in active[:HISTORY_PAGE_SIZE]],
            "activeTotal": len(active), "hasMore": more, "nextCursor": next_cursor, "scope": _scope(identity)}


def _owned_job(value, identity):
    from . import import_jobs
    job = import_jobs.get_job(value)
    if not _job_matches(job, identity):
        raise ValueError("This backfill belongs to another account or destination. Switch back before opening it.")
    return job


def preview_backfill(request):
    from . import backfill_transcripts as t, capabilities
    from .backfill_coverage import Scope
    selected = request.get("sessionIds", [])
    folders = request.get("folders", [])
    if not selected and not folders:
        raise ValueError("Select at least one session or folder.")
    if len(selected) > 10000 or len(folders) > 30:
        raise ValueError("Review at most 10,000 sessions and 30 folders at once.")
    census = _sources() if selected else t.Census()
    available = {f"{row.agent}:{row.session_id}": row for row in census.candidates}
    if any(key not in available for key in selected):
        raise ValueError("A selected session changed or is no longer available. Refresh and review it again.")
    census.candidates = [available[key] for key in dict.fromkeys(selected)]
    folder_rows = []
    for raw in dict.fromkeys(folders):
        folder = Path(raw).expanduser().resolve(strict=True)
        if not folder.is_dir():
            raise ValueError("Select an existing research folder.")
        stat = folder.stat()
        folder_rows.append({"path": str(folder), "name": folder.name,
                            "identity": [stat.st_dev, stat.st_ino]})
    worker = request.get("agent")
    if folder_rows:
        from . import backfill
        # Only the file importer's agents (`backfill.IMPORTER_AGENTS`), installed.
        available_workers = [a.value for a in backfill.available_agents()]
        if worker is None:
            worker = next(iter(available_workers), None)
        if worker not in available_workers:
            raise ValueError("Folder backfills need Claude Code or Codex installed and signed in.")
    with _client() as client:
        identity = _identity(client)
        posters, devices = {}, {}
        for source in dict.fromkeys(row.agent for row in census.candidates):
            resolved = capabilities.resolved_capture_credential(source)
            if resolved is None:
                raise ValueError(f"Connect {source} session capture before importing its history.")
            posters[source] = t.Poster(base_url=resolved[1], token=resolved[0])
            devices[source] = capabilities.capture_device_id(source) or ""
        payload = t._background_payload(census, client=client, posters=posters,
            devices=devices, budget_bytes=None, unpaired=[]) if selected else None
        scope = asdict(Scope.resolve(client)) if folder_rows else None
    key = uuid.uuid4().hex
    public = {"id": key, "sessions": [_source_row(row) for row in census.candidates],
              "folders": [{k: row[k] for k in ("path", "name")} for row in folder_rows],
              "destination": {"customerId": identity["customer_id"], "userId": identity["user_id"],
                              "workspaceId": scope["workspace_id"] if scope else None},
              "warning": ("Start approves automatic scanning, organization, and upload of the selected folders in the background. "
                          "Large files are recorded as references. Session imports include only the reviewed transcript bytes."
                          if folders else "Only the reviewed transcript bytes will be imported; new session capture continues separately.")}
    saved = {"version": 1, "created": time.time(), "account": identity, "transcripts": payload,
             "folders": folder_rows, "scope": scope, "agent": worker, "public": public, "jobs": []}
    write_text_atomic(_preview_path(key), json.dumps(saved, allow_nan=False), mode=0o600)
    return public


def start_backfill(key):
    from . import import_jobs, backfill_import, backfill
    from .backfill_coverage import Scope
    path = _preview_path(key)
    with file_lock(path.with_suffix(".lock")):
        saved = json.loads(path.read_text())
        with _client() as client:
            if not _same_account(_identity(client), saved["account"]):
                raise ValueError("The account or destination changed. Review the selection again.")
            if saved.get("started"):
                return [_public_job(_owned_job(j, saved["account"]), identity=saved["account"], summary=True) for j in saved["jobs"]]
            if time.time() - saved["created"] > PREVIEW_TTL:
                raise ValueError("This backfill review expired. Review the selection again.")
            if saved["folders"] and asdict(Scope.resolve(client)) != saved["scope"]:
                raise ValueError("The destination workspace changed. Review the selection again.")
            for folder in saved["folders"]:
                info = Path(folder["path"]).stat()
                if not Path(folder["path"]).is_dir() or [info.st_dev, info.st_ino] != folder["identity"]:
                    raise ValueError("A selected folder was replaced. Review the selection again.")
            settings = client.settings
        def remember(job):
            if job["id"] not in saved["jobs"]:
                saved["jobs"].append(job["id"])
            write_text_atomic(path, json.dumps(saved, allow_nan=False), mode=0o600)
        if saved["transcripts"]:
            remember(import_jobs.enqueue("transcripts", saved["transcripts"],
                f"{len(saved['transcripts']['files'])} selected agent sessions"))
        from probe.sdk.client import Client
        def factory():
            return Client(settings=settings, async_writes=False, auto_drain=False, attribution="backfill")
        for index, folder in enumerate(saved["folders"]):
            remember(backfill_import.enqueue_auto_import(client_factory=factory,
                folder=folder["path"], agent=backfill.Agent(saved["agent"]), auto_approve=True,
                request_id=uuid.uuid5(uuid.UUID(key), str(index)).hex))
        saved["started"] = True
        write_text_atomic(path, json.dumps(saved, allow_nan=False), mode=0o600)
        return [_public_job(_owned_job(j, saved["account"]), identity=saved["account"], summary=True) for j in saved["jobs"]]


class ServiceState:
    """`snapshot_delivery`'s `serviceState`: the Probe service as the Overview
    found it, and so why its counts are there, partial or missing."""
    RUNNING = "running"
    #: Discovering: open sessions are still checking in, so counts may be low.
    STARTING = "starting"
    #: An update cycle is running.
    UPDATING = "updating"
    #: Nothing answers at its socket: none runs (or it is restarting).
    NOT_RUNNING = "not_running"
    #: It refused the call, or its socket's folder is not this user's alone.
    REFUSED = "refused"
    #: It did not answer in time, or answered something unreadable.
    UNREACHABLE = "unreachable"
    #: No service on this platform yet (Windows).
    UNSUPPORTED = "unsupported"


#: What a person reads when the counts are there, per state.
_COUNTED = {
    ServiceState.RUNNING: "Active counts come from the local live-session registry.",
    ServiceState.STARTING: "The Probe service is starting: open sessions are still checking in, so active counts may be low for a few seconds.",
    ServiceState.UPDATING: "Probe is installing an update; active counts come from the local live-session registry.",
}
#: ... and when they are not. `{detail}` is what failed.
_UNCOUNTED = {
    ServiceState.STARTING: "The Probe service is starting and has not listed live sessions yet. Try again in a few seconds.",
    ServiceState.UPDATING: "The Probe service is installing an update and could not list live sessions. Try again in a minute.",
    ServiceState.NOT_RUNNING: "The Probe service is not running, so live sessions cannot be counted. It starts with the next coding-agent session, or run `probe service start`.",
    ServiceState.REFUSED: "The Probe service refused to list live sessions ({detail}).",
    ServiceState.UNREACHABLE: "The Probe service could not list live sessions: {detail}.",
    ServiceState.UNSUPPORTED: "The Probe service does not run on this system yet, so live sessions cannot be counted.",
}
#: A socket folder someone else could have made: the client will not connect.
_FOREIGN_FOLDER = "Probe will not ask the service for live sessions: its folder is not private to this user."
_NO_RECEIPTS = "Delivery receipts are unavailable."
#: Last received and Pending come from each live session's journal (D29).
_RECEIPTS = ("Last received and Pending are the recorder's own, for the live sessions: when the server last "
             "took a transcript, and the lines it has not taken yet.")
#: Seconds for each of the two calls: the listing, then the service's state.
_LIST_TIMEOUT_S = 3
_STATE_TIMEOUT_S = 1


def _live_sessions():
    """(sessions or None, ServiceState, the reason's text or None for the
    state's own), fail-soft: the listing, then `service.status` for what the
    service is doing (an update, its discovery window) when it answers at all."""
    import os
    from probe import __version__
    from probe.service import client
    from probe.service.protocol import Method, State
    sessions, state, text = None, ServiceState.RUNNING, None
    try:
        listing = client.call(Method.SESSION_LIST, client="app", client_version=__version__, timeout=_LIST_TIMEOUT_S)
        sessions = listing["sessions"]
        if not isinstance(sessions, list):
            raise ValueError("Unreadable service registry")
    except (FileNotFoundError, ConnectionRefusedError):
        return None, ServiceState.NOT_RUNNING, None
    except PermissionError:
        return None, ServiceState.REFUSED, _FOREIGN_FOLDER
    except TimeoutError:
        # A service that did not answer the listing will not answer the next call either.
        return None, ServiceState.UNREACHABLE, _UNCOUNTED[ServiceState.UNREACHABLE].format(detail="it did not answer in time")
    except client.ServiceError as exc:
        sessions, state = None, ServiceState.REFUSED
        text = _UNCOUNTED[state].format(detail=exc.message or f"error {exc.code}")
    except OSError as exc:
        sessions, state = None, ServiceState.UNREACHABLE
        text = _UNCOUNTED[state].format(detail=f"the connection failed ({exc})" if str(exc) else "the connection failed")
    except (ValueError, KeyError, TypeError):
        sessions, state = None, ServiceState.UNREACHABLE
        text = _UNCOUNTED[state].format(detail="its answer could not be read")
    try:
        status = client.call(Method.STATUS, client="app", client_version=__version__, timeout=_STATE_TIMEOUT_S)
    except (OSError, client.ServiceError, ValueError, KeyError, TypeError):
        status = None
    if isinstance(status, dict):
        update = status.get("update")
        if isinstance(update, dict) and update.get("in_progress") is True:
            state, text = ServiceState.UPDATING, None
        elif status.get("state") == State.DISCOVERING:
            state, text = ServiceState.STARTING, None
    return sessions, state, text


def _received(sessions, identity=None):
    """`{agent: (last received as ISO 8601 UTC, lines waiting)}` over the
    sessions the service lists (plan D29), from each one's transcript journal:
    the receipts `session.list` carries (`probe.service.receipts`), or, from a
    service that predates them, read here the same way. Only the receipts of
    the account answered for (`identity`): each names its journal's `scope`,
    and one of another account (or of none named) is left out. Never
    `<capture dir>/state.db`: its outbox stopped moving when capture moved to
    the journal (#1415), so its numbers were weeks old. Empty when nothing is
    known."""
    import os
    import time
    from probe.service import receipts
    rows = [s for s in sessions or [] if isinstance(s, dict)]
    if not rows:
        return {}
    if not any("receipts" in s for s in rows):
        try:
            found = receipts.read([s.get("sid") for s in rows], receipts.journal_roots([dict(os.environ)]), {})
        except Exception:  # noqa: BLE001 -- the Overview shows unknown, never fails
            found = {}
        rows = [{**s, "receipts": found.get(s.get("sid"))} for s in rows]
    if identity is not None:
        mine = {"backend": receipts.backend_of(identity.get("base_url")), "customer": identity.get("customer_id")}
        rows = [s if isinstance(s.get("receipts"), dict) and s["receipts"].get("scope") == mine
                else {**s, "receipts": None} for s in rows]
    out = {}
    for row in receipts.by_harness(rows, scoped=False):
        at = row.get("received_at")
        try:
            last = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(at)) if at is not None else None
        except (TypeError, ValueError, OverflowError, OSError):
            last = None
        out[row["harness"]] = (last, row.get("pending_lines"))
    return out


def snapshot_delivery(identity=None):
    from probe.harness import get_registry
    rows = get_registry().captured()
    sessions, state, text = _live_sessions()
    received = _received(sessions, identity)
    agents = []
    for row in rows:
        last, pending = received.get(row.id, (None, None))
        agents.append({"source": row.id,
                       "activeAgents": (sum(1 for session in sessions
                           if session.get("harness") == row.id and session.get("alive") is True)
                           if sessions is not None else None),
                       "lastReceived": last, "pending": pending})
    reason = (_COUNTED.get(state, _COUNTED[ServiceState.RUNNING]) if sessions is not None
              else text or _UNCOUNTED[state])
    receipts = any(a["lastReceived"] is not None or a["pending"] is not None for a in agents)
    return {"available": sessions is not None, "agents": agents,
            **({"scope": _scope(identity)} if identity is not None else {}),
            "captureControlSupported": False,
            "serviceState": state,
            "reason": f"{reason} {_RECEIPTS if receipts else _NO_RECEIPTS}"}


def analytics_policy():
    """Only a boolean crosses native IPC; configuration remains CLI-owned."""
    from probe.sdk import config, _telemetry_core as core
    try:
        if core.telemetry_disabled():
            return {"enabled": False, "resolved": True}
        data = config.load_file(strict=True)
        contexts = data.get("contexts", {})
        active = contexts.get(config.current_context_name(data), {})
        if not isinstance(active, dict):
            return {"enabled": False, "resolved": False}
        return {"enabled": core.hosted_base_url(core.effective_base_url(active)), "resolved": True}
    except Exception:
        return {"enabled": False, "resolved": False}


def complete_onboarding(request):
    from probe.sdk.transport import deadline_scope
    expected = {key: request.get(key) for key in ("userId", "customerId")}
    if not all(expected.values()):
        raise ValueError("The signed-in account is required to finish onboarding.")
    # One bounded operation: identity lookup and final acknowledgement share
    # the same pinned credential. Never queue this completion in the outbox.
    with deadline_scope(time.monotonic() + 12), _client() as client:
        if expected != _scope(_identity(client)):
            raise ValueError("The account or destination changed. Sign in and finish setup again.")
        result = client.complete_desktop_onboarding()
        if not isinstance(result, dict) or result.get("complete") is not True or result.get("scope") != expected:
            raise ValueError("The server did not acknowledge onboarding for this account.")
        return {"complete": True, "scope": expected}


FIELDS = {
    "jobs": {"cursor": str}, "job": {"id": str}, "discover_sessions": {},
    "preview_backfill": {"sessionIds": list, "folders": list, "agent": str},
    "start_backfill": {"previewId": str}, "resume_job": {"id": str}, "cancel_job": {"id": str},
    "delivery": {}, "profile": {}, "analytics_policy": {}, "set_capture": {"source": str, "enabled": bool},
    "onboarding_complete": {"userId": str, "customerId": str},
    "workspaces": {},
}


def workspaces(client):
    """The Settings → Workspace picker: every workspace on the team, fetched WITHOUT
    this computer's workspace limit (so the menu always lists them all), and the
    limit itself (`probe status --json`'s `account.workspace_limit`)."""
    from . import workspace_limit_cmd

    rows = workspace_limit_cmd.list_workspaces(client)
    limit = workspace_limit_cmd.effective()
    return {
        "workspaces": [
            {"id": str(row["id"]), "name": row.get("name"), "slug": row.get("slug"), "kind": row.get("kind")}
            for row in rows
            if isinstance(row, dict) and row.get("id")
        ],
        "workspace_limit": None if limit is None else limit.as_json(),
    }


def _dispatch(request):
    if not isinstance(request, dict) or request.get("op") not in FIELDS:
        raise ValueError("Unknown desktop operation.")
    op = request["op"]
    fields = FIELDS[op]
    if set(request) - {"op", *fields}:
        raise ValueError("Unknown desktop request field.")
    for name, kind in fields.items():
        if name in request and type(request[name]) is not kind:
            raise ValueError(f"{name} has the wrong JSON type.")
    if op == "preview_backfill":
        for name in ("sessionIds", "folders"):
            if not all(isinstance(v, str) and len(v) <= 4096 for v in request.get(name, [])):
                raise ValueError(f"{name} must contain strings.")
        return preview_backfill(request)
    if op == "start_backfill":
        return start_backfill(request["previewId"])
    if op == "discover_sessions":
        census = _sources()
        if len(census.candidates) > 10000:
            raise ValueError("More than 10,000 saved sessions were found; use the terminal backfill picker for this history.")
        return [_source_row(row) for row in census.candidates]
    if op == "set_capture":
        raise ValueError("Per-agent capture control is not supported by this CLI. Its current capture-off operation affects every local agent, so no setting was changed.")
    if op == "analytics_policy":
        return analytics_policy()
    if op == "onboarding_complete":
        return complete_onboarding(request)
    with _client() as client:
        if op == "profile":
            # The account the app's shell opens with (team, role, members): no
            # workspace content, so it is read WITHOUT this computer's workspace
            # limit. A limit naming a since-deleted workspace makes the API refuse
            # every limited request (422 `workspace_limit_unknown`), and the shell
            # that holds Settings, where that limit is fixed, must still open.
            from probe.sdk import workspace_limit as _workspace_limit

            with _workspace_limit.without_limit():
                return client.transport.get("/v1/desktop/profile")
        if op == "workspaces":
            return workspaces(client)
        identity = _identity(client)
        if op == "delivery":
            return snapshot_delivery(identity)
        from . import import_jobs
        if op == "jobs":
            return _history(identity, request.get("cursor"))
        job = _owned_job(request["id"], identity)
        if op == "resume_job":
            job = import_jobs.resume(job["id"])
        elif op == "cancel_job":
            job = import_jobs.cancel(job["id"])
        return _public_job(job, identity=identity)


#: The ops that take the setup lock (`dispatch`): admission and job lifecycle.
LOCKED = frozenset({"start_backfill", "resume_job", "cancel_job", "onboarding_complete"})


def dispatch(request):
    # Admission and lifecycle changes must not race logout/uninstall/update.
    if isinstance(request, dict) and request.get("op") in LOCKED:
        from . import wizard_lock
        with wizard_lock.held():
            # Existing import_job events retain their names and their approving
            # session. A pipe never becomes interactive: provenance is separate.
            try:
                from . import telemetry
                from probe.sdk import _telemetry_core as core
                telemetry.TelemetryContext.start(via=telemetry.Via.COMMAND, interactive=False,
                    base_url=core.effective_base_url(core.read_cli_config()))
            except Exception:
                pass  # observability never becomes a prerequisite for the import
            return _dispatch(request)
    return _dispatch(request)


def respond(raw: bytes) -> tuple[str, int]:
    """One closed JSON request (its bytes, at most MAX_INPUT) -> (its v1
    envelope as one JSON line, the exit status). What `probe desktop request
    --json` prints and exits with, and what the Probe service's
    `desktop.request` answers (`python -m probe.core.run desktop`): one code
    path, so the two transports cannot answer differently."""
    try:
        if len(raw) > MAX_INPUT:
            raise ValueError("Desktop request exceeds 1 MiB.")
        value = dispatch(json.loads(raw.decode("utf-8"), object_pairs_hook=_closed_object))
        return json.dumps({"v": 1, "ok": True, "data": value}, allow_nan=False), 0
    except Exception as exc:
        from probe.sdk.redaction import scrub_string
        from . import wizard_lock
        return (json.dumps({"v": 1, "ok": False, "error": scrub_string(str(exc))[:1500]}),
                wizard_lock.BUSY_EXIT_CODE if isinstance(exc, wizard_lock.Busy) else 1)


@app.command("request")
def request_command(json_output: bool = typer.Option(False, "--json")):
    """Read one closed JSON request on stdin; return one v1 JSON envelope."""
    if not json_output:
        raise typer.BadParameter("The desktop interface requires --json.")
    text, code = respond(sys.stdin.buffer.read(MAX_INPUT + 1))
    typer.echo(text)
    if code:
        raise typer.Exit(code)
