from __future__ import annotations
from pydantic import BaseModel, Field, model_validator, field_validator
from typing import List, Optional

from letschatty.models.messages.chatty_messages import ChattyMessage
from letschatty.models.utils.types import Status
from .filled_data_from_frontend import FilledRecipientParameter
from .raw_meta_template import WhatsappTemplate
from .required_for_frontend_templates import RequiredTemplateParameter
from enum import StrEnum


class RecipientOfTemplateCampaign(BaseModel):
    phone_number: str
    new_contact_name: Optional[str] = None
    parameters: List[FilledRecipientParameter] = Field(default_factory=list)
    status: Status = Field(default=Status.PENDING)
    details: Optional[str] = None
    message_id: Optional[str] = None

    @field_validator("phone_number", mode="before")
    def validate_phone_number(cls, v):
        if v is None:
            raise ValueError("Phone number is required for all recipients")
        return v

    @model_validator(mode="after")
    def validate_new_contact_name(self) -> RecipientOfTemplateCampaign:
        if self.new_contact_name is None:
            self.new_contact_name = self.phone_number
        return self

    @classmethod
    def example_recipient(cls, whatsapp_template : WhatsappTemplate) -> RecipientOfTemplateCampaign:
        required_parameters = RequiredTemplateParameter.from_whatsapp_template(whatsapp_template)
        return cls(phone_number="5491166317681", new_contact_name="Axel Example", parameters=[FilledRecipientParameter(id=parameter.id, text=parameter.example) for parameter in required_parameters])

    @property
    def is_example_recipient(self) -> bool:
        return self.new_contact_name == "Axel Example"

    def succesfull_meta_api_call(self,message_id:str) -> None:
        self.message_id = message_id
        self.status = Status.META_API_CALL_SUCCESS
        return

    def failed_meta_api_call(self) -> None:
        self.message_id = None
        self.status = Status.FAILED
        return

    def to_row(self, just_columns_and_example: bool = False) -> dict:
        fields = {"phone_number": self.phone_number, "new_contact_name": self.new_contact_name}
        for parameter in self.parameters:
            fields[parameter.id] = parameter.text
        if not just_columns_and_example:
            fields["status"] = self.status
            fields["details"] = self.details
            fields["message_id"] = self.message_id
        return fields

    @property
    def sent_message_id(self) -> str:
        if not self.message_id:
            raise ValueError("Message id is not set for template recipient: " + self.phone_number)
        return self.message_id

    @property
    def was_message_succesfully_sent_and_is_still_updatable(self) -> bool:
        return self.status in [Status.META_API_CALL_SUCCESS, Status.SENT, Status.DELIVERED]

    def update_status(self, message: ChattyMessage) -> None:
        self.status = message.status
        if message.status == Status.FAILED:
            self.details = "El mensaje no pudo ser efectivamente enviado por un problema en Meta. Revisar el chat para más detalles."
        else:
            self.details = f"El último estado notificado por Meta del mensaje es {message.status}"
        return