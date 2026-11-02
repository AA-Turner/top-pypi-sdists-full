"""Deduplicate shared-builder evidence without suppressing another logical run's lifecycle."""

from collections import OrderedDict

from labqoat.cli.console.console_entry import ConsoleEntry


class BuildReplay:
    """Builder sequence numbers are durable and ordered; retain bounded per-builder positions."""

    def __init__(self) -> None:
        """Allocate at most 256 recent builder positions."""
        self.positions: OrderedDict[str, int] = OrderedDict()

    def fresh(self, entry: ConsoleEntry) -> bool:
        """A shared line seen through two children is printed once, including in full mode."""
        source = entry.document.get("source")
        sequence = entry.document.get("seq")
        if entry.source != "build" or not isinstance(source, dict) or not isinstance(sequence, int):
            return True
        key = str(source.get("id", ""))
        if sequence <= self.positions.get(key, -1):
            return False
        self.positions[key] = sequence
        self.positions.move_to_end(key)
        if len(self.positions) > 256:
            self.positions.popitem(last=False)
        return True
