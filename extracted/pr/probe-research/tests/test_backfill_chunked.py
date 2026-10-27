"""Classifying a folder too big for one prompt.

The whole evidence set is ONE message, so `--autocompact` cannot save it -- it
compacts across turns and there are none yet. Past the window the request is
rejected outright, after the walk has already been paid for.

The chunked route splits it so that NO CHUNK EVER NEEDS ANOTHER CHUNK'S DETAIL.
That constraint is the design, and it is what these tests are really about:
feeding the agent slices in sequence and letting compaction absorb the overflow
would also "work", and would quietly place early files against evidence and
later ones against a summary of it, with nothing at the review gate able to tell
which was which.

  SURVEY  each slice describes itself. Local only.
  NAME    one pass over those summaries. The only global step.
  ASSIGN  each slice maps its own rows onto the fixed list. Independent.
"""

from __future__ import annotations

import json

import pytest
from backfill_plan_agent import filing
from backfill_test_client import ScopedClient

from probe.cli import backfill as bf
from probe.cli import backfill_evidence as ev
from probe.cli import backfill_plan as plan_mod
from probe.cli import backfill_prompts as bp
from probe.cli import backfill_run as br


@pytest.fixture
def folder(tmp_path):
    root = tmp_path / "drive"
    root.mkdir()
    (root / "a.py").write_text("import torch\n")
    return root


@pytest.fixture(autouse=True)
def agents_installed(monkeypatch):
    monkeypatch.setattr(bf, "which_agent", lambda agent: f"/bin/{agent.value}")


def _evidence(rows: int, sample_len: int = 600) -> ev.Evidence:
    """Evidence with a known number of sampled rows.

    Every file carries a sample, so `to_jsonl` emits one row each and none get
    rolled up -- the row count is the knob these tests turn.
    """
    files = [
        ev.FileEvidence(
            path=f"/drive/f{i}.py",
            size=100,
            mtime=0,
            tier=ev.Tier.EVIDENCE,
            sample="x" * sample_len,
        )
        for i in range(rows)
    ]
    return ev.Evidence(
        root="/drive",
        files=files,
        clusters=[],
        sampled_files=rows,
        sampled_bytes=rows * sample_len,
    )


def _envelope(payload: dict) -> str:
    """The agent's answer as it really arrives: JSON inside a stream envelope."""
    return json.dumps({"type": "result", "result": f"done\n{json.dumps(payload)}"})


class _Agent:
    """Answers each pass by the shape it was asked for."""

    def __init__(self, projects=("alpha", "beta"), fail_on=None):
        self.projects = list(projects)
        self.fail_on = fail_on  # "survey" | "name" | "assign"
        self.prompts: list[str] = []

    def __call__(self, folder, prompt, **kw):
        self.prompts.append(prompt)
        if "what lines of work one slice" in prompt:
            if self.fail_on == "survey":
                return False, "died"
            return True, _envelope(
                {"findings": [{"work": "training", "evidence": [], "approx_files": 3}], "notes": ""}
            )
        if ("Decide which project each file" in prompt or "Decide the project list" in prompt):
            if self.fail_on == "name":
                return False, "died"
            return True, _envelope(
                {
                    "projects": [{"slug": s, "name": s, "description": "d"} for s in self.projects],
                    "summary": "a folder",
                }
            )
        if "already decided" in prompt:
            if self.fail_on == "assign":
                return False, "died"
            rows = [json.loads(ln) for ln in prompt.splitlines() if ln.startswith('{"path"')]
            return True, _envelope(
                {
                    "assignments": [
                        {
                            "path": r["path"],
                            "project": self.projects[0],
                            "confidence": "high",
                            "why": "w",
                        }
                        for r in rows
                    ],
                    "unsure": [],
                }
            )
        raise AssertionError(f"unrecognised prompt:\n{prompt[:300]}")


# -- the dispatch ------------------------------------------------------------


