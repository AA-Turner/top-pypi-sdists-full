# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Analyze and generate Python connector dependency metadata.

This module replaces the legacy `upload-python-dependencies.sh` script by
providing functions that:

* Detect whether a connector is Python-based (via metadata tags).
* Run `pip freeze` inside the connector's Docker image to capture the
  full dependency tree.
* Build and write a `dependencies.json` artifact matching the format
  expected by downstream consumers (e.g. the compile step's
  `packageInfo.cdk_version` extraction).
* Extract the `airbyte-cdk` version from a dependencies dict.
"""

from __future__ import annotations

import json
import logging
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from airbyte_ops_mcp.registry._constants import (
    CONNECTOR_DEPENDENCY_FILE_NAME,
)

logger = logging.getLogger(__name__)

PYTHON_CDK_SLUG = "python"


def _is_python_connector(metadata_data: dict[str, Any]) -> bool:
    """Check if a connector is Python-based using its metadata tags.

    Returns `True` when the metadata `tags` list includes a
    `language:python` entry.
    """
    tags: list[str] = metadata_data.get("tags", [])
    return any(tag == "language:python" for tag in tags)


def _run_docker_pip_freeze(docker_image: str) -> list[dict[str, str]]:
    """Run `pip freeze` inside the connector Docker image.

    Returns a list of `{"package_name": ..., "version": ...}` dicts,
    matching the format produced by the legacy
    `upload-python-dependencies.sh` script.

    Raises:
        RuntimeError: If the docker command fails.
    """
    cmd = [
        "docker",
        "run",
        "--rm",
        "--entrypoint",
        "pip",
        docker_image,
        "freeze",
    ]
    logger.info("Running: %s", " ".join(cmd))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"docker pip freeze failed with exit code {result.returncode}: "
            f"{result.stderr.strip()}"
        )

    dependencies: list[dict[str, str]] = []
    for line in result.stdout.strip().splitlines():
        line = line.split("#")[0].strip()
        if not line or "==" not in line:
            continue
        parts = line.split("==", 1)
        if len(parts) == 2:
            dependencies.append({"package_name": parts[0], "version": parts[1]})
    return dependencies


def _build_dependencies_json(
    connector_name: str,
    version: str,
    docker_repository: str,
    definition_id: str,
    dependencies: list[dict[str, str]],
) -> dict[str, Any]:
    """Build the `dependencies.json` payload.

    The structure matches the legacy `upload-python-dependencies.sh`
    output so that downstream consumers (e.g. the compile step's
    `packageInfo.cdk_version` extraction) work without changes.
    """
    now = datetime.now(tz=timezone.utc)
    generation_time = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
    return {
        "connector_technical_name": connector_name,
        "connector_repository": docker_repository,
        "connector_version": version,
        "connector_definition_id": definition_id,
        "dependencies": dependencies,
        "generation_time": generation_time,
    }


def generate_python_dependencies_file(
    metadata_data: dict[str, Any],
    docker_image: str,
    output_dir: Path,
) -> dict[str, Any] | None:
    """Generate `dependencies.json` for a Python connector.

    Runs `pip freeze` inside the connector's Docker image and writes
    the result to `output_dir`.  Returns the parsed dependencies dict
    (for use by `_apply_package_info_fields`) or `None` on failure.
    """
    docker_repo = metadata_data.get("dockerRepository", "")
    connector_name = docker_repo.replace("airbyte/", "")
    version = metadata_data.get("dockerImageTag", "")
    definition_id = metadata_data.get("definitionId", "")

    try:
        dependencies = _run_docker_pip_freeze(docker_image)
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        logger.warning("Could not generate dependencies.json: %s", exc)
        return None

    if not dependencies:
        logger.warning("pip freeze returned no dependencies for %s.", docker_image)
        return None

    deps_json = _build_dependencies_json(
        connector_name=connector_name,
        version=version,
        docker_repository=docker_repo,
        definition_id=definition_id,
        dependencies=dependencies,
    )

    out_path = output_dir / CONNECTOR_DEPENDENCY_FILE_NAME
    out_path.write_text(json.dumps(deps_json, indent=2) + "\n")
    logger.info("Wrote %s (%d dependencies)", out_path, len(dependencies))
    return deps_json


def extract_cdk_version_from_dependencies(
    dependencies_json: dict[str, Any],
) -> str | None:
    """Extract the `airbyte-cdk` version string from a dependencies dict.

    Returns a string like `"python:1.2.3"` or `None` if not found.
    """
    for package in dependencies_json.get("dependencies", []):
        if package.get("package_name") == "airbyte-cdk":
            pkg_ver = package.get("version")
            return f"{PYTHON_CDK_SLUG}:{pkg_ver}" if pkg_ver else None
    return None
