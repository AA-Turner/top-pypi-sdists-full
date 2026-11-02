from __future__ import annotations

import json
import os
import subprocess

from click.testing import CliRunner
from pullapprove.cli import cli
from pullapprove.diff import parse_diff_file_line

from pullapprove import git

# A lockfile hunk (trivial) followed by a real code change.
LOCKFILE_AND_CODE = (
    "diff --git a/uv.lock b/uv.lock\n"
    "index 1111111..2222222 100644\n"
    "--- a/uv.lock\n"
    "+++ b/uv.lock\n"
    "@@ -1,1 +1,1 @@\n"
    '-version = "1.0"\n'
    '+version = "1.1"\n'
    "diff --git a/core.py b/core.py\n"
    "index 3333333..4444444 100644\n"
    "--- a/core.py\n"
    "+++ b/core.py\n"
    "@@ -5,1 +5,1 @@\n"
    "-    value = compute_old()\n"
    "+    value = compute_new()\n"
)


def test_diff_hides_trivial_hunks_by_default():
    result = CliRunner().invoke(cli, ["diff"], input=LOCKFILE_AND_CODE)

    assert result.exit_code == 0
    # The lockfile hunk (and its header) is dropped; the real change survives.
    assert "uv.lock" not in result.output
    assert "compute_new()" in result.output
    # The summary goes to stderr, leaving stdout a clean, valid diff.
    assert "generated:lockfile (1)" in result.stderr


def test_diff_forwards_the_pathspec_separator_to_git(tmp_path, monkeypatch):
    """`--` has to reach git, or a deleted path can't be named at all.

    Click eats the first `--` it sees, so `pullapprove diff HEAD -- gone.py`
    used to reach git as `diff HEAD gone.py` — which git rejects, because
    `gone.py` no longer exists to tell a path from a revision.
    """
    monkeypatch.chdir(tmp_path)

    def git_run(*args):
        subprocess.run(args, cwd=tmp_path, check=True, capture_output=True)

    git_run("git", "init", "-q", "-b", "main")
    (tmp_path / "gone.py").write_text("value = 1\n")
    git_run("git", "add", "gone.py")
    git_run("git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init")
    (tmp_path / "gone.py").unlink()

    result = CliRunner().invoke(cli, ["diff", "--no-pager", "HEAD", "--", "gone.py"])

    assert result.exit_code == 0
    assert "deleted file mode" in result.output
    assert "-value = 1" in result.output


def test_diff_hide_family_restricts_what_is_hidden():
    diff = (
        "diff --git a/uv.lock b/uv.lock\n"
        "--- a/uv.lock\n"
        "+++ b/uv.lock\n"
        "@@ -1,1 +1,1 @@\n"
        '-version = "1.0"\n'
        '+version = "1.1"\n'
        "diff --git a/style.js b/style.js\n"
        "--- a/style.js\n"
        "+++ b/style.js\n"
        "@@ -1,1 +1,1 @@\n"
        "-const x = 1\n"
        "+const x = 1;\n"
    )

    # Only the formatting family is hidden; the lockfile hunk stays put.
    result = CliRunner().invoke(cli, ["diff", "--hide", "formatting"], input=diff)

    assert result.exit_code == 0
    assert "uv.lock" in result.output
    assert "style.js" not in result.output
    assert "formatting:style (1)" in result.stderr


def test_diff_hide_accepts_a_full_label():
    # A full label, not just a family, is a valid --hide value.
    result = CliRunner().invoke(
        cli, ["diff", "--hide", "generated:lockfile"], input=LOCKFILE_AND_CODE
    )

    assert result.exit_code == 0
    assert "uv.lock" not in result.output
    assert "compute_new()" in result.output


def test_diff_hide_rejects_unknown_family():
    # A typo'd family must error, not silently hide everything.
    result = CliRunner().invoke(
        cli, ["diff", "--hide", "formating"], input=LOCKFILE_AND_CODE
    )

    assert result.exit_code != 0
    assert "unknown trust family: formating" in result.output
    assert "Valid families:" in result.output


def test_diff_quiet_suppresses_summary():
    result = CliRunner().invoke(cli, ["diff", "--quiet"], input=LOCKFILE_AND_CODE)

    assert result.exit_code == 0
    assert "uv.lock" not in result.output
    assert result.stderr == ""


