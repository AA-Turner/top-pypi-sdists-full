from ..base import Event, EventType, EventData
from ....utils.types.identifier import StrObjectId
from ....base_models.chatty_asset_model import ChattyAssetModel
from pydantic import BaseModel, Field, model_validator
from ....company.assets.company_assets import CompanyAssetType
from ....utils.types.serializer_type import SerializerType
from typing import ClassVar, Optional
from ....utils.types.executor_types import ExecutorType
import json

class AssetData(EventData):
    asset_id: StrObjectId
    asset: Optional[ChattyAssetModel] = Field(default=None)
    asset_type: CompanyAssetType
    executor_type: ExecutorType
    executor_id: StrObjectId

    @property
    def message_group_id(self) -> str:
        return f"asset-{self.asset_id}"

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump["asset"] = self.asset.model_dump_json(serializer=SerializerType.API) if self.asset else None
        return dump

class AssetEvent(Event):
    data: AssetData

    VALID_TYPES: ClassVar[set] = {
        EventType.PRODUCT_CREATED,
        EventType.PRODUCT_UPDATED,
        EventType.PRODUCT_DELETED,
        EventType.SOURCE_CREATED,
        EventType.SOURCE_UPDATED,
        EventType.SOURCE_DELETED,
        EventType.TAG_CREATED,
        EventType.TAG_UPDATED,
        EventType.TAG_DELETED,
        EventType.USER_CREATED,
        EventType.USER_UPDATED,
        EventType.USER_DELETED,
        EventType.FAST_ANSWER_CREATED,
        EventType.FAST_ANSWER_UPDATED,
        EventType.FAST_ANSWER_DELETED,
        EventType.SALE_CREATED,
        EventType.SALE_UPDATED,
        EventType.SALE_DELETED,
        EventType.BUSINESS_AREA_CREATED,
        EventType.BUSINESS_AREA_UPDATED,
        EventType.BUSINESS_AREA_DELETED,
        EventType.TOPIC_CREATED,
        EventType.TOPIC_UPDATED,
        EventType.TOPIC_DELETED,
        EventType.FUNNEL_CREATED,
        EventType.FUNNEL_UPDATED,
        EventType.FUNNEL_DELETED,
        EventType.FUNNEL_STAGE_CREATED,
        EventType.FUNNEL_STAGE_UPDATED,
        EventType.FUNNEL_STAGE_DELETED,
        EventType.WORKFLOW_CREATED,
        EventType.WORKFLOW_UPDATED,
        EventType.WORKFLOW_DELETED,
        EventType.AI_COMPONENT_CREATED,
        EventType.AI_COMPONENT_UPDATED,
        EventType.AI_COMPONENT_DELETED,
        EventType.CHATTY_AI_AGENT_DELETED,
        EventType.CHATTY_AI_AGENT_CREATED,
        EventType.CHATTY_AI_AGENT_UPDATED,
        EventType.FILTER_CRITERIA_CREATED,
        EventType.FILTER_CRITERIA_UPDATED,
        EventType.FILTER_CRITERIA_DELETED,
        EventType.COMPANY_CREATED,
        EventType.COMPANY_UPDATED,
        EventType.COMPANY_DELETED
    }

    @model_validator(mode='after')
    def validate_data_fields(self):
        if "deleted" not in self.type.value and not self.data.asset:
            raise ValueError("asset must be set for all events except DELETED")
        return self

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump
