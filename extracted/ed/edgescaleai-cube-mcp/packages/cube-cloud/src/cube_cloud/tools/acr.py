"""ACR token and Apollo publish tools."""

from __future__ import annotations

import logging

import yaml

from cube_common.apollo_client import ApolloClient, ApolloError
from cube_common.apollo_queries import (
    CREATE_PRODUCT,
    CREATE_PRODUCT_RELEASE_FROM_MANIFEST,
    LIST_PRODUCTS,
)

logger = logging.getLogger(__name__)


async def acr_get_token(client: ApolloClient) -> str:
    """Get a raw ACR OAuth2 token. Returns the full token for agent use."""
    token = await client.get_token()
    return token


def _extract_product_id(manifest_yaml: str) -> tuple[str, str | None]:
    """Extract product_id from a manifest, supporting multiple formats.

    Returns (product_id, error_message). error_message is None on success.

    Supported formats:
    1. V1 format: product-group + product-name top-level fields
    2. Legacy: product-id.maven-coordinate = "group:name:version"
    3. Extensions-only: extensions.helm-chart-operator.products
    """
    try:
        manifest = yaml.safe_load(manifest_yaml)
    except yaml.YAMLError as e:
        return "", f"Error: invalid YAML in manifest: {e}"

    if not isinstance(manifest, dict):
        return "", f"Error: manifest must be a YAML mapping (got {type(manifest).__name__})"

    # Format 1: v1 format with product-group and product-name
    group = manifest.get("product-group")
    name = manifest.get("product-name")
    if group and name:
        return f"{str(group).strip()}:{str(name).strip()}", None

    # Format 2: legacy product-id section
    product_id_section = manifest.get("product-id")
    if product_id_section and isinstance(product_id_section, dict):
        maven_coordinate = product_id_section.get("maven-coordinate")
        if maven_coordinate:
            coord = str(maven_coordinate).strip('"').strip("'")
            parts = coord.split(":")
            if len(parts) >= 2:
                return f"{parts[0]}:{parts[1]}", None

    # Format 3: extensions-only — try to extract from helm-chart-operator
    extensions = manifest.get("extensions", {})
    if isinstance(extensions, dict):
        hco = extensions.get("helm-chart-operator", {})
        if isinstance(hco, dict):
            products = hco.get("products", {})
            if isinstance(products, dict) and products:
                product_id = next(iter(products))
                return product_id, None

    return "", (
        "Error: cannot extract product ID from manifest. "
        "Manifest must have 'product-group' + 'product-name' fields, "
        "a 'product-id.maven-coordinate' field, "
        "or an 'extensions.helm-chart-operator.products' section."
    )


async def _all_product_ids(client: ApolloClient) -> set[str]:
    """Fetch all product IDs with pagination."""
    product_ids: set[str] = set()
    page_token: str | None = None

    while True:
        variables: dict = {"pageSize": 200}
        if page_token:
            variables["pageToken"] = page_token
        data = await client.graphql(LIST_PRODUCTS, variables)
        page_data = data.get("apollo", {}).get("products", {})
        for p in page_data.get("products", []):
            product_ids.add(p.get("productId", ""))
        page_token = page_data.get("nextPageToken")
        if not page_token:
            break

    return product_ids


def _ensure_artifacts(manifest_yaml: str) -> str:
    """Auto-populate extensions.artifacts when missing.

    Apollo's agent requires extensions.artifacts to resolve OCI URIs during
    install. If the manifest has extensions.helm-chart but no artifacts,
    derive the artifact list from the helm-chart section.
    """
    try:
        manifest = yaml.safe_load(manifest_yaml)
    except yaml.YAMLError:
        return manifest_yaml  # let downstream validation handle bad YAML

    if not isinstance(manifest, dict):
        return manifest_yaml

    extensions = manifest.get("extensions")
    if not isinstance(extensions, dict):
        return manifest_yaml

    # Already has artifacts — nothing to do
    if extensions.get("artifacts"):
        return manifest_yaml

    # Derive from helm-chart section
    helm_chart = extensions.get("helm-chart")
    if not isinstance(helm_chart, dict):
        return manifest_yaml

    repo_url = helm_chart.get("helm-repository-url", "")
    version = helm_chart.get("helm-chart-version") or manifest.get("product-version", "")
    if not repo_url or not version:
        return manifest_yaml

    # Artifact URI: strip oci:// scheme, append version tag
    artifact_uri = repo_url.removeprefix("oci://") + f":{version}"
    extensions["artifacts"] = [{"type": "oci", "uri": artifact_uri}]

    logger.info("Auto-populated extensions.artifacts from helm-chart section")
    return yaml.dump(manifest, default_flow_style=False, sort_keys=False)


async def apollo_publish_manifest(client: ApolloClient, manifest_yaml: str) -> str:
    """Publish a manifest to Apollo via GraphQL.

    1. Auto-populate extensions.artifacts if missing (required by Apollo agent).
    2. Parse the product_id (group:name) from the manifest.
    3. If the product doesn't exist yet, create it.
    4. Publish the release using the manifest YAML.

    Supports both standard manifests (with product-id section) and
    extensions-only manifests (helm-chart-operator format).
    """
    # --- ensure extensions.artifacts is present ---
    manifest_yaml = _ensure_artifacts(manifest_yaml)

    # --- extract product_id from manifest ---
    product_id, err = _extract_product_id(manifest_yaml)
    if err:
        return err

    # --- ensure product exists ---
    existing = await _all_product_ids(client)
    created = False
    if product_id not in existing:
        try:
            await client.graphql(CREATE_PRODUCT, {"productId": product_id})
            created = True
            logger.info("Created new Apollo product: %s", product_id)
        except ApolloError as e:
            return f"Error creating product '{product_id}': {e}"

    # --- publish release ---
    try:
        data = await client.graphql(
            CREATE_PRODUCT_RELEASE_FROM_MANIFEST,
            {"productReleaseManifest": manifest_yaml},
        )
    except ApolloError as e:
        return f"Error publishing manifest for '{product_id}': {e}"

    release = data.get("apollo", {}).get("createProductReleaseFromManifestV2", {})
    coordinate = release.get("mavenCoordinate", "")
    parts = coordinate.split(":")
    version = parts[2] if len(parts) >= 3 else coordinate or "?"

    if created:
        return f"Created product '{product_id}' and published release {version}."
    return f"Published release {version} for product '{product_id}'."
