"""VM integration test — workspace e2e via plato chronos test runner.

Spins up a VM, syncs the SDK + test world package, then invokes
``plato-world-runner run --world plato-world-structured-execution``
inside the VM.  All actual test logic (NFS, rsync, permissions, lazy DVC)
lives in ``workspace_test_world/world.py``.

Requires: PLATO_API_KEY
"""

from __future__ import annotations

import asyncio
import os
import shutil
from pathlib import Path

import pytest

from plato.cli.chronos.test import TestConfig, TestRunner

from .conftest import build_plato_fuse_binary

pytestmark = pytest.mark.skipif(
    not os.environ.get("PLATO_API_KEY"),
    reason="PLATO_API_KEY not set",
)

CONFIG_PATH = Path(__file__).parent / "configs" / "workspace-test.json"


class TestWorkspaceVM:
    def test_workspace_world(self, tmp_path: Path) -> None:
        """Run the workspace test world — exercises NFS, rsync, perms, lazy DVC."""
        # Build and stage the FUSE binary so the VM uses the latest version
        fuse_bin_dir = tmp_path / "fuse-bin"
        fuse_bin_dir.mkdir()
        binary_path = build_plato_fuse_binary((2, 34))
        shutil.copy2(binary_path, fuse_bin_dir / "plato-fuse")
        (fuse_bin_dir / "plato-fuse").chmod(0o755)

        config = TestConfig.from_file(CONFIG_PATH)
        config = config.model_copy(
            update={"dev": config.dev.model_copy(update={"extra_sync": {"fuse-bin": fuse_bin_dir}})}
        )
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
        assert exit_code == 0
