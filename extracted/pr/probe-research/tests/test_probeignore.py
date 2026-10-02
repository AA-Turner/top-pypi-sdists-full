"""`.probeignore` loading and matching (plan (n), D22)."""

from __future__ import annotations

import os
import subprocess
import sys
import warnings

import pytest

from probe.sdk import ignore


def _repo(root):
    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    return root


def test_nothing_configured_is_none_and_imports_nothing(tmp_path, monkeypatch):
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    monkeypatch.delenv(ignore.ENV_FILE, raising=False)
    monkeypatch.delitem(sys.modules, "pathspec", raising=False)
    assert ignore.load(str(tmp_path)) is None
    assert "pathspec" not in sys.modules, "opt-in: no pattern, no import"
    (tmp_path / ".probeignore").write_text("# only a comment\n\n")
    assert ignore.load(str(tmp_path)) is None, "no default patterns (D22)"


def test_the_file_at_the_git_toplevel_applies_from_a_subdirectory(tmp_path, monkeypatch):
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    repo = _repo(tmp_path / "repo")
    (repo / ".probeignore").write_text("*.log\n!keep.log\ndata/\n/top.txt\n")
    sub = repo / "src" / "pkg"
    sub.mkdir(parents=True)
    rules = ignore.load(str(sub))
    assert rules is not None and os.path.realpath(rules.root) == os.path.realpath(repo)
    assert rules.source_file and rules.source_file.endswith(".probeignore")
    assert rules.ignored("a.log") and rules.ignored("src/pkg/b.log")
    assert not rules.ignored("keep.log"), "! undoes an earlier .probeignore line"
    assert rules.ignored("data/x.csv") and rules.ignored("src/data/y")
    assert rules.ignored("data", is_dir=True) and not rules.ignored("data")
    assert rules.ignored("top.txt") and not rules.ignored("src/top.txt"), "anchored to the root"
    # Relative to a base, or absolute. Outside the root only the UNANCHORED
    # patterns apply (review MED-1): `*.log` does, `/top.txt` cannot.
    assert rules.ignored("b.log", base=str(sub))
    assert rules.ignored(str(sub / "b.log"))
    assert rules.ignored(str(tmp_path / "elsewhere.log"))
    assert not rules.ignored(str(tmp_path / "top.txt"))


@pytest.mark.parametrize("git", [True, False])
def test_a_path_through_a_symlink_matches_like_the_real_one(tmp_path, monkeypatch, git):
    """git's toplevel is resolved and a plain directory's root is not, while a
    read, an output folder or a working directory can come through either
    form. Both match; a link's OWN name is what a pattern sees."""
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    real = _repo(tmp_path / "real") if git else tmp_path / "real"
    (real / "data").mkdir(parents=True)
    (real / ".probeignore").write_text("data/\nlinked.csv\n")
    link = tmp_path / "link"
    link.symlink_to(real, target_is_directory=True)
    (real / "target.csv").write_text("x")
    (real / "linked.csv").symlink_to(real / "target.csv")
    for start in (link, real):
        rules = ignore.load(str(start))
        assert rules is not None
        for top in (link, real):
            assert rules.ignored(str(top / "data" / "a.csv")), (start, top)
            assert rules.ignored("data/a.csv", base=str(top)), (start, top)
            assert rules.ignored(str(top / "data"), is_dir=True), (start, top)
            assert rules.ignored(str(top / "linked.csv")) and not rules.ignored(str(top / "target.csv"))
        assert rules.ignored(str(tmp_path / "data" / "a.csv")), "unanchored: outside the root too"
        assert not rules.ignored(str(tmp_path / "target.csv"))


def test_outside_a_repo_the_working_directory_is_the_root(tmp_path, monkeypatch):
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    (tmp_path / ".probeignore").write_text("scratch/\n")
    rules = ignore.load(str(tmp_path))
    assert rules is not None and rules.root == str(tmp_path)
    assert rules.ignored("scratch/a.py") and not rules.ignored("train.py")


