"""The project the daemon is writing to, for the researcher's status line.

The status line used to name the project from `GET /v1/sessions/{id}/work`: the
last of the projects the session touched. That list ties for every project of
one session (each link row carries the SESSION's first sighting), so the tie
falls to uuid order and the label never moves -- it named a project the daemon
had stopped writing to. The daemon knows better at the moment it writes. Once a
write has RAN (exit 0, not queued) and its logbook line is in, `stamp` reads the
project or experiment the command names from the CLI's own parse, resolves it to
its project's slug and stores it beside the marker
(`session_marker.write_scope`); `session_marker.read` shows it in place of the
server's guess. Two doors call it: `tools._probe_command` (`stamp`) and the
bypass auto-approve `tools._run_approved` (`stamp_argv`). A researcher's later
yes to a held command (`Worker._run_held`) only `forget`s a deleted project:
an await there would sit between the logbook and the request's outcome, so an
override the researcher approves moves the label at the daemon's next write.

Plain code, no model in the loop: the label says where writes LANDED, never what
the model thinks the session is about. Writes the daemon does not make -- the
agent's own in inline mode, its `--directed` ones, any session the daemon does
not record -- go through the `probe` CLI, which stamps them the same way from
its `main` (`stamp_from_cli`), through its own client.
"""

from __future__ import annotations

import asyncio
import logging
import threading
from typing import Any, Callable

from probe.daemon import precheck

log = logging.getLogger(__name__)


def _artifact_move(parsed: precheck.Parsed) -> str | None:
    """`artifact move A --to project|experiment --target REF` names where it goes;
    a run target is a petname, and no target promotes up the artifact's own chain."""
    if parsed.params.get("to") not in ("project", "experiment"):
        return None
    return _param(parsed, "target")


def _tagging(param: str) -> Callable[[precheck.Parsed], str | None]:
    """`project|experiment tag X` with nothing to add, remove or set lists the tags."""
    def ref(parsed: precheck.Parsed) -> str | None:
        if not any(precheck._strings(parsed.params.get(k)) for k in ("add", "remove", "replace")):
            return None
        return _param(parsed, param)
    return ref


def _sync(parsed: precheck.Parsed) -> str | None:
    """`sync DIR --project P` files a run folder; `--list`, or no folder (a scan that
    changes nothing), sends nothing."""
    if parsed.params.get("list_only") or not _param(parsed, "directory"):
        return None
    return _param(parsed, "project") or _param(parsed, "experiment")


def _artifact_add(parsed: precheck.Parsed) -> str | None:
    """An anchor flag names the container -- unless a manifest is given, whose rows
    may each name another and are only queued when the command returns."""
    if parsed.params.get("from_manifest"):
        return None
    return _param(parsed, "project") or _param(parsed, "experiment")


#: Per write that names a project or experiment: the params (as the CLI's
#: parser binds them) to read it from, first non-empty wins, or a function of the
#: parse. An experiment ref resolves to the experiment's project.
SCOPE_PARAMS: dict[str, tuple[str, ...] | Callable[[precheck.Parsed], str | None]] = {
    "project create": ("slug",),
    "project set": ("project_id",),
    "project patch": ("project_id",),
    "project tag": _tagging("project"),
    "project move": ("project_id",),
    "project reference add": ("project_id",),
    "project code attach": ("project_id",),
    "project code confirm": ("project_id",),
    "paper add": ("project_id",),
    # `--project` defaults to the active one; the new experiment's own slug
    # places it either way.
    "experiment create": ("project", "slug"),
    "experiment set": ("experiment_id",),
    "experiment tag": _tagging("experiment_id"),
    "experiment freeze": ("experiment_id",),
    "experiment move": ("to",),
    "experiment fork": ("source",),
    "group create": ("experiment_id",),
    "version create": ("experiment_id",),
    "run move": ("to",),
    # The agent's own (never the daemon's): a run started into a project, a run
    # folder synced into one. `exec` stamps when its run opens, not here: its
    # job may run for hours (`probe.cli.main._label_status_line_soon`).
    "run start": ("project", "experiment"),
    "sync": _sync,
    "artifact add": _artifact_add,
    "artifact move": _artifact_move,
    # Without either flag a note is on a run, group or artifact, or on the active
    # project -- which the daemon does not read: the label stays.
    "notes create": ("project", "experiment"),
    "notes push": ("project", "experiment"),
    "notes append": ("project", "experiment"),
    "notes edit": ("project", "experiment"),
    "notes rename": ("project", "experiment"),
}

