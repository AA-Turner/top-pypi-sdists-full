"""Integration test for the Rust plato-fuse binary on a real Plato VM.

Builds the local rust binary, copies it plus a synthetic workload bundle to the
VM, mounts the FUSE filesystem, and runs a small-file-heavy workload intended to
look more like a package-manager install than a single large-file transfer.
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest

from .conftest import build_plato_fuse_binary
from .test_workspace_vm import _VM, CHRONOS_URL, SDK_ROOT, _run_async

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

MAX_GLIBC_VERSION = (2, 38)
SEED_FILE_COUNT = 1800
CREATE_FILE_COUNT = 1200
MODIFY_FILE_COUNT = 200
DELETE_FILE_COUNT = 100
RENAME_FILE_COUNT = 150
PARALLEL_WORKERS = 8
RM_RF_FILE_COUNT = 900
REMOTE_BUNDLE_ROOT = "/tmp/plato-fuse-bundle"
AGENT_BUNDLE_ROOT = "/tmp/plato-fuse-agent-bundle"
AGENT_MOUNT_ROOT = "/mnt/plato-fuse-nfs"
AGENT_RAW_MOUNT_ROOT = "/mnt/plato-raw-nfs"
PERF_WORLD_DIR = Path(__file__).resolve().parent / "plato_fuse_perf_world"


def _build_plato_fuse_binary(tmp_path_factory: pytest.TempPathFactory) -> Path:
    del tmp_path_factory
    return build_plato_fuse_binary(MAX_GLIBC_VERSION)


def _write_seed_files(cache_root: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for idx in range(SEED_FILE_COUNT):
        relpath = Path(f"store/pkg_{idx % 240:03d}/version_{idx % 7}/files/file_{idx:05d}.json")
        content = json.dumps(
            {
                "name": f"pkg-{idx}",
                "version": f"1.{idx % 17}.{idx % 5}",
                "integrity": f"sha512-{idx:08x}",
                "deps": [f"dep-{idx % 13}", f"dep-{(idx + 5) % 19}"],
            },
            sort_keys=True,
        ).encode()
        full_path = cache_root / "cache" / relpath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(content)
        entries.append(
            {
                "relpath": relpath.as_posix(),
                "md5": f"{idx:032x}"[:32],
                "size": len(content),
                "isexec": False,
                "islink": False,
                "symlink_target": "",
            }
        )
    return entries


def _write_workload_script(script_path: Path) -> None:
    script_path.write_text(
        f"""#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import json
import pathlib
import shutil
import sys
import time

SEED_FILE_COUNT = {SEED_FILE_COUNT}
CREATE_FILE_COUNT = {CREATE_FILE_COUNT}
MODIFY_FILE_COUNT = {MODIFY_FILE_COUNT}
DELETE_FILE_COUNT = {DELETE_FILE_COUNT}
RENAME_FILE_COUNT = {RENAME_FILE_COUNT}
PARALLEL_WORKERS = {PARALLEL_WORKERS}
RM_RF_FILE_COUNT = {RM_RF_FILE_COUNT}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("--label", required=True)
    return parser.parse_args()

def list_seed_files() -> list[pathlib.Path]:
    return sorted(root.glob("store/**/*.json"))

def read_chunk(paths: list[pathlib.Path]) -> int:
    checksum = 0
    for path in paths:
        checksum ^= path.stat().st_size
        checksum ^= sum(path.read_bytes())
    return checksum

args = parse_args()
root = pathlib.Path(args.root).resolve()
assert root.exists(), root

metrics: dict[str, float | int | str] = {{}}

start = time.perf_counter()
seed_files = list_seed_files()
assert len(seed_files) == SEED_FILE_COUNT, len(seed_files)
total_bytes = 0
for path in seed_files:
    total_bytes += path.stat().st_size
metrics["cold_metadata_walk_s"] = round(time.perf_counter() - start, 3)
metrics["seed_files"] = len(seed_files)
metrics["seed_bytes"] = total_bytes

