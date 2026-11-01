"""The tap's ATIF fragment builder is the one in probe-contracts, byte for byte.

`src/probe/tap_core/atif_fragment.py` and `transcript_render.py` are vendored
from contracts/probe_contracts/transcripts by `scripts/sync_atif_fragment.py`,
which stamps each with the sha256 of its source. The engine rebuilds fragments
from events (with its own vendored copy of probe-contracts) to compare with
what a client sent, so a hand edit here is a silent divergence. The header
proves the body (the one import rewrite reversed, the hash must match), and
`--check` proves the source.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import shutil
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
needs_contracts = pytest.mark.skipif(
    not (SYNC.REPO / "contracts" / "probe_contracts" / "transcripts").is_dir(),
    reason="not a research-os checkout: contracts/ is absent",
)

#: The sha256 of each source file, keyed by the tap file. The engine runs these
#: bytes too (its vendored probe-contracts), so changing them is a change on both
#: sides: re-vendor the tap (scripts/sync_atif_fragment.py) and the engine
#: (scripts/sync_engine_contracts.py), then update these.
SOURCE_PINS = {
    "atif_fragment.py": "c7440c06862e561fe61217614cdb760c6843fd1617e732c8c550f9c2144dde4b",
    "transcript_render.py": "c0bb4168f7aa86f89a9c6360d1f120b588458d94ad5e0b84cd9c077942008c9e",
}


@pytest.mark.parametrize("spec", SYNC.FILES, ids=lambda spec: spec.target)
def test_the_header_proves_the_body(spec):
    text = (SYNC.TAP_CORE / spec.target).read_text("utf-8")
    assert SYNC.self_consistent(spec, text) == []
    fields, body = SYNC.split(text)
    assert fields["source"] == spec.source
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
def test_the_vendored_files_are_the_pinned_ones(spec):
    fields, body = SYNC.split((SYNC.TAP_CORE / spec.target).read_text("utf-8"))
    assert set(SOURCE_PINS) == {f.target for f in SYNC.FILES}
    assert fields["sha256"] == SOURCE_PINS[spec.target]
    assert hashlib.sha256(SYNC.reverse(spec, body).encode("utf-8")).hexdigest() == SOURCE_PINS[spec.target]


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


@needs_contracts
def test_check_passes():
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


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A copy of the two sources and the tap's two files, as the sync sees them."""
    for spec in SYNC.FILES:
        source = tmp_path / spec.source
        source.parent.mkdir(parents=True, exist_ok=True)
        body = SYNC.split((SYNC.TAP_CORE / spec.target).read_text("utf-8"))[1]
        source.write_bytes(SYNC.reverse(spec, body).encode("utf-8"))
    vendored = tmp_path / "tap_core"
    shutil.copytree(SYNC.TAP_CORE, vendored, ignore=shutil.ignore_patterns("__pycache__"))
    monkeypatch.setattr(SYNC, "REPO", tmp_path)
    monkeypatch.setattr(SYNC, "TAP_CORE", vendored)
    return tmp_path, vendored


def test_a_changed_source_is_drift_until_re_vendored(repo):
    root, vendored = repo
    assert SYNC.main(["--check"]) == 0
    source = root / SYNC.FILES[1].source
    source.write_text(source.read_text("utf-8") + "\n# changed\n", "utf-8")
    assert SYNC.main(["--check"]) == 1
    assert SYNC.main([]) == 0
    assert SYNC.main(["--check"]) == 0
    assert SYNC.self_consistent(SYNC.FILES[1], (vendored / SYNC.FILES[1].target).read_text("utf-8")) == []


def test_a_source_importing_the_engine_or_the_package_stops_the_sync(repo):
    root, _vendored = repo
    source = root / SYNC.FILES[1].source
    source.write_text("import probe_contracts.knowledge\n" + source.read_text("utf-8"), "utf-8")
    with pytest.raises(SystemExit, match="standard library"):
        SYNC.main([])
