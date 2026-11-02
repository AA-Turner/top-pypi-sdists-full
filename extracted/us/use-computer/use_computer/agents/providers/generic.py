"""Generic CUA agent — any vision LLM via litellm or tinker, pyautogui-style output."""

from __future__ import annotations

import asyncio
import base64
import io
import os
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, cast

import litellm
from litellm import exceptions as litellm_exceptions
from PIL import Image

from use_computer.agents.base import (
    BaseCUAAgent,
    ComputerSandbox,
    build_system_prompt,
    execute_action,
    load_prompt,
)
from use_computer.agents.types import (
    CoordinateMode,
    DesktopAction,
    DesktopCommand,
    LLMBackend,
    Point,
    ScrollDirection,
)

API_RETRY_TIMES = 5
API_RETRY_INTERVAL = 5
TRANSIENT_LITELLM_ERRORS = (
    litellm_exceptions.APIConnectionError,
    litellm_exceptions.InternalServerError,
    litellm_exceptions.RateLimitError,
    litellm_exceptions.ServiceUnavailableError,
    litellm_exceptions.Timeout,
)


class ReasoningEffort(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAX = "max"


class ReasoningHistory(str, Enum):
    DISABLED = "disabled"
    INTERLEAVED = "interleaved"
    PRESERVED = "preserved"


@dataclass(frozen=True)
class LiteLLMExtraBody:
    reasoning_effort: ReasoningEffort | None = None
    reasoning_history: ReasoningHistory | None = None

    def as_dict(self) -> dict[str, str]:
        values = {
            "reasoning_effort": self.reasoning_effort,
            "reasoning_history": self.reasoning_history,
        }
        return {key: value.value for key, value in values.items() if value is not None}


class GenericCUAAgent(BaseCUAAgent):
    def __init__(
        self,
        logs_dir: Path | str | None = None,
        model_name: str | None = None,
        prompt_template: str = "pyautogui.txt",
        llm_backend: str = LLMBackend.LITELLM.value,
        max_tokens: int = 4096,
        api_key: str | None = None,
        api_base: str | None = None,
        coord_mode: str | None = None,
        reasoning_effort: str | None = None,
        reasoning_history: str | None = None,
        renderer_name: str | None = None,
        model_path: str | None = None,
        temperature: float = 1.0,
        top_p: float = 0.95,
        top_k: int = -1,
        **kwargs: Any,
    ):
        super().__init__(logs_dir=logs_dir, model_name=model_name, **kwargs)
        self._prompt_template = load_prompt(prompt_template)
        self._llm_backend = LLMBackend(llm_backend)
        self._max_tokens = max_tokens
        # Fall back to provider-specific API key env vars.
        # litellm with openai/* prefix would otherwise look for OPENAI_API_KEY.
        if api_key is None and api_base:
            if "fireworks" in api_base:
                api_key = os.environ.get("FIREWORKS_API_KEY")
            elif "lilac" in api_base:
                api_key = os.environ.get("LILAC_API_KEY")
        self._api_key = api_key
        self._api_base = api_base
        self._extra_body = LiteLLMExtraBody(
            reasoning_effort=(
                ReasoningEffort(reasoning_effort) if reasoning_effort is not None else None
            ),
            reasoning_history=(
                ReasoningHistory(reasoning_history) if reasoning_history is not None else None
            ),
        ).as_dict()
        self._tinker_backend = None
        self._renderer_name = renderer_name
        self._model_path = model_path
        self._temperature = temperature
        self._top_p = top_p
        self._top_k = top_k
        # Coordinate convention emitted by the model:
        #   "api_pixel"        — Kimi default: 0..1 floats OR pixel ints in API space (1280x800)
        #   "normalized_1000"  — Qwen-VL default: 0..1000 ints as per-mille of screen
        # Auto-detect: qwen uses per-mille, everything else is Kimi-style.
        if coord_mode is None:
            coord_mode = (
                CoordinateMode.NORMALIZED_1000.value
                if model_name and "qwen" in model_name.lower()
                else CoordinateMode.API_PIXEL.value
            )
        self._coord_mode = CoordinateMode(coord_mode)

    @staticmethod
    def name() -> str:
        return "generic-cua"

    async def _get_completion(
        self, model: str, messages: list[dict], max_tokens: int
    ) -> tuple[str, int, int]:
        """Call LLM and return (text, prompt_tokens, completion_tokens)."""
        if self._llm_backend is LLMBackend.TINKER:
            return await self._tinker_completion(model, messages, max_tokens)

        for attempt in range(API_RETRY_TIMES):
            try:
                return self._litellm_completion(model, messages, max_tokens)
            except TRANSIENT_LITELLM_ERRORS as e:
                if attempt == API_RETRY_TIMES - 1:
                    raise
                self.logger.warning(
                    "litellm transient error, retrying %s/%s: %s",
                    attempt + 1,
                    API_RETRY_TIMES,
                    e,
                )
                await asyncio.sleep(API_RETRY_INTERVAL)

        raise RuntimeError("unreachable litellm retry state")

    def _litellm_completion(
        self, model: str, messages: list[dict], max_tokens: int
    ) -> tuple[str, int, int]:
        kwargs: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
        }
        if self._api_key:
            kwargs["api_key"] = self._api_key
        if self._api_base:
            kwargs["api_base"] = self._api_base
        if self._extra_body:
            kwargs["extra_body"] = self._extra_body
        response = litellm.completion(**kwargs)
        text = response.choices[0].message.content or ""
        usage = response.usage
        return text, usage.prompt_tokens or 0, usage.completion_tokens or 0

    async def _tinker_completion(
        self, model: str, messages: list[dict], max_tokens: int
    ) -> tuple[str, int, int]:
        if self._tinker_backend is None:
            from use_computer.agents.providers.tinker_backend import TinkerBackend

            self._tinker_backend = TinkerBackend(
                model_name=model,
                model_path=self._model_path,
                renderer_name=self._renderer_name,
                temperature=self._temperature,
                top_p=self._top_p,
                top_k=self._top_k,
                max_tokens=max_tokens,
            )
        return await self._tinker_backend.complete(messages, max_tokens)

    async def _run_agent(
        self,
        instruction: str,
        environment: Any,
        context: Any,
    ) -> None:
        sandbox = cast(ComputerSandbox, await self.pre_run(environment))
        self.steps[0]["message"] = instruction

        model = self.model_name or "openai/gpt-4o"

        # The model sees a 1280x800 image (resized from VM's 1920x1080) so the
        # prompt MUST tell it the screen is 1280x800 — otherwise the model emits
        # coords for the wrong space. We then scale model coords back to VM
        # pixel space before clicking. (Mirrors anthropic_cua.)
        api_w, api_h = 1280, 800
        # Coordinate space the model emits in. Qwen-VL ignores prompt size and
        # emits 0..1000 per-mille coords regardless, so we parse against that
        # space and scale directly to VM pixels.
        if self._coord_mode is CoordinateMode.NORMALIZED_1000:
            coord_w, coord_h = 1000, 1000
        else:
            coord_w, coord_h = api_w, api_h
        sx = self.screen_width / coord_w
        sy = self.screen_height / coord_h

        def _resize_for_api(png_bytes: bytes) -> bytes:
            """Resize and re-encode as JPEG q80. JPEG is ~17x smaller than PNG
            for screenshots and vision models read it identically. Fireworks
            rejected even single 1280x800 PNGs (~1.4MB b64) as 'Payload Too
            Large'; JPEG keeps the full sliding history under 1MB total."""
            img = Image.open(io.BytesIO(png_bytes))
            if img.size != (api_w, api_h):
                img = img.resize((api_w, api_h), Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            img.convert("RGB").save(buf, format="JPEG", quality=80)
            return buf.getvalue()

        def _scale_action(a: dict[str, Any]) -> dict[str, Any]:
            """Scale a parsed action's coordinates from model coord space to VM space."""
            for field in ("coordinate", "start_coordinate"):
                if field in a and isinstance(a[field], list) and len(a[field]) == 2:
                    a[field] = [int(a[field][0] * sx), int(a[field][1] * sy)]
            return a

        ss = await sandbox.screenshot.take_full_screen()
        (self.images_dir / "step_000.png").write_bytes(ss)

        # Conversation history (sliding window)
        max_history = 6
        history: list[dict[str, Any]] = []

        for step_idx in range(self.max_steps):
            await self._fire_in_process(environment, step_idx)
            system = build_system_prompt(
                self._prompt_template,
                api_w,
                api_h,
                instruction=instruction,
                step=step_idx + 1,
                max_steps=self.max_steps,
                os_type=self.desktop.os_type,
                os_article=self.desktop.article,
                platform_notes=self.desktop.notes,
            )
            system += f"\n\nYou are on step {step_idx + 1} of {self.max_steps}. Act efficiently."

            ss_b64 = base64.b64encode(_resize_for_api(ss)).decode()
            user_text = (
                "Here is the current screenshot. Complete the task."
                if step_idx == 0
                else "What's the next step?"
            )

            history.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{ss_b64}"},
                        },
                        {"type": "text", "text": user_text},
                    ],
                }
            )

            if len(history) > max_history:
                history = history[-max_history:]

            messages = [{"role": "system", "content": system}, *history]

            text, in_tok, out_tok = await self._get_completion(model, messages, self._max_tokens)
            self.total_in += in_tok
            self.total_out += out_tok

            history.append({"role": "assistant", "content": text})

            code_blocks = re.findall(r"```python\s*\n(.*?)```", text, re.DOTALL)
            code_match = bool(code_blocks)
            has_done = "DONE" in text or "```DONE```" in text
            has_fail = "FAIL" in text or "```FAIL```" in text
            has_wait = "WAIT" in text or "```WAIT```" in text

            if not code_match and has_done:
                self.steps.append(
                    {
                        "step_id": len(self.steps) + 1,
                        "source": "agent",
                        "message": text[:500],
                    }
                )
                break
            if not code_match and has_fail:
                self.steps.append(
                    {
                        "step_id": len(self.steps) + 1,
                        "source": "agent",
                        "message": text[:500],
                    }
                )
                break
            if not code_match and has_wait:
                await asyncio.sleep(2)
                ss = await sandbox.screenshot.take_full_screen()
                continue
            if not code_match:
                self.logger.warning(f"No code block: {text[:200]}")
                continue

            all_code = "\n".join(code_blocks)
            # Parse using the model's coord space (API px for Kimi, per-mille for Qwen),
            # then scale each coord to VM pixels.
            actions = _parse_pyautogui(all_code, coord_w, coord_h)
            actions = [_scale_action(a) for a in actions]

            last_ss_path: str | None = None
            for action in actions:
                _, ss_bytes, ss_path = await execute_action(
                    sandbox,
                    action,
                    self.images_dir,
                    step_idx + 1,
                    key_aliases=self.desktop_key_aliases,
                )
                if ss_bytes:
                    ss = ss_bytes
                    last_ss_path = ss_path

            step_data: dict[str, Any] = {
                "step_id": len(self.steps) + 1,
                "source": "agent",
                "message": text[:500],
                "metrics": {
                    "prompt_tokens": in_tok,
                    "completion_tokens": out_tok,
                },
            }
            if last_ss_path:
                step_data["observation"] = {
                    "results": [
                        {
                            "content": [
                                {"type": "text", "text": "After execution"},
                                {
                                    "type": "image",
                                    "source": {
                                        "media_type": "image/png",
                                        "path": last_ss_path,
                                    },
                                },
                            ],
                        }
                    ],
                }
            self.steps.append(step_data)
            self.checkpoint(context, model, "generic-cua")

            if not actions:
                ss = await sandbox.screenshot.take_full_screen()

        await self.post_run(context, model, "generic-cua")


