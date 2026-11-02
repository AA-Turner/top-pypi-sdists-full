from enum import StrEnum
from pydantic import field_validator, ValidationInfo
from ....utils.types.identifier import StrObjectId
from typing import Optional, ClassVar
from ....utils.types.executor_types import ExecutorType
from ..base import Event, EventType, EventData
from ....utils.types.serializer_type import SerializerType
from ....company.empresa import EmpresaModel
import json
class CompanyEventData(EventData):
    company_id: StrObjectId
    company : Optional[EmpresaModel] = None

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['company'] = self.company.model_dump_json(serializer=SerializerType.API) if self.company else None
        return dump

    @property
    def message_group_id(self) -> str:
        return f"company-{self.company_id}"

class CompanyEvent(Event):
    data: CompanyEventData

    VALID_TYPES: ClassVar[set] = {
        EventType.COMPANY_CREATED,
        EventType.COMPANY_UPDATED,
        EventType.COMPANY_DELETED
    }

    @field_validator('data')
    def validate_data_fields(cls, v: CompanyEventData, info: ValidationInfo):
        if info.data.get('type') == EventType.COMPANY_CREATED and not v.company:
            raise ValueError("company must be set for COMPANY_CREATED events")
        if info.data.get('type') == EventType.COMPANY_UPDATED and not v.company:
            raise ValueError("company must be set for COMPANY_UPDATED events")
        return v

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump