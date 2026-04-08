"""Generic packaged world used for runtime-launched SDK integration tests."""

from __future__ import annotations

import asyncio
import json
import logging
import re
from pathlib import Path
from typing import cast

from pydantic import Field

from plato.worlds.base import BaseWorld, ResolvedWorkspaceRepo, register_world
from plato.worlds.config import RunConfig
from plato.worlds.models import Observation, StepResult, WorldState
from plato.worlds.testing.spec import (
    JsonValue,
    LoadedWorldTestSpec,
    WorldTestRunResult,
    WorldWorkspaceSpec,
    call_world_test_hook,
    load_world_test_spec,
)
from plato.worlds.workspace import Workspace

logger = logging.getLogger(__name__)


class HarnessWorldConfig(RunConfig):
    """Config for the generic runtime-launched test harness world."""

    test_spec_path: str = Field(description="Path to the serialized world test spec JSON.")
    result_path: str = Field(
        default="/tmp/plato-world-test-result.json",
        description="Path where the harness world writes structured test results.",
    )


class HarnessWorldState(WorldState):
    """Generic state model for injected world tests."""

    counter: int = 0
    model_config = {"extra": "allow"}


class WorldTestHarnessWorld(BaseWorld[HarnessWorldConfig, HarnessWorldState]):
    """A generic world that executes cloudpickled reset/step/close hooks."""

    name = "test-harness"
    description = "Generic harness world for runtime-launched SDK tests"

    def __init__(self) -> None:
        super().__init__()
        self.lifecycle: list[str] = []
        self.test_result: object | None = None
        self._loaded_spec: LoadedWorldTestSpec | None = None
        self._workspace_specs: dict[str, WorldWorkspaceSpec] = {}

    async def reset(self) -> Observation:
        spec = self._spec()
        result = await call_world_test_hook(spec.reset, self)
        if result is None:
            return Observation()
        if not isinstance(result, Observation):
            raise TypeError(f"reset hook must return Observation or None, got {type(result).__name__}")
        return result

    async def step(self) -> StepResult:
        spec = self._spec()
        result = await call_world_test_hook(spec.step, self)
        if result is None:
            return StepResult(observation=Observation(), done=True)
        if not isinstance(result, StepResult):
            raise TypeError(f"step hook must return StepResult, got {type(result).__name__}")
        return result

    async def close(self) -> None:
        spec = self._spec_optional()
        try:
            if spec is not None:
                await call_world_test_hook(spec.close, self)
        finally:
            await self._write_result()

    def workspace_repo_name(self, field_name: str) -> str:
        spec_name = "default"
        spec = self._spec_optional()
        if spec is not None:
            spec_name = _slug(spec.name)
        return f"{self.name}/{spec_name}/{field_name}"

    async def _init_declared_workspaces(self) -> None:
        spec = self._spec()
        if not spec.workspaces:
            return

        state_root = Path(self.config.state.path)
        self._workspace_specs = {workspace.name: workspace for workspace in spec.workspaces}

        for workspace_spec in spec.workspaces:
            workspace_root = state_root / (workspace_spec.relative_path or workspace_spec.name)
            workspace_root.mkdir(parents=True, exist_ok=True)

            repo_info = (
                await self._resolve_workspace_repo_by_name(self.workspace_repo_name(workspace_spec.name))
                if workspace_spec.tracked
                else _empty_repo_info()
            )

            workspace = Workspace(
                name=workspace_spec.name,
                path=workspace_root,
                tracked=workspace_spec.tracked,
                mount_path=workspace_spec.mount_path,
                dvcignore=workspace_spec.dvcignore,
                s3_bucket=repo_info.s3_bucket,
                s3_prefix=repo_info.s3_prefix,
                repo_id=repo_info.repo_id,
                repo_name=repo_info.repo_name,
                chronos_url=repo_info.chronos_url,
                api_key=repo_info.api_key,
                session_id=self.chronos.session_id if self.chronos else "",
            )
            await workspace.init()
            self._workspaces[workspace_spec.name] = workspace
            logger.debug(
                "Harness workspace '%s' at %s (tracked=%s, mount_path=%s)",
                workspace_spec.name,
                workspace_root,
                workspace_spec.tracked,
                workspace.mount_path,
            )

    async def _setup_workspaces(self) -> None:
        if not self._workspaces:
            return

        await asyncio.gather(*(workspace.ensure_fuse_mount() for workspace in self._workspaces.values()))

        if self._runtime_info is None:
            return

        runtime_info = self._runtime_info
        nfs_workspaces: list[Workspace] = []
        sshfs_workspaces: list[Workspace] = []
        git_workspaces: list[tuple[Workspace, WorldWorkspaceSpec]] = []

        for workspace in self._workspaces.values():
            workspace_spec = self._workspace_specs.get(workspace.name)
            if workspace_spec is None:
                nfs_workspaces.append(workspace)
                continue
            if workspace_spec.transport == "git":
                git_workspaces.append((workspace, workspace_spec))
            elif self.config.transport_mode == "sshfs" or workspace_spec.transport == "sshfs":
                sshfs_workspaces.append(workspace)
            else:
                nfs_workspaces.append(workspace)

        async def setup_git(workspace: Workspace, workspace_spec: WorldWorkspaceSpec) -> None:
            await workspace.setup_transport(
                runtime_info,
                marker_transport="git",
                git_config=workspace_spec.git_config,
            )

        async def setup_sshfs(workspace: Workspace) -> None:
            await workspace.setup_transport(
                runtime_info,
                transport_mode="sshfs",
            )

        parallel_tasks = [setup_git(workspace, workspace_spec) for workspace, workspace_spec in git_workspaces]
        parallel_tasks.extend(setup_sshfs(workspace) for workspace in sshfs_workspaces)

        nfs_server = None
        for export_fsid, workspace in enumerate(nfs_workspaces):
            nfs_server = await workspace.setup_transport(
                runtime_info,
                transport_mode="nfs_kernel",
                nfs_server=nfs_server,
                export_fsid=export_fsid,
            )

        if parallel_tasks and nfs_server is not None:
            await asyncio.gather(nfs_server.refresh_exports(), *parallel_tasks)
        elif nfs_server is not None:
            await nfs_server.refresh_exports()
        elif parallel_tasks:
            await asyncio.gather(*parallel_tasks)

    def _spec(self) -> LoadedWorldTestSpec:
        if self._loaded_spec is None:
            self._loaded_spec = load_world_test_spec(Path(self.config.test_spec_path))
        return self._loaded_spec

    def _spec_optional(self) -> LoadedWorldTestSpec | None:
        if self._loaded_spec is not None:
            return self._loaded_spec
        test_spec_path = getattr(self.config, "test_spec_path", "")
        if not test_spec_path:
            return None
        self._loaded_spec = load_world_test_spec(Path(test_spec_path))
        return self._loaded_spec

    async def _write_result(self) -> None:
        result_path = Path(self.config.result_path)
        result_path.parent.mkdir(parents=True, exist_ok=True)
        spec = self._spec_optional()

        result = WorldTestRunResult(
            name=spec.name if spec is not None else self.name,
            step_count=self._step_count,
            lifecycle=list(self.lifecycle),
            workspace_repo_names={name: self.workspace_repo_name(name) for name in self._workspaces},
            test_result=_normalize_json(getattr(self, "test_result", None)),
            final_result=_normalize_json(getattr(self, "_final_result", None)),
        )
        result_path.write_text(result.model_dump_json(indent=2) + "\n", encoding="utf-8")


def _empty_repo_info() -> ResolvedWorkspaceRepo:
    return ResolvedWorkspaceRepo(
        s3_bucket="",
        s3_prefix="",
        repo_id="",
        commit_ref="",
        repo_name="",
        chronos_url="",
        api_key="",
    )


def _normalize_json(value: object) -> JsonValue:
    return cast(JsonValue, json.loads(json.dumps(value, default=str)))


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9_-]+", "-", value.lower()).strip("-")
    return slug or "world-test"


register_world("plato-world-test-harness")(cast(type[BaseWorld], WorldTestHarnessWorld))
