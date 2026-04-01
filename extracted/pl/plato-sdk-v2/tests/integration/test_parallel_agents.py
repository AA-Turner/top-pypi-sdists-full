"""Integration test for ParallelAgentOrchestrator via `plato chronos test`."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import pytest

from plato.cli.chronos.test import TestConfig, TestRunner

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not os.environ.get("PLATO_API_KEY"), reason="PLATO_API_KEY not set"),
]

CONFIG_PATH = (
    Path(__file__).resolve().parent / "parallel_agents_test_world" / "tests" / "e2e" / "configs" / "basic.json"
)


def test_parallel_agents_orchestrator_e2e() -> None:
    config = TestConfig.from_file(CONFIG_PATH)
    runner = TestRunner(
        config=config,
        config_path=CONFIG_PATH,
        api_key=os.environ["PLATO_API_KEY"],
        phase_filter="all",
        pytest_args=None,
        artifacts_dir=None,
        verbose=True,
    )

    exit_code = asyncio.run(runner.run())
    assert exit_code == 0, f"parallel agents e2e failed (exit {exit_code})"
