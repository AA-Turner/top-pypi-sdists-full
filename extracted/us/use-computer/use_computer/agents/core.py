"""Direct agent run primitives."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from use_computer.core.sandbox import AsyncSandbox


@dataclass
class AgentRunOptions:
    logs_dir: Path
    task_dir: Path | None = None
    platform: str = "macos"
    max_steps: int | None = None
    fire_in_process: Callable[[int], Awaitable[None]] | None = None


@dataclass
class AgentUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_tokens: int = 0


@dataclass
class AgentRunResult:
    steps: list[dict[str, Any]]
    usage: AgentUsage
    final_message: str = ""


@dataclass
class DirectAgentContext:
    n_input_tokens: int = 0
    n_output_tokens: int = 0
    n_cache_tokens: int = 0


class DirectSandboxEnvironment:
    """Small environment adapter used when running agents without Harbor."""

    def __init__(
        self,
        sandbox: AsyncSandbox,
        *,
        task_dir: Path | None,
        platform: str,
        fire_in_process: Callable[[int], Awaitable[None]] | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.sandbox = sandbox
        self.task_dir = task_dir
        self._task_dir = task_dir
        self._platform = platform
        self.logger = logger or logging.getLogger("use_computer.agents")
        self._fire_in_process = fire_in_process

    async def fire_in_process(self, step: int) -> None:
        if self._fire_in_process is not None:
            await self._fire_in_process(step)
