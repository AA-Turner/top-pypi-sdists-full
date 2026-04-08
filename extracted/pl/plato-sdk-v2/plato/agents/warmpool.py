"""Warm pooling for reusable agent runtimes."""

from __future__ import annotations

import asyncio
import logging
import shlex
import time
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import tenacity

from plato.agents import vm_setup
from plato.runtimes.base import Runtime, RuntimeInfo

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class PooledVM:
    """A reusable started runtime managed by :class:`WarmPool`."""

    vm_runtime: Runtime
    runtime_info: RuntimeInfo
    alias: str
    image: str
    created_at: float
    last_used_at: float
    use_count: int
    healthy: bool = True


class WarmPool:
    """Manage a reusable pool of started runtimes.

    Each pooled entry is backed by a dedicated :class:`Runtime` instance with one
    started environment. The pool handles provisioning, health checks, reset,
    and replenishment.
    """

    def __init__(
        self,
        runtime_factory: Callable[[], Runtime],
        image: str,
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

        self._runtime_factory = runtime_factory
        self._image = image
        self.max_size = max_size
        self._pre_warm_target = min(pre_warm, max_size)
        self.health_check_timeout = health_check_timeout
        self.reset_timeout = reset_timeout

        self._available: deque[PooledVM] = deque()
        self._in_use: dict[str, PooledVM] = {}
        self._all_vms: dict[str, PooledVM] = {}
        self._condition = asyncio.Condition()
        self._provisioning = 0
        self._closed = False
        self._replenish_task: asyncio.Task[None] | None = None
        self._replenish_requests = 0

    def _make_runtime(self) -> Runtime:
        """Create a fresh runtime for one agent environment."""
        return self._runtime_factory()

    async def acquire(self) -> PooledVM:
        """Acquire a healthy pooled VM, provisioning one when capacity allows."""
        while True:
            pooled_vm = await self._acquire_or_provision()
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

        async with self._condition:
            current = len(self._all_vms) + self._provisioning
            needed = max(0, target - current)
            self._provisioning += needed

        if needed <= 0:
            return

        results = await asyncio.gather(*(self._provision_vm() for _ in range(needed)), return_exceptions=True)

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
                if not self._closed:
                    self._all_vms[vm.alias] = vm
                    self._available.append(vm)
            self._condition.notify_all()

        if self._closed:
            await asyncio.gather(*(self._destroy_vm(vm) for vm in provisioned), return_exceptions=True)

    async def shutdown(self) -> None:
        """Destroy every VM managed by the pool."""
        logger.info(
            "Warm pool shutting down: %d total VMs, %d available, %d in-use",
            len(self._all_vms),
            len(self._available),
            len(self._in_use),
        )
        async with self._condition:
            self._closed = True
            self._condition.notify_all()

        if self._replenish_task is not None:
            self._replenish_task.cancel()
            try:
                await self._replenish_task
            except (asyncio.CancelledError, Exception):
                pass
            self._replenish_task = None

        async with self._condition:
            pooled_vms = list(self._all_vms.values())
            self._available.clear()
            self._in_use.clear()
            self._all_vms.clear()

        if pooled_vms:
            await asyncio.gather(*(self._destroy_vm(vm) for vm in pooled_vms), return_exceptions=True)

    async def _acquire_or_provision(self) -> PooledVM:
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
            pooled_vm = await self._provision_vm()
        except Exception:
            async with self._condition:
                self._provisioning -= 1
                self._condition.notify_all()
            raise

        async with self._condition:
            self._provisioning -= 1
            if self._closed:
                destroy_now = True
            else:
                self._all_vms[pooled_vm.alias] = pooled_vm
                self._in_use[pooled_vm.alias] = pooled_vm
                self._condition.notify_all()
                destroy_now = False

        if destroy_now:
            await self._destroy_vm(pooled_vm)
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

        try:
            await pooled_vm.vm_runtime.stop(pooled_vm.runtime_info.runtime_id)
        except Exception as exc:
            logger.warning("Failed to destroy pooled VM %s: %s", pooled_vm.alias, exc)

    def _schedule_replenish(self) -> None:
        if self._closed or self._pre_warm_target <= 0:
            return
        self._replenish_requests += 1
        if self._replenish_task is not None and not self._replenish_task.done():
            return
        self._replenish_task = asyncio.create_task(self._replenish_to_target())

    async def _replenish_to_target(self) -> None:
        try:
            while True:
                async with self._condition:
                    if self._closed:
                        return
                    target = min(self._pre_warm_target, self.max_size)
                    if target <= 0:
                        return
                    before_current = len(self._all_vms) + self._provisioning
                    self._replenish_requests = 0

                await self.pre_warm()

                async with self._condition:
                    if self._closed:
                        return
                    target = min(self._pre_warm_target, self.max_size)
                    after_current = len(self._all_vms) + self._provisioning
                    pending_requests = self._replenish_requests

                if after_current >= target and pending_requests == 0:
                    return

                if after_current <= before_current and pending_requests == 0:
                    logger.warning(
                        "Warm pool replenish stalled below target "
                        "(current=%d target=%d); stopping retries until the next replenish request",
                        after_current,
                        target,
                    )
                    return
        except Exception:
            logger.exception("Warm pool replenish failed")

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=1, max=5),
        before_sleep=tenacity.before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    async def _provision_vm(self) -> PooledVM:
        """Provision a new pooled runtime."""
        alias = vm_setup.make_agent_alias("warm-pool")
        vm_rt = self._make_runtime()

        logger.info(
            "Creating pooled runtime: %s (image: %s)",
            alias,
            self._image,
        )

        info = await vm_rt.start(alias=alias)

        now = time.monotonic()
        return PooledVM(
            vm_runtime=vm_rt,
            runtime_info=info,
            alias=alias,
            image=self._image,
            created_at=now,
            last_used_at=now,
            use_count=0,
        )

    async def _reset_vm(self, pooled_vm: PooledVM, workspace_paths: list[str]) -> bool:
        commands = _runtime_reset_commands(workspace_paths)
        command = " && ".join(f"({cmd}) || true" for cmd in commands)
        command += " && echo warm-pool-reset-ok"
        exit_code, stdout, stderr = await pooled_vm.vm_runtime.exec(
            pooled_vm.runtime_info.runtime_id,
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

    async def _health_check(self, pooled_vm: PooledVM) -> bool:
        exit_code, stdout, _ = await pooled_vm.vm_runtime.exec(
            pooled_vm.runtime_info.runtime_id,
            "echo warm-pool-ok",
            timeout=self.health_check_timeout,
        )
        healthy = exit_code == 0 and stdout.strip() == "warm-pool-ok"
        pooled_vm.healthy = healthy
        return healthy


def _runtime_reset_commands(workspace_paths: list[str]) -> list[str]:
    """Return generic runtime cleanup commands for a pooled VM."""
    commands = [
        "pkill -x plato-agent-runner 2>/dev/null; true",
        "rm -rf /tmp/plato-* /var/tmp/* 2>/dev/null; true",
        ": > /etc/environment",
        "sed -i '/runtime\\.plato\\.internal/d' /etc/hosts 2>/dev/null; true",
    ]
    for workspace_path in workspace_paths:
        quoted_path = shlex.quote(str(Path(workspace_path)))
        commands.append(
            f"umount -l {quoted_path} 2>/dev/null; rm -rf {quoted_path} 2>/dev/null; mkdir -p {quoted_path}"
        )
    return commands
