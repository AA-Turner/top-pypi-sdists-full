"""Unit tests for ``cli._audit_helper.get_cli_audit_writer`` (#925)."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from anteroom.cli._audit_helper import get_cli_audit_writer

# A real Ed25519 PEM (minimal valid form) is not needed — ``AuditWriter``
# only accepts a string and feeds it into HKDF. Any non-empty string
# yields a valid HMAC key for tests.
_TEST_PEM = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MC4CAQAwBQYDK2VwBCIEIKm3jiGLj2ROYfJFzxVxV0iJq0J3XOqT5PnJPBG7vLZE\n"
    "-----END PRIVATE KEY-----"
)


@dataclass
class _AppCfg:
    data_dir: Path
    host: str = "127.0.0.1"
    port: int = 8080


@dataclass
class _AuditCfg:
    enabled: bool
    log_path: str = ""
    tamper_protection: str = "hmac"
    rotation: str = "daily"
    rotate_size_bytes: int = 10_485_760
    retention_days: int = 90
    redact_content: bool = True
    events: dict[str, bool] | None = None


@dataclass
class _IdentityCfg:
    private_key: str = ""


@dataclass
class _Config:
    audit: Any
    identity: Any
    app: _AppCfg


def _make_config(
    *,
    audit_enabled: bool,
    private_key: str,
    tmp_path: Path,
) -> _Config:
    return _Config(
        audit=_AuditCfg(enabled=audit_enabled),
        identity=_IdentityCfg(private_key=private_key),
        app=_AppCfg(data_dir=tmp_path),
    )


class TestGetCliAuditWriter:
    def test_returns_none_when_audit_disabled(self, tmp_path: Path) -> None:
        cfg = _make_config(audit_enabled=False, private_key=_TEST_PEM, tmp_path=tmp_path)
        assert get_cli_audit_writer(cfg) is None

    def test_returns_none_when_no_audit_section(self, tmp_path: Path) -> None:
        cfg = _Config(audit=None, identity=_IdentityCfg(private_key=_TEST_PEM), app=_AppCfg(data_dir=tmp_path))
        assert get_cli_audit_writer(cfg) is None

    def test_returns_none_when_no_identity(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        cfg = _Config(
            audit=_AuditCfg(enabled=True),
            identity=None,
            app=_AppCfg(data_dir=tmp_path),
        )
        with caplog.at_level(logging.WARNING):
            result = get_cli_audit_writer(cfg)
        assert result is None
        assert any("no identity private key" in m for m in caplog.messages)

    def test_returns_none_when_identity_has_no_pem(
        self,
        tmp_path: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        cfg = _make_config(audit_enabled=True, private_key="", tmp_path=tmp_path)
        with caplog.at_level(logging.WARNING):
            result = get_cli_audit_writer(cfg)
        assert result is None
        assert any("no identity private key" in m for m in caplog.messages)

    def test_returns_writer_when_enabled_and_keyed(self, tmp_path: Path) -> None:
        cfg = _make_config(audit_enabled=True, private_key=_TEST_PEM, tmp_path=tmp_path)
        writer = get_cli_audit_writer(cfg)
        assert writer is not None
        assert writer.enabled is True
        # Confirm the HMAC key was derived (not None) — implies PEM was used.
        assert writer._hmac_key is not None
