"""A folder import files into a NEW project unless code or a person says otherwise.

On 2026-10-26 two throwaway smoke folders imported with `--yes` into team
`probe` landed in unrelated existing projects (`import-model-benchmark`, then
`digits-perceptron-training`): the classifier was shown every project, told to
"prefer these", and its pick was reused at creation with nothing on the review
screen saying so. These tests pin the replacement (`backfill_projects`):

  * a re-import of the same folder, and a folder whose repository is a
    project's code source, reuse that project silently (RULE);
  * any other reuse is a checked `probe-backfill-plan project --reuse` call,
    marked EXISTING on the review screen and in plan.json, and turned into a
    new project when nobody reviews the plan (`--yes`, automatic imports);
  * a mistyped reuse is refused with the nearest real project;
  * a new slug an edit away from an existing one is flagged.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from backfill_plan_agent import tool
from backfill_test_client import ScopedClient

from probe.cli import backfill as bf
from probe.cli import backfill_evidence as ev
from probe.cli import backfill_plan as bp
from probe.cli import backfill_plan_tool as t
from probe.cli import backfill_projects as projects
from probe.cli import backfill_run as br
from probe.cli import telemetry as tm
from probe.cli import tui
from probe.sdk import errors

BENCH = "import-model-benchmark"


@pytest.fixture
def folder(tmp_path):
    root = tmp_path / "bench-smoke"
    root.mkdir()
    (root / "README.md").write_text("# Model benchmark\n\nA quick model benchmark smoke.\n")
    (root / "bench.py").write_text("print('benchmark the model')\n")
    return root


@pytest.fixture(autouse=True)
def state_dir(tmp_path, monkeypatch):
    d = tmp_path / "state"
    d.mkdir()
    monkeypatch.setenv("PROBE_BACKFILL_STATE_DIR", str(d))
    monkeypatch.setattr(bf, "which_agent", lambda agent: f"/bin/{agent.value}")
    monkeypatch.setattr(br, "run_units", lambda *a, **k: [])
    monkeypatch.setattr(br, "enqueue_manifests", lambda *a, **k: (0, []))
    return d


class _Client(ScopedClient):
    """A workspace that already holds an unrelated benchmark project."""

    def __init__(self, *, sources=None):
        super().__init__()
        self.made: list[str] = []
        self.sources = sources or {}
        self.bench = self.project_row(BENCH, name="Import model benchmark",
                                      code_source_count=1 if sources else 0)
        self.transport = SimpleNamespace(get=lambda path, params=None: [{}] * 52)

    def create_project(self, slug, name=None, **kwargs):
        assert self.resolve_project(slug) is None, f"{slug} was created twice"
        self.made.append(slug)
        return super().create_project(slug, name, **kwargs)

    def get_project(self, ident):
        if ident not in self.projects:
            raise errors.NotFoundError("no such project")
        return self.projects[ident]

    def list_runs(self, **kwargs):
        return SimpleNamespace(items=[{}] * 14, next_cursor=None)

    def list_project_code_sources(self, project_id):
        return self.sources.get(project_id, [])


class _Events:
    def __init__(self):
        self.events: list[tuple[str, dict]] = []

    def emit(self, event, **props):
        self.events.append((event, props))

    def ready(self) -> dict:
        return [p for e, p in self.events if e == tm.EVENT_BACKFILL_PLAN_READY][-1]


def _agent(*calls):
    """A classifier that files through the real `probe-backfill-plan`."""
    seen: list[str] = []

    def launch(folder_, prompt, **kwargs):
        seen.append(prompt)
        if kwargs.get("path_prepend"):
            for call in calls:
                code, out = tool(kwargs, *call)
                seen.append(out)
        return True, json.dumps({"type": "result", "result": "filed"})

    launch.seen = seen
    return launch


def _plan_json(state_dir: Path) -> dict:
    found = sorted(state_dir.rglob("plan.json"), key=lambda p: p.stat().st_mtime)
    return json.loads(found[-1].read_text())


def _pages(monkeypatch):
    pages: list[list[str]] = []
    monkeypatch.setattr(tui, "page", lambda lines, prompt=None: "")

    def review(title, lines, choices):
        pages.append(list(lines))
        return "import" if title == "Review the import plan" else choices[0][1]

    monkeypatch.setattr(tui, "review", review)
    return pages


REUSE_BENCH = (("project", "--reuse", BENCH), ("assign", BENCH, "--rest"))


# -- unattended: a reuse the model chose becomes a new project ------------------


def test_an_unrelated_folder_gets_a_new_project_under_yes(folder, state_dir, monkeypatch):
    """The 2026-10-26 misfile: a README about "model benchmark", an existing
    `import-model-benchmark`, a classifier that reuses it, and `--yes`."""
    agent = _agent(*REUSE_BENCH)
    monkeypatch.setattr(bf, "launch_agent", agent)
    monkeypatch.setattr(tui, "page", lambda lines, prompt=None: "")
    client, events = _Client(), _Events()

    lines = br.execute(client_factory=lambda: client, folder=folder, agent=bf.Agent.CLAUDE,
                       interactive=False, yes=True, telemetry=events)

    assert client.made == ["bench-smoke"], "a new project, named for the folder"
    entry = {p["slug"]: p for p in _plan_json(state_dir)["projects"]}
    assert set(entry) == {"bench-smoke"} and entry["bench-smoke"]["existing"] is False
    assert entry["bench-smoke"]["possibly_same_as"] == BENCH
    text = "\n".join(lines)
    assert f"to the existing project {BENCH}; they go into a new project, bench-smoke" in text
    assert events.ready()["projects_reuse_declined"] == 1
    assert (events.ready()["projects_new"], events.ready()["projects_reused_model"],
            events.ready()["projects_reused_rule"]) == (1, 0, 0)


def test_the_reviewer_sees_existing_with_what_it_holds_and_can_approve_it(
        folder, state_dir, monkeypatch):
    monkeypatch.setattr(bf, "launch_agent", _agent(*REUSE_BENCH))
    pages = _pages(monkeypatch)
    client, events = _Client(), _Events()

    br.execute(client_factory=lambda: client, folder=folder, agent=bf.Agent.CLAUDE,
               telemetry=events)

    gate = "\n".join(pages[0])
    assert f"{BENCH}" in gate and "EXISTING" in gate
    assert '"Import model benchmark", which already has 14 runs and 52 files' in gate
    assert "Your agent chose it" in gate
    entry = {p["slug"]: p for p in _plan_json(state_dir)["projects"]}[BENCH]
    assert entry["existing"] is True and entry["origin"] == "model"
    assert entry["project_id"] == client.bench["id"]
    assert (entry["existing_runs"], entry["existing_files"]) == (14, 52)
    assert client.made == [], "an approved reuse files into the existing project"
    assert events.ready()["projects_reused_model"] == 1


# -- code reuses a project silently --------------------------------------------


def test_a_re_import_of_the_same_folder_reuses_its_project(folder, state_dir, monkeypatch):
    first = _agent(("project", "bench-smoke-lab", "--name", "Lab"), ("assign", "bench-smoke-lab", "--rest"))
    monkeypatch.setattr(bf, "launch_agent", first)
    monkeypatch.setattr(tui, "page", lambda lines, prompt=None: "")
    client = _Client()
    br.execute(client_factory=lambda: client, folder=folder, agent=bf.Agent.CLAUDE,
               interactive=False, yes=True)
    assert client.made == ["bench-smoke-lab"]

    (folder / "more.py").write_text("print('more benchmark')\n")
    # No declaration: the folder's own project takes files directly.
    second = _agent(("assign", "bench-smoke-lab", "--rest"))
    monkeypatch.setattr(bf, "launch_agent", second)
    events = _Events()
    br.execute(client_factory=lambda: client, folder=folder, agent=bf.Agent.CLAUDE,
               interactive=False, yes=True, telemetry=events)

    assert client.made == ["bench-smoke-lab"], "nothing new was created"
    assert "THIS FOLDER'S OWN PROJECTS" in second.seen[0]
    assert "this folder was imported into it before" in second.seen[0]
    ready = events.ready()
    assert (ready["projects_reused_rule"], ready["projects_new"], ready["projects_reuse_declined"]) == (1, 0, 0)
    entry = {p["slug"]: p for p in _plan_json(state_dir)["projects"]}["bench-smoke-lab"]
    assert entry["existing"] is True and entry["origin"] == "rule"


def test_a_folder_whose_repository_is_a_projects_code_source_reuses_it(
        folder, state_dir, monkeypatch):
    client = _Client()
    client.sources = {client.bench["id"]: [{"repo": "Org/Bench", "status": "active", "path_prefix": ""}]}
    client.bench["code_source_count"] = 1
    monkeypatch.setattr(projects, "_folder_repo",
                        lambda folder_: SimpleNamespace(repo="org/bench", path_prefix=""))
    agent = _agent(("assign", BENCH, "--rest"))
    monkeypatch.setattr(bf, "launch_agent", agent)
    monkeypatch.setattr(tui, "page", lambda lines, prompt=None: "")
    events = _Events()

    br.execute(client_factory=lambda: client, folder=folder, agent=bf.Agent.CLAUDE,
               interactive=False, yes=True, telemetry=events)

    assert client.made == []
    assert "its code source is org/bench" in agent.seen[0]
    assert events.ready()["projects_reused_rule"] == 1
    assert events.ready()["projects_reuse_declined"] == 0


def _coverage(*rows, project_id=None, meta=None):
    meta = dict(meta or {})
    return SimpleNamespace(scope=SimpleNamespace(workspace_id="workspace", project_id=project_id),
                           rows=lambda: list(rows), meta=lambda key, default=None: meta.get(key, default))


def _repo(monkeypatch, path_prefix=""):
    monkeypatch.setattr(projects, "_folder_repo",
                        lambda folder_: SimpleNamespace(repo="org/ml", path_prefix=path_prefix))


def _sourced(client, slug, path_prefix):
    row = client.project_row(slug, name=slug, code_source_count=1)
    client.sources[row["id"]] = [{"repo": "org/ml", "status": "active", "path_prefix": path_prefix}]
    return row


def test_a_shared_repository_makes_no_project_this_folders_own(folder, monkeypatch):
    """A whole-repo source is every subfolder's ancestor: on a monorepo that
    made every project on it "this folder's", unattended imports included."""
    client = _Client()
    _sourced(client, "rl-reward-model", "")
    _sourced(client, "tokenizer-study", "")
    _repo(monkeypatch, "experiments/new-idea")
    assert projects.load(client, _coverage(), folder).own == {}


def test_two_projects_on_this_folders_code_leave_the_choice_to_a_person(folder, monkeypatch):
    client = _Client()
    _sourced(client, "a", "")
    _sourced(client, "b", "")
    _repo(monkeypatch, "")
    assert projects.load(client, _coverage(), folder).own == {}


def test_a_source_on_this_folder_or_inside_it_is_this_folders(folder, monkeypatch):
    client = _Client()
    _sourced(client, "new-idea", "experiments/new-idea/src")
    _repo(monkeypatch, "experiments/new-idea")
    assert list(projects.load(client, _coverage(), folder).own) == ["new-idea"]


def test_a_retry_after_dead_files_still_knows_the_folders_project(folder):
    """`--retry-dead` clears the rows' project before the plan is made; the
    approved units still name it, so the retry is not a duplicate project."""
    client = _Client()
    lab = client.project_row("lab", name="Lab")
    cleared = {"path": "a.py", "project_id": None}
    coverage = _coverage(cleared, meta={"approved_units": {"u1": {"project_id": lab["id"]}}})
    assert list(projects.load(client, coverage, folder).own) == ["lab"]


def test_a_revoked_or_other_repository_source_reuses_nothing(folder, monkeypatch):
    client = _Client()
    client.bench["code_source_count"] = 2
    client.sources = {client.bench["id"]: [
        {"repo": "org/bench", "status": "revoked", "path_prefix": ""},
        {"repo": "org/other", "status": "active", "path_prefix": ""},
    ]}
    monkeypatch.setattr(projects, "_folder_repo",
                        lambda folder_: SimpleNamespace(repo="org/bench", path_prefix=""))
    known = projects.load(client, _coverage(), folder)
    assert known.own == {} and known.others == [BENCH]


def _trashed():
    """What production answers for a deleted project until it is purged."""
    exc = errors.RosError("in the trash", status=410)
    exc.in_trash = True
    return exc


def test_a_trashed_own_project_is_not_reused(folder):
    client = _Client()

    def trashed(project_id):
        raise _trashed()

    client.get_project = trashed
    row = {"path": "a.py", "project_id": "trashed-id", "project_slug": "old"}
    assert projects.load(client, _coverage(row), folder).own == {}


def test_an_existing_project_trashed_after_review_is_named():
    client = _Resolver()

    def trashed(project_id):
        raise _trashed()

    client.get_project = trashed
    with pytest.raises(projects.ExistingGone):
        _dest(client, BENCH, {"slug": BENCH, "origin": "rule", "project_id": "x"})


def test_an_expired_credential_is_never_read_as_a_gone_project(folder):
    client = _Client()

    def expired(project_id):
        raise errors.AuthError("token expired")

    client.get_project = expired
    with pytest.raises(errors.AuthError):
        projects.load(client, _coverage({"path": "a.py", "project_id": "x"}), folder)


def test_a_deleted_own_project_is_not_reused_but_a_failed_read_stops(folder):
    """Gone means a new project; a blip must never split the folder in two."""
    client = _Client()
    gone = {"path": "a.py", "project_id": "deleted-id", "project_slug": "old"}
    assert projects.load(client, _coverage(gone), folder).own == {}

    def blip(project_id):
        raise errors.TransportError("connection reset")

    client.get_project = blip
    with pytest.raises(errors.TransportError):
        projects.load(client, _coverage(gone), folder)


# -- the tool: reuse is a checked selection ----------------------------------------


def _ref(**kw):
    base = dict(root="/r", mode=t.Mode.CLASSIFY, files=("a.py", "b/c.py"),
                existing=(BENCH, "digits-perceptron-training"))
    base.update(kw)
    return t.Reference(**base)


def test_a_typo_in_a_reuse_is_refused_with_the_nearest_real_project():
    state = t.State()
    with pytest.raises(t.Refused, match=f"no existing project is called 'import-model-benchmrak'; nearest: {BENCH}"):
        t.apply(_ref(), state, {"op": "project", "slug": "import-model-benchmrak", "reuse": True})
    assert state.declared == {}
    t.apply(_ref(), state, {"op": "project", "slug": BENCH, "reuse": True})
    t.apply(_ref(), state, {"op": "assign", "project": BENCH, "rest": True})
    assert state.declared[BENCH] == {"slug": BENCH, "reuse": True}


def test_an_existing_project_is_never_a_destination_just_by_being_named():
    with pytest.raises(t.Refused, match="project --reuse import-model-benchmark"):
        t.apply(_ref(), t.State(), {"op": "assign", "project": BENCH, "rest": True})


def test_a_new_project_cannot_take_an_existing_slug():
    with pytest.raises(t.Refused, match="is an existing project's slug"):
        t.apply(_ref(), t.State(), {"op": "project", "slug": BENCH, "name": "Mine"})


def test_the_folders_own_projects_take_files_without_a_selection():
    ref = _ref(projects=("lab",), existing=(BENCH, "lab"))
    state = t.State()
    t.apply(ref, state, {"op": "assign", "project": "lab", "rest": True})
    assert "already holds this folder's work" in t.apply(
        ref, state, {"op": "project", "slug": "lab", "reuse": True})
    with pytest.raises(t.Refused, match="already holds this folder's work"):
        t.apply(ref, state, {"op": "project", "slug": "lab", "name": "Renamed"})


def test_the_command_line_takes_reuse(tmp_path, monkeypatch):
    ref = _ref(root=str(tmp_path))
    ref.write(tmp_path / "ref")
    monkeypatch.setenv(t.REF_ENV, str(tmp_path / "ref"))
    monkeypatch.setenv(t.LOG_ENV, str(tmp_path / "log" / "decisions.jsonl"))
    out: list[str] = []
    writer = SimpleNamespace(write=out.append, flush=lambda: None)
    assert t.main(["project", "--reuse", BENCH], out=writer) == 0
    assert t.main(["project", "--reuse", "import-model-bench"], out=writer) == 1
    text = "".join(out)
    assert "existing project import-model-benchmark is available" in text
    assert "nearest: import-model-benchmark" in text


# -- settle: origins, collisions, near misses -----------------------------------


def _known(*own: str):
    rows = {slug: {"id": f"id-{slug}", "slug": slug, "name": slug.title()}
            for slug in (BENCH, "esm3-baseline", *own)}
    return projects.Known(rows=rows, own={
        slug: bp.ProjectSpec(slug=slug, name=slug, origin=bp.Origin.RULE.value,
                             project_id=f"id-{slug}", reason=projects.IMPORTED_BEFORE)
        for slug in own})


def _plan(*pairs, specs=()):
    return bp.Plan(projects=list(specs), assignments=[bp.Assignment(p, s) for p, s in pairs])


def test_a_new_slug_an_edit_away_from_an_existing_one_is_flagged(tmp_path):
    plan = _plan(("a.py", "esm3-baselin"), specs=[bp.ProjectSpec("esm3-baselin", name="ESM3")])
    projects.settle(plan, _known(), attended=True, folder=tmp_path)
    spec = plan.projects[0]
    assert spec.origin == "new" and spec.near == "esm3-baseline"
    assert projects.detail(spec) == "possibly the same project as existing esm3-baseline"
    assert projects.counts(plan, {"a.py": "esm3-baselin"})["projects_near_miss"] == 1
    far = _plan(("a.py", "protein-folding"), specs=[bp.ProjectSpec("protein-folding")])
    projects.settle(far, _known(), attended=True, folder=tmp_path)
    assert far.projects[0].near == ""


def test_a_new_name_that_is_an_existing_slug_is_renamed_never_merged(tmp_path):
    """The chunked naming answer is JSON nobody checks at call time."""
    plan = _plan(("a.py", BENCH), specs=[bp.ProjectSpec(BENCH, name="Bench")])
    plan.experiments = {"e": {"slug": "e", "project": BENCH, "under": ""}}
    projects.settle(plan, _known(), attended=True, folder=tmp_path)
    assert [s.slug for s in plan.projects] == [f"{BENCH}-2"]
    assert plan.projects[0].near == BENCH and plan.assignments[0].project == f"{BENCH}-2"
    assert plan.experiments["e"]["project"] == f"{BENCH}-2"


def test_settling_twice_changes_nothing(tmp_path):
    plan = _plan(("a.py", BENCH), ("b.py", "lab"),
                 specs=[bp.ProjectSpec(BENCH, origin=bp.Origin.MODEL.value)])
    known = _known("lab")
    projects.settle(plan, known, attended=True, folder=tmp_path)
    first = [(s.slug, s.origin, s.project_id) for s in plan.projects]
    projects.settle(plan, known, attended=True, folder=tmp_path)
    assert [(s.slug, s.origin, s.project_id) for s in plan.projects] == first
    assert sorted(first) == [(BENCH, "model", f"id-{BENCH}"), ("lab", "rule", "id-lab")]


def test_unattended_reimport_reuses_the_project_it_named_for_the_folder(tmp_path):
    """A second unattended import matched to the same existing project goes
    into the folder's own project, never `<folder>-2`."""
    plan = _plan(("a.py", BENCH), specs=[bp.ProjectSpec(BENCH, origin=bp.Origin.MODEL.value)])
    out = projects.settle(plan, _known("lab-drive"), attended=False, folder=tmp_path / "lab-drive")
    assert out.declined == 1
    assert [(s.slug, s.origin) for s in plan.projects] == [("lab-drive", "rule")]
    assert plan.assignments[0].project == "lab-drive"


