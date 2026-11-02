"""Event-backed import waiting with bounded reconnects and publication handoff."""

from time import sleep

from labqoat._generated.dataset_import import DatasetImport
from labqoat._generated.dataset_publication import DatasetPublication
from labqoat.datasets_client import DatasetsClient
from labqoat.errors.import_failed_error import ImportFailedError
from labqoat.errors.transport_error import TransportError
from labqoat.reconnect_budget import ReconnectBudget


class ImportWaiter:
    """Retain the durable import identity across disconnected clients."""

    def __init__(self, client: DatasetsClient, import_id: str, max_reconnects: int) -> None:
        """Capture one import and a bounded transport recovery policy."""
        if max_reconnects < 0:
            raise ValueError("max_reconnects must be nonnegative")
        self.client, self.import_id, self.max_reconnects = client, import_id, max_reconnects

    def run(self) -> DatasetPublication:
        """Follow completion notifications and reread authoritative state at reconnect boundaries."""
        record = self.client.get_import(self.import_id)
        budget = ReconnectBudget(self.max_reconnects)
        while True:
            revision = self._revision(record)
            if revision is not None:
                return self.client.wait(revision)
            budget.opened()
            try:
                for _event in self.client.import_events(self.import_id):
                    break
            except TransportError:
                pass
            record = self.client.get_import(self.import_id)
            revision = self._revision(record)
            if revision is not None:
                return self.client.wait(revision)
            if budget.exhausted():
                raise TransportError(f"Import {self.import_id} stream reconnect limit exceeded.")
            sleep(budget.delay())

    @staticmethod
    def _revision(record: DatasetImport) -> str | None:
        """Keep import failures explicit, including the durable ID for later inspection."""
        if record.revision_id is None and record.status == "failed":
            raise ImportFailedError(record)
        return record.revision_id
