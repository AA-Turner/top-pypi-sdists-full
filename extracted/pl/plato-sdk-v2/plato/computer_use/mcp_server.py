"""HTTP MCP server exposing a remote ubuntu-vm desktop's computer-use tools.

Wraps a :class:`RemoteDesktopComputer` in a :class:`plato.tools.server.ToolServer`
so any agent harness with MCP support (claude-code, codex, ...) can drive the
remote desktop. The constructor deliberately takes a ``RemoteDesktopComputer``
only — MCP computer use always targets a remote ubuntu VM, never the agent VM
itself (the local Xvfb ``DesktopComputer`` stays private to the computer-use
agent harness).

Every action returns the desktop's post-action screenshot as a native MCP
image block (the desktop agent screenshots after each op), so the model always
sees the result of what it just did.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from plato.computer_use.base import ToolResult
from plato.computer_use.remote_computer import RemoteDesktopComputer
from plato.computer_use.ssh_sandbox import SshSandbox
from plato.tools.definition import ToolDefinition
from plato.tools.server import ToolServer


def _result_to_dict(result: ToolResult) -> dict:
    """Convert a ToolResult to the MCP result dict.

    ``screenshot_b64`` is picked up by ToolServer's image extraction and
    returned as a native ImageContent block (PNG frames from the desktop
    agent) instead of bloating the text context.
    """
    out: dict = {}
    if result.output:
        out["output"] = result.output
    if result.error:
        out["error"] = result.error
    if result.base64_image:
        out["screenshot_b64"] = result.base64_image
        out["media_type"] = result.media_type or "image/png"
    if not out:
        out["output"] = "(no output)"
    return out


class ScreenshotInput(BaseModel):
    """No parameters."""


class ClickInput(BaseModel):
    x: int | None = Field(
        default=None, description="X pixel coordinate; omit with y to click at the current cursor position"
    )
    y: int | None = Field(default=None, description="Y pixel coordinate")
    button: Literal["left", "right", "middle"] = Field(default="left", description="Mouse button")
    click_type: Literal["single", "double", "triple"] = Field(default="single", description="Number of clicks")


class TypeTextInput(BaseModel):
    text: str = Field(description="Text to type at the current focus")


class KeyInput(BaseModel):
    key: str = Field(description="Key or key combination in xdotool keysym form, e.g. 'Return', 'ctrl+c', 'alt+Tab'")


class ScrollInput(BaseModel):
    x: int | None = Field(
        default=None,
        description="X pixel coordinate to scroll at; omit with y to scroll at the current cursor position",
    )
    y: int | None = Field(default=None, description="Y pixel coordinate")
    direction: Literal["up", "down", "left", "right"] = Field(default="down", description="Scroll direction")
    amount: int = Field(default=3, description="Number of wheel clicks")


class DragInput(BaseModel):
    start_x: int = Field(description="Drag start X pixel coordinate")
    start_y: int = Field(description="Drag start Y pixel coordinate")
    end_x: int = Field(description="Drag end X pixel coordinate")
    end_y: int = Field(description="Drag end Y pixel coordinate")


class MouseMoveInput(BaseModel):
    x: int = Field(description="X pixel coordinate")
    y: int = Field(description="Y pixel coordinate")


class CursorPositionInput(BaseModel):
    """No parameters."""


class WaitInput(BaseModel):
    seconds: float = Field(default=1.0, description="Seconds to wait before the screenshot")


class BashInput(BaseModel):
    command: str = Field(description="Shell command to run on the desktop VM")
    timeout: int = Field(default=120, description="Command timeout in seconds")


class ReadFileInput(BaseModel):
    path: str = Field(description="Absolute path on the desktop VM (a file, or a directory to list)")
    view_range: list[int] | None = Field(
        default=None,
        description="Optional [start, end] line range (1-based, inclusive; end -1 means to end of file)",
    )


class WriteFileInput(BaseModel):
    path: str = Field(description="Absolute path on the desktop VM; created or overwritten")
    content: str = Field(description="Full file content to write")


class EditFileInput(BaseModel):
    path: str = Field(description="Absolute path of an existing file on the desktop VM")
    old_str: str = Field(description="Exact text to replace; must occur exactly once in the file")
    new_str: str = Field(description="Replacement text")


# The tools that DO WORK on the sandbox, as opposed to the ones that drive its
# screen. A harness whose own shell and file tools already execute on the
# sandbox (Codex, via an exec-server environment) turns exactly these off, so
# the model is not handed two ways to do the same thing. Kept here, beside the
# definitions, because a tool added to this server and not classified here is
# one that silently reaches such a harness - which is exactly what happened when
# grep and glob were added.
SANDBOX_EXECUTION_TOOLS: tuple[str, ...] = (
    "bash",
    "read_file",
    "write_file",
    "edit_file",
    "grep",
    "glob",
)


class GrepInput(BaseModel):
    pattern: str = Field(description="Regular expression to search file contents for")
    path: str | None = Field(default=None, description="File or directory to search; defaults to the cwd")
    glob: str | None = Field(default=None, description="Only search files whose path matches this glob")
    context: int = Field(default=0, description="Lines of context to show around each match")
    ignore_case: bool = Field(default=False, description="Case-insensitive search")
    files_with_matches: bool = Field(default=False, description="List matching file paths instead of the matches")


class GlobInput(BaseModel):
    pattern: str = Field(description="Glob to match against file paths, e.g. '**/*.py'")
    path: str | None = Field(default=None, description="Directory to search under; defaults to the cwd")


class RemoteComputerToolServer(ToolServer):
    """MCP server for a single remote ubuntu-vm desktop."""

    def __init__(
        self,
        computer: RemoteDesktopComputer,
        *,
        sandbox: SshSandbox | None = None,
        name: str = "Remote Desktop Computer",
        host: str = "127.0.0.1",
        port: int = 8766,
    ) -> None:
        self._computer = computer
        # When set, bash and the file tools run over the persistent ssh
        # session on the mesh; the screen tools always use the desktop agent.
        self._sandbox = sandbox
        super().__init__(name=name, host=host, port=port)

    def build_tools(self) -> list[ToolDefinition]:
        c = self._computer
        s = self._sandbox

        async def screenshot(args: ScreenshotInput) -> dict:
            return _result_to_dict(await c.screenshot())

        async def click(args: ClickInput) -> dict:
            return _result_to_dict(await c.click(args.x, args.y, args.button, args.click_type))

        async def type_text(args: TypeTextInput) -> dict:
            return _result_to_dict(await c.type_text(args.text))

        async def key(args: KeyInput) -> dict:
            return _result_to_dict(await c.key(args.key))

        async def scroll(args: ScrollInput) -> dict:
            return _result_to_dict(await c.scroll(args.x, args.y, args.direction, args.amount))

        async def drag(args: DragInput) -> dict:
            return _result_to_dict(await c.drag(args.start_x, args.start_y, args.end_x, args.end_y))

        async def mouse_move(args: MouseMoveInput) -> dict:
            return _result_to_dict(await c.mouse_move(args.x, args.y))

        async def cursor_position(args: CursorPositionInput) -> dict:
            return _result_to_dict(await c.cursor_position())

        async def wait(args: WaitInput) -> dict:
            return _result_to_dict(await c.wait(args.seconds))

        async def bash(args: BashInput) -> dict:
            if s is not None:
                return _result_to_dict(await s.bash(args.command, args.timeout))
            return _result_to_dict(await c.bash(args.command, args.timeout))

        async def read_file(args: ReadFileInput) -> dict:
            assert s is not None  # only registered when the sandbox is configured
            return _result_to_dict(await s.read_file(args.path, args.view_range))

        async def write_file(args: WriteFileInput) -> dict:
            assert s is not None  # only registered when the sandbox is configured
            return _result_to_dict(await s.write_file(args.path, args.content))

        async def edit_file(args: EditFileInput) -> dict:
            assert s is not None  # only registered when the sandbox is configured
            return _result_to_dict(await s.edit_file(args.path, args.old_str, args.new_str))

        async def grep(args: GrepInput) -> dict:
            assert s is not None  # only registered when the sandbox is configured
            return _result_to_dict(
                await s.grep(
                    args.pattern,
                    args.path,
                    args.glob,
                    context=args.context,
                    ignore_case=args.ignore_case,
                    files_with_matches=args.files_with_matches,
                )
            )

        async def glob(args: GlobInput) -> dict:
            assert s is not None
            return _result_to_dict(await s.glob(args.pattern, args.path))

        # The file and search tools exist only on the ssh sandbox. Search needs
        # ripgrep on the far side, which the desktop agent's HTTP API cannot offer;
        # the file tools are gated for a different reason - without a sandbox this
        # server must expose exactly the tool set it exposed before SshSandbox
        # landed, so that an agent which never opted in sees no change at all.
        sandbox_tools = (
            [
                ToolDefinition(
                    name="grep",
                    description="Search file CONTENTS ON THE REMOTE DESKTOP VM with ripgrep.",
                    input_model=GrepInput,
                    handler=grep,
                ),
                ToolDefinition(
                    name="glob",
                    description="Find files BY PATH PATTERN ON THE REMOTE DESKTOP VM, e.g. '**/*.py'.",
                    input_model=GlobInput,
                    handler=glob,
                ),
                ToolDefinition(
                    name="read_file",
                    description=(
                        "Read a file ON THE REMOTE DESKTOP VM (numbered lines, optionally a line range), "
                        "or list a directory there. An image file (png/jpeg/gif/webp) comes back as a "
                        "viewable image rather than as text."
                    ),
                    input_model=ReadFileInput,
                    handler=read_file,
                ),
                ToolDefinition(
                    name="write_file",
                    description="Create or overwrite a file ON THE REMOTE DESKTOP VM with the given content.",
                    input_model=WriteFileInput,
                    handler=write_file,
                ),
                ToolDefinition(
                    name="edit_file",
                    description="Replace one exact occurrence of old_str with new_str in a file ON THE REMOTE DESKTOP VM.",
                    input_model=EditFileInput,
                    handler=edit_file,
                ),
            ]
            if s is not None
            else []
        )

        return sandbox_tools + [
            ToolDefinition(
                name="screenshot",
                description="Take a screenshot of the remote desktop's current screen.",
                input_model=ScreenshotInput,
                handler=screenshot,
            ),
            ToolDefinition(
                name="click",
                description="Click on the remote desktop at pixel coordinates (or the current cursor position). Returns a post-click screenshot.",
                input_model=ClickInput,
                handler=click,
            ),
            ToolDefinition(
                name="type_text",
                description="Type text on the remote desktop at the current keyboard focus. Returns a screenshot.",
                input_model=TypeTextInput,
                handler=type_text,
            ),
            ToolDefinition(
                name="key",
                description="Press a key or key combination on the remote desktop (e.g. 'Return', 'ctrl+c'). Returns a screenshot.",
                input_model=KeyInput,
                handler=key,
            ),
            ToolDefinition(
                name="scroll",
                description="Scroll the mouse wheel on the remote desktop at the given coordinates. Returns a screenshot.",
                input_model=ScrollInput,
                handler=scroll,
            ),
            ToolDefinition(
                name="drag",
                description="Drag the mouse (left button held) from start to end coordinates on the remote desktop. Returns a screenshot.",
                input_model=DragInput,
                handler=drag,
            ),
            ToolDefinition(
                name="mouse_move",
                description="Move the mouse cursor to pixel coordinates on the remote desktop. Returns a screenshot.",
                input_model=MouseMoveInput,
                handler=mouse_move,
            ),
            ToolDefinition(
                name="cursor_position",
                description="Get the current mouse cursor position on the remote desktop.",
                input_model=CursorPositionInput,
                handler=cursor_position,
            ),
            ToolDefinition(
                name="wait",
                description="Wait the given number of seconds, then take a screenshot of the remote desktop.",
                input_model=WaitInput,
                handler=wait,
            ),
            ToolDefinition(
                name="bash",
                description="Run a shell command ON THE REMOTE DESKTOP VM (not your own machine) and return its output. Use this to inspect or manipulate the desktop VM's filesystem.",
                input_model=BashInput,
                handler=bash,
            ),
        ]
