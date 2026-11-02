"""The product's name in tall letters, revealed one letter at a time."""

from __future__ import annotations

from typing import ClassVar


class Banner:
    """Six rows of block letters spelling ``labqoat``."""

    GLYPHS: ClassVar[dict[str, tuple[str, ...]]] = {
        "l": (" _ ", "| |", "| |", "| |", "|_|", "   "),
        "a": ("       ", "  __ _ ", " / _` |", "| (_| |", r" \__,_|", "       "),
        "b": (" _     ", "| |__  ", r"| '_ \ ", "| |_) |", "|_.__/ ", "       "),
        "q": ("       ", "  __ _ ", " / _` |", "| (_| |", r" \__, |", "    |_|"),
        "o": ("       ", "  ___  ", r" / _ \ ", "| (_) |", r" \___/ ", "       "),
        "t": (" _   ", "| |_ ", "| __|", "| |_ ", r" \__|", "     "),
    }
    NAME = "labqoat"

    @classmethod
    def rows(cls, letters: int) -> list[str]:
        """The first ``letters`` letters of the name as six rows; none yet is no rows at all."""
        shown = [cls.GLYPHS[letter] for letter in cls.NAME[:letters]]
        return ["  " + "".join(glyph[row] for glyph in shown) for row in range(6)] if shown else []
