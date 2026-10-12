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


# ---------------------------------------------------------------------------
# Levels: `@probe on|read|off`
# ---------------------------------------------------------------------------


def _level(path) -> str:
    return pc.check(path).level


def test_header_sets_every_line_and_a_suffix_sets_one(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "@probe read\ndata/\nlogs/ @probe off\nREADME.md @probe on\n")
    _write(tmp_path / "data" / "x.csv", "x")
    _write(tmp_path / "logs" / "run.log", "x")
    _write(tmp_path / "README.md", "x")
    _write(tmp_path / "other.py", "x")
    data = pc.check(tmp_path / "data" / "x.csv")
    assert (data.excluded, data.level, data.hidden) == (True, pc.READ, False)
    logs = pc.check(tmp_path / "logs" / "run.log")
    assert (logs.excluded, logs.level, logs.hidden) == (True, pc.OFF, True)
    readme = pc.check(tmp_path / "README.md")
    assert (readme.excluded, readme.level) == (False, pc.ON)
    assert _level(tmp_path / "other.py") == pc.ON


def test_no_header_is_todays_file(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "*.ckpt\n!keep.ckpt\n")
    assert _level(tmp_path / "a.ckpt") == pc.OFF
    assert _level(tmp_path / "keep.ckpt") == pc.ON


def test_a_setting_line_sets_the_lines_after_it(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "data/\n@probe read\nlogs/\n")
    _write(tmp_path / "data" / "x", "x")
    _write(tmp_path / "logs" / "x", "x")
    assert _level(tmp_path / "data" / "x") == pc.OFF
    assert _level(tmp_path / "logs" / "x") == pc.READ


def test_a_header_alone_does_nothing(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "@probe off\n")
    _write(tmp_path / "a.py", "x")
    assert _level(tmp_path / "a.py") == pc.ON


def test_an_off_folder_is_closed_as_git_closes_it(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "secret/\nsecret/important.txt @probe on\n")
    _write(tmp_path / "secret" / pc.CONFIG_NAME, "@probe on\n*\n")
    _write(tmp_path / "secret" / "important.txt", "x")
    verdict = pc.check(tmp_path / "secret" / "important.txt")
    assert verdict.level == pc.OFF and verdict.at == str(tmp_path / "secret")


def test_star_inside_leaves_the_folder_open_for_an_exception(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "secret/*\nsecret/important.txt @probe on\n")
    _write(tmp_path / "secret" / "important.txt", "x")
    _write(tmp_path / "secret" / "other.txt", "x")
    assert _level(tmp_path / "secret" / "important.txt") == pc.ON
    assert _level(tmp_path / "secret" / "other.txt") == pc.OFF


def test_a_read_folder_stays_open(tmp_path):
    _write(
        tmp_path / pc.CONFIG_NAME,
        "notebooks/ @probe read\nnotebooks/private/ @probe off\nnotebooks/public.md @probe on\n",
    )
    _write(tmp_path / "notebooks" / "sub" / pc.CONFIG_NAME, "late.txt @probe off\n")
    for rel in ("a.ipynb", "private/x", "public.md", "sub/late.txt", "sub/deep/y.py"):
        _write(tmp_path / "notebooks" / rel, "x")
    assert _level(tmp_path / "notebooks" / "a.ipynb") == pc.READ
    assert _level(tmp_path / "notebooks" / "private" / "x") == pc.OFF
    assert _level(tmp_path / "notebooks" / "public.md") == pc.ON
    assert _level(tmp_path / "notebooks" / "sub" / "late.txt") == pc.OFF
    assert _level(tmp_path / "notebooks" / "sub" / "deep" / "y.py") == pc.READ


def test_an_unknown_level_counts_as_off_with_a_warning(tmp_path, capsys):
    _write(tmp_path / pc.CONFIG_NAME, "data/ @probe maybe\n@probe sometimes\nlogs/\n")
    _write(tmp_path / "data" / "x", "x")
    _write(tmp_path / "logs" / "x", "x")
    assert _level(tmp_path / "data" / "x") == pc.OFF
    assert _level(tmp_path / "logs" / "x") == pc.OFF
    err = capsys.readouterr().err
    assert "`maybe` is not a level" in err and "`sometimes` is not a level" in err


