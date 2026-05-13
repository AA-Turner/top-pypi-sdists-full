from __future__ import annotations

import asyncio
import base64
import hashlib
import time as time_mod


class KMSSigner:
    """Signs requests using GCP Cloud KMS asymmetric key."""

    def __init__(self, kms_key_name: str) -> None:
        from google.cloud import kms  # lazy import for optional dependency

        self._client = kms.KeyManagementServiceClient()
        self._key_name = kms_key_name

    def sign_request(self, tenant_id: str, request_id: str) -> tuple[str, str]:
        """Returns (base64_signature, unix_timestamp_str)."""
        from google.cloud.kms_v1.types import service as kms_service

        timestamp = str(int(time_mod.time()))
        canonical = f"{tenant_id}\n{timestamp}\n{request_id}"
        digest_bytes = hashlib.sha256(canonical.encode()).digest()

        response = self._client.asymmetric_sign(
            request=kms_service.AsymmetricSignRequest(
                name=self._key_name,
                digest={"sha256": digest_bytes},
            )
        )
        return base64.b64encode(response.signature).decode(), timestamp

    def close(self) -> None:
        self._client.transport.close()


class AsyncKMSSigner:
    """Async wrapper around KMSSigner using asyncio.to_thread()."""

    def __init__(self, kms_key_name: str) -> None:
        self._signer = KMSSigner(kms_key_name)

    async def sign_request(self, tenant_id: str, request_id: str) -> tuple[str, str]:
        """Returns (base64_signature, unix_timestamp_str)."""
        return await asyncio.to_thread(self._signer.sign_request, tenant_id, request_id)

    async def close(self) -> None:
        await asyncio.to_thread(self._signer.close)
