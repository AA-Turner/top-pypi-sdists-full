"""Filter Criteria Collection - Pre-configured AssetCollection for Filter Criterias"""

from ..asset_service import AssetCollection
from ....models.company.assets.filter_criteria import FilterCriteria, FilterCriteriaPreview
from ....models.data_base.mongo_connection import MongoConnection


class FilterCriteriaCollection(AssetCollection[FilterCriteria, FilterCriteriaPreview]):
    """Pre-configured collection for Filter Criteria assets"""

    def __init__(self, connection: MongoConnection):
        super().__init__(
            collection="filter_criterias",
            asset_type=FilterCriteria,
            connection=connection,
            create_instance_method=FilterCriteria.default_create_instance_method,
            preview_type=FilterCriteriaPreview
        )
