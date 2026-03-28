"""Shared VM provisioning logic for chronos dev and test runners.

Both `chronos dev` and `chronos test` follow the same provisioning pattern:
SSH keys → verify gateway → rsync. This module extracts that shared flow
so both runners stay in sync.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

from plato.cli.chronos.dev.ssh import SSHKeyPair, wait_for_ssh_reachable
from plato.cli.chronos.dev.sync import SyncManager
from plato.v2.async_.environment import Environment
from plato.v2.async_.session import Session

logger = logging.getLogger(__name__)


@dataclass
class ProvisionResult:
    """Result of provisioning a VM with SSH and sync ready."""

    session: Session
    env: Environment
    ssh_key: SSHKeyPair
    sync_manager: SyncManager


@dataclass
class SyncTarget:
    """A local path to sync to a remote path on the VM."""

    local_path: Path
    remote_path: str


async def provision_vm(
    *,
    session: Session,
    copy_ssh_key_to_vm: bool = False,
    ensure_rsync: bool = False,
    sync_targets: list[SyncTarget] | None = None,
    verbose: bool = False,
) -> ProvisionResult:
    """Provision a VM with SSH keys, gateway probe, and sync targets.

    Expects the session to already have network connected (the default).

    Args:
        session: An already-created session.
        copy_ssh_key_to_vm: If True, copy the generated SSH key to the VM
            at /root/.ssh/agent_key (used for agent VM SSH).
        ensure_rsync: If True, ensure rsync is installed on the VM.
        sync_targets: List of local→remote sync targets. If None or empty,
            skip the sync step.
        verbose: Enable verbose logging for sync.

    Returns:
        ProvisionResult with all components initialized.
    """
    env = session.envs[0]
    t_total = perf_counter()

    # 1. SSH key setup
    t0 = perf_counter()
    ssh_key = SSHKeyPair.generate()
    ssh_response = await session.add_ssh_key(ssh_key.public_key)
    if not ssh_response.success:
        raise RuntimeError(f"SSH key setup failed: {ssh_response}")
    logger.info("SSH key added in %.1fs", perf_counter() - t0)

    # 2. Parallel: copy SSH key to VM + ensure rsync installed (if requested)
    parallel_tasks: list[asyncio.Task] = []

    if copy_ssh_key_to_vm:

        async def _copy_key() -> None:
            t = perf_counter()
            private_key = ssh_key.private_key_path.read_text()
            public_key = ssh_key.public_key
            escaped_private = private_key.replace("'", "'\\''")
            escaped_public = public_key.replace("'", "'\\''")
            await env.execute(
                f"mkdir -p /root/.ssh && "
                f"echo '{escaped_private}' > /root/.ssh/agent_key && chmod 600 /root/.ssh/agent_key && "
                f"echo '{escaped_public}' > /root/.ssh/agent_key.pub && chmod 644 /root/.ssh/agent_key.pub",
                timeout=30,
            )
            logger.info("SSH key copied to VM in %.1fs", perf_counter() - t)

        parallel_tasks.append(asyncio.create_task(_copy_key()))

    if ensure_rsync:

        async def _ensure_rsync() -> None:
            t = perf_counter()
            await env.execute("which rsync || apt-get update && apt-get install -y rsync", timeout=60)
            logger.info("rsync ensured in %.1fs", perf_counter() - t)

        parallel_tasks.append(asyncio.create_task(_ensure_rsync()))

    if parallel_tasks:
        await asyncio.gather(*parallel_tasks)

    # 3. Verify SSH gateway tunnel is routable before syncing
    t0 = perf_counter()
    reachable = await wait_for_ssh_reachable(env.job_id, ssh_key.private_key_path)
    if reachable:
        logger.info("SSH gateway verified in %.1fs for %s", perf_counter() - t0, env.job_id)
    else:
        raise RuntimeError(f"SSH gateway not reachable for {env.job_id} after {perf_counter() - t0:.1f}s")

    # 4. Setup sync targets and run initial sync
    sync_manager = SyncManager(ssh_key.private_key_path, verbose=verbose)
    if sync_targets:
        for target in sync_targets:
            sync_manager.add_target(
                local_path=target.local_path,
                remote_path=target.remote_path,
                job_id=env.job_id,
            )

        t0 = perf_counter()
        synced = await sync_manager.initial_sync()
        logger.info("Synced %d/%d targets in %.1fs", synced, len(sync_manager.targets), perf_counter() - t0)
        if synced != len(sync_manager.targets):
            failed = len(sync_manager.targets) - synced
            raise RuntimeError(f"Sync failed for {failed} target(s)")

    logger.info("VM provisioning complete in %.1fs (job_id=%s)", perf_counter() - t_total, env.job_id)

    return ProvisionResult(
        session=session,
        env=env,
        ssh_key=ssh_key,
        sync_manager=sync_manager,
    )
