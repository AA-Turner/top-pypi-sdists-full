"""TDD tests for Tier 2 safety harness: T2, T5, T6.

T2: Diff preview before applying batched FILE: writes
T5: Tmpdir staging — every change goes through a tmpdir copy first
T6: Run guard — refuse RUN: <pkg-manager> install on a just-rejected manifest
"""

from __future__ import annotations

from pathlib import Path

import pytest


# ════════════════════════════════════════════════════════════════════════
# T2: Diff preview
# ════════════════════════════════════════════════════════════════════════

def test_render_diff_for_new_file():
    from sage.core.diff_preview import render_diff
    out = render_diff(filepath="src/new.py", before=None, after="def f(): pass\n")
    assert "src/new.py" in out
    assert "+def f()" in out or "+ def f()" in out or "+def" in out
    # New file marker
    assert "(new" in out.lower() or "new file" in out.lower()


def test_render_diff_for_modified_file():
    from sage.core.diff_preview import render_diff
    out = render_diff(
        filepath="src/x.py",
        before="def f():\n    return 1\n",
        after="def f():\n    return 2\n",
    )
    assert "src/x.py" in out
    assert "-    return 1" in out
    assert "+    return 2" in out


def test_render_diff_for_deletion():
    from sage.core.diff_preview import render_diff
    out = render_diff(filepath="src/old.py", before="x = 1\n", after=None)
    assert "src/old.py" in out
    assert "delete" in out.lower() or "deleted" in out.lower() or "(removed" in out.lower()


def test_render_batch_summary_lists_all_changes():
    from sage.core.diff_preview import render_batch_summary, PendingChange
    changes = [
        PendingChange(filepath="src/a.py", before=None, after="content_a"),
        PendingChange(filepath="src/b.py", before="old", after="new"),
        PendingChange(filepath="src/c.py", before="x", after=None),
    ]
    out = render_batch_summary(changes)
    assert "src/a.py" in out
    assert "src/b.py" in out
    assert "src/c.py" in out
    # Counts in summary
    assert "3" in out


def test_pending_change_is_new_modify_or_delete():
    from sage.core.diff_preview import PendingChange
    assert PendingChange("a", None, "x").kind == "new"
    assert PendingChange("a", "x", "y").kind == "modify"
    assert PendingChange("a", "x", None).kind == "delete"
    assert PendingChange("a", "x", "x").kind == "noop"


def test_should_auto_apply_returns_true_when_all_validators_pass():
    from sage.core.diff_preview import PendingChange, should_auto_apply
    changes = [
        PendingChange("server.js", None,
                      "const express = require('express');\n"
                      "const app = express();\napp.listen(3000);\n"),
    ]
    decision = should_auto_apply(changes, auto_threshold_lines=200)
    assert decision.auto is True


def test_should_auto_apply_requires_confirm_for_large_batches():
    from sage.core.diff_preview import PendingChange, should_auto_apply
    changes = [
        PendingChange(f"src/{i}.txt", None, "line\n" * 50)
        for i in range(20)
    ]
    decision = should_auto_apply(changes, auto_threshold_lines=200)
    assert decision.auto is False
    assert "lines" in decision.reason.lower() or "files" in decision.reason.lower()


def test_should_auto_apply_blocks_validator_failures():
    """If even one change fails the content validator, require confirmation."""
    from sage.core.diff_preview import PendingChange, should_auto_apply
    changes = [
        PendingChange("good.js", None, "const x = 1;\n"),
        PendingChange("bad.json", None, '{"dependencies": {"are": "^0.0.1"}}'),
    ]
    decision = should_auto_apply(changes, auto_threshold_lines=10000)
    assert decision.auto is False
    assert "json" in decision.reason.lower() or "valid" in decision.reason.lower() or "reject" in decision.reason.lower()


# ════════════════════════════════════════════════════════════════════════
# T5: Tmpdir staging
# ════════════════════════════════════════════════════════════════════════

def test_staging_area_creates_isolated_workspace(tmp_path):
    from sage.core.staging import StagingArea
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "src").mkdir()
    (repo / "src" / "existing.py").write_text("existing = True\n")

    with StagingArea(repo) as stage:
        # Stage path is NOT the original repo
        assert stage.root != repo
        assert stage.root.is_dir()
        # Existing files copied through
        assert (stage.root / "src" / "existing.py").exists()


def test_staging_area_writes_dont_touch_real_repo(tmp_path):
    from sage.core.staging import StagingArea
    repo = tmp_path / "repo"
    repo.mkdir()
    with StagingArea(repo) as stage:
        stage.stage_write("new.txt", "hello")
        # Real repo still empty
        assert not (repo / "new.txt").exists()
    # After context exit (no commit) — still empty
    assert not (repo / "new.txt").exists()


