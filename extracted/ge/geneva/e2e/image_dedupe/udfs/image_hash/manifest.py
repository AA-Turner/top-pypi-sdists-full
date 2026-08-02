# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Manifest factory for image hash UDFs.

This module creates GenevaManifest objects by reading dependencies
from pyproject.toml, providing a single source of truth for UDF dependencies.
"""

from pathlib import Path

from geneva.manifest import GenevaManifest


def create_manifest(name: str | None = None) -> GenevaManifest:
    """
    Create a GenevaManifest for image hash UDFs.

    Reads dependencies from pyproject.toml and creates a manifest
    that can be uploaded to Ray workers.

    Args:
        name: Optional manifest name. If not provided, uses project name from pyproject.toml

    Returns:
        GenevaManifest configured with dependencies and py_modules
    """
    # Python 3.10 compatibility - use tomli backport if tomllib not available
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore[no-redef]

    udf_dir = Path(__file__).parent
    pyproject_path = udf_dir / "pyproject.toml"

    with pyproject_path.open("rb") as f:
        pyproject = tomllib.load(f)

    manifest_name = name or pyproject["project"]["name"]

    return (
        GenevaManifest.create_pip(manifest_name)
        .pip(pyproject["project"]["dependencies"])
        .upload_site_packages()
        .delete_local_zips(True)
        .build()
    )
