"""hooks/_hook_harness.py: which harness runs a plugin hook, cheaply.

The status line renders and the approvals hook runs on every prompt, so the
resolver answers from the JSON alone and loads the full registry only for the
facts that need it.
"""

from __future__ import annotations

import fnmatch
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

from probe._compat import tomllib

AGENT = Path(__file__).resolve().parents[1]
HOOKS = AGENT / "plugins" / "probe-research" / "hooks"
TAP = AGENT / "plugins" / "probe-research-tap"


def _resolver():
    spec = importlib.util.spec_from_file_location("_hook_harness_under_test", HOOKS / "_hook_harness.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ({"PROBE_AGENT": "codex", "PLUGIN_ROOT": "/p"}, "codex"),
        ({"PLUGIN_ROOT": "/p"}, "codex"),
        ({"CLAUDE_PLUGIN_ROOT": "/x"}, "claude_code"),
        ({"CODEX_THREAD_ID": "t"}, "codex"),
        ({}, "claude_code"),
        # A PROBE_AGENT naming a harness that never runs these hooks is a
        # leftover in the shell, not evidence: Claude Code keeps its row (and
        # its question tool).
        ({"PROBE_AGENT": "pi", "CLAUDE_PLUGIN_ROOT": "/x"}, "claude_code"),
        ({"PROBE_AGENT": "gemini", "CLAUDECODE": "1"}, "claude_code"),
        # Kimi Code: its own plugin root, or the PROBE_AGENT its manifests export.
        ({"KIMI_PLUGIN_ROOT": "/x"}, "kimi_code"),
        ({"PROBE_AGENT": "kimi_code", "KIMI_PLUGIN_ROOT": "/x"}, "kimi_code"),
        # No plugin root: a direct call names its harness (the parity tests
        # and pi's own callers rely on it).
        ({"PROBE_AGENT": "pi"}, "pi"),
    ],
)
def test_the_resolver_tells_the_harnesses_apart(env, expected):
    assert _resolver().current(env).id == expected


def test_claude_code_keeps_its_question_tool_under_a_leaked_probe_agent():
    row = _resolver().current({"PROBE_AGENT": "pi", "CLAUDE_PLUGIN_ROOT": "/x"})
    assert row.question_tool == "AskUserQuestion"
    assert row.can("prompt_context")


def test_the_session_id_fallback_reads_only_captured_harnesses():
    resolver = _resolver()
    assert resolver.session_id({"CLAUDECODE": "1", "CURSOR_TRACE_ID": "terminal"}) == ""
    assert resolver.session_id({"CODEX_THREAD_ID": "s-codex"}) == "s-codex"
    assert resolver.session_id({"PI_SESSION_ID": "s-pi"}) == "s-pi"


def test_the_hot_path_never_loads_the_full_registry():
    """current().id, question_tool, can() and session_id() read the JSON only:
    the full loader's dataclasses + pathlib cost the status line ~16ms."""
    code = (
        "import importlib.util, sys\n"
        f"spec = importlib.util.spec_from_file_location('h', {str(HOOKS / '_hook_harness.py')!r})\n"
        "m = importlib.util.module_from_spec(spec); sys.modules['h'] = m; spec.loader.exec_module(m)\n"
        "row = m.current({'CLAUDE_PLUGIN_ROOT': '/x'})\n"
        "row.id, row.question_tool, row.can('wake'), m.session_id({'CLAUDE_CODE_SESSION_ID': 's'})\n"
        "assert '_probe_hooks._harness_registry' not in sys.modules, 'full registry loaded'\n"
        "assert 'dataclasses' not in sys.modules, 'dataclasses imported'\n"
        "print(row.capture.plugin_dir)\n"  # the full row, on demand
        "assert '_probe_hooks._harness_registry' in sys.modules\n"
    )
    result = subprocess.run([sys.executable, "-I", "-S", "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == ".claude/plugins/probe-research-tap"


def test_the_tap_wheel_ships_every_data_file_it_reads():
    """A pip-installed tap (pi's fallback runtime) imported tap/sources.py,
    which reads harnesses.json on import, from a wheel that had no JSON in it."""
    config = tomllib.loads((TAP / "pyproject.toml").read_text())
    patterns = config["tool"]["setuptools"]["package-data"]["tap"]
    data = [p.name for p in (TAP / "tap").iterdir() if p.is_file() and p.suffix not in {".py", ".pyc"}]
    assert "harnesses.json" in data
    for name in data:
        assert any(fnmatch.fnmatch(name, pattern) for pattern in patterns), name
