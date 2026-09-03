"""Unit tests for generate_runtime_hierarchy_input."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.runtime_inputs import (
    HierarchyChain,
    generate_runtime_hierarchy_input,
)


def test_generate_runtime_input_rejects_unsafe_run_id(tmp_path: Path) -> None:
    chain = HierarchyChain(subtask_key="3")
    with pytest.raises(ValueError, match="run_id"):
        generate_runtime_hierarchy_input(tmp_path, "../outside", chain)
