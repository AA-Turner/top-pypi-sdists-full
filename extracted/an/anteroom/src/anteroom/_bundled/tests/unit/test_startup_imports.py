"""Structural startup tests -- verify heavy modules are NOT imported eagerly.

These tests are deterministic: they check sys.modules membership, not wall-clock
time. They cannot flake on slow CI runners.
"""

from __future__ import annotations

import subprocess
import sys

import pytest

# Modules that must NOT be imported when loading the CLI entry path.
# Each entry is (module_prefix, reason).
BANNED_EAGER_IMPORTS = [
    ("openai", "262ms -- deferred to first AI call (3 paths: ai_service, embeddings, agent_loop)"),
    ("uvicorn", "61ms -- only needed by web subcommand"),
    ("httpx", "transitive via openai -- deferred together"),
    ("pydantic_core", "transitive via openai -- deferred together"),
    ("fastembed", "embedding model -- loaded on first RAG use"),
    ("usearch", "vector index -- loaded on first search (via VectorIndexManager)"),
    ("numpy", "transitive via usearch/vector ops -- loaded on first vector add/search"),
]


def _check_module_not_imported(import_statement: str, banned_prefix: str) -> bool:
    """Run a subprocess that executes import_statement, then check sys.modules."""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            f"{import_statement}; import sys; "
            f"print(any(k == '{banned_prefix}' or k.startswith('{banned_prefix}.') "
            f"for k in sys.modules))",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout.strip() == "False"


class TestNoEagerImports:
    """Verify that importing the CLI entry path does not eagerly load heavy deps."""

    @pytest.mark.parametrize(
        "banned_prefix,reason",
        [(p, r) for p, r in BANNED_EAGER_IMPORTS],
        ids=[p for p, _ in BANNED_EAGER_IMPORTS],
    )
    def test_main_import_does_not_load(self, banned_prefix: str, reason: str) -> None:
        """Importing anteroom.__main__ must not eagerly import {banned_prefix}."""
        assert _check_module_not_imported("from anteroom.__main__ import main", banned_prefix), (
            f"anteroom.__main__ eagerly imports '{banned_prefix}' ({reason}). Move to lazy/local import."
        )

    @pytest.mark.parametrize(
        "banned_prefix,reason",
        [(p, r) for p, r in BANNED_EAGER_IMPORTS],
        ids=[p for p, _ in BANNED_EAGER_IMPORTS],
    )
    def test_repl_import_does_not_load(self, banned_prefix: str, reason: str) -> None:
        """Importing anteroom.cli.repl must not eagerly import {banned_prefix}."""
        assert _check_module_not_imported("from anteroom.cli.repl import run_cli", banned_prefix), (
            f"anteroom.cli.repl eagerly imports '{banned_prefix}' ({reason}). Move to lazy/local import."
        )


class TestImportBudget:
    """Guard total import cost via importtime analysis.

    This is NOT a wall-clock assertion. It counts how many modules exceed
    a self-time threshold, which is proportional (not absolute) and stable
    across machines.
    """

    def test_no_heavy_imports_in_entry_path(self) -> None:
        """No single module import should dominate startup.

        Parse `-X importtime` output. Count modules with self-time > 50ms.
        Allow at most 3 (Python stdlib: importlib.metadata, typing, etc.).
        If a new heavy module appears, it means a lazy import regressed.
        """
        result = subprocess.run(
            [
                sys.executable,
                "-X",
                "importtime",
                "-c",
                "from anteroom.__main__ import main",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        # importtime output goes to stderr, format:
        # "import time: self [us] | cumulative | name"
        heavy: list[tuple[str, int]] = []
        for line in result.stderr.splitlines():
            if "import time:" not in line:
                continue
            parts = line.split("|")
            if len(parts) < 3:
                continue
            self_us_str = parts[0].replace("import time:", "").strip()
            try:
                self_us = int(self_us_str)
            except ValueError:
                continue
            mod_name = parts[2].strip()
            if self_us > 50_000:  # 50ms self-time
                heavy.append((mod_name, self_us))

        # Allow a small number of heavy stdlib imports (importlib.metadata, etc.)
        # but catch regressions where openai/uvicorn/fastembed sneak back in.
        max_allowed = 3
        assert len(heavy) <= max_allowed, (
            f"Found {len(heavy)} modules with >50ms self-import-time "
            f"(max {max_allowed}):\n" + "\n".join(f"  {name}: {us / 1000:.0f}ms" for name, us in heavy)
        )


class TestUpdateCheckNonBlocking:
    """Regression: the update check must not block time-to-prompt (#1377).

    The old code used ``await asyncio.wait_for(_update_task, timeout=2.0)``
    which could stall the prompt for up to 2 seconds. The fix uses
    ``_update_task.add_done_callback()`` so the prompt appears immediately.

    These tests inspect the REAL ``repl.py`` source via AST to ensure the
    non-blocking pattern is preserved. They will catch any future regression
    that reintroduces a blocking await on ``_update_task``.
    """

    @staticmethod
    def _get_repl_source() -> str:
        """Return the source of anteroom.cli.repl without importing it."""
        from pathlib import Path

        repl_path = Path(__file__).resolve().parent.parent.parent / "src" / "anteroom" / "cli" / "repl.py"
        return repl_path.read_text(encoding="utf-8")

    def test_no_await_on_update_task_in_repl_source(self) -> None:
        """repl.py must not contain ``await ... _update_task`` between task creation and _run_repl.

        This catches the exact regression from #1374 where
        ``await asyncio.wait_for(asyncio.shield(_update_task), timeout=2.0)``
        blocked the prompt for up to 2 seconds.
        """
        import ast

        source = self._get_repl_source()
        tree = ast.parse(source)

        # Walk AST looking for Await nodes whose value references _update_task.
        # The non-blocking pattern uses add_done_callback (an Attribute call),
        # not an Await expression.
        blocking_awaits: list[int] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Await):
                continue
            # Check if the awaited expression references _update_task
            await_src = ast.get_source_segment(source, node)
            if await_src and "_update_task" in await_src:
                blocking_awaits.append(node.lineno)

        assert not blocking_awaits, (
            f"repl.py contains blocking await on _update_task at line(s) {blocking_awaits}. "
            f"The update check must use add_done_callback() to avoid blocking time-to-prompt. "
            f"See #1377."
        )

    def test_update_task_uses_done_callback_in_repl_source(self) -> None:
        """repl.py must use ``_update_task.add_done_callback(...)`` for the update check.

        This is the positive counterpart: verify the non-blocking pattern IS present.
        """
        source = self._get_repl_source()
        assert "_update_task.add_done_callback(" in source, (
            "repl.py does not use _update_task.add_done_callback(). "
            "The update check result must be rendered via a done-callback, "
            "not by awaiting the task. See #1377."
        )

    def test_no_wait_for_on_update_task_in_repl_source(self) -> None:
        """repl.py must not use ``asyncio.wait_for(..._update_task...)`` anywhere.

        This catches the specific anti-pattern from the original regression:
        ``await asyncio.wait_for(asyncio.shield(_update_task), timeout=2.0)``
        """
        import re

        source = self._get_repl_source()
        # Match wait_for calls that reference _update_task anywhere in their arguments
        matches = re.findall(r"wait_for\([^)]*_update_task[^)]*\)", source)
        assert not matches, (
            f"repl.py contains asyncio.wait_for on _update_task: {matches}. "
            f"This blocks time-to-prompt. Use add_done_callback instead. See #1377."
        )
