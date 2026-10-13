"""The status line names the project the daemon last WROTE to.

Before: the segment named the last project of `GET /v1/sessions/{id}/work`,
whose order ties for every project of one session (each link row carries the
session's first sighting) and falls to uuid order -- so it showed a project the
daemon had stopped writing to, and never moved. Now every daemon write that ran
and names a project or experiment stores that project's slug beside the marker
(`session_marker.write_scope`), and `session_marker.read` puts it in place of
the server's guess.
"""

from __future__ import annotations

import asyncio
import importlib
import json
import time

import httpx
import pytest

from probe.daemon import approvals as appr, lease, precheck, probe_api, scope, tools
from probe.daemon.store import Store
from probe.sdk import session_marker
from probe.sdk.write_outcome import QUEUED_PREFIX

SID = "11111111-2222-3333-4444-555555555555"
PROJECT = "0b9e6c1a-1d1e-4c39-9d0f-6d1b7f0a2c11"
EXPERIMENT = "5f3c2b1a-7e6d-4c5b-8a9f-0e1d2c3b4a59"


@pytest.fixture(autouse=True)
def _state(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.setattr(probe_api, "_features", None)


def _deps(tmp_path, *, token: str | None = "pk-test", marker: bool = True) -> tools.Deps:
    """A live writer for a session whose status line keeps a marker (the server's
    guess: the literature project)."""
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    deps = tools.Deps(store=Store(tmp_path / "s.sqlite", clock=time.time), board=appr.Board(tmp_path / "appr"),
                      session_id=SID, cwd=work, workdirs=[work], home=tmp_path, write_dirs=[],
                      probe_env={"PROBE_TOKEN": token} if token else {}, bypass=False, mode_known=True, bite_id=1)
    lease.sessions_dir().mkdir(parents=True, exist_ok=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")
    assert lease.renew(SID)
    if marker:
        session_marker.write(SID, {"project": "willow-posttraining-literature", "run_ids": ["r1"]})
    return deps


def _cli(monkeypatch, code: int = 0, stderr: str = "") -> list[list[str]]:
    """Stands in for the real CLI: every command exits `code`."""
    ran: list[list[str]] = []

    async def run(deps, argv, op_id, **kw):
        ran.append(list(argv))
        return tools.ProbeResult(code, "{}", stderr)

    monkeypatch.setattr(tools, "run_probe_process", run)
    return ran


def _probe(monkeypatch, *, delay: float = 0.0, status: int | None = None) -> list[str]:
    """Probe's scope and project reads: `willow` is a project, `lit-review` an
    experiment filed under it."""
    seen: list[str] = []
    willow = {"id": PROJECT, "kind": "project", "project_id": PROJECT, "experiment_id": None, "run_id": None}
    lit = {"id": EXPERIMENT, "kind": "experiment", "project_id": PROJECT, "experiment_id": EXPERIMENT,
           "run_id": None}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.append(f"{request.method} {request.url.path}" + (f"?{request.url.query.decode()}"
                                                             if request.url.query else ""))
        if delay:
            await asyncio.sleep(delay)
        if status is not None:
            return httpx.Response(status, json={"detail": "invalid token"})
        path, slug = request.url.path, request.url.params.get("slug")
        if path == "/v1/scopes" and slug == "willow":
            return httpx.Response(200, json=willow)
        if path == "/v1/scopes" and slug == "lit-review" or path == f"/v1/scopes/{EXPERIMENT}":
            return httpx.Response(200, json=lit)
        if path == f"/v1/scopes/{PROJECT}":
            return httpx.Response(200, json=willow)
        if path == f"/v1/projects/{PROJECT}":
            return httpx.Response(200, json={"id": PROJECT, "slug": "willow"})
        return httpx.Response(404, json={"detail": "Not Found"})

    async def client(env):
        return httpx.AsyncClient(base_url="http://probe.test", transport=httpx.MockTransport(handler))

    monkeypatch.setattr(probe_api, "_client", client)
    return seen


def _run(coro):
    return asyncio.run(coro)


# ---------------------------------------------------------------------------
# Which writes name a project
# ---------------------------------------------------------------------------


def test_every_daemon_write_is_classified_once():
    """A new daemon command must say whether it moves the label."""
    daemon = {path for path, owner in precheck.OWNERS.items() if owner == precheck.DAEMON}
    both = set(scope.SCOPE_PARAMS) & scope.NO_SCOPE
    assert not both, f"in both tables: {sorted(both)}"
    missing = daemon - set(scope.SCOPE_PARAMS) - scope.NO_SCOPE
    assert not missing, f"classify in daemon/scope.py: {sorted(missing)}"
    stale = (set(scope.SCOPE_PARAMS) | scope.NO_SCOPE) - set(precheck.OWNERS)
    assert not stale, f"no longer commands: {sorted(stale)}"


def test_every_scope_param_is_one_the_cli_binds():
    """A renamed CLI param would silently stop moving the label."""
    named = {path: names for path, names in scope.SCOPE_PARAMS.items() if not callable(names)}
    named["artifact add"] = ("project", "experiment", "from_manifest")
    named["artifact move"] = ("to", "target")
    named["project tag"] = ("project", "add", "remove", "replace")
    named["experiment tag"] = ("experiment_id", "add", "remove", "replace")
    named["sync"] = ("directory", "list_only", "project", "experiment")
    for path, names in named.items():
        bound = {p.name for p in precheck.command(path).params}
        assert set(names) <= bound, f"{path}: {sorted(set(names) - bound)} not in {sorted(bound)}"


@pytest.mark.parametrize("argv, ref", [
    (["run", "move", "r1", "--to", "willow"], "willow"),
    (["run", "move", "r1", "--to", "willow "], "willow "),
    (["experiment", "create", "lit-review", "--project", "willow"], "willow"),
    (["experiment", "create", "lit-review"], "lit-review"),
    (["experiment", "set", f"id:{EXPERIMENT}", "--name", "Lit"], f"id:{EXPERIMENT}"),
    (["notes", "create", "n.md", "--experiment", "lit-review"], "lit-review"),
    (["project", "create", "willow", "--kind", "training"], "willow"),
    (["artifact", "add", "--project", "willow", "f.txt"], "willow"),
    (["artifact", "add", "--project", "willow", "--from-manifest", "m.jsonl"], None),
    (["artifact", "move", "a1", "--to", "project", "--target", "willow"], "willow"),
    (["artifact", "move", "a1", "--to", "run", "--target", "brave-otter"], None),
    (["artifact", "move", "a1", "--to", "project"], None),
    (["notes", "create", "n.md", "--run", "r1"], None),
    (["run", "tag", "r1", "best"], None),
    (["project", "delete", "willow"], None),
])
def test_the_ref_a_write_names(argv, ref):
    assert scope.scope_ref(precheck.parse(argv)) == ref


# ---------------------------------------------------------------------------
# The daemon stamps what it wrote
# ---------------------------------------------------------------------------


def test_a_write_to_a_project_names_it_on_the_status_line(tmp_path, monkeypatch):
    """The reported case: the marker's server guess says the literature project,
    the daemon writes to `willow`, and the segment says `willow`."""
    deps = _deps(tmp_path)
    _cli(monkeypatch)
    seen = _probe(monkeypatch)

    _run(tools.run_probe_command(deps, ["run", "move", "r1", "--to", "willow"]))

    assert session_marker.read_scope(SID) == "willow"
    state = session_marker.read(SID)
    assert state["project"] == "willow" and state["run_ids"] == ["r1"]
    segment = session_marker.render(state, configured=True, tracking=True, color=False)
    assert "willow" in segment and "literature" not in segment
    assert seen == ["GET /v1/scopes?slug=willow"], "a project slug needs one read"


@pytest.mark.parametrize("ref", [f"id:{EXPERIMENT}", EXPERIMENT, "slug:lit-review"])
def test_a_write_to_an_experiment_names_its_project(tmp_path, monkeypatch, ref):
    deps = _deps(tmp_path)
    _cli(monkeypatch)
    seen = _probe(monkeypatch)

    _run(tools.run_probe_command(deps, ["experiment", "set", ref, "--name", "Lit"]))

    assert session_marker.read_scope(SID) == "willow"
    assert seen[-1] == f"GET /v1/projects/{PROJECT}"


def test_the_latest_write_wins(tmp_path, monkeypatch):
    deps = _deps(tmp_path)
    _cli(monkeypatch)
    _probe(monkeypatch)
    session_marker.write_scope(SID, "willow-posttraining-literature")

    _run(tools.run_probe_command(deps, ["notes", "create", "n.md", "--project", "willow"]))

    assert session_marker.read_scope(SID) == "willow"


def test_a_bypass_override_names_its_project(tmp_path, monkeypatch):
    """The other door: a blocked write the bypass mode runs at once."""
    deps = _deps(tmp_path)
    deps.bypass = True
    _cli(monkeypatch)
    _probe(monkeypatch)
    deps.blocks["b1"] = precheck.Block(id="b1", why="looks like a secret", check="secret",
                                       argv=["run", "move", "r1", "--to", "willow"], cwd=str(deps.cwd))

    _run(tools.run_probe_command(deps, ["daemon", "override", "b1", "--why", "fine"]))

    assert session_marker.read_scope(SID) == "willow"


@pytest.mark.parametrize("why", ["failed", "queued", "no project", "no key", "no marker", "unknown ref",
                                 "name ref", "unreachable"])
def test_the_label_stays_when_nothing_landed_or_nothing_says_where(tmp_path, monkeypatch, why):
    deps = _deps(tmp_path, token=None if why == "no key" else "pk-test", marker=why != "no marker")
    _cli(monkeypatch, code=1 if why == "failed" else 0,
         stderr=QUEUED_PREFIX + " run move\n" if why == "queued" else "")
    seen = _probe(monkeypatch)
    if why == "unreachable":
        async def down(env):
            def refuse(request):
                raise httpx.ConnectError("down")
            return httpx.AsyncClient(base_url="http://probe.test", transport=httpx.MockTransport(refuse))
        monkeypatch.setattr(probe_api, "_client", down)
    session_marker.write_scope(SID, "before")
    argv = {"no project": ["run", "tag", "r1", "best"],
            "unknown ref": ["run", "move", "r1", "--to", "nowhere"],
            "name ref": ["run", "move", "r1", "--to", "name:Willow"]}.get(why, ["run", "move", "r1", "--to", "willow"])

    _run(tools.run_probe_command(deps, argv))

    assert session_marker.read_scope(SID) == "before"
    if why != "unknown ref" and why != "unreachable":
        assert seen == [], "no lookup when nothing can move the label"


def test_a_refused_key_during_the_lookup_stops_the_writer(tmp_path, monkeypatch):
    deps = _deps(tmp_path)
    _cli(monkeypatch)
    _probe(monkeypatch, status=401)
    session_marker.write_scope(SID, "before")

    _run(tools.run_probe_command(deps, ["run", "move", "r1", "--to", "willow"]))

    assert session_marker.read_scope(SID) == "before"
    assert deps.key_refused is True


def test_a_slow_probe_holds_the_write_no_longer_than_the_lookup_budget(tmp_path, monkeypatch):
    """One bound over the whole lookup, not per request or per read."""
    deps = _deps(tmp_path)
    _cli(monkeypatch)
    _probe(monkeypatch, delay=2.0)
    monkeypatch.setattr(probe_api, "SCOPE_TIMEOUT_S", 0.2)
    session_marker.write_scope(SID, "before")

    started = time.monotonic()
    out = _run(tools.run_probe_command(deps, ["run", "move", "r1", "--to", "willow"]))

    assert time.monotonic() - started < 1.5
    assert out.startswith("[exit 0]")
    assert session_marker.read_scope(SID) == "before"


def test_the_bench_never_stamps(tmp_path, monkeypatch):
    deps = _deps(tmp_path)
    seen = _probe(monkeypatch)

    class Replay:
        async def run(self, argv, op_id):
            return 0, "{}"

    deps.replay = Replay()
    _run(tools.run_probe_command(deps, ["run", "move", "r1", "--to", "willow"]))

    assert session_marker.read_scope(SID) is None and seen == []


def test_a_bite_cut_short_during_the_lookup_still_logs_the_write_as_landed(tmp_path, monkeypatch):
    """The lookup runs AFTER the logbook line: a cancel there must not turn a
    landed write into "cancelled - it may have written part of its work"."""
    deps = _deps(tmp_path)
    _cli(monkeypatch)

    async def cut_short(env, ref):
        raise asyncio.CancelledError

    monkeypatch.setattr(probe_api, "project_slug", cut_short)

    with pytest.raises(asyncio.CancelledError):
        _run(tools.run_probe_command(deps, ["run", "move", "r1", "--to", "willow"]))

    statuses = [row["status"] for row in deps.store.recent_writes()]
    assert statuses and "cancelled" not in statuses, statuses


# ---------------------------------------------------------------------------
# A deleted project leaves the label
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("ref, cleared", [("willow", True), (f"id:{PROJECT}", True), ("slug:willow", True),
                                         (f"id:{PROJECT.upper()}", True), ("name:Willow", False),
                                         ("elsewhere", False)])
def test_deleting_the_labelled_project_clears_it(tmp_path, monkeypatch, ref, cleared):
    deps = _deps(tmp_path)
    deps.bypass = True  # the delete's own question is not what this tests
    _cli(monkeypatch)
    session_marker.write_scope(SID, "willow", PROJECT)
    monkeypatch.setattr(tools, "_server_has_trash", lambda deps: asyncio.sleep(0, True))

    async def own(deps, parsed):
        return {"id": PROJECT, "others": {}}

    monkeypatch.setattr(tools, "deletion_facts", own)
    _run(tools.run_probe_command(deps, ["project", "delete", ref]))

    assert (session_marker.read_scope(SID) is None) is cleared
    assert session_marker.read(SID)["project"] == ("willow-posttraining-literature" if cleared else "willow")


def test_a_yes_to_a_held_delete_clears_it(tmp_path, monkeypatch):
    """The worker's door for a delete the researcher approved later: no await
    there, but the deleted project still leaves the label."""
    from types import SimpleNamespace

    from probe.daemon import worker as worker_mod

    deps = _deps(tmp_path)
    _cli(monkeypatch)
    session_marker.write_scope(SID, "willow", PROJECT)
    req = SimpleNamespace(id="q1", held={"kind": "probe", "argv": ["project", "delete", "willow"], "op_id": "op1",
                                         "cwd": str(deps.cwd)})
    me = SimpleNamespace(store=deps.store, session=SimpleNamespace(cwd=deps.cwd))

    out, stopped = _run(worker_mod.Worker._run_held(me, req, deps))

    assert out.startswith("exit 0") and stopped is None
    assert session_marker.read_scope(SID) is None


def test_the_bench_never_clears_a_real_label(tmp_path):
    deps = _deps(tmp_path)
    deps.replay = object()
    session_marker.write_scope(SID, "willow", PROJECT)

    scope.forget(deps, precheck.parse(["project", "delete", "willow"]))

    assert session_marker.read_scope(SID) == "willow"


# ---------------------------------------------------------------------------
# The scope file
# ---------------------------------------------------------------------------


def test_an_unassigned_code_point_is_still_printed(monkeypatch):
    """The hook's python can be older than the daemon's: a character the daemon
    knows is unassigned there, and must not drop the label."""
    monkeypatch.setattr(session_marker.unicodedata, "category", lambda ch: "Cn")
    assert session_marker.write_scope(SID, "melt") is True
    assert session_marker.read_scope(SID) == "melt"


def test_no_scope_leaves_the_marker_as_it_was():
    session_marker.write(SID, {"project": "from-server", "run_ids": []})
    assert session_marker.read(SID)["project"] == "from-server"


def test_a_scope_without_a_marker_is_not_shown():
    """Nothing installed refreshes a marker for this session, so nothing shows it."""
    session_marker.write_scope(SID, "willow")
    assert session_marker.read(SID) is None


@pytest.mark.parametrize("good", ["willow", "my project", "x" * 300, "über-run"])
def test_a_printable_slug_is_stored(good):
    assert session_marker.write_scope(SID, good) is True
    assert session_marker.read_scope(SID) == good


@pytest.mark.parametrize("bad", ["", "a\nb", "a\x1b[31mb", "a\x9bb", "a‮b", "a b", "a​b",
                                 "x" * (session_marker.MAX_LABEL_CHARS + 1), None, 7])
def test_a_slug_the_segment_cannot_print_is_never_stored(bad):
    assert session_marker.write_scope(SID, bad) is False
    assert session_marker.read_scope(SID) is None


def test_the_servers_project_is_checked_too():
    session_marker.write(SID, {"project": "evil\x1b]0;x\x07", "run_ids": []})
    assert session_marker.read(SID)["project"] is None
    segment = session_marker.render(session_marker.read(SID), configured=True, tracking=True, color=False)
    assert "\x1b" not in segment


@pytest.mark.parametrize("updated_at", ["NaN", "1e400", str(10 ** 400), "true", "0"])
def test_a_tampered_or_expired_scope_is_ignored_and_never_raises(updated_at):
    session_marker.write(SID, {"project": "from-server", "run_ids": []})
    session_marker.write_scope(SID, "willow")
    path = session_marker.scope_path(SID)
    path.write_text('{"project": "willow", "updated_at": %s}' % updated_at)
    assert session_marker.read_scope(SID) is None
    assert session_marker.read(SID)["project"] == "from-server"
    path.write_text(json.dumps({"project": "a\x1b]0;x\x07", "updated_at": time.time()}))
    assert session_marker.read_scope(SID) is None


# ---------------------------------------------------------------------------
# The agent's own writes (inline mode, --directed), from the `probe` CLI
# ---------------------------------------------------------------------------


class FakeClient:
    """The CLI's client, for the label lookup only."""

    def __init__(self, seen: list[str], delay: float = 0.0) -> None:
        self.seen, self.delay = seen, delay

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return None

    def get_scope_by_slug(self, slug):
        self.seen.append(f"scope?slug={slug}")
        time.sleep(self.delay)
        if slug == "willow":
            return {"id": PROJECT, "kind": "project", "project_id": PROJECT}
        if slug == "lit-review":
            return {"id": EXPERIMENT, "kind": "experiment", "project_id": PROJECT}
        raise LookupError(slug)

    def get_scope(self, scope_id):
        self.seen.append(f"scope/{scope_id}")
        return {"id": scope_id, "kind": "experiment", "project_id": PROJECT}

    def get_project(self, project_id):
        self.seen.append(f"project/{project_id}")
        return {"id": project_id, "slug": "willow"}


def _cli_session(monkeypatch, state: str = "full", *, queued: bool = False, delay: float = 0.0,
                 code: int = 0, marker: bool = True) -> tuple[list[list[str]], list[str]]:
    """`probe.cli.main.main` in a coding agent's shell, the command itself stubbed."""
    cli_main = importlib.import_module("probe.cli.main")

    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    monkeypatch.delenv("PROBE_DAEMON_SESSION", raising=False)
    lease.sessions_dir().mkdir(parents=True, exist_ok=True)
    session_marker.set_session_state(SID, state)
    if state == session_marker.STATE_DAEMON:
        assert lease.renew(SID)
    if marker:
        session_marker.write(SID, {"project": "willow-posttraining-literature", "run_ids": []})
    ran: list[list[str]] = []
    seen: list[str] = []
    monkeypatch.setattr(cli_main, "_UNDELIVERED", cli_main._Undelivered())
    precheck._root()  # the real command tree, built before `app` is stubbed below

    def app(*, args, prog_name, standalone_mode):
        ran.append(list(args))
        if queued:
            cli_main._UNDELIVERED.add({"queued": True, "method": "POST", "path": "/v1/x", "error": "timeout"})
        return code

    monkeypatch.setattr(cli_main, "app", app)
    monkeypatch.setattr(cli_main, "_client", lambda **kw: FakeClient(seen, delay))
    return ran, seen


def test_an_inline_write_names_its_project(monkeypatch):
    cli_main = importlib.import_module("probe.cli.main")

    ran, seen = _cli_session(monkeypatch, state="full")
    assert cli_main.agent_session.session_id_from_env() == SID

    assert cli_main.main(["notes", "create", "n.md", "--project", "willow"]) == 0

    assert ran and session_marker.read(SID)["project"] == "willow"
    assert seen == ["scope?slug=willow"]


def test_a_directed_write_under_the_daemon_names_its_project(monkeypatch):
    """The researcher asked the agent itself to write, in daemon mode."""
    cli_main = importlib.import_module("probe.cli.main")

    ran, seen = _cli_session(monkeypatch, state=session_marker.STATE_DAEMON)
    session_marker.write_scope(SID, "daemons-last")

    assert cli_main.main(["--directed", "experiment", "set", "slug:lit-review", "--name", "Lit"]) == 0

    assert ran == [["experiment", "set", "slug:lit-review", "--name", "Lit"]]
    assert session_marker.read_scope(SID) == "willow"


def test_an_agent_launch_names_its_project(monkeypatch):
    cli_main = importlib.import_module("probe.cli.main")

    _cli_session(monkeypatch, state="full")

    assert cli_main.main(["run", "start", "--project", "willow", "--name", "sft"]) == 0

    assert session_marker.read_scope(SID) == "willow"


def test_exec_names_its_project_when_the_run_opens_not_when_the_job_ends(monkeypatch):
    """The job may run for hours, or fail: the run is open in that project either way."""
    cli_main = importlib.import_module("probe.cli.main")

    _cli_session(monkeypatch, state="full")
    session_marker.write_scope(SID, "before")
    assert cli_main.main(["exec", "--project", "willow", "--", "python", "train.py"]) == 0
    assert session_marker.read_scope(SID) == "before", "not after the job: exec labels itself when its run opens"

    cli_main._label_status_line_soon("willow")
    deadline = time.monotonic() + 5
    while session_marker.read_scope(SID) != "willow" and time.monotonic() < deadline:
        time.sleep(0.02)
    assert session_marker.read_scope(SID) == "willow"


def test_a_childs_help_flag_does_not_stop_the_label(monkeypatch):
    cli_main = importlib.import_module("probe.cli.main")

    _cli_session(monkeypatch, state="full")

    assert cli_main.main(["notes", "create", "n.md", "--project", "willow", "--", "-h"]) == 0

    assert session_marker.read_scope(SID) == "willow"


def test_ctrl_c_during_the_lookup_keeps_the_commands_exit(monkeypatch):
    cli_main = importlib.import_module("probe.cli.main")

    _cli_session(monkeypatch, state="full")

    def interrupted(*a, **k):
        raise KeyboardInterrupt

    monkeypatch.setattr(scope, "stamp_from_cli", interrupted)

    assert cli_main.main(["notes", "create", "n.md", "--project", "willow"]) == 0


@pytest.mark.parametrize("why", ["control", "refused", "failed", "queued", "help", "no marker", "a read",
                                 "the daemon's own", "no project", "a tag listing", "a sync listing",
                                 "a sync scan"])
def test_the_cli_leaves_the_label_when_nothing_landed_or_nothing_says_where(monkeypatch, why):
    cli_main = importlib.import_module("probe.cli.main")

    _ran, seen = _cli_session(monkeypatch, state=session_marker.STATE_DAEMON if why == "refused" else "full",
                              queued=why == "queued", code=1 if why == "failed" else 0, marker=why != "no marker")
    session_marker.write_scope(SID, "before")
    if why == "the daemon's own":
        monkeypatch.setenv("PROBE_DAEMON_SESSION", SID)
    argv = {"help": ["notes", "create", "--project", "willow", "--help"],
            "a read": ["project", "get", "willow"],
            "no project": ["notes", "create", "n.md", "--run", "r1"],
            "a tag listing": ["project", "tag", "willow"],
            "a sync listing": ["sync", "runs/", "--list", "--project", "willow"],
            "a sync scan": ["sync", "--project", "willow"]}.get(
        why, ["notes", "create", "n.md", "--project", "willow"])

    cli_main.main(argv)

    if why == "control":  # the same setup, with nothing in the way, does move it
        assert session_marker.read_scope(SID) == "willow"
        return
    assert session_marker.read_scope(SID) == "before"
    assert seen == []


@pytest.mark.parametrize("argv", [["project", "tag", "willow", "best"], ["project", "tag", "willow", "--remove", "x"],
                                  ["sync", "runs/", "--project", "willow"]])
def test_a_tag_change_or_a_folder_sync_names_its_project(monkeypatch, argv):
    cli_main = importlib.import_module("probe.cli.main")

    _cli_session(monkeypatch, state="full")

    assert cli_main.main(argv) == 0

    assert session_marker.read_scope(SID) == "willow"


def test_the_cli_lookup_is_bounded(monkeypatch):
    cli_main = importlib.import_module("probe.cli.main")
    from probe.daemon import probe_api

    _cli_session(monkeypatch, state="full", delay=2.0)
    monkeypatch.setattr(probe_api, "SCOPE_TIMEOUT_S", 0.2)
    session_marker.write_scope(SID, "before")

    started = time.monotonic()
    assert cli_main.main(["notes", "create", "n.md", "--project", "willow"]) == 0

    assert time.monotonic() - started < 1.5
    assert session_marker.read_scope(SID) == "before"


def test_the_agent_deleting_the_labelled_project_clears_it(monkeypatch):
    cli_main = importlib.import_module("probe.cli.main")

    _cli_session(monkeypatch, state="full")
    session_marker.write_scope(SID, "willow", PROJECT)

    assert cli_main.main(["project", "delete", "willow"]) == 0

    assert session_marker.read_scope(SID) is None