def test_already_imported_files_keep_their_slug(tmp_path):
    plan = _plan(("new.py", "fresh"), specs=[bp.ProjectSpec("fresh")])
    plan.fixed = {"old.py": BENCH}  # a slug some other project holds now
    for _ in range(2):
        projects.settle(plan, _known(), attended=True, folder=tmp_path)
    assert sorted(s.slug for s in plan.projects) == sorted(["fresh", BENCH])


def test_unattended_keeps_the_folders_own_projects(tmp_path):
    plan = _plan(("a.py", "lab"), ("b.py", BENCH),
                 specs=[bp.ProjectSpec(BENCH, origin=bp.Origin.MODEL.value)])
    out = projects.settle(plan, _known("lab"), attended=False, folder=tmp_path / "lab-drive")
    assert out.declined == 1
    assert {s.slug: s.origin for s in plan.projects} == {"lab": "rule", "lab-drive": "new"}
    assert {a.project for a in plan.assignments} == {"lab", "lab-drive"}


# -- chunked naming names new projects only -------------------------------------


def _chunk_evidence(rows: int = 600) -> ev.Evidence:
    files = [ev.FileEvidence(path=f"/drive/f{i}.py", size=100, mtime=0, tier=ev.Tier.EVIDENCE,
                             sample="x" * 600) for i in range(rows)]
    return ev.Evidence(root="/drive", files=files, clusters=[], sampled_files=rows,
                       sampled_bytes=rows * 600)


