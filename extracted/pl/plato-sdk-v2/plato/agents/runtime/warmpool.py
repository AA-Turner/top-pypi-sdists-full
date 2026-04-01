"""Warm pooling for reusable agent VMs."""

from __future__ import annotations

import asyncio
import json
import logging
import shlex
import time
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import tenacity

from plato.agents.runtime.base import AgentContext
from plato.agents.runtime.vm import (
    _VM_SSH_EXTRA_OPTS,
    VMConfig,
    _make_agent_alias,
    install_agent_code_on_vm,
    resolve_runner_path,
)
from plato.utils.subprocess import run_ssh
from plato.v2 import Env
from plato.v2.types import SimConfigCompute

if TYPE_CHECKING:
    from plato.v2.async_.environment import Environment

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class PooledVM:
    """A reusable agent VM managed by :class:`WarmPool`."""

    agent_env: Environment
    mesh_ip: str
    alias: str
    image: str
    runner_path: str
    created_at: float
    last_used_at: float
    use_count: int
    healthy: bool = True


class WarmPool:
    """Manage a reusable pool of pre-provisioned agent VMs."""

    def __init__(
        self,
        session,
        ssh_key_path: Path | None,
        vm_config: VMConfig,
        prototype_ctx: AgentContext,
        *,
        max_size: int = 4,
        pre_warm: int = 0,
        health_check_timeout: int = 10,
        reset_timeout: int = 30,
    ) -> None:
        if max_size < 1:
            raise ValueError("max_size must be at least 1")
        if pre_warm < 0:
            raise ValueError("pre_warm must be non-negative")

        self.session = session
        self.ssh_key_path = ssh_key_path
        self.vm_config = vm_config
        self.prototype_ctx = prototype_ctx
        self.max_size = max_size
        self._pre_warm_target = min(pre_warm, max_size)
        self.health_check_timeout = health_check_timeout
        self.reset_timeout = reset_timeout

        self._available: deque[PooledVM] = deque()
        self._in_use: dict[str, PooledVM] = {}
        self._all_vms: dict[str, PooledVM] = {}
        self._untracked_envs: set = set()
        self._condition = asyncio.Condition()
        self._provisioning = 0
        self._closed = False
        self._replenish_task: asyncio.Task[None] | None = None

    async def acquire(self, ctx: AgentContext | None = None) -> PooledVM:
        """Acquire a healthy pooled VM, provisioning one when capacity allows."""
        agent_ctx = ctx or self.prototype_ctx
        self._validate_ctx(agent_ctx)

        while True:
            pooled_vm = await self._acquire_or_provision(agent_ctx)
            if pooled_vm.use_count == 0:
                pooled_vm.use_count = 1
                pooled_vm.last_used_at = time.monotonic()
                logger.info(
                    "Warm pool: acquired fresh VM %s (pool: %d available, %d in-use, %d total)",
                    pooled_vm.alias,
                    len(self._available),
                    len(self._in_use),
                    len(self._all_vms),
                )
                return pooled_vm

            if await self._health_check(pooled_vm):
                pooled_vm.use_count += 1
                pooled_vm.last_used_at = time.monotonic()
                logger.info(
                    "Warm pool: reusing VM %s (use_count=%d, pool: %d available, %d in-use, %d total)",
                    pooled_vm.alias,
                    pooled_vm.use_count,
                    len(self._available),
                    len(self._in_use),
                    len(self._all_vms),
                )
                return pooled_vm

            logger.warning("Discarding unhealthy warm-pooled VM %s", pooled_vm.alias)
            await self._destroy_checked_out_vm(pooled_vm)

    async def release(
        self,
        pooled_vm: PooledVM,
        *,
        workspace_paths: list[str],
        destroy: bool = False,
    ) -> None:
        """Return a VM to the pool or destroy it if reset/health-check fails."""
        await self._mark_not_in_use(pooled_vm.alias)

        if destroy or not pooled_vm.healthy or self._closed:
            await self._destroy_vm(pooled_vm)
            self._schedule_replenish()
            return

        try:
            reset_ok = await self._reset_vm(pooled_vm, workspace_paths)
            health_ok = reset_ok and await self._health_check(pooled_vm)
        except Exception:
            logger.exception("Warm pool reset failed for %s", pooled_vm.alias)
            health_ok = False

        if not health_ok:
            pooled_vm.healthy = False
            logger.info("Warm pool: destroying unhealthy VM %s after reset failure", pooled_vm.alias)
            await self._destroy_vm(pooled_vm)
            self._schedule_replenish()
            return

        pooled_vm.last_used_at = time.monotonic()
        async with self._condition:
            if self._closed:
                destroy_now = True
            else:
                self._available.append(pooled_vm)
                self._condition.notify_all()
                destroy_now = False
                logger.info(
                    "Warm pool: released VM %s back to pool (pool: %d available, %d in-use, %d total)",
                    pooled_vm.alias,
                    len(self._available),
                    len(self._in_use),
                    len(self._all_vms),
                )

        if destroy_now:
            await self._destroy_vm(pooled_vm)

    async def pre_warm(self) -> None:
        """Provision the configured number of warm VMs ahead of time."""
        target = min(self._pre_warm_target, self.max_size)
        if target <= 0:
            return

        # Determine how many VMs we actually need under the lock, then provision outside it.
        async with self._condition:
            current = len(self._all_vms) + self._provisioning
            needed = max(0, target - current)
            self._provisioning += needed

        if needed <= 0:
            return

        results = await asyncio.gather(
            *(self._provision_vm(self.prototype_ctx) for _ in range(needed)),
            return_exceptions=True,
        )

        provisioned: list[PooledVM] = []
        failures = 0
        for result in results:
            if isinstance(result, BaseException):
                failures += 1
                logger.warning("Warm pool pre-warm provision failed: %s", result)
            else:
                provisioned.append(result)

        async with self._condition:
            self._provisioning -= needed
            for vm in provisioned:
                self._untracked_envs.discard(vm.agent_env)
                if not self._closed:
                    self._all_vms[vm.alias] = vm
                    self._available.append(vm)
            self._condition.notify_all()

        if self._closed:
            await asyncio.gather(*(self._destroy_env(vm) for vm in provisioned), return_exceptions=True)

    async def shutdown(self) -> None:
        """Destroy every VM managed by the pool."""
        logger.info(
            "Warm pool shutting down: %d total VMs, %d available, %d in-use, %d untracked",
            len(self._all_vms),
            len(self._available),
            len(self._in_use),
            len(self._untracked_envs),
        )
        async with self._condition:
            self._closed = True
            self._condition.notify_all()

        # Cancel and await the replenish task so any in-flight provisioning
        # finishes cleanup before we collect the final VM set.
        if self._replenish_task is not None:
            self._replenish_task.cancel()
            try:
                await self._replenish_task
            except (asyncio.CancelledError, Exception):
                pass
            self._replenish_task = None

        async with self._condition:
            pooled_vms = list(self._all_vms.values())
            leaked_envs = list(self._untracked_envs)
            self._available.clear()
            self._in_use.clear()
            self._all_vms.clear()
            self._untracked_envs.clear()

        destroy_coros = [self._destroy_env(vm) for vm in pooled_vms]
        destroy_coros += [self._safe_remove_env(env) for env in leaked_envs]
        if destroy_coros:
            await asyncio.gather(*destroy_coros, return_exceptions=True)

    async def _acquire_or_provision(self, ctx: AgentContext) -> PooledVM:
        while True:
            async with self._condition:
                if self._closed:
                    raise RuntimeError("WarmPool has been shut down")

                if self._available:
                    pooled_vm = self._available.popleft()
                    self._in_use[pooled_vm.alias] = pooled_vm
                    return pooled_vm

                if len(self._all_vms) + self._provisioning < self.max_size:
                    self._provisioning += 1
                    break

                await self._condition.wait()

        try:
            pooled_vm = await self._provision_vm(ctx)
        except Exception:
            async with self._condition:
                self._provisioning -= 1
                self._condition.notify_all()
            raise

        async with self._condition:
            self._provisioning -= 1
            self._untracked_envs.discard(pooled_vm.agent_env)
            if self._closed:
                destroy_now = True
            else:
                self._all_vms[pooled_vm.alias] = pooled_vm
                self._in_use[pooled_vm.alias] = pooled_vm
                self._condition.notify_all()
                destroy_now = False

        if destroy_now:
            await self._destroy_env(pooled_vm)
            raise RuntimeError("WarmPool was shut down during provisioning")
        return pooled_vm

    async def _mark_not_in_use(self, alias: str) -> None:
        async with self._condition:
            self._in_use.pop(alias, None)
            self._condition.notify_all()

    async def _destroy_checked_out_vm(self, pooled_vm: PooledVM) -> None:
        await self._mark_not_in_use(pooled_vm.alias)
        await self._destroy_vm(pooled_vm)
        self._schedule_replenish()

    async def _destroy_vm(self, pooled_vm: PooledVM) -> None:
        async with self._condition:
            self._all_vms.pop(pooled_vm.alias, None)
            self._in_use.pop(pooled_vm.alias, None)
            self._available = deque(vm for vm in self._available if vm.alias != pooled_vm.alias)
            self._condition.notify_all()

        await self._destroy_env(pooled_vm)

    async def _destroy_env(self, pooled_vm: PooledVM) -> None:
        try:
            await self.session.remove_env(pooled_vm.agent_env)
        except Exception as exc:
            logger.warning("Failed to destroy pooled VM %s: %s", pooled_vm.alias, exc)

    async def _safe_remove_env(self, agent_env: Environment) -> None:
        try:
            await self.session.remove_env(agent_env)
        except Exception as exc:
            logger.warning("Failed to destroy leaked env: %s", exc)

    def _schedule_replenish(self) -> None:
        if self._closed or self._pre_warm_target <= 0:
            return
        if self._replenish_task is not None and not self._replenish_task.done():
            return
        self._replenish_task = asyncio.create_task(self._replenish_to_target())

    async def _replenish_to_target(self) -> None:
        try:
            await self.pre_warm()
        except Exception:
            logger.exception("Warm pool replenish failed")

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=10, min=10, max=60),
        before_sleep=tenacity.before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    async def _provision_vm(self, ctx: AgentContext) -> PooledVM:
        if not self.ssh_key_path:
            raise RuntimeError("ssh_key_path required for warm pool provisioning")

        alias = _make_agent_alias(ctx.display_name)
        logger.info(
            "Creating pooled agent VM: %s (image: %s, cpus=%d, mem=%dMB)",
            alias,
            ctx.image,
            self.vm_config.cpus,
            self.vm_config.memory,
        )
        agent_env = await self.session.add_env(
            Env.resource(
                simulator=alias,
                sim_config=SimConfigCompute(
                    cpus=self.vm_config.cpus,
                    memory=self.vm_config.memory,
                    disk=self.vm_config.disk,
                ),
                alias=alias,
                docker_image_url=ctx.image,
                upload_rootfs=False,
                rootfs_storage_backend="snapshot-store",
            ),
            timeout=self.vm_config.timeout,
        )
        # Track the env immediately so shutdown can clean it up if we're
        # cancelled before the VM is registered in _all_vms.
        self._untracked_envs.add(agent_env)

        mesh_ip = agent_env.mesh_ip or await agent_env.get_mesh_ip()
        if not mesh_ip:
            try:
                await self.session.remove_env(agent_env)
                self._untracked_envs.discard(agent_env)
            except Exception:
                logger.warning("Failed to clean up VM %s (no mesh IP)", alias)
            raise RuntimeError(f"Failed to get mesh IP for pooled VM {alias}")

        try:
            pub_key = Path(str(self.ssh_key_path) + ".pub").read_text().strip()
            await agent_env.add_ssh_key(pub_key)

            await install_agent_code_on_vm(self.ssh_key_path, mesh_ip, ctx)
            runner_path = await resolve_runner_path(self.ssh_key_path, mesh_ip)
        except BaseException:
            logger.warning("Post-creation provisioning failed for %s, destroying VM", alias)
            try:
                await self.session.remove_env(agent_env)
                self._untracked_envs.discard(agent_env)
            except Exception:
                logger.warning("Failed to clean up VM %s during error handling", alias)
            raise

        now = time.monotonic()
        return PooledVM(
            agent_env=agent_env,
            mesh_ip=mesh_ip,
            alias=alias,
            image=ctx.image,
            runner_path=runner_path,
            created_at=now,
            last_used_at=now,
            use_count=0,
        )

    async def _reset_vm(self, pooled_vm: PooledVM, workspace_paths: list[str]) -> bool:
        commands = await self._get_reset_commands(pooled_vm, workspace_paths)
        # Each command runs in a subshell with || true so one failure doesn't abort the chain.
        command = " && ".join(f"({cmd}) || true" for cmd in commands)
        command += " && echo warm-pool-reset-ok"
        exit_code, stdout, stderr = await self._run_ssh(
            pooled_vm.mesh_ip,
            command,
            timeout=self.reset_timeout,
        )
        if exit_code != 0 or "warm-pool-reset-ok" not in stdout:
            logger.warning(
                "Warm pool reset failed on %s (exit=%d): stdout=%s stderr=%s",
                pooled_vm.alias,
                exit_code,
                stdout.strip()[-200:] if stdout else "",
                stderr.strip()[-200:] if stderr else "",
            )
            return False
        return True

    async def _get_reset_commands(self, pooled_vm: PooledVM, workspace_paths: list[str]) -> list[str]:
        quoted_paths = " ".join(shlex.quote(path) for path in workspace_paths)
        command = f"{shlex.quote(pooled_vm.runner_path)} reset-commands --workspace-paths {quoted_paths}"
        exit_code, stdout, stderr = await self._run_ssh(
            pooled_vm.mesh_ip,
            command,
            timeout=self.reset_timeout,
        )
        if exit_code != 0:
            raise RuntimeError(
                f"Agent VM {pooled_vm.alias} could not report reset commands: {stderr.strip() or stdout.strip()}"
            )
        try:
            commands = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Agent VM {pooled_vm.alias} returned invalid reset command JSON") from exc
        if not isinstance(commands, list) or not all(isinstance(cmd, str) for cmd in commands):
            raise RuntimeError(f"Agent VM {pooled_vm.alias} returned malformed reset commands")
        if not commands:
            raise RuntimeError(f"Agent VM {pooled_vm.alias} returned no reset commands")
        return commands

    async def _health_check(self, pooled_vm: PooledVM) -> bool:
        exit_code, stdout, _ = await self._run_ssh(
            pooled_vm.mesh_ip,
            "echo warm-pool-ok",
            timeout=self.health_check_timeout,
        )
        healthy = exit_code == 0 and stdout.strip() == "warm-pool-ok"
        pooled_vm.healthy = healthy
        return healthy

    async def _run_ssh(
        self,
        hostname: str,
        command: str,
        *,
        timeout: int,
    ) -> tuple[int, str, str]:
        if not self.ssh_key_path:
            raise RuntimeError("ssh_key_path required for warm pool SSH operations")
        return await run_ssh(
            self.ssh_key_path,
            hostname,
            command,
            user="root",
            timeout=timeout,
            extra_opts=_VM_SSH_EXTRA_OPTS,
        )

    def _validate_ctx(self, ctx: AgentContext) -> None:
        if ctx.image != self.prototype_ctx.image:
            raise ValueError(
                f"WarmPool prototype image {self.prototype_ctx.image!r} does not match requested image {ctx.image!r}"
            )
        if ctx.agent_code_path != self.prototype_ctx.agent_code_path:
            raise ValueError("WarmPool prototype agent_code_path does not match requested agent_code_path")
