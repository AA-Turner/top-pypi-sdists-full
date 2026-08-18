"""Shared computer-interface primitives (ToolResult, recorder mixin, caps).

Moved from ``computer_use_agent.computer`` so :class:`RemoteDesktopComputer`
can live in the SDK while the local Xvfb-backed ``DesktopComputer`` stays in
the computer-use agent package (which imports these primitives from here).
"""

from __future__ import annotations

import asyncio
import functools
import logging
import os
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from plato.otel import emit_computer_use_coordinates

_log = logging.getLogger(__name__)

# click_type -> plato.computer_use.action value for coordinate spans.
_CLICK_ACTION = {"single": "click", "double": "double_click", "triple": "triple_click"}

# Bash output cap. One `bash` tool call that dumps a log, `cat`s a binary or
# walks a large tree can return megabytes — observed: a single tool_result of
# ~3M tokens, which overflows the model's context window and kills the session
# on the spot. Mirroring the Claude Code harness, cap what a bash tool_result
# can carry and say plainly that the rest was dropped, so the model narrows the
# command instead of reasoning about output it can't explain. Enforced in
# DesktopComputer.bash / RemoteDesktopComputer.bash — every provider's bash tool
# funnels through those, so the cap is provider-agnostic.
MAX_BASH_OUTPUT_TOKENS = 25_000
# Conservative average for shell/log text (real ratio is usually >4 chars/token,
# so the byte budget under-counts tokens rather than over-counting them).
_CHARS_PER_TOKEN = 4
MAX_BASH_OUTPUT_CHARS = MAX_BASH_OUTPUT_TOKENS * _CHARS_PER_TOKEN
# stderr is normally the diagnostic that matters, so it gets a reserved slice of
# the shared budget rather than being squeezed out by a huge stdout.
_BASH_STDERR_CHARS = MAX_BASH_OUTPUT_CHARS // 4
# Headroom for the notice itself, so head + notice + tail stays under the limit.
_TRUNCATION_NOTICE_CHARS = 400


@runtime_checkable
class ActionRecorderLike(Protocol):
    """Extension-recorder attach point (agent-local ``EnvGenRecorder``)."""

    async def capture_screenshot(self, description: str) -> None: ...


@runtime_checkable
class ClipManagerLike(Protocol):
    """Interaction-clip attach point (agent-local ``ClipManager``)."""

    is_filming: bool

    async def on_op_start(self, kind: str) -> None: ...

    def on_op_end(self) -> None: ...

    def on_op_input_done(self) -> None: ...

    async def handle_bash(self, command: str): ...


class _ActionSummarizer:
    """Generates natural language action descriptions via Claude Haiku."""

    _PROMPT_TEMPLATE = (
        "Based on the AI assistant's reasoning and the action it took, "
        "generate a brief, past-tense description of what was done.\n\n"
        "AI's reasoning: {reasoning}\n\n"
        "Action taken: {action}\n\n"
        "Generate a single concise sentence (max 100 chars) describing "
        "what was done in past tense. Focus on the intent, not coordinates.\n"
        "Examples:\n"
        "- \"Clicked the 'Add to Cart' button\"\n"
        '- "Typed the search query into the search box"\n'
        '- "Scrolled down to see more products"\n\n'
        "Description:"
    )

    def __init__(self) -> None:
        import anthropic

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise ValueError("No ANTHROPIC_API_KEY set")
        self._client = anthropic.Anthropic(api_key=api_key)

    def summarize(self, reasoning: str, action: str) -> str:
        """Call Haiku to generate a concise past-tense description."""
        prompt = self._PROMPT_TEMPLATE.format(
            reasoning=reasoning[:500],
            action=action,
        )
        response = self._client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=80,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip().strip("\"'")
        return text[:150] if text else action


@dataclass
class ToolResult:
    """Result from a computer tool action."""

    output: str | None = None
    error: str | None = None
    base64_image: str | None = None


def _truncate_middle(text: str, limit: int) -> str:
    """Cap ``text`` at ``limit`` characters, keeping its head and its tail.

    Middle-out rather than head-only: in shell output the tail (the failing
    line, the summary, the last log entries) is usually what the model needs,
    while the head carries the command's context. The dropped span is replaced
    by a notice saying how much went away and how to get at the rest.
    """
    if len(text) <= limit:
        return text
    keep = max(limit - _TRUNCATION_NOTICE_CHARS, 0)
    head_len = keep // 2
    tail_len = keep - head_len
    head = text[:head_len]
    tail = text[len(text) - tail_len :] if tail_len else ""
    # Snap each half to a line boundary so neither ends/starts mid-line, but
    # only when that boundary is near the cut — a single enormous line must
    # still yield content instead of collapsing to nothing.
    nl = head.rfind("\n")
    if nl > head_len // 2:
        head = head[: nl + 1]
    nl = tail.find("\n")
    if nl != -1 and nl < len(tail) // 2:
        tail = tail[nl + 1 :]
    omitted = len(text) - len(head) - len(tail)
    notice = (
        f"\n\n<output truncated: {omitted} characters "
        f"(~{omitted // _CHARS_PER_TOKEN} tokens) omitted from the middle because "
        f"this command's output exceeded the ~{MAX_BASH_OUTPUT_TOKENS // 1000}k-token "
        f"tool-result limit. The first and last portions are shown; re-run with "
        f"head/tail/grep or redirect to a file to read the rest.>\n\n"
    )
    return f"{head}{notice}{tail}"