def test_chunked_naming_never_lists_other_projects_and_renames_a_collision(tmp_path, monkeypatch):
    folder = tmp_path / "drive"
    folder.mkdir()
    prompts: list[str] = []

    def launch(folder_, prompt, **kwargs):
        prompts.append(prompt)
        if "what lines of work one slice" in prompt:
            answer = {"findings": [{"work": "benchmark", "evidence": [], "approx_files": 3}], "notes": ""}
        elif "Decide the project list" in prompt:
            answer = {"projects": [{"slug": BENCH, "name": "Bench", "description": "d"},
                                   {"slug": "lab", "name": "Lab again"}], "summary": "s"}
        else:
            tool(kwargs, "assign", f"{BENCH}-2", "--rest")
            answer = {}
        return True, json.dumps({"type": "result", "result": "done\n" + json.dumps(answer)})

    monkeypatch.setattr(bf, "launch_agent", launch)
    own = [bp.ProjectSpec("lab", name="Lab", origin=bp.Origin.RULE.value, project_id="id-lab",
                          reason=projects.IMPORTED_BEFORE)]
    plan, _ = br.classify_chunked(folder, _chunk_evidence(), agent=bf.Agent.CLAUDE,
                                  existing=[BENCH, "digits-perceptron-training"],
                                  work_dir=folder / ".w", own=own)

    naming = next(p for p in prompts if "Decide the project list" in p)
    assert BENCH not in naming
    assert "digits-perceptron-training" not in naming
    assert "lab" in naming and "do not list them" in naming
    slugs = {s.slug: s for s in plan.projects}
    assert set(slugs) == {"lab", f"{BENCH}-2"}
    assert slugs["lab"].origin == "rule" and slugs[f"{BENCH}-2"].near == BENCH
    filing = next(p for p in prompts if "File one slice" in p)
    assert f"{BENCH}-2" in filing and "    lab  —" in filing


