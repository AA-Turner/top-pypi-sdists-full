from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from ....company.assets.sale import Sale
from ....utils.types.identifier import StrObjectId
from pydantic import Field, field_validator, ValidationInfo
from typing import Optional, ClassVar
from ....utils.types.serializer_type import SerializerType
import json

class SaleData(CustomerEventData):
    sale: Optional[Sale] = Field(description="The sale object", default=None)
    sale_id: StrObjectId
    is_first_sale: Optional[bool] = Field(default=None, description="Whether the sale is the first sale of the chat")
    time_to_sale_seconds: Optional[int] = Field(default=None, description="The time it took the chat to get the sale since the chat creation")

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['sale'] = self.sale.model_dump_json(serializer=SerializerType.API) if self.sale else None
        return dump

class SaleEvent(Event):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    data: SaleData

    VALID_TYPES: ClassVar[set] = {
        EventType.SALE_CREATED,
        EventType.SALE_UPDATED,
        EventType.SALE_DELETED
    }

    @field_validator('data')
    def validate_data_fields(cls, v: SaleData, info: ValidationInfo):
        if info.data.get('type') != EventType.SALE_DELETED and not v.sale:
            raise ValueError("sale must be set for all events except SALE_DELETED")
        return v

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump


