"""Shared utilities for adding kolo1.pth to wheels.

Used by both _build_backend.py and scripts/inject_pth_into_wheel.py
to keep the wheel injection logic DRY.
"""

import base64
import hashlib
import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Callable, Tuple


def mutate_wheel_in_place(wheel_path: Path, mutator: Callable[[Path], None]) -> None:
    """Extract wheel to temp dir, run mutator(root_path), rezip to original path."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        with zipfile.ZipFile(wheel_path, "r") as wheel_zip:
            wheel_zip.extractall(temp_path)

        mutator(temp_path)

        temp_wheel = temp_path / "rebuilt.whl"
        with zipfile.ZipFile(temp_wheel, "w", zipfile.ZIP_DEFLATED) as wheel_zip:
            for file_path in temp_path.rglob("*"):
                if file_path.is_file() and file_path != temp_wheel:
                    arcname = str(file_path.relative_to(temp_path))
                    wheel_zip.write(file_path, arcname)

        if wheel_path.exists():
            os.chmod(wheel_path, 0o644)
            os.remove(wheel_path)
        shutil.copy2(str(temp_wheel), str(wheel_path))


def compute_file_hash(file_path: Path) -> Tuple[str, int]:
    """Compute SHA256 hash and size for a file.

    Returns:
        Tuple of (base64-encoded hash, file size in bytes)
    """
    sha256_hash = hashlib.sha256()
    file_size = 0

    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256_hash.update(chunk)
            file_size += len(chunk)

    hash_digest = base64.urlsafe_b64encode(sha256_hash.digest()).rstrip(b"=").decode()
    return hash_digest, file_size


def get_version_from_wheel_name(wheel_name: str) -> str:
    """Extract version from wheel filename like 'kolo-2.42.0-cp312-...'"""
    parts = wheel_name.split("-")
    if len(parts) >= 2:
        return parts[1]
    raise ValueError(f"Cannot extract version from wheel name: {wheel_name}")


def _check_pth_already_present(wheel_path: Path, version: str) -> bool:
    """Check if kolo1.pth is already in the wheel (without extracting fully)."""
    pth_path = f"kolo-{version}.data/purelib/kolo1.pth"
    with zipfile.ZipFile(wheel_path, "r") as wheel_zip:
        return pth_path in wheel_zip.namelist()


def append_to_record(temp_path: Path, record_entry: str) -> None:
    """Append an entry to the RECORD file in an extracted wheel."""
    dist_info_dirs = list(temp_path.glob("*.dist-info"))
    if not dist_info_dirs:
        raise RuntimeError("No .dist-info directory found")
    if len(dist_info_dirs) > 1:
        raise RuntimeError("Multiple .dist-info directories found")

    record_file = dist_info_dirs[0] / "RECORD"
    if not record_file.exists():
        raise RuntimeError("RECORD file not found")

    with open(record_file, "r") as f:
        content = f.read()

    with open(record_file, "a") as f:
        if content and not content.endswith("\n"):
            f.write("\n")
        f.write(record_entry + "\n")


def inject_pth_into_wheel(
    wheel_path: Path,
    pth_source: Path,
    version: str,
) -> bool:
    """Inject the .pth file into a wheel.

    Args:
        wheel_path: Path to the wheel file
        pth_source: Path to the kolo1.pth source file
        version: Package version (e.g., "2.42.0")

    Returns:
        True if injection was performed, False if skipped (already present)
    """
    if _check_pth_already_present(wheel_path, version):
        return False

    def mutator(temp_path: Path) -> None:
        data_dir = temp_path / f"kolo-{version}.data" / "purelib"
        data_dir.mkdir(parents=True, exist_ok=True)
        pth_dest = data_dir / "kolo1.pth"
        shutil.copy2(pth_source, pth_dest)

        hash_digest, file_size = compute_file_hash(pth_dest)
        append_to_record(
            temp_path,
            f"kolo-{version}.data/purelib/kolo1.pth,sha256={hash_digest},{file_size}",
        )

    mutate_wheel_in_place(wheel_path, mutator)
    return True