# -- after approval: new is new, existing is read by id -------------------------


class _Resolver:
    def __init__(self, *taken):
        self.rows = {slug: {"id": f"id-{slug}", "slug": slug} for slug in taken}
        self.made: list[str] = []
        self.lost_ack = False

    def resolve_project(self, slug, strict=False):
        return self.rows.get(slug)

    def get_project(self, project_id):
        row = next((r for r in self.rows.values() if r["id"] == project_id), None)
        if row is None:
            raise errors.NotFoundError("gone")
        return row

    def create_project(self, slug, name=None, metadata=None, **kw):
        if slug in self.rows:
            raise errors.ConflictError("taken")
        self.rows[slug] = {"id": f"id-{slug}", "slug": slug, "metadata": dict(metadata or {})}
        self.made.append(slug)
        if self.lost_ack:
            self.lost_ack = False
            raise TimeoutError("created, answer lost")
        return self.rows[slug]


def _dest(client, slug, spec, created=None):
    created = {} if created is None else created
    return projects.destination(client, slug, spec, workspace_id="w", created=created,
                                remember=lambda: None, authored_by="agent"), created


def test_a_new_project_never_merges_into_a_slug_someone_holds():
    client = _Resolver(BENCH)
    project, created = _dest(client, BENCH, {"slug": BENCH, "origin": "new"})
    assert project["slug"] == f"{BENCH}-2" and client.made == [f"{BENCH}-2"]
    assert created == {BENCH: f"id-{BENCH}-2"}


