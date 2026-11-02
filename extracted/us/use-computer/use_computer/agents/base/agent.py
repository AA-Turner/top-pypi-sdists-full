"""Base CUA agent lifecycle."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any, cast

from use_computer.agents.base.artifacts import ArtifactCaptureMixin
from use_computer.agents.base.desktop import (
    DesktopProfile,
    OpenAIComputerEnvironment,
    desktop_profile,
)
from use_computer.agents.base.final_state import FinalStateMixin
from use_computer.agents.base.recordings import RecordingMixin
from use_computer.agents.base.sandbox import ComputerSandbox
from use_computer.agents.base.task_setup import run_task_setup, task_dir_from_env
from use_computer.agents.base.trajectory import write_trajectory
from use_computer.agents.core import (
    AgentRunOptions,
    AgentRunResult,
    AgentUsage,
    DirectAgentContext,
    DirectSandboxEnvironment,
)
from use_computer.agents.types import Platform
from use_computer.core.sandbox import AsyncSandbox


def _task_dir_from_env(environment: Any) -> Path:
    """Pull the task dir from the environment."""
    p = task_dir_from_env(environment)
    if p is None:
        raise RuntimeError(
            "environment exposes neither task_dir nor task environment_dir; "
            "agent can't locate the task directory"
        )
    return p


class BaseCUAAgent(RecordingMixin, FinalStateMixin, ArtifactCaptureMixin):
    """Shared init/setup for all CUA agents."""

    SUPPORTS_ATIF = True

    def __init__(
        self,
        logs_dir: Path | str | None = None,
        model_name: str | None = None,
        model: str | None = None,
        logger: logging.Logger | None = None,
        max_steps: int = 50,
        screen_width: int = 1920,
        screen_height: int = 1080,
        task_dir: str | Path | None = None,
        platform: Platform | str | None = None,
        os_type: str | None = None,
        platform_notes: str | None = None,
        openai_environment: OpenAIComputerEnvironment | str | None = None,
        save_on_finish: bool | str = False,
        recording_enabled: bool | str = True,
        final_state_enabled: bool | str = True,
        **kwargs: Any,
    ):
        self.logs_dir = Path(logs_dir or "runs/agent").resolve()
        self.model_name = model_name or model
        self.logger = logger or logging.getLogger("use_computer.agents")
        self.mcp_servers = kwargs.get("mcp_servers") or []
        self.skills_dir = kwargs.get("skills_dir")
        self._init_model_info()
        self.max_steps = max_steps
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._desktop_platform = platform
        self._desktop_os_type = os_type
        self._desktop_platform_notes = platform_notes
        self._desktop_openai_environment = openai_environment
        self.save_on_finish = _as_bool(save_on_finish)
        self.desktop = self._desktop_profile_for(platform or Platform.MACOS)
        self.task_dir: Path | None = Path(task_dir) if task_dir else None
        self._recording_id: str | None = None
        self.recording_enabled = _as_bool(recording_enabled)
        self.final_state_enabled = _as_bool(final_state_enabled)
        self.sandbox: AsyncSandbox | None = None
        self.images_dir: Path = (self.logs_dir / "images").resolve()
        self.steps: list[dict[str, Any]] = []
        self.total_in = 0
        self.total_out = 0

    def _init_model_info(self) -> None:
        self._parsed_model_provider = None
        self._parsed_model_name = None
        if self.model_name is None:
            return
        if "/" in self.model_name:
            self._parsed_model_provider, self._parsed_model_name = self.model_name.split(
                "/", maxsplit=1
            )
            return
        self._parsed_model_name = self.model_name

    @property
    def desktop_key_aliases(self) -> dict[str, str] | None:
        return dict(self.desktop.key_aliases) if self.desktop.key_aliases else None

    def _desktop_profile_for(self, platform: Platform | str) -> DesktopProfile:
        return desktop_profile(
            platform,
            os_type=self._desktop_os_type,
            platform_notes=self._desktop_platform_notes,
            openai_environment=self._desktop_openai_environment,
        )

    def _bind_desktop_profile(self, environment: Any) -> None:
        platform = self._desktop_platform or getattr(environment, "_platform", None)
        self.desktop = self._desktop_profile_for(platform or Platform.MACOS)

    @staticmethod
    def name() -> str:
        return "cua"

    def version(self) -> str | None:
        return "1.0.0"

    async def setup(self, environment: Any) -> None:
        await run_task_setup(environment, self.logger)

    async def run(
        self,
        instruction: str,
        environment: Any | None = None,
        context: Any | None = None,
        *,
        sandbox: AsyncSandbox | None = None,
        logs_dir: str | Path | None = None,
        task_dir: str | Path | None = None,
        platform: Platform | str = Platform.MACOS,
        max_steps: int | None = None,
        fire_in_process=None,
    ) -> AgentRunResult | None:
        """Run directly with a sandbox, or through an environment/context adapter."""
        if sandbox is not None:
            return await self.run_direct(
                instruction,
                sandbox,
                logs_dir=logs_dir,
                task_dir=task_dir,
                platform=platform,
                max_steps=max_steps,
                fire_in_process=fire_in_process,
            )
        if environment is None or context is None:
            raise TypeError("run() requires either sandbox=... or environment and context")
        await self._run_agent(instruction, environment, context)
        return None

    async def _run_agent(self, instruction: str, environment: Any, context: Any) -> None:
        raise NotImplementedError

    async def pre_run(self, environment: Any) -> AsyncSandbox:
        """Common setup: bind sandbox/profile, start recording, create images dir."""
        sandbox: AsyncSandbox | None = getattr(environment, "sandbox", None)
        if sandbox is None:
            raise RuntimeError("CUA agents require an environment with a .sandbox property")
        self.sandbox = sandbox
        self._bind_desktop_profile(environment)
        if self.task_dir is None:
            self.task_dir = _task_dir_from_env(environment)
            self.logger.info(f"task_dir={self.task_dir}")
        if self.recording_enabled:
            await self.start_recording(sandbox)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.steps = [{"step_id": 1, "source": "user", "message": ""}]
        self.total_in = 0
        self.total_out = 0
        return sandbox

    async def _fire_in_process(self, environment: Any, step_idx: int) -> None:
        """Fire in_process dialog if the environment supports it and step matches."""
        fn = getattr(environment, "fire_in_process", None)
        if fn:
            await fn(step_idx)

    def checkpoint(self, context: Any, model: str, agent_name: str) -> None:
        """Persist trajectory and update context token fields."""
        write_trajectory(
            self.logs_dir, self.steps, self.total_in, self.total_out, model, agent_name
        )
        context.n_input_tokens = self.total_in
        context.n_output_tokens = self.total_out
        context.n_cache_tokens = getattr(self, "_total_cache_read", 0) + getattr(
            self, "_total_cache_write", 0
        )

    async def post_run(self, context: Any, model: str, agent_name: str) -> None:
        """Common teardown: stop recording, write trajectory, set token counts."""
        assert self.sandbox is not None
        if self.save_on_finish:
            await self._save_focused_app(self.sandbox)
        if self.final_state_enabled:
            await self._save_final_ax_tree(self.sandbox)
            await self._log_final_state_metrics(self.sandbox)
        await self._capture_artifacts(context)
        if self.recording_enabled:
            await self.stop_recording(self.sandbox)
        self.checkpoint(context, model, agent_name)

    async def run_direct(
        self,
        instruction: str,
        sandbox: AsyncSandbox,
        *,
        logs_dir: str | Path | None = None,
        task_dir: str | Path | None = None,
        platform: Platform | str = Platform.MACOS,
        max_steps: int | None = None,
        fire_in_process=None,
    ) -> AgentRunResult:
        """Run against an AsyncSandbox without Harbor."""
        resolved_logs_dir = Path(logs_dir).resolve() if logs_dir else self.logs_dir
        resolved_task_dir = (
            Path(task_dir).resolve() if task_dir else self.task_dir or resolved_logs_dir / "task"
        )
        options = AgentRunOptions(
            logs_dir=resolved_logs_dir,
            task_dir=resolved_task_dir,
            platform=str(platform),
            max_steps=max_steps,
            fire_in_process=fire_in_process,
        )
        self.logs_dir = options.logs_dir
        self.images_dir = (self.logs_dir / "images").resolve()
        self.task_dir = options.task_dir
        if options.max_steps is not None:
            self.max_steps = options.max_steps
        environment = DirectSandboxEnvironment(
            sandbox,
            task_dir=options.task_dir,
            platform=options.platform,
            fire_in_process=options.fire_in_process,
            logger=self.logger,
        )
        context = DirectAgentContext()
        await self._run_agent(instruction, environment, context)
        return AgentRunResult(
            steps=list(self.steps),
            usage=AgentUsage(
                input_tokens=context.n_input_tokens,
                output_tokens=context.n_output_tokens,
                cache_tokens=context.n_cache_tokens,
            ),
            final_message=_final_message(self.steps),
        )

    async def _save_focused_app(self, sandbox: AsyncSandbox) -> None:
        shortcut = "command+s"
        computer = cast(ComputerSandbox, sandbox)
        await computer.keyboard.hotkey(shortcut)
        await asyncio.sleep(1)


def _as_bool(value: bool | str) -> bool:
    if isinstance(value, bool):
        return value
    return value.lower() in {"1", "true", "yes", "on"}


def _final_message(steps: list[dict[str, Any]]) -> str:
    for step in reversed(steps):
        message = step.get("message")
        if isinstance(message, str) and message:
            return message
    return ""
