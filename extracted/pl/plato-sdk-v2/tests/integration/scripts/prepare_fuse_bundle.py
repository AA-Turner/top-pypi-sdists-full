"""Build a FUSE test bundle (binary + seed files + config)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from tests.integration.conftest import build_plato_fuse_binary

MAX_GLIBC_VERSION = (2, 34)

# Correctness world constants
CORRECTNESS_WORLD_DIR = Path(__file__).resolve().parent.parent / "plato_fuse_correctness_world"
UNKNOWN_SIZE_RELPATH = "store/unknown_size/file.txt"
MISSING_RELPATH = "store/missing_size/file.txt"


def _create_seed_files(cache_root: Path, count: int) -> list[dict]:
    entries: list[dict] = []
    for i in range(count):
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
    return entries


def prepare_correctness_bundle(bundle_dir: Path) -> Path:
    """Build a FUSE correctness test bundle with ~20 seed files."""
    cache_root = bundle_dir / "cache-root"
    (cache_root / "overlay").mkdir(parents=True)
    (cache_root / "cache").mkdir(parents=True)
    (bundle_dir / "mnt").mkdir()

    entries = _create_seed_files(cache_root, count=20)

    # Add special files for correctness tests
    unknown_content = b"unknown-size fixture\n"
    unknown_path = cache_root / "cache" / UNKNOWN_SIZE_RELPATH
    unknown_path.parent.mkdir(parents=True, exist_ok=True)
    unknown_path.write_bytes(unknown_content)
    entries.append(
        {
            "relpath": UNKNOWN_SIZE_RELPATH,
            "md5": "f" * 32,
            "size": len(unknown_content),
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

    binary_path = build_plato_fuse_binary(MAX_GLIBC_VERSION)
    shutil.copy2(binary_path, bundle_dir / "plato-fuse")
    (bundle_dir / "plato-fuse").chmod(0o755)

    # Copy workload script
    shutil.copy2(CORRECTNESS_WORLD_DIR / "workload.py", bundle_dir / "workload.py")

    remote_bundle_root = "/extra/fuse-bundle"
    config = {
        "manifest": {"entries": entries},
        "s3_config": {"bucket": "", "prefix": "", "credentials": {}},
        "mountpoint": f"{remote_bundle_root}/mnt",
        "cache_dir": f"{remote_bundle_root}/cache-root",
    }
    (bundle_dir / "config.json").write_text(json.dumps(config))
    return bundle_dir


def prepare_perf_bundle(bundle_dir: Path) -> Path:
    """Build a FUSE perf test bundle with ~1800 seed files."""
    cache_root = bundle_dir / "cache-root"
    (cache_root / "overlay").mkdir(parents=True)
    (cache_root / "cache").mkdir(parents=True)
    (bundle_dir / "mnt").mkdir()

    seed_count = 1800
    entries = _create_perf_seed_files(cache_root, seed_count)

    binary_path = build_plato_fuse_binary((2, 38))
    shutil.copy2(binary_path, bundle_dir / "plato-fuse")
    (bundle_dir / "plato-fuse").chmod(0o755)

    remote_bundle_root = "/extra/fuse-bundle"
    config = {
        "manifest": {"entries": entries},
        "s3_config": {"bucket": "", "prefix": "", "credentials": {}},
        "mountpoint": f"{remote_bundle_root}/mnt",
        "cache_dir": f"{remote_bundle_root}/cache-root",
    }
    (bundle_dir / "config.json").write_text(json.dumps(config))
    _write_perf_workload_script(bundle_dir / "run_smallfile_workload.py", seed_count)
    return bundle_dir


def _create_perf_seed_files(cache_root: Path, count: int) -> list[dict]:
    entries: list[dict] = []
    for idx in range(count):
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


def _write_perf_workload_script(script_path: Path, seed_count: int) -> None:
    create_count = 1200
    modify_count = 200
    delete_count = 100
    rename_count = 150
    parallel_workers = 8
    rm_rf_count = 900

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

SEED_FILE_COUNT = {seed_count}
CREATE_FILE_COUNT = {create_count}
MODIFY_FILE_COUNT = {modify_count}
DELETE_FILE_COUNT = {delete_count}
RENAME_FILE_COUNT = {rename_count}
PARALLEL_WORKERS = {parallel_workers}
RM_RF_FILE_COUNT = {rm_rf_count}

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
