"""OpenAI CUA agent — GPT computer-use via Responses API."""

from __future__ import annotations

import base64
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Any, cast

import openai

from use_computer.agents.base import (
    BaseCUAAgent,
    ComputerSandbox,
    build_system_prompt,
    execute_action,
    load_prompt,
)
from use_computer.agents.types import DesktopAction, ScrollDirection

DEFAULT_OPENAI_COMPUTER_MODEL = "gpt-5.5"
LEGACY_OPENAI_COMPUTER_MODEL = "computer-use-preview"


class OpenAIToolType(str, Enum):
    COMPUTER = "computer"
    COMPUTER_USE_PREVIEW = "computer_use_preview"


class OpenAIItemType(str, Enum):
    COMPUTER_CALL = "computer_call"
    COMPUTER_CALL_OUTPUT = "computer_call_output"
    COMPUTER_SCREENSHOT = "computer_screenshot"
    INPUT_IMAGE = "input_image"
    MESSAGE = "message"
    OUTPUT_TEXT = "output_text"


@dataclass(frozen=True)
class OpenAIComputerObservation:
    call_id: str
    screenshot_b64: str
    pending_safety_checks: tuple[dict[str, Any], ...] = ()

    def to_input_item(self) -> dict[str, Any]:
        item: dict[str, Any] = {
            "type": OpenAIItemType.COMPUTER_CALL_OUTPUT.value,
            "call_id": self.call_id,
            "output": {
                "type": OpenAIItemType.COMPUTER_SCREENSHOT.value,
                "image_url": f"data:image/png;base64,{self.screenshot_b64}",
            },
        }
        if self.pending_safety_checks:
            item["acknowledged_safety_checks"] = list(self.pending_safety_checks)
        return item


class OpenAICUAAgent(BaseCUAAgent):
    @staticmethod
    def name() -> str:
        return "openai-cua"

    async def _run_agent(
        self,
        instruction: str,
        environment: Any,
        context: Any,
    ) -> None:
        sandbox = cast(ComputerSandbox, await self.pre_run(environment))
        self.steps[0]["message"] = instruction

        client = openai.OpenAI()
        model = self._parsed_model_name or DEFAULT_OPENAI_COMPUTER_MODEL

        system = build_system_prompt(
            load_prompt("openai.txt"),
            self.screen_width,
            self.screen_height,
            os_type=self.desktop.os_type,
            os_article=self.desktop.article,
            platform_notes=self.desktop.notes,
        )

        # Initial screenshot
        ss = await sandbox.screenshot.take_full_screen()
        (self.images_dir / "step_000.png").write_bytes(ss)

        tools = _openai_tools_for_model(
            model,
            width=self.screen_width,
            height=self.screen_height,
            environment=self.desktop.openai_environment.value,
        )

        ss_b64 = base64.b64encode(ss).decode()
        input_items: list[Any] = [
            {"role": "system", "content": system},
            {"role": "user", "content": instruction},
            {
                "role": "user",
                "content": [
                    {
                        "type": OpenAIItemType.INPUT_IMAGE.value,
                        "image_url": f"data:image/png;base64,{ss_b64}",
                    }
                ],
            },
        ]
        previous_response_id: str | None = None

        for step_idx in range(self.max_steps):
            await self._fire_in_process(environment, step_idx)
            response = client.responses.create(
                **_response_create_kwargs(
                    model,
                    tools=tools,
                    input_items=input_items,
                    previous_response_id=previous_response_id,
                )
            )
            previous_response_id = response.id

            self.total_in += response.usage.input_tokens if response.usage else 0
            self.total_out += response.usage.output_tokens if response.usage else 0

            computer_calls = [
                item
                for item in response.output
                if getattr(item, "type", None) == OpenAIItemType.COMPUTER_CALL.value
            ]

            if not computer_calls:
                self.steps.append(
                    {
                        "step_id": len(self.steps) + 1,
                        "source": "agent",
                        "message": _response_text(response) or "Task complete.",
                    }
                )
                break

            input_items = []
            for call in computer_calls:
                last_screenshot: bytes | None = None
                for action in _openai_actions(call):
                    mapped = _map_openai_action(action)

                    result_text, ss_bytes, ss_path = await execute_action(
                        sandbox,
                        mapped,
                        self.images_dir,
                        len(self.steps),
                        key_aliases=self.desktop_key_aliases,
                    )

                    step_data: dict[str, Any] = {
                        "step_id": len(self.steps) + 1,
                        "source": "agent",
                        "tool_calls": [
                            {
                                "tool_call_id": call.call_id,
                                "function_name": action.type,
                                "arguments": mapped,
                            }
                        ],
                    }
                    if ss_path:
                        step_data["observation"] = {
                            "results": [
                                {
                                    "content": [
                                        {"type": "text", "text": result_text},
                                        {
                                            "type": "image",
                                            "source": {
                                                "media_type": "image/png",
                                                "path": ss_path,
                                            },
                                        },
                                    ],
                                }
                            ],
                        }
                    self.steps.append(step_data)
                    self.checkpoint(context, model, "openai-cua")
                    if ss_bytes:
                        last_screenshot = ss_bytes

                if last_screenshot:
                    input_items.append(
                        OpenAIComputerObservation(
                            call_id=call.call_id,
                            screenshot_b64=base64.b64encode(last_screenshot).decode(),
                            pending_safety_checks=_pending_safety_checks(call),
                        ).to_input_item()
                    )

            if not input_items:
                break

        await self.post_run(context, model, "openai-cua")


