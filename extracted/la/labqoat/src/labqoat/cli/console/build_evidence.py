"""Bounded per-run build tails retain late diagnostics without mixing sibling builds."""

from collections import OrderedDict, deque

from labqoat.cli.console.console_entry import ConsoleEntry


class BuildEvidence:
    """Track only recent build contexts and never infer failures from output text."""

    def __init__(self) -> None:
        """Allocate bounded state lazily as each build is observed."""
        self.tails: OrderedDict[str, deque[ConsoleEntry]] = OrderedDict()
        self.failed: set[str] = set()

    @staticmethod
    def key(entry: ConsoleEntry) -> str:
        """Use the logical owner so sibling failure output remains independent."""
        source = entry.document.get("source")
        if entry.source == "build" and isinstance(source, dict) and source.get("id"):
            return str(source["id"])
        data = entry.document.get("data")
        if isinstance(data, dict) and data.get("build_id"):
            return str(data["build_id"])
        return str(entry.document.get("run_id") or entry.document.get("run_path") or "")

    def accept(self, entry: ConsoleEntry) -> list[ConsoleEntry]:
        """Return newly available failure diagnostics, including arrivals after failure."""
        key = self.key(entry)
        if key not in self.tails:
            self.tails[key] = deque(maxlen=20)
        self.tails.move_to_end(key)
        if len(self.tails) > 128:
            oldest, _tail = self.tails.popitem(last=False)
            self.failed.discard(oldest)
        if entry.source == "build":
            if key in self.failed:
                return [entry]
            self.tails[key].append(entry)
        data = entry.document.get("data")
        reason = data.get("reason") if isinstance(data, dict) else None
        if entry.kind == "submission.build.failed" or reason == "build_failed":
            self.failed.add(key)
            return self.drain(key)
        return []

    def drain(self, key: str = "") -> list[ConsoleEntry]:
        """Take each retained line once after authoritative build failure."""
        tail = self.tails.get(key, deque())
        result = list(tail)
        tail.clear()
        return result

    def recent(self, entry: ConsoleEntry) -> list[str]:
        """Read the live window for this owner without consuming failure evidence."""
        return [line.content for line in self.tails.get(self.key(entry), ())]
