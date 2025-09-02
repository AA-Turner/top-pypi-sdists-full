from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from typing import ClassVar
from ....utils.types.identifier import StrObjectId
from ....company.assets.product import Product
from typing import Optional
from pydantic import field_validator, ValidationInfo, Field
from ....utils.types.serializer_type import SerializerType
import json

class ProductChatData(CustomerEventData):
    product_id: StrObjectId
    product: Optional[Product] = Field(description="The product object")
    time_to_product_seconds: Optional[int] = None

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['product'] = self.product.model_dump_json(serializer=SerializerType.API) if self.product else None
        return dump

class ProductChatEvent(Event):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    data: ProductChatData

    VALID_TYPES: ClassVar[set] = {
        EventType.PRODUCT_ASSIGNED,
        EventType.PRODUCT_REMOVED
    }

    @field_validator('data')
    def validate_data_fields(cls, v: ProductChatData, info: ValidationInfo):
        if info.data.get('type') != EventType.PRODUCT_REMOVED and not v.product:
            raise ValueError("product must be set for all events except PRODUCT_REMOVED")
        return v

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump