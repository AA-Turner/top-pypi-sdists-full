from __future__ import absolute_import

import logging
import uuid
from typing import Union

from teradataml import DataFrame

from tmo.api.dataset_template_api import (
    DatasetTemplateApi,
    FeaturesEntityTargets,
    Metadata,
    Predictions,
    Variable,
)
from tmo.api.iterator_base_api import IteratorBaseApi
from tmo.types.dataset import Dataset, Scope
from tmo.types.dataset_metadata import TypeEnum
from tmo.types.exceptions import EntityNotFoundError

logger = logging.getLogger(__name__)


class DatasetApi(IteratorBaseApi):
    path = "/api/datasets"
    type = "DATASET"

    def create(
        self,
        dataset_template_id: uuid.UUID,
        name: str,
        description: str,
        scope: Scope,
        sql: dict[str, str] = None,
        tables: dict = None,
    ) -> Dataset:
        """
        Creates a dataset.

        Parameters:
            dataset_template_id (UUID): The dataset template id.
            name (str): The name of the dataset.
            description (str): The description of the dataset.
            scope (str): The scope of the dataset can be 'train' or 'evaluate'
            sql (str, optional): SQL query used to select entity sample and target. If None, this query will be automatically created using the dataset template tables.
                - entityAndTargets: SQL query for extracting entity and targets
                - predictions: SQL query for extracting entity and targets for predictions
            tables (dict, optional): The tables to be used in the dataset. If None, the tables will be automatically created using the dataset template name as a base.
                - data: Contains entity, features and targets.
                - entityTarget: Stores entity and target. If not provided these will be extracted from 'dataTable'.
                - predictions: Contains entity and target for predictions. If not provided, it will be created using the dataset template name as a base.

        Returns:
            (Dataset): dataset

        Example:
            ```python
            from tmo import TmoClient

            vmoClient = TmoClient()

            train_dataset = (
                vmoClient
                .datasets()
                .create(
                    dataset_template_id="1a71337c-8b6f-4500-a129-ef8036578c81",
                    name="Training",
                    description="dataset description",
                    scope="train",
                )
            )
            ```
        """

        sql = sql or {}
        tables = tables or {}

        dataset_template = DatasetTemplateApi(self.tmo_client).find_by_id(
            dataset_template_id
        )

        if dataset_template is None:
            raise EntityNotFoundError(
                f"Dataset template with id {dataset_template_id} not found"
            )

        dataset = Dataset(
            dataset_template_id=dataset_template_id,
            name=name,
            description=description,
            scope=scope,
        )

        entity_and_target = dataset_template.metadata.entity_and_targets.variables
        database = dataset_template.metadata.predictions.database
        dataset_template_metadata = dataset_template.metadata
        features = dataset_template.metadata.features.variables
        features_sql = dataset_template.metadata.features.sql

        entity_and_target_sql = sql.get(
            "entityAndTargets", dataset_template_metadata.entity_and_targets.sql
        )
        predictions_entity_sql = sql.get(
            "predictions", dataset_template_metadata.predictions.entity_sql
        )

        data_table = tables.get(
            "data", f"{dataset_template.name.replace(' ', '_')}_data"
        )
        entity_target_table = tables.get("entityTarget", data_table)
        predictions_table = tables.get(
            "predictions", dataset_template_metadata.predictions.table
        )

        entity_columns_objects = [
            Variable()
            .set_name(col.name)
            .set_data_type(col.data_type)
            .set_type(col.type)
            .set_entity_id(True)
            .set_selected(False)
            for col in entity_and_target
            if col.type == TypeEnum.ENTITY
        ]

        target_columns_objects = [
            Variable()
            .set_name(col.name)
            .set_data_type(col.data_type)
            .set_type(col.type)
            .set_entity_id(False)
            .set_selected(True)
            for col in entity_and_target
            if col.type == TypeEnum.TARGET
        ]

        entity = entity_columns_objects[0].name

        features = (
            FeaturesEntityTargets()
            .set_sql(features_sql)
            .set_entity(entity)
            .set_columns(features)
        )

        entity_columns = [col.name for col in entity_columns_objects]
        target_columns = [col.name for col in target_columns_objects]

        # Create entity targets object with custom SQL if available
        entity_targets = FeaturesEntityTargets().set_entity(entity)
        if sql and "target_entity" in sql:
            logger.debug(f"Using custom SQL for target_entity: {sql['target_entity']}")
            entity_targets.sql(sql["target_entity"])
        else:
            query = (
                f"SELECT {entity_columns[0]}, {', '.join(target_columns)} FROM"
                f" {entity_target_table}"
            )
            logger.debug(
                f"Using data table for target_entity SQL: {entity_target_table}"
            )
            entity_targets.set_sql(query)
        entity_targets.set_columns(entity_columns_objects + target_columns_objects)

        predictions = (
            Predictions()
            .set_database(database)
            .set_entity_sql(predictions_entity_sql)
            .set_table(predictions_table)
        )

        dataset.metadata = (
            Metadata()
            .set_type("CatalogBody")
            .set_features(features)
            .set_entity_and_targets(entity_targets)
            .set_predictions(predictions)
        )

        dataset_request = {
            "datasetTemplateId": str(dataset.dataset_template_id),
            "name": dataset.name,
            "description": dataset.description,
            "scope": dataset.scope.value,
            "metadata": {
                "features": {
                    "sql": features_sql,
                    "entity": entity,
                    "variables": [
                        {
                            "name": col.name,
                            "type": col.type.value,
                            "dataType": col.data_type.value,
                            "selected": col.selected,
                            "entityId": str(col.entity_id),
                        }
                        for col in features.variables
                    ],
                },
                "entityAndTargets": {
                    "entity": entity,
                    "sql": entity_and_target_sql,
                    "variables": [
                        {
                            "name": col.name,
                            "dataType": col.data_type.value,
                            "type": col.type.value,
                        }
                        for col in entity_and_target
                    ],
                },
                "predictions": {
                    "database": database,
                    "entitySql": predictions_entity_sql,
                    "table": predictions_table,
                },
                "type": dataset_template.metadata.type.value,
            },
            "catalogType": dataset_template.catalog_type.value,
        }

        response = self.tmo_client.post_request(
            path=self.path,
            header_params=self._get_header_params(),
            query_params={},
            body=dataset_request,
        )

        dataset.id = uuid.UUID(response.get("id"))

        logger.debug("Dataset created successfully.")

        return dataset

    def save(self, dataset: dict[str, str]):
        """
        register a dataset

        Parameters:
           dataset (dict): dataset to register

        Returns:
            (dict): dataset
        """
        return self.tmo_client.post_request(
            path=self.path,
            header_params=self._get_header_params(),
            query_params={},
            body=dataset,
        )

    def render(self, id: str | uuid.UUID) -> dict:
        """
        returns a rendered dataset

        Parameters:
           id (str): dataset id

        Returns:
            (dict): rendered dataset
        """

        return self.tmo_client.get_request(
            path=f"{self.path}/{str(id)}/render",
            header_params=self._get_header_params(),
            query_params={},
        )

    def find_by_name_like(
        self, name: str, projection: str = None, return_dataframe: bool = False
    ) -> DataFrame | list[Dataset]:
        """
        Returns datasets matching the name as a combined DataFrame or list.

        Parameters:
            name (str): dataset name(string) to match
            projection (str): projection type
            return_dataframe (bool): if True, returns combined DataFrame; if False, returns list of Dataset objects

        Returns:
            DataFrame or list[Dataset]: combined DataFrame of all datasets or list of Dataset objects
        """
        query_vars = ["name", "projection"]
        query_vals = [name, projection]
        query_params = self.generate_params(query_vars, query_vals)

        response = self.tmo_client.get_request(
            path=f"{self.path}/search/findByName",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

        return self._process_datasets_response(
            response, return_dataframe, f" for: {name}"
        )

    def find_by_dataset_template_id(
        self,
        dataset_template_id: Union[str, uuid.UUID],
        archived: bool = False,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
        return_dataframe: bool = False,
    ) -> DataFrame | list[Dataset] | None:
        """
        Returns all datasets of a project by dataset template id as a combined DataFrame or list.

        Parameters:
            dataset_template_id (str|UUID): dataset template id
            archived (bool): archived or not (default False)
            projection (str): projection type
            page (int): page number
            size (int): number of records in a page
            sort (str): column name and sorting order
                e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order
            return_dataframe (bool): if True, returns combined DataFrame; if False, returns list of Dataset objects

        Returns:
            DataFrame or list[Dataset] or None: combined DataFrame of all datasets or list of Dataset objects
        """
        # Validate and convert UUID
        validated_id = self._validate_and_convert_uuid(
            dataset_template_id, "dataset_template_id"
        )
        if validated_id is None:
            return None if return_dataframe else []

        # Build query parameters
        query_vars = [
            "datasetTemplateId",
            "archived",
            "projection",
            "page",
            "size",
            "sort",
        ]
        query_vals = [validated_id, archived, projection, page, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        # Execute API request
        response = self.tmo_client.get_request(
            path=f"{self.path}/search/findByDatasetTemplateId",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

        # Process and return response
        return self._process_datasets_response(
            response, return_dataframe, f" for template id: {validated_id}"
        )

    def find_all(
        self,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
        return_dataframe: bool = False,
    ):
        """
        Returns all datasets.

        Parameters:
            projection (str): projection type
            page (int): page number
            size (int): number of records in a page
            sort (str): column name and sorting order
            return_dataframe (bool): if True, returns DataFrame; if False, returns list of Dataset objects

        Returns:
            DataFrame or list[Dataset]: combined DataFrame of all datasets or list of Dataset objects
        """
        query_vars = ["projection", "page", "size", "sort"]
        query_vals = [projection, page, size, sort]
        built_query_params = self.generate_params(query_vars, query_vals)

        response = self.tmo_client.get_request(
            path=f"{self.path}",
            header_params=self._get_header_params(),
            query_params=built_query_params,
        )

        return self._process_datasets_response(response, return_dataframe)

    def _get_header_params(self):
        return self._get_standard_header_params(
            accept_types=[
                self.json_type,
                "application/hal+json",
                "text/uri-list",
                "application/x-spring-data-compact+json",
            ]
        )

    def _process_datasets_response(
        self, response: dict, return_dataframe: bool, context: str = ""
    ) -> DataFrame | list[Dataset] | None:
        """
        Helper method to process API response containing datasets.
        Reduces cognitive complexity by extracting common processing logic.

        Parameters:
            response (dict): API response containing datasets
            return_dataframe (bool): if True, returns DataFrame; if False, returns list
            context (str): context message for logging (e.g., "for name: xyz")

        Returns:
            DataFrame or list[Dataset] or None: processed datasets
        """
        try:
            datasets_data = response.get("_embedded", {}).get("datasets", [])

            if not datasets_data:
                logger.info(f"No datasets found{context}")
                return None if return_dataframe else []

            datasets = []
            for dataset_data in datasets_data:
                dataset = self._parse_dataset_from_response(dataset_data)
                if dataset:
                    datasets.append(dataset)

            return (
                self._datasets_to_dataframe(datasets) if return_dataframe else datasets
            )

        except Exception as e:
            logger.error(f"Error while parsing dataset response: {str(e)}")
            return None if return_dataframe else []

    @staticmethod
    def _validate_and_convert_uuid(
        value: Union[str, uuid.UUID], param_name: str = "id"
    ) -> uuid.UUID | None:
        """
        Helper method to validate and convert a value to UUID.

        Parameters:
            value: value to convert (str or UUID)
            param_name: parameter name for logging

        Returns:
            UUID or None: converted UUID or None if invalid
        """
        if isinstance(value, uuid.UUID):
            return value

        try:
            return uuid.UUID(value)
        except ValueError:
            logger.error(f"Invalid UUID format for {param_name}: {value}")
            return None

    @staticmethod
    def _parse_dataset_from_response(dataset_data: dict) -> Dataset | None:
        """Helper method to parse a single dataset from API response"""
        try:
            dataset = Dataset(
                dataset_template_id=uuid.UUID(dataset_data.get("datasetTemplateId")),
                name=dataset_data.get("name"),
                description=dataset_data.get("description"),
                scope=Scope(dataset_data.get("scope")),
            )

            dataset.id = dataset_data.get("id")

            # get metadata
            metadata = dataset_data.get("metadata")
            if not metadata:
                return dataset

            features_data = metadata.get("features", {})
            entity_targets_data = metadata.get("entityAndTargets", {})
            predictions_data = metadata.get("predictions", {})

            # Extract entity
            entity = features_data.get("entity")
            dataset.entity = entity

            # Extract targets
            if "variables" in entity_targets_data:
                target_variables = []
                for variable in entity_targets_data.get("variables", []):
                    if variable.get("type") == "target":
                        target_variables.append(variable.get("name"))
                dataset.target = target_variables

            # Set up the metadata structure
            dataset.metadata = Metadata()
            dataset.metadata.features = FeaturesEntityTargets()
            dataset.metadata.entityAndTargets = FeaturesEntityTargets()
            dataset.metadata.predictions = Predictions()
            dataset.metadata.type = metadata.get("type")

            # Parse entity target columns
            entity_target_columns = []  # noqa
            for variable in entity_targets_data.get("variables", []):  # noqa
                column = Variable()
                column.name = variable.get("name")
                column.dataType = variable.get("dataType")
                column.type = variable.get("type")
                entity_target_columns.append(column)
            dataset.metadata.entityAndTargets.variables = entity_target_columns
            dataset.metadata.entityAndTargets.entity = entity
            dataset.metadata.entityAndTargets.sql = entity_targets_data.get("sql")

            # Parse feature columns
            feature_columns = []  # noqa
            for variable in features_data.get("variables", []):
                column = Variable()
                column.name = variable.get("name")
                column.dataType = variable.get("dataType")
                column.type = variable.get("type")
                feature_columns.append(column)
            dataset.metadata.features.variables = feature_columns
            dataset.metadata.features.entity = entity
            dataset.metadata.features.sql = features_data.get("sql")

            # Parse predictions
            dataset.metadata.predictions.database = predictions_data.get("database")
            dataset.metadata.predictions.entity_sql = predictions_data.get("entitySql")
            dataset.metadata.predictions.table = predictions_data.get("table")

            return dataset

        except Exception as e:
            logger.error(f"Error parsing dataset: {str(e)}")
            return None

    @staticmethod
    def _datasets_to_dataframe(datasets: list[Dataset]):
        """
        Helper method to combine multiple datasets into a single DataFrame

        Parameters:
            datasets (list[Dataset]): list of datasets to combine

        Returns:
            DataFrame: Combined DataFrame containing all datasets, or None if conversion fails
        """
        if not datasets:
            return None

        try:
            from tmo.util.utils import to_dataframe

            combined_data = []
            for dataset in datasets:
                combined_data.append(dataset.get_df_template())

            return to_dataframe(combined_data)
        except Exception as e:
            logger.error(f"Could not combine datasets to DataFrame: {str(e)}")
            return None