def test_env_and_init_patterns_add_to_the_file(tmp_path, monkeypatch):
    (tmp_path / ".probeignore").write_text("*.log\n")
    monkeypatch.setenv(ignore.ENV_PATTERNS, "ckpt/, *.tmp\nwandb/")
    rules = ignore.load(str(tmp_path), extra=["*.npy"])
    assert rules is not None
    for path in ("x.log", "ckpt/a.pt", "a.tmp", "wandb/run/x", "arr.npy"):
        assert rules.ignored(path), path
    assert not rules.ignored("train.py")
    monkeypatch.delenv(ignore.ENV_PATTERNS)
    (tmp_path / ".probeignore").unlink()
    only_init = ignore.load(str(tmp_path), extra=["*.npy"])
    assert only_init is not None and only_init.source_file is None and only_init.ignored("a.npy")


def test_the_exported_file_wins_over_the_lookup(tmp_path, monkeypatch):
    """`probe exec` exports PROBE_IGNORE_FILE so a child that `cd`s elsewhere
    still reads the parent's file, matched against the parent's root."""
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    parent = tmp_path / "parent"
    parent.mkdir()
    (parent / ".probeignore").write_text("secret_data/\n")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / ".probeignore").write_text("*.py\n")
    monkeypatch.setenv(ignore.ENV_FILE, str(parent / ".probeignore"))
    rules = ignore.load(str(elsewhere))
    assert rules is not None and rules.root == str(parent)
    assert rules.ignored(str(parent / "secret_data" / "x.csv"))
    assert not rules.ignored(str(elsewhere / "train.py")), "outside the exported root"


def test_a_bad_pattern_is_dropped_loudly_not_fatally(tmp_path, monkeypatch):
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    import pathspec

    real = pathspec.GitIgnoreSpec.from_lines

    def picky(lines):
        lines = list(lines)
        if "BAD" in lines:
            raise ValueError("bad pattern")
        return real(lines)

    monkeypatch.setattr(pathspec.GitIgnoreSpec, "from_lines", staticmethod(picky))
    (tmp_path / ".probeignore").write_text("*.log\nBAD\n")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        rules = ignore.load(str(tmp_path))
    assert rules is not None and rules.ignored("a.log") and rules.patterns == ("*.log",)
    assert any("are ignored" in str(w.message) and "'BAD'" in str(w.message) for w in caught)


def test_split_patterns():
    assert ignore.split_patterns(None) == []
    assert ignore.split_patterns(" a/ ,b.log\n\n c ") == ["a/", "b.log", "c"]


@pytest.mark.skipif(os.name == "nt", reason="posix paths")
def test_no_git_binary_falls_back_to_the_working_directory(tmp_path, monkeypatch):
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    repo = _repo(tmp_path / "repo")
    (repo / ".probeignore").write_text("*.log\n")
    sub = repo / "sub"
    sub.mkdir()
    (sub / ".probeignore").write_text("*.tmp\n")
    empty = tmp_path / "empty-bin"
    empty.mkdir()
    monkeypatch.setenv("PATH", str(empty))
    rules = ignore.load(str(sub))
    assert rules is not None and rules.root == str(sub) and rules.ignored("a.tmp")


# -- the #2045 review ----------------------------------------------------------


def _file_rules(tmp_path, text, extra=()):
    (tmp_path / ".probeignore").write_text(text)
    return ignore.load(str(tmp_path), extra=list(extra))


