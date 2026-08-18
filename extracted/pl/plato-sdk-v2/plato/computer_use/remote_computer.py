"""Remote desktop computer interface via ubuntu_vm SDK.

Drop-in replacement for the computer-use agent's local DesktopComputer that
proxies all actions to a remote VM over HTTP using the ubuntu_vm AsyncClient.
Lives in the SDK (moved from ``computer_use_agent.remote_computer``) so the
computer-use MCP server can drive a remote desktop from any agent harness.
"""

from __future__ import annotations

import asyncio
import base64
import logging
from typing import TYPE_CHECKING, Literal

from plato.computer_use.base import (
    _CLICK_ACTION,
    ToolResult,
    _ActionRecorderMixin,
    _cap_bash_result,
    _clip_op,
)
from plato.sims.ubuntu_vm import AsyncClient as VMAsyncClient
from plato.sims.ubuntu_vm.models import (
    Action,
    BashRequest,
    ComputerRequest,
    ScrollDirection,
)
from plato.utils.api_retry import api_retry

if TYPE_CHECKING:
    from plato.computer_use.base import ActionRecorderLike

_log = logging.getLogger(__name__)

# Map DesktopComputer scroll directions to SDK ScrollDirection enum
_SCROLL_DIR_MAP = {
    "up": ScrollDirection.up,
    "down": ScrollDirection.down,
    "left": ScrollDirection.left,
    "right": ScrollDirection.right,
}


