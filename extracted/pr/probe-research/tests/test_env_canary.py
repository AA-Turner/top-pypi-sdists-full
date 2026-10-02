"""Import-origin canary for the two-Python-project monorepo.

The monorepo holds two `probe`-adjacent Python projects: the server at the
repo root and this agent tree under agent/. If CI's environment wiring ever
regresses (root venv leaking in, an editable install of the wrong tree, a
PYTHONPATH pointing at another checkout), pytest can import a `probe` that is
NOT the code under test — and every green run is then meaningless. That exact
failure has happened outside CI: a worktree's green suite once tested the
primary checkout's main.

Two lines of assertion make the discipline mechanical.
"""

from pathlib import Path

import probe


def test_probe_imports_from_this_tree():
    agent_src = Path(__file__).resolve().parent.parent / "src"
    probe_file = Path(probe.__file__).resolve()
    assert probe_file.is_relative_to(agent_src), (
        f"probe imported from {probe_file}, expected it under {agent_src} — "
        "the test run is wired to the wrong environment and is not testing "
        "this tree. Install with agent/'s own env (pip install -e agent[dev])."
    )
