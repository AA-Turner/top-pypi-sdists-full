from __future__ import absolute_import

import logging
import uuid
import warnings
from typing import Any, Optional, Union

import pandas as pd
from teradataml import DataFrame, execute_sql

from tmo.api.iterator_base_api import IteratorBaseApi
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


class DatasetTemplateApi(IteratorBaseApi):
    path = "/api/datasetTemplates"
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
            .set_data_type(
                DataType.FLOAT if dtype.startswith("float") else DataType.INTEGER
            )
            .set_type(TypeEnum.FEATURE)
            for col, dtype in zip(column_names, column_dtypes)
            if col not in entity_columns + target_columns
        ]

        entity_columns_objects = [
            Variable()
            .set_name(col)
            .set_data_type(
                DataType.FLOAT
                if str(dataframe[col].dtype).startswith("float")
                else DataType.INTEGER
            )
            .set_type(TypeEnum.ENTITY)
            for col in entity_columns
        ]

        target_columns_objects = [
            Variable()
            .set_name(col)
            .set_data_type(
                DataType.FLOAT
                if str(dataframe[col].dtype).startswith("float")
                else DataType.INTEGER
            )
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
                        for col in dataset_template.metadata.entity_and_targets.variables
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
            path=self.path,
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
            path=f"{self.path}/{str(id)}/render",
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
        query_vars = ["name", "projection"]
        query_vals = [name, projection]
        query_params = self.generate_params(query_vars, query_vals)

        response = self.tmo_client.get_request(
            path=f"{self.path}/search/findByName",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

        try:
            dataset_templates_data = response.get("_embedded", {}).get(
                "datasetTemplates", []
            )

            if not dataset_templates_data:
                logger.info(f"No dataset templates found for name: {name}")
                return None if return_dataframe else []

            dataset_templates = []
            for data in dataset_templates_data:
                dataset_template = self._parse_dataset_template_from_response(data)
                if dataset_template:
                    dataset_templates.append(dataset_template)

            if return_dataframe:
                return self._dataset_templates_to_dataframe(dataset_templates)
            else:
                return dataset_templates

        except Exception as e:
            logger.error(f"Error parsing dataset templates: {str(e)}")
            return None if return_dataframe else []

    def find_by_id(
        self, dataset_template_id: Union[str, uuid.UUID], return_dataframe: bool = False
    ) -> None | DataFrame | DatasetTemplate:
        """
        returns a dataset template by id

        Parameters:
        id (str): dataset_template id
        return_dataframe (bool): if True, returns DataFrame; if False, returns DatasetTemplate object

        Returns:
            (dict): dataset template
            (DatasetTemplate): dataset template object if return_dataframe is True
        """

        if not isinstance(dataset_template_id, uuid.UUID):
            try:
                dataset_template_id = uuid.UUID(dataset_template_id)
            except ValueError:
                logger.error(f"Invalid UUID format for id: {dataset_template_id}")
                return None

        query_vars = ["id"]
        query_vals = [str(dataset_template_id)]
        query_params = self.generate_params(query_vars, query_vals)

        response = self.tmo_client.get_request(
            path=f"{self.path}/search/findById",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

        try:
            dataset_template = self._parse_dataset_template_from_response(response)

            if dataset_template is None:
                logger.error(
                    f"Dataset template with id {dataset_template_id} not found."
                )
                return None

            if return_dataframe:
                return dataset_template.to_dataframe()
            else:
                return dataset_template

        except Exception as e:
            logger.error(f"Error parsing dataset template: {str(e)}")
            return None

    def find_all(
        self,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
        return_dataframe: bool = False,
    ) -> list[Any] | DataFrame:
        """
        returns all dataset templates

        Parameters:
        projection (str): projection type
        page (int): page number
        size (int): number of records in a page
        sort (str): column name and sorting order
        return_dataframe (bool): if True, returns DataFrame; if False, returns list of DatasetTemplate objects

        Returns:
            (list): dataset templates
        """

        query_vars = ["projection", "page", "size", "sort"]
        query_vals = [projection, page, size, sort]
        built_query_params = self.generate_params(query_vars, query_vals)

        response = self.tmo_client.get_request(
            path=f"{self.path}",
            header_params=self._get_header_params(),
            query_params=built_query_params,
        )

        try:
            dataset_templates_data = response.get("_embedded", {}).get(
                "datasetTemplates", []
            )

            if not dataset_templates_data:
                logger.info("No dataset templates found.")
                return [] if not return_dataframe else pd.DataFrame()

            dataset_templates = []
            for data in dataset_templates_data:
                dataset_template = self._parse_dataset_template_from_response(data)
                if dataset_template:
                    dataset_templates.append(dataset_template)

            if return_dataframe:
                return self._dataset_templates_to_dataframe(dataset_templates)
            else:
                return dataset_templates

        except Exception as e:
            logger.error(f"Error parsing dataset templates: {str(e)}")
            return [] if not return_dataframe else pd.DataFrame()

    def _get_header_params(self) -> dict:
        return self._get_standard_header_params(
            accept_types=[
                self.json_type,
                "application/hal+json",
                "text/uri-list",
                "application/x-spring-data-compact+json",
            ]
        )

    @staticmethod
    def _parse_dataset_template_from_response(response: dict) -> DatasetTemplate | None:
        try:
            dataset_template = DatasetTemplate(
                id=uuid.UUID(response.get("id")),
                name=response.get("name"),
                description=response.get("description"),
                project_id=uuid.UUID(response.get("projectId")),
                owner_id=response.get("ownerId"),
                catalog_type=CatalogType(response.get("catalogType")),
            )

            # Get metadata
            metadata = response.get("metadata")
            features_data = metadata.get("features")
            entity_targets_data = metadata.get("entityAndTargets")

            # Extract entity
            entity = features_data.get("entity")
            dataset_template.entity = entity

            # Extract targets
            if "variables" in entity_targets_data:
                target_variables = []
                for variable in entity_targets_data.get("variables"):
                    if variable.get("type") == TypeEnum.TARGET.value:
                        target_variables.append(variable.get("name"))
                dataset_template.target = target_variables

            # Set up the metadata structure
            dataset_template.metadata = Metadata()
            dataset_template.metadata.features = FeaturesEntityTargets()
            dataset_template.metadata.entity_and_targets = FeaturesEntityTargets()
            dataset_template.metadata.predictions = Predictions()
            dataset_template.metadata.type = CatalogBodyType(metadata.get("type"))

            entity_target_columns = DatasetTemplateApi._dict_list_to_variable_list(
                entity_targets_data.get("variables")
            )

            dataset_template.metadata.entity_and_targets.variables = (
                entity_target_columns
            )
            dataset_template.metadata.entity_and_targets.entity = entity
            dataset_template.metadata.entity_and_targets.sql = entity_targets_data.get(
                "sql"
            )

            feature_columns = DatasetTemplateApi._dict_list_to_variable_list(
                features_data.get("variables")
            )

            dataset_template.metadata.features.variables = feature_columns
            dataset_template.metadata.features.entity = entity
            dataset_template.metadata.features.sql = features_data.get("sql")

            predictions_data = metadata.get("predictions")
            dataset_template.metadata.predictions.database = predictions_data.get(
                "database"
            )
            dataset_template.metadata.predictions.entity_sql = predictions_data.get(
                "entitySql"
            )
            dataset_template.metadata.predictions.table = predictions_data.get("table")

            return dataset_template
        except Exception as e:
            logger.error(f"Error parsing dataset template from response: {str(e)}")
            return None

    @staticmethod
    def _dataset_templates_to_dataframe(
        dataset_templates: list[DatasetTemplate],
    ) -> DataFrame | None:
        """
        Helper method to combine multiple dataset templates into a single DataFrame

        Parameters:
            dataset_templates (list[DatasetTemplate]): a list of dataset templates to combine

        Returns:
            DataFrame: Combined DataFrame containing all dataset templates, or None if conversion fails
        """
        if not dataset_templates:
            return None

        try:
            from tmo.util.utils import to_dataframe

            combined_data = []
            for dataset_template in dataset_templates:
                combined_data.append(dataset_template.get_df_template())

            return to_dataframe(combined_data)
        except Exception as e:
            logger.error(f"Could not combine dataset templates to DataFrame: {str(e)}")
            return None

    @staticmethod
    def _dict_list_to_variable_list(variables: list[dict]) -> list[Variable]:
        return [
            Variable()
            .set_name(var["name"])
            .set_data_type(DataType(var["dataType"]))
            .set_type(TypeEnum(var["type"]))
            for var in variables
        ]

    @staticmethod
    def _create_tables(
        target_columns_objects: list[Variable],
        entity_columns: list[str],
        database: str,
        predictions_table: str,
        feature_metadata_table: str,
    ):
        # Create the predictions table schema
        predictions_table_schema = ", ".join([
            f"{col.name} {'FLOAT' if col.data_type == DataType.FLOAT else 'INTEGER'}"
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
        except:  # noqa #NOSONAR
            try:
                execute_sql(create_predictions_table_query)
                warnings.warn(
                    f"Table {predictions_table} already exists. Using existing table.",
                    UserWarning,
                )
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
            except Exception as e:
                raise EntityCreationError(
                    f"Error creating table {feature_metadata_table}: {e}"
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
