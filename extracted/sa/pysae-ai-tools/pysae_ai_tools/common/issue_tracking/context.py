"""The repository coordinates a provider operates on."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RepoContext:
    """Where a provider acts: the project and its owner namespace.

    ``project`` is the host identifier (a ``group/repo`` path or a numeric id);
    ``owner`` is the top-level namespace holding the group-scoped labels and
    epics (the ``owner`` field of ``detect-context``); ``url`` is the repo URL.
    """

    project: str = ""
    owner: str = ""
    url: str = ""
