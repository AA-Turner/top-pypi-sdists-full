import logging
from typing import Optional

import pandas
from teradataml import DataFrame

from tmo.types.dataset_metadata import Metadata

logger = logging.getLogger(__name__)


class BaseDatasetMixin:
    """Mixin that provides common functionality for Dataset and DatasetTemplate."""

    metadata: Metadata

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
        return self.metadata.features.sql

    @property
    def entity_targets_query(self) -> str:
        return self.metadata.entity_and_targets.sql

    @property
    def predictions_query(self) -> str:
        return self.metadata.predictions.entity_sql

    @property
    def features(self) -> list[str]:
        return [col.name for col in self.metadata.features.variables]

    def list_features(self) -> Optional[DataFrame | pandas.DataFrame]:
        """
        Returns the features in the dataset template as a DataFrame.

        Returns:
            Optional[teradataml.DataFrame | pandas.DataFrame]: A DataFrame containing feature information
        """
        from tmo.util.utils import to_dataframe
        from tmo.stats.stats_util import infer_columns_type

        if not hasattr(self, "metadata") or not hasattr(self.metadata, "features"):
            logger.error("Metadata or features not defined in the dataset template.")
            return None

        try:
            features = self.metadata.features.variables
            feature_columns = self.features
            features_query = self.metadata.features.sql

            categorical_features, _ = infer_columns_type(
                query=features_query,
                feature_columns=feature_columns,
            )

            feature_data = []
            for column in features:
                feature_type = (
                    "categorical"
                    if column.name in categorical_features
                    else "continuous"
                )
                feature_data.append({
                    "name": column.name,
                    "dataType": column.data_type,
                    "type": column.type,
                    "featureType": feature_type,
                })

            return to_dataframe(feature_data)
        except Exception as e:
            logger.error(f"Could not convert features to DataFrame: {str(e)}")
            return None

    def to_dataframe(self) -> Optional[DataFrame | pandas.DataFrame]:
        """
        Converts the dataset template to a DataFrame.

        Returns:
            Optional[teradataml.DataFrame | pandas.DataFrame]: A DataFrame representation of the dataset template.
        """
        from tmo.util.utils import to_dataframe

        try:
            return to_dataframe([self.get_df_template()])
        except Exception as e:
            logger.error(f"Could not convert dataset template to DataFrame: {str(e)}")
            return None

    @staticmethod
    def _isclass(obj, cls):
        return obj.__class__ == cls().__class__
