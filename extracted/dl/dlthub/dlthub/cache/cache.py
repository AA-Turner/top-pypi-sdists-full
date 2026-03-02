from typing import Dict, Any, List, Type

import dlt
import os
from contextlib import contextmanager

from dlt import Pipeline, Schema
from dlt.common import logger
from dlt.common.exceptions import DltException, MissingDependencyException
from dlt import Relation

from dlt.destinations import duckdb as duckdb_destination
from dlt.destinations.exceptions import DatabaseUndefinedRelation
from dlt.destinations.dataset import ReadableDBAPIDataset
from dlthub.destinations.dataset import WritableDataset

try:
    from dlt.destinations.impl.duckdb.sql_client import WithTableScanners
    from dlt.destinations.impl.filesystem.sql_client import (
        FilesystemSqlClient as FilesystemSqlClient,
    )
except ImportError as import_ex:
    from dlthub import version

    raise MissingDependencyException(
        "transformations and local cache",
        [f"{version.PKG_NAME}[cache]"],
        "Install extras above to run local cache and transformations",
    ) from import_ex

from dlthub.cache.config import (
    CacheConfig,
    CacheInputBinding,
    set_defaults_and_validate,
    CacheBinding,
)


def create_cache(config: CacheConfig) -> "Cache":
    return Cache(config)


class CacheException(DltException):
    pass


