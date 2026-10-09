"""`.probe.config`: the gitignore-style list of paths Probe never records.

The matcher is our own (stdlib-only, so the hooks and the tap can carry it), so
its answer key is git itself: random trees with the same rules written as
`.gitignore` and `.probe.config`, compared against `git ls-files -o -i
--exclude-standard`, which walks folders the way git really applies them
(an excluded folder cannot have a file re-included under it).
"""

from __future__ import annotations

import json
import os
import random
import shutil
import stat
import subprocess
import sys
import time

import pytest

from probe.sdk import probe_config as pc


@pytest.fixture(autouse=True)
def _fresh_cache():
    pc._CACHE.clear()
    pc._WARNED.clear()
    yield
    pc._CACHE.clear()


def _write(path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Git is the answer key
# ---------------------------------------------------------------------------

_NAMES = ["a", "b", "c.txt", "d.log", "data", "x1", "keep.csv", "B"]
_DIRS = ["a", "b", "data", "x1", "a/b", "data/a", "b/data", "a/b/c"]
_PATTERNS = [
    "*", "/*", "*.txt", "*.log", "a", "/a", "a/", "/a/", "data/", "b/data", "a/b", "**/b",
    "a/**", "a/**/c.txt", "**/data/**", "[ab]", "[!a]*", "?", "?.txt", "d*", "*1", "x[0-9]",
    "data/*", "/data/keep.csv", "keep.csv", "b/", "**", "a/*/c.txt", "\\!x", "B", "[a-c]*",
    "*.[tl][xo][tg]", "**/a/b",
]


def _random_rules(rng: random.Random) -> str:
    lines = []
    for _ in range(rng.randint(1, 4)):
        pattern = rng.choice(_PATTERNS)
        if rng.random() < 0.3:
            pattern = "!" + pattern
        lines.append(pattern)
    if rng.random() < 0.2:
        lines.insert(0, "# a comment")
    return "\n".join(lines) + "\n"


def _git_ignored(root) -> set[str]:
    out = subprocess.run(
        ["git", "ls-files", "-o", "-i", "--exclude-standard", "-z"],
        cwd=root, capture_output=True, check=True,
    ).stdout.decode()
    return {p for p in out.split("\0") if p}


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
@pytest.mark.parametrize("seed", range(150))
def test_matches_git_on_random_trees(tmp_path, seed):
    rng = random.Random(seed)
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "."], cwd=root, check=True)
    files = set()
    for _ in range(14):
        folder = rng.choice(["", *_DIRS])
        name = rng.choice(_NAMES)
        rel = f"{folder}/{name}".lstrip("/")
        if any(rel == d or rel.startswith(d + "/") for d in _DIRS if d.startswith(rel + "/")):
            continue
        target = root / rel
        if target.is_dir():
            continue
        try:
            _write(target, "x")
        except (IsADirectoryError, NotADirectoryError, FileExistsError):
            continue
        files.add(rel)
    for folder in rng.sample(["", *_DIRS], k=rng.randint(1, 3)):
        base = root / folder if folder else root
        if not base.is_dir():
            continue
        rules = _random_rules(rng)
        _write(base / ".gitignore", rules)
        _write(base / pc.CONFIG_NAME, rules)
    git = {p for p in _git_ignored(root) if not p.endswith((".gitignore", pc.CONFIG_NAME))}
    ours = {rel for rel in files if (root / rel).is_file() and pc.check(root / rel).excluded}
    assert ours == git, (seed, sorted(ours ^ git))


# ---------------------------------------------------------------------------
# The shapes the docs promise
# ---------------------------------------------------------------------------


def test_only_some_repos(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "/*\n!/repo-a/\n")
    _write(tmp_path / "repo-a" / "train.py")
    _write(tmp_path / "repo-a" / "src" / "m.py")
    _write(tmp_path / "repo-b" / "x.py")
    assert not pc.check(tmp_path / "repo-a" / "train.py").excluded
    assert not pc.check(tmp_path / "repo-a" / "src" / "m.py").excluded
    verdict = pc.check(tmp_path / "repo-b" / "x.py")
    assert verdict.excluded
    assert verdict.at == str(tmp_path / "repo-b")
    assert verdict.rule.pattern == "/*"


