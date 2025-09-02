from pydantic import BaseModel, Field, model_validator
from typing import List, Any, Dict, Optional
from enum import StrEnum
from .schema.values.value_messages import Message
from .schema.values.value_statuses import StatusNotification
from .schema.values.value_errors import Error

class NotificationType(StrEnum):
    MESSAGES = "messages"
    STATUSES = "statuses"
    ERRORS = "errors"  
    UNKNOWN = "unknown"
    
class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str

class Profile(BaseModel):
    name: str

class Contact(BaseModel):
    profile: Profile
    wa_id: str
    
    def get_name(self) -> str:
        return self.profile.name
    
    def get_wa_id(self) -> str:
        return self.wa_id

class Value(BaseModel):
    messaging_product: str
    metadata: Metadata = Field(default=None)
    contacts: List[Contact] = Field(default_factory= lambda: [])
    messages: List[Message] = Field(default_factory= lambda: [])
    statuses: List[StatusNotification] = Field(default_factory= lambda: [])
    errors: List[Error] = Field(default_factory= lambda: [])

    def is_messages(self) -> bool:
        return bool(self.messages != [])

    def is_statuses(self) -> bool:
        return bool(self.statuses != [])
    
    def is_errors(self) -> bool:
        return bool(self.errors != [])
    
class Change(BaseModel):
    value: Value
    field: str

    @model_validator(mode='before')
    @classmethod
    def not_implemented_field(cls, data: Dict) -> Dict:
        # Handle case where data is None
        if not isinstance(data, dict):
            return data
        
        # Be explicit about which fields are not implemented
        not_implemented_fields = {
            'message_template_quality_update',
            'message_template_status_update',
            'account_update'
        }
        
        if data.get('field') in not_implemented_fields:
            raise NotImplementedError(f"Field '{data.get('field')}' is not implemented")
        return data

class Entry(BaseModel):
    id: str = Field(description="WABA id")
    changes: List[Change]

class BaseMetaNotificationJson(BaseModel):
    object: str
    entry: List[Entry]

    def get_notification_type(self) -> NotificationType: 
    
        try: 
            value = self.entry[0].changes[0].value

            if value.is_messages():
                return NotificationType.MESSAGES
            elif value.is_statuses():
                return NotificationType.STATUSES
            elif value.is_errors():
                return NotificationType.ERRORS
            else:
                return NotificationType.UNKNOWN
                
        except ValueError:
            return NotificationType.UNKNOWN
        
    
    def get_value(self) -> Value:
        return self.entry[0].changes[0].value
    
    def get_metadata(self) -> Metadata:
        return self.get_value().metadata
    
    def get_phone_number_id(self) -> str:
        return self.get_metadata().phone_number_id
