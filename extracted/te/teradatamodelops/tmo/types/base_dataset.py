import logging
from typing import Optional, Union

import pandas
from teradataml import DataFrame

from tmo.types.base_entity import BaseEntityMixin
from tmo.types.dataset_metadata import Metadata, CatalogType

logger = logging.getLogger(__name__)


class BaseDatasetMixin(BaseEntityMixin):
    """
    Mixin that provides common functionality for Dataset and DatasetTemplate.

    Inherits from BaseEntityMixin which provides:
    - __repr__: Multi-line representation
    - __str__: Pretty JSON representation
    - to_json(): JSON string conversion
    - to_dict(): Dictionary conversion

    This mixin adds dataset-specific properties like entity, target, and metadata access.
    """

    catalog_type: Optional[CatalogType] = None
    metadata: Optional[Union[Metadata, dict]]  # noqa
    _entity: Optional[str] = None
    _target: Optional[list[str]] = None
    _metadata: Optional[Union[Metadata, dict]] = None  # noqa

    @property
    def metadata(self) -> Optional[Union[Metadata, dict]]:  # NOSONAR
        """Get the metadata (Metadata object for VANTAGE, dict for NO_CATALOG, or None)."""
        return self._metadata

    @metadata.setter
    def metadata(self, value: Optional[Union[Metadata, dict]]):  # NOSONAR
        """
        Set the metadata with validation based on catalog_type.

        For VANTAGE: Strictly requires Metadata object
        For NO_CATALOG and others: Allows dict (JSON) or Metadata

        Args:
            value: Metadata object or dict depending on catalog_type

        Raises:
            ValueError: If value type doesn't match catalog_type requirements
        """

        # Determine the effective catalog type, preferring the public attribute
        catalog_type = getattr(self, "catalog_type", None)
        if catalog_type is None and hasattr(self, "_catalog_type"):
            catalog_type = self._catalog_type
        # For VANTAGE, strictly require Metadata object
        if catalog_type == CatalogType.VANTAGE:  # noqa
            if value is not None and not self._isclass(value, Metadata):  # noqa
                raise ValueError(
                    "Metadata must be an instance of Metadata class for VANTAGE catalog"
                    " type."
                )
            self._metadata = value
        else:
            # For NO_CATALOG and all other catalog types, allow dict (JSON) or Metadata
            if value is not None and not (
                isinstance(value, dict) or self._isclass(value, Metadata)  # noqa
            ):
                raise ValueError(
                    "Metadata must be a dict or Metadata instance for non-VANTAGE"
                    " catalog types."
                )
            self._metadata = value

    @property
    def entity(self) -> str:
        return self._entity

    @entity.setter
    def entity(self, value: str):
        if value is not None and not isinstance(value, str):
            raise ValueError("Entity must be a string.")
        self._entity = value

    @property
    def target(self) -> list[str]:
        return self._target

    @target.setter
    def target(self, value: list[str]):
        if value is not None and not isinstance(value, list):
            raise ValueError("Target must be a list of strings.")
        self._target = value

    @property
    def features_query(self) -> str:
        # Check if this is a NO_CATALOG type - queries are not applicable
        if (
            hasattr(self, "catalog_type")
            and self.catalog_type == CatalogType.NO_CATALOG
        ):
            logger.warning(
                "Features query is not applicable for"
                f" {CatalogType.NO_CATALOG.value} catalog type. Access metadata"
                " directly via .metadata property."
            )
            return ""

        if not self.metadata:
            return ""
        if isinstance(self.metadata, dict):
            return self.metadata.get("features", {}).get("sql", "")
        if (
            hasattr(self.metadata, "features")
            and self.metadata.features is not None
            and hasattr(self.metadata.features, "sql")
            and self.metadata.features.sql is not None
        ):
            return self.metadata.features.sql
        return ""

    @property
    def entity_targets_query(self) -> str:
        # Check if this is a NO_CATALOG type - queries are not applicable
        if (
            hasattr(self, "catalog_type")
            and self.catalog_type == CatalogType.NO_CATALOG
        ):
            logger.warning(
                "Entity/targets query is not applicable for"
                f" {CatalogType.NO_CATALOG.value} catalog type. Access metadata"
                " directly via .metadata property."
            )
            return ""

        if not self.metadata:
            return ""
        if isinstance(self.metadata, dict):
            return self.metadata.get("entityAndTargets", {}).get("sql", "")
        if (
            hasattr(self.metadata, "entity_and_targets")
            and self.metadata.entity_and_targets is not None
            and hasattr(self.metadata.entity_and_targets, "sql")
            and self.metadata.entity_and_targets.sql is not None
        ):
            return self.metadata.entity_and_targets.sql
        return ""

    @property
    def predictions_query(self) -> str:
        # Check if this is a NO_CATALOG type - queries are not applicable
        if (
            hasattr(self, "catalog_type")
            and self.catalog_type == CatalogType.NO_CATALOG
        ):
            logger.warning(
                "Predictions query is not applicable for"
                f" {CatalogType.NO_CATALOG.value} catalog type. Access metadata"
                " directly via .metadata property."
            )
            return ""

        if not self.metadata:
            return ""
        if isinstance(self.metadata, dict):
            return self.metadata.get("predictions", {}).get("entitySql", "")
        if (
            hasattr(self.metadata, "predictions")
            and self.metadata.predictions is not None
            and hasattr(self.metadata.predictions, "entity_sql")
            and self.metadata.predictions.entity_sql is not None
        ):
            return self.metadata.predictions.entity_sql
        return ""

    @property
    def features(self) -> list[str]:
        # Check if this is a NO_CATALOG type - features are not applicable
        if (
            hasattr(self, "catalog_type")
            and self.catalog_type == CatalogType.NO_CATALOG
        ):
            logger.warning(
                "Features property is not applicable for"
                f" {CatalogType.NO_CATALOG.value} catalog type. Access metadata"
                " directly via .metadata property."
            )
            return []

        if not self.metadata:
            return []
        if isinstance(self.metadata, dict):
            variables = self.metadata.get("features", {}).get("variables", [])
            return [
                var.get("name") if isinstance(var, dict) else var.name
                for var in variables
            ]
        # For Metadata objects, safely check nested attributes
        if (
            hasattr(self.metadata, "features")
            and self.metadata.features is not None
            and hasattr(self.metadata.features, "variables")
            and self.metadata.features.variables is not None
        ):
            return [col.name for col in self.metadata.features.variables]
        return []

    def list_features(self) -> Optional[DataFrame | pandas.DataFrame]:
        """
        Returns the features in the dataset template as a DataFrame.

        Returns:
            Optional[teradataml.DataFrame | pandas.DataFrame]: A DataFrame containing feature information
        """
        from tmo.util.utils import to_dataframe

        try:
            if isinstance(self.metadata, dict):
                return self._list_features_from_dict(to_dataframe)

            return self._list_features_from_metadata(to_dataframe)
        except Exception as e:
            logger.error(f"Could not convert features to DataFrame: {str(e)}")
            return None

    @staticmethod
    def _create_feature_dict_from_var(var: dict) -> dict:
        """
        Creates a feature dictionary from a variable dict (NO_CATALOG).

        Args:
            var: Variable dictionary

        Returns:
            dict: Feature information dictionary
        """
        return {
            "name": var.get("name"),
            "dataType": var.get("dataType"),
            "type": var.get("type"),
            "featureType": "unknown",  # Cannot infer without SQL
        }

    @staticmethod
    def _create_feature_dict_from_column(column, categorical_features: set) -> dict:
        """
        Creates a feature dictionary from a column object (VANTAGE).

        Args:
            column: Column object with name, data_type, and type attributes
            categorical_features: Set of categorical feature names

        Returns:
            dict: Feature information dictionary
        """
        if column.name in categorical_features:
            feature_type = "categorical"
        else:
            feature_type = "continuous"

        return {
            "name": column.name,
            "dataType": column.data_type,
            "type": column.type,
            "featureType": feature_type,
        }

    def _infer_categorical_features(self, infer_columns_type) -> set:
        """
        Infers which features are categorical based on the features query.

        Args:
            infer_columns_type: Function to infer column types

        Returns:
            set: Set of categorical feature names
        """
        feature_columns = self.features
        features_query = self.metadata.features.sql

        categorical_features, _ = infer_columns_type(
            query=features_query,
            feature_columns=feature_columns,
        )

        return set(categorical_features)

    def _list_features_from_dict(
        self, to_dataframe
    ) -> Optional[DataFrame | pandas.DataFrame]:
        """
        Extracts features from dict metadata (NO_CATALOG case).

        Args:
            to_dataframe: Function to convert data to DataFrame

        Returns:
            Optional[DataFrame | pandas.DataFrame]: DataFrame with feature information or None
        """
        features_data_raw = self.metadata.get("features", {}).get("variables", [])
        dict_vars = [var for var in features_data_raw if isinstance(var, dict)]
        if not dict_vars:
            return None

        feature_data = [self._create_feature_dict_from_var(var) for var in dict_vars]
        return to_dataframe(feature_data)

    def _list_features_from_metadata(
        self, to_dataframe
    ) -> Optional[DataFrame | pandas.DataFrame]:
        """
        Extracts features from Metadata object (VANTAGE case).

        Args:
            to_dataframe: Function to convert data to DataFrame

        Returns:
            Optional[DataFrame | pandas.DataFrame]: DataFrame with feature information or None
        """
        from tmo.stats.stats_util import infer_columns_type

        features = self.metadata.features.variables
        categorical_features = self._infer_categorical_features(infer_columns_type)

        feature_data = []
        for column in features:
            feature_data.append(
                self._create_feature_dict_from_column(column, categorical_features)
            )

        return to_dataframe(feature_data)
