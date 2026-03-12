"""Integration test for the Rust plato-fuse binary on a real Plato VM.

Builds the local Rust binary, copies it plus a synthetic workload bundle to the
VM, mounts the FUSE filesystem, and runs a small-file-heavy workload intended to
look more like a package-manager install than a single large-file transfer.

Requires: PLATO_API_KEY, RUN_FUSE_PERF=1
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import pytest

from plato.cli.chronos.test import TestConfig, TestRunner

from .scripts.prepare_fuse_bundle import prepare_perf_bundle

pytestmark = [
    pytest.mark.skipif(
        not os.environ.get("PLATO_API_KEY"),
        reason="PLATO_API_KEY not set",
    ),
    pytest.mark.skipif(
        not os.environ.get("RUN_FUSE_PERF"),
        reason="FUSE perf benchmark skipped by default (set RUN_FUSE_PERF=1 to enable)",
    ),
]

CONFIG_PATH = Path(__file__).parent / "configs" / "fuse-perf-test.json"


class TestPlatoFuseVM:
    def test_plato_fuse_small_file_workload(self, tmp_path: Path) -> None:
        bundle_dir = prepare_perf_bundle(tmp_path / "fuse-bundle")

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
