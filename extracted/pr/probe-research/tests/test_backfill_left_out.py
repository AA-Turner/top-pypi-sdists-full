"""The classifier may leave rows out as not research, with a why.

A wizard import of a product monorepo (2026-10-16) uploaded a Rails + React web
app, a TypeScript harness, a Go CLI and an iOS app file by file: every prompt
required each row to land in a project, and the naming step asked for a project
of "build noise". Leaving out is now the model's call, stated per row, and the
code treats it exactly like an assignment so nothing can go silent.
"""

from __future__ import annotations

import json

from probe.cli import backfill_evidence as ev
from probe.cli import backfill_plan as bp
from probe.cli import backfill_prompts as prompts
from probe.cli import backfill_run as br
from probe.cli.backfill_coverage import Coverage, Scope


def _write(root, rel, text="x"):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def _monorepo(root):
    _write(root, "workloads/train.py", "import torch")
    _write(root, "workloads/results.csv", "step,loss\n1,0.5\n")
    _write(root, "apps/web/package.json", "{}")
    _write(root, "apps/web/app/pages/Show.tsx")
    _write(root, "apps/web/app/models/scan.rb")
    return root


def _plan(**kw):
    return bp.Plan(
        projects=[bp.ProjectSpec(slug="training")],
        assignments=kw.get("assignments", [bp.Assignment("workloads", "training")]),
        left_out=kw.get("left_out", [bp.LeftOut("apps/web", "Rails + React product app")]),
    )


def test_a_left_out_directory_expands_and_never_reaches_the_map(tmp_path):
    evidence = ev.gather(_monorepo(tmp_path))
    left: dict[str, str] = {}
    assigned, disc = bp.resolve(evidence, _plan(), left_out=left)

    assert assigned == {"workloads/train.py": "training", "workloads/results.csv": "training"}
    assert left == dict.fromkeys(
        ["apps/web/package.json", "apps/web/app/pages/Show.tsx", "apps/web/app/models/scan.rb"],
        "Rails + React product app",
    )
    assert disc.clean, "a left-out file must not read as missing"


def test_inheritance_never_leaves_a_file_out(tmp_path):
    """Only a row the model named is left out. An unnamed file among left-out
    neighbours follows the nearest REAL project -- at the root of a monorepo
    the web app's files would otherwise outvote a forgotten README."""
    root = _monorepo(tmp_path)
    _write(root, "README.md", "# datamatrix decoder research")
    evidence = ev.gather(root)
    plan = _plan(left_out=[bp.LeftOut("apps/web/app", "app source")])  # 2 files unnamed
    left: dict[str, str] = {}
    assigned, disc = bp.resolve(evidence, plan, left_out=left)

    assert disc.missing == ["README.md", "apps/web/package.json"]
    assert assigned["README.md"] == assigned["apps/web/package.json"] == "training"
    assert sorted(left) == ["apps/web/app/models/scan.rb", "apps/web/app/pages/Show.tsx"]


def test_a_row_both_placed_and_left_out_makes_the_plan_untrustworthy(tmp_path):
    evidence = ev.gather(_monorepo(tmp_path))
    plan = _plan(assignments=[bp.Assignment("workloads", "training"),
                              bp.Assignment("apps/web/app/models/scan.rb", "training")],
                 left_out=[bp.LeftOut("apps/web/app/models/scan.rb"), bp.LeftOut("apps/web")])
    _, disc = bp.resolve(evidence, plan)
    assert disc.duplicated == ["apps/web/app/models/scan.rb"]
    assert not disc.trustworthy


def test_a_file_placed_inside_a_left_out_directory_keeps_its_project(tmp_path):
    """The more specific row wins, as it always has -- which is how a reviewer's
    "keep apps/web/docs/design.md" survives leaving the rest of the app out."""
    evidence = ev.gather(_monorepo(tmp_path))
    plan = _plan(assignments=[bp.Assignment("workloads", "training"),
                              bp.Assignment("apps/web/app/models/scan.rb", "training")])
    left: dict[str, str] = {}
    assigned, disc = bp.resolve(evidence, plan, left_out=left)
    assert assigned["apps/web/app/models/scan.rb"] == "training"
    assert "apps/web/app/models/scan.rb" not in left
    assert disc.clean


