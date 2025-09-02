from __future__ import annotations
from typing import List, TYPE_CHECKING
from pydantic import BaseModel
import logging
from letschatty.models.messages.message_templates.raw_meta_template import ParameterFormat

if TYPE_CHECKING:
    from letschatty.models.messages.message_templates.raw_meta_template import NamedParameter
    from letschatty.models.messages.message_templates.raw_meta_template import WhatsappTemplate

logger = logging.getLogger(__name__)

class RequiredTemplateParameter(BaseModel):
    id: str
    example: str

    @classmethod
    def from_whatsapp_template(cls, template : WhatsappTemplate) -> List[RequiredTemplateParameter]:
        if template.parameter_format == ParameterFormat.NAMED:
            return RequiredTemplateParameter.from_named_parameters(template.body_component.example.body_text_named_params)
                    
        if template.parameter_format == ParameterFormat.POSITIONAL:
            return RequiredTemplateParameter.from_positional_parameters(template.body_component.example.body_text[0])
        
        if template.parameter_format == ParameterFormat.NONE:
            return []

    @classmethod
    def from_named_parameters(cls, parameters : List[NamedParameter]) -> List[RequiredTemplateParameter]:
        return [RequiredTemplateParameter(id=parameter.param_name, example=parameter.example) for parameter in parameters]
    
    @classmethod
    def from_positional_parameters(cls, parameters : List[str]) -> List[RequiredTemplateParameter]:
        return [RequiredTemplateParameter(id=str(index+1), example=parameter) for index, parameter in enumerate(parameters)]

class RequiredTemplateData(BaseModel):
    name: str
    text: str
    parameters: List[RequiredTemplateParameter]