def test_star_then_bang_does_not_allow_a_repo(tmp_path):
    # The classic trap: `*` matches at every depth, so repo-a's files stay out.
    _write(tmp_path / pc.CONFIG_NAME, "*\n!repo-a/\n")
    _write(tmp_path / "repo-a" / "train.py")
    assert pc.check(tmp_path / "repo-a" / "train.py").excluded


def test_inherits_and_deeper_file_wins(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "*.ckpt\n")
    _write(tmp_path / "repo" / "keep" / pc.CONFIG_NAME, "!*.ckpt\n")
    assert pc.check(tmp_path / "repo" / "model.ckpt").excluded
    assert not pc.check(tmp_path / "repo" / "keep" / "model.ckpt").excluded


def test_no_file_anywhere_excludes_nothing(tmp_path):
    assert pc.check(tmp_path / "a" / "b.txt") == pc.NOT_EXCLUDED


def test_relative_path_and_tilde(tmp_path, monkeypatch):
    _write(tmp_path / pc.CONFIG_NAME, "data/\n")
    _write(tmp_path / "data" / "x")
    assert pc.check("data/x", cwd=str(tmp_path)).excluded
    monkeypatch.setenv("HOME", str(tmp_path))
    assert pc.check("~/data/x").excluded


def test_symlink_into_excluded_folder(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "/secret/\n")
    _write(tmp_path / "secret" / "x.txt")
    (tmp_path / "link").symlink_to(tmp_path / "secret")
    assert pc.check(tmp_path / "link" / "x.txt").excluded


def test_dir_only_pattern_needs_a_dir(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "out/\n")
    _write(tmp_path / "out")  # a FILE named out
    assert not pc.check(tmp_path / "out").excluded
    assert pc.check(tmp_path / "x" / "out", is_dir=True).excluded


def test_check_cwd(tmp_path):
    _write(tmp_path / "repo" / pc.CONFIG_NAME, "*\n")
    assert pc.check_cwd(tmp_path / "repo").excluded
    _write(tmp_path / "other" / pc.CONFIG_NAME, "*.ckpt\n")
    assert not pc.check_cwd(tmp_path / "other").excluded
    _write(tmp_path / pc.CONFIG_NAME, "/third/\n")
    (tmp_path / "third").mkdir()
    assert pc.check_cwd(tmp_path / "third").excluded


# ---------------------------------------------------------------------------
# Fails closed; skips what git skips
# ---------------------------------------------------------------------------


@pytest.mark.skipif(os.geteuid() == 0 if hasattr(os, "geteuid") else True, reason="root reads anything")
def test_unreadable_file_excludes_its_folder(tmp_path, capsys):
    cfg = tmp_path / pc.CONFIG_NAME
    _write(cfg, "nothing-matches\n")
    cfg.chmod(0)
    try:
        verdict = pc.check(tmp_path / "any" / "file.py")
        assert verdict.excluded and verdict.rule.pattern == "unreadable"
        assert "could not be read" in capsys.readouterr().err
    finally:
        cfg.chmod(stat.S_IRUSR | stat.S_IWUSR)


def test_fifo_and_directory_fail_closed_without_hanging(tmp_path):
    if not hasattr(os, "mkfifo"):
        pytest.skip("no fifo")
    a = tmp_path / "a"
    a.mkdir()
    os.mkfifo(a / pc.CONFIG_NAME)
    started = time.monotonic()
    assert pc.check(a / "x").excluded
    assert time.monotonic() - started < 2
    b = tmp_path / "b"
    (b / pc.CONFIG_NAME).mkdir(parents=True)
    assert pc.check(b / "x").excluded


