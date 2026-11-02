"""A directory inside a sandbox, as its host lists it."""

from dataclasses import dataclass

from labqoat.json_document import JsonDocument
from labqoat.sandbox.sandbox_entry import SandboxEntry


@dataclass(frozen=True)
class SandboxListing:
    """A directory's entries, hidden ones included, in name order; ``truncated`` when it held more than 500."""

    path: str
    entries: tuple[SandboxEntry, ...]
    truncated: bool

    @staticmethod
    def decode(document: JsonDocument) -> "SandboxListing":
        """Read a host's listing of one directory."""
        path = JsonDocument.expect_scalar(document["path"], str)
        entries = JsonDocument.expect_list(document["entries"])
        return SandboxListing(
            path,
            tuple(SandboxEntry.decode(path, JsonDocument.expect_dict(entry)) for entry in entries),
            JsonDocument.expect_scalar(document["truncated"], bool),
        )