def test_an_existing_project_is_read_by_the_id_the_review_showed():
    client = _Resolver(BENCH)
    project, _ = _dest(client, BENCH, {"slug": BENCH, "origin": "model", "project_id": f"id-{BENCH}"})
    assert project["id"] == f"id-{BENCH}" and client.made == []


def test_sibling_projects_do_not_block_each_other():
    """No near-miss guard at creation: the plan was settled and reviewed."""
    client = _Resolver()
    for slug in ("odyssey-cluster-deploy", "odyssey-protein-benchmarks", "odyssey-protein-lm"):
        _dest(client, slug, {"slug": slug, "origin": "new"})
    assert len(client.made) == 3


def test_a_lost_create_answer_resumes_into_the_project_it_made():
    client = _Resolver()
    client.lost_ack = True
    created: dict = {}
    with pytest.raises(TimeoutError):
        _dest(client, "lab", {"slug": "lab", "origin": "new"}, created)
    project, _ = _dest(client, "lab", {"slug": "lab", "origin": "new"}, created)
    assert project["slug"] == "lab" and client.made == ["lab"]


def test_a_lost_create_never_adopts_a_project_someone_else_made():
    client = _Resolver()
    created = {"lab": {"pending": "lab", "nonce": "ours"}}
    client.rows["lab"] = {"id": "theirs", "slug": "lab", "metadata": {}}
    project, _ = _dest(client, "lab", {"slug": "lab", "origin": "new"}, created)
    assert project["slug"] == "lab-2" and client.made == ["lab-2"]