class Cache:
    """A duckdb backed cache for working on data locally"""

    def __init__(self, config: CacheConfig) -> None:
        self.config = set_defaults_and_validate(config)

    def populate(self) -> None:
        """load data from the connected input datasets into cache"""
        # NOTE: At this moment only filesystem view mounts are supported
        self.verify_inputs()

        # collect datasets to load
        # tables_to_copy: Dict[str, Relation] = {}
        for cache_input in self.config["inputs"]:
            # filesystem destination tables can be mounted as views in most cases
            with self._get_table_scanner_sql_client(cache_input) as sql_client:
                # force view refreshing for bucket filesystem destinations
                sql_client.remote_client.config.always_refresh_views = True  # type: ignore[attr-defined]
                sql_client.create_views_for_tables(self._get_tables_for_input(cache_input))

        # NOTE: the below currently will not run ever,
        # as we are just linking filesystem views for now
        # later we can also copy data into the cache
        # for in_table, out_table in cache_input["tables"].items():
        #    tables_to_copy[out_table] = input_pipeline.dataset()[in_table]

        # @dlt.source()
        # def in_source():
        #     for name, dataset in tables_to_copy.items():
        #         yield dlt.resource(
        #             dataset.iter_arrow(500),
        #             name=name,
        #             write_disposition="replace",
        #         )

        # cache_pipeline.run(in_source())

    #
    # Outputs
    #
    def flush(self) -> None:
        """Flushes the results into the connected output datasets"""
        self.verify_outputs()

        cache_dataset = self.get_cache_dataset(transformed_data=True)

        for cache_output in self.config["outputs"]:
            # sync result tables into output dataset
            data: Dict[str, Relation] = {}

            for in_table, out_table in cache_output["tables"].items():
                data[out_table] = cache_dataset(
                    f"SELECT * FROM {in_table}", _execute_raw_query=True
                )

            @dlt.source()
            def out_source() -> Any:
                for name, dataset in data.items():
                    yield dlt.resource(
                        dataset.iter_arrow(50000), name=name, write_disposition="append"
                    )

            output_pipeline = self.get_binding_pipeline(cache_output)
            output_pipeline.run(
                out_source(),
                loader_file_format=cache_output.get("loader_file_format", None),  # type: ignore
            )

    def verify_outputs(self) -> None:
        """checks that we have tables for all defined output tables"""

        if len(self.config["outputs"]) != 1:
            raise CacheException("Currently only one output is supported.")

        cache_dataset = self.get_cache_dataset(transformed_data=True)

        for cache_output in self.config["outputs"]:
            for table in cache_output["tables"].keys():
                try:
                    cache_dataset(f"SELECT * FROM {table}", _execute_raw_query=True).fetchone()
                except DatabaseUndefinedRelation:
                    raise Exception(
                        f"Table {table} defined in output "
                        + f"{self.get_binding_pipeline(cache_output).dataset_name} does "
                        + "not exist in transformed dataset."
                    )

    #
    # Inputs
    #
    def verify_inputs(self) -> None:
        """connect to each input and verify specified tables exist in schema"""

        if len(self.config["inputs"]) != 1:
            raise CacheException("Currently only one input is supported.")

        for cache_input in self.config["inputs"]:
            input_dataset = self.get_binding_dataset(cache_input)

            for table in (cache_input.get("tables") or {}).keys():
                if not input_dataset[table].columns_schema:
                    raise Exception(
                        f"Table {table} doesn't exist in the input "
                        + f"dataset {input_dataset.dataset_name}"
                    )

    def discover_input_schema(self) -> Schema:
        """Sync all inputs and calculate the input schema"""
        self.verify_inputs()
        schema = Schema(self.config["pipeline_name"])
        for cache_input in self.config["inputs"]:
            input_dataset = self.get_binding_dataset(cache_input)
            for in_table, out_table in self._get_tables_for_input(cache_input).items():
                schema.tables[out_table] = input_dataset.schema.tables[in_table]

        return schema

    def _get_tables_for_input(self, cache_input: CacheInputBinding) -> Dict[str, str]:
        input_dataset = self.get_binding_dataset(cache_input)
        tables = cache_input.get("tables") or {}

        # no tables declared means sync all data tables
        if not tables:
            for t in input_dataset.schema.data_tables():
                tables[t["name"]] = t["name"]

        # add load id table
        tables[input_dataset.schema.loads_table_name] = input_dataset.schema.loads_table_name

        return tables

    #
    # Cache management
    #
    def drop(self) -> None:
        self.drop_input_dataset()
        self.drop_output_dataset()

    def drop_input_dataset(self) -> None:
        try:
            dataset_ = self.get_cache_dataset(False)
            with dataset_.sql_client as sql_client:
                sql_client.drop_dataset()
            logger.info(f"Dataset {dataset_.dataset_name} deleted")
        except DatabaseUndefinedRelation:
            logger.info(
                f"Cache input dataset {dataset_.dataset_name} does not exist. Nothing to do."
            )

    def drop_output_dataset(self) -> None:
        try:
            dataset_ = self.get_cache_dataset(True)
            with dataset_.sql_client as sql_client:
                sql_client.drop_dataset()
            logger.info(f"Dataset {dataset_.dataset_name} deleted")
        except DatabaseUndefinedRelation:
            logger.info(
                f"Cache output dataset {dataset_.dataset_name} does not exist. Nothing to do."
            )

    #
    # Managing secrets
    #
    @contextmanager
    def with_persistent_secrets(self) -> Any:
        try:
            self.create_persistent_secrets()
            yield
        finally:
            self.clear_persistent_secrets()

    def create_persistent_secrets(self) -> None:
        for cache_input in self.config["inputs"]:
            with self._get_table_scanner_sql_client(cache_input):
                pass
                # try:
                #     sql_client.create_authentication(
                #         sql_client.remote_client.config.bucket_url,
                #         sql_client.config.credentials,
                #         persistent=True,
                #         secret_name=self.secret_name_for_input(cache_input),
                #     )
                # except Exception:
                #     pass

    def clear_persistent_secrets(self) -> None:
        for cache_input in self.config["inputs"]:
            with self._get_table_scanner_sql_client(cache_input) as sql_client:
                for secret_name in sql_client.list_secrets():
                    sql_client.drop_secret(secret_name)
                # try:
                #     sql_client.drop_authentication(
                #         secret_name=self.secret_name_for_input(cache_input)
                #     )
                # except duckdb.InvalidInputException:
                #     pass

    def get_cache_input_dataset(self) -> WritableDataset:
        return self.get_cache_dataset(transformed_data=False)

    def get_cache_output_dataset(self) -> WritableDataset:
        return self.get_cache_dataset(transformed_data=True)

    @property
    def cache_location(self) -> str:
        """Returns the cache location ie. duckdb path"""
        cache_db_name = self.config["name"] + "_cache.duckdb"
        return os.path.join(self.config["location"], cache_db_name)

    def get_cache_dataset(self, transformed_data: bool = False) -> WritableDataset:
        dataset_name = (
            self.config["transformed_dataset_name"]
            if transformed_data
            else self.config["dataset_name"]
        )
        # TODO: pass input/output. the code that will extract relevant part of the schema
        #  form input and output datasets/schemas is missing so this our best approximation
        #  note that state and schemas dlt tables are not mapped, only load ids
        bindings: List[CacheBinding] = (
            self.config["outputs"] if transformed_data else self.config["inputs"]  # type: ignore
        )
        if len(bindings) == 0:
            # TODO: ad hoc schema, is this a valid use case when input/output dataset is
            # not at all defined?
            schema = Schema("dataset_name")
        else:
            schema = self.get_binding_dataset(bindings[0]).schema.clone(
                remove_processing_hints=True
            )
        # TODO: place cache location in transformation working dir
        # (same concept as pipeline working dir!)
        return WritableDataset(
            dataset_config={},
            dataset_name=dataset_name,
            destination=duckdb_destination(credentials=self.cache_location),
            schema=schema,
        )

    def get_cache_pipeline_for_dbt(self, dataset: ReadableDBAPIDataset) -> Pipeline:
        """This pipeline is used to pass info to dbt runner and really not needed
        It will never be ran
        """
        return dlt.pipeline(
            self.config["pipeline_name"],
            destination=duckdb_destination(credentials=self.cache_location),
            dataset_name=dataset.dataset_name,
        )

    def get_binding_pipeline(self, o: CacheBinding) -> Pipeline:
        """Get pipeline that connects to external dataset (input or output)"""
        # TODO: make this unique per output or something, not sure
        dataset = self.get_binding_dataset(o)
        pipeline_name = "cache_" + dataset._dataset_name + "_output"
        return dlt.pipeline(
            pipeline_name=pipeline_name,
            destination=dataset._destination,
            dataset_name=dataset._dataset_name,
        )

    #
    # Private helpers
    #
    def get_binding_dataset(self, i: CacheBinding) -> ReadableDBAPIDataset:
        dataset = i.get("dataset")
        if isinstance(dataset, ReadableDBAPIDataset):
            return dataset
        raise Exception(f"Dataset {dataset} is not a valid dataset or unresolved dataset")

    def _get_table_scanner_sql_client(self, cache_input: CacheInputBinding) -> WithTableScanners:
        input_dataset = self.get_binding_dataset(cache_input)
        destination_client = input_dataset.destination_client

        sql_client_class: Type[WithTableScanners] = input_dataset.sql_client_class  # type: ignore
        if not issubclass(sql_client_class, WithTableScanners):
            in_dest = input_dataset._destination.destination_type
            raise CacheException(
                "SqlClient must implement WithTableScanners in order to be used by cache. "
                "Currently only filesystem and pyiceberg destinations are supported. "
                f"Dataset {input_dataset._dataset_name} is on "
                f"{in_dest} destination which does not."
            )
        cache_input_dataset = self.get_cache_dataset()
        # open any connections if necessary
        with destination_client:
            return sql_client_class(
                remote_client=destination_client,
                dataset_name=cache_input_dataset.dataset_name,
                # cache_input_dataset is on duckdb so credentials will match
                cache_db=cache_input_dataset.destination_client.config.credentials,  # type: ignore[arg-type]
                persist_secrets=True,
            )
