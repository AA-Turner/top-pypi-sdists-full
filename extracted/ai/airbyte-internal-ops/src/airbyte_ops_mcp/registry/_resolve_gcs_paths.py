# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Centralised GCS path resolution for all registry artifacts.

**Security-auditable module**: every GCS blob path and full `gs://` URI
used by the generate and publish pipelines is built here.  Reviewing this
single file is sufficient to verify that development stages never write to
production buckets.

## Stage isolation

Functions that resolve *write* destinations (`versioned_gcs_uri`,
`dependencies_gcs_uri`, `sbom_gcs_uri`) accept a
`RegistryStore` which encodes the stage (`dev` / `prod`), the
concrete bucket name, and an optional path prefix.  The bucket is
derived deterministically from the stage:

- `coral:prod`           -> `gs://prod-airbyte-cloud-connector-metadata-service/...`
- `coral:dev`            -> `gs://dev-airbyte-cloud-connector-metadata-service-2/...`
- `coral:dev/my-prefix`  -> `gs://dev-airbyte-cloud-connector-metadata-service-2/my-prefix/...`

There is **no code path** that allows a `dev` stage to resolve to a
`prod` bucket or vice-versa; the mapping is defined in
`store.BUCKET_MAP` and enforced by `RegistryStore.bucket`.

## Connector identity

All functions use `connector_name` (e.g. `"source-faker"`) and
`version` (e.g. `"7.0.1"`) -- never raw Docker image references.
The Docker image owner (`airbyte`) is a module-level constant
(`DOCKER_IMAGE_OWNER`) embedded automatically in every path.

## Path layout

**Versioned metadata** (all artifacts for one connector version):

    gs://<bucket>/[<prefix>/]metadata/airbyte/<connector>/<version>/

**Dependencies dual-load** (pip-freeze output for Python connectors):

    gs://<bucket>/[<prefix>/]connector_dependencies/<connector>/<version>/dependencies.json

**SBOM dual-load** (Syft SPDX output):

    gs://<bucket>/[<prefix>/]sbom/airbyte/<connector>/<version>.spdx.json

**Production CDN URLs** (read-only annotations, never used for writes):

    https://connectors.airbyte.com/files/sbom/airbyte/<connector>/<version>.spdx.json
    https://connectors.airbyte.com/files/metadata/airbyte/<connector>/latest/icon.svg