def test_outside_the_root_only_unanchored_patterns_apply(tmp_path, monkeypatch):
    """MED-1. A read outside the root (no capture root): unanchored patterns,
    against the whole path. With a capture root (an `outputs=` folder): the
    file's unanchored patterns and EVERY ignore= / PROBE_IGNORE one, relative
    to that folder. Anchored file patterns never apply out there."""
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    root = tmp_path / "repo"
    root.mkdir()
    rules = _file_rules(root, "*.jsonl\nckpt/\n/data\nruns/*/dump\n", extra=["/tmp", "*.ckpt"])
    far = tmp_path / "scratch"
    # A read: no capture root.
    assert rules.ignored(str(far / "rows.jsonl")) and rules.ignored(str(far / "a" / "ckpt" / "w.pt"))
    assert rules.ignored(str(far / "m.ckpt"))
    assert not rules.ignored(str(far / "data" / "x.csv")), "anchored file pattern"
    assert not rules.ignored(str(far / "tmp" / "x")), "anchored ignore= pattern: no root to anchor to"
    assert not rules.ignored(str(far / "results.csv"))
    # An output sweep of `far`.
    assert rules.ignored(str(far / "tmp" / "x"), capture_root=str(far)), "ignore= anchors to the folder"
    assert rules.ignored(str(far / "rows.jsonl"), capture_root=str(far))
    assert not rules.ignored(str(far / "data" / "x.csv"), capture_root=str(far))
    assert not rules.ignored(str(far / "runs" / "1" / "dump"), capture_root=str(far))
    # Inside the root nothing changed.
    assert rules.ignored(str(root / "data" / "x.csv")) and rules.ignored(str(root / "runs" / "1" / "dump"))
    assert not rules.ignored(str(root / "sub" / "data" / "x.csv"))


def test_unreachable_names_the_anchored_file_patterns(tmp_path, monkeypatch):
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    rules = _file_rules(tmp_path, "*.jsonl\n/data\nruns/*/dump\n**/tmp\n", extra=["/x"])
    assert rules.unreachable(str(tmp_path.parent / "scratch")) == ("/data", "runs/*/dump")
    assert rules.unreachable(str(tmp_path / "out")) == (), "inside the root: all apply"


def test_a_bom_does_not_eat_the_first_pattern(tmp_path, monkeypatch):
    """LOW-2: a Windows editor's UTF-8 BOM used to glue itself to line one."""
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    (tmp_path / ".probeignore").write_bytes(b"\xef\xbb\xbf*.jsonl\nckpt/\n")
    rules = ignore.load(str(tmp_path))
    assert rules is not None and rules.patterns == ("*.jsonl", "ckpt/")
    assert rules.ignored("rows.jsonl")


def test_a_costly_pattern_is_skipped_loudly_and_matching_stays_fast(tmp_path, monkeypatch):
    """LOW-4: `*a*a*a*a*a*a*a*a*b` backtracked for 51 s on one 60-character
    name, in probe.init and on every open() the read hook saw."""
    import time

    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    evil = "*a" * 8 + "*b"
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        rules = _file_rules(tmp_path, f"{evil}\n*.log\n**/x/**/y/*.z\n")
    assert rules is not None and rules.patterns == ("*.log", "**/x/**/y/*.z")
    assert any("too costly" in str(w.message) for w in caught)
    started = time.perf_counter()
    for _ in range(200):
        rules.ignored("a" * 59 + "c")
    assert time.perf_counter() - started < 1.0
    assert ignore.load(str(tmp_path), extra=["*a*a*b"]).ignored("xaab"), "three stars are fine"


def test_file_size_and_line_count_are_capped(tmp_path, monkeypatch):
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    lines = [f"f{i}.txt" for i in range(ignore.MAX_PATTERNS + 50)]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        rules = _file_rules(tmp_path, "\n".join(lines) + "\n")
    assert len(rules.patterns) == ignore.MAX_PATTERNS and rules.ignored("f0.txt")
    assert not rules.ignored(f"f{ignore.MAX_PATTERNS + 1}.txt")
    assert any(f"past the first {ignore.MAX_PATTERNS}" in str(w.message) for w in caught)
    (tmp_path / ".probeignore").write_text("*.log\n" + "#" * (ignore.MAX_FILE_BYTES + 10) + "\n*.late\n")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        big = ignore.load(str(tmp_path))
    assert big.patterns == ("*.log",) and any("only its first" in str(w.message) for w in caught)


