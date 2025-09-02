from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field
from .filled_data_from_frontend import FilledRecipientParameter
from .raw_meta_template import ComponentType, NamedParameter

class NamedParameterForPayload(BaseModel):
    type: str = Field(default="text")
    parameter_name: str
    text: str
    
    @classmethod
    def from_template_parameters(cls, payload_parameters: List[FilledRecipientParameter], template_parameters: List[NamedParameter]) -> List[NamedParameterForPayload]:
        #first validate that the ids of the payload params are in the template params
        param_names = [named_param.param_name for named_param in template_parameters]
        if not all(param.id in param_names for param in payload_parameters):
            raise ValueError(f"The ids of the payload params {[param.id for param in payload_parameters]} are not in the template params {param_names}")
        return [cls(type="text", parameter_name=parameter.id, text=parameter.text) for parameter in payload_parameters]

class PositionalParameterForPayload(BaseModel):
    type: str = Field(default="text")
    text: str
    
    @classmethod
    def from_template_parameters(cls, payload_parameters: List[FilledRecipientParameter], template_parameters: List[str]) -> List[PositionalParameterForPayload]:
        # Create a dict mapping parameter id (position) to parameter text
        param_dict = {int(param.id): param.text for param in payload_parameters}
        #validate that the ids of the payload params are in the template params
        if not all(param_index <= len(template_parameters) for param_index in param_dict):
            raise ValueError(f"Expecting {len(template_parameters)} positional parameters, but got indexes: {param_dict.keys()}")
        param_payloads = []
        for param in param_dict:
            param_payload = cls(type="text", text=param_dict[param])
            param_payloads.append(param_payload)
        return param_payloads

class ComponentForPayload(BaseModel):
    type: ComponentType
    parameters: List[NamedParameterForPayload | PositionalParameterForPayload]

class TemplateComponentForPayload(BaseModel):
    name: str
    language: dict 
    components: List[ComponentForPayload]

class TemplateRequestPayload(BaseModel):
    messaging_product: str = Field(default="whatsapp")
    recipient_type: str = Field(default="individual")
    to: str
    type: str = Field(default="template")
    template: TemplateComponentForPayload