OpenAIComputerAgent = OpenAICUAAgent


def _openai_tools_for_model(
    model: str,
    *,
    width: int,
    height: int,
    environment: str,
) -> list[dict[str, Any]]:
    if _uses_legacy_preview_tool(model):
        return [
            {
                "type": OpenAIToolType.COMPUTER_USE_PREVIEW.value,
                "display_width": width,
                "display_height": height,
                "environment": environment,
            }
        ]
    return [{"type": OpenAIToolType.COMPUTER.value}]


def _response_create_kwargs(
    model: str,
    *,
    tools: list[dict[str, Any]],
    input_items: list[Any],
    previous_response_id: str | None,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "model": model,
        "tools": tools,
        "input": input_items,
    }
    if previous_response_id is not None:
        kwargs["previous_response_id"] = previous_response_id
    if _uses_legacy_preview_tool(model):
        kwargs["truncation"] = "auto"
    return kwargs


def _uses_legacy_preview_tool(model: str) -> bool:
    return model in {LEGACY_OPENAI_COMPUTER_MODEL, "computer-use-preview-2025-03-11"}


def _openai_actions(call: Any) -> list[Any]:
    actions = getattr(call, "actions", None)
    if isinstance(actions, Iterable) and not isinstance(actions, (str, bytes)):
        return list(actions)
    action = getattr(call, "action", None)
    return [action] if action is not None else []


def _pending_safety_checks(call: Any) -> tuple[dict[str, Any], ...]:
    checks = getattr(call, "pending_safety_checks", None)
    if not isinstance(checks, Iterable) or isinstance(checks, (str, bytes)):
        return ()
    normalized = []
    for check in checks:
        if hasattr(check, "model_dump"):
            normalized.append(check.model_dump(exclude_none=True))
        elif isinstance(check, dict):
            normalized.append({k: v for k, v in check.items() if v is not None})
    return tuple(normalized)


def _response_text(response: Any) -> str:
    output_text = getattr(response, "output_text", "")
    if isinstance(output_text, str) and output_text:
        return output_text

    text_parts = []
    for item in getattr(response, "output", []):
        if getattr(item, "type", None) != OpenAIItemType.MESSAGE.value:
            continue
        content = getattr(item, "content", None)
        if isinstance(content, Iterable) and not isinstance(content, (str, bytes)):
            for block in content:
                if getattr(block, "type", None) == OpenAIItemType.OUTPUT_TEXT.value:
                    text = getattr(block, "text", "")
                    if text:
                        text_parts.append(text)
        else:
            text = getattr(item, "text", "")
            if text:
                text_parts.append(text)
    return "\n".join(text_parts)


def _map_openai_action(action: Any) -> dict[str, Any]:
    """Map OpenAI computer actions to our standard format."""
    action_type = action.type

    type_map = {
        "keypress": DesktopAction.KEY,
        "move": DesktopAction.MOVE,
        "click": DesktopAction.CLICK,
        "double_click": DesktopAction.DOUBLE_CLICK,
        "drag": DesktopAction.DRAG,
        "screenshot": DesktopAction.SCREENSHOT,
        "type": DesktopAction.TYPE,
        "scroll": DesktopAction.SCROLL,
        "wait": DesktopAction.WAIT,
    }
    mapped_action = type_map.get(action_type)
    mapped: dict[str, Any] = {"action": mapped_action.value if mapped_action else action_type}

    if hasattr(action, "x") and hasattr(action, "y"):
        x = getattr(action, "x", None)
        y = getattr(action, "y", None)
        if x is not None and y is not None:
            mapped["coordinate"] = [x, y]

    if hasattr(action, "keys") and action.keys:
        mapped["key"] = "+".join(action.keys)

    if hasattr(action, "text") and action.text:
        mapped["text"] = action.text

    if hasattr(action, "scroll_x"):
        sx = getattr(action, "scroll_x", 0) or 0
        sy = getattr(action, "scroll_y", 0) or 0
        if sy < 0:
            mapped["direction"] = ScrollDirection.DOWN.value
            mapped["amount"] = abs(sy)
        elif sy > 0:
            mapped["direction"] = ScrollDirection.UP.value
            mapped["amount"] = sy
        elif sx < 0:
            mapped["direction"] = ScrollDirection.LEFT.value
            mapped["amount"] = abs(sx)
        else:
            mapped["direction"] = ScrollDirection.RIGHT.value
            mapped["amount"] = abs(sx) or 3

    if hasattr(action, "start_x") and action.start_x is not None:
        mapped["start_coordinate"] = [action.start_x, action.start_y]
        if hasattr(action, "x"):
            mapped["coordinate"] = [action.x, action.y]

    if hasattr(action, "path") and action.path:
        path = action.path
        start = path[0]
        end = path[-1]
        mapped["start_coordinate"] = [start.x, start.y]
        mapped["coordinate"] = [end.x, end.y]

    if hasattr(action, "button") and action.button == "right":
        mapped["action"] = DesktopAction.RIGHT_CLICK.value

    return mapped