def test_a_negation_never_reaches_into_an_excluded_folder(tmp_path, monkeypatch):
    """LOW-5, as in git: `secrets/` then `!secrets/notes.md` keeps notes.md
    OUT (read capture used to send its path and hash); `data/*` then
    `!data/keep.csv` re-includes, because the folder itself is not excluded."""
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    rules = _file_rules(tmp_path, "secrets/\n!secrets/notes.md\ndata/*\n!data/keep.csv\n")
    assert rules.ignored(str(tmp_path / "secrets" / "notes.md"))
    assert rules.ignored(str(tmp_path / "secrets" / "deep" / "x"))
    assert rules.ignored(str(tmp_path / "data" / "drop.csv"))
    assert not rules.ignored(str(tmp_path / "data" / "keep.csv")), "control: the folder is not excluded"


def test_a_path_on_another_drive_is_simply_not_matched(tmp_path, monkeypatch):
    """LOW-6: `os.path.relpath` raises ValueError across Windows drives."""
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    rules = _file_rules(tmp_path, "/data\n")

    def cross_drive(path, start=None):
        raise ValueError("path is on mount 'D:', start on mount 'C:'")

    monkeypatch.setattr(ignore.os.path, "relpath", cross_drive)
    assert rules.ignored(str(tmp_path / "data" / "x")) is False
    assert rules.unreachable(str(tmp_path)) == ("/data",)


def test_a_leading_space_is_part_of_the_pattern(tmp_path, monkeypatch):
    """As in git; pathspec before 1.0 stripped it (hence `pathspec>=1.0`)."""
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    rules = _file_rules(tmp_path, " notes.txt\n")
    assert rules.ignored(" notes.txt") and not rules.ignored("notes.txt")


def test_matching_is_case_sensitive(tmp_path, monkeypatch):
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    rules = _file_rules(tmp_path, "Data/\n")
    assert rules.ignored("Data/x") and not rules.ignored("data/x")


def test_exported_patterns_keep_their_commas(monkeypatch, tmp_path):
    """LOW-7: `probe exec` exports ignore= in PROBE_IGNORE_EXPORTED, one per
    line, because PROBE_IGNORE splits on commas."""
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    monkeypatch.setenv(ignore.ENV_EXPORTED, ignore.join_lines(["a,b.bin", "*.ckpt"]))
    rules = ignore.load(str(tmp_path))
    assert rules.patterns == ("a,b.bin", "*.ckpt") and rules.ignored("a,b.bin")
    assert ignore.split_patterns("a,b.bin") == ["a", "b.bin"], "PROBE_IGNORE still splits (documented)"


def test_a_record_keeps_which_patterns_came_from_the_file(tmp_path, monkeypatch):
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    rules = _file_rules(tmp_path, "/data\n", extra=["/tmp"])
    rebuilt = ignore.from_record(ignore.to_record(rules))
    far = tmp_path.parent / "scratch"
    assert rebuilt.n_file == 1 and rebuilt.unreachable(str(far)) == ("/data",)
    assert rebuilt.ignored(str(far / "tmp" / "x"), capture_root=str(far))


# -- the #2045 re-review ---------------------------------------------------------


def test_a_trailing_space_never_anchors_a_pattern(tmp_path, monkeypatch):
    """LOW: `ckpt/ ` read as anchored (the space made `/` look inner), so it
    was dropped outside the root and named in the anchored warning. git trims
    unescaped trailing spaces first; so does this."""
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    rules = _file_rules(tmp_path, "ckpt/ \n*.jsonl  \nkeep\\ \n", extra=["*.bin "])
    assert rules.patterns == ("ckpt/", "*.jsonl", "keep\\ ", "*.bin")
    far = tmp_path.parent / "scratch"
    assert rules.unreachable(str(far)) == (), "nothing anchored"
    assert rules.ignored(str(far / "run" / "ckpt" / "w.pt")), "applies outside the root"
    assert rules.ignored(str(far / "rows.jsonl"), capture_root=str(far))
    assert rules.ignored("keep ") and not rules.ignored("keep"), "an escaped space stays"
    assert ignore._trim_trailing_spaces("a\\  ") == "a\\ " and ignore._trim_trailing_spaces("   ") == ""


