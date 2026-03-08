"""Integration test for Rust plato-fuse correctness on a real Plato VM.

Builds the local Rust binary, creates a small bundle of ~20 seed files, copies
everything to the VM, and runs a world that exercises FUSE + NFS correctness:
- lazy loading (files not fetched until read)
- all filesystem operations through FUSE
- metadata tracking (created/modified/deleted)
- cross-VM NFS sync (agent ↔ world)
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest

from .conftest import build_plato_fuse_binary
from .test_workspace_vm import _VM, CHRONOS_URL, SDK_ROOT, _run_async

pytestmark = pytest.mark.skipif(
    not os.environ.get("PLATO_API_KEY"),
    reason="PLATO_API_KEY not set",
)

CORRECTNESS_WORLD_DIR = Path(__file__).resolve().parent / "plato_fuse_correctness_world"
SEED_FILE_COUNT = 20
REMOTE_BUNDLE_ROOT = "/tmp/plato-fuse-bundle"
UNKNOWN_SIZE_RELPATH = "store/unknown_size/file.txt"
MISSING_RELPATH = "store/missing_size/file.txt"


def _build_plato_fuse_binary() -> Path:
    return build_plato_fuse_binary((2, 34))


def _create_seed_files(cache_root: Path) -> list[dict]:
    """Create a small set of seed files in the cache directory."""
    entries: list[dict] = []
    for i in range(SEED_FILE_COUNT):
        relpath = f"store/pkg_{i:03d}/file_{i:04d}.json"
        content = json.dumps({"name": f"pkg-{i}", "version": f"1.{i % 5}.0"}).encode()
        full_path = cache_root / "cache" / relpath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(content)
        entries.append(
            {
                "relpath": relpath,
                "md5": f"{i:032x}"[:32],
                "size": len(content),
                "isexec": False,
                "islink": False,
                "symlink_target": "",
            }
        )

    unknown_content = b"unknown-size fixture\n"
    unknown_path = cache_root / "cache" / UNKNOWN_SIZE_RELPATH
    unknown_path.parent.mkdir(parents=True, exist_ok=True)
    unknown_path.write_bytes(unknown_content)
    entries.append(
        {
            "relpath": UNKNOWN_SIZE_RELPATH,
            "md5": "f" * 32,
            "size": 0,
            "isexec": False,
            "islink": False,
            "symlink_target": "",
        }
    )
    entries.append(
        {
            "relpath": MISSING_RELPATH,
            "md5": "e" * 32,
            "size": 0,
            "isexec": False,
            "islink": False,
            "symlink_target": "",
        }
    )
    return entries


@pytest.fixture(scope="module")
def plato_fuse_bundle(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Build the binary + create a small bundle with seed files."""
    bundle_dir = tmp_path_factory.mktemp("plato-fuse-bundle")
    cache_root = bundle_dir / "cache-root"
    (cache_root / "overlay").mkdir(parents=True)
    (cache_root / "cache").mkdir(parents=True)
    (bundle_dir / "mnt").mkdir()

    entries = _create_seed_files(cache_root)
    binary_path = _build_plato_fuse_binary()
    shutil.copy2(binary_path, bundle_dir / "plato-fuse")
    (bundle_dir / "plato-fuse").chmod(0o755)

    # Copy workload script into bundle (so it gets rsync'd to agent too)
    shutil.copy2(CORRECTNESS_WORLD_DIR / "workload.py", bundle_dir / "workload.py")

    config = {
        "manifest": {"entries": entries},
        "s3_config": {"bucket": "", "prefix": "", "credentials": {}},
        "mountpoint": f"{REMOTE_BUNDLE_ROOT}/mnt",
        "cache_dir": f"{REMOTE_BUNDLE_ROOT}/cache-root",
    }
    (bundle_dir / "config.json").write_text(json.dumps(config))
    return bundle_dir


@pytest.fixture(scope="module")
def correctness_vm(plato_fuse_bundle: Path):
    """Spin up a VM, sync SDK + correctness world + bundle."""
    loop = __import__("asyncio").new_event_loop()
    __import__("asyncio").set_event_loop(loop)
    v = _VM(world_name="plato-world-fuse-correctness", tags=["ci.test", "fuse-correctness"])
    try:
        loop.run_until_complete(v.start())
        v.rsync_to(str(SDK_ROOT), "/sdk")
        v.rsync_to(str(CORRECTNESS_WORLD_DIR), "/correctness-world")
        v.rsync_to(str(plato_fuse_bundle), REMOTE_BUNDLE_ROOT)
        loop.run_until_complete(
            v.exec_ok(
                "which rsync || (apt-get update && apt-get install -y rsync)",
                timeout=60,
            )
        )
        loop.run_until_complete(
            v.exec_ok(
                "uv pip install --system -e /sdk -e /correctness-world 2>&1",
                timeout=300,
            )
        )
        yield v
    finally:
        loop.run_until_complete(v.close())
        loop.close()


