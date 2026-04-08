"""Shared queued agent execution for pooled parallel runs."""

from __future__ import annotations

import asyncio
import logging
import shutil
import tempfile
import uuid
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING

from git import Repo
from git.exc import GitCommandError

from plato.agents.mounts import AgentWorkspaceMount, GitCheckoutPolicy, GitSyncPolicy
from plato.agents.warmpool import WarmPool
from plato.git_ops.repo import trust_git_directory
from plato.runtimes.base import Runtime, RuntimeInfo
from plato.transports.git import GitPublishedRef, GitTransport
from plato.worlds.workspace import Workspace

if TYPE_CHECKING:
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
    ) -> None:
        if agent_config.max_parallel is None:
            raise ValueError("AgentExecutionManager requires agent_config.max_parallel")

        self._agent_config = agent_config
        self._world_runtime_info = world_runtime_info
        self._checkpoint = checkpoint
        self._primary_workspace = primary_workspace
        self._primary_mount = primary_mount
        self._warm_pool = WarmPool(
            runtime_factory=runtime_factory,
            image=agent_config.image,
            max_size=agent_config.max_parallel,
            pre_warm=0,
        )
        self._integration_lock = asyncio.Lock()

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

        if published_transport is not None and published_transport.published_ref is not None:
            await self._integrate_published_ref(
                task_name=task_name,
                published_ref=published_transport.published_ref,
            )
        return agent_id

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
            temp_dir = Path(tempfile.mkdtemp(prefix=f"merge-{task_name}-"))
            try:
                await asyncio.to_thread(_clone_repo_local, transport.bare_repo_path, temp_dir)
                await asyncio.to_thread(_fetch_ref_local, temp_dir, published_ref.ref)

                merge_conflicted = await asyncio.to_thread(_merge_fetched_commit_local, temp_dir, task_name)
                if merge_conflicted:
                    raise RuntimeError(f"Merge conflict integrating task {task_name}")

                await asyncio.to_thread(_push_main_local, temp_dir, False)
                await transport._refresh_local_workspace_from_main()
                await self._checkpoint_tracked_workspace(task_name, published_ref)
                await asyncio.to_thread(_delete_remote_ref_local, temp_dir, published_ref.ref)
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)

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
        config.set_value("user", "email", "agent@plato.dev")
        config.set_value("user", "name", "Plato Agent")


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
