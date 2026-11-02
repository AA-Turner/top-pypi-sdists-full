"""Collapse adjacent repeated application lines while preserving immediate first delivery."""

from labqoat.cli.console.console_entry import ConsoleEntry
from labqoat.json_document import JsonDocument


class ConsoleRepeats:
    """Retain one human-readable record; raw JSON evidence is never compressed."""

    def __init__(self) -> None:
        """Keep bounded repeat state independently of the duration of a run."""
        self.last: ConsoleEntry | None = None
        self.count = 0
        self.siblings = False

    def accept(self, entry: ConsoleEntry) -> list[ConsoleEntry]:
        """Print the first line now and summarize subsequent identical application records."""
        entry.content = "\n".join(line.rstrip("\r").rsplit("\r", 1)[-1] for line in entry.content.split("\n"))
        previous = self.last
        if previous is not None and self.same(previous, entry):
            self.count += 1
            self.siblings |= previous.document.get("run_path") != entry.document.get("run_path")
            return []
        output = self.flush()
        if entry.source in ("stdout", "stderr", "logging"):
            self.last, self.count = entry, 1
        return [*output, entry]

    @staticmethod
    def same(previous: ConsoleEntry, entry: ConsoleEntry) -> bool:
        """Level and source remain significant even when message text happens to match."""
        return (previous.source, previous.level, previous.content) == (entry.source, entry.level, entry.content)

    def flush(self) -> list[ConsoleEntry]:
        """Release one repeat summary before unrelated output or a finite-page boundary."""
        output = []
        if self.last is not None and self.count > 1:
            suffix = " across sibling runs" if self.siblings else ""
            record = JsonDocument(self.last.document, content=f"[repeated {self.count}x{suffix}]")
            output.append(ConsoleEntry(record))
        self.last, self.count, self.siblings = None, 0, False
        return output
