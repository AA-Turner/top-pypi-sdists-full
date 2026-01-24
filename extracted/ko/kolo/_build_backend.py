"""Custom build backend that wraps maturin and adds .pth file support."""

import os
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any, Dict, Union

# Add scripts/ to path for wheel_utils import
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from maturin import build_sdist as maturin_build_sdist
from maturin import build_wheel as maturin_build_wheel
from maturin import build_editable as maturin_build_editable
from maturin import (
    get_requires_for_build_sdist,
    get_requires_for_build_wheel,
    get_requires_for_build_editable as maturin_get_requires_for_build_editable,
    prepare_metadata_for_build_wheel,
    prepare_metadata_for_build_editable as maturin_prepare_metadata_for_build_editable,
)

from wheel_utils import (
    inject_pth_into_wheel,
    get_version_from_wheel_name,
    mutate_wheel_in_place,
    append_to_record,
    compute_file_hash,
)


def build_wheel(
    wheel_directory: str,
    config_settings: Union[Dict[str, Any], None] = None,
    metadata_directory: Union[str, None] = None,
) -> str:
    """Build wheel using maturin, then add our .pth file."""
    wheel_name = maturin_build_wheel(
        wheel_directory, config_settings, metadata_directory
    )

    wheel_path = Path(wheel_directory) / wheel_name
    pth_source = Path("kolo1.pth")

    if pth_source.exists():
        version = get_version_from_wheel_name(wheel_name)
        inject_pth_into_wheel(wheel_path, pth_source, version)

    return wheel_name


def build_editable(
    wheel_directory: str,
    config_settings: Union[Dict[str, Any], None] = None,
    metadata_directory: Union[str, None] = None,
) -> str:
    """Build an editable wheel using maturin, then add our .pth file."""
    wheel_name = maturin_build_editable(
        wheel_directory, config_settings, metadata_directory
    )

    # For editable installs, the .pth file goes directly in the wheel root,
    # not in .data/purelib/. maturin creates kolo.pth for src/ path, we add
    # kolo1.pth separately for KOLO=1 auto-activation.
    wheel_path = Path(wheel_directory) / wheel_name
    pth_source = Path("kolo1.pth")

    if pth_source.exists():

        def mutator(temp_path: Path) -> None:
            pth_dest = temp_path / "kolo1.pth"
            shutil.copy2(pth_source, pth_dest)
            hash_digest, file_size = compute_file_hash(pth_dest)
            append_to_record(temp_path, f"kolo1.pth,sha256={hash_digest},{file_size}")

        mutate_wheel_in_place(wheel_path, mutator)

    return wheel_name


def get_requires_for_build_editable(config_settings=None):
    """Return requirements for building an editable install."""
    return maturin_get_requires_for_build_editable(config_settings)


def prepare_metadata_for_build_editable(
    metadata_directory: str,
    config_settings: Union[Dict[str, Any], None] = None,
) -> str:
    """Prepare metadata for editable install."""
    return maturin_prepare_metadata_for_build_editable(
        metadata_directory, config_settings
    )


def build_sdist(
    sdist_directory: str,
    config_settings: Union[Dict[str, Any], None] = None,
) -> str:
    """Build sdist using maturin, then add our .pth file and wheel_utils."""
    # First build the sdist with maturin
    sdist_name = maturin_build_sdist(sdist_directory, config_settings)

    # Now we need to add the .pth file to the sdist
    sdist_path = Path(sdist_directory) / sdist_name

    # Extract tarball, add file, rebuild
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Extract the sdist
        with tarfile.open(sdist_path, "r:gz") as tar:
            tar.extractall(temp_path)

        # Find the extracted directory (should be kolo-{version})
        extracted_dirs = [d for d in temp_path.iterdir() if d.is_dir()]
        if not extracted_dirs:
            raise RuntimeError("No directory found in sdist")
        if len(extracted_dirs) > 1:
            raise RuntimeError(f"Multiple directories found in sdist: {extracted_dirs}")
        extracted_dir = extracted_dirs[0]

        # Copy kolo1.pth to the extracted directory
        pth_source = Path("kolo1.pth")
        if pth_source.exists():
            shutil.copy2(pth_source, extracted_dir / "kolo1.pth")

        # Copy _build_backend.py to the extracted directory (needed for building from sdist)
        backend_source = Path("_build_backend.py")
        if backend_source.exists():
            shutil.copy2(backend_source, extracted_dir / "_build_backend.py")

        # Copy scripts/wheel_utils.py to the extracted directory (needed for building from sdist)
        utils_source = Path("scripts/wheel_utils.py")
        if utils_source.exists():
            scripts_dir = extracted_dir / "scripts"
            scripts_dir.mkdir(exist_ok=True)
            shutil.copy2(utils_source, scripts_dir / "wheel_utils.py")

        # Rebuild the sdist
        # Use temporary file to avoid data loss if rebuild fails
        temp_sdist = sdist_path.with_suffix(".tar.gz.tmp")
        with tarfile.open(temp_sdist, "w:gz") as tar:
            tar.add(extracted_dir, arcname=extracted_dir.name)
        os.remove(sdist_path)
        temp_sdist.rename(sdist_path)

    return sdist_name


# Re-export other required functions from maturin
__all__ = [
    "build_wheel",
    "build_sdist",
    "build_editable",
    "get_requires_for_build_wheel",
    "get_requires_for_build_sdist",
    "get_requires_for_build_editable",
    "prepare_metadata_for_build_wheel",
    "prepare_metadata_for_build_editable",
]