GenericComputerAgent = GenericCUAAgent


# ── pyautogui parser ────────────────────────────────────────────────


def _parse_coord(s: str, dim: int) -> int:
    """Parse a coordinate from a model-emitted string.

    Tolerates floats (some models ignore "use integers" prompts) and
    normalized [0, 1] floats (scaled to `dim`). Falls back to 0 on garbage.
    """
    try:
        return int(s)
    except ValueError:
        pass
    try:
        f = float(s)
    except ValueError:
        return 0
    # Normalized coordinate (0..1) — scale to screen dim. Use < 1 (not <= 1)
    # so that "1" or "1.0" stays a literal pixel, not the right edge.
    if 0.0 <= f < 1.0:
        return int(f * dim)
    return int(f)


def _parse_int(s: str) -> int:
    """Parse an int field that should not be scaled (e.g. scroll clicks, drag delta)."""
    try:
        return int(s)
    except ValueError:
        try:
            return int(float(s))
        except ValueError:
            return 0


_MODIFIER_KEYS = {
    "ctrl",
    "control",
    "alt",
    "option",
    "shift",
    "cmd",
    "command",
    "win",
    "super",
    "meta",
}


def _parse_pyautogui(code: str, screen_w: int = 1920, screen_h: int = 1080) -> list[dict[str, Any]]:
    """Parse pyautogui code into action dicts."""
    actions: list[dict[str, Any]] = []
    held_mods: list[str] = []  # ordered list of held modifier keys for keyDown/keyUp pairs

    for line in code.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if "pyautogui.tripleClick(" in line:
            args = _args(line)
            if len(args) >= 2:
                actions.append(
                    DesktopCommand.create(
                        DesktopAction.TRIPLE_CLICK,
                        coordinate=Point(
                            _parse_coord(args[0], screen_w),
                            _parse_coord(args[1], screen_h),
                        ),
                    ).to_mapping()
                )

        elif "pyautogui.doubleClick(" in line:
            args = _args(line)
            if len(args) >= 2:
                actions.append(
                    DesktopCommand.create(
                        DesktopAction.DOUBLE_CLICK,
                        coordinate=Point(
                            _parse_coord(args[0], screen_w),
                            _parse_coord(args[1], screen_h),
                        ),
                    ).to_mapping()
                )

        elif "pyautogui.click(" in line:
            args = _args(line)
            if len(args) >= 2:
                action = (
                    DesktopAction.RIGHT_CLICK
                    if "'right'" in line or '"right"' in line
                    else DesktopAction.CLICK
                )
                actions.append(
                    DesktopCommand.create(
                        action,
                        coordinate=Point(
                            _parse_coord(args[0], screen_w),
                            _parse_coord(args[1], screen_h),
                        ),
                    ).to_mapping()
                )

        elif "pyautogui.moveTo(" in line:
            args = _args(line)
            if len(args) >= 2:
                actions.append(
                    DesktopCommand.create(
                        DesktopAction.MOVE,
                        coordinate=Point(
                            _parse_coord(args[0], screen_w),
                            _parse_coord(args[1], screen_h),
                        ),
                    ).to_mapping()
                )

        elif "pyautogui.scroll(" in line:
            args = _args(line)
            clicks = _parse_int(args[0]) if args else -3
            x = _parse_coord(args[1], screen_w) if len(args) > 1 else 0
            y = _parse_coord(args[2], screen_h) if len(args) > 2 else 0
            actions.append(
                DesktopCommand.create(
                    DesktopAction.SCROLL,
                    coordinate=Point(x, y),
                    direction=(ScrollDirection.UP if clicks > 0 else ScrollDirection.DOWN),
                    amount=abs(clicks),
                ).to_mapping()
            )

        elif "pyautogui.typewrite(" in line or "pyautogui.write(" in line:
            text = _str_arg(line)
            if text:
                actions.append(DesktopCommand.create(DesktopAction.TYPE, text=text).to_mapping())

        elif "pyautogui.press(" in line:
            key = _str_arg(line)
            if key:
                actions.append(DesktopCommand.create(DesktopAction.KEY, key=key).to_mapping())

        elif "pyautogui.hotkey(" in line:
            keys = _str_args(line)
            if keys:
                actions.append(
                    DesktopCommand.create(DesktopAction.KEY, key="+".join(keys)).to_mapping()
                )

        elif "pyautogui.keyDown(" in line:
            key = _str_arg(line)
            if key:
                if key.lower() in _MODIFIER_KEYS:
                    held_mods.append(key)
                else:
                    # non-modifier key — fire it now combined with any held mods
                    combo = "+".join(held_mods + [key])
                    actions.append(DesktopCommand.create(DesktopAction.KEY, key=combo).to_mapping())

        elif "pyautogui.keyUp(" in line:
            key = _str_arg(line)
            if key and key in held_mods:
                held_mods.remove(key)
            # otherwise: partner of an already-emitted keyDown, ignore

        elif "pyautogui.drag(" in line:
            args = _args(line)
            if len(args) >= 2:
                # drag uses relative deltas, not absolute coordinates — don't normalize
                actions.append(
                    DesktopCommand.create(
                        DesktopAction.DRAG,
                        start_coordinate=Point(),
                        coordinate=Point(_parse_int(args[0]), _parse_int(args[1])),
                    ).to_mapping()
                )

        elif "time.sleep(" in line or "pyautogui.sleep(" in line:
            args = _args(line)
            if args:
                try:
                    duration = float(args[0])
                except ValueError:
                    duration = 1.0
                actions.append(
                    DesktopCommand.create(DesktopAction.WAIT, duration=duration).to_mapping()
                )

    return actions


