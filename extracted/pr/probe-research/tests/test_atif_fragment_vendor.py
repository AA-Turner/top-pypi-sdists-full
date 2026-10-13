"""The tap's ATIF fragment builder is the engine's, byte for byte.

`src/probe/tap_core/atif_fragment.py` and `transcript_render.py` are vendored
from prbe-knowledge by `scripts/sync_atif_fragment.py`, which stamps each with
the engine commit and the sha256 of the engine file. The engine rebuilds
fragments from events to compare with what a client sent, so a hand edit here
is a silent divergence. These need no engine checkout: the header proves the
body (the one import rewrite reversed, the hash must match), and
`--check --knowledge-root <checkout> --ref <commit>` proves the source.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

_AGENT = Path(__file__).resolve().parent.parent
_SCRIPT = _AGENT / "scripts" / "sync_atif_fragment.py"


def _sync():
    spec = importlib.util.spec_from_file_location("_sync_atif_fragment", _SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SYNC = _sync()

#: The engine's pins (prbe-knowledge): the sha256 of each engine file the tap
#: must run, so client and server build the same fragments. Moving one is a
#: change on both sides: re-vendor (scripts/sync_atif_fragment.py), then here.
ENGINE_PINS = {
    "engine/ingest/atif/fragment.py": "b0d5ac850d7c84ff1028d42ee95a04041c80ce1f73b6ea580ec8b00a2516a809",
    "engine/shared/transcript_render.py": "c0bb4168f7aa86f89a9c6360d1f120b588458d94ad5e0b84cd9c077942008c9e",
}


@pytest.mark.parametrize("spec", SYNC.FILES, ids=lambda spec: spec.target)
def test_the_header_proves_the_body(spec):
    text = (SYNC.TAP_CORE / spec.target).read_text("utf-8")
    assert SYNC.self_consistent(spec, text) == []
    fields, body = SYNC.split(text)
    assert fields["source"] == spec.source
    assert len(fields["commit"]) == 40 and int(fields["commit"], 16) >= 0
    original = SYNC.reverse(spec, body).encode("utf-8")
    assert hashlib.sha256(original).hexdigest() == fields["sha256"]
    # The rewrite is reversible exactly: applying it again gives the body back.
    assert SYNC.apply(spec, original.decode("utf-8")) == body


@pytest.mark.parametrize("spec", SYNC.FILES, ids=lambda spec: spec.target)
def test_a_hand_edit_is_caught(spec):
    text = (SYNC.TAP_CORE / spec.target).read_text("utf-8")
    edited = text.replace("from __future__ import annotations", "from __future__ import annotations  # x", 1)
    assert edited != text
    assert SYNC.self_consistent(spec, edited)


@pytest.mark.parametrize("spec", SYNC.FILES, ids=lambda spec: spec.target)
def test_the_vendored_files_are_the_engines_pinned_ones(spec):
    fields, body = SYNC.split((SYNC.TAP_CORE / spec.target).read_text("utf-8"))
    assert set(ENGINE_PINS) == {f.source for f in SYNC.FILES}
    assert fields["sha256"] == ENGINE_PINS[spec.source]
    assert hashlib.sha256(SYNC.reverse(spec, body).encode("utf-8")).hexdigest() == ENGINE_PINS[spec.source]


def test_the_header_names_the_modules_fragment_version():
    from probe.tap_core import atif_fragment

    fields, _body = SYNC.split((SYNC.TAP_CORE / "atif_fragment.py").read_text("utf-8"))
    assert int(fields["fragment_version"]) == atif_fragment.FRAGMENT_VERSION


def test_the_fragment_imports_its_renderer_relatively():
    """The same bytes must resolve as probe.tap_core.* and as the plugin's tap.*."""
    tree = ast.parse((SYNC.TAP_CORE / "atif_fragment.py").read_text("utf-8"))
    imports = [
        (node.level, node.module)
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module and "transcript_render" in node.module
    ]
    assert imports == [(1, "transcript_render")]


