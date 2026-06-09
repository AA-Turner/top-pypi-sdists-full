# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Constants for registry operations.

These constants define the GCS folder structure and file names used by the
Airbyte connector registry.
"""

from __future__ import annotations

# GCS folder structure
METADATA_FOLDER = "metadata"
LATEST_GCS_FOLDER_NAME = "latest"
RELEASE_CANDIDATE_GCS_FOLDER_NAME = "release_candidate"

# File names
METADATA_FILE_NAME = "metadata.yaml"
SPEC_FILE_NAME = "spec.json"
ICON_FILE_NAME = "icon.svg"
DOC_FILE_NAME = "doc.md"
MANIFEST_FILE_NAME = "manifest.yaml"
COMPONENTS_PY_FILE_NAME = "components.py"
COMPONENTS_ZIP_FILE_NAME = "components.zip"
COMPONENTS_ZIP_SHA256_FILE_NAME = "components.zip.sha256"

# Dependency storage layout in GCS
CONNECTOR_DEPENDENCY_FOLDER = "connector_dependencies"
CONNECTOR_DEPENDENCY_FILE_NAME = "dependencies.json"

# SBOM (Software Bill of Materials)
SBOM_FILE_NAME = "spdx.json"
SBOM_GCS_FOLDER = "sbom"
SYFT_DOCKER_IMAGE = "anchore/syft:v1.6.0"

# CDN base URL for public registry files
METADATA_CDN_BASE_URL = "https://connectors.airbyte.com/files"

# Bucket names for metadata service (coral / Airbyte Cloud registry)
PROD_METADATA_SERVICE_BUCKET_NAME = "prod-airbyte-cloud-connector-metadata-service"
DEV_METADATA_SERVICE_BUCKET_NAME = "dev-airbyte-cloud-connector-metadata-service-2"

# Default to dev bucket for safety - use --bucket prod to target production
DEFAULT_METADATA_SERVICE_BUCKET_NAME = DEV_METADATA_SERVICE_BUCKET_NAME

# Bucket names for sonar / agent connector registry (S3)
SONAR_PROD_BUCKET_NAME = "airbyte-connector-registry"
SONAR_DEV_BUCKET_NAME = "airbyte-connector-registry-dev"

# Feature flag: allow GA versions to enable progressive rollout.
ALLOW_GA_PROGRESSIVE_ROLLOUT = True

# Registry channels supported by the Coral connector registry.
VALID_REGISTRIES = ("cloud", "oss")
