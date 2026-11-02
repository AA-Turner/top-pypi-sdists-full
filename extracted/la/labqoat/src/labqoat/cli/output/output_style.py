"""Choose between terminal presentation and the compact form read by agents and pipes."""

import os
from typing import IO


class OutputStyle:
    """Let people see designed output while redirected output stays small and escape-free."""

    @staticmethod
    def current(stream: IO[str]) -> str:
        """Honor LABQOAT_OUTPUT=pretty|compact, otherwise follow whether the stream is a terminal."""
        chosen = os.environ.get("LABQOAT_OUTPUT", "auto")
        if chosen in ("pretty", "compact"):
            return chosen
        return "pretty" if stream.isatty() else "compact"

    @staticmethod
    def interactive(stream: IO[str]) -> bool:
        """Whether a person is watching this stream live, so moving displays are worth drawing."""
        return OutputStyle.current(stream) == "pretty" and stream.isatty()
