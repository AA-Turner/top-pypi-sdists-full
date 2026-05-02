from __future__ import annotations

import os
import uuid
from contextlib import suppress

import pytest

from capsule_sdk import CapsuleAuthError, CapsuleClient, CapsuleHTTPError, CapsuleNotFound


@pytest.fixture
def base_url() -> str:
    return os.environ.get("CAPSULE_CONTROL_PLANE_ADDR", "http://localhost:8080").rstrip("/")


@pytest.fixture
def kms_key_name() -> str:
    return os.environ.get("CAPSULE_KMS_KEY_NAME", "")


@pytest.fixture
def tenant_id() -> str:
    return os.environ.get("CAPSULE_TENANT_ID", "test-tenant")


@pytest.fixture
def client(base_url: str, kms_key_name: str, tenant_id: str) -> CapsuleClient:
    with CapsuleClient(control_plane_addr=base_url, kms_key_name=kms_key_name or None, tenant_id=tenant_id) as bf:
        yield bf


@pytest.fixture
def unauthenticated_client(base_url: str, tenant_id: str) -> CapsuleClient:
    invalid_key = (
        "projects/invalid/locations/global/keyRings/capsule/cryptoKeys/capsule-attestation/cryptoKeyVersions/1"
    )
    with CapsuleClient(
        control_plane_addr=base_url,
        kms_key_name=invalid_key,
        tenant_id=tenant_id,
    ) as bf:
        yield bf


def _layered_config_body(name: str) -> dict[str, object]:
    return {
        "display_name": name,
        "base_image": "ubuntu:22.04",
        "layers": [
            {
                "name": "workspace",
                "init_commands": [
                    {
                        "type": "shell",
                        "args": ["bash", "-lc", f"echo {name} > /workspace/{name}.txt"],
                    }
                ],
            }
        ],
        "config": {
            "tier": "m",
            "auto_rollout": False,
        },
    }


@pytest.mark.contract
class TestContract:
    def test_auth_required(self, unauthenticated_client: CapsuleClient) -> None:
        with pytest.raises(CapsuleAuthError):
            unauthenticated_client.runners.list()

    def test_auth_works(self, client: CapsuleClient) -> None:
        runners = client.runners.list()
        assert isinstance(runners, list)

    def test_layered_config_crud(self, client: CapsuleClient) -> None:
        name = f"contract-{uuid.uuid4().hex[:8]}"
        created = client.workloads.onboard(_layered_config_body(name), build=False)

        config_id = created.config_id
        assert config_id
        assert created.workload_key

        try:
            listed_ids = {cfg.config_id for cfg in client.workloads.list() if cfg.config_id}
            assert config_id in listed_ids

            detail = client.workloads.get(name)
            assert detail.config_id == config_id
            assert detail.display_name == name
        finally:
            with suppress(Exception):
                client.workloads.delete(name)

        with pytest.raises(CapsuleNotFound):
            client.workloads.get(name)

    def test_invalid_layered_config_returns_http_400(self, client: CapsuleClient) -> None:
        with pytest.raises(CapsuleHTTPError) as exc:
            client.workloads.onboard(
                {"display_name": "invalid", "layers": [{"name": "", "init_commands": []}]},
                build=False,
            )

        assert exc.value.status_code == 400
        assert "layer name must not be empty" in exc.value.message
