"""Event-backed publication waiting with bounded transport-recovery backoff."""

from time import sleep

from labqoat._generated.dataset_publication import DatasetPublication
from labqoat.datasets_client import DatasetsClient
from labqoat.errors.api_error import ApiError
from labqoat.errors.publication_failed_error import PublicationFailedError
from labqoat.errors.transport_error import TransportError
from labqoat.reconnect_budget import ReconnectBudget


class PublicationWaiter:
    """Retain the last delivered cursor across interrupted publication streams."""

    def __init__(self, client: DatasetsClient, revision_id: str, max_reconnects: int) -> None:
        """Capture a bounded reconnect policy and one immutable revision."""
        if max_reconnects < 0:
            raise ValueError("max_reconnects must be nonnegative")
        self._client = client
        self._revision_id = revision_id
        self._max_reconnects = max_reconnects
        self._cursor: str | None = None

    def run(self) -> DatasetPublication:
        """Use reads at entry and reconnect boundaries; idle progress follows SSE."""
        revision = self._client.get_revision(self._revision_id)
        budget = ReconnectBudget(self._max_reconnects)
        while True:
            if self._terminal(revision):
                return revision
            budget.opened()
            try:
                self._follow()
            except TransportError:
                pass
            except ApiError as error:
                if error.status != 422 or self._cursor is None:
                    raise
                self._cursor = None
            revision = self._client.get_revision(self._revision_id)
            if self._terminal(revision):
                return revision
            if budget.exhausted():
                raise TransportError("Publication stream reconnect limit exceeded.")
            sleep(budget.delay())

    def _follow(self) -> None:
        """Stop at terminal evidence without treating snapshots as authoritative results."""
        for event in self._client.events(self._revision_id, cursor=self._cursor):
            self._cursor = event.id
            if event.event in ("publication.ready", "publication.failed", "publication.deleted"):
                return
            if event.event == "publication.snapshot" and event.data.get("status") != "publishing":
                return

    @staticmethod
    def _terminal(revision: DatasetPublication) -> bool:
        """Failed publication remains an explicit typed failure with retained evidence."""
        if revision.status == "failed":
            raise PublicationFailedError(revision)
        return revision.status == "ready"