def test_left_out_parses_by_either_key_and_alone_is_still_a_plan():
    payload = {"projects": [], "assignments": [],
               "left_out": [{"dir": "apps/web", "why": "product app"}, "vendor",
                            {"path": ""}, {"path": "  "}, ""]}
    plan = bp.parse(json.dumps(payload))
    assert plan is not None
    assert plan.left_out == [bp.LeftOut("apps/web", "product app"), bp.LeftOut("vendor")]
    assert bp.parse_left_out("none") == [], "a string is not a list of characters"
    assert br._usable_pass({"assignments": [], "left_out": ["vendor"]}, "assignments")
    assert not br._usable_pass({"assignments": [], "left_out": []}, "assignments")


def test_a_left_out_root_row_covers_the_roots_own_files_only(tmp_path):
    """The root's rollup row is its loose files (a monorepo's lockfiles). Left
    out recursively, longest-row-first, it took exactly what the model forgot."""
    root = _monorepo(tmp_path)
    _write(root, "yarn.lock")
    _write(root, "research/train.py", "import torch")  # the model never names it
    evidence = ev.gather(root)
    plan = _plan(left_out=[bp.LeftOut("apps/web", "product app"), bp.LeftOut(".", "lockfiles")])
    left: dict[str, str] = {}
    assigned, disc = bp.resolve(evidence, plan, left_out=left)

    assert left["yarn.lock"] == "lockfiles"
    assert "research/train.py" in disc.missing
    assert assigned["research/train.py"] == "training"
    joined = "\n".join(br.describe_plan(evidence, plan, assigned, disc, left_out=left))
    assert ".  (1 files)  lockfiles" in joined


def test_the_review_names_each_left_out_row_with_its_count_and_why(tmp_path):
    evidence = ev.gather(_monorepo(tmp_path))
    plan = _plan()
    left: dict[str, str] = {}
    assigned, disc = bp.resolve(evidence, plan, left_out=left)
    joined = "\n".join(br.describe_plan(evidence, plan, assigned, disc, left_out=left))
    assert "3 files left out as not research (nothing uploads):" in joined
    assert "apps/web  (3 files)  Rails + React product app" in joined


def test_every_filing_prompt_offers_left_out_and_naming_makes_no_junk_project(tmp_path):
    common = dict(root=tmp_path, evidence_jsonl="{}", work_dir=str(tmp_path))
    filing = [
        prompts.classify(existing=[], truncated=False, **common),
        prompts.assign_chunk(projects="training", index=1, total=2, **common),
        prompts.revise(feedback="keep apps/lab", root=tmp_path, work_dir=str(tmp_path),
                       resumed=True, plan_view="    apps/  ->  training  (3 files)"),
    ]
    for text in filing:
        assert "probe-backfill-plan leave-out" in text
    for text in filing[:2]:
        assert prompts.LEAVE_OUT in text
    naming = prompts.name_projects(root=tmp_path, findings_json="[]", own=[])
    assert "belong in one project of their own" not in naming
    assert "make no project for what is not research" in " ".join(naming.split())
    # The slice filer decides what is left out, so a correction must reach it.
    corrected = prompts.assign_chunk(projects="training", index=1, total=2,
                                     feedback="keep apps/lab, it is research", **common)
    assert "keep apps/lab, it is research" in corrected


def test_an_excluded_file_stays_settled_until_review_excluded(tmp_path):
    """Leaving a file out was a call about what it IS: an edit to a product's
    code must not reopen the import. `--review-excluded` is the way back."""
    root = tmp_path / "folder"
    _write(root, "app.rb", "before")
    scope = Scope("https://example.test", "tenant-a", "workspace-a", "project-a")
    with Coverage.for_folder(root, scope, directory=tmp_path / "state").writer() as state:
        state.observe(root, ["app.rb"])
        state.exclude({"app.rb": "product app"})
        assert state.report()["excluded"] == ["app.rb"]
        assert state.report()["new"] == []
    _write(root, "app.rb", "after!")
    with Coverage.for_folder(root, scope, directory=tmp_path / "state").writer() as state:
        state.observe(root, ["app.rb"])
        assert state.report()["excluded"] == ["app.rb"]
        assert state.clear_exclusions() == 1
        assert state.report()["new"] == ["app.rb"]