@pytest.mark.skipif(os.name == "nt" or os.geteuid() == 0, reason="posix permissions; root reads anything")
def test_an_unreadable_file_warns_instead_of_applying_nothing_silently(tmp_path, monkeypatch):
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    path = tmp_path / ".probeignore"
    path.write_text("*.ckpt\n")
    path.chmod(0)
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            assert ignore.load(str(tmp_path)) is None
    finally:
        path.chmod(0o644)
    assert any("could not be read" in str(w.message) and ".probeignore" in str(w.message) for w in caught)


def test_a_utf16_file_is_decoded_not_garbage(tmp_path, monkeypatch):
    """LOW: PowerShell's `>` writes UTF-16 LE with a BOM; it used to decode as
    NUL-riddled garbage, matching nothing, with no word said."""
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    for encoding in ("utf-16-le", "utf-16-be"):
        bom = b"\xff\xfe" if encoding.endswith("le") else b"\xfe\xff"
        (tmp_path / ".probeignore").write_bytes(bom + "*.ckpt\r\ndata/\r\n".encode(encoding))
        rules = ignore.load(str(tmp_path))
        assert rules is not None and rules.patterns == ("*.ckpt", "data/"), encoding
        assert rules.ignored("m.ckpt") and rules.ignored("data/x")
    # Without a BOM it cannot be told apart from bytes: say so, apply nothing.
    (tmp_path / ".probeignore").write_bytes("*.ckpt\n".encode("utf-16-le"))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert ignore.load(str(tmp_path)) is None
    assert any("NUL bytes" in str(w.message) for w in caught)


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="needs FIFOs")
def test_a_fifo_named_probeignore_cannot_hang_init(tmp_path, monkeypatch):
    """LOW: `open()` on a FIFO with no writer blocks forever, and it was on
    the probe.init() path. Run in a child with a timeout, so a regression
    fails instead of hanging the suite."""
    os.mkfifo(tmp_path / ".probeignore")
    code = (
        "import warnings, sys\n"
        "warnings.simplefilter('always')\n"
        "from probe.sdk import ignore\n"
        f"print(ignore.load({str(tmp_path)!r}, environ={{}}))\n"
    )
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0 and proc.stdout.strip() == "None", proc.stderr
    assert "not a regular file" in proc.stderr
    (tmp_path / ".probeignore").unlink()
    (tmp_path / ".probeignore").mkdir()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert ignore.load(str(tmp_path), environ={}) is None
    assert any("not a regular file" in str(w.message) for w in caught)


