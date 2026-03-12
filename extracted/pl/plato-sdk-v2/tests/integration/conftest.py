"""Shared fixtures for integration tests."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import uuid
from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from dotenv import load_dotenv

if TYPE_CHECKING:
    from plato.storage import RolloutStorage

SDK_ROOT = Path(__file__).resolve().parents[2]
PLATO_FUSE_ROOT = SDK_ROOT / "plato-fuse"
CI_SESSION_BASE_TAG = "ci.test"

# Load the nearest .env discovered from the current working directory.
load_dotenv()


# Skip tests that require PLATO_API_KEY
def pytest_collection_modifyitems(config, items):  # type: ignore[no-untyped-def]
    """Skip integration tests that require PLATO_API_KEY if not set.

    Tests in test_browser_agent.py and TestE2EBrowserAgentBasic do NOT require PLATO_API_KEY.
    """
    if not os.environ.get("PLATO_API_KEY"):
        skip_marker = pytest.mark.skip(reason="PLATO_API_KEY not set")
        for item in items:
            # Skip integration tests EXCEPT browser agent tests and basic E2E tests
            if "integration" in str(item.fspath):
                # Allow test_browser_agent.py
                if "test_browser_agent" in str(item.fspath):
                    continue
                # Allow TestE2EBrowserAgentBasic tests
                if "test_e2e_browser_agent" in str(item.fspath) and "TestE2EBrowserAgentBasic" in item.nodeid:
                    continue
                # Allow test_harbor_agent_runner.py (uses its own API keys)
                if "test_harbor_agent_runner" in str(item.fspath):
                    continue
                # Allow test_chronos_callback.py (uses its own API keys)
                if "test_chronos_callback" in str(item.fspath):
                    continue
                item.add_marker(skip_marker)


@pytest.fixture
def run_id() -> str:
    """Generate unique run ID for test."""
    return f"test-{uuid.uuid4().hex[:8]}"


@pytest.fixture
def temp_db_path() -> Generator[Path, None, None]:
    """Create temporary database path for test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir) / "test_rollouts.db"


@pytest.fixture
def storage(run_id: str, temp_db_path: Path) -> Generator[RolloutStorage, None, None]:
    """Create RolloutStorage for test."""
    from plato.storage import RolloutStorage

    storage = RolloutStorage(
        run_id=run_id,
        agent_type="test-agent",
        model="test-model",
        world_name="test-world",
        db_path=temp_db_path,
    )
    yield storage
    storage.close()


@pytest.fixture
def temp_workspace() -> Generator[Path, None, None]:
    """Create temporary workspace directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def parse_glibc_versions(binary_path: Path) -> list[tuple[int, int]]:
    proc = subprocess.run(
        ["objdump", "-T", str(binary_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    versions: set[tuple[int, int]] = set()
    for major, minor in re.findall(r"GLIBC_(\d+)\.(\d+)", proc.stdout):
        versions.add((int(major), int(minor)))
    return sorted(versions)


def build_plato_fuse_binary(max_glibc_version: tuple[int, int]) -> Path:
    """Build a VM-compatible plato-fuse binary from current source."""
    build_root = Path("/tmp/plato-fuse-build-cache")
    build_root.mkdir(parents=True, exist_ok=True)

    zigbuild = shutil.which("cargo-zigbuild")
    zig = shutil.which("zig")
    assert zigbuild and zig, "zig and cargo-zigbuild are required to build a VM-compatible plato-fuse binary"

    target = f"x86_64-unknown-linux-gnu.{max_glibc_version[0]}.{max_glibc_version[1]}"
    cmd = [
        "cargo",
        "zigbuild",
        "--release",
        "--manifest-path",
        str(PLATO_FUSE_ROOT / "Cargo.toml"),
        "--target",
        target,
        "--target-dir",
        str(build_root),
    ]
    binary_path = build_root / "x86_64-unknown-linux-gnu" / "release" / "plato-fuse"

    subprocess.run(cmd, check=True, cwd=SDK_ROOT)
    assert binary_path.exists(), f"Expected built binary at {binary_path}"

    max_required = max(parse_glibc_versions(binary_path), default=(0, 0))
    assert max_required <= max_glibc_version, (
        f"Built binary requires GLIBC_{max_required[0]}.{max_required[1]}, "
        f"expected <= GLIBC_{max_glibc_version[0]}.{max_glibc_version[1]}"
    )
    return binary_path


@pytest.fixture(scope="session")
def plato_fuse_binary_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Stage a source-built plato-fuse binary in a rsync-friendly directory."""
    staged_dir = tmp_path_factory.mktemp("plato-fuse-bin")
    binary_path = build_plato_fuse_binary((2, 34))
    shutil.copy2(binary_path, staged_dir / "plato-fuse")
    (staged_dir / "plato-fuse").chmod(0o755)
    return staged_dir
