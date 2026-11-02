"""The goat the CLI draws: still for pipes, and acting out what someone watching a terminal asks of it."""

from __future__ import annotations

from typing import ClassVar


class Goat:
    """A front-facing goat with swept horns, ears and a beard, drawn in thirteen lines."""

    REST = ("o", "__", "||", 0)
    SCENES: ClassVar[dict[str, tuple[tuple[str, str, str, int], ...]]] = {
        "greet": (("o", "~~", "//", 0), REST, ("o", "~~", "\\\\", 0), ("-", "__", "||", 0), REST),
        "feed": (("o", "~~", "//", 0), ("o", "__", "||", 0), ("o", "~~", "\\\\", 0), ("o", "__", "||", 0)) * 2,
        "pet": (
            ("^", "__", "||", 0),
            ("^", "~~", "//", 0),
            ("^", "__", "||", 0),
            ("^", "~~", "\\\\", 0),
            ("^", "__", "||", 0),
        ),
        "butt": (
            ("o", "__", "||", 0),
            ("-", "__", "||", 0),
            (">", "__", "//", 6),
            (">", "__", "//", 14),
            ("o", "__", "||", 4),
            REST,
        ),
        "dance": (
            ("^", "__", "//", 0),
            ("^", "~~", "\\\\", 4),
            ("^", "__", "//", 8),
            ("^", "~~", "\\\\", 4),
            ("^", "__", "//", 0),
            ("^", "~~", "\\\\", 4),
            ("^", "__", "//", 8),
            ("^", "~~", "||", 4),
            ("^", "__", "||", 0),
        ),
        "idle": (
            REST,
            ("o", "~~", "//", 0),
            REST,
            ("o", "~~", "\\\\", 0),
            REST,
            REST,
            ("-", "__", "||", 0),
            REST,
            ("o", "~~", "//", 0),
            ("o", "__", "\\\\", 0),
        ),
        "sleep": (("-", "__", "||", 0), ("-", "__", "//", 0), ("-", "__", "||", 0), ("-", "__", "\\\\", 0)),
    }

    @staticmethod
    def frame(eye: str, jaw: str, beard: str, shift: int = 0) -> list[str]:
        """One pose as lines: the eyes, the chewing jaw, the swaying beard and a lunge sideways are what move."""
        lines = [
            r"   (\              /)",
            r"    \\            //",
            r"     \\    __    //",
            r"      \\__/  \__//",
            r"   ___/          \___",
            rf"  '--.   {eye}    {eye}   .--'",
            r"      \          /",
            r"       \   ..   /",
            rf"        \  {jaw}  /",
            r"         '.__.'",
            f"           {beard}",
            f"           {beard}",
            r"           ''",
        ]
        return [" " * shift + line for line in lines]

    @classmethod
    def still(cls) -> str:
        """The goat at rest."""
        return "\n".join(cls.frame(*cls.REST))

    @classmethod
    def scene(cls, name: str) -> list[list[str]]:
        """The poses of one act, in order, each ready to be drawn over the last."""
        return [cls.frame(*pose) for pose in cls.SCENES[name]]
