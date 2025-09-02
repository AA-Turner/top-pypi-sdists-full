from __future__ import annotations
from enum import StrEnum
from typing import List, Optional, Any, Dict, Union
from pydantic import BaseModel, Field, model_validator

class Category(StrEnum):
    MARKETING = "MARKETING"
    UTILITY = "UTILITY"
    AUTHENTICATION = "AUTHENTICATION"

class ParameterFormat(StrEnum):
    NAMED = "NAMED"
    POSITIONAL = "POSITIONAL"
    NONE = "NONE"

class NamedParameter(BaseModel):
    param_name: str
    example: str


class TemplateExample(BaseModel):
    body_text_named_params: Optional[List[NamedParameter]] = None
    body_text: Optional[List[List[str]]] = None

class ComponentType(StrEnum):
    HEADER = "HEADER"
    BODY = "BODY"
    FOOTER = "FOOTER"
    BUTTONS = "BUTTONS"

class ButtonType(StrEnum):
    QUICK_REPLY = "QUICK_REPLY"
    URL = "URL"
    PHONE_NUMBER = "PHONE_NUMBER"
    COPY_CODE = "COPY_CODE"


class Button(BaseModel):
    type: ButtonType
    text: str
    url: Optional[str] = None
    phone_number: Optional[str] = None
    example: Optional[List[str]] = None

class HeaderExample(BaseModel):
    header_handle: Optional[List[str]] = None

class HeaderFormat(StrEnum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"


class TemplateComponent(BaseModel):
    type: ComponentType
    text: Optional[str] = None
    format: Optional[HeaderFormat] = None
    example: Optional[Union[TemplateExample, HeaderExample]] = None
    buttons: Optional[List[Button]] = None

    @model_validator(mode='before')
    def validate_component(cls, values):
        comp_type = values.get('type')
        if comp_type == ComponentType.BUTTONS and not values.get('buttons'):
            raise ValueError("Buttons component must have buttons field")
        if comp_type == ComponentType.HEADER and values.get('format') == HeaderFormat.IMAGE:
            if not values.get('example') or not values['example'].get('header_handle'):
                raise ValueError("Image header must have header_handle example")
        return values

    class ConfigDict:
        exclude_none = True

class WhatsappTemplate(BaseModel):
    name: str
    parameter_format: ParameterFormat | None = None
    components: List[TemplateComponent]
    language: str
    status: str
    category: str
    sub_category: Optional[str] = None
    id: str

    @property
    def body_parameters(self) -> List[NamedParameter | str]:
        if self.parameter_format == ParameterFormat.NAMED:
            return self.body_component.example.body_text_named_params
        elif self.parameter_format == ParameterFormat.POSITIONAL:
            return self.body_component.example.body_text[0]
        else:
            return []

    @property
    def body_component(self) -> TemplateComponent:
        return next((component for component in self.components if component.type == ComponentType.BODY), None)

    @property
    def header_component(self) -> TemplateComponent:
        return next((component for component in self.components if component.type == ComponentType.HEADER), None)

    @property
    def footer_component(self) -> TemplateComponent:
        return next((component for component in self.components if component.type == ComponentType.FOOTER), None)

    @property
    def buttons_component(self) -> TemplateComponent:
        return next((component for component in self.components if component.type == ComponentType.BUTTONS), None)

    @classmethod
    def from_meta_template(cls, template: Dict[str, Any]) -> WhatsappTemplate:
        return cls(**template)

    @classmethod
    def is_supported_by_chatty(cls, template: WhatsappTemplate) -> bool:
        if template.category not in [Category.MARKETING, Category.UTILITY]:
            return False
        #So far we only support text templates, only body
        if len(template.components) > 1 or template.components[0].type != ComponentType.BODY:
            return False
        return True

    @model_validator(mode='after')
    def validate_parameter_format(self):
        if not any(component.example for component in self.components):
            self.parameter_format = ParameterFormat.NONE

        return self
