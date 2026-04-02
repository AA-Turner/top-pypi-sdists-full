"""Parallel agent orchestration for git-transported workspaces."""

from __future__ import annotations

import asyncio
import logging
import shutil
import tempfile
import time
import uuid
from collections.abc import Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, cast

from git import Repo
from git.exc import GitCommandError

from plato.agents.runtime.base import AgentContext
from plato.agents.runtime.vm import VMConfig
from plato.agents.runtime.warmpool import WarmPool
from plato.git_ops.repo import AGENT_ACTOR, trust_git_directory
from plato.runtime import VMRuntimeConfig
from plato.transports import GitCheckout, GitPublishedRef, GitSyncBack, GitTransport, RsyncTransport
from plato.worlds.workspace import Workspace

if TYPE_CHECKING:
    from plato.worlds.base import BaseWorld
    from plato.worlds.config import AgentConfig

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ParallelAgentResult:
    """Structured result for one submitted parallel agent task."""

    name: str
    status: Literal["success", "failed", "skipped"]
    agent_id: str | None = None
    error: str | None = None
    merged: bool = False
    branch_name: str | None = None


@dataclass(slots=True)
class _SubmittedTask:
    name: str
    instruction: str
    display_name: str | None
    skip_if: Callable[[], bool] | None
    on_completed: Callable[[ParallelAgentResult], None] | None


@dataclass(slots=True)
class _QueuedIntegration:
    task: _SubmittedTask
    published_ref: GitPublishedRef
    future: asyncio.Future[bool]


