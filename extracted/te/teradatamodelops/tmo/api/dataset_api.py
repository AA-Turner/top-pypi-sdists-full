from __future__ import absolute_import

import logging
import uuid
from typing import Union

from teradataml import DataFrame

from tmo.api.base_entity_api import BaseEntityApiMixin
from tmo.api.dataset_template_api import (
    DatasetTemplateApi,
    FeaturesEntityTargets,
    Metadata,
    Predictions,
    Variable,
)
from tmo.types.dataset import Dataset, Scope
from tmo.types.dataset_metadata import (
    TypeEnum,
    CatalogType,
    body_type_string_to_catalog_type,
)
from tmo.types.exceptions import EntityNotFoundError

logger = logging.getLogger(__name__)


class DatasetApi(BaseEntityApiMixin):
    name = "Dataset API"
    path = "datasets"
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
            entity_targets.set_sql(sql["target_entity"])
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
            path=self.base_path + self.path,
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
            path=self.base_path + self.path,
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
            path=f"{self.base_path + self.path}/{str(id)}/render",
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

        response = self.build_get_request(
            "/search/findByName", {"name": name}, projection
        )

        return self.process_entities_response(
            response, return_dataframe, f" with name like: {name}"
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
            DataFrame or list[Dataset] or None: combined DataFrame of all datasets or list of Dataset objects.
            Returns None only if dataset_template_id is not a valid UUID. Returns empty list/DataFrame if no datasets found or parsing fails.
        """
        dataset_template_id = self.validate_uuid(dataset_template_id)
        if dataset_template_id is None:
            return None

        response = self.build_get_request(
            "/search/findByDatasetTemplateId",
            {"datasetTemplateId": dataset_template_id, "archived": archived},
            projection,
            page,
            size,
            sort,
        )

        # Process and return response (returns list of datasets, not single dataset)
        return self.process_entities_response(
            response,
            return_dataframe,
            f" for dataset template id: {dataset_template_id}",
        )

    @staticmethod
    def _get_catalog_from_metadata(metadata: dict) -> CatalogType:
        """
        Helper method to extract catalog type from metadata.

        Parameters:
            metadata (dict): metadata dictionary from API response
        Returns:
            CatalogType: extracted catalog type or default to VANTAGE
        """
        if not metadata:
            logger.warning(
                "No metadata found in response, defaulting catalog type to VANTAGE"
            )
            return CatalogType.VANTAGE

        catalog_body_type = metadata.get("type")

        try:
            return body_type_string_to_catalog_type(catalog_body_type)
        except ValueError:
            logger.warning(
                f"Unknown catalog type in metadata: {catalog_body_type}, defaulting to"
                " VANTAGE"
            )
            return CatalogType.VANTAGE

    def _parse_entity_from_dictionary(self, response: dict) -> Dataset | None:
        """
        Helper method to parse a single dataset from API response

        Parameters:
            response (dict): API response containing dataset information
        Returns:
            Dataset or None: parsed Dataset object or None if parsing fails
        """
        try:
            # Validate required fields exist
            if not response.get("id"):
                logger.error("Dataset response missing 'id' field")
                return None
            if not response.get("datasetTemplateId"):
                logger.error("Dataset response missing 'datasetTemplateId' field")
                return None

            metadata = response.get("metadata")
            catalog_type = self._get_catalog_from_metadata(metadata)
            dataset = Dataset(
                id=uuid.UUID(response.get("id")),
                dataset_template_id=uuid.UUID(response.get("datasetTemplateId")),
                name=response.get("name"),
                description=response.get("description"),
                scope=Scope(response.get("scope", "train").lower()),
                catalog_type=catalog_type,
            )

            from tmo.api.utils.metadata_parser import parse_metadata_from_response

            dataset.metadata = parse_metadata_from_response(
                metadata, catalog_type, dataset
            )

            return dataset
        except Exception as e:
            logger.error(f"Error parsing dataset from response: {str(e)}")
            return None