def _args(line: str) -> list[str]:
    m = re.search(r"\(([^)]*)\)", line)
    if not m:
        return []
    parts = []
    for p in m.group(1).split(","):
        p = p.strip()
        if "=" in p:
            p = p.split("=", 1)[1].strip()
        p = p.strip("'\"")
        if p:
            parts.append(p)
    return parts


def _str_arg(line: str) -> str:
    """Extract first string literal. Handles ''' """ + '"""' + """, ''', ", '."""
    # triple-quoted forms first (longer match wins)
    m = re.search(r'"""(.*?)"""', line, re.DOTALL)
    if m:
        return m.group(1)
    m = re.search(r"'''(.*?)'''", line, re.DOTALL)
    if m:
        return m.group(1)
    m = re.search(r'"([^"]*)"', line)
    if m:
        return m.group(1)
    m = re.search(r"'([^']*)'", line)
    if m:
        return m.group(1)
    return ""


def _str_args(line: str) -> list[str]:
    """Extract all string literals. Handles triple-quoted and single-quoted forms."""
    out: list[str] = []
    # Strip triple-quoted matches first so they don't get double-counted
    remaining = line
    for pat in (r'"""(.*?)"""', r"'''(.*?)'''"):
        for m in re.finditer(pat, remaining, re.DOTALL):
            out.append(m.group(1))
        remaining = re.sub(pat, "", remaining, flags=re.DOTALL)
    for m in re.finditer(r'"([^"]*)"', remaining):
        out.append(m.group(1))
    for m in re.finditer(r"'([^']*)'", remaining):
        out.append(m.group(1))
    return out
