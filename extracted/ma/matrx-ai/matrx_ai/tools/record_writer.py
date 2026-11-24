"""The host's one record write, reached by the `task` and `project` tools.

A server host (aidream) injects ``record_writer`` through ``matrx_ai.configure``: it writes
one record through that record's registered Action (``task.create`` / ``task.update`` /
``task.delete`` / ``project.create`` / ``project.update``), so the record's rules run (a new
task's starting status, a timed task's zone, completing a repeating task rolls it forward)
and the write is one action run, door ``tool``, authority ``agent``. A CLIENT host injects
none and the tools keep writing through their own managers.

``trusted`` carries columns the record's field policy refuses that the tool reconciled itself
(``published_to_web`` and its stamps, ``shown_to``): the host writes them in the SAME write, so a
create is one insert, one version, one action run.

``because`` (optional) is why the agent writes it: ``{source_kind, source_id, said_by, exact_words}``, a pointer
to the source and the person's exact words. The host carries it to the action run and its task rule reads it
(an agent acting on something its person did not directly ask may be asked to propose). A tool passes it only
when the agent gave one.

Contract: ``matrx_ai._ext`` (``_RECORD_WRITER_KEY``).
"""

from __future__ import annotations

from typing import Any, Literal, Protocol

from matrx_ai._ext import get_record_writer

RecordOperation = Literal["create", "update", "delete"]


class RecordWriter(Protocol):
    async def __call__(
        self,
        *,
        operation: RecordOperation,
        noun: str,
        data: dict[str, Any],
        organization_id: str | None = None,
        trusted: dict[str, Any] | None = None,
        because: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None: ...


class RecordWriteRefused(Exception):
    """The host refused the write in words the caller can act on.

    ``error_type``: ``not_found`` (no such row for this person, or they may not change it),
    ``validation`` (a field or a record rule refused), ``refused`` (a policy said no).
    """

    def __init__(self, message: str, *, error_type: str = "validation", suggested_action: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.suggested_action = suggested_action


def host_record_writer() -> RecordWriter | None:
    """The host's record writer, resolved at call time; None on a client host."""
    return get_record_writer()


__all__ = ["RecordOperation", "RecordWriteRefused", "RecordWriter", "host_record_writer"]
