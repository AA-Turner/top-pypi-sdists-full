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
    assert {"browse", "entity", "search_knowledge"} <= names
    assert not notes.isError and "the verdict" in notes.content[0].text
    assert not tree.isError and "svm-vs-logreg" in tree.content[0].text


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
    assert prices["gemini-3.8-flash"] == pytest.approx((0.75, 3.75, 0.075))  # from the LiteLLM chart
    rnd = {"model": "gemini/gemini-3.8-flash", "input_tokens": 1_000_000, "output_tokens": 100_000,
           "cached_tokens": None}
    assert bench.round_cost(rnd, prices) == pytest.approx(0.75 + 0.375)
    assert bench.round_cost(dict(rnd, cached_tokens=800_000), prices) == pytest.approx(0.15 + 0.06 + 0.375)
    assert bench.round_cost(dict(rnd, model="no-such-model"), prices) is None


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
    """L16: rule 3 marks a rerun with an edge from the new run, not a tag; E8
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
