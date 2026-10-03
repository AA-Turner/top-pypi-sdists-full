"""The ratchet on harness names written into agent/ core code.

See agent/tools/harness_literals.py. The allowlist only goes down: a file over
its number fails, a new file with any fails, and a file under its number fails
until you lower it, so every cleanup is locked in. When the registry refactor
is done the allowlist is empty.

Regenerate after a deliberate change:
    python agent/tools/harness_literals.py agent --write agent/tests/fixtures/harness_literals_allowlist.json
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

AGENT = Path(__file__).resolve().parents[1]
ALLOWLIST = AGENT / "tests" / "fixtures" / "harness_literals_allowlist.json"


def _scanner():
    spec = importlib.util.spec_from_file_location(
        "harness_literals", AGENT / "tools" / "harness_literals.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_agent_code_names_no_more_harnesses_than_the_ratchet_allows():
    problems = _scanner().compare("agent", ALLOWLIST)
    assert not problems, "\n".join(problems)


def test_the_scanner_finds_a_literal_and_honours_the_escape(tmp_path, monkeypatch):
    scanner = _scanner()
    probe_dir = tmp_path / "agent" / "src" / "probe"
    probe_dir.mkdir(parents=True)
    (probe_dir / "core.py").write_text(
        'a = "codex" if x else "claude_code"\n'
        'b = os.environ.get("CODEX_THREAD_ID")\n'
        'c = "pi"  # harness-literal-ok: the circle constant\n'
    )
    (probe_dir / "harness").mkdir()
    (probe_dir / "harness" / "registry.py").write_text('"codex"\n')
    monkeypatch.setattr(scanner, "REPO", tmp_path)
    assert scanner.count("agent") == {"agent/src/probe/core.py": 3}


def test_the_scanner_guards_every_registry_row():
    """The words it counts come from the registry, so a new harness is guarded
    the moment its row lands, with no edit to the scanner."""
    from probe.harness import registry

    scanner = _scanner()
    for harness in registry.get_registry().all():
        assert harness.id in scanner.HARNESS_WORDS
        if harness.route:
            assert harness.route in scanner.HARNESS_WORDS
        for name in (*harness.detect_env, harness.session_env):
            if name:
                assert name in scanner.ENV_MARKERS
