from __future__ import annotations

import os

import pytest

from capsule_sdk._config import ConnectionConfig


def _kms_key_name(tenant: str) -> str:
    return f"projects/{tenant}/locations/global/keyRings/capsule/cryptoKeys/capsule-attestation/cryptoKeyVersions/1"


class TestConnectionConfig:
    def test_explicit_values(self) -> None:
        cfg = ConnectionConfig.resolve(
            control_plane_addr="http://example.com",
            kms_key_name=_kms_key_name("test-tenant"),
            tenant_id="test-tenant",
            request_timeout=10.0,
            startup_timeout=50.0,
            operation_timeout=90.0,
        )
        assert cfg.control_plane_addr == "http://example.com"
        assert cfg.kms_key_name == _kms_key_name("test-tenant")
        assert cfg.tenant_id == "test-tenant"
        assert cfg.timeout == 10.0
        assert cfg.request_timeout == 10.0
        assert cfg.startup_timeout == 50.0
        assert cfg.operation_timeout == 90.0
        assert "capsule-sdk-python" in cfg.user_agent

    def test_env_fallback(self, monkeypatch: object) -> None:
        import pytest

        mp = pytest.MonkeyPatch()
        mp.setenv("CAPSULE_CONTROL_PLANE_ADDR", "http://env-host:9090")
        mp.setenv("CAPSULE_KMS_KEY_NAME", _kms_key_name("env-tenant"))
        mp.setenv("CAPSULE_TENANT_ID", "env-tenant")
        try:
            cfg = ConnectionConfig.resolve(tenant_id="")
            assert cfg.control_plane_addr == "http://env-host:9090"
            assert cfg.kms_key_name == _kms_key_name("env-tenant")
            assert cfg.tenant_id == "env-tenant"
        finally:
            mp.undo()

    def test_kms_key_name_auto_derived(self) -> None:
        cfg = ConnectionConfig.resolve(tenant_id="my-tenant")
        assert cfg.kms_key_name == _kms_key_name("my-tenant")

    def test_cloud_provider_defaults_to_gcp(self) -> None:
        cfg = ConnectionConfig.resolve(tenant_id="my-tenant")
        assert cfg.cloud_provider == "gcp"

    def test_cloud_provider_env_fallback(self) -> None:
        mp = pytest.MonkeyPatch()
        mp.setenv("CAPSULE_CLOUD_PROVIDER", "aws")
        try:
            cfg = ConnectionConfig.resolve(tenant_id="my-tenant")
            assert cfg.cloud_provider == "aws"
        finally:
            mp.undo()

    def test_aws_has_no_default_key_name(self) -> None:
        cfg = ConnectionConfig.resolve(tenant_id="my-tenant", cloud_provider="aws")
        assert cfg.cloud_provider == "aws"
        assert cfg.kms_key_name is None

    def test_defaults(self) -> None:
        # Clear env vars if set
        env_backup = {}
        for key in ("CAPSULE_CONTROL_PLANE_ADDR", "CAPSULE_KMS_KEY_NAME", "CAPSULE_TENANT_ID"):
            if key in os.environ:
                env_backup[key] = os.environ.pop(key)
        try:
            with pytest.raises(ValueError, match="tenant_id is required"):
                ConnectionConfig.resolve(tenant_id="")
        finally:
            os.environ.update(env_backup)

    def test_trailing_slash_stripped(self) -> None:
        cfg = ConnectionConfig.resolve(control_plane_addr="http://example.com/", tenant_id="test-tenant")
        assert cfg.control_plane_addr == "http://example.com"
