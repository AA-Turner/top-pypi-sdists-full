# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Manifest factory for the Whisper transcription UDFs."""

from pathlib import Path

from geneva.manifest.mgr import GenevaManifest


def create_manifest(name: str | None = None) -> GenevaManifest:
    try:
        import tomllib
    except ModuleNotFoundError:  # Python 3.10 compatibility
        import tomli as tomllib  # type: ignore[no-redef]

    udf_dir = Path(__file__).parent
    pyproject_path = udf_dir / "pyproject.toml"

    with pyproject_path.open("rb") as f:
        pyproject = tomllib.load(f)

    manifest_name = name or pyproject["project"]["name"]

    return (
        GenevaManifest.create_pip(manifest_name)
        .pip([
            "--extra-index-url=https://pypi.fury.io/lancedb/",
            "--extra-index-url=https://pypi.fury.io/lance-format/",
            "--pre",
            *pyproject["project"]["dependencies"],
        ])
        .py_modules([])
        .delete_local_zips(True)
        .upload_site_packages()
        .build()
    )
