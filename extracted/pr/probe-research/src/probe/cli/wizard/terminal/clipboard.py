"""copy a report to the reader's clipboard (native tool, or OSC 52 over SSH) and the copy prompt."""

from __future__ import annotations

import base64
import os
import shutil
import sys


def _copy_to_clipboard(
    text: str, output, *, label: str = "Full report", compact: bool = False,
) -> str:
    """Prefer the local clipboard; SSH must address the reader's terminal.

    OSC 52 has no success acknowledgement, so report sending the request
    separately from a native clipboard command that completed successfully.
    """
    import base64
    import os
    import subprocess

    commands: list[tuple[list[str], str]] = []
    if not (os.environ.get("SSH_CONNECTION") or os.environ.get("SSH_TTY")):
        if sys.platform == "darwin":
            commands.append((["pbcopy"], "utf-8"))
        elif sys.platform == "win32":
            commands.append((["clip.exe"], "utf-16le"))
        else:
            if os.environ.get("WAYLAND_DISPLAY"):
                commands.append((["wl-copy"], "utf-8"))
            if os.environ.get("DISPLAY"):
                commands.extend([
                    (["xclip", "-selection", "clipboard"], "utf-8"),
                    (["xsel", "--clipboard", "--input"], "utf-8"),
                ])
    for command, encoding in commands:
        if not shutil.which(command[0]):
            continue
        try:
            subprocess.run(
                command,
                input=text.encode(encoding),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2,
                check=True,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        return f"{label} copied." if compact else f"{label} copied to clipboard."

    if interactive() and os.environ.get("TERM") != "dumb":
        payload = base64.b64encode(text.encode("utf-8")).decode("ascii")
        try:
            # https://www.invisible-island.net/xterm/ctlseqs/ctlseqs.html
            output.write_raw(f"\033]52;c;{payload}\a")
            output.flush()
        except OSError:
            pass
        else:
            return "Copy sent; paste to check." if compact else "Copy sent to terminal; paste to check clipboard support."
    return "Copy unavailable; select text." if compact else "Could not copy. Run `probe doctor` to get the report as text."


def _copy_prompt(text: str, message: str) -> str:
    """Copy on a single keypress and stay on the report until Enter/Escape."""
    from prompt_toolkit import PromptSession
    from prompt_toolkit.application import get_app_session
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.keys import Keys

    bindings = KeyBindings()
    status = ""

    @bindings.add("c")
    @bindings.add("C")
    def copy(event) -> None:
        nonlocal status
        status = _copy_to_clipboard(text, event.app.output)
        event.app.invalidate()

    @bindings.add("enter")
    @bindings.add("escape", eager=True)
    def back(event) -> None:
        event.app.exit(result="")

    @bindings.add(Keys.Any)
    @bindings.add(Keys.BracketedPaste)
    def ignore(event) -> None:
        pass

    def hint() -> str:
        lines = ([status] if status else []) + [f"c Copy full report · {message}"]
        return indent("\n".join(lines))

    # An explicit output keeps prompt_toolkit's TERM=dumb fallback from
    # replacing our single-key bindings with its default line input.
    return PromptSession(output=get_app_session().output).prompt(hint, key_bindings=bindings)
from probe.cli.wizard.terminal.forms import text  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.layout import indent  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.terminal import interactive  # noqa: E402 -- pieces need each other; the front door loads this one first
