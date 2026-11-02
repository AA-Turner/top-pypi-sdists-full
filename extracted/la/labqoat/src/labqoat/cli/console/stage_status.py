"""The stage a run is in right now, drawn with a spinner and a running clock."""

import time
from datetime import UTC, datetime
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from rich.text import Text


class StageStatus:
    """Render the current stage afresh on every terminal refresh so its clock keeps moving."""

    frames: ClassVar[str] = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

    def __init__(self, label: str, since: datetime | None = None) -> None:
        """Start the clock when the stage began, or when it is first shown if the record carries no instant."""
        self.label = label
        behind = 0.0 if since is None else max(0.0, (datetime.now(UTC) - since).total_seconds())
        self.started = time.monotonic() - behind

    def __rich__(self) -> "Text":
        """One line: an animated mark, the stage, and how long it has lasted."""
        from rich.text import Text

        elapsed = time.monotonic() - self.started
        minutes, seconds = divmod(int(elapsed), 60)
        frame = self.frames[int(elapsed * 10) % len(self.frames)]
        name, _, detail = self.label.partition(" · ")
        clock = f"{minutes:02d}:{seconds:02d}".rjust(7)
        return Text.assemble(
            ("  " + frame, "cyan"),
            f" {name.ljust(22)}",
            (clock, "bright_black"),
            (f"  {detail}".rstrip(), "bright_black"),
        )
