from typing import Any, List, Optional, Union

from dlt.common.typing import TypedDict
from typing_extensions import Self

import dlt
from dlt.common.pipeline import LoadInfo
from dlt.common.destination.reference import TDestinationReferenceArg
from dlt.common.schema import Schema
from dlt.common.schema.typing import TWriteDisposition, TSchemaContract
from dlt.extract.hints import TResourceHints
from dlt.sources import DltResource
from dlt.destinations.dataset import ReadableDBAPIDataset


class DatasetConfig(TypedDict, total=False):
    destination: Optional[List[str]]
    contract: Optional[TSchemaContract]


class WritableDataset(ReadableDBAPIDataset):
    def __init__(
        self,
        dataset_config: DatasetConfig,
        destination: TDestinationReferenceArg,
        dataset_name: str,
        schema: Union[Schema, str, None] = None,
    ) -> None:
        super().__init__(destination, dataset_name, schema=schema)
        self.dataset_config = dataset_config or {}

    @classmethod
    def from_dataset(cls, dataset: ReadableDBAPIDataset) -> Self:
        """Converts readable dataset into writable one"""
        return cls({}, dataset._destination, dataset.dataset_name, dataset.schema)

    def save(
        self, data: Any, table_name: str, write_disposition: TWriteDisposition = "append"
    ) -> LoadInfo:
        """Saves `data` into a table `table_name`. Resource hints saved in schema will be used,
        otherwise new table will be created. `data` may also be an instance of dlt resource.

        """
        resource = self.data_to_resource(
            data, table_name=table_name, write_disposition=write_disposition
        )

        # TODO: generate short pipeline name
        pipeline = dlt.pipeline(
            pipeline_name=f"save_{table_name}_pipeline",
            dataset_name=self._dataset_name,
            destination=self._destination,
        )  # .drop()  # make sure we do not retry any pending data
        # we do not want to preserve pipeline state in the destination. incremental loads
        # must happen via regular pipelines
        pipeline.config.restore_from_destination = False

        # TODO: introduce external contracts that are applied for a single run of the pipeline
        # right now we'll modify the schema which is not what we want.
        if self.dataset_config.get("contract"):
            # TODO: this will not override table-level contract
            self.schema.set_schema_contract(self.dataset_config["contract"])
        # TODO: we'll need to create a pipeline with the correct schema when Dataset is multi-schema
        # TODO: use pipeline runner from pipeline manager
        info = pipeline.run(resource, schema=self.schema)
        # apply the (possibly) changed schema to dataset schema
        self._schema = pipeline.default_schema
        # note that info contains pipeline instance and metrics for further inspection
        return info

    def data_to_resource(
        self, data: Any, table_name: str, write_disposition: TWriteDisposition
    ) -> DltResource:
        """Converts `data` into a dlt resource to be loaded into `table_name"""
        table_schema = self.schema.tables.get(table_name)
        hints: TResourceHints
        if table_schema:
            hints = table_schema  # type: ignore[assignment]
        else:
            hints = dlt.mark.make_hints(table_name=table_name, write_disposition=write_disposition)
        # hints["schema_contract"] = "freeze"
        return DltResource.from_data(data, name=table_name, section=self._dataset_name, hints=hints)

    def __str__(self) -> str:
        msg = (
            f"Dataset {self._dataset_name} tables in logical schema "
            f"{self.schema.name}@v{self.schema.version}\n"
        )
        for table in self.schema.data_table_names():
            msg += f"{table}\n"
        return msg
