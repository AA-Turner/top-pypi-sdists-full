"""Fixtures for trusted reconciliation workflow tests."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from agentic_devtools.cli.ci.reconciliation.reconciler import TrustedObservationProvider


class WorkflowProvider(TrustedObservationProvider):
    """Simple provider fixture for workflow reconciliation tests."""

    def __init__(self, pages: list[tuple[Sequence[Mapping[str, object]], str | None]]) -> None:
        self._pages = pages
        self._index = 0

    def list_pull_requests(self, *, cursor: str | None) -> tuple[Sequence[Mapping[str, object]], str | None]:
        del cursor
        page = self._pages[self._index]
        self._index += 1
        return page