# A lockfile hunk (trusted), a comment-only hunk (trusted), and a real change.
TRUST_DIFF = (
    "diff --git a/uv.lock b/uv.lock\n"
    "--- a/uv.lock\n"
    "+++ b/uv.lock\n"
    "@@ -1,1 +1,1 @@\n"
    '-version = "1.0"\n'
    '+version = "1.1"\n'
    "diff --git a/app.py b/app.py\n"
    "--- a/app.py\n"
    "+++ b/app.py\n"
    "@@ -1,1 +1,1 @@\n"
    "-# old comment\n"
    "+# new comment\n"
    "diff --git a/core.py b/core.py\n"
    "--- a/core.py\n"
    "+++ b/core.py\n"
    "@@ -5,1 +5,1 @@\n"
    "-value = compute_old()\n"
    "+value = compute_new()\n"
)


def test_trust_summary_breaks_down_trusted_and_review():
    result = CliRunner().invoke(cli, ["trust"], input=TRUST_DIFF)

    assert result.exit_code == 0
    assert "3 hunks" in result.output
    assert "3 files" in result.output
    assert "2 trusted (67%)" in result.output
    assert "1 need review (33%)" in result.output
    assert "generated:lockfile" in result.output
    assert "comments:modified" in result.output
    # uv.lock and app.py have only trusted hunks; core.py does not.
    assert "2 files fully trusted" in result.output
    assert "uv.lock" in result.output


def test_trust_list_shows_every_hunk_with_its_label():
    result = CliRunner().invoke(cli, ["trust", "--list"], input=TRUST_DIFF)

    assert result.exit_code == 0
    assert "@@ -1,1 +1,1 @@" in result.output
    assert "generated:lockfile" in result.output
    assert "comments:modified" in result.output
    # The real code change is surfaced as needing review.
    assert "needs review" in result.output


def test_git_diff_stream_forces_path_prefixes(tmp_path, monkeypatch):
    """A user's `diff.noprefix = true` must not strip the path prefixes the diff
    parser needs to recognize file headers. (A mnemonicPrefix config may still
    swap `a/`/`b/` for `i/`/`w/` etc. — any single-char prefix parses fine, so
    assert the property that matters: the header is parseable.)"""
    # Scrub any hook environment: when the suite runs under `git commit` (the
    # pre-commit hook), git exports GIT_DIR/GIT_INDEX_FILE pointing at the
    # OUTER repo, which would redirect this test's temp-repo git calls at it.
    for var in [v for v in os.environ if v.startswith("GIT_")]:
        monkeypatch.delenv(var)

    def run_git(*args: str) -> None:
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True)

    run_git("init", "-q")
    run_git("config", "diff.noprefix", "true")
    (tmp_path / "a.py").write_text("x = 1\n")
    run_git("add", "a.py")
    (tmp_path / "a.py").write_text("x = 2\n")

    output = "".join(git.git_diff_stream(tmp_path))

    header = next(line for line in output.splitlines() if line.startswith("diff --git"))
    file = parse_diff_file_line(header)
    assert file is not None
    assert file.new_path == "a.py"


def test_page_writes_through_git_pager(monkeypatch, capfd):
    # GIT_PAGER overrides core.pager, so the pager resolves to a plain `cat`.
    monkeypatch.setenv("GIT_PAGER", "cat")

    git.page("alpha\nbeta\n")

    out, _ = capfd.readouterr()
    assert out == "alpha\nbeta\n"


def test_page_falls_back_to_stdout_when_pager_fails(monkeypatch, capfd):
    # A pager that can't run mustn't swallow the diff.
    monkeypatch.setenv("GIT_PAGER", "pullapprove-no-such-pager-xyz")

    git.page("the diff\n")

    out, _ = capfd.readouterr()
    assert "the diff\n" in out


JSON_CONFIG = (
    "[[scopes]]\n"
    'name = "video"\n'
    'paths = ["video/**/*"]\n'
    "\n"
    "[[scopes]]\n"
    'name = "secrets"\n'
    'paths = ["**/*.py"]\n'
    'code = [".*API_KEY.*"]\n'
)


# video/ is path-owned, lib/keys.py is only matched by a code pattern, and
# README.md is owned by nothing
JSON_REPO = {
    "CODEREVIEW.toml": JSON_CONFIG,
    "video/player.py": "x = 1\n",
    "lib/keys.py": "x = 1\nAPI_KEY = 'abc'\n",
    "README.md": "hi\n",
}


def run_git_in(repo, *args):
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    )