def test_at_names_stay_patterns(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "@types/\nx \\@probe read\n@probe\n")
    _write(tmp_path / "@types" / "a.d.ts", "x")
    _write(tmp_path / "x @probe read", "x")
    _write(tmp_path / "@probe", "x")
    assert _level(tmp_path / "@types" / "a.d.ts") == pc.OFF
    assert _level(tmp_path / "x @probe read") == pc.OFF
    assert _level(tmp_path / "@probe") == pc.OFF


def test_level_words_ignore_case_and_bang_takes_a_suffix(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "@Probe READ\n*.csv @PROBE OFF\n!keep.csv @probe read\n*.md\n")
    assert _level(tmp_path / "a.csv") == pc.OFF
    assert _level(tmp_path / "keep.csv") == pc.READ
    assert _level(tmp_path / "a.md") == pc.READ  # the header, in any case


def test_suffix_keeps_an_escaped_trailing_space(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "name\\  @probe read\n")
    _write(tmp_path / "name ", "x")
    assert _level(tmp_path / "name ") == pc.READ


def test_check_cwd_gives_the_loosest_level_inside(tmp_path):
    _write(tmp_path / "a" / pc.CONFIG_NAME, "* @probe read\n")
    _write(tmp_path / "b" / pc.CONFIG_NAME, "*\nnotes.md @probe read\n")
    _write(tmp_path / "c" / pc.CONFIG_NAME, "*\n")
    _write(tmp_path / "d" / pc.CONFIG_NAME, "*\nnotes.md @probe on\n")
    assert pc.check_cwd(tmp_path / "a").level == pc.READ
    assert pc.check_cwd(tmp_path / "b").level == pc.READ
    assert pc.check_cwd(tmp_path / "c").level == pc.OFF
    assert not pc.check_cwd(tmp_path / "d").excluded


def test_a_link_takes_the_stricter_level(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "open/ @probe read\nshut/\n")
    _write(tmp_path / "shut" / "x.csv", "x")
    (tmp_path / "open").mkdir()
    (tmp_path / "open" / "link.csv").symlink_to(tmp_path / "shut" / "x.csv")
    assert _level(tmp_path / "open" / "link.csv") == pc.OFF


def test_describe_rule_leaves_the_level_out(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "/notebooks/ @probe read\n*.ckpt @probe off\n")
    loaded = pc._load(str(tmp_path))
    shown = [pc.describe_rule(r) for r in loaded.rules]
    assert shown[0].endswith("/notebooks/") and "@probe" not in shown[0]
    assert shown[1].startswith("*.ckpt under ")


def test_summarize_never_looks_inside_a_closed_folder(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "secret/\nnotebooks/ @probe read\n")
    _write(tmp_path / "secret" / pc.CONFIG_NAME, "inside.txt\n")
    _write(tmp_path / "open" / pc.CONFIG_NAME, "*.ckpt\n")
    entries = pc.summarize(tmp_path).entries
    assert "secret/ under " + pc._display(str(tmp_path)) in entries
    assert any("notebooks/" in e for e in entries)
    assert any("*.ckpt" in e for e in entries)
    assert not any("inside.txt" in e for e in entries)


def test_a_read_rule_above_the_launch_folder_reaches_it(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "repo/notebooks/ @probe read\nrepo/keep @probe on\n")
    (tmp_path / "repo").mkdir()
    parents = pc.parents_reaching(tmp_path / "repo")
    assert [p.folder for p in parents] == [str(tmp_path)]


# ---------------------------------------------------------------------------
# Checker: many checks in a row give `check`'s answers exactly
# ---------------------------------------------------------------------------

_LEVEL_SUFFIXES = ["", "", " @probe read", " @probe off", " @probe on"]


def _random_level_rules(rng: random.Random) -> str:
    lines = []
    if rng.random() < 0.4:
        lines.append("@probe " + rng.choice(pc.LEVELS))
    for _ in range(rng.randint(1, 4)):
        pattern = rng.choice(_PATTERNS)
        if rng.random() < 0.2:
            pattern = "!" + pattern
        lines.append(pattern + rng.choice(_LEVEL_SUFFIXES))
    return "\n".join(lines) + "\n"


