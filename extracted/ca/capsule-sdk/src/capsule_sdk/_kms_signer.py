from __future__ import annotations

from abc import ABC, abstractmethod

# Cloud platform selectors (mirror pkg/objectstore CloudGCP/CloudAWS).
CLOUD_GCP = "gcp"
CLOUD_AWS = "aws"


class Signer(ABC):
    """Signs API requests with a tenant's attestation key."""

    @abstractmethod
    def sign_request(self, tenant_id: str, request_id: str) -> tuple[str, str]:
        """Returns (base64_signature, unix_timestamp_str)."""
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class AsyncSigner(ABC):
    """Async counterpart of Signer."""

    @abstractmethod
    async def sign_request(self, tenant_id: str, request_id: str) -> tuple[str, str]:
        """Returns (base64_signature, unix_timestamp_str)."""
        pass

    @abstractmethod
    async def close(self) -> None:
        pass


def new_signer(cloud_provider: str, kms_key_name: str) -> Signer:
    """Constructs a Signer for the cloud platform (gcp or aws)."""
    if cloud_provider == CLOUD_AWS:
        raise NotImplementedError("AWS KMS signer not yet implemented")
    from capsule_sdk._gcp_kms_signer import GCPKMSSigner
    return GCPKMSSigner(kms_key_name)


def new_async_signer(cloud_provider: str, kms_key_name: str) -> AsyncSigner:
    """Constructs an AsyncSigner for the cloud platform (gcp or aws)."""
    if cloud_provider == CLOUD_AWS:
        raise NotImplementedError("AWS KMS signer not yet implemented")
    from capsule_sdk._gcp_kms_signer import AsyncGCPKMSSigner
    return AsyncGCPKMSSigner(kms_key_name)
