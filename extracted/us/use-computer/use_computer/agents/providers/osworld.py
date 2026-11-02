"""OSWorld prompt agent preserving the benchmark's pyautogui action DSL."""

from __future__ import annotations

import base64
import re
from pathlib import Path
from typing import Any

from use_computer.agents.base import load_prompt
from use_computer.agents.providers.generic import GenericCUAAgent


class OSWorldAgent(GenericCUAAgent):
    def __init__(
        self,
        logs_dir: Path | str | None = None,
        model_name: str | None = None,
        prompt_template: str = "osworld_pyautogui.txt",
        client_password: str = "password",
        max_trajectory_length: int = 3,
        **kwargs: Any,
    ):
        super().__init__(
            logs_dir=logs_dir,
            model_name=model_name,
            prompt_template=prompt_template,
            **kwargs,
        )
        self._prompt_template = load_prompt(prompt_template)
        self._client_password = client_password
        self._max_trajectory_length = max_trajectory_length
        self._thoughts: list[str] = []
        self._actions: list[Any] = []
        self._observations: list[dict[str, Any]] = []

    @staticmethod
    def name() -> str:
        return "osworld-agent"

    async def _run_agent(self, instruction: str, environment: Any, context: Any) -> None:
        await self.pre_run(environment)
        self.steps[0]["message"] = instruction
        model = self.model_name or "gpt-4o"

        obs = await environment.observe()
        _write_screenshot(self.images_dir, "step_000", obs["screenshot"])

        action_idx = 0
        done = False
        for step_idx in range(self.max_steps):
            await self._fire_in_process(environment, step_idx)
            response, actions, in_tok, out_tok = await self._predict(model, instruction, obs)
            self.total_in += in_tok
            self.total_out += out_tok

            if not actions:
                self.logger.warning(f"OSWorld agent produced no parseable action: {response[:200]}")
                continue

            last_ss_path: str | None = None
            last_info: dict[str, Any] = {}
            for action in actions:
                action_idx += 1
                obs, reward, done, info = await environment.step(action)
                last_info = info
                ss_path = _write_screenshot(
                    self.images_dir,
                    f"step_{action_idx:03d}",
                    obs["screenshot"],
                )
                last_ss_path = f"images/{ss_path.name}"
                if done:
                    break

            step_data: dict[str, Any] = {
                "step_id": len(self.steps) + 1,
                "source": "agent",
                "message": response[:500],
                "metrics": {
                    "prompt_tokens": in_tok,
                    "completion_tokens": out_tok,
                },
            }
            if actions:
                step_data["action"] = actions[-1]
            if last_info:
                step_data["info"] = last_info
            if last_ss_path:
                step_data["observation"] = {
                    "results": [
                        {
                            "content": [
                                {"type": "text", "text": "After execution"},
                                {
                                    "type": "image",
                                    "source": {
                                        "media_type": _image_media_type(obs["screenshot"]),
                                        "path": last_ss_path,
                                    },
                                },
                            ],
                        }
                    ],
                }
            self.steps.append(step_data)
            self.checkpoint(context, model, "osworld-agent")
            if done:
                break

        await self.post_run(context, model, "osworld-agent")

    async def _predict(
        self, model: str, instruction: str, obs: dict[str, Any]
    ) -> tuple[str, list[Any], int, int]:
        system = (
            self._prompt_template.format(CLIENT_PASSWORD=self._client_password)
            + f"\nYou are asked to complete the following task: {instruction}"
        )
        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": [{"type": "text", "text": system}],
            }
        ]

        for previous_obs, previous_thought in zip(
            self._observations[-self._max_trajectory_length :],
            self._thoughts[-self._max_trajectory_length :],
            strict=False,
        ):
            messages.append(
                _screenshot_user_message(
                    previous_obs["screenshot"],
                    previous_obs.get("media_type", "image/png"),
                )
            )
            messages.append(
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": previous_thought.strip() or "No valid action",
                        }
                    ],
                }
            )

        current = {
            "screenshot": base64.b64encode(obs["screenshot"]).decode(),
            "media_type": _image_media_type(obs["screenshot"]),
        }
        self._observations.append(current)
        messages.append(_screenshot_user_message(current["screenshot"], current["media_type"]))

        response, in_tok, out_tok = await self._get_completion(model, messages, self._max_tokens)
        actions = parse_code_from_string(response)
        self._thoughts.append(response)
        self._actions.extend(actions)
        return response, actions, in_tok, out_tok


def _screenshot_user_message(
    screenshot_b64: str,
    media_type: str = "image/png",
) -> dict[str, Any]:
    prompt = (
        "Given the screenshot as below. What's the next step that you will do "
        "to help with the task?"
    )
    return {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt,
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{media_type};base64,{screenshot_b64}",
                    "detail": "high",
                },
            },
        ],
    }


def _write_screenshot(images_dir: Path, stem: str, data: bytes) -> Path:
    path = images_dir / f"{stem}{_image_extension(data)}"
    path.write_bytes(data)
    return path


def _image_media_type(data: bytes) -> str:
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    return "image/png"


def _image_extension(data: bytes) -> str:
    if _image_media_type(data) == "image/jpeg":
        return ".jpg"
    return ".png"


def parse_code_from_string(input_string: str) -> list[str]:
    input_string = "\n".join(line.strip() for line in input_string.split(";") if line.strip())
    if input_string.strip() in ["WAIT", "DONE", "FAIL"]:
        return [input_string.strip()]

    matches = re.findall(r"```(?:\w+\s+)?(.*?)```", input_string, re.DOTALL)
    codes: list[str] = []
    for match in matches:
        match = match.strip()
        commands = ["WAIT", "DONE", "FAIL"]
        if match in commands:
            codes.append(match.strip())
        elif match.split("\n")[-1] in commands:
            if len(match.split("\n")) > 1:
                codes.append("\n".join(match.split("\n")[:-1]))
            codes.append(match.split("\n")[-1])
        else:
            codes.append(match)
    return codes


OSWorldComputerAgent = OSWorldAgent