start = time.perf_counter()
checksum = 0
for path in seed_files:
    checksum ^= sum(path.read_bytes())
metrics["cold_read_seed_s"] = round(time.perf_counter() - start, 3)
metrics["checksum"] = checksum

start = time.perf_counter()
warm_checksum = 0
for path in seed_files:
    warm_checksum ^= sum(path.read_bytes())
metrics["warm_read_seed_s"] = round(time.perf_counter() - start, 3)
metrics["warm_checksum"] = warm_checksum

start = time.perf_counter()
warm_seed_files = list_seed_files()
warm_total_bytes = 0
for path in warm_seed_files:
    warm_total_bytes += path.stat().st_size
metrics["warm_metadata_walk_s"] = round(time.perf_counter() - start, 3)
metrics["warm_seed_bytes"] = warm_total_bytes

start = time.perf_counter()
chunk_size = max(1, len(seed_files) // PARALLEL_WORKERS)
chunks = [seed_files[idx : idx + chunk_size] for idx in range(0, len(seed_files), chunk_size)]
parallel_checksum = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=PARALLEL_WORKERS) as executor:
    for part in executor.map(read_chunk, chunks):
        parallel_checksum ^= part
metrics["parallel_stat_read_s"] = round(time.perf_counter() - start, 3)
metrics["parallel_checksum"] = parallel_checksum

start = time.perf_counter()
created = []
create_root = root / "node_modules_like"
for idx in range(CREATE_FILE_COUNT):
    target = create_root / f"pkg_{{idx % 150:03d}}" / "node_modules" / f"dep_{{idx % 29:02d}}" / f"file_{{idx:05d}}.js"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"export const value = {{idx}};\\n")
    created.append(target)
metrics["create_small_files_s"] = round(time.perf_counter() - start, 3)

start = time.perf_counter()
for idx, path in enumerate(seed_files[:MODIFY_FILE_COUNT]):
    path.write_text(path.read_text() + f"\\n// modified {{idx}}\\n")
metrics["modify_existing_s"] = round(time.perf_counter() - start, 3)

start = time.perf_counter()
renamed_dir = root / "node_modules_like_renamed"
renamed_dir.mkdir(exist_ok=True)
for path in created[:RENAME_FILE_COUNT]:
    new_path = renamed_dir / path.name
    path.rename(new_path)
metrics["rename_created_s"] = round(time.perf_counter() - start, 3)

start = time.perf_counter()
rmrf_root = root / "rmrf_tree"
for idx in range(RM_RF_FILE_COUNT):
    target = rmrf_root / f"pkg_{{idx % 120:03d}}" / "node_modules" / f"dep_{{idx % 17:02d}}" / f"artifact_{{idx:05d}}.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"rmrf-{{idx}}\\n")
metrics["rm_rf_tree_create_s"] = round(time.perf_counter() - start, 3)

start = time.perf_counter()
shutil.rmtree(rmrf_root)
metrics["rm_rf_tree_delete_s"] = round(time.perf_counter() - start, 3)

start = time.perf_counter()
for path in seed_files[MODIFY_FILE_COUNT:MODIFY_FILE_COUNT + DELETE_FILE_COUNT]:
    path.unlink()
metrics["delete_existing_s"] = round(time.perf_counter() - start, 3)

