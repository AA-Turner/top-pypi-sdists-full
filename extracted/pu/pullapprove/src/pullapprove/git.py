from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Generator
from pathlib import Path


def git_pager() -> str:
    """The pager command git would use, honoring core.pager/GIT_PAGER/PAGER.

    Returns a shell command string (git's pager values can include arguments or
    pipes, so callers run it through a shell, the way git does). Falls back to
    `cat` when git is unavailable or paging is disabled.
    """
    try:
        output = subprocess.check_output(["git", "var", "GIT_PAGER"], text=True).strip()
    except (subprocess.CalledProcessError, OSError):
        output = ""
    return output or os.environ.get("PAGER", "") or "cat"


def page(text: str) -> None:
    """Display `text` through git's configured pager, the way `git diff` does."""
    env = {**os.environ}
    env.setdefault("LESS", "FRX")  # quit if one screen, keep colors, no init clear
    proc = subprocess.Popen(
        git_pager(), shell=True, stdin=subprocess.PIPE, text=True, env=env
    )
    try:
        proc.communicate(text)
    except BrokenPipeError:
        pass  # the pager was closed before reading everything (e.g. `q` in less)
    if proc.returncode:
        sys.stdout.write(text)  # the pager failed to run; don't lose the output


def git_ls_files(path: Path) -> Generator[str]:
    """Yield files in the git repository one at a time.

    A file deleted from the working tree is both cached and deleted, and git
    lists it once for each, so it's yielded the first time only.
    """
    seen = set()
    process = subprocess.Popen(
        [
            "git",
            "ls-files",
            "--cached",
            "--deleted",
            "--others",
            "--exclude-standard",
        ],
        cwd=path,
        stdout=subprocess.PIPE,
        text=True,
    )

    assert process.stdout is not None
    for line in process.stdout:
        file_path = line.strip()
        if file_path not in seen:
            seen.add(file_path)
            yield file_path

    process.stdout.close()
    process.wait()


def git_ls_changes(path: Path) -> list[str]:
    """Every changed or untracked file in the working tree and index."""
    # -z so paths come through unquoted, one NUL-terminated `XY path` entry
    # each (a rename's entry is followed by its old path)
    output = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=path,
        text=True,
        encoding="utf-8",
    )

    changed = []
    entries = iter(output.split("\0"))
    for entry in entries:
        if not entry:
            continue
        status, file_path = entry[:2], entry[3:]
        changed.append(file_path)
        if "R" in status or "C" in status:
            next(entries)
    return changed


# The diff GitHub serves for a pull request uses git's defaults: three lines
# of context, rename detection, the myers algorithm (checked against real
# pull requests). Passed explicitly so a gitconfig like
# `diff.algorithm = histogram` can't shape the hunks differently, since code
# patterns see context lines too.
HOST_DIFF_ARGS = ("--unified=3", "--find-renames", "--diff-algorithm=myers")


def git_commit_sha(*, path: Path, ref: str) -> str:
    """The commit `ref` names (`--end-of-options` so a ref can't pass for an
    option)."""
    return subprocess.check_output(
        ["git", "rev-parse", "--verify", "--quiet", "--end-of-options"]
        + [f"{ref}^{{commit}}"],
        cwd=path,
        text=True,
        encoding="utf-8",
    ).strip()


def git_ls_tree(*, path: Path, ref: str) -> list[str]:
    """Every file in `ref`'s tree, as repo-root-relative paths."""
    output = subprocess.check_output(
        ["git", "ls-tree", "-r", "-z", "--name-only", "--full-tree", ref],
        cwd=path,
        text=True,
        encoding="utf-8",
    )
    return [name for name in output.split("\0") if name]


def git_file_at(*, path: Path, ref: str, file_path: str) -> str:
    """A file's content as committed at `ref`."""
    return subprocess.check_output(
        ["git", "cat-file", "blob", f"{ref}:{file_path}"],
        cwd=path,
        text=True,
        # The same decoding the working tree's configs get (tomllib reads UTF-8)
        encoding="utf-8",
    )


def git_diff_stream(path: Path, *diff_args: str) -> Generator[str]:
    # `-c diff.noprefix=false` because our diff parser requires the `a/`/`b/`
    # (or mnemonic single-char) path prefixes to recognize file headers — a user
    # with `diff.noprefix = true` in their gitconfig would otherwise produce a
    # diff whose files we silently misattribute. `--no-color` for the same
    # reason: `color.ui = always` would put escape codes in front of every
    # line. An explicit `--no-prefix` or `--color` in diff_args still wins
    # (later flags override).
    process = subprocess.Popen(
        ["git", "-c", "diff.noprefix=false", "diff", "--no-ext-diff", "--no-color"]
        + list(diff_args),
        cwd=path,
        stdout=subprocess.PIPE,
        text=True,
    )

    assert process.stdout is not None
    yield from process.stdout

    process.stdout.close()
    returncode = process.wait()
    # 0 = success, 1 = changes found (with --exit-code); anything else is a real
    # git error (bad revision, unknown option) that would otherwise masquerade
    # as an empty diff. git has already printed the reason to stderr.
    if returncode not in (0, 1):
        raise subprocess.CalledProcessError(returncode, ["git", "diff", *diff_args])