"""

from __future__ import annotations

from airbyte_ops_mcp.registry._constants import (
    CONNECTOR_DEPENDENCY_FILE_NAME,
    CONNECTOR_DEPENDENCY_FOLDER,
    METADATA_CDN_BASE_URL,
    METADATA_FILE_NAME,
    METADATA_FOLDER,
    SBOM_FILE_NAME,
    SBOM_GCS_FOLDER,
)
from airbyte_ops_mcp.registry.store import RegistryStore

# The Docker image owner / namespace.  All Airbyte connectors live under
# this prefix (e.g. `airbyte/source-faker`).
DOCKER_IMAGE_OWNER = "airbyte"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _prefix_part(prefix: str) -> str:
    """Return `<prefix>/` when *prefix* is non-empty, else `""`."""
    return f"{prefix}/" if prefix else ""


# ---------------------------------------------------------------------------
# Blob-path helpers (relative to bucket root)
# ---------------------------------------------------------------------------
# These return the *blob path* only (no `gs://` scheme or bucket name).
# They are used internally by the full-URI resolvers below and may also
# be useful when the caller already has a bucket reference (e.g. via
# `gcsfs.GCSFileSystem`).


def versioned_blob_root(
    *,
    connector_name: str,
    version: str,
    store: RegistryStore | None = None,
) -> str:
    """Return the GCS blob-path root for a versioned artifact set.

    When *store* is provided, its prefix is prepended to the blob path.

    Examples:
        >>> versioned_blob_root(connector_name="source-faker", version="7.0.1")
        'metadata/airbyte/source-faker/7.0.1'
        >>> from airbyte_ops_mcp.registry.store import RegistryStore
        >>> versioned_blob_root(
        ...     connector_name="source-faker",
        ...     version="7.0.1",
        ...     store=RegistryStore.parse("coral:dev/my-test"),
        ... )
        'my-test/metadata/airbyte/source-faker/7.0.1'
    """
    prefix = store.prefix if store else ""
    return (
        f"{_prefix_part(prefix)}"
        f"{METADATA_FOLDER}/{DOCKER_IMAGE_OWNER}/{connector_name}/{version}"
    )


def dependencies_blob_path(
    *,
    connector_name: str,
    version: str,
    store: RegistryStore | None = None,
) -> str:
    """Return the GCS blob path for the dual-loaded `dependencies.json`.

    When *store* is provided, its prefix is prepended to the blob path.

    Examples:
        >>> dependencies_blob_path(connector_name="source-faker", version="7.0.1")
        'connector_dependencies/source-faker/7.0.1/dependencies.json'
        >>> from airbyte_ops_mcp.registry.store import RegistryStore
        >>> dependencies_blob_path(
        ...     connector_name="source-faker",
        ...     version="7.0.1",
        ...     store=RegistryStore.parse("coral:dev/my-test"),
        ... )
        'my-test/connector_dependencies/source-faker/7.0.1/dependencies.json'
    """
    prefix = store.prefix if store else ""
    return (
        f"{_prefix_part(prefix)}"
        f"{CONNECTOR_DEPENDENCY_FOLDER}"
        f"/{connector_name}/{version}/{CONNECTOR_DEPENDENCY_FILE_NAME}"
    )


def sbom_blob_path(
    *,
    connector_name: str,
    version: str,
    store: RegistryStore | None = None,
) -> str:
    """Return the GCS blob path for the dual-loaded SBOM file.

    When *store* is provided, its prefix is prepended to the blob path.

    Examples:
        >>> sbom_blob_path(connector_name="source-faker", version="7.0.1")
        'sbom/airbyte/source-faker/7.0.1.spdx.json'
        >>> from airbyte_ops_mcp.registry.store import RegistryStore
        >>> sbom_blob_path(
        ...     connector_name="source-faker",
        ...     version="7.0.1",
        ...     store=RegistryStore.parse("coral:dev/my-test"),
        ... )
        'my-test/sbom/airbyte/source-faker/7.0.1.spdx.json'
    """
    prefix = store.prefix if store else ""
    return (
        f"{_prefix_part(prefix)}"
        f"{SBOM_GCS_FOLDER}/{DOCKER_IMAGE_OWNER}/{connector_name}"
        f"/{version}.{SBOM_FILE_NAME}"
    )


def versioned_file_blob_path(
    *,
    connector_name: str,
    version: str,
    file_name: str = METADATA_FILE_NAME,
) -> str:
    """Return the blob path for a file inside a versioned artifact directory.

    This is always unprefixed -- it describes the *canonical* production
    location regardless of where the artifact was actually uploaded.

    Args:
        connector_name: Connector name without owner prefix
            (e.g. `source-faker`).
        version: Connector version / Docker image tag (e.g. `7.0.1`).
        file_name: Name of the file within the version directory.
            Defaults to `metadata.yaml`.

    Examples:
        >>> versioned_file_blob_path(connector_name="source-faker", version="7.0.1")
        'metadata/airbyte/source-faker/7.0.1/metadata.yaml'
        >>> versioned_file_blob_path(
        ...     connector_name="source-faker", version="7.0.1", file_name="spec.json"
        ... )
        'metadata/airbyte/source-faker/7.0.1/spec.json'
    """
    return (
        f"{METADATA_FOLDER}/{DOCKER_IMAGE_OWNER}/{connector_name}/{version}/{file_name}"
    )


# ---------------------------------------------------------------------------
# Full GCS URI resolvers (stage-aware)
# ---------------------------------------------------------------------------
# These accept a `RegistryStore` and return a complete `gs://` URI.
# The bucket is derived from the stage encoded in the store, so
# `coral:dev` **always** maps to the dev bucket and `coral:prod`
# **always** maps to the prod bucket.  There is no way to accidentally
# cross stages.


def versioned_gcs_uri(
    *,
    connector_name: str,
    version: str,
    store: RegistryStore,
) -> str:
    """Return the full `gs://` URI for a versioned artifact set.

    The bucket is determined by the *store* stage (dev vs. prod).
    The prefix (if any) from the store is prepended to the blob path.

    Examples:
        >>> from airbyte_ops_mcp.registry.store import RegistryStore
        >>> versioned_gcs_uri(
        ...     connector_name="source-faker",
        ...     version="7.0.1",
        ...     store=RegistryStore.parse("coral:prod"),
        ... )
        'gs://prod-airbyte-cloud-connector-metadata-service/metadata/airbyte/source-faker/7.0.1'
        >>> versioned_gcs_uri(
        ...     connector_name="source-faker",
        ...     version="7.0.1",
        ...     store=RegistryStore.parse("coral:dev/my-test"),
        ... )
        'gs://dev-airbyte-cloud-connector-metadata-service-2/my-test/metadata/airbyte/source-faker/7.0.1'
    """
    blob = versioned_blob_root(
        connector_name=connector_name, version=version, store=store
    )
    return f"gs://{store.bucket}/{blob}"


def dependencies_gcs_uri(
    *,
    connector_name: str,
    version: str,
    store: RegistryStore,
) -> str:
    """Return the full `gs://` URI for the dual-loaded `dependencies.json`.

    Examples:
        >>> from airbyte_ops_mcp.registry.store import RegistryStore
        >>> dependencies_gcs_uri(
        ...     connector_name="source-faker",
        ...     version="7.0.1",
        ...     store=RegistryStore.parse("coral:prod"),
        ... )
        'gs://prod-airbyte-cloud-connector-metadata-service/connector_dependencies/source-faker/7.0.1/dependencies.json'
        >>> dependencies_gcs_uri(
        ...     connector_name="source-faker",
        ...     version="7.0.1",
        ...     store=RegistryStore.parse("coral:dev/my-test"),
        ... )
        'gs://dev-airbyte-cloud-connector-metadata-service-2/my-test/connector_dependencies/source-faker/7.0.1/dependencies.json'
    """
    blob = dependencies_blob_path(
        connector_name=connector_name, version=version, store=store
    )
    return f"gs://{store.bucket}/{blob}"


def sbom_gcs_uri(
    *,
    connector_name: str,
    version: str,
    store: RegistryStore,
) -> str:
    """Return the full `gs://` URI for the dual-loaded SBOM file.

    Examples:
        >>> from airbyte_ops_mcp.registry.store import RegistryStore
        >>> sbom_gcs_uri(
        ...     connector_name="source-faker",
        ...     version="7.0.1",
        ...     store=RegistryStore.parse("coral:prod"),
        ... )
        'gs://prod-airbyte-cloud-connector-metadata-service/sbom/airbyte/source-faker/7.0.1.spdx.json'
        >>> sbom_gcs_uri(
        ...     connector_name="source-faker",
        ...     version="7.0.1",
        ...     store=RegistryStore.parse("coral:dev/my-test"),
        ... )
        'gs://dev-airbyte-cloud-connector-metadata-service-2/my-test/sbom/airbyte/source-faker/7.0.1.spdx.json'
    """
    blob = sbom_blob_path(connector_name=connector_name, version=version, store=store)
    return f"gs://{store.bucket}/{blob}"


# ---------------------------------------------------------------------------
# Production CDN URLs (read-only annotations)
# ---------------------------------------------------------------------------
# These resolve *public* URLs on the production CDN.  They are used
# exclusively as *read-only annotations* embedded inside generated
# metadata (e.g. `iconUrl`, `sbomUrl`).  They are **never** used
# as write destinations.  There is no dev equivalent -- the CDN always
# serves from the production bucket.


def prod_icon_cdn_url(*, connector_name: str) -> str:
    """Return the **production** CDN URL for a connector's icon.

    This URL is embedded as a read-only annotation in registry metadata
    (`iconUrl` field).  It always points to the production CDN and is
    **never** used as a write destination.

    Example:
        >>> prod_icon_cdn_url(connector_name="source-faker")
        'https://connectors.airbyte.com/files/metadata/airbyte/source-faker/latest/icon.svg'
    """
    return (
        f"{METADATA_CDN_BASE_URL}/{METADATA_FOLDER}"
        f"/{DOCKER_IMAGE_OWNER}/{connector_name}/latest/icon.svg"
    )


def prod_sbom_cdn_url(*, connector_name: str, version: str) -> str:
    """Return the **production** CDN URL for a connector's SBOM.

    This URL is embedded as a read-only annotation in registry metadata
    (`sbomUrl` field).  It always points to the production CDN and is
    **never** used as a write destination.

    Example:
        >>> prod_sbom_cdn_url(connector_name="source-faker", version="7.0.1")
        'https://connectors.airbyte.com/files/sbom/airbyte/source-faker/7.0.1.spdx.json'
    """
    return (
        f"{METADATA_CDN_BASE_URL}/{SBOM_GCS_FOLDER}"
        f"/{DOCKER_IMAGE_OWNER}/{connector_name}"
        f"/{version}.{SBOM_FILE_NAME}"
    )