def test_a_folder_that_fits_still_goes_to_one_agent(folder, monkeypatch):
    """Single-shot is the BETTER classification -- every file judged against
    every other, in one decision -- so chunking must stay a fallback."""
    calls: list[str] = []

    def fake(folder_, prompt, **kw):
        calls.append(prompt)
        return True, _envelope(
            {"projects": [{"slug": "alpha", "name": "a"}],
             "assignments": [{"path": ".", "project": "alpha"}], "summary": "s"}
        )

    monkeypatch.setattr(bf, "launch_agent", filing(fake))
    br.classify(folder, _evidence(3), agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w")
    assert len(calls) == 1
    assert "Decide which project each file" in calls[0]


def test_a_folder_too_big_for_one_prompt_is_chunked(folder, monkeypatch):
    agent = _Agent()
    monkeypatch.setattr(bf, "launch_agent", filing(agent))
    big = _evidence(600)
    assert ev.estimate_tokens(ev.to_jsonl(big)) > ev.SINGLE_SHOT_TOKEN_BUDGET

    plan, tail, session = br.classify(
        folder, big, agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w"
    )
    assert plan is not None
    assert "slices" in tail
    # No session: the chunked route runs many, and resuming "the" one would
    # resume whichever happened to be last.
    assert session is None


def test_every_row_survives_the_round_trip(folder, monkeypatch):
    """A classification silently missing files is the one outcome worth failing
    over -- `resolve` would report them as unassigned and the plan untrusted."""
    agent = _Agent()
    monkeypatch.setattr(bf, "launch_agent", filing(agent))
    big = _evidence(600)
    rows = [json.loads(ln)["path"] for ln in ev.to_jsonl(big).splitlines()]

    plan, _, _ = br.classify(
        folder, big, agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w"
    )
    assert sorted(a.path for a in plan.assignments) == sorted(rows)


# -- the constraint the design exists for ------------------------------------


def test_no_survey_slice_is_told_about_another_slice(folder, monkeypatch):
    """Local only. A slice that could see its siblings would be back to needing
    the whole folder in context, which is the thing that does not fit."""
    agent = _Agent()
    monkeypatch.setattr(bf, "launch_agent", filing(agent))
    br.classify(folder, _evidence(600), agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w")

    surveys = [p for p in agent.prompts if "what lines of work one slice" in p]
    assert len(surveys) > 1, "the evidence did not actually split"
    for prompt in surveys:
        assert "Do not name projects" in prompt
        assert "not all of it" in prompt


def test_the_assign_pass_is_given_the_projects_and_cannot_invent_one(folder, monkeypatch):
    """This is what makes assignment independent: the global decision is
    already made, so a slice needs nothing from its siblings."""
    agent = _Agent(projects=("alpha", "beta"))
    monkeypatch.setattr(bf, "launch_agent", filing(agent))
    br.classify(folder, _evidence(600), agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w")

    assigns = [p for p in agent.prompts if "already decided" in p]
    assert assigns
    for prompt in assigns:
        assert "alpha" in prompt and "beta" in prompt
        assert "do not invent or rename one" in prompt


def test_an_invented_project_is_refused_at_the_call_and_its_files_wait(folder, monkeypatch):
    """Told the project list is closed, an agent that files into a slug of its
    own is refused by the tool -- nothing lands in a project nobody named. A
    slice that then decided under 80% of its files counts as failed: its
    undecided files are excluded and named, not guessed from neighbours."""

    class _Inventing(_Agent):
        def __call__(self, folder_, prompt, **kw):
            if "already decided" in prompt:
                rows = [json.loads(ln) for ln in prompt.splitlines() if ln.startswith('{"path"')]
                return True, _envelope({"assignments": [
                    {"path": r["path"], "project": "made-up" if i % 2 else "alpha"}
                    for i, r in enumerate(rows)
                ]})
            return super().__call__(folder_, prompt, **kw)

    monkeypatch.setattr(bf, "launch_agent", filing(_Inventing()))
    big = _evidence(600)
    plan, _, _ = br.classify(
        folder, big, agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w"
    )
    rows = len(ev.to_jsonl(big).splitlines())
    assert all(a.project == "alpha" for a in plan.assignments)
    assert len(plan.assignments) + len(plan.excluded) == rows
    assert plan.excluded and plan.stats["refused_selectors"] >= len(plan.excluded)
    assert plan.stats["failed_sessions"] > 0


# -- what failing costs --------------------------------------------------------


@pytest.mark.parametrize("stage", ["survey", "assign"])
def test_a_pass_that_fails_everywhere_returns_no_plan(folder, monkeypatch, stage):
    """No findings, or no slice that filed anything: there is nothing to review.
    (One failed ASSIGN slice costs only its own files; see
    `test_backfill_classification_cache`. A failed NAME pass falls back to one
    project; see below.)"""
    monkeypatch.setattr(bf, "launch_agent", filing(_Agent(fail_on=stage)))
    plan, tail, _ = br.classify(
        folder, _evidence(600), agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w"
    )
    assert plan is None
    assert tail


class _NamesNothing(_Agent):
    def __call__(self, folder_, prompt, **kw):
        if ("Decide which project each file" in prompt or "Decide the project list" in prompt):
            self.prompts.append(prompt)
            return True, _envelope({"projects": [], "summary": ""})
        return super().__call__(folder_, prompt, **kw)


@pytest.mark.parametrize("naming", ["died", "named nothing"])
def test_a_naming_pass_that_fails_files_everything_into_one_folder_project(
    folder, monkeypatch, naming
):
    """Naming is the one global step, so its failure used to throw away every
    finished survey. Now the folder goes into one project named for it, and the
    review screen says so: splitting it is the reviewer's call, not a re-run."""
    fallback = br._folder_project(folder)
    assert fallback["slug"] == "drive"
    fake = (_Agent(projects=(fallback["slug"],), fail_on="name") if naming == "died"
            else _NamesNothing(projects=(fallback["slug"],)))
    monkeypatch.setattr(bf, "launch_agent", filing(fake))
    evidence = _evidence(600)
    plan, _tail, _ = br.classify(
        folder, evidence, agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w"
    )
    assert plan is not None
    assert [p.slug for p in plan.projects] == ["drive"]
    assert len(plan.assignments) == 600 and not plan.excluded
    assert plan.stats["naming_fallback"] is True
    assigned, disc = plan_mod.resolve(evidence, plan)
    text = "\n".join(br.describe_plan(evidence, plan, assigned, disc))
    assert "named for the folder" in text


def test_folder_project_slug_is_always_valid(tmp_path):
    for name, slug in [("My Runs (2024)", "my-runs-2024"), ("___", "imported-research"),
                       ("x" * 100, "x" * 56),
                       ("3f2a9c1e5b7d4f60a1b2c3d4e5f60718", "folder-3f2a9c1e5b7d4f60a1b2c3d4e5f60718"),
                       ("3F2A9C1E-5B7D-4F60-A1B2-C3D4E5F60718",
                        "folder-3f2a9c1e-5b7d-4f60-a1b2-c3d4e5f60718")]:
        assert br._folder_project(tmp_path / name)["slug"] == slug


# -- the chunker itself ------------------------------------------------------


def test_chunks_stay_under_the_budget():
    jsonl = "\n".join(json.dumps({"path": f"f{i}.py", "sample": "x" * 600}) for i in range(500))
    for chunk in ev.chunk_lines(jsonl):
        assert ev.estimate_tokens("\n".join(chunk)) <= ev.CHUNK_TOKEN_BUDGET


def test_row_count_is_capped_independently_of_tokens():
    """The assign pass emits one object per row, so a chunk of tiny rollup rows
    can fit the INPUT budget and still ask for more output than the model
    produces -- and a truncated final message loses assignments silently."""
    jsonl = "\n".join(json.dumps({"dir": f"d{i}"}) for i in range(5_000))
    chunks = ev.chunk_lines(jsonl)
    assert all(len(c) <= ev.CHUNK_MAX_ROWS for c in chunks)
    assert len(chunks) >= 10


def test_no_row_is_lost_or_split_by_chunking():
    jsonl = "\n".join(json.dumps({"path": f"f{i}.py"}) for i in range(1_000))
    flat = [ln for c in ev.chunk_lines(jsonl) for ln in c]
    assert flat == jsonl.splitlines()


def test_a_row_bigger_than_the_budget_still_gets_through():
    """Half a JSON object is not evidence. An oversized row gets its own chunk
    rather than being dropped or cut."""
    jsonl = json.dumps({"path": "huge.py", "sample": "x" * 400_000})
    chunks = ev.chunk_lines(jsonl)
    assert len(chunks) == 1 and chunks[0] == [jsonl]


def test_the_estimate_runs_high_not_low():
    """Guessing low is the expensive direction: it sends a prompt the model
    rejects after the walk has already been paid for."""
    # JSON tokenises worse than prose, so the estimate must exceed chars/4.
    text = json.dumps({"path": "a/b/c.py", "sample": "def f(): return 1"}) * 100
    assert ev.estimate_tokens(text) > len(text) / 4


# -- the two regressions the review caught ----------------------------------


def test_a_rollup_row_answered_by_dir_is_not_dropped(folder, monkeypatch):
    """The assign prompt tells the agent to use a rollup's "dir" value verbatim,
    so it answers with that key -- and accepting only "path" dropped every one
    of them. `backfill_plan._plan_from` already carries this exact fix, with a
    comment saying it cost "thousands of files ... with nothing reported"."""

    class _ByDir(_Agent):
        def __call__(self, folder_, prompt, **kw):
            if "already decided" in prompt:
                rows = [json.loads(ln) for ln in prompt.splitlines() if ln.startswith('{"path"')]
                return True, _envelope(
                    {
                        # The agent echoes `dir`, as the prompt taught it to.
                        "assignments": [
                            {"dir": r["path"], "project": self.projects[0]} for r in rows
                        ],
                        "unsure": [],
                    }
                )
            return super().__call__(folder_, prompt, **kw)

    monkeypatch.setattr(bf, "launch_agent", filing(_ByDir()))
    big = _evidence(600)
    plan, _, _ = br.classify(
        folder, big, agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w"
    )
    assert plan is not None
    assert len(plan.assignments) == len(ev.to_jsonl(big).splitlines())


def test_a_plan_that_places_nothing_is_a_failure_not_an_empty_success(folder, monkeypatch):
    """Without this, an all-empty result is not an error: resolve returns an
    empty map, nothing is unknown or duplicated so the plan reads trustworthy,
    pack yields no units, and the run reports "0 queued · 0/0 units done" as a
    success. A green no-op is the answer a reader stops investigating."""

    class _Empty(_Agent):
        def __call__(self, folder_, prompt, **kw):
            if "already decided" in prompt:
                return True, _envelope({"assignments": [], "unsure": ["x"]})
            return super().__call__(folder_, prompt, **kw)

    monkeypatch.setattr(bf, "launch_agent", filing(_Empty()))
    plan, tail, _ = br.classify(
        folder, _evidence(600), agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w"
    )
    assert plan is None
    assert "placed" in tail


def test_a_low_confidence_selection_reaches_the_reviewer_as_written(folder, monkeypatch):
    """`--low` on a directory reads as that directory on the review screen, not
    as every file under it."""

    class _Unsure(_Agent):
        def __call__(self, folder_, prompt, **kw):
            if "already decided" in prompt:
                return True, _envelope({"assignments": [
                    {"path": ".", "project": "alpha", "confidence": "low", "why": "guess"}
                ]})
            return super().__call__(folder_, prompt, **kw)

    monkeypatch.setattr(bf, "launch_agent", filing(_Unsure()))
    plan, _, _ = br.classify(
        folder, _evidence(600), agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w"
    )
    assert plan.assignments and all(a.confidence == "low" for a in plan.assignments)
    assert plan.unsure == ["."]


# -- the review follow-ups ---------------------------------------------------


def test_a_rollup_travels_with_its_own_directory_not_at_the_end():
    """Emitting all sampled rows first and every rollup after them is harmless
    in one prompt and ruinous once sliced: sampling stops at
    SAMPLE_BUDGET_FILES, so on a folder big enough to chunk every `dir` row
    lands in a later slice holding no sample text at all -- and is then asked to
    place tail files "with their neighbours" while holding no neighbours."""
    files = [
        ev.FileEvidence(
            path=f"/drive/{area}/src/f{i}.py", size=10, mtime=0, tier=ev.Tier.EVIDENCE, sample="x"
        )
        for area in ("alpha", "beta")
        for i in range(3)
    ] + [
        ev.FileEvidence(path=f"/drive/{area}/ckpt/step_{i}.pt", size=10, mtime=0, tier=ev.Tier.TAIL)
        for area in ("alpha", "beta")
        for i in range(4)
    ]
    e = ev.Evidence(root="/drive", files=files, clusters=[], sampled_files=6, sampled_bytes=6)
    rows = [json.loads(ln) for ln in ev.to_jsonl(e).splitlines()]

    # Every rollup sits AMONG rows sharing its own top-level directory -- on
    # either side, since a directory's rollup may sort before or after its
    # sampled siblings depending on the names. What must not happen is every
    # rollup ending up in one block at the end.
    for i, row in enumerate(rows):
        if "dir" not in row:
            continue
        area = row["dir"].split("/")[0]
        window = rows[max(0, i - 4) : i] + rows[i + 1 : i + 5]
        assert any(n.get("path", "").startswith(area + "/") for n in window), (
            f"rollup {row['dir']} has no sampled neighbour from {area}"
        )
    # And they are not all bunched at the end.
    dir_positions = [i for i, r in enumerate(rows) if "dir" in r]
    assert min(dir_positions) < len(rows) - len(dir_positions), (
        "every rollup landed in a trailing block"
    )


def test_the_truncation_caveat_reaches_the_chunked_prompts(folder, monkeypatch):
    """The chunked route fires on exactly the folders that blow the 600-file
    sample cap, so `sample_budget_hit` is true in essentially every chunked run
    -- and the agent was never told."""
    agent = _Agent()
    monkeypatch.setattr(bf, "launch_agent", filing(agent))
    big = _evidence(600)
    big.sample_budget_hit = True
    br.classify(folder, big, agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w")

    # BOTH passes, checked separately. Asserting only that "some chunked
    # prompt" carries it let the survey pass lose it silently while the assign
    # pass kept it -- and the survey pass is the one deciding what the folder
    # even contains.
    surveys = [p for p in agent.prompts if "what lines of work one slice" in p]
    assigns = [p for p in agent.prompts if "already decided" in p]
    assert surveys and assigns
    assert all("sample budget ran out" in p for p in surveys), "survey pass"
    assert all("sample budget ran out" in p for p in assigns), "assign pass"


def test_a_failed_pass_reports_what_the_agent_actually_said(folder, monkeypatch):
    """Substituting "slice 1 of 3 could not be read" hid every message worth
    acting on -- "`claude` is not on PATH", the confinement refusal, a
    timeout -- behind a sentence naming only where it happened."""

    def dying(folder_, prompt, **kw):
        return False, "`claude` is not on PATH — install Claude Code"

    monkeypatch.setattr(bf, "launch_agent", filing(dying))
    _, tail, _ = br.classify(
        folder, _evidence(600), agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w"
    )
    assert "not on PATH" in tail


def test_a_transient_pass_failure_is_retried(folder, monkeypatch):
    """Losing a forty-slice run to one dropped connection, after an hour of
    successful slices, is the expensive outcome."""
    attempts: list[int] = []

    class _Flaky(_Agent):
        def __call__(self, folder_, prompt, **kw):
            if "what lines of work one slice" in prompt:
                attempts.append(1)
                if len(attempts) == 1:
                    return False, "connection reset"
            return super().__call__(folder_, prompt, **kw)

    monkeypatch.setattr(bf, "launch_agent", filing(_Flaky()))
    plan, _, _ = br.classify(
        folder, _evidence(600), agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w"
    )
    assert plan is not None, "one transient failure killed the whole run"
    assert len(attempts) > 1


def test_slice_summaries_are_dropped_whole_never_cut_mid_object():
    """A fixed character slice lands inside an object: the naming pass then
    sees a malformed tail, silently never learns what the last slices held, and
    names projects those slices' files are afterwards forced into."""
    findings = [{"slice": i, "work": "w" * 5_000, "evidence": []} for i in range(200)]
    text, dropped = br._fit_findings(findings)
    assert dropped > 0, "this fixture was meant to overflow"
    # VALID JSON is the property the character slice broke: it cut inside an
    # object, so the naming pass saw a malformed tail and simply never learned
    # what the last slices held.
    kept = json.loads(text)
    assert len(kept) == len(findings) - dropped
    # Every entry that survived is intact, not a prefix of itself.
    assert all(len(k["work"]) == 5_000 for k in kept)
    assert [k["slice"] for k in kept] == list(range(len(kept)))


def test_the_naming_pass_carries_a_reviewer_correction():
    prompt = bp.name_projects(
        root="/r", findings_json="[]", own=[], feedback="lockfiles are not research"
    )
    assert "lockfiles are not research" in prompt
    assert "outranks" in prompt


def test_a_correction_on_a_chunked_folder_is_one_session_not_every_slice(folder, monkeypatch):
    """A correction used to re-run every slice of a chunked folder -- another
    hour on a 144k-file drive. It is now one session, started from the plan the
    reviewer read, whichever route classified it."""
    monkeypatch.setattr(bf, "launch_agent", filing(_Agent()))
    monkeypatch.setattr(br, "run_units", lambda *a, **k: [])
    monkeypatch.setattr(br, "enqueue_manifests", lambda *a, **k: (0, []))
    # `enrich`, not `gather`: `_execute` runs the two phases separately now so
    # the early exits can skip sampling, and it never calls `gather` at all.
    monkeypatch.setattr(br.evidence_mod, "enrich", lambda f, records: _evidence(600))

    revises: list = []
    monkeypatch.setattr(br, "revise", lambda *a, **k: revises.append(k["plan"]) or (None, "", None))
    chunked: list = []
    real = br.classify_chunked
    monkeypatch.setattr(
        br, "classify_chunked", lambda *a, **k: chunked.append(k.get("feedback")) or real(*a, **k)
    )

    answers = iter(["revise", "import"])
    # `tui` is imported inside `execute`, so the module itself is patched.
    from probe.cli import tui

    monkeypatch.setattr(tui, "page", lambda lines, prompt=None: "")
    monkeypatch.setattr(tui, "review", lambda *a, **kw: next(answers))
    monkeypatch.setattr(tui, "text", lambda *a, **kw: "merge the two projects")
    monkeypatch.setattr(tui, "interactive", lambda: True)

    br.execute(client_factory=ScopedClient, folder=folder, agent=bf.Agent.CLAUDE)
    assert len(chunked) == 1, "only the first classification ran the slices"
    assert len(revises) == 1 and revises[0].assignments, "the correction starts from the plan"


def test_tags_survive_the_chunked_route(folder, monkeypatch):
    """`name_projects` asks for them and `_plan_from` parses them on the other
    route; dropping them made the two paths produce different Plans from the
    same answer."""

    class _Tagged(_Agent):
        def __call__(self, folder_, prompt, **kw):
            if ("Decide which project each file" in prompt or "Decide the project list" in prompt):
                return True, _envelope(
                    {
                        "projects": [
                            {
                                "slug": "alpha",
                                "name": "a",
                                "description": "d",
                                "tags": ["proteins", "rl"],
                            }
                        ],
                        "summary": "s",
                    }
                )
            return super().__call__(folder_, prompt, **kw)

    monkeypatch.setattr(bf, "launch_agent", filing(_Tagged(projects=("alpha",))))
    plan, _, _ = br.classify(
        folder, _evidence(600), agent=bf.Agent.CLAUDE, existing=[], work_dir=folder / ".w"
    )
    assert plan.projects[0].tags == ["proteins", "rl"]


# -- the boundaries the outside review found -----------------------------------


def _tree(folder):
    """Two directories, each a sampled file plus a rollup of checkpoints."""
    files = []
    for area in ("alpha", "beta"):
        files.append(ev.FileEvidence(path=f"{folder}/{area}/train.py", size=10, mtime=0,
                                     tier=ev.Tier.EVIDENCE, sample="train()"))
        files += [ev.FileEvidence(path=f"{folder}/{area}/step_{i}.pt", size=10, mtime=0,
                                  tier=ev.Tier.TAIL) for i in range(3)]
    return ev.Evidence(root=str(folder), files=files, clusters=[], sampled_files=2, sampled_bytes=14)


def _one_row_per_slice(monkeypatch):
    monkeypatch.setattr(ev, "needs_chunking", lambda _: True)
    monkeypatch.setattr(ev, "chunk_lines", lambda jsonl: [[line] for line in jsonl.splitlines()])


class _Named(_Agent):
    def __init__(self, filer, **kw):
        super().__init__(projects=("alpha", "beta"), **kw)
        self.filer = filer

    def __call__(self, folder_, prompt, **kw):
        if "already decided" in prompt:
            return self.filer(prompt, kw)
        return super().__call__(folder_, prompt, **kw)


def test_a_failed_slices_file_is_never_claimed_by_its_directorys_rollup(folder, monkeypatch):
    """The sampled `alpha/train.py` and the rollup of `alpha/` sit in different
    slices. When the sampled file's slice fails, `--under alpha` in the rollup's
    slice must not reach it: a slice owns its rows' files and no others, and a
    failed slice's files are excluded, not inherited."""
    _one_row_per_slice(monkeypatch)

    def filer(prompt, kw):
        rows = [json.loads(ln) for ln in prompt.splitlines() if ln.startswith('{"')]
        if any(r.get("path") == "alpha/train.py" for r in rows):
            return False, "connection lost"
        return True, _envelope({"assignments": [{"path": r.get("path") or r.get("dir"),
                                                  "project": "alpha"} for r in rows]})

    monkeypatch.setattr(bf, "launch_agent", filing(_Named(filer)))
    plan, _, _ = br.classify(folder, _tree(folder), agent=bf.Agent.CLAUDE, existing=[],
                             work_dir=folder / ".w")
    assert plan.excluded == ["alpha/train.py"]
    assigned, _ = __import__("probe.cli.backfill_plan", fromlist=["resolve"]).resolve(_tree(folder), plan)
    assert "alpha/train.py" not in assigned
    assert {p for p in assigned if p.startswith("alpha/")} == {f"alpha/step_{i}.pt" for i in range(3)}


def test_an_agent_that_edits_its_reference_copy_widens_nothing(folder, monkeypatch):
    """The reference beside the work dir is for the agent's own feedback; the
    import checks the log against the copy it holds in memory."""
    from backfill_plan_agent import tool

    def filer(prompt, kw):
        script = (__import__("pathlib").Path(kw["path_prepend"]) / bf.PLAN_TOOL_COMMAND).read_text()
        ref_dir = script.split("PROBE_PLAN_REF=", 1)[1].split(";", 1)[0].strip("'")
        owned = __import__("pathlib").Path(ref_dir) / "owned.json"
        data = json.loads(owned.read_text())
        data["projects"].append("evil")
        owned.write_text(json.dumps(data))
        tool(kw, "assign", "evil", "--rest")  # the tool, reading the edited copy, accepts it
        return True, _envelope({"summary": "done"})

    monkeypatch.setattr(bf, "launch_agent", _Named(filer))
    plan, _, _ = br.classify(folder, _tree(folder), agent=bf.Agent.CLAUDE, existing=[],
                             work_dir=folder / ".w")
    assert plan is None or all(a.project != "evil" for a in plan.assignments)


def test_one_unsampled_file_inside_a_rollup_can_be_filed_on_its_own(folder, monkeypatch):
    """Every walked file stays addressable: `--file` reaches a checkpoint the
    prompt only showed as part of its directory's rollup."""

    def filer(prompt, kw):
        from backfill_plan_agent import tool

        tool(kw, "assign", "alpha", "--rest")
        tool(kw, "assign", "beta", "--file", "alpha/step_1.pt")
        return True, _envelope({"summary": "done"})

    monkeypatch.setattr(bf, "launch_agent", _Named(filer))
    monkeypatch.setattr(ev, "chunk_lines", lambda jsonl: [jsonl.splitlines()])
    monkeypatch.setattr(ev, "needs_chunking", lambda _: True)
    plan, _, _ = br.classify(folder, _tree(folder), agent=bf.Agent.CLAUDE, existing=[],
                             work_dir=folder / ".w")
    where = {a.path: a.project for a in plan.assignments}
    assert where["alpha/step_1.pt"] == "beta" and where["alpha/step_0.pt"] == "alpha"


def test_a_correction_keeps_what_the_reviewer_saw_inherited(folder, monkeypatch):
    """Outside review: seeding a correction with only the explicit assignments let
    an untouched checkpoint, shown under `alpha` by inheritance, re-inherit into
    another project once its directory's scripts moved."""
    from backfill_plan_agent import tool

    from probe.cli import backfill_plan as plans

    e = _tree(folder)
    plan = plans.Plan([plans.ProjectSpec("alpha"), plans.ProjectSpec("beta")], [
        plans.Assignment("alpha/train.py", "alpha"),
        plans.Assignment("beta/train.py", "beta"),
        *[plans.Assignment(f"beta/step_{i}.pt", "beta") for i in range(3)],
    ])
    shown, _ = plans.resolve(e, plan)
    assert shown["alpha/step_0.pt"] == "alpha"  # inherited

    def correct(folder_, prompt, **kw):
        tool(kw, "assign", "beta", "--file", "alpha/train.py")
        return True, _envelope({"summary": "moved the script"})

    monkeypatch.setattr(bf, "launch_agent", correct)
    revised, _, _ = br.revise(folder, e, "move alpha/train.py to beta", agent=bf.Agent.CODEX,
                              session_id=None, work_dir=folder / ".w", plan=plan)
    after, _ = plans.resolve(e, revised)
    assert after["alpha/train.py"] == "beta"
    assert {after[f"alpha/step_{i}.pt"] for i in range(3)} == {"alpha"}


def test_a_correction_can_rename_a_project(folder, monkeypatch):
    from backfill_plan_agent import tool

    from probe.cli import backfill_plan as plans

    e = _tree(folder)
    plan = plans.Plan([plans.ProjectSpec("alpha", name="Old name")], [plans.Assignment("alpha/train.py", "alpha")])

    def rename(folder_, prompt, **kw):
        tool(kw, "project", "alpha", "--name", "Corrected name")
        return True, _envelope({"summary": "renamed"})

    monkeypatch.setattr(bf, "launch_agent", rename)
    revised, _, _ = br.revise(folder, e, "rename alpha", agent=bf.Agent.CODEX,
                              session_id=None, work_dir=folder / ".w", plan=plan)
    assert [p.name for p in revised.projects if p.slug == "alpha"] == ["Corrected name"]
