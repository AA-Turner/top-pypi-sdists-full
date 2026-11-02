"""InlineImageProtocol: which protocol this terminal draws images with (read from the environment), draw and forget an agent's logo."""

from __future__ import annotations

import base64
import os
import sys

from probe.foundation.compat.compat import StrEnum


class ImageProtocol(StrEnum):
    """How this terminal draws an image into its cells, when it can at all."""

    KITTY = "kitty"  # kitty, Ghostty, WezTerm, Warp
    ITERM = "iterm"  # iTerm2's OSC 1337 inline images


#: `off` draws the agents' names instead of their logos; `kitty` or `iterm`
#: forces that protocol on a terminal this module does not recognise.
ICONS_ENV = "PROBE_WIZARD_ICONS"

#: Kitty image ids are per terminal window, so ours sit far from the small
#: numbers another program in the same window would pick.
IMAGE_ID_BASE = 0x50524200


def image_protocol() -> ImageProtocol | None:
    """The protocol this terminal draws images with, or None for names.

    Read from the environment, never asked of the terminal: an answer arrives
    on stdin, where the menu would read it as keystrokes. A multiplexer (tmux,
    screen) swallows the escapes unless configured to pass them through, so
    it gets names too.
    """
    choice = os.environ.get(ICONS_ENV, "").strip().lower()
    if choice in {"0", "off", "false", "no"}:
        return None
    if choice in {protocol.value for protocol in ImageProtocol}:
        return ImageProtocol(choice)
    if not sys.stdout.isatty():
        return None
    term = os.environ.get("TERM", "")
    program = os.environ.get("TERM_PROGRAM", "")
    if os.environ.get("TMUX") or os.environ.get("STY") or term.startswith(("screen", "tmux")):
        return None
    if (term in {"xterm-kitty", "xterm-ghostty"} or os.environ.get("KITTY_WINDOW_ID")
            or program in {"ghostty", "WezTerm", "WarpTerminal"}):
        return ImageProtocol.KITTY
    if program == "iTerm.app":
        return ImageProtocol.ITERM
    return None


def image_escape(png: bytes, protocol: ImageProtocol, *, cells: int, image_id: int) -> str:
    """Draw `png` over the `cells` cells LEFT of the cursor; the cursor stays put.

    Saved and restored around the drawing (DECSC/DECRC) rather than trusting
    each terminal's cursor rule for images: prompt_toolkit moves the cursor
    relative to where it believes it is, and one cell of drift shifts every
    character after it on the row.
    """
    data = base64.standard_b64encode(png).decode()
    if protocol is ImageProtocol.KITTY:
        # q=2: no reply, which would reach stdin as keystrokes. C=1: no cursor move.
        keys = f"a=T,f=100,t=d,i={image_id},p=1,c={cells},r=1,C=1,q=2,"
        chunks = [data[at:at + 4096] for at in range(0, len(data), 4096)] or [""]
        body = "".join(
            f"\x1b_G{keys if not index else ''}m={int(index < len(chunks) - 1)};{chunk}\x1b\\"
            for index, chunk in enumerate(chunks)
        )
    else:
        body = (f"\x1b]1337;File=inline=1;size={len(png)};width={cells};height=1;"
                f"preserveAspectRatio=1;doNotMoveCursor=1:{data}\x07")
    return f"\x1b7\x1b[{cells}D{body}\x1b8"


def forget_images(protocol: ImageProtocol | None, count: int) -> str:
    """Delete the menu's logos. Kitty keeps an image on its own layer until told
    to drop it, so without this they would sit on top of the next screen; an
    iTerm2 image is cell content and goes with the text drawn over it."""
    if protocol is not ImageProtocol.KITTY:
        return ""
    return "".join(f"\x1b_Ga=d,d=I,i={IMAGE_ID_BASE + index},q=2\x1b\\" for index in range(count))
