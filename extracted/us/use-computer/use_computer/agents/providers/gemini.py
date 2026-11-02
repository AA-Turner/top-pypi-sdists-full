"""Gemini CUA agent — Google's computer-use tool via google-genai SDK.

Converts Gemini's normalized (0-999) coordinate actions into our standard
action format for execution via the SDK, following the same BaseCUAAgent
pattern as the Anthropic and OpenAI agents.
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from typing import Any, cast

from google import genai
from google.genai import types
from google.genai.types import (
    Content,
    FunctionResponse,
    FunctionResponseBlob,
    FunctionResponsePart,
    Part,
)

from use_computer.agents.base import (
    BaseCUAAgent,
    ComputerSandbox,
    build_system_prompt,
    execute_action,
    load_prompt,
)
from use_computer.agents.types import DesktopAction, DesktopCommand, Point, ScrollDirection

logger = logging.getLogger(__name__)

API_RETRY_TIMES = 5
API_RETRY_INTERVAL = 5
DEFAULT_GEMINI_COMPUTER_USE_MODEL = "gemini-2.5-computer-use-preview-10-2025"

# Browser-only actions that don't apply to desktop VMs
_EXCLUDED_ACTIONS = ["navigate", "go_back", "go_forward", "open_web_browser", "search"]


def _denormalize(coord: int, screen_dim: int) -> int:
    """Convert Gemini's 0-999 normalized coordinate to pixel coordinate."""
    return int(coord / 1000 * screen_dim)


