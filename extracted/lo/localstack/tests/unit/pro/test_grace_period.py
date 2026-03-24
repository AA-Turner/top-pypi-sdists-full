"""
Tests for the grace period / LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT feature.

Temporary — this entire file should be removed when the grace period expires.
"""

from unittest.mock import MagicMock

import pytest
from localstack_cli.pro.core import config as pro_config
from localstack_cli.pro.core.bootstrap.licensingv2 import LicensingError
from localstack_cli.pro.core.plugins import (
    GRACE_PERIOD_EXPIRED_MESSAGE,
    LICENSE_ERROR_MESSAGE,
    activate_pro_key_on_host,
)
from localstack_cli.runtime.exceptions import LocalstackExit


def _patch_licensing_failure(monkeypatch):
    """Set up a mock licensed environment that fails activation."""
    mock_env = MagicMock()
    mock_env.activate.side_effect = LicensingError("no credentials")

    import localstack_cli.pro.core.plugins as plugins_module

    monkeypatch.setattr(plugins_module.licensingv2, "get_licensed_environment", lambda: mock_env)
    monkeypatch.setattr(plugins_module.licensingv2, "LicensingError", LicensingError)


def test_no_ack_grace_active_exits_with_license_message(monkeypatch):
    """No LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT + grace active should exit with license error message."""
    import localstack_cli.pro.core.plugins as plugins_module

    _patch_licensing_failure(monkeypatch)
    monkeypatch.delenv("LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT", raising=False)
    monkeypatch.delenv("ACKNOWLEDGE_ACCOUNT_REQUIREMENT", raising=False)
    monkeypatch.setattr(plugins_module, "_check_grace_period_active", lambda ack: True)

    with pytest.raises(LocalstackExit) as exc_info:
        activate_pro_key_on_host()

    assert "LocalStack requires an account to run" in str(exc_info.value)
    assert "LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1" in str(exc_info.value)


def test_no_ack_grace_inactive_exits_with_licensing_error(monkeypatch):
    """No LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT + grace inactive should exit with LicensingError message."""
    import localstack_cli.pro.core.plugins as plugins_module

    _patch_licensing_failure(monkeypatch)
    monkeypatch.delenv("LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT", raising=False)
    monkeypatch.delenv("ACKNOWLEDGE_ACCOUNT_REQUIREMENT", raising=False)
    monkeypatch.setattr(plugins_module, "_check_grace_period_active", lambda ack: False)

    with pytest.raises(LocalstackExit) as exc_info:
        activate_pro_key_on_host()

    assert "no credentials" in str(exc_info.value)


ACK_ENV_VARS = [
    "LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT",
    "ACKNOWLEDGE_ACCOUNT_REQUIREMENT",
]


@pytest.mark.parametrize("ack_env_var", ACK_ENV_VARS)
def test_ack_with_grace_active_starts_community(monkeypatch, ack_env_var):
    """ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1 + grace period active should run in community mode."""
    import localstack_cli.pro.core.plugins as plugins_module

    _patch_licensing_failure(monkeypatch)
    for var in ACK_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv(ack_env_var, "1")
    monkeypatch.setattr(plugins_module, "_check_grace_period_active", lambda ack: True)
    monkeypatch.setattr(pro_config, "ACTIVATE_PRO", True)

    activate_pro_key_on_host()

    assert pro_config.ACTIVATE_PRO is False


@pytest.mark.parametrize("ack_env_var", ACK_ENV_VARS)
def test_ack_with_grace_expired_exits(monkeypatch, ack_env_var):
    """ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1 + grace period expired/404 should exit with licensing error."""
    import localstack_cli.pro.core.plugins as plugins_module

    _patch_licensing_failure(monkeypatch)
    for var in ACK_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv(ack_env_var, "1")
    monkeypatch.setattr(plugins_module, "_check_grace_period_active", lambda ack: False)
    monkeypatch.setattr(pro_config, "ACTIVATE_PRO", True)

    with pytest.raises(LocalstackExit) as exc_info:
        activate_pro_key_on_host()

    assert GRACE_PERIOD_EXPIRED_MESSAGE in str(exc_info.value)
    assert pro_config.ACTIVATE_PRO is False
