"""The realistic daemon bench (evals/companion/bench.py) -- its own logic, no model.

Pins what a bench number depends on and what keeps a bench run from touching
the researcher's machine: the sandbox guard, the jail, the fake Probe's route
mapping (the real CLI and the real MCP against it, 501 for what it does not
serve), files revealed by mtime, and the scorer's final-state, lineage-direction
and penalty rules.
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parents[1]
EVALS = AGENT / "evals" / "companion"
SRC = AGENT / "src"


def _load(name: str):
    if str(EVALS) not in sys.path:
        sys.path.insert(0, str(EVALS))
    spec = importlib.util.spec_from_file_location(name, EVALS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


fp = _load("fake_probe")
sb = _load("sandbox")
wd = _load("workdir")
score = _load("score")
bench = _load("bench")

PROJECT = "11111111-1111-4111-8111-111111111111"
SVM = "22222222-2222-4222-8222-222222222222"
PCA_EXP = "33333333-3333-4333-8333-333333333333"
CHOSEN = "44444444-4444-4444-8444-444444444444"
PCA_RUN = "55555555-5555-4555-8555-555555555555"
FILE_ID = "66666666-6666-4666-8666-666666666666"
OLD_RUN = "77777777-7777-4777-8777-777777777777"
T0 = fp.parse_ts("2026-09-23T08:00:00Z")


def _reads() -> dict:
    return {
        f"/v1/projects/{PROJECT}": {"id": PROJECT, "slug": "digits", "name": "Digits", "kind": "training",
                                    "description": None, "parent_project_id": None, "tags": [], "notes": None,
                                    "notes_version": 0, "created_at": "2026-09-23T08:01:00Z"},
        f"/v1/projects/{SVM}": {"id": SVM, "slug": "svm-vs-logreg", "name": "SVM vs logistic regression",
                                "kind": "experiment", "description": "Does an SVM beat logistic regression?",
                                "parent_project_id": PROJECT, "tags": [], "notes": None, "notes_version": 0,
                                "created_at": "2026-09-23T08:01:01Z"},
        f"/v1/runs/{CHOSEN}": {"id": CHOSEN, "slug": "fortunate-quail-346", "name": "svm C=10", "status": "completed",
                               "project_id": PROJECT, "experiment_id": SVM, "tags": ["sweep"], "notes": None,
                               "notes_version": 0, "created_at": "2026-09-23T08:02:00Z",
                               "ended_at": "2026-09-23T08:03:00Z"},
        f"/v1/runs/{CHOSEN}/artifacts": [
            {"id": FILE_ID, "run_id": CHOSEN, "kind": "file", "name": "results/table.md", "notes": None,
             "notes_version": 0, "created_at": "2026-09-23T08:02:30Z"},
            {"id": "c0de0000-0000-4000-8000-000000000000", "run_id": CHOSEN, "kind": "code", "name": "run.py",
             "notes": None, "created_at": "2026-09-23T08:02:01Z"}],
        f"/v1/runs/{CHOSEN}/edges": [],
        f"/v1/runs/{PCA_RUN}": {"id": PCA_RUN, "slug": "masterful-wildebeest-029", "name": "pca", "status": "completed",
                                "project_id": PROJECT, "experiment_id": SVM, "tags": [], "notes": None,
                                "notes_version": 0, "created_at": "2026-09-23T08:05:00Z",
                                "ended_at": "2026-09-23T08:05:30Z"},
    }


def _fake(now: float, **kw) -> "fp.FakeProbe":
    return fp.FakeProbe(_reads(), clock=fp.ManualClock(now), token="bench-fake-t", **kw)


def _call(fake, method, path, body=None, *, query="", token="bench-fake-t", key=None):
    headers = {"authorization": f"Bearer {token}"}
    if key:
        headers["idempotency-key"] = key
    raw = json.dumps(body).encode() if body is not None else b""
    return fake.handle(method, path, query, raw, headers)


# ---------------------------------------------------------------------------
# The sandbox guard.
# ---------------------------------------------------------------------------


def _layout(tmp_path: Path) -> "sb.Layout":
    layout = sb.Layout(tmp_path / "run", tmp_path / "recorded-home", jail=False, nonce=uuid.uuid4().hex)
    layout.make()
    return layout


def test_the_guard_accepts_its_own_sandbox_and_refuses_everything_else(tmp_path):
    layout = _layout(tmp_path)
    real = tmp_path / "real-home"
    env = sb.worker_env(layout, base_url="http://127.0.0.1:5555", token="bench-fake-x")
    layout.check(env, real_home=real)  # its own sandbox: fine

    def refused(**change) -> str:
        bad = {**env, **change}
        for key, value in change.items():
            if value is None:
                bad.pop(key)
        with pytest.raises(sb.SandboxError) as err:
            layout.check(bad, real_home=real)
        return str(err.value)

    assert "real home" in refused(HOME=str(real), XDG_CONFIG_HOME=str(real / ".config"),
                                  XDG_STATE_HOME=str(real / ".local/state"),
                                  PROBE_CONFIG_PATH=str(real / ".config/probe/config.toml"))
    assert "outside the sandbox HOME" in refused(XDG_STATE_HOME=str(tmp_path / "elsewhere"))
    assert "outside the sandbox HOME" in refused(PROBE_CONFIG_PATH=str(real / ".config/probe/config.toml"))
    assert "unset" in refused(PROBE_CONFIG_PATH=None)
    assert "loopback" in refused(PROBE_BASE_URL="https://api.research.prbe.ai")
    assert "loopback" in refused(PROBE_MCP_URL="https://mcp.research.prbe.ai/mcp")
    assert "fake token" in refused(PROBE_DAEMON_KEY="ros_pat_real_looking")
    assert "fake token" in refused(PROBE_TOKEN="ros_pat_real_looking")
    assert "must not reach" in refused(ANTHROPIC_API_KEY="sk-ant-x")
    # A sandbox HOME without THIS run's marker (a jail whose mount did not happen
    # leaves HOME at a directory that has none).
    (layout.home / sb.MARKER).write_text("another-run\n")
    with pytest.raises(sb.SandboxError, match="marker"):
        layout.check(env, real_home=real)


def test_the_guard_shim_never_execs_the_worker_outside_the_sandbox(tmp_path):
    layout = _layout(tmp_path)
    env = sb.worker_env(layout, base_url="http://127.0.0.1:5555", token="bench-fake-x")
    shim = [sys.executable, str(EVALS / "sandbox.py"), "--guard", layout.nonce, "--", "/bin/echo", "worker ran"]
    ok = subprocess.run(shim, env=env, capture_output=True, text=True, timeout=60)
    assert ok.returncode == 0 and "worker ran" in ok.stdout
    bad = subprocess.run(shim, env={**env, "HOME": str(tmp_path / "real-home")}, capture_output=True, text=True,
                         timeout=60)
    assert bad.returncode == 97 and "worker ran" not in bad.stdout and "refusing" in bad.stderr


@pytest.mark.skipif(not sb.jail_available(), reason="no unprivileged user + mount namespace here")
def test_inside_the_jail_the_recorded_home_is_the_sandbox_and_tmp_is_empty(tmp_path, request):
    if not (Path(sys.prefix) / "pyvenv.cfg").exists():
        pytest.skip("needs to run from a venv")
    if not os.access("/dev/shm", os.W_OK):
        pytest.skip("needs /dev/shm for a stand-in home outside the /tmp the jail masks")
    import tempfile

    recorded = Path(tempfile.mkdtemp(prefix="probe-bench-home-", dir="/dev/shm"))
    request.addfinalizer(lambda: __import__("shutil").rmtree(recorded, ignore_errors=True))
    (recorded / "keep").mkdir(parents=True)
    (recorded / "keep" / "secret.txt").write_text("the real home's file")
    layout = sb.Layout(tmp_path / "run", recorded, jail=True, nonce=uuid.uuid4().hex)
    layout.make()
    py = sb.Python.find(Path(sys.prefix), SRC)
    python = sb.build_overlay_venv(py, layout.outside(layout.venv_seen), seen=layout.venv_seen)
    env = sb.worker_env(layout, base_url="http://127.0.0.1:5555", token="bench-fake-x")
    probe = ("import os, json; h = os.environ['HOME']; open(os.path.join(h, 'written'), 'w').write('x');"
             "print(json.dumps({'home': h, 'marker': open(os.path.join(h, '.probe-bench-sandbox')).read().strip(),"
             "'tmp': os.listdir('/tmp'), 'real_file': os.path.exists(os.path.join(h, 'keep', 'secret.txt'))}))")
    argv = sb.launch_argv(layout, py, python, cwd_seen=recorded, inner=[str(python), "-c", probe])
    out = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr
    seen = json.loads(out.stdout.strip().splitlines()[-1])
    assert seen == {"home": str(recorded), "marker": layout.nonce, "tmp": [], "real_file": False}
    # The write landed in the sandbox, not in the directory the jail covered.
    assert (layout.home / "written").exists() and not (recorded / "written").exists()


# ---------------------------------------------------------------------------
# The fake Probe.
# ---------------------------------------------------------------------------


def test_rows_appear_when_the_clock_passes_them_and_runs_end_on_time():
    fake = _fake(fp.parse_ts("2026-09-23T08:02:30Z"))
    assert _call(fake, "GET", "/v1/runs/fortunate-quail-346").body["status"] == "running"
    assert _call(fake, "GET", f"/v1/runs/{PCA_RUN}").status == 404  # not created yet
    assert [r["id"] for r in _call(fake, "GET", "/v1/runs", query=f"project_id={PROJECT}").body] == [CHOSEN]
    fake.clock.now = fp.parse_ts("2026-09-23T08:06:00Z")
    assert _call(fake, "GET", f"/v1/runs/{CHOSEN}").body["status"] == "completed"
    assert {r["id"] for r in _call(fake, "GET", "/v1/runs", query=f"project_id={PROJECT}").body} == {CHOSEN, PCA_RUN}
    # The unfiltered project list hides experiments, like the server's.
    assert [p["id"] for p in _call(fake, "GET", "/v1/projects").body] == [PROJECT]
    assert [p["id"] for p in _call(fake, "GET", "/v1/projects", query="slug=svm-vs-logreg").body] == [SVM]


def test_notes_follow_the_servers_version_rules():
    fake = _fake(T0 + 3600)
    first = _call(fake, "PATCH", f"/v1/projects/{SVM}", {"notes": "v1 text", "base_version": 0})
    assert first.status == 200 and first.body["notes_version"] == 1
    stale = _call(fake, "PATCH", f"/v1/projects/{SVM}", {"notes": "lost", "base_version": 0})
    assert stale.status == 409 and stale.body["detail"]["notes_version"] == 1
    # No base_version is a force today ("enforced when supplied, not yet required").
    assert _call(fake, "PATCH", f"/v1/runs/{CHOSEN}", {"notes": "caveat"}).body["notes_version"] == 1
    assert _call(fake, "PATCH", f"/v1/runs/{CHOSEN}", {"notes": "x" * 4001}).status == 422  # a run's cap
    made = _call(fake, "POST", f"/v1/projects/{SVM}/sub-notes", {"title": "Verdict", "body": ""})
    _call(fake, "POST", f"/v1/projects/{SVM}/sub-notes", {"title": "Verdict", "body": ""})
    ambiguous = _call(fake, "PATCH", f"/v1/projects/{SVM}/sub-notes", {"note_title": "Verdict", "body": "b",
                                                                     "force": True})
    assert made.status == 201 and ambiguous.status == 409 and ambiguous.body["detail"]["match_count"] == 2
    state = fake.final_state()
    assert state["entities"][SVM]["notes"] == "v1 text" and state["entities"][CHOSEN]["notes"] == "caveat"


def test_a_fork_is_served_like_the_servers():
    """`experiment fork` (app/experiments/fork.py): a new experiment of the
    source's project, its notes opening with the source line, linked
    `forked_from` by the server -- and the link the wire refuses by hand."""
    fake = _fake(T0 + 3600)
    base = f"/v1/projects/{PROJECT}/experiments/{SVM}"
    assert _call(fake, "PATCH", base, {"notes": "C=10 wins.", "base_version": 0}).status == 200
    forked = _call(fake, "POST", f"{base}/fork", {"slug": "svm-rbf", "question": "Does an RBF kernel help?"})
    assert forked.status == 201, forked.body
    fid = forked.body["id"]
    assert forked.body["fork"]["source_id"] == SVM and forked.body["project_id"] == PROJECT
    notes = _call(fake, "GET", f"/v1/projects/{PROJECT}/experiments/{fid}").body["notes"]
    assert notes.startswith("Forked from experiment `") and notes.endswith("C=10 wins.")
    links = [e for e in fake.live_edges() if e["relation"] == "forked_from"]
    assert [(e["source_id"], e["target_id"]) for e in links] == [(fid, SVM)]
    inherited = _call(fake, "GET", f"/v1/projects/{PROJECT}/experiments/{fid}/inherited", query="kind=runs").body
    assert [x["id"] for x in inherited["sources"]] == [SVM]
    assert {r["id"] for r in inherited["items"]} == {CHOSEN, PCA_RUN}
    by_hand = _call(fake, "POST", "/v1/edges", {"source_type": "project", "source_id": fid,
                                                "relation": "forked_from", "target_type": "project",
                                                "target_id": SVM})
    assert by_hand.status == 422
    assert not fake.unmapped


def test_an_experiments_children_are_served_on_the_experiment_api():
    """What the tap's companion worker reads and writes for an experiment
    (X21b): its place, its detail and notes, its sub-notes, its files and an
    upload -- never through `/v1/projects/{E}`."""
    fake = _fake(T0 + 3600)
    base = f"/v1/projects/{PROJECT}/experiments/{SVM}"
    scope = _call(fake, "GET", f"/v1/scopes/{SVM}").body
    assert (scope["kind"], scope["project_id"]) == ("experiment", PROJECT)
    assert _call(fake, "PATCH", base, {"notes": "v1", "base_version": 0}).body["notes_version"] == 1
    assert _call(fake, "PATCH", base, {"notes": "v2", "base_version": 0, "op_key": "k"}).status == 422  # closed
    assert _call(fake, "POST", f"{base}/sub-notes", {"title": "companion: verdict", "body": "b"}).status == 201
    listed = _call(fake, "GET", f"{base}/sub-notes").body
    assert [s["title"] for s in listed["sub_notes"]] == ["companion: verdict"]
    upload = _call(fake, "POST", f"{base}/artifacts/uploads", {"name": "table.md", "content_hash": "a" * 64,
                                                               "size_bytes": 3, "content_type": "text/markdown"})
    assert upload.status == 201
    assert upload.body["artifact_id"] in {a["id"] for a in _call(fake, "GET", f"{base}/artifacts").body}
    # Addressed under another project: not found, as the server answers.
    assert _call(fake, "GET", f"/v1/projects/{SVM}/experiments/{SVM}/sub-notes").status == 404
    assert not fake.unmapped


def test_unmapped_routes_answer_501_and_are_listed_never_404():
    fake = _fake(T0 + 3600)
    answer = _call(fake, "GET", f"/v1/runs/{CHOSEN}/lineage")
    assert answer.status == 501 and "not served" in answer.body["detail"]
    assert _call(fake, "POST", "/v1/sql", {"sql": "select 1"}).status == 501
    assert [(u["method"], u["path"]) for u in fake.unmapped] == [("GET", f"/v1/runs/{CHOSEN}/lineage"),
                                                                 ("POST", "/v1/sql")]
    assert _call(fake, "GET", f"/v1/runs/{CHOSEN}", token="the-real-key").status == 401


def test_a_reused_idempotency_key_replays_or_refuses_like_the_server():
    fake = _fake(T0 + 3600)
    edge = {"source_type": "run", "source_id": PCA_RUN, "relation": "derived_from", "target_type": "run",
            "target_id": CHOSEN}
    first = _call(fake, "POST", "/v1/edges", edge, key="k1")
    again = _call(fake, "POST", "/v1/edges", edge, key="k1")
    assert first.status == 201 and again.status == 201 and again.headers.get("Idempotent-Replay") == "true"
    assert len(fake.live_edges()) == 1
    other = _call(fake, "POST", "/v1/edges", dict(edge, target_id=PCA_RUN, source_id=CHOSEN), key="k1")
    assert other.status == 422 and other.body["detail"]["code"] == "idempotency_key_reused"
    # A route off the allowlist ignores the header (a GET here).
    assert _call(fake, "GET", f"/v1/runs/{CHOSEN}", key="k1").status == 200
    # The allowlist is the server's own, read from its source.
    routes = {(m, p.pattern) for m, p in fp.idempotent_routes()}
    assert ("POST", r"^/v1/edges$") in routes and ("PATCH", r"^/v1/runs/[^/]+$") in routes
    assert routes == {(m, p) for m, p in fp._FALLBACK_IDEMPOTENT}


@pytest.fixture
def served(tmp_path):
    fake = _fake(T0 + 3600)
    server = fp.Served(fake, upstream=None, mcp=True)
    yield fake, server
    server.stop()


def _cli(tmp_path: Path, server, *args: str) -> subprocess.CompletedProcess:
    layout = _layout(tmp_path)
    env = sb.worker_env(layout, base_url=server.url, token=server.fake.token,
                        extra={"PROBE_TOKEN": server.fake.token, "PYTHONPATH": str(SRC), "PROBE_ASYNC": "0"})
    return subprocess.run([sys.executable, "-c", "import sys; from probe.cli import main; sys.exit(main())", *args],
                          env=env, capture_output=True, text=True, timeout=120, cwd=str(layout.home))


def test_the_real_cli_writes_through_the_fake_unmodified(tmp_path, served):
    fake, server = served
    out = _cli(tmp_path, server, "notes", "checkout", "--experiment", "svm-vs-logreg")
    assert out.returncode == 0, out.stderr
    path = Path(json.loads(out.stdout)["path"])
    path.write_text("SVM wins: 0.9889 vs 0.9603\n")
    assert _cli(tmp_path, server, "notes", "push", "--experiment", "svm-vs-logreg").returncode == 0
    assert _cli(tmp_path, server, "run", "tag", "fortunate-quail-346", "abandoned").returncode == 0
    edge = _cli(tmp_path, server, "edge", "add", "--source", f"run:{PCA_RUN}", "--relation", "derived_from",
                "--target", f"run:{CHOSEN}")
    assert edge.returncode == 0, edge.stderr
    state = fake.final_state()
    assert state["entities"][SVM]["notes"] == "SVM wins: 0.9889 vs 0.9603\n"
    assert "abandoned" in state["entities"][CHOSEN]["tags"]
    assert [(e["source_id"], e["relation"], e["target_id"]) for e in state["edges"]] == [(PCA_RUN, "derived_from",
                                                                                         CHOSEN)]
    assert fake.unmapped == []


def test_the_real_mcp_reads_the_same_evolving_state(served):
    fake, server = served
    from mcp import ClientSession
    from mcp.client.streamable_http import streamable_http_client

    _call(fake, "PATCH", f"/v1/projects/{SVM}", {"notes": "the verdict", "force": True})

    async def main():
        import httpx

        http = httpx.AsyncClient(headers={"Authorization": f"Bearer {fake.token}"}, timeout=60)
        async with http, streamable_http_client(server.url + "/mcp", http_client=http) as (r, w, _):
            async with ClientSession(r, w) as session:
                await session.initialize()
                names = {t.name for t in (await session.list_tools()).tools}
                notes = await session.call_tool("entity", {"refs": ["experiment:svm-vs-logreg"], "view": "notes"})
                tree = await session.call_tool("browse", {"ref": f"project:{PROJECT}"})
                return names, notes, tree

    names, notes, tree = asyncio.run(main())
    assert {"browse", "entity", "search"} <= names
    assert not notes.isError and "the verdict" in notes.content[0].text
    assert not tree.isError and "svm-vs-logreg" in tree.content[0].text


def test_the_fake_answers_keyword_search_and_the_name_only_switch():
    """`search(semantic=false)` reaches the fake as `retrieval: "keyword"`: the
    same word match (the fake's semantic was always one) with the mode echoed,
    so the MCP labels the hits `keyword`. `include_semantic: false` leaves the
    semantic section empty, as the server does."""
    fake = _fake(fp.parse_ts(LATER))
    answer = _call(fake, "POST", "/v1/search", {"query": "pca", "retrieval": "keyword"})
    body = answer.body
    assert body["semantic"]["retrieval"] == "keyword"
    assert body["semantic"]["results"], "the keyword search finds the pca run by its words"
    plain = _call(fake, "POST", "/v1/search", {"query": "pca"}).body
    assert "retrieval" not in plain["semantic"]
    assert [h["doc_id"] for h in plain["semantic"]["results"]] == [
        h["doc_id"] for h in body["semantic"]["results"]
    ]
    names_only = _call(fake, "POST", "/v1/search", {"query": "pca", "include_semantic": False}).body
    assert names_only["semantic"]["results"] == []


# ---------------------------------------------------------------------------
# The folder, file by file.
# ---------------------------------------------------------------------------


def test_files_appear_when_the_clock_passes_their_mtime(tmp_path):
    src = tmp_path / "live" / "trials" / "digits"
    (src / "results").mkdir(parents=True)
    for name, at in (("old.py", T0 - 100), ("results/table.md", T0 + 30), ("later.txt", T0 + 10_000)):
        (src / name).write_text(name)
        os.utime(src / name, (at, at))
    (src / "__pycache__").mkdir()
    (src / "__pycache__" / "x.pyc").write_text("skip")
    dest = tmp_path / "sandbox"
    reveal = wd.Reveal([wd.scan(src)], lambda p: dest / p.relative_to(src.parent.parent), session_end=T0 + 600)
    shown = dest / "trials" / "digits"
    reveal.until(T0)
    assert sorted(p.name for p in shown.rglob("*") if p.is_file()) == ["old.py"]
    assert (shown / "old.py").stat().st_mtime == pytest.approx(T0 - 100)
    reveal.until(T0 + 29)
    assert not (shown / "results" / "table.md").exists()
    reveal.until(T0 + 31)
    assert (shown / "results" / "table.md").read_text() == "results/table.md"
    reveal.until(T0 + 20_000)
    assert not (shown / "later.txt").exists()  # changed after the session: never shown
    assert reveal.summary() == {"folders": [str(src)], "revealed": 2, "not_yet": 0, "after_session": 1,
                                "skipped": 0}


def test_the_working_folders_come_from_the_transcript_like_the_daemons(tmp_path):
    home = tmp_path / "home"
    (home / "trials" / "digits" / "sub").mkdir(parents=True)
    (home / ".cache" / "x").mkdir(parents=True)

    def line(block):
        return json.dumps({"type": "assistant", "cwd": str(home), "message": {"content": [block]}}).encode()

    lines = [line({"type": "tool_use", "name": "Bash", "input": {"command": "cd ~/trials/digits && python run.py"}}),
             line({"type": "tool_use", "name": "Write", "input": {"file_path": f"{home}/trials/digits/sub/a.py"}}),
             line({"type": "tool_use", "name": "Bash", "input": {"command": "cd ~/.cache/x; ls"}}),
             line({"type": "tool_use", "name": "Bash", "input": {"command": "cd ~ && ls"}})]
    assert wd.derive_workdirs(lines, home) == [home / "trials" / "digits"]


# ---------------------------------------------------------------------------
# The scorer.
# ---------------------------------------------------------------------------

KEY = {"project": PROJECT, "svm_experiment": SVM, "pca_experiment": PCA_EXP, "chosen_runs": [CHOSEN],
       "pca_run": PCA_RUN, "superseded_run": None}
READS = {f"/v1/runs/{CHOSEN}/artifacts": [{"id": FILE_ID, "kind": "file"}, {"id": "c", "kind": "code"}]}
GOOD = ("RBF SVM (C=10, gamma=0.001) wins: CV 0.9889 vs 0.9603 for logistic regression. Caveat: one split only. "
        "PCA to 32 components was dropped.")


def _entity(kind="project", **kw):
    return {"kind": kind, "notes": None, "description": None, "tags": [], "sub_notes": [], "frozen": True,
            "status": None, "name": None, "slug": None, "parent": None, **kw}


def _final(entities=None, edges=(), file_notes=None, created=()):
    return {"label": "x", "fixture": "fx", "final": {"entities": entities or {}, "edges": list(edges),
                                                     "file_notes": file_notes or {}, "created": list(created)}}


def test_the_final_state_is_scored_not_a_write_that_was_overwritten():
    later_wrong = {"label": "x", "fixture": "fx", "edges": [], "entity_patches": {}, "file_notes": {},
                   "notes": [{"target": ["project", PROJECT], "title": "", "body": GOOD, "main": True},
                             {"target": ["project", PROJECT], "title": "", "body": "The SVM wins.", "main": True}]}
    assert not score.score(later_wrong, KEY, READS)["checks"]["E1 headline"]
    later_right = dict(later_wrong, notes=list(reversed(later_wrong["notes"])))
    assert score.score(later_right, KEY, READS)["checks"]["E1 headline"]
    # The same for a titled sub-note: its last body is what Probe holds.
    sub = dict(later_wrong, notes=[dict(n, title="Decision", main=False) for n in later_wrong["notes"]])
    assert not score.score(sub, KEY, READS)["checks"]["E1 headline"]
    # A bench result is its final state.
    s = score.score(_final({PROJECT: _entity(notes=GOOD)}), KEY, READS)
    assert s["checks"]["E1 headline"] and s["checks"]["E2 pca"] and s["checks"]["E3 caveat"]


def test_a_description_that_was_already_there_is_not_the_daemons_record():
    frozen = _entity("run", description="Caveat: only one split; C=10 gamma=0.001 0.9889 vs 0.9603")
    assert not score.score(_final({CHOSEN: frozen}), KEY, READS)["checks"]["E1 headline"]
    written = dict(frozen, description_changed=True)
    assert score.score(_final({CHOSEN: written}), KEY, READS)["checks"]["E1 headline"]


@pytest.mark.parametrize(("svm", "logreg", "passes"), [
    ("0.9889", "0.9701", True),  # as the key has them
    ("98.89%", "97.01%", True),
    ("0.989", "0.970", True),  # rounded to 3 decimals: a correct record
    ("98.9%", "97.0 %", True),  # the percent to 1 decimal, with its sign
    ("0.989", "0.970.", True),  # a full stop after it is not a digit
    ("0.99", "0.97", False),  # 2 decimals: 0.97 is as near 0.9660 as 0.9701
    ("0.989", "97%", False),
    ("0.989", "0.9702", False),  # another 4-decimal value, not a rounding
    ("0.989", "10.970", False),  # a different number that ends the same
    ("0.989", "97.0", False),  # a one-decimal percent needs its % sign
    ("0.990", "0.970", False),  # rounded the wrong way
])
def test_e1_accepts_the_keys_numbers_rounded_to_three_decimals(svm, logreg, passes):
    key = dict(KEY, numbers={"svm": "0.9889", "logreg": "0.9701"})
    note = f"RBF SVM (C=10, gamma=0.001) wins: CV {svm} vs {logreg} for logistic regression."
    assert score.score(_final({PROJECT: _entity(notes=note)}), key, READS)["checks"]["E1 headline"] is passes


def test_a_number_the_key_gives_at_three_decimals_or_fewer_is_matched_as_before():
    pattern = score._number({"numbers": {"pca": "0.96"}}, "pca", score.PCA_VERDICT)
    assert pattern.pattern == r"0\.96|96"
    tie = score._number({"numbers": {"x": "0.9885"}}, "x", score.NUM_SVM)  # half-up 0.989, half-even 0.988
    assert tie.search("0.989") and tie.search("0.988") and tie.search("98.9%") and not tie.search("0.987")


def test_lineage_counts_only_from_the_pca_run_with_a_derivation_relation():
    def lineage(edge):
        return score.score(_final(edges=[edge]), KEY, READS)

    right = {"source_id": PCA_RUN, "target_id": CHOSEN, "relation": "derived_from"}
    assert lineage(right)["metrics"]["E5 lineage"]
    backwards = lineage({"source_id": CHOSEN, "target_id": PCA_RUN, "relation": "derived_from"})
    assert not backwards["metrics"]["E5 lineage"] and backwards["lineage"]["reversed"] == ["derived_from"]
    wrong = lineage(dict(right, relation="produces"))
    assert not wrong["metrics"]["E5 lineage"] and wrong["lineage"]["wrong_relation"] == ["produces"]
    assert lineage(dict(right, relation="branched_from"))["metrics"]["E5 lineage"]


def test_penalties_for_duplicates_and_numbers_the_transcript_never_shows():
    new_exp = "88888888-8888-4888-8888-888888888888"
    entities = {
        SVM: _entity("experiment", name="SVM vs logistic regression", slug="svm-vs-logreg", parent=PROJECT),
        new_exp: _entity("experiment", name="SVM vs Logistic Regression", slug="svm-vs-logreg-2", parent=PROJECT,
                         frozen=False),
        PROJECT: _entity(notes="Best CV 0.9889 (98.89%); logistic 0.9603; invented 0.9123 and 4242 digits.",
                         sub_notes=[{"title": "Verdict", "body": "a"}, {"title": "verdict", "body": "b"}]),
    }
    evidence = score.Evidence('{"cv_accuracy_mean": 0.9888646922183508, "logreg": 0.96031} 1437 test digits')
    s = score.score(_final(entities, created=[new_exp]), KEY, READS, evidence)
    assert len(s["penalties"]["duplicate_entities"]) == 1
    assert len(s["penalties"]["duplicate_notes"]) == 1
    assert sorted(x.split()[0] for x in s["penalties"]["unsupported_numbers"]) == ["0.9123", "4242"]
    assert s["penalty"] == pytest.approx(1.0 + 0.5 + 0.5)
    assert s["net"] == pytest.approx(s["passed"] - 2.0)


def test_file_notes_are_a_parity_check_only_when_the_key_has_the_inline_count():
    reads = {f"/v1/runs/{CHOSEN}/artifacts": [{"id": f"f{i}", "kind": "file"} for i in range(10)]}
    notes = {f"f{i}": "a note" for i in range(9)}
    plain = score.score(_final(file_notes=notes), KEY, reads)
    assert "E7 files" not in plain["checks"] and plain["file_note_fraction"] == pytest.approx(0.9)
    key = dict(KEY, file_notes_parity={"fraction": 1.0, "tolerance": 0.1})
    assert score.score(_final(file_notes=notes), key, reads)["checks"]["E7 files"]
    fewer = {f"f{i}": "a note" for i in range(8)}
    assert not score.score(_final(file_notes=fewer), key, reads)["checks"]["E7 files"]


def test_no_answer_key_requires_file_notes():
    """Notes are optional, only for learnings and decisions worth sharing."""
    for path in (EVALS / "expected").glob("*.json"):
        assert "file_notes_parity" not in json.loads(path.read_text()), path.name


def test_a_round_is_priced_with_its_cache_reads_and_one_without_a_count_read_none():
    prices = bench.load_prices()
    # From the LiteLLM chart; Google bills no separate write, so a write is input.
    assert prices["gemini-3.8-flash"] == pytest.approx((0.75, 3.75, 0.075, 0.75))
    rnd = {"model": "gemini/gemini-3.8-flash", "input_tokens": 1_000_000, "output_tokens": 100_000,
           "cached_tokens": None}
    assert bench.round_cost(rnd, prices) == pytest.approx(0.75 + 0.375)
    assert bench.round_cost(dict(rnd, cached_tokens=800_000), prices) == pytest.approx(0.15 + 0.06 + 0.375)
    assert bench.round_cost(dict(rnd, model="no-such-model"), prices) is None


def test_a_gpt_6_1_sol_round_is_priced_at_its_context_tier():
    """Past 272,000 prompt tokens (cached and written included) every token of a
    gpt-6.1-sol round is at the long rates, as OpenAI bills and the proxy meters."""
    prices = dict(bench.PRICES)
    rnd = {"model": "gpt-6.1-sol", "input_tokens": 272_000, "output_tokens": 10_000,
           "cached_tokens": 200_000, "cache_write_tokens": 0}
    assert bench.round_cost(rnd, prices) == pytest.approx((72_000 * 2 + 200_000 * 0.10 + 10_000 * 10) / 1e6)
    assert bench.round_cost(dict(rnd, input_tokens=272_001), prices) == pytest.approx(
        (72_001 * 4 + 200_000 * 0.20 + 10_000 * 15) / 1e6)


@pytest.mark.parametrize(
    "model,expected",
    [
        # 1M prompt = 600K read + 300K written + 100K fresh, plus 100K output, per MTok:
        # Opus 5.5 read 0.20 / write 5 / input 4 / output 20
        ("claude-opus-5-5", 0.6 * 0.20 + 0.3 * 5.00 + 0.1 * 4.00 + 0.1 * 20.00),
        # Opus 5 read 0.50 / write 6.25 / input 5 / output 25
        ("claude-opus-5", 0.6 * 0.50 + 0.3 * 6.25 + 0.1 * 5.00 + 0.1 * 25.00),
        # Sonnet 5 read 0.20 / write 2.50 / input 2 / output 10
        ("claude-sonnet-5", 0.6 * 0.20 + 0.3 * 2.50 + 0.1 * 2.00 + 0.1 * 10.00),
    ],
)
def test_a_claude_round_prices_its_cache_writes_at_the_write_rate(model, expected):
    """The model arms of the daemon-model bench: a round on each Claude model is
    priced with its cache writes at the write rate (#2381 reports them as
    `prompt_tokens_details.cache_write_tokens`), not as plain input."""
    prices = bench.load_prices()
    rnd = {"model": model, "input_tokens": 1_000_000, "output_tokens": 100_000,
           "cached_tokens": 600_000, "cache_write_tokens": 300_000}
    assert bench.round_cost(rnd, prices) == pytest.approx(expected)
    # An older route that reports no writes prices the same tokens as input.
    old_route = dict(rnd, cache_write_tokens=None)
    assert bench.round_cost(old_route, prices) == pytest.approx(
        expected - 0.3 * (prices[model][3] - prices[model][0]))


def test_the_fake_records_the_cache_writes_the_route_reports():
    body = json.dumps({"model": "claude-sonnet-5", "choices": [],
                       "usage": {"prompt_tokens": 1000, "completion_tokens": 10,
                                 "prompt_tokens_details": {"cached_tokens": 600, "cache_write_tokens": 300}}}).encode()
    rec = fp._round_record("/v1/companion/chat/completions", b"{}", 200, body, 0.0, 0.0, "write")
    assert (rec["cached_tokens"], rec["cache_write_tokens"]) == (600, 300)


def test_a_generic_key_scores_any_session():
    key = {"facts": [{"name": "F1 verdict", "targets": ["svm-vs-logreg"], "all": [r"0\.9889"], "any": ["wins", "beats"]}],
           "lineage": [{"name": "L1", "from": PCA_RUN, "to": [CHOSEN]}],
           "describe": [PROJECT], "flagged": [{"run": CHOSEN}],
           "file_notes_parity": {"fraction": 0.5, "tolerance": 0.0}}
    entities = {SVM: _entity("experiment", slug="svm-vs-logreg", notes="The SVM wins at 0.9889."),
                PROJECT: _entity(description="digits", description_changed=True),
                CHOSEN: _entity("run", tags=["abandoned"])}
    s = score.score(_final(entities, edges=[{"source_id": PCA_RUN, "target_id": CHOSEN, "relation": "derived_from"}],
                           file_notes={FILE_ID: "t"}), key, READS)
    assert s["checks"] == {"F1 verdict": True, f"flagged {CHOSEN[:8]}": True, "E7 files": True}
    # Lineage and descriptions are reported, never counted (Richard, 2026-09-26).
    assert s["metrics"] == {"L1": True, f"describe {PROJECT[:8]}": True} and s["applicable"] == 3
    entities[SVM]["notes"] = "The SVM is at 0.9889."  # no verdict word
    assert not score.score(_final(entities), key, READS)["checks"]["F1 verdict"]


def test_a_fixture_can_be_built_from_any_session_with_a_draft_key(tmp_path):
    fixtures = _load("fixtures")
    at = "2026-09-23T08:0{}:00Z"
    note = ("cat > /home/me/.local/state/probe/notes/experiment/" + SVM + "/note.md <<'EOF'\n"
            "SVM wins: CV 0.9889 vs 0.9603 (C=10)\nEOF")
    rows = [{"type": "user", "timestamp": at.format(0), "cwd": "/home/me", "message": {"content": "go"}},
            {"type": "assistant", "timestamp": at.format(1), "message": {"content": [
                {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "python train.py"}},
                {"type": "tool_use", "id": "t2", "name": "Bash", "input": {"command": note}}]}},
            {"type": "user", "timestamp": at.format(2), "message": {"content": [
                {"type": "tool_result", "tool_use_id": "t2", "content": "pushed"}]}}]
    lines = [json.dumps(r).encode() for r in rows]
    cut: list[str] = []
    masked, n = fixtures.mask_recording(lines, cut)
    assert n == 1 and cut == [note] and b"notes/experiment" not in b"".join(masked)
    with pytest.raises(SystemExit):
        fixtures.offsets(masked)  # no switch line: the caller must say where the daemon takes over
    marks = fixtures.offsets(masked, "start")
    assert marks["handover_offset"] == len(masked[0]) + 1 and marks["cwd"] == "/home/me"
    reads = {f"/v1/projects/{SVM}": {"id": SVM, "slug": "svm-vs-logreg"}}
    key = fixtures.draft_key(cut, reads, {"files": 20, "noted": 5}, inline=True)
    assert key["facts"][0]["targets"] == [SVM] and key["facts"][0]["all"] == [r"0\.9889", r"0\.9603"]
    assert "file_notes_parity" not in key  # notes are optional: never a required count
    assert "file_notes_parity" not in fixtures.draft_key(cut, reads, {"files": 20, "noted": 5}, inline=False)
    # The folder, with its mtimes, travels with the fixture.
    src = tmp_path / "work"
    src.mkdir()
    (src / "a.txt").write_text("a")
    (src / ".env").write_text("SECRET=1")
    (src / "prod.pem").write_text("key")
    os.utime(src / "a.txt", (T0 + 5, T0 + 5))
    fixtures.snapshot_files([src], tmp_path / "fx")
    [folder] = wd.from_snapshot(tmp_path / "fx")
    assert [(e.rel, e.mtime) for e in folder.entries] == [("a.txt", T0 + 5)]
    assert folder.recorded == src and folder.entries[0].source.read_text() == "a"


def test_the_sdk_inbox_is_rebuilt_from_the_runs_the_session_started_after_the_handover():
    reads = _reads()
    reads[f"/v1/runs/{OLD_RUN}"] = {"id": OLD_RUN, "name": "before", "status": "completed",
                                     "created_at": "2026-09-23T07:00:00Z", "ended_at": "2026-09-23T07:10:00Z"}
    reads[f"/v1/runs/{CHOSEN}"]["config"] = {"C": 10, "big": "x" * 5000}
    fx = bench.Fixture(Path("fx"), {"session_id": "s1", "handover_time": T0}, reads, [(b"{}\n", T0)])
    messages = fx.sdk_messages("s1")
    assert [(m["event"], m["run_id"]) for _, m in messages] == [
        ("run started", CHOSEN), ("run ended", CHOSEN), ("run started", PCA_RUN), ("run ended", PCA_RUN)]
    started = messages[0][1]
    assert started["config_truncated"] and "config" not in started and started["session_id"] == "s1"
    assert messages[0][0] == fp.parse_ts("2026-09-23T08:02:00Z") and messages[1][1]["status"] == "completed"


def test_a_superseding_edge_into_the_run_flags_it():
    """L16: track-work marks a replaced run with an edge from the new run, not a tag; E8
    read tags and notes only, so that signal counted for nothing."""
    key = dict(KEY, superseded_run=OLD_RUN)
    unflagged = score.score(_final(), key, READS)
    assert unflagged["checks"]["E8 abandoned"] is False
    for relation in ("supersedes", "retried_from"):
        edge = {"source_type": "run", "source_id": PCA_RUN, "relation": relation, "target_type": "run",
                "target_id": OLD_RUN}
        assert score.score(_final(edges=[edge]), key, READS)["checks"]["E8 abandoned"], relation
    # Pointing the other way, from the old run, or with another relation: not a flag.
    for edge in ({"source_id": OLD_RUN, "relation": "supersedes", "target_id": PCA_RUN},
                 {"source_id": PCA_RUN, "relation": "derived_from", "target_id": OLD_RUN},
                 {"source_id": OLD_RUN, "relation": "retried_from", "target_id": OLD_RUN}):
        assert not score.score(_final(edges=[edge]), key, READS)["checks"]["E8 abandoned"], edge
    generic = {"facts": [], "flagged": [{"name": "old run replaced", "run": OLD_RUN}]}
    edge = {"source_id": PCA_RUN, "relation": "supersedes", "target_id": OLD_RUN}
    assert score.score(_final(edges=[edge]), generic, READS)["checks"]["old run replaced"]


# ---------------------------------------------------------------------------
# Edges: the fake refuses what the server refuses (app/lineage/schemas.py
# `EdgeCreate`, app/lineage/service.py `create_edge`), no more and no less.
# ---------------------------------------------------------------------------

PAPER = "88888888-8888-4888-8888-888888888888"
LATER = "2026-09-23T09:00:00Z"


def _edge_reads() -> dict:
    reads = _reads()
    reads[f"/v1/projects/{PCA_EXP}"] = {"id": PCA_EXP, "slug": "pca-ablation", "name": "PCA", "kind": "experiment",
                                        "description": "Does PCA help?", "parent_project_id": PROJECT, "tags": [],
                                        "notes": None, "notes_version": 0, "created_at": "2026-09-23T08:04:00Z"}
    reads[f"/v1/projects/{PROJECT}/papers"] = {"items": [{"id": PAPER, "title": "A paper",
                                                          "created_at": "2026-09-23T08:00:30Z"}]}
    reads[f"/v1/runs/{OLD_RUN}"] = {"id": OLD_RUN, "slug": "old-run-001", "name": "old", "status": "failed",
                                    "project_id": PROJECT, "experiment_id": SVM, "parent_run_id": PCA_RUN,
                                    "tags": [], "notes": None, "notes_version": 0,
                                    "created_at": "2026-09-23T08:06:00Z", "ended_at": "2026-09-23T08:07:00Z"}
    reads[f"/v1/runs/{CHOSEN}/edges"] = [
        {"id": "e0000000-0000-4000-8000-000000000001", "customer_id": "probe", "source_type": "run",
         "source_id": CHOSEN, "relation": "derived_from", "target_type": "run", "target_id": PCA_RUN,
         "meta": {}, "provenance": "human", "reason": None, "created_at": "2026-09-23T08:05:40Z", "derived": False}]
    return reads


def _edge_fake() -> "fp.FakeProbe":
    return fp.FakeProbe(_edge_reads(), clock=fp.ManualClock(fp.parse_ts(LATER)), token="bench-fake-t")


def _post_edge(fake, st, sid, relation, tt, tid, **extra):
    return _call(fake, "POST", "/v1/edges", {"source_type": st, "source_id": sid, "relation": relation,
                                             "target_type": tt, "target_id": tid, **extra})


@pytest.mark.parametrize("st, sid, relation, tt, tid, extra, status", [
    # experiment and project ends (0278): derived_from / supersedes / informed_by only
    ("project", PCA_EXP, "derived_from", "project", SVM, {}, 201),
    ("project", PCA_EXP, "supersedes", "project", SVM, {}, 201),
    ("project", PCA_EXP, "derived_from", "run", CHOSEN, {}, 201),
    ("experiment", PCA_EXP, "supersedes", "run", CHOSEN, {}, 422),  # EdgeCreate has no `experiment` type
    ("project", PCA_EXP, "informed_by", "paper", PAPER, {"provenance": "inferred"}, 201),
    ("project", PCA_EXP, "branched_from", "project", SVM, {}, 422),
    ("project", PCA_EXP, "retried_from", "run", CHOSEN, {}, 422),
    ("project", PCA_EXP, "consumes", "artifact", FILE_ID, {}, 422),
    # run ends
    ("run", PCA_RUN, "supersedes", "run", CHOSEN, {}, 201),
    ("run", PCA_RUN, "informed_by", "paper", PAPER, {"provenance": "inferred"}, 201),
    ("run", PCA_RUN, "informed_by", "paper", PAPER, {}, 422),  # a paper edge needs a provenance
    ("run", PCA_RUN, "derived_from", "paper", PAPER, {"provenance": "inferred"}, 422),
    ("run", PCA_RUN, "supersedes", "artifact", FILE_ID, {}, 422),
    ("run", PCA_RUN, "forked_from", "artifact", FILE_ID, {}, 201),  # no genealogy-shape rule on the server
    ("run", PCA_RUN, "derived_from", "run", CHOSEN, {"provenance": "provider_citation"}, 422),
    ("run", CHOSEN, "retried_from", "run", CHOSEN, {}, 422),  # an entity to itself
    ("run", PCA_RUN, "branched_from", "run", OLD_RUN, {}, 422),  # OLD's frozen parent is PCA: a cycle
    ("run", CHOSEN, "derived_from", "run", PCA_RUN, {}, 409),  # a frozen stored edge already says it
    ("run", PCA_RUN, "derived_from", "run", "99999999-9999-4999-8999-999999999999", {}, 404),
    ("project", "99999999-9999-4999-8999-999999999999", "derived_from", "project", SVM, {}, 404),
])
def test_the_fakes_edge_rules_are_the_servers(st, sid, relation, tt, tid, extra, status):
    answer = _post_edge(_edge_fake(), st, sid, relation, tt, tid, **extra)
    assert answer.status == status, answer.body
    if status == 201:
        assert answer.body["source_type"] == st


def test_a_frozen_edge_from_later_in_the_session_does_not_exist_yet():
    """Every read hides a frozen edge until the clock reaches it, so a write of
    it before then is the replay's own (201), and it closes no cycle yet."""
    reads = _edge_reads()
    reads[f"/v1/runs/{PCA_RUN}/edges"] = [
        {"id": "e0000000-0000-4000-8000-0000000000f1", "source_type": "run", "source_id": PCA_RUN,
         "relation": "derived_from", "target_type": "run", "target_id": CHOSEN, "derived": False,
         "created_at": "2026-09-23T10:00:00Z"},
        {"id": "e0000000-0000-4000-8000-0000000000f2", "source_type": "run", "source_id": CHOSEN,
         "relation": "retried_from", "target_type": "run", "target_id": PCA_RUN, "derived": False,
         "created_at": "2026-09-23T10:00:00Z"}]
    fake = fp.FakeProbe(reads, clock=fp.ManualClock(fp.parse_ts(LATER)), token="bench-fake-t")
    assert _post_edge(fake, "run", PCA_RUN, "derived_from", "run", CHOSEN).status == 201
    assert _post_edge(fake, "run", PCA_RUN, "branched_from", "run", CHOSEN).status == 201
    assert len(fake.final_state()["edges"]) == 2


def test_a_genealogy_link_fills_the_runs_parent_and_its_origin_like_the_server():
    """create_edge mirrors the first genealogy parent into the run's column, and
    the lineage read derives the run's origin from it; deleting the edge clears it."""
    from probe._generated.models import ProjectLineageOut

    fake = _edge_fake()
    made = _post_edge(fake, "run", CHOSEN, "branched_from", "run", PCA_RUN).body
    row = _call(fake, "GET", f"/v1/runs/{CHOSEN}").body
    assert (row["parent_run_id"], row["parent_relation"]) == (PCA_RUN, "branch")
    nodes = ProjectLineageOut.model_validate(_call(fake, "GET", f"/v1/projects/{SVM}/lineage").body).nodes
    origin = {str(n.id): n.origin for n in nodes}[CHOSEN]
    assert (str(origin.id), origin.via, origin.relation) == (PCA_RUN, "lineage", "branched_from")
    second = _post_edge(fake, "run", CHOSEN, "retried_from", "run", OLD_RUN).body
    _post_edge(fake, "run", CHOSEN, "forked_from", "artifact", FILE_ID)  # a file is never a run's origin
    assert _call(fake, "DELETE", f"/v1/edges/{made['id']}").status == 204
    row = _call(fake, "GET", f"/v1/runs/{CHOSEN}").body  # the next parent moves up, as delete_edge does
    assert (row["parent_run_id"], row["parent_relation"]) == (OLD_RUN, "retry")
    assert _call(fake, "DELETE", f"/v1/edges/{second['id']}").status == 204
    assert _call(fake, "GET", f"/v1/runs/{CHOSEN}").body["parent_run_id"] is None
    nodes = ProjectLineageOut.model_validate(_call(fake, "GET", f"/v1/projects/{SVM}/lineage").body).nodes
    origin = {str(n.id): n.origin for n in nodes}[CHOSEN]  # with no parent left: what it was built on
    assert (str(origin.id), origin.via, origin.relation) == (PCA_RUN, "lineage", "derived_from")


def test_a_group_filed_under_a_project_is_its_child():
    reads = _edge_reads()
    group = "abababab-abab-4bab-8bab-abababababab"
    reads[f"/v1/projects/{PROJECT}/groups"] = [{"id": group, "project_id": PROJECT, "experiment_id": None,
                                                "name": "sweep", "created_at": "2026-09-23T08:01:30Z"}]
    fake = fp.FakeProbe(reads, clock=fp.ManualClock(fp.parse_ts(LATER)), token="bench-fake-t")
    nodes = _call(fake, "GET", f"/v1/projects/{PROJECT}/lineage").body["nodes"]
    assert {(n["type"], n["id"]) for n in nodes} == {("experiment", SVM), ("experiment", PCA_EXP), ("group", group)}


def test_an_end_in_the_trash_answers_410_like_the_server():
    fake = _edge_fake()
    assert _call(fake, "DELETE", f"/v1/runs/{CHOSEN}").status in (200, 204)
    answer = _post_edge(fake, "run", PCA_RUN, "derived_from", "run", CHOSEN)
    assert answer.status == 410 and answer.body["detail"] == "in_trash"


def test_a_duplicate_answers_like_the_server_so_the_cli_prints_already_linked():
    """`{"detail": {"message", "existing_id"}}` is what `edge add` reads as
    already-linked (exit 0); a bare string reads as a refusal (exit 1)."""
    fake = _edge_fake()
    first = _post_edge(fake, "project", PCA_EXP, "supersedes", "project", SVM)
    again = _post_edge(fake, "project", PCA_EXP, "supersedes", "project", SVM)
    frozen = _post_edge(fake, "run", CHOSEN, "derived_from", "run", PCA_RUN)
    assert again.status == 409 and again.body["detail"] == {"message": "lineage edge already exists",
                                                             "existing_id": first.body["id"]}
    assert frozen.body["detail"]["existing_id"] == "e0000000-0000-4000-8000-000000000001"


def test_an_experiments_own_lineage_is_served_in_the_servers_shape():
    from probe._generated.models import ProjectLineageOut

    reads = _edge_reads()
    seen = {"id": "e0000000-0000-4000-8000-000000000002", "customer_id": "probe", "source_type": "project",
            "source_id": SVM, "relation": "derived_from", "target_type": "run", "target_id": CHOSEN, "meta": {},
            "provenance": "human", "reason": "built on the C=10 run", "created_at": "2026-09-23T08:04:30Z",
            "derived": False}
    future = dict(seen, id="e0000000-0000-4000-8000-000000000003", relation="supersedes",
                  created_at="2026-09-23T10:00:00Z")
    derived = dict(seen, id=None, derived=True, provenance="observed_call", created_at="2026-09-23T08:04:40Z")
    # A frozen origin and node list are not served as they are: both are derived now.
    reads[f"/v1/projects/{SVM}/lineage"] = {"project_id": SVM, "kind": "experiment", "edges": [future, seen, derived],
                                            "nodes": [{"type": "run", "id": OLD_RUN}],
                                            "origin": {"type": "project", "id": PROJECT, "via": "container"}}
    fake = fp.FakeProbe(reads, clock=fp.ManualClock(fp.parse_ts(LATER)), token="bench-fake-t")
    made = _post_edge(fake, "project", PCA_EXP, "supersedes", "project", SVM).body
    for path in (f"/v1/projects/{PROJECT}/experiments/{SVM}/lineage", f"/v1/projects/{SVM}/lineage",
                 "/v1/projects/svm-vs-logreg/lineage"):
        answer = _call(fake, "GET", path)
        assert answer.status == 200, (path, answer.body)
        body = ProjectLineageOut.model_validate(answer.body)
        # Stored newest first (the replay's write, then the frozen one; the 10:00 one not yet), then derived.
        assert [(str(e.id) if e.id else None, e.derived) for e in body.edges] == [
            (made["id"], False), (seen["id"], False), (None, True)], path
        # Its origin is its oldest link out (to the run), not the frozen container.
        assert (body.kind, str(body.origin.id), body.origin.via, body.origin.relation) == (
            "experiment", CHOSEN, "lineage", "derived_from")
        # Its children are the runs filed at it, each from where it came.
        assert {str(n.id) for n in body.nodes} == {CHOSEN, PCA_RUN, OLD_RUN}
        assert {str(n.id): str(n.origin.id) for n in body.nodes}[OLD_RUN] == PCA_RUN  # its parent run
    top = ProjectLineageOut.model_validate(_call(fake, "GET", f"/v1/projects/{PROJECT}/lineage").body)
    # A project lists its experiments, never the runs filed in them; the replay's
    # write is PCA_EXP's origin now.
    assert {str(n.id) for n in top.nodes} == {SVM, PCA_EXP} and top.origin is None
    assert {str(n.id): (str(n.origin.id), n.origin.via) for n in top.nodes}[PCA_EXP] == (SVM, "lineage")
    assert _call(fake, "GET", f"/v1/projects/{PROJECT}/experiments/{PROJECT}/lineage").status == 404
    assert not fake.unmapped


# ---------------------------------------------------------------------------
# Fixtures: the live v2 daemon's own links never reach a replay.
# ---------------------------------------------------------------------------


def _v2_store(state: Path, session: str, writes: list[tuple[float, list[str], str, str, str]]) -> None:
    """The live daemon's store, written by the daemon's own `Store`."""
    from probe.daemon.store import Store

    clock = {"now": 0.0}
    store = Store(state / "probe" / "daemon" / f"{session}.sqlite", clock=lambda: clock["now"])
    for at, argv, head, status, output in writes:
        clock["now"] = at
        store.log_write(bite=None, op_id="o", argv=argv, head=head, status=status, output=output)


def test_the_live_daemons_edges_are_scrubbed_from_every_frozen_listing(tmp_path):
    fixtures = _load("fixtures")
    at = fp.parse_ts("2026-09-23T08:10:00Z")
    by_id = "e0000000-0000-4000-8000-0000000000aa"
    run_edge = {"id": by_id, "source_type": "run", "source_id": PCA_RUN, "relation": "branched_from",
                "target_type": "run", "target_id": CHOSEN, "derived": False, "created_at": "2026-09-23T08:09:59Z"}
    exp_edge = {"id": "e0000000-0000-4000-8000-0000000000bb", "source_type": "project", "source_id": PCA_EXP,
                "relation": "derived_from", "target_type": "run", "target_id": CHOSEN, "derived": False,
                "created_at": "2026-09-23T08:09:58Z"}
    queued_edge = {"id": "e0000000-0000-4000-8000-0000000000cc", "source_type": "experiment", "source_id": PCA_EXP,
                   "relation": "supersedes", "target_type": "project", "target_id": SVM, "derived": False,
                   "created_at": "2026-09-23T08:12:00Z"}
    # A person's link the daemon tried to write again: `already_linked`, never scrubbed.
    persons = {"id": "e0000000-0000-4000-8000-0000000000ee", "source_type": "run", "source_id": PCA_RUN,
               "relation": "derived_from", "target_type": "run", "target_id": CHOSEN, "derived": False,
               "created_at": "2026-09-23T08:06:00Z", "provenance": "human"}
    # The same key as a ran write with no id, but made long before it: not the daemon's.
    older = dict(exp_edge, id="e0000000-0000-4000-8000-0000000000dd", created_at="2026-09-23T08:00:30Z",
                 source_id=PCA_EXP, target_id=CHOSEN)
    derived = dict(exp_edge, id=None, derived=True)
    edge = ["probe", "edge", "add"]
    _v2_store(tmp_path, "s1", [
        (at, [*edge, "--source", f"run:{PCA_RUN}", "--relation", "branched_from", "--target", f"run:{CHOSEN}"],
         "edge add", "ran", json.dumps({"id": by_id}) + "\nprobe: a note on stderr\n"),
        (at, [*edge, "--source", "experiment:pca-ablation", "--relation=derived_from",
              "--target", "run:fortunate-quail-346"], "edge add", "ran", "not json"),
        (at, ["probe", "--sync", *edge, "--source", f"experiment:id:{PCA_EXP}", "--relation", "supersedes",
              "--target", "project:svm-vs-logreg"], "edge add", "queued", ""),
        (at, [*edge, "--source", f"run:{PCA_RUN}", "--relation", "derived_from", "--target", f"run:{CHOSEN}",
              "--reason", "again"], "edge add", "ran",
         json.dumps({"already_linked": True, "id": persons["id"], "applied": False}) + "\nprobe: --reason not applied\n"),
        (at, [*edge, "--source", f"experiment:{PCA_EXP}", "--relation", "supersedes", "--target", f"run:{CHOSEN}"],
         "edge add", "failed", "error: ..."),
        # Cut short: it MAY have landed, but a same-key edge may be someone else's.
        (at, [*edge, "--source", f"run:{PCA_RUN}", "--relation", "derived_from", "--target", f"run:{CHOSEN}"],
         "edge add", "cancelled", None),
        (at, ["probe", "notes", "push"], "notes push", "ran", "{}"),
    ])
    writes = fixtures.daemon_edge_writes("s1", state=tmp_path)
    assert [(w["status"], w["id"]) for w in writes] == [("ran", by_id), ("ran", None), ("queued", None)]
    reads = _edge_reads()
    reads[f"/v1/runs/{PCA_RUN}"] = dict(reads[f"/v1/runs/{PCA_RUN}"], parent_run_id=CHOSEN, parent_relation="branch")
    reads[f"/v1/runs/{PCA_RUN}/edges"] = [run_edge, persons]
    reads[f"/v1/projects/{PCA_EXP}/lineage"] = {"project_id": PCA_EXP, "edges": [exp_edge, queued_edge, older,
                                                                                 derived]}
    assert fixtures.scrub_daemon_edges(reads, writes) == 3
    assert reads[f"/v1/runs/{PCA_RUN}/edges"] == [persons]
    assert reads[f"/v1/projects/{PCA_EXP}/lineage"]["edges"] == [older, derived]
    # The genealogy write had filled the run's parent: put back what is left (none).
    assert (reads[f"/v1/runs/{PCA_RUN}"]["parent_run_id"], reads[f"/v1/runs/{PCA_RUN}"]["parent_relation"]) == (
        None, None)
    assert fixtures.daemon_edge_writes("no-such-session", state=tmp_path) == []


def test_a_slug_two_rows_share_is_not_guessed(tmp_path):
    fixtures = _load("fixtures")
    reads = _edge_reads()
    twin = "99999999-9999-4999-8999-999999999990"
    reads[f"/v1/projects/{twin}"] = dict(reads[f"/v1/projects/{PCA_EXP}"], id=twin)  # same slug, other project
    edge = {"id": "e0000000-0000-4000-8000-0000000000ab", "source_type": "project", "source_id": PCA_EXP,
            "relation": "derived_from", "target_type": "run", "target_id": CHOSEN, "derived": False,
            "created_at": "2026-09-23T08:09:58Z"}
    reads[f"/v1/projects/{PCA_EXP}/lineage"] = {"edges": [edge]}
    writes = [{"source": "experiment:pca-ablation", "relation": "derived_from", "target": f"run:{CHOSEN}",
               "id": None, "at": fp.parse_ts("2026-09-23T08:10:00Z"), "status": "ran"}]
    assert fixtures.scrub_daemon_edges(reads, writes) == 0


def test_an_arm_whose_skills_differ_from_the_venvs_installed_copy_is_named(tmp_path):
    """`--src` swaps Python code, but the daemon reads `track-work` from the
    venv's installed copy first (`bite.skills_root()`): an arm with other skill
    text would run the venv's. The bench names it before anything starts."""
    venv, agent = tmp_path / "venv", tmp_path / "arm" / "agent"
    (venv / "lib" / "python3.12" / "site-packages").mkdir(parents=True)
    (venv / "pyvenv.cfg").write_text("version_info = 3.12.0\n")
    (venv / "bin").mkdir()
    (venv / "bin" / "python").symlink_to(sys.executable)
    (agent / "src").mkdir(parents=True)
    for root, text in ((venv / "share" / "probe-research" / "skills", "main's rule"), (agent / "skills", "main's rule")):
        for name in ("track-work", "edit-notes"):
            (root / name).mkdir(parents=True)
            (root / name / "SKILL.md").write_text(text)
    py = sb.Python.find(venv, agent / "src")
    assert py.stale_skills() == []
    (agent / "skills" / "track-work" / "SKILL.md").write_text("the arm's new rule")
    assert py.stale_skills() == ["track-work"]
    import shutil

    shutil.rmtree(venv / "share")  # nothing installed: the daemon falls back to the arm's own
    assert py.stale_skills() == []


def test_the_mlp_keys_paper_why_reads_the_rule_however_it_is_conjugated():
    """F4 failed notes that stated the stopping rule as "stops after 5 epochs ...
    keeps the best epoch" (bench of #2418): the pattern wanted "stop after" and
    "keep the best". Any form of the verb is the same rule."""
    import re

    key = json.loads((EVALS / "expected" / "sxs-mlp-daemon-a.json").read_text())
    [f4] = [f for f in key["facts"] if f["name"].startswith("F4")]
    prechelt = re.compile(f4["all"][1], re.I)
    for note in ("Early Stopping, But When? (Prechelt): the follow-up's rule, which stops after 5 epochs",
                 "Prechelt (1998): the follow-up keeps the best validation epoch",
                 "But When? (Prechelt): stop after 5 epochs with no gain, keep the best epoch"):
        assert prechelt.search(note), note
    assert not prechelt.search("Prechelt (1998): a paper about early stopping in general")


def test_worker_env_takes_only_daemon_and_reader_tuning():
    """`--worker-env` passes daemon/reader tuning only: never a key, an outbox,
    telemetry, or a setting the bench sets itself (which would mislabel an arm)."""
    bench = _load("bench")
    for name in ("PROBE_DAEMON_CONTEXT_TOKENS", "PROBE_READER_CONTEXT_TOKENS"):
        assert name.startswith(bench.WORKER_ENV_PREFIXES) and name not in bench.WORKER_ENV_REFUSED
    for name in ("PROBE_OUTBOX_DIR", "PROBE_TELEMETRY_HOST", "PROBE_DAEMON_KEY", "PROBE_DAEMON_READS",
                 "PROBE_COMPANION_MODEL"):
        assert not name.startswith(bench.WORKER_ENV_PREFIXES) or name in bench.WORKER_ENV_REFUSED


def test_track_work_linking_names_only_relations_the_server_takes():
    """Every relation track-work's "Linking" section teaches is in the server's
    vocabulary (the generated `LineageRelation`), every `--source X --relation R
    --target Y` example passes the fake's copy of the server's edge rules, and the
    "end takes only" list is the fake's project/experiment end list: a renamed or
    narrowed relation would otherwise leave the daemon writing an edge that 422s,
    with every skill-sync test still green."""
    import re

    from probe._generated.models import LineageRelation

    text = (AGENT / "skills" / "track-work" / "SKILL.md").read_text(encoding="utf-8")
    section = text.split("### Linking", 1)[1].split("\n## ", 1)[0]
    flat = " ".join(section.split())
    named = set(re.findall(r"`([a-z]+_(?:from|by|on|via)|supersedes)`", section))
    named |= set(re.findall(r"--relation (\w+)", flat))
    assert {"branched_from", "retried_from", "derived_from", "supersedes", "informed_by"} <= named
    assert named <= {r.value for r in LineageRelation}, named - {r.value for r in LineageRelation}
    examples = re.findall(r"--source (\w+):\S+ --relation (\w+) --target (\w+):", flat)
    assert examples
    end = {"experiment": "project"}
    for st, relation, tt in examples:
        assert fp.FakeProbe._edge_shape(fp.FakeProbe, end.get(st, st), relation, end.get(tt, tt), "a", "b", None) \
            is None, (st, relation, tt)
    ends = re.search(r"end takes only(.*?)\n\s*- ", section, re.S)
    assert ends and set(re.findall(r"`(\w+)`", ends.group(1))) == fp.FakeProbe.PROJECT_END_RELATIONS


def test_the_model_proxy_forwards_the_servers_pushed_settings(monkeypatch):
    """A bench worker hears the server's pushed daemon settings (`x-probe-*`:
    context sizes, reader gate, writer gap and layout) as a live one does --
    before 10-14 only the retry hints were forwarded -- and nothing else."""
    import httpx
    from starlette.testclient import TestClient

    def upstream(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer the-real-key", "the real key goes upstream only"
        return httpx.Response(200, json={"id": "c", "object": "chat.completion", "created": 0, "model": "m",
                                         "choices": []},
                              headers={"x-probe-writer-history": "lean", "x-probe-reader-gate": "shadow",
                                       "x-should-retry": "false", "set-cookie": "s=1"})

    real = httpx.AsyncClient
    monkeypatch.setattr(httpx, "AsyncClient",
                        lambda **kw: real(**{**kw, "transport": httpx.MockTransport(upstream)}))
    fake = _fake(T0 + 3600)
    app = fp.build_app(fake, upstream=fp.Upstream("https://upstream.test", "the-real-key"), mcp=False)
    with TestClient(app) as client:
        answer = client.post("/v1/companion/chat/completions", json={"model": "m", "messages": []},
                             headers={"Authorization": f"Bearer {fake.token}"})
    assert answer.headers["x-probe-writer-history"] == "lean" and answer.headers["x-probe-reader-gate"] == "shadow"
    assert answer.headers["x-should-retry"] == "false"
    assert "set-cookie" not in answer.headers
