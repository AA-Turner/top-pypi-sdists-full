"""Every program the machine worker runs by name is installed AND proven by the image build.

2026-11-02: the safety branch (``machine_git_safety``) and the agent's git door call ``git``, and the
Cloud Computer image never installed it: the carry-over gate's git door answered
``/bin/sh: 1: git: not found`` on the live build. This reads every literal program name the worker
passes to ``asyncio.create_subprocess_exec`` and requires it in the Dockerfile's
``command -v`` line, which fails the image build when the program is missing.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
WORKER = PKG / "matrx_scraper/cloud_browser/worker"
DOCKERFILE = PKG / "docker/cloud-computer/Dockerfile"


def _programs_the_worker_runs() -> dict[str, str]:
    found: dict[str, str] = {}
    for path in sorted(WORKER.glob("*.py")):
        for node in ast.walk(ast.parse(path.read_text(), filename=str(path))):
            if not (isinstance(node, ast.Call) and node.args):
                continue
            func = node.func
            name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
            first = node.args[0]
            if name == "create_subprocess_exec" and isinstance(first, ast.Constant) and isinstance(first.value, str):
                found.setdefault(first.value, f"{path.name}:{node.lineno}")
    return found


def _programs_the_build_proves() -> set[str]:
    text = DOCKERFILE.read_text().replace("\\\n", " ")
    proven: set[str] = set()
    for match in re.finditer(r"command -v ([^&;|\n]+)", text):
        proven.update(match.group(1).split())
    return proven


def test_the_worker_runs_programs_by_name() -> None:
    # The scan must see real calls, or the check below proves nothing.
    assert "git" in _programs_the_worker_runs()


def test_every_program_the_worker_runs_is_proven_by_the_image_build() -> None:
    proven = _programs_the_build_proves()
    missing = {prog: where for prog, where in _programs_the_worker_runs().items() if prog not in proven}
    assert not missing, (
        f"the Cloud Computer image never proves these programs exist: {missing}; install them in "
        f"{DOCKERFILE.name} and add them to its `command -v` line"
    )
