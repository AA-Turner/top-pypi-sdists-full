from __future__ import annotations
from pathlib import Path
import shutil
import subprocess
from typing import NamedTuple
import pytest
from ghrepo import GHRepo


class TmpRepo(NamedTuple):
    path: Path
    branch: str
    remotes: dict[str, GHRepo]
    upstreams: dict[str, GHRepo]

    def run(self, *args: str) -> None:
        subprocess.run(["git", *args], check=True, cwd=self.path)

    def detach(self) -> None:
        (self.path / "file.txt").write_text("This is test text\n")
        self.run("add", "file.txt")
        self.run("commit", "-m", "Add a file")
        (self.path / "file2.txt").write_text("This is also text\n")
        self.run("add", "file2.txt")
        self.run("commit", "-m", "Add another file")
        self.run("checkout", "HEAD^")


@pytest.fixture(scope="session")
def tmp_repo(tmp_path_factory: pytest.TempPathFactory) -> TmpRepo:
    if shutil.which("git") is None:
        pytest.skip("Git not installed")
    tmp_path = tmp_path_factory.mktemp("tmp_repo")
    BRANCH = "trunk"
    REMOTES = {
        "origin": GHRepo("octocat", "repository"),
        "upstream": GHRepo("foobar", "repo"),
    }
    subprocess.run(
        ["git", "-c", f"init.defaultBranch={BRANCH}", "init"],
        check=True,
        cwd=str(tmp_path),
    )
    subprocess.run(
        ["git", "remote", "add", "origin", REMOTES["origin"].ssh_url],
        check=True,
        cwd=str(tmp_path),
    )
    subprocess.run(
        ["git", "remote", "add", "upstream", REMOTES["upstream"].clone_url],
        check=True,
        cwd=str(tmp_path),
    )
    subprocess.run(
        ["git", "config", "branch.draft.remote", "upstream"],
        check=True,
        cwd=str(tmp_path),
    )
    return TmpRepo(tmp_path, BRANCH, REMOTES, {"draft": REMOTES["upstream"]})
