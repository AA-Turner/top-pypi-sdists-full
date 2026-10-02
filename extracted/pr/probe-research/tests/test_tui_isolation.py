"""The `tui` marker is what keeps the parallel lane honest.

CI splits the agent suite in two: `-m "not tui"` sharded across runners, and
`-m tui` serial and alone on its own runner. That split is only safe while every
test that measures a rendered terminal frame carries the marker.

Two shapes qualify, and the second is the one that bit us:

  * a real pty -- tests/test_setup_wizard.py forks one and reads the bytes back;
  * a prompt_toolkit app session whose frames are captured through
    `create_app_session` / `renderer._last_screen`.

Both assert on a render that has to have FINISHED. Unmarked, they land in the
parallel lane and share the box, and the symptom is not a clear failure -- it is
an assertion about UI text failing somewhere unrelated to the change that
triggered it, green on a re-run. test_tui_review.py did exactly that on
2026-09-10: it has no pty at all, so the original guard (which only knew about
`_pty_screen`) never looked at it.

So the rule is asserted over both shapes, at MODULE level for the app-session
kind: those files are wholly made of frame assertions, and marking the module is
both cheaper to keep true and harder to get half-right than marking each test.
"""

from __future__ import annotations

import ast
from pathlib import Path

TESTS = Path(__file__).parent
SELF = Path(__file__).name  # this file NAMES both harnesses; it does not use them.

# Forking a pty, or building a prompt_toolkit app session to capture frames.
# `_pty_screen` too: a file that IMPORTS the wizard's harness drives a pty just
# as surely as one that forks its own, and test_tui_cursor.py did exactly that
# unnoticed until its shard moved (2026-09-11).
_PTY = ("pty.fork", "pty.openpty", "_pty_screen")
_APP_SESSION = ("create_app_session", "create_pipe_input", "_last_screen")


def _source(path: Path) -> str:
    return path.read_text()


def _module_is_marked_tui(tree: ast.AST) -> bool:
    """`pytestmark = pytest.mark.tui`, bare or in a list."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not any(getattr(t, "id", "") == "pytestmark" for t in node.targets):
            continue
        items = node.value.elts if isinstance(node.value, (ast.List, ast.Tuple)) else [node.value]
        for item in items:
            if isinstance(item, ast.Attribute) and item.attr == "tui":
                return True
    return False


def _tests_calling(tree: ast.AST, names: tuple[str, ...]) -> set[str]:
    found = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not node.name.startswith("test_"):
            continue
        body = ast.dump(node)
        if any(n.split(".")[-1] in body for n in names):
            found.add(node.name)
    return found


def _is_marked_tui(node: ast.FunctionDef) -> bool:
    return any(
        isinstance(d, ast.Attribute) and d.attr == "tui" for d in node.decorator_list
    )


def test_every_pty_test_is_marked_tui():
    """The wizard's harness: marked per TEST, because most of that file is not tui."""
    offenders = []
    for path in sorted(TESTS.glob("test_*.py")):
        if path.name == SELF:
            continue
        text = _source(path)
        if not any(p in text for p in _PTY):
            continue
        tree = ast.parse(text)
        if _module_is_marked_tui(tree):
            continue
        want = _tests_calling(tree, ("_pty_screen", "_pty_screens"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name in want and not _is_marked_tui(node):
                    offenders.append(f"{path.name}::{node.name}")
    assert not offenders, (
        "these tests drive a pty but are not marked `@pytest.mark.tui`, so CI "
        "would run them in the parallel lane where they read half-drawn "
        "screens:\n  " + "\n  ".join(offenders)
    )


def test_every_app_session_module_is_marked_tui():
    """The prompt_toolkit kind: marked per MODULE.

    This is the guard test_tui_review.py needed and did not have.
    """
    offenders = []
    for path in sorted(TESTS.glob("test_*.py")):
        if path.name == SELF:
            continue
        text = _source(path)
        if not any(marker in text for marker in _APP_SESSION):
            continue
        if _module_is_marked_tui(ast.parse(text)):
            continue
        offenders.append(path.name)
    assert not offenders, (
        "these modules capture prompt_toolkit frames but do not declare "
        "`pytestmark = pytest.mark.tui`, so CI would run them in the parallel "
        "lane where a frame index can outrun the render:\n  " + "\n  ".join(offenders)
    )
