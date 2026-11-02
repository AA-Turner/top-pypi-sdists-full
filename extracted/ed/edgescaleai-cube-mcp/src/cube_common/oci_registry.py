"""Pure Python OCI registry push for Helm charts.

Pushes a .tgz chart to an OCI-compliant registry (like Apollo ACR)
using only httpx — no helm CLI needed.

OCI Helm chart push protocol:
1. POST /v2/{repo}/blobs/uploads/ → get upload URL
2. PUT upload URL with chart .tgz content (blob)
3. PUT /v2/{repo}/manifests/{tag} with OCI manifest JSON
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

# OCI media types for Helm charts
HELM_CHART_CONFIG_MEDIA_TYPE = "application/vnd.cncf.helm.config.v1+json"
HELM_CHART_CONTENT_MEDIA_TYPE = "application/vnd.cncf.helm.chart.content.v1.tar+gzip"
OCI_MANIFEST_MEDIA_TYPE = "application/vnd.oci.image.manifest.v1+json"


class OCIPushError(Exception):
    """Raised when an OCI push operation fails."""


async def push_chart(
    tgz_path: str,
    registry: str,
    repository: str,
    tag: str,
    token: str,
) -> str:
    """Push a Helm chart .tgz to an OCI registry.

    Args:
        tgz_path: Path to the .tgz chart archive.
        registry: Registry hostname (e.g. "edgescaleai.palantirapollo.com").
        repository: Repository path (e.g. "charts/com.edgescaleai-cube/my-chart").
        tag: Version tag (e.g. "1.0.0").
        token: Bearer token for authentication.

    Returns:
        Manifest digest string.
    """
    tgz_data = Path(tgz_path).read_bytes()
    tgz_digest = f"sha256:{hashlib.sha256(tgz_data).hexdigest()}"
    tgz_size = len(tgz_data)

    # Empty config (Helm convention)
    config_data = b"{}"
    config_digest = f"sha256:{hashlib.sha256(config_data).hexdigest()}"
    config_size = len(config_data)

    base_url = f"https://{registry}/v2/{repository}"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(timeout=120) as http:
        # 1. Upload config blob
        await _upload_blob(http, base_url, headers, config_data, config_digest)
        logger.info("Uploaded config blob: %s", config_digest)

        # 2. Upload chart blob
        await _upload_blob(http, base_url, headers, tgz_data, tgz_digest)
        logger.info("Uploaded chart blob: %s (%d bytes)", tgz_digest, tgz_size)

        # 3. Push manifest
        manifest = {
            "schemaVersion": 2,
            "mediaType": OCI_MANIFEST_MEDIA_TYPE,
            "config": {
                "mediaType": HELM_CHART_CONFIG_MEDIA_TYPE,
                "digest": config_digest,
                "size": config_size,
            },
            "layers": [
                {
                    "mediaType": HELM_CHART_CONTENT_MEDIA_TYPE,
                    "digest": tgz_digest,
                    "size": tgz_size,
                }
            ],
        }

        manifest_data = json.dumps(manifest, separators=(",", ":")).encode()

        resp = await http.put(
            f"{base_url}/manifests/{tag}",
            content=manifest_data,
            headers={
                **headers,
                "Content-Type": OCI_MANIFEST_MEDIA_TYPE,
            },
        )
        if resp.status_code not in (200, 201):
            raise OCIPushError(f"Manifest push failed ({resp.status_code}): {resp.text[:500]}")

        manifest_digest = resp.headers.get(
            "Docker-Content-Digest",
            f"sha256:{hashlib.sha256(manifest_data).hexdigest()}",
        )
        logger.info("Pushed manifest %s:%s -> %s", repository, tag, manifest_digest)
        return manifest_digest


async def _upload_blob(
    http: httpx.AsyncClient,
    base_url: str,
    headers: dict,
    data: bytes,
    digest: str,
) -> None:
    """Upload a single blob to the OCI registry."""
    # Check if blob already exists
    head_resp = await http.head(f"{base_url}/blobs/{digest}", headers=headers)
    if head_resp.status_code == 200:
        logger.debug("Blob already exists: %s", digest)
        return

    # Initiate upload
    post_resp = await http.post(f"{base_url}/blobs/uploads/", headers=headers)
    if post_resp.status_code not in (200, 202):
        raise OCIPushError(f"Blob upload init failed ({post_resp.status_code}): {post_resp.text[:500]}")

    upload_url = post_resp.headers.get("Location", "")
    if not upload_url:
        raise OCIPushError("No Location header in blob upload response")

    # Make upload URL absolute
    if upload_url.startswith("/"):
        # Extract scheme+host from base_url
        from urllib.parse import urlparse
        parsed = urlparse(base_url)
        upload_url = f"{parsed.scheme}://{parsed.netloc}{upload_url}"

    # Complete upload with data
    sep = "&" if "?" in upload_url else "?"
    put_url = f"{upload_url}{sep}digest={digest}"

    put_resp = await http.put(
        put_url,
        content=data,
        headers={
            **headers,
            "Content-Type": "application/octet-stream",
            "Content-Length": str(len(data)),
        },
    )
    if put_resp.status_code not in (200, 201):
        raise OCIPushError(f"Blob upload failed ({put_resp.status_code}): {put_resp.text[:500]}")