def _map_gemini_action(
    name: str, args: dict, screen_w: int, screen_h: int
) -> dict[str, Any] | None:
    """Convert a Gemini function call into our standard action dict."""
    x = _denormalize(args.get("x", 0), screen_w)
    y = _denormalize(args.get("y", 0), screen_h)

    if name == "click_at":
        return DesktopCommand.create(DesktopAction.CLICK, coordinate=Point(x, y)).to_mapping()

    if name == "double_click_at":
        return DesktopCommand.create(
            DesktopAction.DOUBLE_CLICK, coordinate=Point(x, y)
        ).to_mapping()

    if name == "right_click_at":
        return DesktopCommand.create(DesktopAction.RIGHT_CLICK, coordinate=Point(x, y)).to_mapping()

    if name == "type_text_at":
        text = args.get("text", "")
        # Click first to focus, then type
        actions_text = text
        mapped = DesktopCommand.create(DesktopAction.TYPE, text=actions_text).to_mapping()
        mapped["_click_first"] = [x, y]
        mapped["_clear"] = args.get("clear_before_typing", False)
        mapped["_enter"] = args.get("press_enter", False)
        return mapped

    if name == "hover_at":
        return DesktopCommand.create(DesktopAction.MOVE, coordinate=Point(x, y)).to_mapping()

    if name in ("scroll_document", "scroll_at"):
        direction = args.get("direction", ScrollDirection.DOWN.value)
        amount = args.get("magnitude", 3)
        coord = Point(x, y) if name == "scroll_at" else Point(screen_w // 2, screen_h // 2)
        return DesktopCommand.create(
            DesktopAction.SCROLL,
            coordinate=coord,
            direction=ScrollDirection.parse(direction),
            amount=int(amount),
        ).to_mapping()

    if name == "key_combination":
        keys_str = args.get("keys", "")
        keys = [k.strip().lower() for k in keys_str.split("+")]
        key_map = {
            "control": "ctrl",
            "meta": "command",
            "command": "command",
            "arrowup": "up",
            "arrowdown": "down",
            "arrowleft": "left",
            "arrowright": "right",
            "escape": "esc",
        }
        mapped = [key_map.get(k, k) for k in keys]
        if len(mapped) == 1:
            return DesktopCommand.create(DesktopAction.KEY, key=mapped[0]).to_mapping()
        return DesktopCommand.create(DesktopAction.KEY, key="+".join(mapped)).to_mapping()

    if name == "drag_and_drop":
        dest_x = _denormalize(args.get("destination_x", 0), screen_w)
        dest_y = _denormalize(args.get("destination_y", 0), screen_h)
        return DesktopCommand.create(
            DesktopAction.DRAG,
            start_coordinate=Point(x, y),
            coordinate=Point(dest_x, dest_y),
        ).to_mapping()

    if name == "wait_5_seconds":
        return DesktopCommand.create(DesktopAction.WAIT, duration=5).to_mapping()

    if name in _EXCLUDED_ACTIONS:
        logger.warning("Gemini returned browser action '%s' — skipping", name)
        return None

    logger.warning("Unknown Gemini action: %s (args=%s)", name, args)
    return None


class GeminiCUAAgent(BaseCUAAgent):
    @staticmethod
    def name() -> str:
        return "gemini-cua"

    async def _run_agent(
        self,
        instruction: str,
        environment: Any,
        context: Any,
    ) -> None:
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if api_key is None:
            raise ValueError("GeminiCUAAgent requires GEMINI_API_KEY or GOOGLE_API_KEY")

        sandbox = cast(ComputerSandbox, await self.pre_run(environment))
        self.steps[0]["message"] = instruction

        client = genai.Client(api_key=api_key)
        model = self._parsed_model_name or DEFAULT_GEMINI_COMPUTER_USE_MODEL

        system_instruction = build_system_prompt(
            load_prompt("gemini.txt"),
            self.screen_width,
            self.screen_height,
            os_type=self.desktop.os_type,
            os_article=self.desktop.article,
            platform_notes=self.desktop.notes,
        ).replace("{DATE}", time.strftime("%A, %B %d, %Y"))

        config = types.GenerateContentConfig(
            tools=[
                types.Tool(
                    computer_use=types.ComputerUse(
                        environment=types.Environment.ENVIRONMENT_UNSPECIFIED,
                        excluded_predefined_functions=_EXCLUDED_ACTIONS,
                    )
                )
            ],
            system_instruction=system_instruction,
        )

        # Initial screenshot
        ss = await sandbox.screenshot.take_full_screen()
        (self.images_dir / "step_000.png").write_bytes(ss)

        contents: list = [
            Content(
                role="user",
                parts=[
                    Part(text=instruction),
                    Part.from_bytes(data=ss, mime_type="image/png"),
                ],
            )
        ]

        pending_calls: list = []

        for step_idx in range(self.max_steps):
            await self._fire_in_process(environment, step_idx)
            # Feed back screenshot for pending function calls
            if step_idx > 0 and pending_calls:
                parts = []
                for fc in pending_calls:
                    response_payload = {"url": "about:blank"}
                    args = dict(fc.args) if fc.args else {}
                    if "safety_decision" in args:
                        response_payload["safety_acknowledgement"] = "true"
                    fr = FunctionResponse(
                        id=fc.id,
                        name=fc.name,
                        response=response_payload,
                        parts=[
                            FunctionResponsePart(
                                inline_data=FunctionResponseBlob(
                                    mime_type="image/png",
                                    data=ss,
                                )
                            )
                        ],
                    )
                    parts.append(Part(function_response=fr))
                contents.append(Content(role="user", parts=parts))

            # API call with retry
            response = None
            for attempt in range(API_RETRY_TIMES):
                try:
                    response = client.models.generate_content(
                        model=model,
                        contents=contents,
                        config=config,
                    )
                    break
                except Exception as e:
                    err_str = str(e)
                    if "400" in err_str or "INVALID_ARGUMENT" in err_str:
                        logger.error("Gemini client error (not retryable): %s", err_str[:500])
                        self.steps.append(
                            {
                                "step_id": len(self.steps) + 1,
                                "source": "agent",
                                "message": f"API error: {err_str[:300]}",
                            }
                        )
                        await self.post_run(context, model, "gemini-cua")
                        return
                    logger.warning(
                        "Gemini API error (attempt %d/%d): %s",
                        attempt + 1,
                        API_RETRY_TIMES,
                        err_str[:300],
                    )
                    if attempt < API_RETRY_TIMES - 1:
                        time.sleep(API_RETRY_INTERVAL)

            if response is None:
                self.steps.append(
                    {
                        "step_id": len(self.steps) + 1,
                        "source": "agent",
                        "message": "All API attempts failed",
                    }
                )
                break

            # Track usage
            usage_meta = getattr(response, "usage_metadata", None)
            if usage_meta:
                self.total_in += getattr(usage_meta, "prompt_token_count", 0) or 0
                self.total_out += getattr(usage_meta, "candidates_token_count", 0) or 0

            # Parse response
            candidate = response.candidates[0] if response.candidates else None
            content = candidate.content if candidate else None
            if content is None or content.parts is None:
                self.steps.append(
                    {
                        "step_id": len(self.steps) + 1,
                        "source": "agent",
                        "message": "No content from model",
                    }
                )
                # Take new screenshot and retry
                ss = await sandbox.screenshot.take_full_screen()
                pending_calls = []
                continue

            contents.append(content)
            pending_calls = []

            # Extract actions and text
            tool_calls: list[dict[str, Any]] = []
            obs_results: list[dict[str, Any]] = []
            text_parts: list[str] = []

            for part in content.parts:
                if part.function_call:
                    fc = part.function_call
                    if fc.name is None:
                        continue
                    pending_calls.append(fc)
                    args = dict(fc.args) if fc.args else {}
                    name = fc.name
                    mapped = _map_gemini_action(name, args, self.screen_width, self.screen_height)

                    if mapped is None:
                        continue

                    tool_calls.append(
                        {
                            "tool_call_id": getattr(fc, "id", fc.name),
                            "function_name": name,
                            "arguments": mapped,
                        }
                    )

                    # Handle type_text_at special: click first, optionally clear, then type
                    if mapped.get("_click_first"):
                        cx, cy = mapped["_click_first"]
                        await sandbox.mouse.click(cx, cy)
                        await asyncio.sleep(0.3)
                        if mapped.get("_clear"):
                            clear_hotkey = "ctrl+a" if self.desktop.key_aliases else "command+a"
                            await sandbox.keyboard.hotkey(clear_hotkey)
                            await asyncio.sleep(0.1)
                            await sandbox.keyboard.press("Delete")
                            await asyncio.sleep(0.1)
                        # Now execute the type action
                        clean_action = {
                            "action": DesktopAction.TYPE.value,
                            "text": mapped.get("text", ""),
                        }
                        result_text, ss_bytes, ss_path = await execute_action(
                            sandbox,
                            clean_action,
                            self.images_dir,
                            step_idx + 1,
                            key_aliases=self.desktop_key_aliases,
                        )
                        if mapped.get("_enter"):
                            await sandbox.keyboard.press("Return")
                    else:
                        result_text, ss_bytes, ss_path = await execute_action(
                            sandbox,
                            mapped,
                            self.images_dir,
                            step_idx + 1,
                            key_aliases=self.desktop_key_aliases,
                        )

                    if ss_bytes:
                        ss = ss_bytes

                    obs: dict[str, Any] = {"content": result_text}
                    if ss_path:
                        obs["content"] = [
                            {"type": "text", "text": result_text},
                            {
                                "type": "image",
                                "source": {"media_type": "image/png", "path": ss_path},
                            },
                        ]
                    obs_results.append(obs)

                elif part.text:
                    text_parts.append(part.text)
                    if "INFEASIBLE" in part.text:
                        self.steps.append(
                            {
                                "step_id": len(self.steps) + 1,
                                "source": "agent",
                                "message": part.text[:500],
                            }
                        )
                        await self.post_run(context, model, "gemini-cua")
                        return

            # No function calls = model is done
            if not tool_calls:
                self.steps.append(
                    {
                        "step_id": len(self.steps) + 1,
                        "source": "agent",
                        "message": "\n".join(text_parts) or "Task complete.",
                    }
                )
                break

            # Record step
            step_data: dict[str, Any] = {
                "step_id": len(self.steps) + 1,
                "source": "agent",
                "message": "\n".join(text_parts) or None,
                "tool_calls": tool_calls,
                "metrics": {
                    "prompt_tokens": getattr(usage_meta, "prompt_token_count", 0) or 0
                    if usage_meta
                    else 0,
                    "completion_tokens": getattr(usage_meta, "candidates_token_count", 0) or 0
                    if usage_meta
                    else 0,
                },
            }
            if obs_results:
                step_data["observation"] = {"results": obs_results}
            self.steps.append(step_data)
            self.checkpoint(context, model, "gemini-cua")

        await self.post_run(context, model, "gemini-cua")


GeminiComputerAgent = GeminiCUAAgent