@pytest.mark.parametrize("seed", range(120))
def test_checker_gives_checks_answers(tmp_path, seed):
    rng = random.Random(seed)
    root = tmp_path / "repo"
    paths = []
    for folder in _DIRS:
        (root / folder).mkdir(parents=True, exist_ok=True)
    for _ in range(25):
        folder = rng.choice(["", *_DIRS])
        rel = f"{folder}/{rng.choice(_NAMES)}".lstrip("/")
        if (root / rel).is_dir():
            continue
        try:
            _write(root / rel, "x")
        except (IsADirectoryError, NotADirectoryError, FileExistsError):
            continue
    for folder in rng.sample(["", *_DIRS], k=rng.randint(1, 4)):
        _write(((root / folder) if folder else root) / pc.CONFIG_NAME, _random_level_rules(rng))
    for dirpath, dirnames, filenames in os.walk(root):
        paths.extend(os.path.join(dirpath, n) for n in dirnames + filenames)
    expected = {p: pc.check(p) for p in paths}
    for order in (sorted(paths), rng.sample(paths, len(paths))):
        checker = pc.Checker()
        got = {p: checker.check(p) for p in order}
        assert {p: (v.excluded, v.level) for p, v in got.items()} == {
            p: (v.excluded, v.level) for p, v in expected.items()
        }, seed


# ---------------------------------------------------------------------------
# Review round: the read ceiling, off_inside, closed parents
# ---------------------------------------------------------------------------


def test_a_deeper_file_cannot_turn_a_read_folder_back_on(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "clients/ @probe read\nclients/public.md @probe on\n")
    _write(tmp_path / "clients" / "acme" / pc.CONFIG_NAME, "@probe on\n*\nkeys/ @probe off\n")
    _write(tmp_path / "clients" / "acme" / "x.py", "x")
    _write(tmp_path / "clients" / "acme" / "keys" / "k", "x")
    _write(tmp_path / "clients" / "public.md", "x")
    assert _level(tmp_path / "clients" / "acme" / "x.py") == pc.READ  # the deeper `on` is capped
    assert _level(tmp_path / "clients" / "acme" / "keys" / "k") == pc.OFF  # narrowing still works
    assert _level(tmp_path / "clients" / "public.md") == pc.ON  # the same file's exception stands
    checker = pc.Checker()
    assert checker.check(tmp_path / "clients" / "acme" / "x.py").level == pc.READ


def test_off_inside(tmp_path):
    _write(tmp_path / "repo" / "src" / "a.py", "x")
    _write(tmp_path / "repo" / "data" / "rows.csv", "x")
    assert not pc.off_inside(tmp_path / "repo")  # no file anywhere: nothing walked per file
    _write(tmp_path / "repo" / "data" / pc.CONFIG_NAME, "rows.csv\n")
    assert pc.off_inside(tmp_path / "repo")  # a file below the folder
    assert not pc.off_inside(tmp_path / "repo" / "src")
    (tmp_path / "repo" / "data" / pc.CONFIG_NAME).unlink()
    _write(tmp_path / pc.CONFIG_NAME, "*.ckpt\n")
    assert not pc.off_inside(tmp_path / "repo")  # a rule that reaches, but no such file
    _write(tmp_path / "repo" / "src" / "m.ckpt", "x")
    assert pc.off_inside(tmp_path / "repo") and pc.off_inside(tmp_path / "repo" / "src")
    assert pc.off_inside(tmp_path / "repo", max_entries=1)  # cannot finish: counts as holding one


def test_parents_reaching_never_reads_inside_a_closed_folder(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "/closed/\n")
    _write(tmp_path / "closed" / pc.CONFIG_NAME, "@probe on\n*\n")
    (tmp_path / "closed" / "launch").mkdir()
    parents = pc.parents_reaching(tmp_path / "closed" / "launch")
    assert [p.folder for p in parents] == [str(tmp_path)]


def test_witness_is_fast_on_many_globstars(tmp_path):
    rule = pc.parse_line("/" + "/".join(["**", "*"] * 8) + "/x", str(tmp_path), "f", 1)
    started = time.monotonic()
    pc._witness(rule, tuple(f"d{i}" for i in range(20)))
    assert time.monotonic() - started < 0.5


def test_the_read_ceiling_holds_at_every_depth(tmp_path):
    _write(tmp_path / pc.CONFIG_NAME, "clients/ @probe read\n")
    _write(tmp_path / "clients" / pc.CONFIG_NAME, "* @probe on\n")
    for rel in ("a", "sub/b", "sub/deeper/c"):
        _write(tmp_path / "clients" / rel, "x")
        assert _level(tmp_path / "clients" / rel) == pc.READ, rel
        assert pc.Checker().check(tmp_path / "clients" / rel).level == pc.READ, rel


def test_a_broken_check_fails_closed(tmp_path, monkeypatch):
    monkeypatch.setattr(pc, "_check_one", lambda *a, **k: 1 / 0)
    assert pc.check(tmp_path / "x").hidden
