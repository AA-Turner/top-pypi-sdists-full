import os
from functools import partial
from typing import Dict, cast, List, Generator
import importlib

from dlt.destinations.impl.filesystem.sql_client import FilesystemSqlClient

from dlthub.legacy.transformations.base_transformation import Transformation

from dlt.destinations.exceptions import DatabaseUndefinedRelation

from dlthub.legacy.transformations.dataframes.decorators import (
    TransformationUtils,
    TTransformationFunc,
)

from duckdb import DuckDBPyConnection, CatalogException

FILE_NAME = "__init__.py"

TABLE_NAMES_QUERY = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = ?;
"""


class DataframeTransformation(Transformation):
    def render_transformation_layer(self, force: bool = False) -> None:
        """Renders a starting point for the t-layer"""
        schema = self.cache.discover_input_schema()
        # TODO: render arrow project
        os.makedirs(self.transformation_layer_path, exist_ok=True)

        file_path = os.path.join(self.transformation_layer_path, FILE_NAME)
        if os.path.exists(file_path):
            raise FileExistsError(
                f"The file {file_path} already exists. Cannot overwrite existing file."
            )
        # Open the arrow_run_template.py file
        vars = {"project_name": self.cache.config["name"]}
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self._get_template("dataframes_header_template.py", vars))

            transformations = []
            for table_name in schema.tables.keys():
                if table_name.startswith("_"):
                    continue
                f.write(
                    self._get_template(
                        "dataframes_table_template.py",
                        {
                            "table_name": table_name,
                            "stg_table_name": f"stg_{table_name}",
                            "stg_table_name_func": f"stg_{table_name}_transformation",
                            "table_name_func": f"{table_name}_transformation",
                        },
                    )
                )
                transformations.append(f"stg_{table_name}_transformation")
                transformations.append(f"{table_name}_transformation")

            vars = {
                "transformations": ",\n".join([
                    "        " + table_name for table_name in transformations
                ])
            }
            f.write(self._get_template("dataframes_transformation_group_template.py", vars))

    def _get_template(self, template_name: str, vars: Dict[str, str]) -> str:
        template_path = os.path.join(os.path.dirname(__file__), "templates", template_name)

        with open(template_path, "r", encoding="utf-8") as template_file:
            template_content = template_file.read()

        for key, value in vars.items():
            template_content = template_content.replace("{{ " + key + " }}", str(value))

        return template_content

    def _do_transform(self) -> None:
        cache_dataset = self.cache.get_cache_dataset()

        # create helpers to make qualified table names
        input_client = self.cache.get_cache_input_dataset().sql_client
        output_client = self.cache.get_cache_output_dataset().sql_client

        def make_qualified_input_table_name(table_name: str) -> str:
            return input_client.make_qualified_table_name(table_name)

        def make_qualified_output_table_name(table_name: str) -> str:
            return output_client.make_qualified_table_name(table_name)

        def existing_tables(connection: DuckDBPyConnection, dataset: str) -> List[str]:
            return [
                table_name
                for (table_name,) in connection.execute(TABLE_NAMES_QUERY, [dataset]).fetchall()
            ]

        # 2.
        # run transformations
        full_path = os.path.join(self.transformation_layer_path, FILE_NAME)
        spec = importlib.util.spec_from_file_location("module.name", full_path)
        transformations_group = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(transformations_group)

        # get the transformations
        transformations = cast(List[TTransformationFunc], transformations_group.transformations())

        # check that transformations have metadata
        for transformation in transformations:
            if not hasattr(transformation, "__transformation_args__"):
                raise ValueError(
                    f"Transformation {transformation} does not seem to be a valid "
                    "transformation function. Did you use the @transformation decorator?"
                )

        # execute transformations
        with cache_dataset.sql_client as client:
            # TODO: move logic elsewhere and make conditional on existence of `iceberg_scan` views
            # TODO: please fix soon!
            FilesystemSqlClient._setup_iceberg(client._conn)

            transformation_utils = TransformationUtils(
                make_qualified_input_table_name,
                make_qualified_output_table_name,
                existing_input_tables=partial(
                    existing_tables,
                    client._conn,
                    self.cache.get_cache_input_dataset()._dataset_name,
                ),
                existing_output_tables=partial(
                    existing_tables,
                    client._conn,
                    self.cache.get_cache_output_dataset()._dataset_name,
                ),
            )

            for transformation in transformations:
                table_name = transformation.__transformation_args__["table_name"]  # type: ignore
                materialization = transformation.__transformation_args__["materialization"]  # type: ignore
                write_disposition = transformation.__transformation_args__["write_disposition"]  # type: ignore
                table_name = transformation_utils.make_qualified_output_table_name(table_name)

                # here we just execute the function, all database manipulation happens inside
                if materialization == "sql":
                    result = transformation(client._conn, transformation_utils)
                    if result is not None:
                        raise ValueError(
                            f"Transformation {transformation} returned a non-None value. "
                            "Transformations with sql materialization should return None."
                        )
                # TODO: for these materializations we should hand over a readonly connection
                # to the transformation function
                elif materialization in ["table", "view"]:
                    # here we expect an sql string as the basis of a new table or view
                    t = transformation(client._conn, transformation_utils)
                    if isinstance(t, str):
                        if write_disposition == "replace":
                            client.execute(
                                f"CREATE OR REPLACE {materialization} {table_name} AS {t}"
                            )
                        elif write_disposition == "append" and materialization == "table":
                            try:
                                client.execute(f"INSERT INTO {table_name} {t}")
                            except (CatalogException, DatabaseUndefinedRelation):
                                client.execute(f"CREATE TABLE {table_name} AS {t}")
                        else:
                            raise ValueError(
                                f"Write disposition {write_disposition} is not supported for "
                                f"materialization {materialization}"
                            )
                    elif isinstance(t, Generator):
                        if materialization == "view":
                            raise ValueError("Views need to be created with an sql statement")
                        # here we expect a generator of batches, the first
                        # batch needs to create the table, the
                        # rest will be inserted as it arrives
                        is_first_batch = True
                        for batch in t:
                            if is_first_batch:
                                if write_disposition == "replace":
                                    client.execute(
                                        f"CREATE OR REPLACE TABLE {table_name} AS "
                                        "SELECT * from batch LIMIT 0"
                                    )
                                elif write_disposition == "append":
                                    client.execute(
                                        f"CREATE TABLE IF NOT EXISTS {table_name} AS "
                                        "SELECT * from batch LIMIT 0"
                                    )
                                else:
                                    raise ValueError(
                                        f"Write disposition {write_disposition} is not supported"
                                    )
                                is_first_batch = False
                            client.execute(f"INSERT INTO {table_name} SELECT * FROM batch")
                    else:
                        raise ValueError(
                            f"Transformation {transformation} returned an invalid type {type(t)}"
                        )
                else:
                    raise ValueError(f"Materialization {materialization} is not supported")