class ParallelAgentOrchestrator:
    """Run multiple git-transported agent tasks with world-side serialized integration."""

    def __init__(
        self,
        world: BaseWorld,
        workspace: Workspace,
        agent_config: AgentConfig,
        *,
        max_parallel: int = 4,
        merge_agent_config: AgentConfig | None = None,
        extra_workspaces: list[Workspace] | None = None,
        warm_pool: bool = False,
        use_named_branches: bool = False,
        agent_prepare: Callable[..., Any] | None = None,
        pre_integrate: Callable[..., Any] | None = None,
    ) -> None:
        """
        Args:
            use_named_branches: When True, each task publishes to a named branch
                ``pr/<slug>`` instead of a hidden ref.  This makes the branch
                visible for code review (e.g. ``git diff main...pr/<slug>``).
            agent_prepare: Optional async callback ``(runner, task_name) -> None``
                called after the agent runner is created but before ``runner.run()``.
                Use this to add ``on_prepare`` hooks (e.g. starting dev servers).
            pre_integrate: Optional async callback
                ``(task_name, branch_name, published_ref) -> bool`` called before
                the integration worker merges a task's ref into main.  Return
                ``True`` to proceed with the merge, ``False`` to skip it.
        """
        if not isinstance(workspace.transport, GitTransport):
            raise ValueError("ParallelAgentOrchestrator requires a git-transported workspace")
        if max_parallel < 1:
            raise ValueError("max_parallel must be at least 1")

        self._world = world
        self._workspace = workspace
        self._git_transport = workspace.transport
        self._agent_config = agent_config
        self._merge_agent_config = merge_agent_config or agent_config
        self._warm_pool_enabled = warm_pool
        self._warm_pool: WarmPool | None = None
        self._max_parallel = max_parallel
        self._extra_workspaces: list[Workspace] = extra_workspaces or []

        if warm_pool:
            self._semaphore = None  # pool.acquire() provides backpressure
        else:
            self._semaphore = asyncio.Semaphore(max_parallel)

        self._tasks: list[_SubmittedTask] = []
        self._use_named_branches = use_named_branches
        self._agent_prepare = agent_prepare
        self._pre_integrate = pre_integrate
        self._resolved_base_ref: str | None = None

    @property
    def resolved_base_ref(self) -> str | None:
        """Pinned base SHA resolved for the current orchestrator run."""
        return self._resolved_base_ref

    async def submit(
        self,
        name: str,
        instruction: str,
        *,
        display_name: str | None = None,
        skip_if: Callable[[], bool] | None = None,
        on_completed: Callable[[ParallelAgentResult], None] | None = None,
    ) -> None:
        """Register a task to be run later by :meth:`run_all`.

        Args:
            on_completed: Called immediately after the task's result is
                determined (including merge/integration), *before*
                ``run_all`` returns.  Use this to write durable cache
                files so they are captured by the next DVC checkpoint.
        """
        self._tasks.append(
            _SubmittedTask(
                name=name,
                instruction=instruction,
                display_name=display_name,
                skip_if=skip_if,
                on_completed=on_completed,
            )
        )

    async def run_all(self) -> list[ParallelAgentResult]:
        """Run every submitted task and return one result per task."""
        if not self._tasks:
            return []

        self._resolved_base_ref = await self._resolve_base_ref()

        if self._warm_pool_enabled:
            self._warm_pool = self._create_warm_pool(num_tasks=len(self._tasks))

        integration_queue: asyncio.Queue[_QueuedIntegration | None] = asyncio.Queue()
        integration_worker = asyncio.create_task(self._integration_worker(integration_queue))
        try:
            if self._warm_pool is not None:
                await self._warm_pool.pre_warm()
            pending = [asyncio.create_task(self._run_task(task, integration_queue)) for task in self._tasks]
            return await asyncio.gather(*pending)
        finally:
            await integration_queue.put(None)
            await integration_worker
            if self._warm_pool is not None:
                await self._warm_pool.shutdown()

    def _create_warm_pool(self, *, num_tasks: int) -> WarmPool:
        """Build a WarmPool from the world's session and agent config."""
        world = self._world
        session = world.plato_session
        ssh_key_path = world._ssh_key_path  # noqa: SLF001
        if session is None or ssh_key_path is None:
            raise RuntimeError("Warm pool requires a live Plato session with SSH key")

        runtime_cfg = self._agent_config.runtime
        if not isinstance(runtime_cfg, VMRuntimeConfig):
            raise RuntimeError("Warm pool requires a VM runtime config")

        # Scale timeout: each pooled VM may run ceil(num_tasks / max_parallel) sequential tasks
        waves = -(-num_tasks // self._max_parallel)  # ceiling division
        base_timeout = runtime_cfg.vm.timeout or 7200
        pool_timeout = base_timeout * waves

        vm_config = VMConfig(
            cpus=runtime_cfg.vm.cpus or 2,
            memory=runtime_cfg.vm.memory or 4096,
            disk=runtime_cfg.vm.disk or 10240,
            timeout=pool_timeout,
        )

        prototype_ctx = AgentContext(
            image=self._agent_config.image,
            config={},
            instruction="",
            display_name="warm-pool",
        )

        pool = WarmPool(
            session=session,
            ssh_key_path=ssh_key_path,
            vm_config=vm_config,
            prototype_ctx=prototype_ctx,
            max_size=self._max_parallel,
            pre_warm=self._max_parallel,
        )
        logger.info(
            "Created warm pool: max_size=%d, pre_warm=%d, vm_timeout=%ds (%d tasks, %d waves)",
            self._max_parallel,
            self._max_parallel,
            pool_timeout,
            num_tasks,
            waves,
        )
        return pool

    async def _run_task(
        self,
        task: _SubmittedTask,
        integration_queue: asyncio.Queue[_QueuedIntegration | None],
    ) -> ParallelAgentResult:
        try:
            if task.skip_if is not None and task.skip_if():
                result = ParallelAgentResult(name=task.name, status="skipped")
                self._fire_on_completed(task, result)
                return result
        except Exception as exc:
            return ParallelAgentResult(name=task.name, status="failed", error=str(exc))

        # Report task started to stage tracking
        from plato.worlds.durable import _get_otel_ids
        from plato.worlds.stage_tracking import _current_stage_public_id, report_stage

        parent_id = _current_stage_public_id.get(None)
        trace_id, span_id = _get_otel_ids()
        task_started_at = datetime.now(timezone.utc)
        t0 = time.monotonic()
        await report_stage(
            stage_name=task.name,
            stage_type="orchestrator_task",
            status="started",
            started_at=task_started_at,
            parent_stage_public_id=parent_id,
            trace_id=trace_id,
            span_id=span_id,
        )

        try:
            async with _optional_semaphore(self._semaphore):
                task_workspace, task_transport = self._make_task_workspace(task)
                logger.info(
                    "Starting parallel task '%s' with publish_ref_prefix=%s transport_id=%s",
                    task.name,
                    task_transport.publish_ref_prefix,
                    id(task_transport),
                )
                runner = self._world.agent(
                    self._agent_config,
                    display_name=task.display_name or task.name,
                    workspaces=[task_workspace, *self._extra_workspaces],
                    warm_pool=self._warm_pool,
                )
                if self._agent_prepare is not None:
                    await self._agent_prepare(runner, task.name)
                agent_id = await runner.run(task.instruction)
        except Exception as exc:
            elapsed = time.monotonic() - t0
            await report_stage(
                stage_name=task.name,
                stage_type="orchestrator_task",
                status="failed",
                started_at=task_started_at,
                completed_at=datetime.now(timezone.utc),
                elapsed_seconds=elapsed,
                error_message=str(exc)[:2000],
                parent_stage_public_id=parent_id,
            )
            return ParallelAgentResult(
                name=task.name,
                status="failed",
                error=str(exc),
            )

        branch = f"pr/{_slug(task.name)}" if self._use_named_branches else None
        published_ref = task_transport.published_ref
        if published_ref is None:
            logger.info(
                "Parallel task '%s' finished without a published ref; treating sync as already merged", task.name
            )
            result = ParallelAgentResult(
                name=task.name,
                status="success",
                agent_id=agent_id,
                merged=True,
                branch_name=branch,
            )
            elapsed = time.monotonic() - t0
            await report_stage(
                stage_name=task.name,
                stage_type="orchestrator_task",
                status="completed",
                started_at=task_started_at,
                completed_at=datetime.now(timezone.utc),
                elapsed_seconds=elapsed,
                parent_stage_public_id=parent_id,
                metadata={"agent_id": agent_id, "merged": True, "branch_name": branch},
            )
            self._fire_on_completed(task, result)
            return result

        logger.info("Parallel task '%s' published ref %s (%s)", task.name, published_ref.ref, published_ref.commit_sha)
        integration_future: asyncio.Future[bool] = asyncio.get_running_loop().create_future()
        await integration_queue.put(
            _QueuedIntegration(
                task=task,
                published_ref=published_ref,
                future=integration_future,
            )
        )

        try:
            merged = await integration_future
        except Exception as exc:
            elapsed = time.monotonic() - t0
            await report_stage(
                stage_name=task.name,
                stage_type="orchestrator_task",
                status="failed",
                started_at=task_started_at,
                completed_at=datetime.now(timezone.utc),
                elapsed_seconds=elapsed,
                error_message=str(exc)[:2000],
                parent_stage_public_id=parent_id,
                metadata={"agent_id": agent_id},
            )
            return ParallelAgentResult(
                name=task.name,
                status="failed",
                agent_id=agent_id,
                error=str(exc),
            )

        result = ParallelAgentResult(
            name=task.name,
            status="success",
            agent_id=agent_id,
            merged=merged,
            branch_name=branch,
        )
        elapsed = time.monotonic() - t0
        await report_stage(
            stage_name=task.name,
            stage_type="orchestrator_task",
            status="completed",
            started_at=task_started_at,
            completed_at=datetime.now(timezone.utc),
            elapsed_seconds=elapsed,
            parent_stage_public_id=parent_id,
            metadata={"agent_id": agent_id, "merged": merged, "branch_name": branch},
        )
        self._fire_on_completed(task, result)
        return result

    @staticmethod
    def _fire_on_completed(task: _SubmittedTask, result: ParallelAgentResult) -> None:
        if task.on_completed is not None:
            try:
                task.on_completed(result)
            except Exception:
                logger.exception("on_completed callback failed for task '%s'", task.name)

    def _make_task_workspace(self, task: _SubmittedTask) -> tuple[Workspace, GitTransport]:
        if self._use_named_branches:
            publish_prefix = f"refs/heads/pr/{_slug(task.name)}"
            exact = True
        else:
            publish_prefix = f"refs/plato/tasks/{_slug(task.name)}-{uuid.uuid4().hex}"
            exact = False

        checkout = None
        if self._resolved_base_ref is not None:
            checkout = GitCheckout(
                self._resolved_base_ref,
                branch_name=f"plato-task/{_slug(task.name)}",
            )
        task_workspace = self._workspace.for_git_agent(
            checkout=checkout,
            sync_back=GitSyncBack.publish_ref(publish_prefix, exact=exact),
            mount_path=self._workspace.mount_path,
        )
        assert task_workspace.transport is not None
        task_transport = cast(GitTransport, task_workspace.transport)
        return task_workspace, task_transport

    async def _resolve_base_ref(self) -> str:
        try:
            return await asyncio.to_thread(_rev_parse_ref, self._git_transport.bare_repo_path, "main")
        except Exception as exc:
            raise RuntimeError(
                f"Failed to resolve orchestrator base ref from {self._git_transport.bare_repo_path}: {exc}"
            ) from exc

    async def _integration_worker(self, integration_queue: asyncio.Queue[_QueuedIntegration | None]) -> None:
        merge_cfg = self._git_transport.merge_config.merge_agent
        while True:
            queued = await integration_queue.get()
            try:
                if queued is None:
                    return
                merged = await self._integrate_published_ref(queued.task, queued.published_ref, merge_cfg.max_retries)
                if not queued.future.done():
                    queued.future.set_result(merged)
            except Exception as exc:
                if queued is not None and not queued.future.done():
                    queued.future.set_exception(exc)
            finally:
                integration_queue.task_done()

    async def _integrate_published_ref(
        self, task: _SubmittedTask, published_ref: GitPublishedRef, max_retries: int
    ) -> bool:
        if self._pre_integrate is not None:
            branch = f"pr/{_slug(task.name)}" if self._use_named_branches else published_ref.ref
            try:
                should_merge = await self._pre_integrate(task.name, branch, published_ref)
                if not should_merge:
                    logger.info("pre_integrate rejected task '%s' — skipping merge", task.name)
                    await self._delete_ref_direct(published_ref.ref)
                    return False
            except Exception:
                logger.exception("pre_integrate hook failed for task '%s'", task.name)
                raise

        merge_cfg = self._git_transport.merge_config.merge_agent
        async with _optional_lock(self._git_transport.sync_lock):
            for attempt in range(1, max_retries + 1):
                temp_dir = Path(tempfile.mkdtemp(prefix=f"merge-{_slug(task.name)}-"))
                try:
                    await self._clone_repo(temp_dir)
                    await self._fetch_ref(temp_dir, published_ref.ref)

                    if merge_cfg.strategy == "theirs":
                        logger.info("Discarding task ref %s using 'theirs' strategy", published_ref.ref)
                        await self._delete_ref(temp_dir, published_ref.ref)
                        return False

                    if merge_cfg.strategy == "ours":
                        await self._force_push_fetched_commit(temp_dir)
                        await self._checkpoint_tracked_workspace(task, published_ref)
                        await self._delete_ref(temp_dir, published_ref.ref)
                        return True

                    merge_conflicted = await self._merge_fetched_commit(temp_dir, task.name)
                    if merge_conflicted:
                        await self._run_merge_agent(task, temp_dir, merge_cfg.instruction_template)
                        await self._ensure_merge_complete(temp_dir)

                    await self._push_resolved_main(temp_dir, force=False)
                    await self._checkpoint_tracked_workspace(task, published_ref)
                    await self._delete_ref(temp_dir, published_ref.ref)
                    return True
                except RuntimeError:
                    if attempt == max_retries:
                        raise
                finally:
                    shutil.rmtree(temp_dir, ignore_errors=True)

        raise RuntimeError(f"Failed to integrate task {task.name} after {max_retries} attempts")

    async def _clone_repo(self, temp_dir: Path) -> None:
        await asyncio.to_thread(_clone_repo_local, self._git_transport.bare_repo_path, temp_dir)

    async def _fetch_ref(self, temp_dir: Path, ref: str) -> None:
        await asyncio.to_thread(_fetch_ref_local, temp_dir, ref)

    async def _force_push_fetched_commit(self, temp_dir: Path) -> None:
        await asyncio.to_thread(_reset_hard_local, temp_dir, "FETCH_HEAD")
        await self._push_resolved_main(temp_dir, force=True)

    async def _merge_fetched_commit(self, temp_dir: Path, task_name: str) -> bool:
        return await asyncio.to_thread(_merge_fetched_commit_local, temp_dir, task_name)

    async def _run_merge_agent(self, task: _SubmittedTask, temp_dir: Path, base_instruction: str) -> None:
        merge_workspace = Workspace(
            name=f"merge-{task.name}",
            path=temp_dir,
            tracked=False,
            mount_path=self._workspace.mount_path,
            backup=False,
        )
        merge_workspace.transport = RsyncTransport(
            str(temp_dir),
            self._git_transport.ssh_key_path,
            mount_path=self._workspace.mount_path,
        )
        runner = self._world.agent(
            self._merge_agent_config,
            display_name=f"merge-{task.name}",
            workspaces=[merge_workspace],
        )
        instruction = (
            f"{base_instruction}\n"
            f"Resolve the conflicts for task '{task.name}' in {self._workspace.mount_path}. "
            "When you are done, stage all resolved files and commit the merge."
        )
        await runner.run(instruction)

    async def _ensure_merge_complete(self, temp_dir: Path) -> None:
        unresolved = await asyncio.to_thread(_unmerged_files_local, temp_dir)
        if unresolved:
            raise RuntimeError(f"Merge agent left unresolved conflicts: {' '.join(unresolved)}")

        parent_count = await asyncio.to_thread(_head_parent_count, temp_dir)
        if parent_count < 2:
            raise RuntimeError("Merge agent did not create a merge commit")

    async def _push_resolved_main(self, temp_dir: Path, *, force: bool) -> None:
        await asyncio.to_thread(_push_main_local, temp_dir, force)

    async def _checkpoint_tracked_workspace(self, task: _SubmittedTask, published_ref: GitPublishedRef) -> None:
        if not self._workspace.tracked:
            return

        step_name = f"parallel_agents.{_slug(task.name)}.{published_ref.commit_sha[:12]}"
        await self._workspace.ensure_fuse_mount()
        await self._workspace.materialize_current_tree_into_overlay()
        logger.info("Checkpointing tracked world state at '%s'", step_name)
        await self._world.checkpoint(step_name)

    async def _delete_ref(self, temp_dir: Path, ref: str) -> None:
        deleted = await asyncio.to_thread(_delete_remote_ref_local, temp_dir, ref)
        if not deleted:
            logger.warning("Failed to delete ref %s", ref)

    async def _delete_ref_direct(self, ref: str) -> None:
        """Delete a ref from the bare repo without needing a temp clone."""
        deleted = await asyncio.to_thread(_delete_bare_ref_local, self._git_transport.bare_repo_path, ref)
        if not deleted:
            logger.warning("Failed to delete ref %s directly", ref)


@asynccontextmanager
async def _optional_lock(lock: asyncio.Lock | None):
    if lock is None:
        yield
        return
    async with lock:
        yield


@asynccontextmanager
async def _optional_semaphore(semaphore: asyncio.Semaphore | None):
    if semaphore is None:
        yield
        return
    async with semaphore:
        yield


def _slug(value: str) -> str:
    chars: list[str] = []
    for char in value.lower():
        if char.isalnum():
            chars.append(char)
        else:
            chars.append("-")
    return "".join(chars).strip("-") or "task"


def _repo(path: Path | str) -> Repo:
    trust_git_directory(path)
    return Repo(path)


def _rev_parse_ref(repo_path: str, ref: str) -> str:
    return _repo(repo_path).commit(ref).hexsha


def _clone_repo_local(bare_repo_path: str, temp_dir: Path) -> None:
    trust_git_directory(bare_repo_path)
    trust_git_directory(temp_dir)
    repo = Repo.clone_from(bare_repo_path, temp_dir)
    with repo.config_writer() as config:
        config.set_value("user", "email", AGENT_ACTOR.email)
        config.set_value("user", "name", AGENT_ACTOR.name)


def _fetch_ref_local(temp_dir: Path, ref: str) -> None:
    _repo(temp_dir).remote("origin").fetch(ref)


def _reset_hard_local(temp_dir: Path, ref: str) -> None:
    _repo(temp_dir).git.reset("--hard", ref)


def _merge_fetched_commit_local(temp_dir: Path, task_name: str) -> bool:
    repo = _repo(temp_dir)
    try:
        repo.git.merge("FETCH_HEAD", "-m", f"Merge parallel task {task_name}")
        return False
    except GitCommandError as exc:
        unresolved = _unmerged_files_local(temp_dir)
        if unresolved:
            return True
        raise RuntimeError(exc.stderr.strip() or exc.stdout.strip() or str(exc)) from exc


def _unmerged_files_local(temp_dir: Path) -> list[str]:
    return sorted(str(path) for path in _repo(temp_dir).index.unmerged_blobs().keys())


def _head_parent_count(temp_dir: Path) -> int:
    return len(_repo(temp_dir).head.commit.parents)


def _push_main_local(temp_dir: Path, force: bool) -> None:
    args = ["--porcelain"]
    if force:
        args.append("--force")
    args.extend(["origin", "HEAD:main"])
    _repo(temp_dir).git.push(*args)


def _delete_remote_ref_local(temp_dir: Path, ref: str) -> bool:
    try:
        _repo(temp_dir).git.push("--porcelain", "origin", f":{ref}")
        return True
    except GitCommandError:
        return False


def _delete_bare_ref_local(bare_repo_path: str, ref: str) -> bool:
    try:
        _repo(bare_repo_path).git.update_ref("-d", ref)
        return True
    except GitCommandError:
        return False