def test_oversize_fails_closed(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "x\n" * (pc.MAX_BYTES // 2 + 10))
    assert pc.check(tmp_path / "y").excluded


def test_bad_pattern_is_skipped_with_a_warning(tmp_path, capsys):
    _write(tmp_path / pc.CONFIG_NAME, "abc[\n*.log\n")
    assert not pc.check(tmp_path / "abc[").excluded
    assert pc.check(tmp_path / "x.log").excluded
    assert f"{pc.CONFIG_NAME}:1` is not a valid pattern" in capsys.readouterr().err


def test_bom_crlf_and_utf16(tmp_path):
    _write(tmp_path / "a" / pc.CONFIG_NAME, "")
    (tmp_path / "a" / pc.CONFIG_NAME).write_bytes(b"\xef\xbb\xbfdata/\r\n")
    _write(tmp_path / "a" / "data" / "x")
    assert pc.check(tmp_path / "a" / "data" / "x").excluded
    (tmp_path / "b").mkdir()
    (tmp_path / "b" / pc.CONFIG_NAME).write_bytes("*.ckpt\n".encode("utf-16"))
    assert pc.check(tmp_path / "b" / "m.ckpt").excluded


def test_pathological_pattern_is_fast(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "*a*a*a*a*a*a*a*a*a*a*a*a*b\n")
    name = "a" * 250
    started = time.monotonic()
    assert not pc.check(tmp_path / name).excluded
    assert time.monotonic() - started < 0.5


def test_check_never_raises(tmp_path):
    assert pc.check("\0bad") == pc.NOT_EXCLUDED


# ---------------------------------------------------------------------------
# Retired folder defaults (#1252) count as `*` until converted
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("stored", "excluded"),
    [({"session_state": "off"}, True), ({"session_state": "read-only"}, True),
     ({"session_tracking": False}, True), ({"session_state": "full"}, False),
     ({"session_tracking": True}, False)],
)
def test_legacy_folder_default(tmp_path, stored, excluded):
    _write(tmp_path / "repo" / ".probe" / "config.json", json.dumps({"defaults": stored}))
    verdict = pc.check(tmp_path / "repo" / "x.py", legacy=True)
    assert verdict.excluded is excluded
    if excluded:
        assert "retired folder default" in verdict.rule.pattern
    # Outside an agent session (a terminal, a training node) a retired default
    # never applied, and still does not: no run is silently disabled.
    assert not pc.check(tmp_path / "repo" / "x.py").excluded


def test_legacy_default_reader(tmp_path):
    assert pc.legacy_default(str(tmp_path)) is None
    _write(tmp_path / ".probe" / "config.json", json.dumps({"defaults": {"session_state": "read-only"}}))
    assert pc.legacy_default(str(tmp_path)) == "read-only"
    _write(tmp_path / ".probe" / "config.json", "not json")
    assert pc.legacy_default(str(tmp_path)) is None


# ---------------------------------------------------------------------------
# Files above the launch folder, and the session's answer
# ---------------------------------------------------------------------------


def test_parents_reaching(tmp_path):
    launch = tmp_path / "code" / "repo-a"
    launch.mkdir(parents=True)
    _write(tmp_path / "code" / pc.CONFIG_NAME, "/repo-b/\n")  # a sibling only
    assert pc.parents_reaching(launch) == []
    _write(tmp_path / "code" / pc.CONFIG_NAME, "/repo-a/data/\n")
    assert [p.folder for p in pc.parents_reaching(launch)] == [str(tmp_path / "code")]
    _write(tmp_path / "code" / pc.CONFIG_NAME, "*.ckpt\n")  # unanchored reaches anywhere
    assert len(pc.parents_reaching(launch)) == 1
    _write(tmp_path / "code" / pc.CONFIG_NAME, "!/repo-a/\n")  # a re-include alone excludes nothing
    assert pc.parents_reaching(launch) == []
    _write(tmp_path / pc.CONFIG_NAME, "/code/\n")  # an ancestor of the launch folder
    assert [p.folder for p in pc.parents_reaching(launch)] == [str(tmp_path)]


def test_launch_folder_file_is_not_a_parent(tmp_path):
    launch = tmp_path / "repo"
    _write(launch / pc.CONFIG_NAME, "*\n")
    assert pc.parents_reaching(launch) == []


def test_session_answer_flow(tmp_path):
    sessions = tmp_path / "sessions"
    sid = "11111111-2222-3333-4444-555555555555"
    launch = tmp_path / "code" / "repo-a"
    launch.mkdir(parents=True)
    _write(tmp_path / "code" / pc.CONFIG_NAME, "/*\n")
    _write(launch / pc.CONFIG_NAME, "secret/\n")
    target = launch / "train.py"
    _write(target)

    assert pc.session_check(target, sessions, sid).excluded  # no launch dir recorded: all files apply
    assert pc.record_launch_dir(sessions, sid, str(launch))
    assert not pc.record_launch_dir(sessions, sid, str(tmp_path))  # first one sticks
    assert pc.launch_dir(sessions, sid) == str(launch)

    status, parents = pc.parent_status(sessions, sid)
    assert status == pc.UNASKED and len(parents) == 1
    assert pc.session_check(target, sessions, sid).excluded  # unanswered: followed
    pc.mark_asked(sessions, sid, parents)
    assert pc.parent_status(sessions, sid)[0] == pc.PENDING

    ok, _ = pc.record_answer(sessions, sid, pc.IGNORE)
    assert ok and pc.parent_status(sessions, sid)[0] == pc.IGNORE
    assert not pc.session_check(target, sessions, sid).excluded
    # The launch folder's own file still applies.
    assert pc.session_check(launch / "secret" / "k", sessions, sid, is_dir=False).excluded

    # The parent file changes: the answer is void, asked again, followed meanwhile.
    _write(tmp_path / "code" / pc.CONFIG_NAME, "/*\n*.ckpt\n")
    assert pc.parent_status(sessions, sid)[0] == pc.UNASKED
    assert pc.session_check(target, sessions, sid).excluded

    pc.record_answer(sessions, sid, pc.FOLLOW)
    assert pc.parent_status(sessions, sid)[0] == pc.FOLLOW
    assert pc.session_check(target, sessions, sid).excluded
    with pytest.raises(ValueError):
        pc.record_answer(sessions, sid, "maybe")


def test_no_parent_means_nothing_to_ask(tmp_path):
    sessions = tmp_path / "s"
    sid = "11111111-2222-3333-4444-555555555556"
    pc.record_launch_dir(sessions, sid, str(tmp_path))
    assert pc.parent_status(sessions, sid) == ("", [])


# ---------------------------------------------------------------------------
# What a session is told at start
# ---------------------------------------------------------------------------


def test_summarize(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "/repo/data/\n")
    _write(tmp_path / "repo" / "sub" / pc.CONFIG_NAME, "*.ckpt\n!keep.ckpt\n")
    (tmp_path / "repo" / "node_modules").mkdir(parents=True)
    _write(tmp_path / "repo" / "node_modules" / pc.CONFIG_NAME, "ignored-by-scan\n")
    out = pc.summarize(tmp_path / "repo")
    assert any(e.endswith("repo/data/") for e in out.entries)
    assert any(e.startswith("*.ckpt under ") for e in out.entries)
    assert not any("ignored-by-scan" in e for e in out.entries)
    assert not any("keep.ckpt" in e for e in out.entries)
    assert pc.summarize(tmp_path / "repo", skip=frozenset({str(tmp_path)})).entries == [
        e for e in out.entries if not e.endswith("repo/data/")
    ]


def test_summarize_whole_folder(tmp_path):
    _write(tmp_path / "repo" / pc.CONFIG_NAME, "*\n")
    out = pc.summarize(tmp_path / "repo")
    assert out.entries[0].startswith("this folder (")


def test_module_is_stdlib_only():
    import ast
    import pathlib

    tree = ast.parse(pathlib.Path(pc.__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert node.level == 0 and node.module and not node.module.startswith("probe"), node.module
            assert node.module.split(".")[0] in sys.stdlib_module_names | {"__future__"}
        elif isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] in sys.stdlib_module_names, alias.name


# ---------------------------------------------------------------------------
# Review fixes
# ---------------------------------------------------------------------------


def test_ignore_sets_aside_only_the_files_it_was_about(tmp_path, monkeypatch):
    """`~/.probe.config` `/private/` never reaches `~/code/repo-a`, so it is not
    asked about; an `ignore` for `~/code/.probe.config` must not drop it."""
    sessions = tmp_path / "sessions"
    sid = "11111111-2222-3333-4444-555555555557"
    home = tmp_path / "home"
    launch = home / "code" / "repo-a"
    launch.mkdir(parents=True)
    _write(home / pc.CONFIG_NAME, "/private/\n")
    _write(home / "code" / pc.CONFIG_NAME, "scratch/\n")
    _write(home / "private" / "x.csv")
    pc.record_launch_dir(sessions, sid, str(launch))
    status, parents = pc.parent_status(sessions, sid)
    assert [p.folder for p in parents] == [str(home / "code")]
    pc.record_answer(sessions, sid, pc.IGNORE)
    assert pc.session_check(home / "private" / "x.csv", sessions, sid).excluded
    assert not pc.session_check(launch / "scratch" / "y", sessions, sid, is_dir=False).excluded


def test_check_cwd_counts_parent_rules(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "repo-b/**\n")
    (tmp_path / "repo-b").mkdir()
    (tmp_path / "repo-a").mkdir()
    assert pc.check_cwd(tmp_path / "repo-b").excluded
    assert not pc.check_cwd(tmp_path / "repo-a").excluded


def test_dangling_symlink_config_fails_closed(tmp_path):
    (tmp_path / "repo").mkdir()
    (tmp_path / "repo" / pc.CONFIG_NAME).symlink_to(tmp_path / "unmounted" / "probe.config")
    verdict = pc.check(tmp_path / "repo" / "x.py")
    assert verdict.excluded and verdict.rule.pattern == "unreadable"


def test_dotdot_through_a_link_is_the_file_the_os_opens(tmp_path):
    """`link/../secret.txt` opens deep/secret.txt (the link resolves before `..`);
    normpath alone would check tmp/secret.txt and miss deep's rule."""
    (tmp_path / "deep" / "inner").mkdir(parents=True)
    (tmp_path / "link").symlink_to(tmp_path / "deep" / "inner")
    _write(tmp_path / "deep" / "secret.txt", "y")
    _write(tmp_path / "deep" / pc.CONFIG_NAME, "secret.txt\n")
    assert not pc.check(tmp_path / "secret.txt").excluded
    assert pc.check(str(tmp_path / "link") + "/../secret.txt").excluded


def test_a_path_too_long_or_through_a_file_is_absent_not_unreadable(tmp_path, capsys):
    """Only a `.probe.config` that exists and cannot be read fails closed."""
    (tmp_path / "f").write_text("x")
    assert not pc.check(tmp_path / "f" / "below.py").excluded  # ENOTDIR
    assert not pc.check(tmp_path / ("n" * 300) / "x.py").excluded  # ENAMETOOLONG
    assert "could not be read" not in capsys.readouterr().err


def test_check_cwd_respects_a_reinclude_inside(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "repo-b/*\n!repo-b/keep/\n")
    (tmp_path / "repo-b" / "keep").mkdir(parents=True)
    assert not pc.check(tmp_path / "repo-b" / "keep" / "out.txt").excluded
    assert not pc.check_cwd(tmp_path / "repo-b").excluded
    _write(tmp_path / "own" / pc.CONFIG_NAME, "*\n!train.py\n")
    assert not pc.check_cwd(tmp_path / "own").excluded


def test_local_path_of():
    assert pc.local_path_of("file:///a%20b/c.pt") == "/a b/c.pt"
    assert pc.local_path_of("file://localhost/x") == "/x"
    assert pc.local_path_of("file://otherhost/x") is None
    assert pc.local_path_of("s3://bucket/x") is None
    assert pc.local_path_of(None) is None


def test_session_view_includes_real_paths(tmp_path):
    real_home = tmp_path / "real-home"
    (real_home / "code" / "repo-a").mkdir(parents=True)
    (tmp_path / "home").symlink_to(real_home)
    _write(real_home / "code" / pc.CONFIG_NAME, "/*\n")
    sessions = tmp_path / "s"
    sid = "11111111-2222-3333-4444-55555555555b"
    pc.record_launch_dir(sessions, sid, str(tmp_path / "home" / "code" / "repo-a"))
    pc.record_answer(sessions, sid, pc.IGNORE)
    _start, skip = pc.session_view(sessions, sid)
    assert str(real_home / "code") in skip
    assert not pc.session_check(real_home / "code" / "repo-a" / "t.py", sessions, sid, is_dir=False).excluded


@pytest.mark.parametrize(
    "files, cwd",
    [
        ({"": "/*\n!/data/\n/data/private/*\n"}, "data/private"),  # `!` names a parent, not inside
        ({"repo": "!keep.py\n*\n"}, "repo"),  # last match wins
        ({"repo": "*\n!sub/train.py\n"}, "repo"),  # sub/ is excluded: nothing below comes back
        ({"": "!*.md\n", "repo": "*\n"}, "repo"),  # the deeper file wins
    ],
)
def test_check_cwd_is_not_fooled_by_a_reinclude_that_reinclues_nothing(tmp_path, files, cwd):
    for folder, text in files.items():
        _write(tmp_path / folder / pc.CONFIG_NAME, text)
    (tmp_path / cwd).mkdir(parents=True, exist_ok=True)
    assert pc.check_cwd(tmp_path / cwd).excluded


def test_check_cwd_unreadable_child_and_parent_reinclude_fails_closed(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "!*.md\n")
    (tmp_path / "repo").mkdir()
    (tmp_path / "repo" / pc.CONFIG_NAME).symlink_to(tmp_path / "gone")
    assert pc.check_cwd(tmp_path / "repo").excluded
