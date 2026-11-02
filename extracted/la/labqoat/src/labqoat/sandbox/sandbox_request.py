"""One operation of the sandbox host protocol, independent of how it is carried."""

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

from labqoat.json_document import JsonValue


@dataclass(frozen=True)
class SandboxRequest:
    """A method and path with at most one body: a JSON document, bytes, or part of a local file to stream.

    A file body is the ``source_length`` bytes of ``source`` that start at ``source_start``.
    """

    method: str
    path: str
    query: Mapping[str, str] = field(default_factory=dict)
    document: Mapping[str, JsonValue] | None = None
    content: bytes | None = None
    source: Path | None = None
    source_start: int = 0
    source_length: int = 0
    timeout: float | None = None

    def headers(self) -> dict[str, str]:
        """Name the body's type, the exact length of raw bytes, and the sandbox concerned."""
        session = self.session()
        concerned = {} if session is None else {"X-Labqoat-Session": session}
        if self.document is not None:
            return {"Content-Type": "application/json", **concerned}
        if self.source is not None:
            length = str(self.source_length)
            return {"Content-Type": "application/octet-stream", "Content-Length": length, **concerned}
        if self.content is None:
            return concerned
        return {"Content-Type": "application/octet-stream", "Content-Length": str(len(self.content)), **concerned}

    def session(self) -> str | None:
        """Name the sandbox a request concerns, as its path spells it.

        Several hosts may be served under one name; requests naming one sandbox all reach the host that has it.
        A request about no sandbox in particular, such as reading capacity, may reach any of them.
        """
        segments = self.path.split("/")
        if len(segments) > 2:
            return segments[2]
        created = None if self.document is None else self.document.get("id")
        return quote(created, safe="") if isinstance(created, str) else None

    def encoded(self) -> bytes | None:
        """Return the bytes of an in-memory body; a streamed file is read by the transport."""
        if self.document is None:
            return self.content
        return json.dumps(self.document, separators=(",", ":"), allow_nan=False, ensure_ascii=False).encode()
