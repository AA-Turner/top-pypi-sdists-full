
from typing import Dict, List
from .....models.messages.message_templates import WhatsappTemplate, RequiredTemplateData, TemplateComponentForPayload, TemplateRequestPayload, FilledTemplateData
from .....models.messages.message_templates.required_for_frontend_templates import RequiredTemplateParameter
from .....models.messages.message_templates.filled_data_from_frontend import FilledRecipientParameter
from .....models.messages.message_templates.payload_for_sending_template import ComponentForPayload, TemplateComponentForPayload, TemplateRequestPayload, PositionalParameterForPayload, NamedParameterForPayload
from .....models.messages.message_templates.raw_meta_template import ParameterFormat
from .....models.execution.execution import ExecutionContext
from zoneinfo import ZoneInfo
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

class TemplateFactory:

    @staticmethod
    def instantiate_supported_templates(raw_templates : List[Dict]) -> List[WhatsappTemplate]:
        supported_templates = []
        for raw_template in raw_templates:
            try:
                template = WhatsappTemplate(**raw_template)
                supported_templates.append(template)
            except Exception as e:
                logger.warning(f"Error instantiating template {raw_template['name']}: {e}")
        return supported_templates

    @staticmethod
    def required_fields_for_template(template: WhatsappTemplate, execution_context : ExecutionContext) -> RequiredTemplateData:
        parameters = RequiredTemplateParameter.from_whatsapp_template(template)
        required_template_data = RequiredTemplateData(name=template.name, text=template.body_component.text, parameters=parameters)
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        return required_template_data

    @staticmethod
    def build_template_payload(template: WhatsappTemplate, template_data : FilledTemplateData) -> TemplateComponentForPayload:
        template_data.body = TemplateFactory.replace_parameters_in_body(template.body_component.text, template_data.parameters)

        if template.parameter_format == ParameterFormat.NAMED:
            parameters = NamedParameterForPayload.from_template_parameters(payload_parameters=template_data.parameters, template_parameters=template.body_parameters)
            components = [ComponentForPayload(type=template.body_component.type, parameters=parameters)]
        elif template.parameter_format == ParameterFormat.POSITIONAL:
            parameters = PositionalParameterForPayload.from_template_parameters(payload_parameters=template_data.parameters, template_parameters=template.body_parameters)
            components = [ComponentForPayload(type=template.body_component.type, parameters=parameters)]
        else:
            components = []

        return TemplateComponentForPayload(name=template.name, language={"code": template.language}, components=components)

    @staticmethod
    def build_template_request_payload(whatsapp_template : WhatsappTemplate, filled_template_data : FilledTemplateData) -> TemplateRequestPayload:
        template_payload = TemplateFactory.build_template_payload(template=whatsapp_template, template_data=filled_template_data)
        return TemplateRequestPayload(messaging_product="whatsapp", recipient_type="individual", to=filled_template_data.phone_number, type="template", template=template_payload)

    @staticmethod
    def replace_parameters_in_body(body : str, parameters : List[FilledRecipientParameter]) -> str:
        for parameter in parameters:
            body = body.replace(f"{{{{{parameter.id}}}}}", parameter.text)
        return body