from __future__ import annotations

from pathlib import Path
from subprocess import CalledProcessError, check_call, run
from typing import Final

from git import Commit, Remote, Repo
from packaging.version import Version

_ROOT_SRC_DIR: Final[Path] = Path(__file__).parents[1]


def main(version_str: str) -> None:
    version = Version(version_str)
    repo = Repo(str(_ROOT_SRC_DIR))

    if repo.is_dirty():
        msg = "Current repository is dirty. Please commit any changes and try again."
        raise RuntimeError(msg)
    upstream = get_upstream(repo)
    upstream.fetch()
    if str(version) in {tag.name for tag in repo.tags}:
        msg = f"release tag {version} already exists"
        raise RuntimeError(msg)
    repo.git.checkout("-B", f"release-{version}", upstream.refs.main)
    release_commit = release_changelog(repo, version)
    repo.create_tag(str(version), ref=release_commit.hexsha, message=f"release {version}")
    repo.git.push(upstream.name, "HEAD:main")
    repo.git.push(upstream.name, f"refs/tags/{version}")
    create_github_release(version)


def get_upstream(repo: Repo) -> Remote:
    for remote in repo.remotes:
        if any("tox-dev/python-discovery" in url for url in remote.urls):
            return remote
    msg = "could not find tox-dev/python-discovery remote"
    raise RuntimeError(msg)


def release_changelog(repo: Repo, version: Version) -> Commit:
    print("generate release commit")  # ruff:ignore[print]
    check_call(["towncrier", "build", "--yes", "--version", version.public], cwd=str(_ROOT_SRC_DIR))  # ruff:ignore[start-process-with-partial-path]
    print("format changelog with pre-commit")  # ruff:ignore[print]
    changelog_path = _ROOT_SRC_DIR / "docs" / "changelog.rst"
    try:
        check_call(["pre-commit", "run", "--files", str(changelog_path)], cwd=str(_ROOT_SRC_DIR))  # ruff:ignore[start-process-with-partial-path]
    except CalledProcessError:
        check_call(["pre-commit", "run", "--files", str(changelog_path)], cwd=str(_ROOT_SRC_DIR))  # ruff:ignore[start-process-with-partial-path]
    repo.git.add("-A", "--", "docs/changelog.rst", "docs/changelog")
    return repo.index.commit(f"release {version}")


def create_github_release(version: Version) -> None:
    print("create github release")  # ruff:ignore[print]
    version_str = str(version)
    try:
        result = run(
            ["gh", "release", "create", version_str, "--title", f"v{version_str}", "--generate-notes"],  # ruff:ignore[start-process-with-partial-path]
            cwd=str(_ROOT_SRC_DIR),
            capture_output=True,
            text=True,
            check=True,
        )
        if result.stdout:
            print(result.stdout)  # ruff:ignore[print]
    except CalledProcessError as e:
        print(f"gh release create failed with exit code {e.returncode}")  # ruff:ignore[print]
        if e.stdout:
            print(f"stdout: {e.stdout}")  # ruff:ignore[print]
        if e.stderr:
            print(f"stderr: {e.stderr}")  # ruff:ignore[print]
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="release")
    parser.add_argument("--version", required=True)
    options = parser.parse_args()
    main(options.version)