def test_an_existing_project_deleted_after_review_is_named():
    with pytest.raises(projects.ExistingGone, match=BENCH):
        _dest(_Resolver(), BENCH, {"slug": BENCH, "origin": "model", "project_id": "gone"})


def test_a_deleted_existing_project_sets_the_approval_aside_for_review(tmp_path):
    """Without this every re-run failed on the same saved approval for good."""
    from probe.cli import backfill_import as imp

    meta = {"approved_request": {"hashes": {}, "left_out": {}, "import_changed": False,
                                 "assigned": {"a.py": BENCH},
                                 "projects": [{"slug": BENCH, "origin": "model", "project_id": "gone"}]}}
    coverage = SimpleNamespace(
        meta=lambda key, default=None: meta.get(key, default),
        put_meta=lambda key, value: meta.__setitem__(key, value),
        rows=lambda: [], exclude=lambda *a, **k: None,
        scope=SimpleNamespace(workspace_id="w", project_id=None))
    with pytest.raises(imp._Stopped) as stopped:
        imp._finish_approved_request(coverage, _Resolver(), ledger=None)
    assert "was deleted after the plan was approved" in stopped.value.lines[0]
    assert meta["approved_request"] is None and meta["superseded_request"]["assigned"] == {"a.py": BENCH}


