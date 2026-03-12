"""Integration test for Rust plato-fuse correctness on a real Plato VM.

Builds the local Rust binary, creates a small bundle of ~20 seed files,
syncs everything to the VM via extra_sync, and runs a world that exercises
FUSE + NFS correctness.

Requires: PLATO_API_KEY
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import pytest

from plato.cli.chronos.test import TestConfig, TestRunner

from .scripts.prepare_fuse_bundle import prepare_correctness_bundle

pytestmark = pytest.mark.skipif(
    not os.environ.get("PLATO_API_KEY"),
    reason="PLATO_API_KEY not set",
)

CONFIG_PATH = Path(__file__).parent / "configs" / "fuse-correctness-test.json"


class TestPlatoFuseCorrectness:
    def test_fuse_correctness(self, tmp_path: Path) -> None:
        bundle_dir = prepare_correctness_bundle(tmp_path / "fuse-bundle")

        config = TestConfig.from_file(CONFIG_PATH)
        config = config.model_copy(
            update={"dev": config.dev.model_copy(update={"extra_sync": {"fuse-bundle": bundle_dir}})}
        )

        runner = TestRunner(
            config=config,
            config_path=CONFIG_PATH,
            api_key=os.environ["PLATO_API_KEY"],
            phase_filter="all",
            pytest_args=None,
            artifacts_dir=None,
            keep_vm_on_fail=False,
            verbose=True,
        )
        exit_code = asyncio.run(runner.run())
        assert exit_code == 0