def test_a_read_matches_through_a_symlink_both_ways(tmp_path, monkeypatch):
    """LOW: read capture escaped through links. `data/` excluded and
    `datalink -> data`: `datalink/rows.csv` was recorded. `bigdata/` excluded
    and `bigdata -> /elsewhere`: a loader opening the resolved path was
    recorded. A read (follow=True) now matches as opened AND as resolved, and
    against where the root's excluded links lead."""
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    repo = _repo(tmp_path / "repo")
    (repo / "data").mkdir()
    (repo / "data" / "rows.csv").write_text("x")
    (repo / "datalink").symlink_to("data", target_is_directory=True)
    ext = tmp_path / "elsewhere"
    ext.mkdir()
    (ext / "shard.bin").write_text("x")
    (repo / "bigdata").symlink_to(ext, target_is_directory=True)
    deep = tmp_path / "deep"
    deep.mkdir()
    (deep / "w.pt").write_text("x")
    (repo / "models").mkdir()
    (repo / "models" / "big").symlink_to(deep, target_is_directory=True)
    (repo / "weights.ckpt").write_text("x")
    (repo / "weights.bin").symlink_to("weights.ckpt")
    (repo / "notes.txt").write_text("x")
    (repo / ".probeignore").write_text("data/\nbigdata/\nmodels/big\n*.ckpt\n")
    rules = ignore.load(str(repo))
    for path in (
        repo / "datalink" / "rows.csv",  # a link inside the root, into an excluded folder
        ext / "shard.bin",  # where an excluded top-level link leads
        deep / "w.pt",  # where a link a plain pattern names leads
        repo / "weights.bin",  # a file link to an excluded file
    ):
        assert rules.ignored(str(path), follow=True), path
    assert not rules.ignored(str(repo / "notes.txt"), follow=True), "control: nothing names it"
    assert not rules.ignored(str(tmp_path / "other.txt"), follow=True), "control: outside, unnamed"
    # Code and output capture never follow a link: a link matches by its own name.
    assert not rules.ignored(str(repo / "datalink" / "rows.csv"))
    assert not rules.ignored(str(ext / "shard.bin"))


def test_a_link_holding_the_root_is_never_followed(tmp_path, monkeypatch):
    """`up -> ..` excluded must not turn into "every read under the parent"."""
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    repo = _repo(tmp_path / "repo")
    (repo / "up").symlink_to("..", target_is_directory=True)
    (repo / "self").symlink_to(".", target_is_directory=True)
    (tmp_path / "sibling.csv").write_text("x")
    (repo / ".probeignore").write_text("up/\nself/\n")
    rules = ignore.load(str(repo))
    assert rules._link_targets() == ()
    assert not rules.ignored(str(tmp_path / "sibling.csv"), follow=True)
    assert not rules.ignored(str(repo / "train.py"), follow=True)


def test_combine_and_unseen_by_launcher(tmp_path, monkeypatch):
    monkeypatch.delenv(ignore.ENV_PATTERNS, raising=False)
    a = ignore.load(str(tmp_path), extra=["*.a"], environ={})
    b = ignore.load(str(tmp_path), extra=["*.b"], environ={})
    assert ignore.combine(None, None) is None and ignore.combine(a, None) is a
    both = ignore.combine(a, b, a)
    assert isinstance(both, ignore.AnyOf) and len(both.rules) == 2
    assert both.ignored("x.a") and both.ignored("x.b") and not both.ignored("x.c")
    (tmp_path / ".probeignore").write_text("*.file\n")
    env = {
        ignore.ENV_FILE: str(tmp_path / ".probeignore"),
        ignore.ENV_PATTERNS: "*.env",
        ignore.ENV_EXPORTED: "*.exported",
    }
    rules = ignore.load(str(tmp_path), extra=["*.file", "*.env", "*.exported", "*.new "], environ=env)
    unseen = ignore.unseen_by_launcher(["*.file", "*.env", "*.exported", "*.new "], rules, env)
    assert unseen == ["*.new "], "only what the launcher never loaded"
    assert ignore.unseen_by_launcher(["*.file"], rules, {}) == ["*.file"], "no exported file: the launcher had none"


# -- under `probe exec` (#2045 re-review, MED) -------------------------------------

_EXEC_CHILD = (
    "open('early.ckpt').read()\n"  # before probe.init(): the child's hook spools it
    "open('keep.csv').read()\n"
    "import probe\n"
    "probe.init({init})\n"
    "open('data.ckpt').read()\n"
    "open('model.ckpt', 'w').write('weights')\n"
    "open('metrics.json', 'w').write('{{}}')\n"
)