def make_repo(tmp_path, monkeypatch, files):
    """Commit `files` (path -> content) on main in tmp_path, and work there."""
    monkeypatch.chdir(tmp_path)
    for path, content in files.items():
        (tmp_path / path).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / path).write_text(content)
    run_git_in(tmp_path, "init", "-q", "-b", "main")
    run_git_in(tmp_path, "add", ".")
    run_git_in(tmp_path, "commit", "-qm", "init")


def test_match_json_lists_every_file_scope_and_code_match(tmp_path, monkeypatch):
    make_repo(tmp_path, monkeypatch, JSON_REPO)

    result = CliRunner().invoke(cli, ["match", "--json"])

    assert result.exit_code == 0, result.output
    output = json.loads(result.stdout)
    assert output["paths"] == {
        "CODEREVIEW.toml": {"path": "CODEREVIEW.toml", "scopes": []},
        "README.md": {"path": "README.md", "scopes": []},
        "lib/keys.py": {"path": "lib/keys.py", "scopes": []},
        "video/player.py": {"path": "video/player.py", "scopes": ["video"]},
    }

    [(location_id, code_match)] = output["code"].items()
    assert code_match == {
        "path": "lib/keys.py",
        "scopes": ["secrets"],
        "start_line": 2,
        "end_line": 2,
        "start_column": 1,
        "end_column": 16,
        "location_id": location_id,
    }

    assert list(output["scopes"]) == ["video", "secrets"]
    assert output["scopes"]["video"]["name"] == "video"
    assert output["scopes"]["video"]["paths"] == ["video/**/*"]
    assert output["scopes"]["secrets"]["code"] == [".*API_KEY.*"]


def test_match_json_changed_includes_unowned_and_code_only_files(tmp_path, monkeypatch):
    make_repo(tmp_path, monkeypatch, JSON_REPO)
    (tmp_path / "README.md").write_text("changed\n")
    (tmp_path / "lib" / "keys.py").write_text("x = 2\nAPI_KEY = 'xyz'\n")

    result = CliRunner().invoke(cli, ["match", "--changed", "--json"])

    assert result.exit_code == 0, result.output
    output = json.loads(result.stdout)
    assert output["paths"] == {
        "README.md": {"path": "README.md", "scopes": []},
        "lib/keys.py": {"path": "lib/keys.py", "scopes": []},
    }
    [code_match] = output["code"].values()
    assert code_match["path"] == "lib/keys.py"
    assert code_match["scopes"] == ["secrets"]


def test_match_json_diff_includes_unowned_files_and_code_matches(tmp_path, monkeypatch):
    make_repo(tmp_path, monkeypatch, JSON_REPO)
    (tmp_path / "README.md").write_text("changed\n")
    (tmp_path / "video" / "player.py").write_text("x = 2\n")
    (tmp_path / "lib" / "keys.py").write_text("x = 1\nAPI_KEY = 'xyz'\n")

    result = CliRunner().invoke(cli, ["match", "--diff", "--json"])

    assert result.exit_code == 0, result.output
    output = json.loads(result.stdout)
    assert output["paths"] == {
        "README.md": {"path": "README.md", "scopes": []},
        "lib/keys.py": {"path": "lib/keys.py", "scopes": []},
        "video/player.py": {"path": "video/player.py", "scopes": ["video"]},
    }
    # The removed and added API_KEY lines both match
    assert len(output["code"]) == 2
    for code_match in output["code"].values():
        assert code_match["path"] == "lib/keys.py"
        assert code_match["scopes"] == ["secrets"]


def test_match_rejects_unknown_scope(tmp_path, monkeypatch):
    make_repo(tmp_path, monkeypatch, JSON_REPO)

    result = CliRunner().invoke(cli, ["match", "--scope", "vidoe"])

    assert result.exit_code == 2
    assert "Unknown scope: vidoe" in result.output


def test_match_json_rejects_views_of_the_matches():
    for args in (["--by-scope"], ["--scope", "video"]):
        result = CliRunner().invoke(cli, ["match", "--json", *args])

        assert result.exit_code == 2
        assert "--json can't be combined" in result.output


