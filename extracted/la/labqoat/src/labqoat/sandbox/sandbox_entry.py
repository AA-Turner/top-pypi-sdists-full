"""One entry of a directory inside a sandbox."""

import posixpath
from dataclasses import dataclass
from datetime import datetime

from labqoat.json_document import JsonDocument


@dataclass(frozen=True)
class SandboxEntry:
    """A directory entry's name, absolute path, kind, size and modification time.

    ``kind`` is ``dir``, ``file``, ``link`` or ``other``. A directory has no size, and an image without
    ``stat`` reports neither sizes nor times.
    """

    name: str
    path: str
    kind: str
    size: int | None
    modified_at: datetime | None

    @property
    def is_dir(self) -> bool:
        """Report whether the entry is a directory, not a link to one."""
        return self.kind == "dir"

    @staticmethod
    def decode(directory: str, document: JsonDocument) -> "SandboxEntry":
        """Read one entry of a host's listing of ``directory``."""
        name = JsonDocument.expect_scalar(document["name"], str)
        modified_at = JsonDocument.expect_optional_scalar(document["modified_at"], str)
        return SandboxEntry(
            name,
            posixpath.join(directory, name),
            JsonDocument.expect_scalar(document["type"], str),
            JsonDocument.expect_optional_scalar(document["size"], int),
            None if modified_at is None else datetime.fromisoformat(modified_at),
        )
