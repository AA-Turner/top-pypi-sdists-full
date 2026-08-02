# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Manifest factory for AV image curation UDFs (OWLv2 + SigLIP2).

Creates a GenevaManifest by reading dependencies from pyproject.toml.
"""

from pathlib import Path

from geneva.manifest import GenevaManifest


def create_manifest(name: str | None = None) -> GenevaManifest:
    """Create a GenevaManifest for AV curation GPU UDFs."""
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
        .pip(
            [
                "--extra-index-url=https://pypi.fury.io/lancedb/",
                "--extra-index-url=https://pypi.fury.io/lance-format/",
                "--pre",
                *pyproject["project"]["dependencies"],
            ]
        )
        .upload_site_packages()
        .delete_local_zips(True)
        .build()
    )