class RemoteDesktopComputer(_ActionRecorderMixin):
    """Desktop computer interface that proxies to a remote VM.

    Implements the same interface as DesktopComputer so providers
    can use it as a drop-in replacement.
    """

    def __init__(
        self,
        vm_client: VMAsyncClient,
        width: int = 1280,
        height: int = 800,
        display: str = ":0",
        recorder: ActionRecorderLike | None = None,
        screenshots_to_runtime: bool = False,
        screenshot_delay_s: float | None = None,
    ):
        self._vm = vm_client
        self.width = width
        self.height = height
        self.display = display
        self.recorder = recorder
        # When True (native-desktop exploration): the agent + workspace live on
        # the RUNTIME while the desktop is a separate VM. The exploration prompt
        # persists screenshots via `bash: cp /tmp/screenshot.png /workspace/...`,
        # which must run on the runtime (not the desktop VM) against a real
        # /tmp/screenshot.png. So we mirror each frame to the runtime's
        # /tmp/screenshot.png and route bash to the runtime. Off by default so
        # cua-task's desktop-bash behavior is unchanged.
        self._screenshots_to_runtime = screenshots_to_runtime
        # Forwarded on every ComputerRequest so the in-VM desktop agent can use
        # it as the post-action settle time before its screenshot. None keeps
        # each agent's built-in default (2.0s on Windows). Old agents ignore
        # unknown request fields, so this degrades gracefully.
        self._screenshot_delay_s = screenshot_delay_s
        self._init_action_state()

    async def sync_dimensions_from_remote(self) -> None:
        """Overwrite ``self.width/self.height`` with the remote VM's actual
        resolution via ``GET /status``. Providers read these live to build
        prompts and scale coordinates, so a constructor/VM mismatch silently
        translates every click. Call once after construction; keeps defaults
        on failure rather than aborting session setup.
        """
        try:
            status = await self._vm.status()
        except Exception as exc:
            _log.warning(
                "Failed to query remote VM /status for display resolution; keeping defaults %dx%d: %s",
                self.width,
                self.height,
                exc,
            )
            return
        new_w, new_h = status.resolution.width, status.resolution.height
        if (new_w, new_h) != (self.width, self.height):
            _log.info(
                "Remote VM resolution %dx%d differs from configured %dx%d; using remote values.",
                new_w,
                new_h,
                self.width,
                self.height,
            )
        self.width = new_w
        self.height = new_h

    def _to_tool_result(self, sdk_result) -> ToolResult:
        """Convert ubuntu_vm SDK ToolResult to agent ToolResult."""
        return ToolResult(
            output=sdk_result.output,
            error=sdk_result.error,
            base64_image=sdk_result.base64_image,
        )

    def _mirror_frame(self, sdk_result) -> None:
        """Keep the runtime's /tmp/screenshot.png in sync with the frame just
        returned to the agent (``screenshots_to_runtime`` mode only).

        The remote VM screenshots after EVERY computer op and returns that frame
        in ``base64_image`` (verified: click/key/move all return a fresh frame),
        so the agent's "current screenshot" is the last action's result image.
        The exploration prompt then runs ``cp /tmp/screenshot.png ...`` on the
        runtime to persist it. Local DesktopComputer gets this for free — every
        action ends with ``scrot`` writing /tmp/screenshot.png — but here actions
        execute on the desktop VM, so we must mirror each frame to the runtime.
        Mirroring on screenshot() ALONE is not enough: in clickpath mode the
        navigator drives clicks/keys (never the screenshot action), so without
        this /tmp/screenshot.png stays frozen at the first frame and every cp
        copies the stale desktop. Best-effort; never break an action."""
        if not self._screenshots_to_runtime:
            return
        img = getattr(sdk_result, "base64_image", None)
        if not img:
            return
        try:
            with open("/tmp/screenshot.png", "wb") as f:
                f.write(base64.b64decode(img))
        except Exception as e:
            _log.warning("Failed to mirror screenshot to runtime /tmp: %s", e)

    async def _computer(self, request: ComputerRequest):
        """Run a computer action on the remote VM and mirror its post-action
        frame to the runtime (see :meth:`_mirror_frame`). All action methods
        route through here so /tmp/screenshot.png tracks every op, matching
        local DesktopComputer's per-action scrot."""
        # Attach the configured settle time unless the caller already set one;
        # single choke point so every action (click, scroll, key, ...) carries it.
        if self._screenshot_delay_s is not None and request.screenshot_delay_s is None:
            request.screenshot_delay_s = self._screenshot_delay_s
        # api_retry: a transient 502/503 from the sims proxy (VM briefly pegged,
        # desktop agent restarting) previously killed the whole session on a single
        # read-only screenshot. The retry predicate only replays statuses where the
        # request provably never reached the agent.
        result = await api_retry(self._vm.computer)(request)
        self._mirror_frame(result)
        return result

    async def screenshot(self, record_action: str | None = None) -> ToolResult:
        """Take a screenshot of the remote VM."""
        result = await self._computer(ComputerRequest(action=Action.screenshot))
        if record_action:
            await self._record_action(record_action)
        return self._to_tool_result(result)

    @_clip_op
    async def mouse_move(self, x: int, y: int) -> ToolResult:
        """Move mouse to coordinates on the remote VM."""
        self._emit_coords("mouse_move", x, y)
        result = await self._computer(ComputerRequest(action=Action.mouse_move, coordinate=[x, y]))
        self._clip_mark_input_done()
        await self._record_action(f"mouse_move({x}, {y})")
        return self._to_tool_result(result)

    @_clip_op
    async def click(
        self,
        x: int | None = None,
        y: int | None = None,
        button: Literal["left", "right", "middle"] = "left",
        click_type: Literal["single", "double", "triple"] = "single",
    ) -> ToolResult:
        """Click at coordinates on the remote VM."""
        single_action = {
            "left": Action.left_click,
            "right": Action.right_click,
            "middle": Action.middle_click,
        }[button]
        native_multi = {
            ("left", "double"): Action.double_click,
            ("left", "triple"): Action.triple_click,
        }
        coord = None
        if x is not None and y is not None:
            coord = [x, y]
            # .get default mirrors computer.py: model-supplied click_type strings
            # must not abort the click on an unrecognized value.
            self._emit_coords(_CLICK_ACTION.get(click_type, "click"), x, y, button=button)

        if click_type == "single":
            result = await self._computer(ComputerRequest(action=single_action, coordinate=coord))
        elif (button, click_type) in native_multi:
            result = await self._computer(ComputerRequest(action=native_multi[(button, click_type)], coordinate=coord))
        else:
            # Server lacks native double/triple for right/middle. Emit N sequential
            # single clicks of the requested button to match xdotool --repeat.
            n = 2 if click_type == "double" else 3
            if coord:
                await self._computer(ComputerRequest(action=Action.mouse_move, coordinate=coord))
            result = None
            for _ in range(n):
                result = await self._computer(ComputerRequest(action=single_action))

        self._clip_mark_input_done()
        coord_str = f"({x}, {y})" if x is not None and y is not None else "(current)"
        await self._record_action(f"{click_type}_{button}_click{coord_str}")
        return self._to_tool_result(result)

    @_clip_op
    async def type_text(self, text: str) -> ToolResult:
        """Type text on the remote VM."""
        result = await self._computer(ComputerRequest(action=Action.type, text=text))
        self._clip_mark_input_done()
        text_preview = text[:50] + "..." if len(text) > 50 else text
        await self._record_action(f"type_text({text_preview!r})")
        return self._to_tool_result(result)

    @_clip_op
    async def key(self, key: str) -> ToolResult:
        """Press a key or key combination on the remote VM."""
        result = await self._computer(ComputerRequest(action=Action.key, text=key))
        self._clip_mark_input_done()
        await self._record_action(f"key({key})")
        return self._to_tool_result(result)

    @_clip_op
    async def scroll(
        self,
        x: int | None = None,
        y: int | None = None,
        direction: Literal["up", "down", "left", "right"] = "down",
        amount: int = 3,
    ) -> ToolResult:
        """Scroll at coordinates on the remote VM."""
        coord = None
        if x is not None and y is not None:
            coord = [x, y]
            self._emit_coords("scroll", x, y)
        result = await self._computer(
            ComputerRequest(
                action=Action.scroll,
                coordinate=coord,
                scroll_direction=_SCROLL_DIR_MAP.get(direction, ScrollDirection.down),
                scroll_amount=amount,
            )
        )
        return self._to_tool_result(result)

    # Filmed drags decompose the server's instant left_click_drag into a
    # held-button stepped sweep, mirroring DesktopComputer._filmed_drag_cmd:
    # the payoff motion is otherwise a single-frame jump the clip can't show,
    # and drag-sensitive UIs (sliders, canvas handles) often miss instant
    # grabs entirely. The hover dwell + 1px jiggle before the press lets
    # hover-activated handles arm their drag handler (see the desktop
    # constant's docstring). The server rejects coordinates on
    # left_mouse_down/up, so the press/release land at the pointer's
    # current position.
    _FILMED_DRAG_STEPS = 12
    _FILMED_DRAG_STEP_SLEEP = 0.05
    _FILMED_DRAG_HOVER_PRE_S = 0.3
    _FILMED_DRAG_HOVER_POST_S = 0.5
    _FILMED_DRAG_GRAB_HOLD_S = 0.15

    async def _filmed_drag(self, start_x: int, start_y: int, end_x: int, end_y: int):
        await self._computer(ComputerRequest(action=Action.mouse_move, coordinate=[start_x, start_y]))
        await asyncio.sleep(self._FILMED_DRAG_HOVER_PRE_S)
        await self._computer(ComputerRequest(action=Action.mouse_move, coordinate=[start_x + 1, start_y]))
        await self._computer(ComputerRequest(action=Action.mouse_move, coordinate=[start_x, start_y]))
        await asyncio.sleep(self._FILMED_DRAG_HOVER_POST_S)
        await self._computer(ComputerRequest(action=Action.left_mouse_down))
        await asyncio.sleep(self._FILMED_DRAG_GRAB_HOLD_S)
        for i in range(1, self._FILMED_DRAG_STEPS + 1):
            t = i / self._FILMED_DRAG_STEPS
            xi = round(start_x + (end_x - start_x) * t)
            yi = round(start_y + (end_y - start_y) * t)
            await self._computer(ComputerRequest(action=Action.mouse_move, coordinate=[xi, yi]))
            await asyncio.sleep(self._FILMED_DRAG_STEP_SLEEP)
        return await self._computer(ComputerRequest(action=Action.left_mouse_up))

    @_clip_op
    async def drag(self, start_x: int, start_y: int, end_x: int, end_y: int) -> ToolResult:
        """Drag from start to end coordinates on the remote VM."""
        self._emit_coords("drag", start_x, start_y, end_x=end_x, end_y=end_y, button="left")
        if self.clip_manager is not None and self.clip_manager.is_filming:
            result = await self._filmed_drag(start_x, start_y, end_x, end_y)
        else:
            # Move to start position first, then drag to end
            await self._computer(ComputerRequest(action=Action.mouse_move, coordinate=[start_x, start_y]))
            result = await self._computer(ComputerRequest(action=Action.left_click_drag, coordinate=[end_x, end_y]))
        self._clip_mark_input_done()
        await self._record_action(f"drag({start_x},{start_y})->({end_x},{end_y})")
        return self._to_tool_result(result)

    async def cursor_position(self) -> ToolResult:
        """Get current cursor position on the remote VM."""
        result = await self._computer(ComputerRequest(action=Action.cursor_position))
        return self._to_tool_result(result)

    @_clip_op
    async def wait(self, seconds: float = 1.0) -> ToolResult:
        """Wait and take a screenshot."""
        # See DesktopComputer.wait: filmed waits keep only the fixed inter-op
        # margin (known limitation for animations outlasting the wait's start).
        self._clip_mark_input_done()
        result = await self._computer(ComputerRequest(action=Action.wait, duration=seconds))
        return self._to_tool_result(result)

    async def bash(self, command: str, timeout: int = 120) -> ToolResult:
        """Execute a bash command.

        Default: on the remote desktop VM. In ``screenshots_to_runtime`` mode
        (native-desktop exploration), run on the RUNTIME instead — the prompt
        only uses bash to ``cp /tmp/screenshot.png /workspace/screenshots/...``,
        and both that file and ``/workspace`` live on the runtime, not the
        desktop VM.

        Either way the output is capped (see :func:`_cap_bash_result`) so one
        runaway command cannot blow the model's context window.
        """
        if self.clip_manager is not None:
            handled = await self.clip_manager.handle_bash(command)
            if handled is not None:
                return handled
        if self._screenshots_to_runtime:
            proc = None
            try:
                proc = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                out, err = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            except TimeoutError:
                # Kill the still-running child; wait_for cancelled communicate()
                # but does not terminate the subprocess, which would otherwise
                # linger holding its pipes.
                if proc is not None:
                    proc.kill()
                    try:
                        await proc.communicate()
                    except Exception:
                        pass
                return ToolResult(error=f"runtime bash timed out after {timeout}s: {command!r}")
            except Exception as e:
                return ToolResult(error=f"runtime bash failed: {e}")
            error = None
            if proc.returncode:
                # Non-zero exit must surface as an error even when stderr is
                # empty (e.g. `exit 3`), matching DesktopComputer.bash semantics.
                error = err.decode("utf-8", "replace").strip() or f"command exited with code {proc.returncode}"
            return _cap_bash_result(
                ToolResult(
                    output=out.decode("utf-8", "replace") or None,
                    error=error,
                )
            )
        result = await api_retry(self._vm.bash)(BashRequest(command=command, timeout=timeout))
        return _cap_bash_result(self._to_tool_result(result))
