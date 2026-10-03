"""Every copy of the wizard pointer must say the same thing as the canonical one.

Setup is wizard-only (Richard 2026-09-29): a message that sends a person to set
up, sign in, update or repair points at the Probe wizard, never at a
`probe <setup command>`. The words live ONCE, as
`probe.sdk.session_marker.WIZARD_HINT`, but three surfaces cannot import it:

  * the tap plugin is stdlib-only and runs without `probe` on sys.path, so
    `tap/config.py` carries a copy;
  * the pi extension is TypeScript, so `src/wizardHint.ts` carries a copy;
  * two shell scripts inline the sentence.

A copy that drifts keeps working and quietly tells people something different,
which is the failure this pins. Same contract as tests/test_tap_core_sync.py.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

from probe.sdk.session_marker import WIZARD_HINT

_ROOT = Path(__file__).resolve().parent.parent
_PLUGINS = _ROOT / "plugins"


def _python_constant(path: Path, name: str) -> str:
    """The string a module-level ``name = "..."`` assigns, read without importing."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in node.targets
        ):
            assert isinstance(node.value, ast.Constant) and isinstance(node.value.value, str), (
                f"{path}: {name} must be a plain string literal"
            )
            return node.value.value
    raise AssertionError(f"{path} defines no module-level {name}")


def test_the_canonical_hint_names_the_wizard_and_no_setup_command() -> None:
    assert "npx probe-research" in WIZARD_HINT
    assert "probe login" not in WIZARD_HINT and "probe setup" not in WIZARD_HINT


def test_the_tap_copy_matches() -> None:
    tap_config = _PLUGINS / "probe-research-tap" / "tap" / "config.py"
    assert _python_constant(tap_config, "WIZARD_HINT") == WIZARD_HINT


def test_the_pi_copy_matches() -> None:
    source = (_PLUGINS / "probe-research-pi" / "src" / "core" / "wizardHint.ts").read_text(encoding="utf-8")
    match = re.search(r'^export const WIZARD_HINT = "([^"\\]*)";$', source, re.MULTILINE)
    assert match, "src/wizardHint.ts must export WIZARD_HINT as one plain string literal"
    assert match.group(1) == WIZARD_HINT


@pytest.mark.parametrize(
    "script",
    [
        "probe-research/bin/probe-mcp-headers",
        "probe-research-tap/hooks/session-start.sh",
    ],
)
def test_the_shell_scripts_inline_the_same_words(script: str) -> None:
    assert WIZARD_HINT in (_PLUGINS / script).read_text(encoding="utf-8")