@pytest.mark.parametrize("spec", SYNC.FILES, ids=lambda spec: spec.target)
def test_the_vendored_files_are_python_310(spec):
    """The CLI's floor is 3.10 (pyproject `requires-python`); the 3.10 CI leg
    imports every module, this pins the syntax on any interpreter."""
    ast.parse((SYNC.TAP_CORE / spec.target).read_text("utf-8"), feature_version=(3, 10))


def test_check_without_an_engine_checkout_passes():
    result = subprocess.run(
        [sys.executable, str(_SCRIPT), "--check"], capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stderr


# -- every byte is checked, the header's included ----------------------------------------


def _planted(text: str) -> str:
    first, rest = text.split("\n", 1)
    return f"{first}\nimport os; os.environ['PLANTED'] = '1'  # looks like a header line\n{rest}"


@pytest.mark.parametrize("spec", SYNC.FILES, ids=lambda spec: spec.target)
def test_a_line_planted_among_the_header_lines_is_caught(spec):
    """A comment-looking header is still Python: a line slipped in before the
    end marker runs on import, and the hash of the body cannot see it."""
    text = (SYNC.TAP_CORE / spec.target).read_text("utf-8")
    assert SYNC.self_consistent(spec, _planted(text))
    commit = SYNC.split(text)[0]["commit"]
    assert SYNC.self_consistent(spec, text.replace(commit, commit[:12], 1))  # a stamp names a full id


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=synthetic", "-c", "user.email=synthetic@example.invalid",
         "-c", "commit.gpgsign=false", *args],
        check=True, capture_output=True, text=True,
    ).stdout.strip()


@pytest.fixture
def engine(tmp_path, monkeypatch):
    """A prbe-knowledge history holding the vendored files' engine bytes:
    `main` = [A: the two files] -> [B: an unrelated change]; `side` = A + a
    copy of those bytes in a commit off main's history (a squashed branch)."""
    repo = tmp_path / "prbe-knowledge"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    for spec in SYNC.FILES:
        body = SYNC.split((SYNC.TAP_CORE / spec.target).read_text("utf-8"))[1]
        source = repo / spec.source
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(SYNC.reverse(spec, body).encode("utf-8"))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "A")
    a = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "-q", "-b", "side")
    _git(repo, "commit", "-q", "--allow-empty", "-m", "branch commit")
    side = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "-q", "main")
    (repo / "README").write_text("unrelated\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "B")
    b = _git(repo, "rev-parse", "HEAD")
    vendored = tmp_path / "tap_core"
    vendored.mkdir()
    monkeypatch.setattr(SYNC, "TAP_CORE", vendored)
    return repo, vendored, {"A": a, "B": b, "side": side}


def _check(repo: Path, ref: str) -> int:
    return SYNC.main(["--check", "--knowledge-root", str(repo), "--ref", ref])


def test_a_check_against_a_moving_main_passes_until_the_files_change(engine):
    repo, vendored, commits = engine
    assert SYNC.main(["--knowledge-root", str(repo), "--ref", commits["A"]]) == 0
    assert _check(repo, commits["A"]) == 0
    assert _check(repo, commits["B"]) == 0  # main moved; these bytes did not
    assert SYNC.main(["--check"]) == 0  # and CI's no-checkout check agrees
    target = vendored / "atif_fragment.py"
    target.write_text(_planted(target.read_text("utf-8")), "utf-8")
    assert _check(repo, commits["B"]) == 1 and _check(repo, commits["A"]) == 1
    assert SYNC.main(["--check"]) == 1


def test_a_stamp_off_mains_history_is_drift(engine):
    repo, _vendored, commits = engine
    assert SYNC.main(["--knowledge-root", str(repo), "--ref", commits["side"]]) == 0
    assert _check(repo, commits["side"]) == 0
    assert _check(repo, commits["B"]) == 1  # same bytes, but a commit main never had
