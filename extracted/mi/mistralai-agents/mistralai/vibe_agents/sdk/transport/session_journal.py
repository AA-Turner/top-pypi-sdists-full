"""Where a local root session is saved, so that a later process can continue it.

Experimental: ``mistralai.agents.experimental`` exports ``JsonFileSessionJournal``. The Harness
keeps the session's state; this class only says which file holds it.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from mistralai.vibe.harness.runtime.hosts.local import journal as harness_journal
from mistralai.vibe.harness.runtime.session.journal import SessionJournal

__all__ = ["JsonFileSessionJournal", "SessionJournals", "harness_journals"]

type SessionJournals = Callable[[str], JsonFileSessionJournal]


class JsonFileSessionJournal:
    """The JSON file that saves one local root session. Experimental: a minor release may change it.

    Pass ``JsonFileSessionJournal.in_directory("./sessions")`` as ``journal_factory=`` to
    ``agents.local_runtime()``, and each root session of the block is saved in
    ``./sessions/<session id>/``. A later process with the same agent and the same directory
    continues it with ``agent.session(session_id)``. An ``agent.run()`` in the block saves its
    session too. The factory is fixed when the event loop's runtime starts: entering a block with
    another one while the runtime runs raises ``SdkError``.

    The uploads that its messages linked are saved next to the file, in ``<file stem>.files``.
    """

    __slots__ = ("_path",)

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self._path = Path(path)

    @property
    def path(self) -> Path:
        """The JSON file of the session."""
        return self._path

    @classmethod
    def in_directory(cls, directory: str | os.PathLike[str]) -> SessionJournals:
        """Return the ``journal_factory`` that saves each session in ``directory/<session id>/session.json``.

        Args:
            directory: The folder that holds the saved sessions.
        """
        return _InDirectory(Path(directory))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, JsonFileSessionJournal):
            return NotImplemented
        return self._path == other._path

    def __hash__(self) -> int:
        return hash((JsonFileSessionJournal, self._path))

    def __repr__(self) -> str:
        return f"JsonFileSessionJournal({str(self._path)!r})"


@dataclass(frozen=True, slots=True)
class _InDirectory:
    """A journal factory that two calls of ``in_directory`` with one directory build equal."""

    directory: Path

    def __call__(self, session_id: str) -> JsonFileSessionJournal:
        # The session id names a directory, so it must not leave ``directory``.
        if session_id in {"", ".", ".."} or Path(session_id).name != session_id:
            raise ValueError(f"Session id {session_id!r} cannot name a journal directory")
        return JsonFileSessionJournal(self.directory / session_id / "session.json")

    def __repr__(self) -> str:
        return f"JsonFileSessionJournal.in_directory({str(self.directory)!r})"


def harness_journals(journals: SessionJournals) -> Callable[[str], SessionJournal]:
    """The Harness journal factory that saves each session where ``journals`` says."""

    def journal(session_id: str) -> SessionJournal:
        saved = journals(session_id)
        if not isinstance(saved, JsonFileSessionJournal):
            raise TypeError(
                "journal_factory= must return a mistralai.agents.experimental.JsonFileSessionJournal, "
                f"got {type(saved).__name__}"
            )
        return harness_journal.JsonFileSessionJournal(saved.path)

    return journal