def test_staging_area_commit_applies_writes(tmp_path):
    from sage.core.staging import StagingArea
    repo = tmp_path / "repo"
    repo.mkdir()
    with StagingArea(repo) as stage:
        stage.stage_write("new.txt", "hello")
        stage.stage_write("subdir/file.py", "x = 1\n")
        stage.commit()
    assert (repo / "new.txt").read_text() == "hello"
    assert (repo / "subdir" / "file.py").read_text() == "x = 1\n"


def test_staging_area_excludes_node_modules(tmp_path):
    """Don't copy heavy directories into staging — they'd be slow + unused."""
    from sage.core.staging import StagingArea
    repo = tmp_path / "repo"
    (repo / "node_modules" / "lib").mkdir(parents=True)
    (repo / "node_modules" / "lib" / "a.js").write_text("// vendored")
    (repo / "src").mkdir()
    (repo / "src" / "main.js").write_text("// real")
    with StagingArea(repo) as stage:
        assert (stage.root / "src" / "main.js").exists()
        assert not (stage.root / "node_modules").exists()


def test_staging_area_run_command_executes_in_stage(tmp_path):
    from sage.core.staging import StagingArea
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "marker.txt").write_text("real")
    with StagingArea(repo) as stage:
        stage.stage_write("marker.txt", "staged")
        # `cat marker.txt` should see the staged content
        result = stage.run(["cat", "marker.txt"])
        assert result.returncode == 0
        assert "staged" in result.stdout


def test_staging_area_rolls_back_on_validator_failure(tmp_path):
    from sage.core.staging import StagingArea
    repo = tmp_path / "repo"
    repo.mkdir()
    with StagingArea(repo) as stage:
        # Stage some valid content
        stage.stage_write("good.js", "const x = 1;\n")
        # Stage poison
        ok = stage.stage_write("package.json",
                               '{"dependencies": {"are": "^0.0.1"}}',
                               validate=True)
        assert ok is False  # validator rejected
    # Real repo should have nothing because we never committed
    assert not (repo / "good.js").exists()
    assert not (repo / "package.json").exists()


# ════════════════════════════════════════════════════════════════════════
# T6: Run guard — refuse install commands after a rejected manifest
# ════════════════════════════════════════════════════════════════════════

def test_run_guard_allows_arbitrary_commands_when_no_recent_rejects():
    from sage.core.run_guard import RunGuard
    g = RunGuard()
    assert g.allow("npm install").allowed is True
    assert g.allow("ls -la").allowed is True
    assert g.allow("pytest -x").allowed is True


def test_run_guard_blocks_npm_install_after_rejected_package_json():
    from sage.core.run_guard import RunGuard
    g = RunGuard()
    g.record_rejection("package.json", reason="json_poison")
    decision = g.allow("npm install")
    assert decision.allowed is False
    assert "package.json" in decision.reason


def test_run_guard_blocks_pip_install_after_rejected_requirements():
    from sage.core.run_guard import RunGuard
    g = RunGuard()
    g.record_rejection("requirements.txt", reason="protocol_leak")
    assert g.allow("pip install -r requirements.txt").allowed is False


def test_run_guard_blocks_yarn_install_after_rejected_package_json():
    from sage.core.run_guard import RunGuard
    g = RunGuard()
    g.record_rejection("package.json", reason="json_poison")
    assert g.allow("yarn install").allowed is False
    assert g.allow("pnpm install").allowed is False


def test_run_guard_recovers_after_clean_write():
    from sage.core.run_guard import RunGuard
    g = RunGuard()
    g.record_rejection("package.json", reason="json_poison")
    assert g.allow("npm install").allowed is False
    # A subsequent valid write to the same file should clear the block
    g.record_clean_write("package.json")
    assert g.allow("npm install").allowed is True


def test_run_guard_does_not_block_unrelated_commands():
    from sage.core.run_guard import RunGuard
    g = RunGuard()
    g.record_rejection("package.json", reason="json_poison")
    # Reading and listing should still work
    assert g.allow("ls").allowed is True
    assert g.allow("cat src/main.js").allowed is True
    # Tests too
    assert g.allow("pytest").allowed is True


def test_run_guard_blocks_destructive_commands_when_recently_rejected():
    """If we just rejected a write, also block rm/git reset that could
    erase the user's actual real files."""
    from sage.core.run_guard import RunGuard
    g = RunGuard()
    g.record_rejection("src/server.js", reason="protocol_leak")
    # Destructive on the repo? Block out of caution
    assert g.allow("rm -rf .").allowed is False
    assert g.allow("git reset --hard").allowed is False
