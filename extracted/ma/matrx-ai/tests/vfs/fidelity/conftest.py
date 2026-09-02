from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio

from .fixtures import BASIC_TREE, ERROR_TREE, GREP_TREE
from .harness import FidelityHarness, gnu_coreutils_available


_FIDELITY_DIR = str(__import__("pathlib").Path(__file__).resolve().parent)


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    # The fidelity test files (test_fidelity_*.py) compare VFS output against
    # the OS's native binaries — meaningful only when those are GNU coreutils.
    # On macOS without brew's `coreutils` we'd be diffing GNU-mimicry against
    # BSD output, so every assertion would fail for reasons unrelated to the
    # VFS. Skip cleanly with a hint instead.
    #
    # Other tests in this directory (e.g. test_harness_routing.py) verify the
    # harness's plumbing and don't need real GNU coreutils — leave those alone.
    #
    # NOTE: this hook is global once pytest discovers it, so we must restrict
    # the marker to items that actually live under tests/vfs/fidelity/.
    if gnu_coreutils_available():
        return
    skip_marker = pytest.mark.skip(
        reason=(
            "GNU coreutils not found — fidelity tests need them to compare "
            "byte-exact output. Install with `brew install coreutils gnu-sed "
            "grep findutils gawk` on macOS, or run on Linux."
        )
    )
    for item in items:
        item_path = str(item.path)
        if not item_path.startswith(_FIDELITY_DIR):
            continue
        # Only mark the actual byte-comparison fidelity files, not the
        # harness's own self-tests.
        if Path(item_path).name.startswith("test_fidelity_"):
            item.add_marker(skip_marker)


async def _make_harness(tree: dict[str, Any]) -> AsyncIterator[FidelityHarness]:
    h = FidelityHarness(tree)
    await h.setup()
    try:
        yield h
    finally:
        h.cleanup()


@pytest_asyncio.fixture
async def basic_harness() -> AsyncIterator[FidelityHarness]:
    async for h in _make_harness(BASIC_TREE):
        yield h


@pytest_asyncio.fixture
async def grep_harness() -> AsyncIterator[FidelityHarness]:
    async for h in _make_harness(GREP_TREE):
        yield h


@pytest_asyncio.fixture
async def error_harness() -> AsyncIterator[FidelityHarness]:
    async for h in _make_harness(ERROR_TREE):
        yield h
