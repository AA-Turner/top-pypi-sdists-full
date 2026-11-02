
from typing import Dict, List
from .....models.messages.message_templates import WhatsappTemplate, RequiredTemplateData, TemplateComponentForPayload, TemplateRequestPayload, FilledTemplateData
from .....models.messages.message_templates.required_for_frontend_templates import RequiredTemplateParameter
from .....models.messages.message_templates.filled_data_from_frontend import FilledRecipientParameter
from .....models.messages.message_templates.payload_for_sending_template import ComponentForPayload, TemplateComponentForPayload, TemplateRequestPayload, PositionalParameterForPayload, NamedParameterForPayload
from .....models.messages.message_templates.raw_meta_template import ParameterFormat
from .....models.messages.message_templates.header_media import TemplateHeaderKind
from .....models.messages.chatty_messages.schema.chatty_context.template_rendering import TemplateRendering, TemplateRenderedButton
from .component_builders import DEFAULT_COMPONENT_BUILDERS
from .....models.execution.execution import ExecutionContext
from zoneinfo import ZoneInfo
from datetime import datetime
import logging
import re
logger = logging.getLogger(__name__)

class TemplateFactory:

    @staticmethod
    def _header_text(template):
        """El texto crudo del encabezado, sólo si es de TEXTO. Un encabezado multimedia no tiene."""
        from .....models.messages.message_templates.raw_meta_template import HeaderFormat
        header = template.header_component
        if header is None or (header.format or HeaderFormat.TEXT) != HeaderFormat.TEXT:
            return None
        return header.text

    @staticmethod
    def _header_parameters(template) -> list:
        """Las variables del encabezado, con su ejemplo, para que la pantalla las pida."""
        from .....models.messages.message_templates.required_for_frontend_templates import RequiredTemplateParameter
        if not template.header_has_variable:
            return []
        header = template.header_component
        ejemplo = header.example if header else None
        ejemplos = list(getattr(ejemplo, "header_text", None) or [])
        return [
            RequiredTemplateParameter(id=nombre, example=(ejemplos[i] if i < len(ejemplos) else ""))
            for i, nombre in enumerate(template.header_parameters)
        ]

    @staticmethod
    def _button_parameters(template) -> list:
        """Los botones que piden un valor, con su texto visible."""
        from .....models.messages.message_templates.required_for_frontend_templates import RequiredButtonParameter
        from .....models.messages.message_templates.raw_meta_template import ComponentType
        componente = next((c for c in template.components if c.type == ComponentType.BUTTONS), None)
        botones = (componente.buttons if componente else None) or []
        return [
            RequiredButtonParameter(
                index=indice, sub_type=sub_type, label=botones[indice].text,
                example=(botones[indice].example or [None])[0] if botones[indice].example else None,
            )
            for indice, sub_type in template.buttons_needing_parameters
        ]

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
    def render_for_chat(template: WhatsappTemplate, data: FilledTemplateData | None = None) -> TemplateRendering:
        """Lo que el cliente ve además del cuerpo: encabezado de texto, pie y botones.

        Con `data` (un envío) las variables quedan completadas: el encabezado con sus valores, el enlace
        con su sufijo y el código de copiar. Sin `data` (la vista previa, antes de completar nada)
        queda la plantilla tal cual, con sus `{{1}}`: la pantalla los completa mientras se escribe.
        Es la MISMA función para las dos cosas, así la previa y el chat no pueden contar historias
        distintas.

        El encabezado usa la misma sustitución que el cuerpo (`replace_parameters_in_body`). Sólo
        cubre el mensaje principal: los botones de las tarjetas de un carrusel quedan afuera.
        """
        from .....models.messages.message_templates.raw_meta_template import ComponentType, HeaderFormat

        header_text = None
        header = template.header_component
        if header is not None and (header.format or HeaderFormat.TEXT) == HeaderFormat.TEXT and header.text:
            header_text = header.text
            if data is not None and data.header_parameters:
                header_text = TemplateFactory.replace_parameters_in_body(header_text, data.header_parameters)

        footer = next((c for c in template.components if c.type == ComponentType.FOOTER), None)
        footer_text = (footer.text or None) if footer is not None else None

        valores = {p.index: p.text for p in data.button_parameters} if data is not None else {}
        bloque = next((c for c in template.components if c.type == ComponentType.BUTTONS), None)
        botones = []
        for indice, boton in enumerate((bloque.buttons if bloque is not None else None) or []):
            valor = valores.get(indice)
            url = boton.url
            if url and valor is not None and "{{" in url:
                url = re.sub(r"\{\{\s*[^{}]+?\s*\}\}", lambda _m: valor, url, count=1)
            botones.append(TemplateRenderedButton(
                type=str(boton.type.value if hasattr(boton.type, "value") else boton.type),
                text=boton.text,
                url=url,
                phone_number=boton.phone_number,
                code=valor if str(boton.type) == "COPY_CODE" else None,
            ))
        return TemplateRendering(header_text=header_text, footer_text=footer_text, buttons=botones)

    @staticmethod
    def required_fields_for_template(template: WhatsappTemplate, execution_context : ExecutionContext) -> RequiredTemplateData:
        parameters = RequiredTemplateParameter.from_whatsapp_template(template)
        # S-6: null-guard the BODY deref — a template with no BODY component (possible under the widened
        # read model) would AttributeError here and 500 /required_fields. Fall back to "".
        body = template.body_component
        text = body.text if body is not None else ""
        # Qué necesita el encabezado. Sin esto quien llama no tiene forma de saber que la plantilla pide
        # un archivo, y el envío falla recién en Meta.
        header = template.header_component
        header_format = header.format.value if header is not None and header.format is not None else None
        header_kind = TemplateHeaderKind.from_header_format(header_format)
        required_template_data = RequiredTemplateData(
            name=template.name, text=text or "", parameters=parameters,
            category=template.category, language=template.language, status=template.status,   # A5 (additive)
            header_format=header_format,
            requires_header_media=header_kind is not None,
            header_media_kind=header_kind.value if header_kind is not None else None,
            # Si la plantilla ya trae su archivo, adjuntar es opcional: sin adjunto se usa ése.
            header_media_available=bool(header_kind is not None and template.header_media_example_url),
            header_text=TemplateFactory._header_text(template),
            header_parameters=TemplateFactory._header_parameters(template),
            button_parameters=TemplateFactory._button_parameters(template),
            # Para que la vista previa muestre la imagen real en vez de un cartel "[imagen]".
            header_media_url=template.header_media_example_url if header_kind is not None else None,
        )
        # Pie y botones para la vista previa: la misma función que después guarda el mensaje enviado.
        rendering = TemplateFactory.render_for_chat(template)
        required_template_data.footer_text = rendering.footer_text
        required_template_data.buttons = rendering.buttons
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        return required_template_data

    @staticmethod
    def build_template_payload(template: WhatsappTemplate, template_data : FilledTemplateData) -> TemplateComponentForPayload:
        """Arma el bloque `template` del payload de /messages recorriendo los armadores de componentes.

        Cada armador decide si le toca y arma lo suyo (ver `component_builders`). Una plantilla de sólo
        texto produce exactamente el mismo payload que antes de que existiera el encabezado multimedia:
        el armador del encabezado no aplica y queda únicamente el cuerpo.
        """
        # El cuerpo renderizado se guarda en el DTO: es lo que después se muestra en el chat. El guard
        # es por las plantillas sin BODY, que el modelo de lectura ahora acepta y antes reventaban acá.
        body = template.body_component
        if body is not None:
            template_data.body = TemplateFactory.replace_parameters_in_body(body.text or "", template_data.parameters)

        # Un armador puede emitir uno o varios componentes: los botones necesitan uno POR botón, porque
        # Meta los identifica por su posición en el array BUTTONS. `build_many` es el caso general.
        components = []
        for builder in DEFAULT_COMPONENT_BUILDERS:
            if not builder.applies(template, template_data):
                continue
            construir_varios = getattr(builder, "build_many", None)
            if construir_varios is not None:
                components.extend(construir_varios(template, template_data))
            else:
                components.append(builder.build(template, template_data))

        return TemplateComponentForPayload(name=template.name, language={"code": template.language}, components=components)

    @staticmethod
    def build_template_request_payload(whatsapp_template : WhatsappTemplate, filled_template_data : FilledTemplateData) -> TemplateRequestPayload:
        """Arma el payload de /messages, ruteando el destinatario segun la identidad.

        Telefono → `to` (camino de siempre, payload sin cambios). Solo BSUID —
        contacto que adopto username de WhatsApp — → `recipient`. Antes esto pasaba
        `to=phone_number` a secas, asi que un contacto sin telefono producia
        `to=None` y el modelo lo rechazaba.
        """
        template_payload = TemplateFactory.build_template_payload(template=whatsapp_template, template_data=filled_template_data)
        recipient_kwargs = (
            {"recipient": filled_template_data.user_id}
            if filled_template_data.is_phone_less
            else {"to": filled_template_data.phone_number}
        )
        return TemplateRequestPayload(messaging_product="whatsapp", recipient_type="individual", type="template", template=template_payload, **recipient_kwargs)

    @staticmethod
    def replace_parameters_in_body(body : str, parameters : List[FilledRecipientParameter]) -> str:
        for parameter in parameters:
            body = body.replace(f"{{{{{parameter.id}}}}}", parameter.text)
        return body