"""Debug CUA agent."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

from use_computer.agents.base import BaseCUAAgent
from use_computer.agents.debug.actions import (
    desktop_replay_platform,
    dispatch_desktop_replay_action,
    run_desktop_debug_action,
    run_desktop_exec,
    run_realistic_exec,
)
from use_computer.agents.debug.models import (
    DESKTOP_ACTION_POOL,
    REAL_EXEC_SLEEP_SEC,
    REPLAY_DELAY_SEC,
    ReplayAction,
    load_replay_actions,
    rotating_actions,
)
from use_computer.core.sandbox import AsyncSandbox


class DebugCUAAgent(BaseCUAAgent):
    def __init__(
        self,
        *args,
        realistic: bool = False,
        replay: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.realistic = realistic
        self.replay = replay

    @staticmethod
    def name() -> str:
        return "debug-cua"

    async def pre_run(self, environment: Any) -> AsyncSandbox:
        return await super().pre_run(environment)

    async def _run_agent(
        self,
        instruction: str,
        environment: Any,
        context: Any,
    ) -> None:
        sandbox = await self.pre_run(environment)
        self.steps[0]["message"] = instruction

        if self.replay:
            await self._run_replay(sandbox)
            await self.post_run(context, "debug", "debug-cua-replay")
            return

        await self._run_smoke_steps(sandbox, environment)
        await self.post_run(context, "debug", "debug-cua")

    async def _run_smoke_steps(self, sandbox: AsyncSandbox, environment: Any) -> None:
        for step in range(1, self.max_steps + 1):
            if self.realistic:
                await self._realistic_desktop_step(sandbox, step)
            else:
                await self._minimal_desktop_step(sandbox, step)
            await self._fire_in_process(environment, step)
            if step < self.max_steps:
                await asyncio.sleep(1.0)

    async def _run_replay(self, sandbox: AsyncSandbox) -> None:

        platform = desktop_replay_platform(sandbox)
        await self._replay_actions(
            sandbox,
            platform=platform,
            actions=load_replay_actions(self.task_dir),
            dispatch=dispatch_desktop_replay_action,
        )

    async def _replay_actions(
        self,
        sandbox: AsyncSandbox,
        *,
        platform: str,
        actions: list[ReplayAction],
        dispatch: Callable[[Any, ReplayAction], Awaitable[None]],
    ) -> None:
        total = len(actions)
        self.logger.info(f"[replay-{platform}] replaying {total} action(s)")

        for index, action in enumerate(actions, start=1):
            if index > 1:
                await asyncio.sleep(REPLAY_DELAY_SEC)

            screenshot_path = await self._capture_replay_screenshot(sandbox, index)
            try:
                await dispatch(sandbox, action)
                self.logger.info(f"[replay-{platform}] {index}/{total} {action.label}")
            except Exception as exc:  # noqa: BLE001
                self.logger.warning(
                    f"[replay-{platform}] {index}/{total} {action.function} ERR: "
                    f"{type(exc).__name__}: {exc}"
                )
            self._append_replay_step(action, screenshot_path)

        await asyncio.sleep(REPLAY_DELAY_SEC)
        await self._capture_replay_screenshot(sandbox, total + 1)

    async def _capture_replay_screenshot(self, sandbox: AsyncSandbox, step: int) -> Path:
        screenshot = await sandbox.screenshot.take_full_screen()
        path = self.images_dir / f"step_{step:03d}.png"
        path.write_bytes(screenshot)
        return path

    def _append_replay_step(self, action: ReplayAction, screenshot_path: Path) -> None:
        try:
            rel_path = screenshot_path.relative_to(self.logs_dir.parent)
        except ValueError:
            rel_path = Path("agent/images") / screenshot_path.name

        self.steps.append(
            {
                "step_id": len(self.steps) + 1,
                "source": "agent",
                "message": f"[replay] {action.label}",
                "tool_calls": [
                    {
                        "function": action.function,
                        "args": action.args,
                        "arguments": json.dumps(action.args),
                    }
                ],
                "observation": {
                    "results": [
                        {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"step screenshot: {rel_path}",
                                },
                                {
                                    "type": "image",
                                    "source": {
                                        "media_type": "image/png",
                                        "path": str(rel_path),
                                    },
                                },
                            ]
                        }
                    ]
                },
            }
        )

    async def _minimal_desktop_step(self, sandbox: Any, step: int) -> None:
        screenshot = await sandbox.screenshot.take_full_screen()
        (self.images_dir / f"step_{step:03d}.png").write_bytes(screenshot)
        await sandbox.mouse.click(960, 540)
        result = await run_desktop_exec(sandbox, "echo hello world")
        self.logger.info(
            f"[debug] step={step}/{self.max_steps} screenshot={len(screenshot)}B exec={result}"
        )

    async def _realistic_desktop_step(self, sandbox: Any, step: int) -> None:
        screenshot = await sandbox.screenshot.take_full_screen()
        if self._should_persist_realistic_screenshot(step):
            (self.images_dir / f"step_{step:03d}.png").write_bytes(screenshot)

        actions = rotating_actions(DESKTOP_ACTION_POOL, step)
        executed = await self._run_desktop_actions(sandbox, actions)
        await self._run_realistic_exec(sandbox, step)

        self.logger.info(
            f"[debug-realistic] step={step}/{self.max_steps} "
            f"ss={len(screenshot)}B actions={','.join(executed)} "
            f"exec_sleep={REAL_EXEC_SLEEP_SEC}s"
        )

    def _should_persist_realistic_screenshot(self, step: int) -> bool:
        return step == 1 or step % 10 == 0 or step == self.max_steps

    async def _run_desktop_actions(self, sandbox: Any, actions: list[str]) -> list[str]:
        executed: list[str] = []
        for action in actions:
            try:
                await run_desktop_debug_action(sandbox, action, self.desktop.platform)
                executed.append(action)
            except Exception as exc:  # noqa: BLE001
                executed.append(f"{action}!err={type(exc).__name__}")
        return executed

    async def _run_realistic_exec(self, sandbox: Any, step: int) -> None:
        try:
            await run_realistic_exec(sandbox, step)
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(f"[debug-realistic] exec err: {type(exc).__name__}: {exc}")


DebugComputerAgent = DebugCUAAgent
