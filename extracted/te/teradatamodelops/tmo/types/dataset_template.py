import logging
import uuid
from typing import Optional

from tmo.types.base_dataset import BaseDatasetMixin
from tmo.types.dataset_metadata import (
    DataType,
    TypeEnum,
    CatalogType,
    CatalogBodyType,
    Variable,
    FeaturesEntityTargets,
    Predictions,
    Metadata,
    FeatureMetadata,
)

logger = logging.getLogger(__name__)

# Re-export classes from dataset_metadata for backward compatibility
__all__ = [
    "DataType",
    "TypeEnum",
    "CatalogType",
    "CatalogBodyType",
    "Variable",
    "FeaturesEntityTargets",
    "Predictions",
    "Metadata",
    "FeatureMetadata",
    "DatasetTemplate",
]


class DatasetTemplate(BaseDatasetMixin):
    id: uuid.UUID
    name: str
    description: str
    project_id: uuid.UUID
    owner_id: str
    catalog_type: CatalogType
    metadata: Metadata
    feature_metadata: FeatureMetadata
    entity: str
    target: list[str]

    def __init__(
        self,
        id: Optional[uuid.UUID] = None,
        name: Optional[str] = "SDK Dataset Template",
        description: Optional[str] = "VANTAGE dataset template",
        project_id: Optional[uuid.UUID] = None,
        owner_id: Optional[str] = None,
        catalog_type: Optional[CatalogType] = CatalogType.VANTAGE,
        metadata: Optional[Metadata] = Metadata(),
        feature_metadata: Optional[FeatureMetadata] = FeatureMetadata(),
    ):
        self.id = id
        self.name = name
        self.description = description
        self.project_id = project_id
        self.owner_id = owner_id
        self.catalog_type = catalog_type
        self.metadata = metadata
        self.feature_metadata = feature_metadata

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @id.setter
    def id(self, value: uuid.UUID):
        if value is not None and not isinstance(value, uuid.UUID):
            try:
                value = uuid.UUID(value)  # noqa
            except ValueError:
                raise ValueError("ID must be a valid UUID.")
        self._id = value

    @property
    def project_id(self) -> uuid.UUID:
        return self._project_id

    @project_id.setter
    def project_id(self, value: uuid.UUID):
        if value is not None and not isinstance(value, uuid.UUID):
            try:
                value = uuid.UUID(value)  # noqa
            except ValueError:
                raise ValueError("Project ID must be a valid UUID.")
        self._project_id = value

    @property
    def owner_id(self) -> str:
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        if value is not None and not isinstance(value, str):
            raise ValueError("Owner ID must be a string.")
        self._owner_id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Template name must be a string.")
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Description must be a string.")
        self._description = value

    @property
    def catalog_type(self) -> CatalogType:
        return self._catalog_type

    @catalog_type.setter
    def catalog_type(self, value: CatalogType):
        if not isinstance(value, CatalogType):
            raise ValueError("Catalog type must be an instance of CatalogType Enum.")
        self._catalog_type = value

    @property
    def metadata(self) -> Metadata:
        return self._metadata

    @metadata.setter
    def metadata(self, value: Metadata):
        if not self._isclass(value, Metadata):
            raise ValueError("Metadata must be an instance of Metadata class.")
        self._metadata = value

    @property
    def feature_metadata(self) -> FeatureMetadata:
        return self._feature_metadata

    @feature_metadata.setter
    def feature_metadata(self, value: FeatureMetadata):
        if not self._isclass(value, FeatureMetadata):
            raise ValueError(
                "FeatureMetadata must be an instance of FeatureMetadata class."
            )
        self._feature_metadata = value

    def get_df_template(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "catalogType": self.catalog_type,
            "entity": self.entity,
            "target": self.target,
            "features": self.features,
            "featuresQuery": self.features_query,
            "entityTargetsQuery": self.entity_targets_query,
            "predictionsQuery": self.predictions_query,
        }
