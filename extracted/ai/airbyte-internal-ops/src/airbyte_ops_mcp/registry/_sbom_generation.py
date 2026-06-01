# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""SBOM (Software Bill of Materials) generation and upload.

This module provides functions to generate SPDX SBOMs from connector Docker
images using `anchore/syft` and upload them to GCS.

The GCS destination path for SBOMs is:

    gs://<bucket>/sbom/<docker_repo>/<docker_tag>.spdx.json

This mirrors the layout used by the legacy `upload-connector-metadata.sh`
script.
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from airbyte_ops_mcp.registry._constants import (
    SBOM_FILE_NAME,
    SYFT_DOCKER_IMAGE,
)
from airbyte_ops_mcp.registry._gcs_helpers import get_gcs_storage_client
from airbyte_ops_mcp.registry._resolve_gcs_paths import sbom_blob_path
from airbyte_ops_mcp.registry.store import RegistryStore

logger = logging.getLogger(__name__)


def generate_sbom(
    docker_image: str,
    output_dir: Path,
) -> Path:
    """Generate an SPDX SBOM for *docker_image* using Syft.

    Runs the `anchore/syft` Docker image against the given connector
    image and writes the SPDX JSON output to `output_dir`.

    Args:
        docker_image: Fully qualified image (e.g. `airbyte/source-faker:1.2.3`).
        output_dir: Directory to write the SBOM file to.

    Returns:
        Path to the generated SBOM file.

    Raises:
        RuntimeError: If the `docker run` command fails.
    """
    output_path = output_dir / SBOM_FILE_NAME

    cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        "/var/run/docker.sock:/var/run/docker.sock",
        SYFT_DOCKER_IMAGE,
        "-o",
        "spdx-json",
        docker_image,
    ]
    logger.info("Generating SBOM: %s", " ".join(cmd))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"SBOM generation failed with exit code {result.returncode}: "
            f"{result.stderr.strip()}"
        )

    output_path.write_text(result.stdout)
    logger.info("Wrote SBOM to %s", output_path)
    return output_path


def upload_sbom(
    sbom_path: Path,
    connector_name: str,
    version: str,
    store: RegistryStore,
    dry_run: bool = False,
) -> str:
    """Upload a locally generated SBOM to GCS.

    Args:
        sbom_path: Path to the local SBOM file.
        connector_name: Connector name without owner prefix
            (e.g. `source-faker`).
        version: Connector version / Docker image tag (e.g. `1.2.3`).
        store: Parsed store target containing bucket, prefix, and stage info.
        dry_run: If `True`, report what would be uploaded without writing.

    Returns:
        The GCS URI of the uploaded (or would-be-uploaded) SBOM file.

    Raises:
        FileNotFoundError: If `sbom_path` does not exist.
    """
    if not sbom_path.is_file():
        raise FileNotFoundError(f"SBOM file not found: {sbom_path}")

    blob_path = sbom_blob_path(
        connector_name=connector_name, version=version, store=store
    )
    gcs_uri = f"gs://{store.bucket}/{blob_path}"

    if dry_run:
        logger.info("[DRY RUN] Would upload SBOM to %s", gcs_uri)
        return gcs_uri

    client = get_gcs_storage_client()
    bucket = client.bucket(store.bucket)
    blob = bucket.blob(blob_path)
    blob.upload_from_filename(str(sbom_path))
    logger.info("Uploaded SBOM to %s", gcs_uri)
    return gcs_uri