class TestPlatoFuseCorrectness:
    def test_fuse_correctness(self, correctness_vm: _VM) -> None:
        config = {
            "world": {
                "package": "plato-world-fuse-correctness:0.0.1",
                "runtime": {
                    "type": "vm",
                    "vm": {"cpus": 2, "memory": 4096, "disk": 20480},
                },
                "config": {
                    "bundle_root": REMOTE_BUNDLE_ROOT,
                    "agent_bundle_root": "/tmp/plato-fuse-agent-bundle",
                    "agent_mount_root": "/mnt/plato-fuse-nfs",
                },
            },
            "session": {
                "session_id": correctness_vm.chronos_session_id,
                "plato_session": correctness_vm.session.dump().model_dump(),
                "chronos_url": CHRONOS_URL,
                "otel_url": correctness_vm.otel_url or "",
                "transport_mode": "nfs_kernel",
            },
            "dev": {
                "ssh_key_path": "/root/.ssh/agent_key",
            },
        }

        config_path = "/tmp/plato-fuse-correctness-config.json"
        config_b64 = __import__("base64").b64encode(json.dumps(config).encode()).decode()
        _run_async(
            correctness_vm.exec_ok(
                f"echo '{config_b64}' | base64 -d > {config_path}",
                timeout=10,
            )
        )

        # Debug: verify world is installed and config is readable
        _run_async(
            correctness_vm.exec_ok(
                "python3 -c \"from plato_fuse_correctness_world import FuseCorrectnessWorld; print('World found')\"",
                timeout=60,
            )
        )
        _run_async(correctness_vm.exec_ok(f"cat {config_path} | python3 -m json.tool > /dev/null", timeout=10))
        _run_async(correctness_vm.exec_ok(f"ls -la {REMOTE_BUNDLE_ROOT}/", timeout=10))

        log_file = "/tmp/plato-fuse-correctness-runner.log"
        code, stdout, stderr = _run_async(
            correctness_vm.exec(
                f"PLATO_API_KEY='{os.environ['PLATO_API_KEY']}' "
                f"plato-world-runner run "
                f"--world plato-world-fuse-correctness "
                f"--config {config_path} -v "
                f"> {log_file} 2>&1; "
                f"status=$?; echo EXIT_CODE=$status; exit $status",
                timeout=1800,
            )
        )

        # Read a bounded tail from the log file so failures in the world run
        # don't get masked by a secondary timeout while collecting diagnostics.
        try:
            log_code, log_output, log_err = _run_async(
                correctness_vm.exec(
                    f"test -f {log_file} && tail -n 400 {log_file}",
                    timeout=120,
                )
            )
            if log_code == 0:
                print(f"WORLD RUNNER LOG:\n{log_output}")
            else:
                log_output = f"<log unavailable: {log_err}>"
        except Exception as exc:
            log_output = f"<log unavailable: {exc}>"

        # Read and display test results even if the world failed so we keep the
        # per-phase JSON instead of only the runner log.
        try:
            code2, results_json, err2 = _run_async(
                correctness_vm.exec(
                    f"test -f {REMOTE_BUNDLE_ROOT}/test_results.json && cat {REMOTE_BUNDLE_ROOT}/test_results.json",
                    timeout=30,
                )
            )
        except Exception as exc:
            code2, results_json, err2 = 1, "", str(exc)
        results = json.loads(results_json) if code2 == 0 else None
        if results is not None:
            print(f"TEST RESULTS:\n{json.dumps(results, indent=2)}")

        assert code == 0, (
            f"Fuse correctness world failed (exit {code})\n"
            f"World stdout: {stdout}\nWorld stderr: {stderr}\n"
            f"World log: {log_output}\n"
            f"Results: {json.dumps(results, indent=2) if results is not None else f'missing ({err2})'}"
        )

        assert results is not None, (
            f"test_results.json not found after successful world run.\n"
            f"World stdout: {stdout}\nWorld stderr: {stderr}\n"
            f"cat stderr: {err2}"
        )

        for test_name, result in results.items():
            if isinstance(result, dict):
                assert result.get("pass"), f"{test_name}: {result.get('errors')}"
