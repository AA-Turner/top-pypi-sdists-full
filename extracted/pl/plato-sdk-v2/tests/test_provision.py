"""Tests for the shared VM provisioning module."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from plato.cli.chronos.provision import ProvisionResult, SyncTarget, provision_vm


def _make_mock_session():
    """Create a mock Session with one env."""
    env = MagicMock()
    env.job_id = "test-job-123"
    env.execute = AsyncMock()

    session = MagicMock()
    session.envs = [env]
    session.add_ssh_key = AsyncMock(return_value=MagicMock(success=True))
    return session, env


@pytest.mark.asyncio
async def test_provision_vm_basic():
    """provision_vm generates SSH key, adds it, probes gateway, and returns result."""
    session, env = _make_mock_session()

    with (
        patch("plato.cli.chronos.provision.SSHKeyPair") as mock_keypair_cls,
        patch("plato.cli.chronos.provision.wait_for_ssh_reachable", new_callable=AsyncMock, return_value=True),
        patch("plato.cli.chronos.provision.SyncManager"),
    ):
        mock_keypair = MagicMock()
        mock_keypair.public_key = "ssh-ed25519 AAAA..."
        mock_keypair.private_key_path = Path("/tmp/fake_key")
        mock_keypair_cls.generate.return_value = mock_keypair

        result = await provision_vm(session=session)

        assert isinstance(result, ProvisionResult)
        assert result.session is session
        assert result.env is env
        assert result.ssh_key is mock_keypair
        session.add_ssh_key.assert_awaited_once_with("ssh-ed25519 AAAA...")


@pytest.mark.asyncio
async def test_provision_vm_copy_ssh_key():
    """When copy_ssh_key_to_vm=True, the key is written to /root/.ssh/agent_key."""
    session, env = _make_mock_session()

    with (
        patch("plato.cli.chronos.provision.SSHKeyPair") as mock_keypair_cls,
        patch("plato.cli.chronos.provision.wait_for_ssh_reachable", new_callable=AsyncMock, return_value=True),
        patch("plato.cli.chronos.provision.SyncManager"),
    ):
        mock_keypair = MagicMock()
        mock_keypair.public_key = "ssh-ed25519 AAAA..."
        mock_keypair.private_key_path = MagicMock()
        mock_keypair.private_key_path.read_text.return_value = "PRIVATE_KEY_DATA"
        mock_keypair_cls.generate.return_value = mock_keypair

        await provision_vm(session=session, copy_ssh_key_to_vm=True)

        env.execute.assert_awaited()
        call_args = env.execute.call_args_list[0][0][0]
        assert "agent_key" in call_args
        assert "PRIVATE_KEY_DATA" in call_args


@pytest.mark.asyncio
async def test_provision_vm_ssh_key_failure():
    """Raises RuntimeError when SSH key setup fails."""
    session, env = _make_mock_session()
    session.add_ssh_key = AsyncMock(return_value=MagicMock(success=False))

    with (
        patch("plato.cli.chronos.provision.SSHKeyPair") as mock_keypair_cls,
        patch("plato.cli.chronos.provision.wait_for_ssh_reachable", new_callable=AsyncMock),
    ):
        mock_keypair = MagicMock()
        mock_keypair.public_key = "ssh-ed25519 AAAA..."
        mock_keypair_cls.generate.return_value = mock_keypair

        with pytest.raises(RuntimeError, match="SSH key setup failed"):
            await provision_vm(session=session)


@pytest.mark.asyncio
async def test_provision_vm_ssh_gateway_unreachable():
    """Raises RuntimeError when SSH gateway is not reachable."""
    session, env = _make_mock_session()

    with (
        patch("plato.cli.chronos.provision.SSHKeyPair") as mock_keypair_cls,
        patch("plato.cli.chronos.provision.wait_for_ssh_reachable", new_callable=AsyncMock, return_value=False),
    ):
        mock_keypair = MagicMock()
        mock_keypair.public_key = "ssh-ed25519 AAAA..."
        mock_keypair.private_key_path = Path("/tmp/fake_key")
        mock_keypair_cls.generate.return_value = mock_keypair

        with pytest.raises(RuntimeError, match="SSH gateway not reachable"):
            await provision_vm(session=session)


@pytest.mark.asyncio
async def test_provision_vm_with_sync_targets(tmp_path):
    """Sync targets are added and initial_sync is called."""
    session, env = _make_mock_session()
    local_dir = tmp_path / "mycode"
    local_dir.mkdir()

    with (
        patch("plato.cli.chronos.provision.SSHKeyPair") as mock_keypair_cls,
        patch("plato.cli.chronos.provision.wait_for_ssh_reachable", new_callable=AsyncMock, return_value=True),
        patch("plato.cli.chronos.provision.SyncManager") as mock_sync_cls,
    ):
        mock_keypair = MagicMock()
        mock_keypair.public_key = "ssh-ed25519 AAAA..."
        mock_keypair.private_key_path = Path("/tmp/fake_key")
        mock_keypair_cls.generate.return_value = mock_keypair

        mock_sync = MagicMock()
        mock_sync.targets = [MagicMock()]
        mock_sync.initial_sync = AsyncMock(return_value=1)
        mock_sync_cls.return_value = mock_sync

        targets = [SyncTarget(local_path=local_dir, remote_path="/app")]
        result = await provision_vm(session=session, sync_targets=targets)

        mock_sync.add_target.assert_called_once()
        mock_sync.initial_sync.assert_awaited_once()
        assert result.sync_manager is mock_sync


@pytest.mark.asyncio
async def test_provision_vm_sync_failure(tmp_path):
    """Raises RuntimeError when sync fails."""
    session, env = _make_mock_session()
    local_dir = tmp_path / "mycode"
    local_dir.mkdir()

    with (
        patch("plato.cli.chronos.provision.SSHKeyPair") as mock_keypair_cls,
        patch("plato.cli.chronos.provision.wait_for_ssh_reachable", new_callable=AsyncMock, return_value=True),
        patch("plato.cli.chronos.provision.SyncManager") as mock_sync_cls,
    ):
        mock_keypair = MagicMock()
        mock_keypair.public_key = "ssh-ed25519 AAAA..."
        mock_keypair.private_key_path = Path("/tmp/fake_key")
        mock_keypair_cls.generate.return_value = mock_keypair

        mock_sync = MagicMock()
        mock_sync.targets = [MagicMock(), MagicMock()]
        mock_sync.initial_sync = AsyncMock(return_value=1)  # 1 of 2 succeeded
        mock_sync_cls.return_value = mock_sync

        targets = [
            SyncTarget(local_path=local_dir, remote_path="/app"),
            SyncTarget(local_path=local_dir, remote_path="/sdk"),
        ]

        with pytest.raises(RuntimeError, match="Sync failed for 1 target"):
            await provision_vm(session=session, sync_targets=targets)