#: Daemon writes that leave the label where it is: they name a run, an artifact,
#: a note, a paper or a view by id (no project without another read), they
#: delete, or they write nothing to a project at all. A `project delete` of the
#: stored project clears it instead (`stamp`). Every daemon-owned command is in
#: exactly one of the two tables (tests/test_daemon_scope.py).
NO_SCOPE: frozenset[str] = frozenset({
    *precheck.DELETES,
    "daemon override", "notes checkout", "notes sync",
    "run set", "run tag", "run end",
    "artifact set", "artifact version-add",
    "group set", "edge add", "paper update", "paper tag",
    "views create", "views rename", "views update",
})


def _param(parsed: precheck.Parsed, name: str) -> str | None:
    # Exactly as given: server slugs are free-form, and a trimmed `willow ` is
    # another project's slug.
    return next((v for v in precheck._strings(parsed.params.get(name)) if v.strip()), None)


def scope_ref(parsed: precheck.Parsed) -> str | None:
    """The project or experiment ref a write names, or None."""
    source = SCOPE_PARAMS.get(parsed.path, ())
    if callable(source):
        return source(parsed)
    for name in source:
        value = _param(parsed, name)
        if value:
            return value
    return None


def _live_writer(deps: Any) -> bool:
    """Not the bench's recorded Probe, the audit or the reader."""
    return deps.replay is None and not deps.audit and not deps.reader


def _stamps(deps: Any) -> bool:
    """Only the live writer stamps, not a process with no key (a test's bare
    `Deps`), and only for a session whose status line keeps a marker
    (`statusline_refresh` writes it only where a status line or the notice is
    installed): nobody else reads the label."""
    from probe.sdk import session_marker

    return (_live_writer(deps) and bool(deps.probe_env.get("PROBE_TOKEN"))
            and session_marker.marker_path(deps.session_id).is_file())


def forget(deps: Any, parsed: precheck.Parsed) -> None:
    """After a `project delete` RAN: clear the label when it names the deleted
    project. Synchronous (a file), so it fits the doors that may not await."""
    if not _live_writer(deps):
        return
    _clear_deleted(deps.session_id, parsed)


def _clear_deleted(session_id: str, parsed: precheck.Parsed) -> None:
    from probe.daemon import probe_api
    from probe.sdk import session_marker

    if parsed.path != "project delete":
        return
    target = precheck.delete_target(parsed)
    target = probe_api.selector(target) if target else None
    if target:
        session_marker.clear_scope(session_id, target)


def forget_argv(deps: Any, argv: list[str]) -> None:
    """`forget` from a command's words: the worker's door for a held delete the
    researcher said yes to."""
    try:
        forget(deps, precheck.parse(argv))
    except precheck.ParseError:
        return


async def stamp(deps: Any, parsed: precheck.Parsed) -> None:
    """After a write RAN and was logged: store its project for the status line.
    Never raises but a cancellation, and never anything but a label -- a lookup
    that fails or outlasts `SCOPE_TIMEOUT_S` leaves the last one."""
    from probe.daemon import probe_api
    from probe.sdk import session_marker

    if parsed.path == "project delete":
        forget(deps, parsed)
        return
    ref = scope_ref(parsed)
    if ref is None or not _stamps(deps):
        return
    try:
        place = await asyncio.wait_for(probe_api.project_slug(deps.probe_env, ref), probe_api.SCOPE_TIMEOUT_S)
    except probe_api.KeyRefused:
        from probe.daemon import tools

        tools._mark_key_refused(deps)
        return
    except Exception as exc:  # noqa: BLE001 -- a label; the write already landed
        log.info("status-line project lookup for %r failed: %s", ref, type(exc).__name__)
        return
    if place is not None:
        session_marker.write_scope(deps.session_id, *place)


