"""Writes `coverage.sqlite3`: a folder-import store made by RELEASED CLI 0.327.0.

The store an import made before hidden folders and worktree copies were
skipped (CLI 0.328.0). Its code, not this repo's, writes every byte: run it
with that release's interpreter, isolated so this repo cannot shadow it:

    uv venv /tmp/old --python 3.12
    VIRTUAL_ENV=/tmp/old uv pip install probe-research==0.327.0
    cd /tmp && /tmp/old/bin/python -I <this file> <this folder>

It builds `layout.json`'s folder (a git repo with an agent worktree under
`.claude/worktrees/agent-x`), walks it by 0.327.0's rules, takes the census,
approves and delivers the files the way an import does (receipts shaped as the
server returns them), and leaves one worktree file unapproved, as a plan that
left it undecided would. The folder itself is thrown away; the test rebuilds it
from `layout.json` (`test_backfill_skipped_by_rule.py`).
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import probe
from probe.cli import backfill_evidence as evidence
from probe.cli.backfill_coverage import Coverage, Scope

assert probe.__version__ == "0.327.0", probe.__version__

HERE = Path(sys.argv[1]).resolve()
LAYOUT = json.loads((HERE / "layout.json").read_text())
SCOPE = Scope(**LAYOUT["scope"])
ENV = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
       "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid",
       "GIT_CONFIG_NOSYSTEM": "1"}


def git(cwd, *args):
    subprocess.run(["git", "-c", "init.defaultBranch=main", *args], cwd=cwd, check=True,
                   capture_output=True, env=ENV)


def write(root, files):
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)


with tempfile.TemporaryDirectory() as scratch:
    root = Path(scratch) / "drive"
    root.mkdir()
    git(root, "init", "-q")
    write(root, LAYOUT["committed"])
    git(root, "add", "-A")
    git(root, "commit", "-qm", "init")
    git(root, "worktree", "add", "-q", LAYOUT["worktree"])
    write(root, LAYOUT["untracked"])

    paths = sorted(str(Path(f.path).relative_to(root.resolve()))
                   for f in evidence.walk(root))
    state = Path(scratch) / "state"
    store = Coverage.for_folder(root, SCOPE, directory=state, source_id=None)
    with store.writer() as coverage:
        coverage.observe(root, paths)
        projects = {p["id"]: p for p in LAYOUT["projects"]}
        approved = {path: projects[pid] for path, pid in LAYOUT["approved"].items()}
        assert set(approved) | set(LAYOUT["undecided"]) == set(paths), paths
        coverage.approve(approved)
        for n, row in enumerate(r for r in coverage.rows() if r["path"] in approved):
            intent = coverage.intend(row, reference=False)
            coverage.accept_receipt(intent["correlation"], {
                "correlation": intent["correlation"], "state": "delivered",
                "status": "complete", "readable": True, "artifact_id": f"artifact-{n:03d}",
                "anchor": "project", "anchor_id": row["project_id"], "name": row["path"],
                "content_hash": intent["content_hash"], "size_bytes": intent["size_bytes"],
                "source_content_hash": intent["content_hash"], "is_reference": False,
                "uri": None,
            })
        coverage.put_meta("last_verified_complete", False)
        report = coverage.report()
    shutil.copyfile(store.path, HERE / "coverage.sqlite3")
    (HERE / "source_id").write_text(store.source_id + "\n")
    print(json.dumps({k: len(v) for k, v in report.items()}))
