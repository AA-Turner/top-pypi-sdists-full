"""`probe-backfill-plan`: the classifier selects files; it never copies them back.

On 2026-10-25 a classifier asked to echo 10,537 rows "verbatim" retyped two of
200 random-hex directory names wrong, the whole plan was refused, and 52 minutes
of classification were lost. These tests pin the replacement: a selection that
names nothing is refused AT THE CALL, with the nearest real names, and changes
nothing -- so the model fixes it in the same turn -- and the import rebuilds the
plan by replaying the log through the same rules, so a line the agent wrote by
hand is checked like any other.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess

import pytest

from probe.cli import backfill as bf
from probe.cli import backfill_plan_tool as t

ROOT = "/data/llm-env-auditing"
#: Distinct random-looking names, like the 200 attempt directories in the
#: incident (`<24 hex>` each), with the real one the model mistyped at [3].
HEX = [f"br532501ba-f1140f-{hashlib.sha256(str(i).encode()).hexdigest()[:24]}-a1" for i in range(5)]
HEX.insert(3, "br532501ba-f1140f-af72a798d320f35583e08eb9-a1")
ATTEMPTS = "customers/abundant/programsmith/attempts"
FILES = tuple(
    [f"{ATTEMPTS}/{h}/result.json" for h in HEX]
    + ["research/docs/audit.md", "research/eval/run.py", "vendor/deep-swe/tasks/a/solve.sh", "README.md"]
)


def ref(mode=t.Mode.FILE, projects=("envcheck", "auditor-evaluation"), **kw):
    return t.Reference(root=ROOT, mode=mode, files=FILES, projects=projects, **kw)


def apply(r, state, **op):
    return t.apply(r, state, op)


# -- selecting --------------------------------------------------------------


@pytest.mark.parametrize(
    ("selector", "expected"),
    [
        ({"under": ATTEMPTS}, len(HEX)),
        ({"under": f"{ATTEMPTS}/"}, len(HEX)),
        ({"under": f"./{ATTEMPTS}"}, len(HEX)),
        ({"under": f"{ROOT}/{ATTEMPTS}"}, len(HEX)),  # the absolute path the agent reads by
        ({"under": "research"}, 2),
        ({"under": "."}, len(FILES)),
        ({"file": "research/eval/run.py"}, 1),
        ({"under": "research/eval/run.py"}, 1),  # a file named as a directory is still that file
    ],
)
def test_a_selector_files_exactly_the_files_it_names(selector, expected):
    r, state = ref(), t.State()
    apply(r, state, op="assign", project="envcheck", **selector)
    assert len(state.decided) == expected


def test_a_mistyped_random_hex_directory_is_refused_with_the_real_one_nearest():
    """The Tokenless failure: first four hex digits right, the rest invented."""
    r, state = ref(), t.State()
    real = HEX[3]
    typo = real[:22] + "c9eca6da5f88b0f0f3ee-a1"
    with pytest.raises(t.Refused) as refused:
        apply(r, state, op="assign", project="envcheck", under=f"{ATTEMPTS}/{typo}")
    assert f"{ATTEMPTS}/{real}" in str(refused.value)
    assert state.decided == {}  # a refused call changes nothing


@pytest.mark.parametrize(
    ("op", "message"),
    [
        ({"op": "assign", "project": "envcheck", "file": "research"}, "is a directory here"),
        ({"op": "assign", "project": "envcheck", "under": "/etc"}, "is not inside"),
        ({"op": "assign", "project": "envcheck", "under": "research/../../etc"}, "is not inside"),
        ({"op": "assign", "project": "ghost", "under": "research"}, "is not a project here"),
        ({"op": "assign", "project": "envcheck"}, "give exactly one of"),
        ({"op": "assign", "project": "envcheck", "under": "research", "rest": True}, "give exactly one of"),
        ({"op": "leave_out", "under": "vendor"}, "say why"),
        ({"op": "project", "slug": "new"}, "not available in this slice"),
        ({"op": "note", "file": "README.md", "notes": "x"}, "not available in this slice"),
        ({"op": "delete", "under": "research"}, "unknown operation"),
    ],
)
def test_what_is_refused_and_why(op, message):
    r, state = ref(), t.State()
    with pytest.raises(t.Refused, match=message):
        t.apply(r, state, op)
    assert state.decided == {} and state.declared == {}


def test_the_rest_is_only_what_is_still_undecided():
    r, state = ref(), t.State()
    apply(r, state, op="leave_out", under="vendor", why="vendored benchmark")
    apply(r, state, op="assign", project="auditor-evaluation", under="research")
    apply(r, state, op="assign", project="envcheck", rest=True)
    assert state.decided["vendor/deep-swe/tasks/a/solve.sh"].kind is t.Kind.LEFT_OUT
    assert state.decided["research/docs/audit.md"].project == "auditor-evaluation"
    assert state.decided["README.md"].project == "envcheck"


def test_a_later_selection_overrides_and_says_what_moved():
    r, state = ref(), t.State()
    apply(r, state, op="assign", project="envcheck", under="research")
    msg = apply(r, state, op="assign", project="auditor-evaluation", file="research/eval/run.py")
    assert "moved 1 from envcheck" in msg
    assert state.decided["research/docs/audit.md"].project == "envcheck"
    assert state.decided["research/eval/run.py"].project == "auditor-evaluation"


def test_a_low_confidence_selection_is_kept_as_written_for_the_reviewer():
    r, state = ref(), t.State()
    apply(r, state, op="assign", project="envcheck", under=ATTEMPTS, low=True, why="named by neighbours")
    assert state.unsure == [ATTEMPTS]
    assert all(d.low for d in state.decided.values())


def test_a_whole_folder_session_declares_its_projects_before_using_them():
    r, state = ref(mode=t.Mode.CLASSIFY, projects=("existing",)), t.State()
    with pytest.raises(t.Refused, match="Declare it first"):
        apply(r, state, op="assign", project="vision", under="research")
    apply(r, state, op="project", slug="vision", name="Vision", description="d", tags=["x"])
    apply(r, state, op="assign", project="vision", under="research")
    apply(r, state, op="assign", project="existing", rest=True)
    assert state.declared["vision"]["name"] == "Vision"
    with pytest.raises(t.Refused, match="usable slug"):
        apply(r, state, op="project", slug="Not A Slug")


def test_a_note_is_capped_so_it_can_never_cost_its_file():
    r = t.Reference(root=ROOT, mode=t.Mode.NOTE, files=FILES)
    state = t.State()
    apply(r, state, op="note", file="README.md", notes="the entry point")
    with pytest.raises(t.Refused, match="keep it under"):
        apply(r, state, op="note", file="README.md", notes="x" * (t.NOTE_MAX_CHARS + 1))
    with pytest.raises(t.Refused, match="not available"):
        apply(r, state, op="assign", project="envcheck", file="README.md")
    assert state.notes == {"README.md": "the entry point"}


# -- replay is the authority ---------------------------------------------------


def test_replay_checks_every_line_including_ones_the_agent_wrote_by_hand():
    r = ref()
    lines = [
        json.dumps({"op": "assign", "project": "envcheck", "under": ATTEMPTS}),
        # What the old contract produced: a path copied back wrong.
        json.dumps({"op": "assign", "project": "envcheck", "file": f"{ATTEMPTS}/{HEX[0][:-4]}zz-a1/result.json"}),
        json.dumps({"op": "assign", "project": "invented", "under": "research"}),
        "not json",
        json.dumps({"op": "leave_out", "under": "vendor", "why": "vendored"}),
    ]
    state = t.replay(r, lines)
    assert state.invalid == 3 and state.accepted == 2
    assert len(state.decided) == len(HEX) + 1
    assert "research/docs/audit.md" not in state.decided


def test_a_revision_starts_from_the_plan_it_corrects():
    r = ref(mode=t.Mode.REVISE, seed={
        "research/docs/audit.md": {"kind": "assigned", "project": "envcheck"},
        "README.md": {"kind": "left_out", "why": "readme"},
        "not/walked.py": {"kind": "assigned", "project": "envcheck"},  # dropped, never invented
    })
    state = t.replay(r, [json.dumps({"op": "assign", "project": "auditor-evaluation", "under": "research"})])
    assert state.decided["research/docs/audit.md"].project == "auditor-evaluation"
    assert state.decided["README.md"].kind is t.Kind.LEFT_OUT
    assert "not/walked.py" not in state.decided and state.accepted == 1


# -- what the agent reads ------------------------------------------------------


def test_status_names_what_is_left_grouped_and_bounded():
    many = tuple(f"d{i}/f{j}.py" for i in range(200) for j in range(2))
    r = t.Reference(root=ROOT, mode=t.Mode.FILE, files=many, projects=("p",))
    state = t.State()
    apply(r, state, op="assign", project="p", under="d0")
    text = t.status(r, state)
    assert text.startswith("2 of 400 files decided (p 2).")
    assert "398 undecided:" in text
    assert len(text.splitlines()) <= t.STATUS_MAX_LINES + 4
    apply(r, state, op="assign", project="p", rest=True)
    assert "0 undecided" in t.status(r, state)


def test_show_lists_a_directory_with_where_each_part_went():
    r, state = ref(), t.State()
    apply(r, state, op="assign", project="envcheck", under=ATTEMPTS)
    text = t.show(r, state, "customers/abundant/programsmith")
    assert "attempts/  (6)  -> envcheck" in text


# -- the command, through the launcher the import puts on PATH -----------------


def _launch(tmp_path, r):
    tool = bf.PlanTool(ref_dir=tmp_path / "ref", log=tmp_path / "work" / "plan" / "s" / "decisions.jsonl")
    r.write(tool.ref_dir)
    tool.log.parent.mkdir(parents=True)
    return tool


def _run(bin_dir, *args, cwd):
    proc = subprocess.run([f"{bin_dir}/{bf.PLAN_TOOL_COMMAND}", *args], capture_output=True,
                          text=True, cwd=cwd, timeout=60)
    return proc.returncode, proc.stdout


def test_the_launcher_runs_the_tool_and_only_accepted_calls_reach_the_log(tmp_path):
    tool = _launch(tmp_path, ref())
    work = tool.log.parents[2]
    with bf.plan_tool_launcher(tool) as bin_dir:
        code, out = _run(bin_dir, "assign", "envcheck", "--under", f"{ATTEMPTS}/{HEX[2][:-6]}xxxx-a1", cwd=work)
        assert code == 1 and "refused" in out and HEX[2] in out
        code, out = _run(bin_dir, "assign", "envcheck", "--under", ATTEMPTS, cwd=work)
        assert code == 0 and f"envcheck: {len(HEX)} files" in out
        (work / "more.jsonl").write_text("\n".join([
            json.dumps({"op": "leave_out", "under": "vendor", "why": "vendored"}),
            json.dumps({"op": "assign", "project": "nope", "rest": True}),
        ]))
        code, out = _run(bin_dir, "apply", "--from", "more.jsonl", cwd=work)
        assert code == 1 and "line 1: left out" in out and "line 2: refused" in out
        code, out = _run(bin_dir, "status", cwd=work)
        assert code == 0 and "3 undecided" in out
    logged = [json.loads(line)["op"] for line in tool.log.read_text().splitlines()]
    assert logged == ["assign", "leave_out"]
    assert t.refused_count(tool.log) == 2


def test_the_launcher_needs_no_environment_from_the_agent(tmp_path):
    """Codex filters what reaches its shell; the state is baked into the script."""
    tool = _launch(tmp_path, ref())
    with bf.plan_tool_launcher(tool) as bin_dir:
        proc = subprocess.run([f"{bin_dir}/{bf.PLAN_TOOL_COMMAND}", "status"], capture_output=True,
                              text=True, env={"PATH": "/usr/bin:/bin"}, timeout=60)
    assert proc.returncode == 0 and f"0 of {len(FILES)} files decided" in proc.stdout


def test_two_sessions_launched_side_by_side_keep_their_own_state(tmp_path):
    a = _launch(tmp_path / "a", ref())
    b = _launch(tmp_path / "b", ref(projects=("other",)))
    with bf.plan_tool_launcher(a) as bin_a, bf.plan_tool_launcher(b) as bin_b:
        assert _run(bin_a, "assign", "envcheck", "--rest", cwd=tmp_path)[0] == 0
        assert _run(bin_b, "assign", "envcheck", "--rest", cwd=tmp_path)[0] == 1
    assert a.log.exists() and not b.log.exists()


def test_outside_a_classifier_session_the_tool_says_so():
    out = []

    class Sink:
        def write(self, text):
            out.append(text)

    assert t.main(["status"], out=Sink()) == 2
    assert "only runs inside" in "".join(out)


def test_a_relative_work_dir_still_reaches_its_state_from_the_agents_cwd(tmp_path, monkeypatch):
    """The agent's shell runs in its work dir; state baked in relative to the
    importer's cwd was not found there (live smoke, 2026-10-25)."""
    monkeypatch.chdir(tmp_path)
    tool = bf.PlanTool(ref_dir=pathlib.Path("work.plan-ref/s"), log=pathlib.Path("work/plan/s/decisions.jsonl"))
    ref().write(tool.ref_dir)
    tool.log.parent.mkdir(parents=True)
    with bf.plan_tool_launcher(tool) as bin_dir:
        code, out = _run(bin_dir, "status", cwd=tmp_path / "work")
    assert code == 0 and "files decided" in out


def test_names_differing_only_by_a_backslash_or_trailing_space_stay_apart():
    """Outside review: folding `a\\b.py` into `a/b.py` selected the wrong file."""
    r = t.Reference(root=ROOT, mode=t.Mode.FILE, files=("a\\b.py", "a/b.py", "x.py", "x.py "), projects=("p",))
    state = t.State()
    apply(r, state, op="assign", project="p", file="a/b.py")
    apply(r, state, op="assign", project="p", file="x.py ")
    assert set(state.decided) == {"a/b.py", "x.py "}
