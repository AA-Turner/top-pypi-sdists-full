"""The aiwatch runtime must resolve host from MDM + secrets from keychain only.

It must never read or write ``~/.runlayer/config.yaml``. These tests pin the
gate in ``config.load_config`` / ``save_config`` / ``clear_config`` and the
hook-path host precedence (MDM wins over a stray developer YAML).
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from runlayer_cli import config as config_module
from runlayer_cli.config import (
    Config,
    clear_config,
    load_config,
    save_config,
    url_to_host_key,
)
from runlayer_cli.credential_store import reset_credential_store
from runlayer_cli.hook import relay
from runlayer_cli.runtime import (
    mark_aiwatch_runtime,
    reset_aiwatch_runtime,
)

GOOD_HOST = "https://good.example.com"
EVIL_HOST = "https://evil.example.com"


@pytest.fixture
def config_file(tmp_path: Path, monkeypatch) -> Path:
    """Redirect config.get_config_path to a tmp config.yaml."""
    path = tmp_path / "config.yaml"
    monkeypatch.setattr(config_module, "get_config_path", lambda: path)
    return path


@pytest.fixture(autouse=True)
def _reset_runtime_and_keyring():
    reset_aiwatch_runtime()
    reset_credential_store()
    yield
    reset_aiwatch_runtime()
    reset_credential_store()


def _write_yaml(path: Path, default_host: str) -> None:
    path.write_text(
        yaml.safe_dump(
            {
                "default_host": default_host,
                "hosts": {url_to_host_key(default_host): {"url": default_host}},
            }
        )
    )


def test_aiwatch_load_does_not_read_yaml(config_file: Path):
    """Marked aiwatch: load_config synthesizes from MDM host, ignores the YAML."""
    _write_yaml(config_file, EVIL_HOST)
    mark_aiwatch_runtime()

    with patch.object(
        config_module, "read_managed_config", return_value={"host": GOOD_HOST}
    ):
        cfg = load_config()

    assert cfg.default_host == GOOD_HOST
    assert url_to_host_key(GOOD_HOST) in cfg.hosts
    assert url_to_host_key(EVIL_HOST) not in cfg.hosts


def test_aiwatch_load_empty_without_mdm_host(config_file: Path):
    """No MDM host → empty Config (never falls back to the YAML)."""
    _write_yaml(config_file, EVIL_HOST)
    mark_aiwatch_runtime()

    with patch.object(config_module, "read_managed_config", return_value={}):
        cfg = load_config()

    assert cfg.default_host is None
    assert cfg.hosts == {}


def test_aiwatch_keychain_still_resolves_secret(config_file: Path):
    """The synthesized host entry keeps the keychain lookup live for the MDM host."""
    mark_aiwatch_runtime()
    host_key = url_to_host_key(GOOD_HOST)
    secret = "rl_user_keychain"

    with (
        patch.object(
            config_module, "read_managed_config", return_value={"host": GOOD_HOST}
        ),
        patch("keyring.get_keyring"),
        patch("keyring.get_password") as mock_get,
    ):
        # Probe (__probe__) returns None; the host-key lookup returns the secret.
        mock_get.side_effect = lambda service, key: secret if key == host_key else None
        cfg = load_config()
        resolved = cfg.get_secret_for_host(GOOD_HOST)

    assert resolved == secret


def test_aiwatch_hook_host_precedence_comes_from_mdm(config_file: Path):
    """Core security test: MDM host wins over a stray developer YAML default_host."""
    _write_yaml(config_file, EVIL_HOST)
    mark_aiwatch_runtime()

    managed = {"host": GOOD_HOST, "org_api_key": "rl_org_x"}
    with (
        patch.object(config_module, "read_managed_config", return_value=managed),
        patch.object(relay, "read_managed_config", return_value=managed),
    ):
        host, secret = relay._load_credentials()

    assert host == GOOD_HOST
    assert secret == "rl_org_x"


def test_aiwatch_save_config_is_noop(config_file: Path):
    """Marked aiwatch: save_config writes nothing and reports it didn't persist."""
    mark_aiwatch_runtime()
    persisted = save_config(
        Config(default_host=GOOD_HOST, hosts={"k": {"url": GOOD_HOST}})
    )
    assert not config_file.exists()
    assert persisted is False


def test_aiwatch_clear_config_is_noop(config_file: Path):
    """Marked aiwatch: clear_config does not delete the shared YAML."""
    _write_yaml(config_file, EVIL_HOST)
    mark_aiwatch_runtime()
    clear_config()
    assert config_file.exists()


def test_full_cli_load_reads_yaml(config_file: Path):
    """Not aiwatch: load_config reads the file exactly as before."""
    _write_yaml(config_file, EVIL_HOST)
    # runtime not marked → full CLI path
    cfg = load_config()
    assert cfg.default_host == EVIL_HOST


def test_full_cli_save_writes_yaml(config_file: Path):
    """Not aiwatch: save_config persists to the file and reports True."""
    persisted = save_config(
        Config(
            default_host=GOOD_HOST,
            hosts={url_to_host_key(GOOD_HOST): {"url": GOOD_HOST}},
        )
    )
    assert config_file.exists()
    data = yaml.safe_load(config_file.read_text())
    assert data["default_host"] == GOOD_HOST
    assert persisted is True
