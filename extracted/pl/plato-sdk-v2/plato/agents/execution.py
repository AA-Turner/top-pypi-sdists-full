"""Shared queued agent execution for pooled parallel runs."""

from __future__ import annotations

import asyncio
import logging
import uuid
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from plato.agents.mounts import AgentWorkspaceMount, GitCheckoutPolicy, GitSyncPolicy
from plato.agents.warmpool import WarmPool
from plato.git_ops.merge import delete_remote_ref, merge_ref_to_main
from plato.git_ops.repo import trust_git_directory
from plato.runtimes.base import Runtime, RuntimeInfo
from plato.runtimes.config import VMRuntimeConfig
from plato.transports.git import GitPublishedRef, GitTransport
from plato.worlds.workspace import Workspace

if TYPE_CHECKING:
    from plato.agents.review_gate import ReviewGateResult
    from plato.agents.task import AgentTask
    from plato.worlds.config import AgentConfig

logger = logging.getLogger(__name__)


class AgentExecutionManager:
    """World-scoped queued executor for one agent-config/primary-mount pair."""

    def __init__(
        self,
        *,
        agent_config: AgentConfig,
        runtime_factory: Callable[[], Runtime],
        world_runtime_info: RuntimeInfo | None = None,
        checkpoint: Callable[[str], Awaitable[None]] | None = None,
        primary_workspace: Workspace | None = None,
        primary_mount: AgentWorkspaceMount | None = None,
        total_agents: int | None = None,
        min_warmpool_timeout: int = 43200,
    ) -> None:
        if agent_config.max_parallel is None:
            raise ValueError("AgentExecutionManager requires agent_config.max_parallel")

        self._agent_config = agent_config
        self._world_runtime_info = world_runtime_info
        self._checkpoint = checkpoint
        self._primary_workspace = primary_workspace
        self._primary_mount = primary_mount
        self._min_warmpool_timeout = min_warmpool_timeout

        vm_timeout: int | None = None
        if isinstance(agent_config.runtime, VMRuntimeConfig):
            if total_agents is not None:
                vm_timeout = agent_config.runtime.timeout * total_agents
            vm_timeout = max(vm_timeout or 0, min_warmpool_timeout) if min_warmpool_timeout > 0 else vm_timeout

        self._warm_pool = WarmPool(
            runtime_factory=runtime_factory,
            image=agent_config.image,
            max_size=agent_config.max_parallel,
            pre_warm=0,
            vm_timeout=vm_timeout,
        )
        self._integration_lock = asyncio.Lock()

    def update_vm_timeout(self, total_agents: int) -> None:
        """Recompute the pool's VM sandbox timeout for a (possibly larger) agent count."""
        if not isinstance(self._agent_config.runtime, VMRuntimeConfig):
            return
        new_timeout = max(
            self._agent_config.runtime.timeout * total_agents,
            self._min_warmpool_timeout,
        )
        if self._warm_pool._vm_timeout is None or new_timeout > self._warm_pool._vm_timeout:
            self._warm_pool._vm_timeout = new_timeout

    async def shutdown(self) -> None:
        await self._warm_pool.shutdown()

    async def run(
        self,
        task: AgentTask,
        instruction: str,
        display_name: str | None = None,
    ) -> str:
        run_mounts = [mount.clone_for_run() for mount in task._all_mounts()]
        task_name = _task_slug(display_name or task._display_name or "agent-task")
        published_transport = await self._prepare_git_mount(run_mounts, task_name)

        # Wire up review gate if the task has a review_fn
        review_fn = task._review_fn
        if review_fn is not None and published_transport is not None:
            self._attach_review_gate(task, task_name, published_transport, review_fn)

        pooled_runtime = await self._warm_pool.acquire()
        try:
            agent_id = await task._run_on_runtime(
                pooled_runtime.runtime_info,
                instruction,
                display_name=display_name,
                mounts=run_mounts,
            )
        except Exception:
            await self._warm_pool.release(
                pooled_runtime,
                workspace_paths=[mount.agent_path for mount in run_mounts],
                destroy=True,
            )
            raise

        await self._warm_pool.release(
            pooled_runtime,
            workspace_paths=[mount.agent_path for mount in run_mounts],
        )

        # Only auto-merge if no review gate handled it
        if review_fn is None and published_transport is not None and published_transport.published_ref is not None:
            await self._integrate_published_ref(
                task_name=task_name,
                published_ref=published_transport.published_ref,
            )
            task.merged = True
        return agent_id

    def _attach_review_gate(
        self,
        task: AgentTask,
        task_name: str,
        published_transport: GitTransport,
        review_fn: Callable[..., Awaitable[ReviewGateResult]],
    ) -> None:
        """Wire up the review gate on the task for review-before-merge flow."""
        from plato.agents.review_gate import ReviewGateMergeResult, attach_review_gate

        primary_transport = _git_transport_from_mount(self._primary_mount) if self._primary_mount else None

        async def _merge() -> bool | ReviewGateMergeResult:
            # published_ref is set after workspace sync-back during each attempt
            pub_ref = published_transport.published_ref
            if pub_ref is None:
                logger.warning("No published ref available for merge after review pass")
                return ReviewGateMergeResult(merged=False, error="missing published ref")

            if primary_transport is None:
                return ReviewGateMergeResult(merged=False, error="missing primary transport")

            async with self._integration_lock, _optional_lock(primary_transport.sync_lock):
                result = await merge_ref_to_main(
                    primary_transport.bare_repo_path,
                    pub_ref.ref,
                    squash=True,
                    commit_message=f"Merge {task_name}",
                )
                if not result.merged:
                    return ReviewGateMergeResult(merged=False, conflict_files=result.unmerged_files)

                await primary_transport._refresh_local_workspace_from_main()

                # Checkpoint tracked workspace
                workspace = self._primary_workspace
                if workspace is not None and workspace.tracked and self._checkpoint is not None:
                    step_name = f"parallel_agents.{task_name}.{result.commit_sha[:12]}"
                    await workspace.ensure_fuse_mount()
                    await workspace.materialize_current_tree_into_overlay()
                    await self._checkpoint(step_name)

                await delete_remote_ref(primary_transport.bare_repo_path, pub_ref.ref)
                task.merged = True
                return ReviewGateMergeResult(merged=True)

        _review_attempt = 0

        async def _review_with_no_change_guard(hostname: str, *, attempt_number: int = 1) -> ReviewGateResult:
            from plato.agents.review_gate import ReviewGateResult

            nonlocal _review_attempt
            _review_attempt += 1

            if published_transport.published_ref is None and _review_attempt > 1:
                logger.warning(
                    "No published ref for %s on attempt %d — builder made no changes, skipping review",
                    task_name,
                    _review_attempt,
                )
                return ReviewGateResult(
                    passed=False,
                    feedback=(
                        "Your code was not submitted for review because no changes were committed. "
                        "You must actually modify the code to address the requested changes, "
                        "then commit your work. Re-read the instructions and make the required changes."
                    ),
                    result_data={},
                )
            return await review_fn(hostname, attempt_number=attempt_number)

        result_dir = self._primary_mount.world_path if self._primary_mount else None

        attach_review_gate(
            task,
            review_fn=_review_with_no_change_guard,
            branch_name=f"plato-task/{task_name}",
            merge_fn=_merge,
            reviewed_commit_fn=lambda: (
                published_transport.published_ref.commit_sha if published_transport.published_ref is not None else None
            ),
            max_continuations=task._max_review_continuations,
            result_dir=result_dir,
            exhaustion_policy=getattr(task, "_review_exhaustion_policy", "fail"),
        )

    async def _prepare_git_mount(
        self,
        mounts: list[AgentWorkspaceMount],
        task_name: str,
    ) -> GitTransport | None:
        if not mounts:
            return None

        primary_mount = mounts[0]
        if primary_mount.transport_kind != "git" or primary_mount.git_sync is None:
            return None
        # Already configured for publish_ref — use the caller's setup as-is
        if primary_mount.git_sync.mode == "publish_ref":
            return _git_transport_from_mount(primary_mount)

        if primary_mount.git_sync.mode != "merge_to_main":
            return None

        transport = _git_transport_from_mount(primary_mount)
        base_ref = await asyncio.to_thread(_rev_parse_ref, transport.bare_repo_path, "main")
        publish_prefix = f"refs/plato/tasks/{task_name}-{uuid.uuid4().hex}"
        mounts[0] = primary_mount.with_git_options(
            checkout=GitCheckoutPolicy(
                ref=base_ref,
                branch_name=f"plato-task/{task_name}",
            ),
            sync=GitSyncPolicy.publish_ref(publish_prefix, exact=False),
            raise_on_conflict=False,
        )
        return _git_transport_from_mount(mounts[0])

    async def _integrate_published_ref(
        self,
        *,
        task_name: str,
        published_ref: GitPublishedRef,
    ) -> None:
        if self._primary_mount is None or self._primary_mount.transport_kind != "git":
            return

        transport = _git_transport_from_mount(self._primary_mount)

        async with self._integration_lock, _optional_lock(transport.sync_lock):
            result = await merge_ref_to_main(
                transport.bare_repo_path,
                published_ref.ref,
                squash=True,
                commit_message=f"Merge parallel task {task_name}",
            )
            if not result.merged:
                raise RuntimeError(f"Merge conflict integrating task {task_name}")

            await transport._refresh_local_workspace_from_main()
            await self._checkpoint_tracked_workspace(task_name, published_ref)
            await delete_remote_ref(transport.bare_repo_path, published_ref.ref)

    async def _checkpoint_tracked_workspace(self, task_name: str, published_ref: GitPublishedRef) -> None:
        workspace = self._primary_workspace
        if workspace is None or not workspace.tracked or self._checkpoint is None:
            return
        step_name = f"parallel_agents.{task_name}.{published_ref.commit_sha[:12]}"
        await workspace.ensure_fuse_mount()
        await workspace.materialize_current_tree_into_overlay()
        await self._checkpoint(step_name)


@asynccontextmanager
async def _optional_lock(lock: asyncio.Lock | None):
    if lock is None:
        yield
        return
    async with lock:
        yield


def _task_slug(value: str) -> str:
    chars: list[str] = []
    for char in value.lower():
        if char.isalnum():
            chars.append(char)
        else:
            chars.append("-")
    return "".join(chars).strip("-") or "task"


def _git_transport_from_mount(mount: AgentWorkspaceMount) -> GitTransport:
    transport = mount.transport
    if not isinstance(transport, GitTransport):
        raise TypeError(f"Expected git transport, got {type(transport).__name__}")
    return transport


def _rev_parse_ref(repo_path: str, ref: str) -> str:
    from git import Repo

    trust_git_directory(repo_path)
    return Repo(repo_path).commit(ref).hexsha
