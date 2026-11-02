"""Filter Criteria Service - Pre-configured AssetService for Filter Criterias"""

from ..asset_service import AssetService, CacheConfig
from ..collections import FilterCriteriaCollection
from ....models.company.assets.filter_criteria import FilterCriteria, FilterCriteriaPreview
from ....models.data_base.mongo_connection import MongoConnection
from ....models.analytics.events import CompanyAssetType, EventType


class FilterCriteriaService(AssetService[FilterCriteria, FilterCriteriaPreview]):
    """Pre-configured service for Filter Criteria assets with sensible defaults"""

    # Event configuration - enables automatic event handling in API
    asset_type_enum = CompanyAssetType.FILTER_CRITERIA
    event_type_created = EventType.FILTER_CRITERIA_CREATED
    event_type_updated = EventType.FILTER_CRITERIA_UPDATED
    event_type_deleted = EventType.FILTER_CRITERIA_DELETED

    def __init__(self,
                 connection: MongoConnection,
                 cache_config: CacheConfig = CacheConfig()):
        collection = FilterCriteriaCollection(connection)
        super().__init__(
            collection=collection,
            cache_config=cache_config
        )

