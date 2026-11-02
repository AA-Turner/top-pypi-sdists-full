"""Generate Apollo manifest.yml — replaces apollo-cli for manifest generation.

Apollo expects a manifest.yml with product metadata for publishing Helm charts
as Apollo entities. This module generates that YAML without the apollo-cli binary.
"""

from __future__ import annotations


def generate_manifest(
    chart_name: str,
    version: str,
    group_id: str,
    oci_url: str,
    docker_image_uri: str | None = None,
) -> str:
    """Generate an Apollo-compatible manifest.yml string.

    Args:
        chart_name: Helm chart name (e.g. "mosquitto")
        version: Chart version (e.g. "1.2.3")
        group_id: Maven group ID (e.g. "com.edgescaleai-cube")
        oci_url: OCI registry URL for the chart, of the form
            ``oci://<registry>/charts/<group>/<chart>`` (no tag).
        docker_image_uri: Optional fully-qualified Docker image URI such as
            ``<registry>/<group>/<chart>:<version>``. When provided, an
            additional ``oci`` artifact entry is emitted for the image.

    Returns:
        YAML string for the manifest.

    Notes:
        Apollo's manifest schema requires ``extensions.artifacts`` — a list of
        OCI artifact references that the Apollo entity installer resolves when
        deploying a release. Without it, downstream operations fail with
        ``manifest missing 'extensions.artifacts' field``.
    """
    # Apollo artifact URIs do NOT use the "oci://" scheme prefix and DO include
    # the version tag. ``helm-repository-url`` is the inverse: it keeps the
    # scheme prefix and omits the tag.
    chart_artifact_uri = f"{oci_url.removeprefix('oci://')}:{version}"

    artifact_lines = [f'    - type: oci\n      uri: "{chart_artifact_uri}"']
    if docker_image_uri:
        artifact_lines.append(f'    - type: oci\n      uri: "{docker_image_uri}"')
    artifacts_block = "\n".join(artifact_lines)

    return f"""manifest-version: "1.0"
product-type: helm-chart.v1
product-group: "{group_id}"
product-name: "{chart_name}"
product-version: "{version}"
extensions:
  artifacts:
{artifacts_block}
  helm-chart:
    helm-chart-name: "{chart_name}"
    helm-chart-version: "{version}"
    helm-repository-url: "{oci_url}"
"""