metrics["label"] = args.label
print(json.dumps(metrics, sort_keys=True))
""",
        encoding="utf-8",
    )
    script_path.chmod(0o755)


@pytest.fixture(scope="module")
def plato_fuse_bundle(tmp_path_factory: pytest.TempPathFactory) -> Path:
    bundle_dir = tmp_path_factory.mktemp("plato-fuse-bundle")
    cache_root = bundle_dir / "cache-root"
    overlay_dir = cache_root / "overlay"
    mount_dir = bundle_dir / "mnt"
    overlay_dir.mkdir(parents=True, exist_ok=True)
    (cache_root / "cache").mkdir(parents=True, exist_ok=True)
    mount_dir.mkdir(parents=True, exist_ok=True)

    entries = _write_seed_files(cache_root)
    binary_path = _build_plato_fuse_binary(tmp_path_factory)
    shutil.copy2(binary_path, bundle_dir / "plato-fuse")
    (bundle_dir / "plato-fuse").chmod(0o755)

    config = {
        "manifest": {"entries": entries},
        "s3_config": {"bucket": "", "prefix": "", "credentials": {}},
        "mountpoint": f"{REMOTE_BUNDLE_ROOT}/mnt",
        "cache_dir": f"{REMOTE_BUNDLE_ROOT}/cache-root",
    }
    (bundle_dir / "config.json").write_text(json.dumps(config), encoding="utf-8")
    _write_workload_script(bundle_dir / "run_smallfile_workload.py")
    return bundle_dir


@pytest.fixture(scope="module")
def perf_vm(plato_fuse_bundle: Path):
    loop = __import__("asyncio").new_event_loop()
    __import__("asyncio").set_event_loop(loop)
    v = _VM()
    try:
        loop.run_until_complete(v.start())
        v.rsync_to(str(SDK_ROOT), "/sdk")
        v.rsync_to(str(PERF_WORLD_DIR), "/perf-world")
        v.rsync_to(str(plato_fuse_bundle), REMOTE_BUNDLE_ROOT)
        loop.run_until_complete(
            v.exec_ok(
                "which rsync || (apt-get update && apt-get install -y rsync)",
                timeout=60,
            )
        )
        loop.run_until_complete(
            v.exec_ok(
                "uv pip install --system -e /sdk -e /perf-world 2>&1",
                timeout=300,
            )
        )
        yield v
    finally:
        loop.run_until_complete(v.close())
        loop.close()


class TestPlatoFuseVM:
    def test_plato_fuse_small_file_workload(self, perf_vm: _VM) -> None:
        config = {
            "world": {
                "package": "plato-world-plato-fuse-perf-test:0.0.1",
                "runtime": {"type": "vm", "vm": {"cpus": 2, "memory": 4096, "disk": 20480}},
                "config": {
                    "bundle_root": REMOTE_BUNDLE_ROOT,
                    "agent_bundle_root": AGENT_BUNDLE_ROOT,
                    "agent_mount_root": AGENT_MOUNT_ROOT,
                    "agent_raw_mount_root": AGENT_RAW_MOUNT_ROOT,
                },
            },
            "session": {
                "session_id": perf_vm.chronos_session_id,
                "plato_session": perf_vm.session.dump().model_dump(),
                "chronos_url": CHRONOS_URL,
                "transport_mode": "nfs_kernel",
            },
            "dev": {
                "ssh_key_path": "/root/.ssh/agent_key",
            },
        }

        config_path = "/tmp/plato-fuse-perf-config.json"
        config_b64 = __import__("base64").b64encode(json.dumps(config).encode()).decode()
        _run_async(perf_vm.exec_ok(f"echo '{config_b64}' | base64 -d > {config_path}", timeout=10))

        code, stdout, stderr = _run_async(
            perf_vm.exec(
                f"PLATO_API_KEY='{os.environ['PLATO_API_KEY']}' "
                f"plato-world-runner run "
                f"--world plato-world-plato-fuse-perf-test "
                f"--config {config_path} -v",
                timeout=1800,
            )
        )

        print(f"STDOUT:\n{stdout}")
        if stderr:
            print(f"STDERR:\n{stderr}")

        assert code == 0, f"Plato fuse perf world failed (exit {code})"

        metrics_json = _run_async(
            perf_vm.exec_ok(
                f"cat {REMOTE_BUNDLE_ROOT}/perf_metrics.json",
                timeout=30,
            )
        )
        print(f"METRICS:\n{metrics_json}")