def _exec_child(app, tmp_path, init: str, **env: str):
    """`probe exec -- python train.py` against the served fake, every capture on."""
    from tests.served_fake_app import child_env, serve

    app.seed_experiment("e1")
    for name, text in (("data.ckpt", "read"), ("early.ckpt", "read"), ("keep.csv", "read"),
                       ("tokens_cache.ckpt", "beside the code")):
        (tmp_path / name).write_text(text + "\n")
    (tmp_path / "train.py").write_text(_EXEC_CHILD.format(init=init))
    argv = [sys.executable, "-m", "probe.cli", "exec", "--experiment", "e1", "--", sys.executable, "train.py"]
    with serve(app) as url:
        proc = subprocess.run(
            argv,
            env=child_env(url, PROBE_AUTO_SNAPSHOT="1", PROBE_CAPTURE_OUTPUTS="1", PROBE_CAPTURE_READS="1", **env),
            cwd=tmp_path,
            capture_output=True,
            text=True,
            timeout=180,
        )
    assert proc.returncode == 0, proc.stderr[-3000:]
    return proc


def _what_reached(app) -> dict[str, set[str]]:
    """The file names each capture sent the server, or queued for it."""
    import json
    from pathlib import Path

    reads: set[str] = set()
    code: set[str] = set()
    for request in app.requests:
        if request.method != "POST":
            continue
        if request.url.path.endswith("/inputs"):
            reads |= {os.path.basename(row["path"]) for row in json.loads(request.content)["inputs"]}
        elif request.url.path == "/v1/execution-records":
            code |= {e["path"] for e in json.loads(request.content)["code"]["manifest"]["entries"]}
    names = {a["name"] for rows in app.artifacts.values() for a in rows}
    for root in {os.environ["PROBE_OUTBOX_DIR"], os.environ["XDG_STATE_HOME"]}:
        for op_file in Path(root).rglob("*.json"):
            if op_file.parent.name == "ops":
                op = json.loads(op_file.read_text())
                if op.get("kind") == "upload":
                    names.add(op["upload"]["name"])
    outputs = {n[len("outputs/"):] for n in names if n.startswith("outputs/")}
    return {"read": reads, "code": code, "output": outputs}


@pytest.mark.parametrize("how", ["init(ignore=)", "PROBE_IGNORE", "nothing (control)"])
def test_patterns_reach_every_capture_under_probe_exec(app, tmp_path, how):
    """The re-review's MED: `probe.init(ignore=['*.ckpt'])` inside `probe exec`
    did nothing -- the launcher collects the child's reads and sweeps its
    folder with ITS rules, and took the code snapshot before the child ran.
    The child now hands its patterns to the launcher for reads and outputs;
    the code snapshot it cannot reach, so the child says so, pointing at
    PROBE_IGNORE / .probeignore, which do reach all three."""
    init, env = {
        "init(ignore=)": ("ignore=['*.ckpt']", {}),
        "PROBE_IGNORE": ("", {"PROBE_IGNORE": "*.ckpt"}),
        "nothing (control)": ("", {}),
    }[how]
    proc = _exec_child(app, tmp_path, init, **env)
    got = _what_reached(app)
    # Capture worked at all, in every arm.
    assert "keep.csv" in got["read"] and "metrics.json" in got["output"] and "train.py" in got["code"], got
    warned = "cannot keep files out of this run's code snapshot" in proc.stderr
    if how == "nothing (control)":
        assert {"data.ckpt", "early.ckpt"} <= got["read"] and "model.ckpt" in got["output"]
        assert {"data.ckpt", "tokens_cache.ckpt"} <= got["code"] and not warned
        return
    leaked = {"read": {"data.ckpt", "early.ckpt"} & got["read"], "output": {"model.ckpt"} & got["output"]}
    assert leaked == {"read": set(), "output": set()}
    if how == "PROBE_IGNORE":
        assert not {"data.ckpt", "tokens_cache.ckpt"} & got["code"] and not warned
    else:
        # Taken before the child started: ignore= cannot reach it, and says so.
        assert "tokens_cache.ckpt" in got["code"]
        assert warned and "ignore=['*.ckpt']" in proc.stderr and "PROBE_IGNORE" in proc.stderr
