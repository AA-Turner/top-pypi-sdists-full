from __future__ import annotations

import os
from dataclasses import dataclass

from capsule_sdk._kms_signer import CLOUD_AWS, CLOUD_GCP
from capsule_sdk._version import __version__


def _default_kms_key_name(cloud_provider: str, tenant_id: str) -> str | None:
    """Derives the default attestation key name for a tenant.

    GCP: the Cloud KMS resource path. AWS: no safe default (the key ARN/alias
    depends on account and region), so it must be provided explicitly.
    """
    if cloud_provider == CLOUD_AWS:
        return None
    return (
        f"projects/{tenant_id}/locations/global/keyRings/capsule"
        f"/cryptoKeys/capsule-attestation/cryptoKeyVersions/1"
    )


@dataclass(frozen=True)
class ConnectionConfig:
    """Resolved connection configuration."""

    control_plane_addr: str
    kms_key_name: str | None
    cloud_provider: str
    tenant_id: str
    api_proxy_addr: str
    request_timeout: float
    startup_timeout: float
    operation_timeout: float
    user_agent: str

    @property
    def timeout(self) -> float:
        """Backward-compatible alias for the request timeout."""
        return self.request_timeout

    @classmethod
    def resolve(
        cls,
        *,
        control_plane_addr: str | None = None,
        kms_key_name: str | None = None,
        cloud_provider: str | None = None,
        tenant_id: str,
        api_proxy_addr: str | None = None,
        timeout: float = 30.0,
        request_timeout: float | None = None,
        startup_timeout: float | None = None,
        operation_timeout: float | None = None,
    ) -> ConnectionConfig:
        resolved_control_plane_addr = (
            control_plane_addr or os.environ.get("CAPSULE_CONTROL_PLANE_ADDR") or "http://localhost:8080"
        ).rstrip("/")

        resolved_tenant_id = tenant_id or os.environ.get("CAPSULE_TENANT_ID", "")
        if not resolved_tenant_id:
            raise ValueError("tenant_id is required. Pass it directly or set CAPSULE_TENANT_ID.")

        resolved_cloud_provider = cloud_provider or os.environ.get("CAPSULE_CLOUD_PROVIDER") or CLOUD_GCP

        resolved_kms_key_name = kms_key_name or os.environ.get("CAPSULE_KMS_KEY_NAME")
        if not resolved_kms_key_name:
            resolved_kms_key_name = _default_kms_key_name(resolved_cloud_provider, resolved_tenant_id)

        resolved_api_proxy_addr = (api_proxy_addr or os.environ.get("CAPSULE_API_PROXY_ADDR", "")).rstrip("/")
        resolved_request_timeout = (
            request_timeout
            if request_timeout is not None
            else float(os.environ.get("CAPSULE_REQUEST_TIMEOUT", timeout))
        )
        resolved_startup_timeout = (
            startup_timeout if startup_timeout is not None else float(os.environ.get("CAPSULE_STARTUP_TIMEOUT", 45.0))
        )
        resolved_operation_timeout = (
            operation_timeout
            if operation_timeout is not None
            else float(os.environ.get("CAPSULE_OPERATION_TIMEOUT", 120.0))
        )

        return cls(
            control_plane_addr=resolved_control_plane_addr,
            kms_key_name=resolved_kms_key_name,
            cloud_provider=resolved_cloud_provider,
            tenant_id=resolved_tenant_id,
            api_proxy_addr=resolved_api_proxy_addr,
            request_timeout=resolved_request_timeout,
            startup_timeout=resolved_startup_timeout,
            operation_timeout=resolved_operation_timeout,
            user_agent=f"capsule-sdk-python/{__version__}",
        )