def _cap_bash_result(result: ToolResult) -> ToolResult:
    """Bound a bash ToolResult's text to ``MAX_BASH_OUTPUT_CHARS`` overall.

    stderr is capped first against its reserved slice, then stdout gets whatever
    of the shared budget is left, so the two together can never exceed the cap.
    Returns the original object untouched when nothing needed trimming.
    """
    error = result.error
    if error and len(error) > _BASH_STDERR_CHARS:
        error = _truncate_middle(error, _BASH_STDERR_CHARS)
    output = result.output
    if output:
        output = _truncate_middle(output, MAX_BASH_OUTPUT_CHARS - len(error or ""))
    if output is result.output and error is result.error:
        return result
    return ToolResult(output=output, error=error, base64_image=result.base64_image)


def _clip_op(fn):
    """Wrap an interactive computer op with interaction-clip timing hooks.

    The ClipManager needs exact op execution boundaries so armed clips start
    with the op (not with the arm command) and trim their tail to the last
    op's end. Ops mark end-of-input via ``_clip_settle`` /
    ``_clip_mark_input_done`` before their settle sleep + screenshot so the
    kept window covers the physical input only (the manager's inter-op margin
    films the UI reaction); ops that never mark it (``wait``) keep their full
    duration as footage. Inert when no manager is attached (the default).
    """

    @functools.wraps(fn)
    async def wrapper(self, *args, **kwargs):
        manager = self.clip_manager
        if manager is None:
            return await fn(self, *args, **kwargs)
        await manager.on_op_start(kind=fn.__name__)
        try:
            return await fn(self, *args, **kwargs)
        finally:
            manager.on_op_end()

    return wrapper


class _ActionRecorderMixin:
    """Shared action-summarization and screenshot-recording logic.

    Subclasses must set ``width``, ``height``, and ``recorder`` attributes on
    self, then call ``self._init_action_state()`` to initialize the internal
    reasoning/summarizer cache used by ``set_action_context`` and
    ``_record_action``.
    """

    width: int
    height: int
    recorder: ActionRecorderLike | None
    _action_reasoning: str | None
    _summarizer: _ActionSummarizer | None

    # Interaction-clip manager; attached by the agent when interaction_clips
    # is enabled. None (the default) keeps every op byte-identical.
    clip_manager: ClipManagerLike | None = None

    def _init_action_state(self) -> None:
        self._action_reasoning = None
        self._summarizer = None

    def _clip_mark_input_done(self) -> None:
        """Tell an armed clip the op's physical input just finished."""
        if self.clip_manager is not None:
            self.clip_manager.on_op_input_done()

    async def _clip_settle(self, seconds: float) -> None:
        """Post-input settle sleep, kept out of any armed clip's footage.

        Interactive ops sleep before their confirmation screenshot (up to
        several seconds via config.click_screenshot_delay); marking input-done
        first stops that frozen wait from counting as kept action time.
        """
        self._clip_mark_input_done()
        await asyncio.sleep(seconds)

    @property
    def dimensions(self) -> tuple[int, int]:
        """Return (width, height) of the display."""
        return (self.width, self.height)

    def set_action_context(self, reasoning: str) -> None:
        """Store the model's reasoning text for the next action description.

        Called by provider agents after extracting model reasoning but before
        executing tool calls.  The stored reasoning is consumed by
        ``_record_action`` when generating the natural language description.
        No-op when the extension recorder is not enabled.
        """
        if not self.recorder:
            return
        self._action_reasoning = reasoning

    async def _summarize_action(self, reasoning: str, raw_action: str) -> str:
        """Generate a natural language description via LLM, with fallback."""
        try:
            if self._summarizer is None:
                self._summarizer = _ActionSummarizer()
            return await asyncio.to_thread(self._summarizer.summarize, reasoning, raw_action)
        except Exception:
            _log.debug("Action summarization failed, using raw action", exc_info=True)
            return raw_action

    async def _record_action(self, description: str) -> None:
        """Generate a natural language description and capture a screenshot."""
        if not self.recorder:
            return
        reasoning = self._action_reasoning
        self._action_reasoning = None  # consume
        if reasoning:
            summary = await self._summarize_action(reasoning, description)
            description = f"{summary} [{description}]"
        await self.recorder.capture_screenshot(description)

    def _emit_coords(
        self,
        action: str,
        x: float,
        y: float,
        *,
        end_x: float | None = None,
        end_y: float | None = None,
        path: list[tuple[float, float]] | None = None,
        button: str | None = None,
    ) -> None:
        """Emit the normalized ``plato.computer-use.coordinates`` span for a
        mouse action at real-pixel (x, y). One funnel point for every provider:
        all mouse tools go through DesktopComputer/RemoteDesktopComputer, so
        emitting here keeps the contract provider-agnostic (Chronos cinema mode
        overlays these on the action's screenshot)."""
        emit_computer_use_coordinates(
            None,
            action=action,
            x=x,
            y=y,
            screen_width=self.width,
            screen_height=self.height,
            end_x=end_x,
            end_y=end_y,
            path=path,
            button=button,
        )
