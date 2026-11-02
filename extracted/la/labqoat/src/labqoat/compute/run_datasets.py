"""Assignment-owned typed row publication and verified materialized dataset access."""

import time
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import TYPE_CHECKING, TypeVar, cast
from uuid import uuid4

from labqoat._generated.dataset_publication import DatasetPublication
from labqoat.argument_codec import encode_result
from labqoat.compute.published_dataset import PublishedDataset
from labqoat.compute.value_codec import ValueCodec
from labqoat.dataset import Dataset
from labqoat.dataset_access.worker_dataset_provider import WorkerDatasetProvider
from labqoat.dataset_access.worker_dataset_requester import WorkerDatasetRequester
from labqoat.json_document import JsonValue
from labqoat.storage.cache_settings import CacheSettings
from labqoat.training.transfer_log import TransferLog
from labqoat.worker.worker_api import WorkerApi

if TYPE_CHECKING:
    from labqoat.compute.dataset_row_parts import DatasetRowParts

T = TypeVar("T")


@dataclass(frozen=True)
class RunDatasets:
    """Reuse service-owned materialization and verified readers with only scoped worker credentials."""

    api: WorkerApi
    root: Path
    log: TransferLog = field(default_factory=TransferLog)
    _views: dict[str, tuple[WorkerDatasetProvider, Path]] = field(default_factory=dict, compare=False, repr=False)

    def publish(self, name: str, *, row_type: type[T], rows: Iterable[T], key: str) -> Dataset[T]:
        """Durably accept typed rows of any count and follow committed terminal publication evidence."""
        from labqoat.compute.dataset_row_parts import DatasetRowParts
        from labqoat.data_layout.dataset_layout import DatasetLayout

        codec = ValueCodec(row_type)
        schema = codec.schema()
        parts = DatasetRowParts(self.root / "publications" / uuid4().hex, DatasetLayout.capture(schema))
        started = time.monotonic()
        try:
            for row in rows:
                parts.add(codec.encode(row))
            if not parts.paths and not parts.rows:
                raise ValueError(f"Dataset {name!r} has no rows: a dataset holds at least one, so skip publishing it")
            request: dict[str, JsonValue] = {"dataset": name, "schema": schema, "key": key, **self._source(parts, name)}
            publication = DatasetPublication.from_dict(self.api.json("POST", "/api/v1/worker/datasets", request))
        finally:
            parts.discard()
        if publication.status == "publishing":
            self.log.note(f"dataset {name}: rows received, building the revision")
            completed = self.api.completion(f"/api/v1/worker/datasets/{publication.id}/completion", "revision")
            publication = DatasetPublication.from_dict(completed)
        seconds = time.monotonic() - started
        if seconds >= self.log.announce_seconds:
            self.log.note(f"dataset {name}: published in {seconds:.1f}s", {"dataset": name, "seconds": seconds})
        return PublishedDataset.capture(publication, row_type)

    def _source(self, parts: "DatasetRowParts", name: str) -> dict[str, JsonValue]:
        """Send small publications inline; retain larger ones as ordered Parquet artifacts and name those."""
        if not parts.paths:
            return {"rows": parts.rows}
        from labqoat.training.assets.worker_asset_publisher import WorkerAssetPublisher

        parts.close()
        size = TransferLog.size(sum(path.stat().st_size for path in parts.paths))
        self.log.note(f"dataset {name}: uploading {len(parts.paths)} part file(s) ({size})")
        publisher = WorkerAssetPublisher(self.api, purpose="dataset", log=self.log)
        media_type = "application/vnd.apache.parquet"
        retained = [publisher.publish(path, media_type=media_type, name=path.name) for path in parts.paths]
        return {"files": [encode_result(asset) for asset in retained]}

    def rows(self, dataset: Dataset[T], split: str | None = None) -> Iterator[T]:
        """Decode verified Parquet records into authored dataclasses, optionally keeping one ``split``.

        The reader validates every row against the revision's schema, and a ``Dataset`` exists only when its
        row type has that same schema digest, so rows are rebuilt here without validating them a second time.
        """
        if split is not None and "split" not in {item.name for item in fields(dataset.row_type)}:  # type: ignore[arg-type]
            raise ValueError(
                f"{dataset.row_type.__name__} has no `split` field; declare one, for example "
                '`split: Literal["train", "validation", "test"]`, to keep every split in one dataset'
            )
        provider = self._provider(dataset)
        codec = ValueCodec(dataset.row_type)
        try:
            for row in provider.records(dataset.reference):
                if split is None or row.get("split") == split:
                    yield codec.restore(cast(JsonValue, row))
        finally:
            provider.close()

    def files(self, dataset: Dataset[T]) -> Path:
        """A read-only directory holding the revision's verified data files, as Parquet parts.

        Read whole columns or record batches with pyarrow (``pyarrow.dataset.dataset(path)``) when decoding rows one
        by one is too slow, for example to turn a token column into one array. The files stay until the run ends.
        """
        if dataset.id not in self._views:
            provider = self._provider(dataset)
            self._views[dataset.id] = (provider, provider.path(dataset.reference))
        return self._views[dataset.id][1]

    def _provider(self, dataset: Dataset[T]) -> WorkerDatasetProvider:
        """A verified reader of this one input revision under the assignment's credentials."""
        inputs = (dataset.reference,)
        return WorkerDatasetProvider(
            requester=WorkerDatasetRequester(self.api, inputs),
            inputs=inputs,
            root=self.root,
            cache=CacheSettings.worker(self.root / "assets"),
        )
