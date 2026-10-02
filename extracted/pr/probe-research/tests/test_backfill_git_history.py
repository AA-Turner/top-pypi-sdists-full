"""The wizard's git awareness (0134): detection, the deterministic digest, and
the GIT_HISTORY prompt fragment — present when the folder is a work tree,
absent otherwise, and never able to fail an import."""

from __future__ import annotations

import subprocess
from pathlib import Path

from probe.cli import backfill as bf
from probe.cli import backfill_prompts as prompts
from probe.cli.backfill_run import _git_note


def _init_repo(root: Path, *, remote: str | None = "git@github.com:Acme-Lab/Train.git"):
    def git(*args: str) -> None:
        subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            env={
                "PATH": "/usr/bin:/bin",
                "GIT_AUTHOR_NAME": "m",
                "GIT_AUTHOR_EMAIL": "m@x",
                "GIT_COMMITTER_NAME": "m",
                "GIT_COMMITTER_EMAIL": "m@x",
                "HOME": str(root),
            },
        )

    git("init", "-q", "-b", "odyssey3")
    (root / "train.py").write_text("print('hi')\n")
    git("add", "train.py")
    git("commit", "-q", "-m", "first commit by us")
    (root / "eval.py").write_text("print('eval')\n")
    git("add", "eval.py")
    git("commit", "-q", "-m", "feat: add eval")
    git("tag", "v0.1")
    if remote:
        git("remote", "add", "origin", remote)


def test_git_context_detects_repo_branch_and_github_remote(tmp_path):
    _init_repo(tmp_path)
    context = bf.git_context(tmp_path)
    assert context is not None
    assert context.toplevel == tmp_path
    assert context.branch == "odyssey3"
    assert context.repo == "Acme-Lab/Train"


def test_git_context_is_none_outside_a_work_tree(tmp_path):
    assert bf.git_context(tmp_path) is None


def test_non_github_remote_is_a_normal_answer(tmp_path):
    _init_repo(tmp_path, remote="https://gitlab.com/acme/train.git")
    context = bf.git_context(tmp_path)
    assert context is not None
    assert context.repo is None
    assert context.remote and "gitlab.com" in context.remote


def test_credentialed_remote_is_scrubbed(tmp_path):
    _init_repo(tmp_path, remote="https://x-access-token:SECRET@github.com/a/b.git")
    context = bf.git_context(tmp_path)
    assert context is not None
    assert "SECRET" not in (context.remote or "")


def test_digest_is_bounded_and_carries_the_story(tmp_path):
    _init_repo(tmp_path)
    work = tmp_path / "scratch"
    work.mkdir()
    context = bf.git_context(tmp_path)
    out = bf.write_git_history(context, work)
    assert out is not None and out.name == "git-history.md"
    text = out.read_text()
    assert "Acme-Lab/Train" in text and "odyssey3" in text
    assert "first commit by us" in text
    assert "v0.1" in text
    assert len(text.encode()) <= bf.GIT_HISTORY_MAX_BYTES + 64


def test_fragment_present_for_a_repo_and_absent_otherwise(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    work = tmp_path / "scratch"
    work.mkdir()
    note = _git_note(repo, work)
    assert "THIS FOLDER IS A GIT REPOSITORY" in note
    assert "git-history.md" in note
    assert "probe project code attach" in note
    assert "--via wizard" in note
    assert "never present an old commit's state" in note

    plain = tmp_path / "plain"
    plain.mkdir()
    assert _git_note(plain, work) == ""


def test_fragment_offers_no_attach_without_a_github_remote():
    text = prompts.git_history(history_path="/x/git-history.md", repo=None, branch="main")
    assert "probe project code attach" not in text
    assert "git-history.md" in text