def test_match_base_matches_the_branch_against_the_base_configs(tmp_path, monkeypatch):
    make_repo(tmp_path, monkeypatch, JSON_REPO)
    run_git_in(tmp_path, "checkout", "-qb", "feature")
    # The branch drops the video scope, but that only applies once it merges
    (tmp_path / "CODEREVIEW.toml").write_text(JSON_CONFIG.replace("video", "other"))
    (tmp_path / "video" / "player.py").unlink()
    (tmp_path / "lib" / "keys.py").write_text("x = 1\nAPI_KEY = 'xyz'\n")
    run_git_in(tmp_path, "commit", "-qam", "change")

    # Committed, so plain --diff sees nothing
    result = CliRunner().invoke(cli, ["match", "--base", "main", "--json"])

    assert result.exit_code == 0, result.output
    output = json.loads(result.stdout)
    assert list(output["scopes"]) == ["video", "secrets"]
    assert output["paths"] == {
        "CODEREVIEW.toml": {"path": "CODEREVIEW.toml", "scopes": []},
        "lib/keys.py": {"path": "lib/keys.py", "scopes": []},
        # Deleted on the branch, still owned
        "video/player.py": {"path": "video/player.py", "scopes": ["video"]},
    }
    assert len(output["code"]) == 2


def test_match_base_explains_a_missing_merge_base(tmp_path, monkeypatch):
    make_repo(tmp_path, monkeypatch, JSON_REPO)
    run_git_in(tmp_path, "checkout", "-q", "--orphan", "unrelated")
    run_git_in(tmp_path, "commit", "-qm", "unrelated")

    result = CliRunner().invoke(cli, ["match", "--base", "main", "--json"])

    assert result.exit_code == 1
    assert "fetch-depth" in result.output


def test_match_base_explains_a_missing_base(tmp_path, monkeypatch):
    make_repo(tmp_path, monkeypatch, JSON_REPO)

    # A shallow clone without the base, and a value git would take for an option
    for base in ("0123456789abcdef0123456789abcdef01234567", "--help"):
        result = CliRunner().invoke(cli, ["match", f"--base={base}", "--json"])

        assert result.exit_code == 1
        assert "Could not find the commit" in result.output
        assert "fetch-depth" in result.output


def test_match_json_lists_deleted_and_staged_files(tmp_path, monkeypatch):
    make_repo(tmp_path, monkeypatch, JSON_REPO)
    (tmp_path / "lib" / "keys.py").unlink()
    (tmp_path / "video" / "player.py").write_text("x = 2\n")
    run_git_in(tmp_path, "add", "video/player.py")
    run_git_in(tmp_path, "mv", "README.md", "README.txt")

    for args in ([], ["--changed"]):
        result = CliRunner().invoke(cli, ["match", "--json", *args])

        assert result.exit_code == 0, result.output
        paths = json.loads(result.stdout)["paths"]
        # Deleted: still listed, but there's no code left to match
        assert paths["lib/keys.py"] == {"path": "lib/keys.py", "scopes": []}
        assert paths["video/player.py"]["scopes"] == ["video"]
        assert "README.txt" in paths

    assert set(paths) == {"lib/keys.py", "video/player.py", "README.txt"}


def test_match_base_rejects_other_modes():
    result = CliRunner().invoke(cli, ["match", "--base", "main", "--changed"])

    assert result.exit_code == 2
    assert "--base" in result.output


AUTHORS_CONFIG = (
    "[[scopes]]\n"
    'name = "teams"\n'
    'paths = ["deploy/**/*"]\n'
    'authors = ["!ci[bot]"]\n'
    "\n"
    "[[scopes]]\n"
    'name = "teams-sync"\n'
    'paths = ["deploy/**/*"]\n'
    'authors = ["ci[bot]"]\n'
)


def test_match_author_decides_which_scope_owns_a_path(tmp_path, monkeypatch):
    make_repo(
        tmp_path,
        monkeypatch,
        {"CODEREVIEW.toml": AUTHORS_CONFIG, "deploy/teams.json": "{}\n"},
    )

    def owners(*args):
        result = CliRunner().invoke(cli, ["match", "--json", *args])
        assert result.exit_code == 0, result.output
        return json.loads(result.stdout)["paths"]["deploy/teams.json"]["scopes"]

    # Without an author nothing is excluded, and the last scope wins the path
    assert owners() == ["teams-sync"]
    assert owners("--author", "doug") == ["teams"]
    assert owners("--author", "ci[bot]") == ["teams-sync"]


def test_match_author_refuses_team_authors(tmp_path, monkeypatch):
    make_repo(
        tmp_path,
        monkeypatch,
        {
            "CODEREVIEW.toml": AUTHORS_CONFIG.replace('"!ci[bot]"', '"!@org/bots"'),
            "deploy/teams.json": "{}\n",
        },
    )

    result = CliRunner().invoke(cli, ["match", "--json", "--author", "doug"])

    assert result.exit_code == 1
    assert "@org/bots" in result.output