async def stamp_argv(deps: Any, argv: list[str]) -> None:
    """`stamp` for a command that ran (not queued), from its words (the words
    after `probe`)."""
    if not argv:
        return
    try:
        parsed = precheck.parse(argv)
    except precheck.ParseError:
        return
    await stamp(deps, parsed)


# ---------------------------------------------------------------------------
# The agent's own writes, from the `probe` CLI
# ---------------------------------------------------------------------------

#: Command paths worth parsing for: the label's writes and the delete that clears it.
_CANDIDATES = frozenset(SCOPE_PARAMS) | {"project delete"}


def _candidate(args: list[str]) -> bool:
    """Could `args` name a project? A word-level look before the CLI's own parse
    (~85 ms the first time), so a read pays nothing."""
    # A window, not a prefix: a root option's value (`--base-url URL`) comes first.
    words = [a for a in args if not a.startswith("-")][:5]
    return any(" ".join(words[i:i + n]) in _CANDIDATES for i in range(len(words)) for n in (1, 2, 3))


def place_with_client(client: Any, ref: str) -> tuple[str, str] | None:
    """`probe_api.project_slug` through the CLI's own client, so the lookup asks
    the server, context and credential the write just used. None on any failure."""
    from probe.daemon import probe_api

    ref = probe_api.selector(ref)
    if ref is None:
        return None
    try:
        place = client.get_scope(ref) if probe_api._UUID.fullmatch(ref) else client.get_scope_by_slug(ref)
        project = place.get("project_id") if isinstance(place, dict) else None
        if not isinstance(project, str) or not probe_api._UUID.fullmatch(project):
            return None
        if place.get("kind") == "project" and not probe_api._UUID.fullmatch(ref):
            return ref, project
        data = client.get_project(project)
    except Exception:  # noqa: BLE001 -- a label; the write already landed
        return None
    slug = data.get("slug") if isinstance(data, dict) else None
    return (slug, project) if isinstance(slug, str) and slug else None


def _cli_session(session_id: str | None) -> bool:
    from probe.sdk import session_marker

    return (bool(session_id) and session_marker.valid_session_id(session_id)
            and session_marker.marker_path(session_id).is_file())


def stamp_from_cli(args: list[str], session_id: str | None, client_factory: Callable[[], Any]) -> None:
    """After a CLI command that exited 0 with nothing queued: the agent's write
    (inline mode, `--directed`, a session the daemon does not record) names its
    project on the status line, as the daemon's writes do. Only for a session
    whose status line keeps a marker. Never raises."""
    if not _cli_session(session_id):
        return
    # Before `--` only: what follows is a child's command line (`--help` there is its own).
    head = args[:args.index("--")] if "--" in args else args
    if any(a in ("--help", "-h") for a in head) or not _candidate(head):
        return
    try:
        parsed = precheck.parse(args)
    except precheck.ParseError:
        return
    if parsed.path == "project delete":
        _clear_deleted(session_id, parsed)
        return
    ref = scope_ref(parsed)
    if ref is not None:
        stamp_ref_from_cli(session_id, ref, client_factory)


def stamp_ref_from_cli(session_id: str | None, ref: str, client_factory: Callable[[], Any]) -> None:
    """Resolve `ref` through the CLI's client and store its project: at most
    `SCOPE_TIMEOUT_S`, the lookup left behind past it. Never raises."""
    from probe.daemon import probe_api
    from probe.sdk import session_marker

    if not _cli_session(session_id):
        return
    found: list[tuple[str, str] | None] = []

    def look() -> None:
        with client_factory() as client:
            found.append(place_with_client(client, ref))

    worker = threading.Thread(target=look, name="probe-status-line-label", daemon=True)
    worker.start()
    worker.join(probe_api.SCOPE_TIMEOUT_S)
    if found and found[0] is not None:
        session_marker.write_scope(session_id, *found[0])
