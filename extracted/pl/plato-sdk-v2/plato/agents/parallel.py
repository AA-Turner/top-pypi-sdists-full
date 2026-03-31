"""Parallel agent orchestration for git-transported workspaces."""

from __future__ import annotations

import asyncio
import logging
import shlex
import shutil
import tempfile
import uuid
from collections.abc import Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from plato.agents.runtime.transport import GitPublishedRef, GitTransport, RsyncTransport
from plato.utils.subprocess import run_local
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
    ) -> None:
        if not isinstance(workspace.transport, GitTransport):
            raise ValueError("ParallelAgentOrchestrator requires a git-transported workspace")
        if max_parallel < 1:
            raise ValueError("max_parallel must be at least 1")

        self._world = world
        self._workspace = workspace
        self._git_transport = workspace.transport
        self._agent_config = agent_config
        self._merge_agent_config = merge_agent_config or agent_config
        self._semaphore = asyncio.Semaphore(max_parallel)
        self._extra_workspaces: list[Workspace] = extra_workspaces or []
        self._tasks: list[_SubmittedTask] = []

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

        integration_queue: asyncio.Queue[_QueuedIntegration | None] = asyncio.Queue()
        integration_worker = asyncio.create_task(self._integration_worker(integration_queue))
        try:
            pending = [asyncio.create_task(self._run_task(task, integration_queue)) for task in self._tasks]
            return await asyncio.gather(*pending)
        finally:
            await integration_queue.put(None)
            await integration_worker

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

        try:
            async with self._semaphore:
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
                )
                agent_id = await runner.run(task.instruction)
        except Exception as exc:
            return ParallelAgentResult(
                name=task.name,
                status="failed",
                error=str(exc),
            )

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
        publish_prefix = f"refs/plato/tasks/{_slug(task.name)}-{uuid.uuid4().hex}"
        task_transport = self._git_transport.with_path(self._git_transport.path)
        task_transport.mount_path = self._workspace.mount_path
        task_transport.set_publish_ref_prefix(publish_prefix)

        task_workspace = self._workspace.clone()
        task_workspace.transport = task_transport
        return task_workspace, task_transport

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
        bare_repo = shlex.quote(self._git_transport.bare_repo_path)
        target = shlex.quote(str(temp_dir))
        await _run_local_checked(f"git clone {bare_repo} {target}")
        await _run_local_checked(
            "git config user.email plato@plato.dev && git config user.name Plato",
            cwd=temp_dir,
        )

    async def _fetch_ref(self, temp_dir: Path, ref: str) -> None:
        await _run_local_checked(
            f"git fetch origin {shlex.quote(ref)}",
            cwd=temp_dir,
        )

    async def _force_push_fetched_commit(self, temp_dir: Path) -> None:
        await _run_local_checked("git reset --hard FETCH_HEAD", cwd=temp_dir)
        await self._push_resolved_main(temp_dir, force=True)

    async def _merge_fetched_commit(self, temp_dir: Path, task_name: str) -> bool:
        exit_code, _, stderr = await run_local(
            f"cd {shlex.quote(str(temp_dir))} && git merge FETCH_HEAD -m {shlex.quote(f'Merge parallel task {task_name}')}",
            timeout=60,
        )
        if exit_code == 0:
            return False

        unresolved = await _run_local_checked(
            "git diff --name-only --diff-filter=U",
            cwd=temp_dir,
        )
        if not unresolved.strip():
            raise RuntimeError(stderr.strip() or f"git merge failed for task {task_name}")
        return True

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
        unresolved = await _run_local_checked("git diff --name-only --diff-filter=U", cwd=temp_dir)
        if unresolved.strip():
            raise RuntimeError(f"Merge agent left unresolved conflicts: {unresolved.strip()}")

        parents = (await _run_local_checked("git rev-list --parents -n 1 HEAD", cwd=temp_dir)).split()
        if len(parents) < 3:
            raise RuntimeError("Merge agent did not create a merge commit")

    async def _push_resolved_main(self, temp_dir: Path, *, force: bool) -> None:
        push_flag = "--force " if force else ""
        await _run_local_checked(f"git push {push_flag}origin HEAD:main", cwd=temp_dir)

    async def _checkpoint_tracked_workspace(self, task: _SubmittedTask, published_ref: GitPublishedRef) -> None:
        if not self._workspace.tracked:
            return

        step_name = f"parallel_agents.{_slug(task.name)}.{published_ref.commit_sha[:12]}"
        await self._workspace.ensure_fuse_mount()
        await self._workspace.materialize_current_tree_into_overlay()
        logger.info("Checkpointing tracked world state at '%s'", step_name)
        await self._world.checkpoint(step_name)

    async def _delete_ref(self, temp_dir: Path, ref: str) -> None:
        exit_code, _, _ = await run_local(
            f"cd {shlex.quote(str(temp_dir))} && git push origin :{shlex.quote(ref)}",
            timeout=30,
        )
        if exit_code != 0:
            logger.warning("Failed to delete hidden ref %s", ref)


@asynccontextmanager
async def _optional_lock(lock: asyncio.Lock | None):
    if lock is None:
        yield
        return
    async with lock:
        yield


def _slug(value: str) -> str:
    chars: list[str] = []
    for char in value.lower():
        if char.isalnum():
            chars.append(char)
        else:
            chars.append("-")
    return "".join(chars).strip("-") or "task"


async def _run_local_checked(command: str, *, cwd: Path | None = None) -> str:
    prefix = ""
    if cwd is not None:
        prefix = f"cd {shlex.quote(str(cwd))} && "
    exit_code, stdout, stderr = await run_local(prefix + command, timeout=60)
    if exit_code != 0:
        raise RuntimeError(stderr.strip() or stdout.strip() or f"Command failed: {command}")
    return stdout
