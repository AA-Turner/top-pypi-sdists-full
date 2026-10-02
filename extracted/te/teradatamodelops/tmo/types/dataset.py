import logging
import uuid
from enum import Enum
from typing import Optional, Union

from tmo.types.base_dataset import BaseDatasetMixin
from tmo.types.dataset_metadata import Metadata, CatalogType

logger = logging.getLogger(__name__)


class Scope(Enum):
    TRAIN = "train"
    EVALUATE = "evaluate"


class Dataset(BaseDatasetMixin):
    id: uuid.UUID
    dataset_template_id: uuid.UUID
    name: str
    description: str
    query: str
    scope: Scope
    metadata: Union[Metadata, dict]  # NOSONAR
    catalog_type: CatalogType

    def __init__(
        self,
        id: Optional[uuid.UUID] = None,
        dataset_template_id: Optional[uuid.UUID] = None,
        name: Optional[str] = "SDK Dataset",
        description: Optional[str] = "VANTAGE dataset",
        query: Optional[str] = None,
        scope: Optional[Scope] = None,
        metadata: Optional[Union[Metadata, dict]] = None,
        catalog_type: CatalogType = CatalogType.VANTAGE,
    ):
        self.id = id
        self.dataset_template_id = dataset_template_id
        self.name = name
        self.description = description
        self.query = query
        self.scope = scope
        # IMPORTANT: Set catalog_type BEFORE metadata (setter validates based on catalog_type)
        self.catalog_type = catalog_type
        # Initialize metadata based on catalog_type if not provided
        if metadata is None:
            metadata = Metadata() if catalog_type == CatalogType.VANTAGE else {}
        self.metadata = metadata

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @id.setter
    def id(self, value: uuid.UUID):
        if value is not None and not isinstance(value, uuid.UUID):
            try:
                value = uuid.UUID(value)  # noqa
            except ValueError:
                raise ValueError("Project ID must be a valid UUID.")
        self._id = value  # noqa

    @property
    def dataset_template_id(self) -> uuid.UUID:
        return self._dataset_template_id

    @dataset_template_id.setter
    def dataset_template_id(self, value: uuid.UUID):
        if value is not None and not isinstance(value, uuid.UUID):
            try:
                value = uuid.UUID(value)  # noqa
            except ValueError:
                raise ValueError("Dataset template ID must be a valid UUID.")
        self._dataset_template_id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def query(self) -> str:
        return self._query

    @query.setter
    def query(self, value: str):
        if value is not None and not isinstance(value, str):
            raise ValueError("Query must be a string.")
        self._query = value

    @property
    def scope(self) -> Scope:
        return self._scope

    @scope.setter
    def scope(self, value: Scope):
        self._scope = value

    @property
    def catalog_type(self) -> CatalogType:
        return self._catalog_type

    @catalog_type.setter
    def catalog_type(self, value: CatalogType):
        if not isinstance(value, CatalogType):
            raise ValueError("Catalog type must be an instance of CatalogType.")
        self._catalog_type = value

    def get_df_template(self) -> dict:
        from tmo.types.utils.datasets import build_df_template

        return build_df_template(self)
