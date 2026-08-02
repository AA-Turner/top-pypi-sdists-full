# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Manifest factory for frame extractor UDF.

This module creates GenevaManifest objects with conda dependencies for
torchcodec, FFmpeg, Pillow, etc. (required for frame extraction; torchcodec
needs FFmpeg shared libs from conda).
"""

from pathlib import Path

from geneva.manifest import GenevaManifest

# Conda env for frame extraction: pytorch, torchcodec, ffmpeg, Pillow
# ray-ml images are deprecated (removed after Ray 2.50.x), so all ML deps
# must be installed via the conda env on base rayproject/ray images.
CONDA_ENV = {
    "channels": ["conda-forge"],
    "dependencies": [
        "python=3.10",
        "ffmpeg<8",
        "imageio",
        "moviepy",
        "Pillow",
        "pyarrow=21.0.0",
        "pandas",
        "pip",
        {
            "pip": [
                "--extra-index-url=https://pypi.fury.io/lance-format/",
                "--extra-index-url=https://pypi.fury.io/lancedb/",
                "attrs>=23,<25",
                "cattrs",
                "pylance>=1.1.0b2",
                "lancedb>=0.25.4b2",
                "lance-namespace>=0.2.1",
                "cloudpickle",
                "tenacity",
                "requests",
                "urllib3>=2,<3",
                "more-itertools",
                "toml>=0.10.2",
                "pyyaml>=6.0.2",
                "tqdm",
                "bidict",
                "emoji",
                "multiprocess",
                "aiohttp>=3.12.12",
                "fsspec",
                "torch==2.10.0",
                "torchvision==0.25.0",
                "torchcodec==0.10.0",
                "fsspec[gcs]>=2023.0.0",
                "gcsfs>=2023.0.0",
                "numpy>=2.2.6",
                "tomli>=2.0; python_version<'3.11'",
                "kubernetes",
                "geneva",
                "google-cloud-storage",
            ],
        },
    ],
}


def create_manifest(name: str | None = None) -> GenevaManifest:
    """
    Create a GenevaManifest for frame extractor UDF with conda deps.

    Args:
        name: Optional manifest name. If not provided, uses project name
              from pyproject.toml

    Returns:
        GenevaManifest configured with conda env (no pip; conda provides all).
    """
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
        GenevaManifest.create_conda(manifest_name)
        .conda(CONDA_ENV)
        .delete_local_zips(True)
        .build()
    )