def test_a_plan_saved_by_an_older_cli_resolves_by_slug_as_it_did():
    client = _Resolver(BENCH)
    project, _ = _dest(client, BENCH, {"slug": BENCH, "name": "x"})
    assert project["slug"] == BENCH and client.made == []


def test_a_naming_answer_with_no_usable_slug_falls_back_even_with_own_projects(tmp_path, monkeypatch):
    """Otherwise every file is forced into the folder's own projects."""
    folder = tmp_path / "drive"
    folder.mkdir()

    def launch(folder_, prompt, **kwargs):
        if "what lines of work one slice" in prompt:
            answer = {"findings": [{"work": "x", "evidence": [], "approx_files": 3}], "notes": ""}
        elif "Decide the project list" in prompt:
            answer = {"projects": [{"name": "no slug here"}], "summary": ""}
        else:
            tool(kwargs, "assign", "drive", "--rest")
            answer = {}
        return True, json.dumps({"type": "result", "result": "done\n" + json.dumps(answer)})

    monkeypatch.setattr(bf, "launch_agent", launch)
    own = [bp.ProjectSpec("lab", origin=bp.Origin.RULE.value, project_id="id-lab")]
    plan, _ = br.classify_chunked(folder, _chunk_evidence(), agent=bf.Agent.CLAUDE, existing=[],
                                  work_dir=folder / ".w", own=own)
    assert plan.stats["naming_fallback"] is True
    assert {s.slug for s in plan.projects} == {"lab", "drive"}
