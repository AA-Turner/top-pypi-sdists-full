from __future__ import absolute_import

import logging
import uuid
import warnings
from typing import Any, Optional

import pandas as pd
from teradataml import DataFrame, execute_sql

from tmo.api.base_entity_api import BaseEntityApiMixin
from tmo.types.dataset_metadata import (
    CatalogBodyType,
    CatalogType,
    DataType,
    FeatureMetadata,
    FeaturesEntityTargets,
    Metadata,
    Predictions,
    TypeEnum,
    Variable,
)
from tmo.types.dataset_template import DatasetTemplate
from tmo.types.exceptions import EntityCreationError

logger = logging.getLogger(__name__)


class DatasetTemplateApi(BaseEntityApiMixin):
    name = "Dataset Template API"
    path = "datasetTemplates"
    type = "DATASET_TEMPLATE"

    def create(
        self,
        name: str = "SDK Dataset Template",
        columns: dict[str, list[str]] = None,
        dataframe: Optional[DataFrame | pd.DataFrame] = None,
        database: Optional[str] = "TD_MODELOPS",
        tables: Optional[dict] = None,
        sql: Optional[dict] = None,
        description: Optional[str] = "SDK dataset template",
        catalog_type: Optional[CatalogType] = CatalogType.VANTAGE,
    ) -> DatasetTemplate:
        """
        Initialize a DatasetTemplate object.

        Parameters:
            name (str): The name of the dataset template
            description (str): A brief description of the dataset template. (Default is "VANTAGE dataset template")
            columns (list[str]): A list containing the target and entity columns in the dataset template
            dataframe (DataFrame): The dataframe to be used for creating the dataset template
            database (str, optional): The name of the database. (Default is "td_modelops")
            catalog_type (CatalogType, optional): The type of catalog to use. (Default is "VANTAGE")
            tables (dict, optional): A dictionary containing the table names for feature metadata, data, and predictions. If None, the tables will be automatically created using the dataset template name as a base.
                - data: Contains entity, features and targets.
                - features: Contains features.  If not present data table will be used.
                - entityTarget: Contains entity and targets. If not present data table will be used.
                - featureMetadata: Stores metadata about the features.
                - predictions: Holds prediction results generated during model evaluation.
            sql (dict, optional): A dictionary containing the SQL queries for features, entity and target, and predictions. If None, the SQL queries will be automatically generated based on the provided dataframe.
                Required sql queries:
                - features: SQL query for extracting features
                - target_entity: SQL query for extracting entity and targets
                - predictions: SQL query for generating predictions

        Returns:
            dict: The created dataset template.

        Example:
            ```python
            from tmo import TmoClient
            from teradataml import DataFrame

            con = create_context(host="10.15.126.184",username="admin",password="admin",database="td_modelops")

            data = DataFrame.from_table("PIMA")

            vmoClient = TmoClient()

            dataset_template = (
                vmoClient
                .dataset_templates()
                .create(
                    name="New Dataset Template",
                    columns={
                        "entity": ["PatientId"],
                        "targets": ["HasDiabetes"],
                    },
                    dataframe=data,
                    database="my_database",
                    tables={
                        "data": "pima_patient_data",
                        "featureMetadata": "pima_statistics_metadata",
                        "predictions": "pima_predictions",
                    },
                    sql={
                        "features": "SELECT * FROM pima_patient_data",
                        "target_entity": "SELECT * FROM pima_patient_diagnoses",
                        "predictions": "SELECT * FROM pima_patient_data F WHERE F.patientId MOD 5 = 0",
                    }
                )
            )
            ```
        """

        sql = sql or {}
        tables = tables or {}
        columns = columns or {}

        if (
            columns is None
            or not isinstance(columns, dict)
            or "entityColumns" not in columns
            or "targetColumns" not in columns
        ):
            raise ValueError(
                "Columns must be a dictionary with 'entityColumns' and 'targetColumns'"
                " keys."
            )

        if dataframe is None or not isinstance(dataframe, DataFrame):
            raise ValueError("Dataframe must be a valid teradataml DataFrame object.")

        entity_columns = columns["entityColumns"]
        target_columns = columns["targetColumns"]

        dataset_template = DatasetTemplate()
        dataset_template.name = name
        dataset_template.description = description
        dataset_template.catalog_type = catalog_type
        dataset_template.entity = entity_columns[0]
        dataset_template.target = target_columns

        data_table = tables.get(
            "data", f"{dataset_template.name.replace(' ', '_')}_data"
        )
        entity_target_table = tables.get("entityTarget", data_table)
        feature_metadata_table = tables.get(
            "featureMetadata",
            f"{dataset_template.name.replace(' ', '_')}_feature_metadata",
        )
        predictions_table = tables.get(
            "predictions", f"{dataset_template.name.replace(' ', '_')}_predictions"
        )

        dataframe.to_sql(
            table_name=data_table, schema_name=database, if_exists="replace"
        )

        dataframe = dataframe.to_pandas()

        column_names = dataframe.columns
        column_dtypes = [str(dtype) for dtype in dataframe.dtypes]

        feature_columns_objects = [
            Variable()
            .set_name(col)
            .set_data_type(self._infer_data_type_from_dtype(dtype))
            .set_type(TypeEnum.FEATURE)
            for col, dtype in zip(column_names, column_dtypes)
            if col not in entity_columns + target_columns
        ]

        entity_columns_objects = [
            Variable()
            .set_name(col)
            .set_data_type(self._infer_data_type_from_dtype(dataframe[col].dtype))
            .set_type(TypeEnum.ENTITY)
            for col in entity_columns
        ]

        target_columns_objects = [
            Variable()
            .set_name(col)
            .set_data_type(self._infer_data_type_from_dtype(dataframe[col].dtype))
            .set_type(TypeEnum.TARGET)
            for col in target_columns
        ]

        self._create_tables(
            target_columns_objects,
            entity_columns,
            database,
            predictions_table,
            feature_metadata_table,
        )

        feature_metadata, metadata = self._build_metadata(
            entity_columns,
            target_columns,
            feature_columns_objects,
            entity_columns_objects,
            target_columns_objects,
            sql,
            database,
            data_table,
            entity_target_table,
            predictions_table,
            feature_metadata_table,
        )

        dataset_template.feature_metadata = feature_metadata
        dataset_template.metadata = metadata

        template_request = {
            "name": dataset_template.name,
            "description": dataset_template.description,
            "catalogType": dataset_template.catalog_type.value,
            "metadata": {
                "features": {
                    "sql": dataset_template.metadata.features.sql,
                    "entity": dataset_template.metadata.features.entity,
                    "variables": [
                        {
                            "name": col.name,
                            "dataType": col.data_type.value,
                            "type": col.type.value,
                        }
                        for col in dataset_template.metadata.features.variables
                    ],
                },
                "entityAndTargets": {
                    "entity": dataset_template.entity,
                    "sql": dataset_template.metadata.entity_and_targets.sql,
                    "variables": [
                        {
                            "name": col.name,
                            "dataType": col.data_type.value,
                            "type": col.type.value,
                        }
                        for col in (
                            dataset_template.metadata.entity_and_targets.variables
                        )
                    ],
                },
                "predictions": {
                    "database": dataset_template.metadata.predictions.database,
                    "entitySql": dataset_template.metadata.predictions.entity_sql,
                    "table": dataset_template.metadata.predictions.table,
                },
                "type": dataset_template.metadata.type.value,
            },
            "featureMetadata": {
                "database": dataset_template.feature_metadata.database,
                "table": dataset_template.feature_metadata.table,
            },
        }

        response = self.tmo_client.post_request(
            path=self.base_path + self.path,
            header_params=self._get_header_params(),
            query_params={},
            body=template_request,
        )

        dataset_template_id = uuid.UUID(response["id"])
        dataset_template.id = dataset_template_id

        logger.debug("Dataset template created successfully.")

        return dataset_template

    def render(self, id: str | uuid.UUID) -> dict:
        """
        returns a rendered dataset template

        Parameters:
           id (str): dataset_template id

        Returns:
            (dict): rendered dataset template
        """
        return self.tmo_client.get_request(
            path=f"{self.base_path + self.path}/{str(id)}/render",
            header_params=self._get_header_params(),
            query_params={},
        )

    def find_by_name_like(
        self, name: str, projection: str = None, return_dataframe: bool = False
    ) -> None | list[Any] | DataFrame:
        """
        returns datasets matching the name as a combined DataFrame or list

        Parameters:
            name (str): dataset name(string) to find
            projection (str): projection type
            return_dataframe (bool): if True, returns combined DataFrame; if False, returns list of Dataset objects

        Returns:
            (list): dataset template
        """
        response = self.build_get_request(
            "/search/findByName", {"name": name}, projection
        )

        return self.process_entities_response(
            response, return_dataframe, f" with name like: {name}"
        )

    @staticmethod
    def _build_metadata(
        entity_columns: list[str],
        target_columns: list[str],
        feature_columns_objects: list[Variable],
        entity_columns_objects: list[Variable],
        target_columns_objects: list[Variable],
        sql: Optional[dict],
        database: str,
        data_table: str,
        entity_target_table: str,
        predictions_table: str,
        feature_metadata_table: str,
    ) -> tuple[FeatureMetadata, Metadata]:
        # Build the 'features' metadata section
        features = FeaturesEntityTargets()
        features.entity = entity_columns[0]

        if sql and "features" in sql:
            logger.debug(f"Using custom SQL for features section: {sql['features']}")
            features.sql = sql["features"]
        else:
            features_table = data_table
            query = (
                f"SELECT {entity_columns[0]},"
                f" {', '.join([col.name for col in feature_columns_objects])} FROM"
                f" {features_table}"
            )
            logger.debug(f"Using data table for features SQL: {features_table}")
            features.sql = query
        features.variables = feature_columns_objects

        # Build the 'entityAndTargets' metadata section (entity + target columns)
        entity_and_targets = FeaturesEntityTargets(entity=entity_columns[0])

        if sql and "target_entity" in sql:
            logger.debug(
                f"Using custom SQL for entityAndTargets section: {sql['target_entity']}"
            )
            entity_and_targets.set_sql(sql["target_entity"])
        else:
            logger.debug(
                f"Using data table for entityAndTargets SQL: {entity_target_table}"
            )
            query = (
                f"SELECT {entity_columns[0]}, {', '.join(target_columns)} FROM"
                f" {entity_target_table}"
            )
            entity_and_targets.set_sql(query)
        entity_and_targets.set_variables(
            entity_columns_objects + target_columns_objects
        )

        # Create predictions object with custom SQL if available
        predictions = Predictions(database=database, table=predictions_table)
        if sql and "predictions" in sql:
            logger.debug(f"Using custom SQL for predictions: {sql['predictions']}")
            predictions.set_entity_sql(sql["predictions"])
        else:
            query = (
                f"SELECT {entity_columns[0]}, {', '.join(target_columns)} FROM"
                f" {data_table}"
            )
            logger.debug(
                "Custom SQL for predictions not provided. Using auto-generated SQL:"
                f" {query}"
            )
            predictions.set_entity_sql(query)

        feature_metadata = FeatureMetadata(database, feature_metadata_table)

        metadata = Metadata(
            type=CatalogBodyType.VANTAGE,
            predictions=predictions,
            entity_and_targets=entity_and_targets,
            features=features,
        )

        return feature_metadata, metadata

    @staticmethod
    def _create_tables(
        target_columns_objects: list[Variable],
        entity_columns: list[str],
        database: str,
        predictions_table: str,
        feature_metadata_table: str,
    ):
        # Create the predictions table schema
        def get_sql_type(data_type: DataType) -> str:
            """Map DataType enum to SQL type."""
            if data_type == DataType.FLOAT:
                return "FLOAT"
            elif data_type == DataType.INTEGER:
                return "INTEGER"
            else:  # DataType.VARCHAR
                return "VARCHAR(40000)"

        predictions_table_schema = ", ".join([
            f"{col.name} {get_sql_type(col.data_type)}"
            for col in target_columns_objects
        ])

        predictions_table_schema = (
            f"job_id VARCHAR(128), {entity_columns[0]} VARCHAR(128),"
            f" {predictions_table_schema}, json_report CLOB"
        )

        create_predictions_table_query = f"""CREATE TABLE "{database}"."{predictions_table}" ({predictions_table_schema});"""

        # Create the predictions table if it doesn't exist
        try:
            execute_sql(f'SELECT TOP 1 * FROM "{database}"."{predictions_table}";')
            # If SELECT succeeds, table already exists
            warnings.warn(
                f"Table {predictions_table} already exists. Using existing table.",
                UserWarning,
            )
        except:  # noqa #NOSONAR
            # Table doesn't exist, create it
            try:
                execute_sql(create_predictions_table_query)
                logger.debug(f"Created predictions table: {predictions_table}")
            except Exception as e:
                raise EntityCreationError(
                    f"Error creating table {predictions_table}: {e}"
                )

        # Create the feature metadata table if it doesn't exist
        try:
            execute_sql(f'SELECT TOP 1 * FROM "{database}"."{feature_metadata_table}";')
            warnings.warn(
                f"Table {feature_metadata_table} already exists. Using existing table.",
                UserWarning,
            )
        except:  # noqa #NOSONAR
            try:
                from ..stats.store import create_features_stats_table

                create_features_stats_table(feature_metadata_table)
                logger.debug(
                    f"Created feature metadata table: {feature_metadata_table}"
                )
            except Exception as e:
                raise EntityCreationError(
                    f"Error creating table {feature_metadata_table}: {e}"
                )

    @staticmethod
    def _infer_data_type_from_dtype(dtype_str: str) -> DataType:
        """
        Infer DataType enum from pandas dtype string.

        Args:
            dtype_str: String representation of pandas dtype

        Returns:
            DataType: FLOAT for float types, INTEGER for int types, VARCHAR for others
        """
        dtype_lower = str(dtype_str).lower()
        if dtype_lower.startswith("float"):
            return DataType.FLOAT
        elif dtype_lower.startswith("int"):
            return DataType.INTEGER
        else:
            return DataType.VARCHAR

    def _parse_entity_from_dictionary(self, response: dict) -> DatasetTemplate | None:
        try:
            metadata = response.get("metadata")
            catalog_type = CatalogType(response.get("catalogType"))
            dataset_template = DatasetTemplate(
                id=uuid.UUID(response.get("id")),
                name=response.get("name"),
                description=response.get("description"),
                project_id=uuid.UUID(response.get("projectId")),
                owner_id=response.get("ownerId"),
                catalog_type=catalog_type,
            )

            from tmo.api.utils.metadata_parser import parse_metadata_from_response

            dataset_template.metadata = parse_metadata_from_response(
                metadata, catalog_type, dataset_template
            )

            return dataset_template
        except Exception as e:
            logger.error(f"Error parsing dataset template from response: {str(e)}")
            return None
