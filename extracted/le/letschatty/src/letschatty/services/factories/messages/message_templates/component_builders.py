"""Armadores de los componentes del payload de una plantilla.

Antes `build_template_payload` era un `if/elif` que sólo sabía armar el BODY. Sumarle el encabezado
multimedia con más ramas obligaba a volver a tocar —y arriesgar— el código que envía **todas** las
plantillas cada vez que aparece un formato nuevo.

Acá cada componente es un armador independiente que responde dos preguntas: *¿me toca?* (`applies`) y
*¿cuál es mi componente?* (`build`). El factory sólo los recorre en orden. Sumar ubicación, carrusel o
botones más adelante es **agregar** un armador, no **modificar** los que ya andan.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Optional, Protocol

from .....models.messages.message_templates.filled_data_from_frontend import FilledTemplateData
from .....models.messages.message_templates.header_media import TemplateHeaderKind
from .....models.messages.message_templates.payload_for_sending_template import (
    ButtonTextParameter,
    ComponentForPayload,
    CouponCodeParameter,
    FlowActionParameter,
    LimitedTimeOfferParameter,
    HeaderMediaParameter,
    NamedParameterForPayload,
    PositionalParameterForPayload,
)
from .....models.messages.message_templates.raw_meta_template import (
    ButtonType,
    ComponentType,
    ParameterFormat,
    WhatsappTemplate,
)
from .....models.utils.custom_exceptions.custom_exceptions import (
    TemplateButtonParameterMissing,
    TemplateHeaderMediaMismatch,
    TemplateHeaderMediaMissing,
    TemplateHeaderMediaUnresolved,
    TemplateHeaderParameterMissing,
)


@dataclass(frozen=True)
class Shape:
    """Las formas de plantilla que un armador sabe enviar.

    Se declara por conjuntos y no por una lista de strings sueltos para que la unión de dos armadores
    sea trivial y no haya que interpretar nada al reconciliarlos.
    """

    header_formats: frozenset[str] = field(default_factory=frozenset)
    button_kinds: frozenset[str] = field(default_factory=frozenset)
    component_types: frozenset[str] = field(default_factory=frozenset)

    def __or__(self, other: "Shape") -> "Shape":
        return Shape(
            header_formats=self.header_formats | other.header_formats,
            button_kinds=self.button_kinds | other.button_kinds,
            component_types=self.component_types | other.component_types,
        )


class TemplateComponentBuilder(Protocol):
    """Contrato de un armador de componentes.

    `applies` decide si el componente corresponde para esta plantilla y estos datos; `build` sólo se
    llama si `applies` dio True, así que puede asumir esa precondición.

    `handles` es la declaración de CAPACIDAD: qué formas sabe enviar este armador. De la unión de esas
    declaraciones sale la compuerta de enviabilidad (`unsupported_shapes`), en vez de una lista escrita
    a mano en otro repo. Es lo que hace imposible volver a ofrecer una forma sin su armador: la
    enviabilidad se DERIVA del armador, no se declara al lado.
    """

    def applies(self, template: WhatsappTemplate, data: FilledTemplateData) -> bool: ...

    def build(self, template: WhatsappTemplate, data: FilledTemplateData) -> ComponentForPayload: ...

    def handles(self) -> Shape: ...


class HeaderComponentBuilder:
    """Componente `header` con el archivo multimedia.

    Aplica sólo a encabezados de imagen, video o documento. Un encabezado de texto no arma componente:
    si es fijo Meta no lo espera, y si tiene variables todavía no está soportado (queda como el
    siguiente armador a escribir). Un formato desconocido tampoco aplica, así que una plantilla rara
    nunca produce un payload roto.
    """

    def applies(self, template: WhatsappTemplate, data: FilledTemplateData) -> bool:
        return self._kind(template) is not None


    def handles(self) -> Shape:
        return Shape(header_formats=frozenset({"IMAGE", "VIDEO", "DOCUMENT"}))

    def build(self, template: WhatsappTemplate, data: FilledTemplateData) -> ComponentForPayload:
        kind = self._kind(template)
        media = data.header_media

        if media is None:
            raise TemplateHeaderMediaMissing(
                f"La plantilla '{template.name}' necesita un archivo de tipo {kind.value} en el encabezado "
                f"y el envío no adjuntó ninguno",
                details=f"template={template.name} kind={kind.value}",
            )
        if media.kind != kind:
            raise TemplateHeaderMediaMismatch(
                f"La plantilla '{template.name}' espera un archivo de tipo {kind.value} en el encabezado, "
                f"pero se adjuntó uno de tipo {media.kind.value}",
                details=f"template={template.name} esperado={kind.value} recibido={media.kind.value}",
            )
        if not media.media_id:
            # Error de programación: se llegó a armar el payload sin resolver la media contra Meta.
            raise TemplateHeaderMediaUnresolved(
                f"El archivo del encabezado de '{template.name}' no tiene media_id de Meta",
                details=f"template={template.name} url={media.url}",
            )

        return ComponentForPayload(
            type=ComponentType.HEADER,
            parameters=[
                HeaderMediaParameter(type=kind, media_id=media.media_id, filename=media.filename)
            ],
        )

    @staticmethod
    def _kind(template: WhatsappTemplate) -> TemplateHeaderKind | None:
        header = template.header_component
        if header is None:
            return None
        return TemplateHeaderKind.from_header_format(header.format)


class BodyComponentBuilder:
    """Componente `body` con las variables de texto.

    Encapsula, sin cambiarla, la lógica que ya existía: variables con nombre o posicionales, y ningún
    componente cuando la plantilla no tiene variables. Se le suma un guard por si no hay BODY —antes
    reventaba con AttributeError— posible desde que el modelo de lectura acepta más formas.
    """

    def applies(self, template: WhatsappTemplate, data: FilledTemplateData) -> bool:
        if template.body_component is None:
            return False
        return template.parameter_format in (ParameterFormat.NAMED, ParameterFormat.POSITIONAL)

    def handles(self) -> Shape:
        return Shape(component_types=frozenset({"BODY"}))

    def build(self, template: WhatsappTemplate, data: FilledTemplateData) -> ComponentForPayload:
        if template.parameter_format == ParameterFormat.NAMED:
            parameters = NamedParameterForPayload.from_template_parameters(
                payload_parameters=data.parameters, template_parameters=template.body_parameters
            )
        else:
            parameters = PositionalParameterForPayload.from_template_parameters(
                payload_parameters=data.parameters, template_parameters=template.body_parameters
            )
        return ComponentForPayload(type=template.body_component.type, parameters=parameters)




class HeaderTextComponentBuilder:
    """El encabezado de TEXTO con variable.

    Un encabezado de texto estático no lleva componente (Meta ya lo tiene aprobado). Uno con `{{1}}`
    SÍ, y hasta ahora no se armaba: la plantilla pasaba todas las compuertas y Meta la rechazaba por
    cantidad de parámetros. Meta admite **una sola** variable en el encabezado.
    """

    def handles(self) -> Shape:
        return Shape(header_formats=frozenset({"TEXT_CON_VARIABLE"}))

    def applies(self, template: WhatsappTemplate, data: FilledTemplateData) -> bool:
        return template.header_has_variable

    def build(self, template: WhatsappTemplate, data: FilledTemplateData) -> ComponentForPayload:
        if not data.header_parameters:
            raise TemplateHeaderParameterMissing(
                f"La plantilla '{template.name}' tiene una variable en el encabezado y no se completó."
            )
        if template.parameter_format == ParameterFormat.NAMED:
            parameters = [
                NamedParameterForPayload(parameter_name=p.id, text=p.text) for p in data.header_parameters
            ]
        else:
            parameters = [PositionalParameterForPayload(text=p.text) for p in data.header_parameters]
        return ComponentForPayload(type=ComponentType.HEADER, parameters=parameters)


class ButtonComponentBuilder:
    """Los botones que llevan un valor: URL con sufijo dinámico y COPY_CODE.

    A diferencia de los demás, **no emite un componente sino varios**: Meta pide uno por botón, y los
    identifica por su POSICIÓN en el array BUTTONS. De ahí que el armador exponga `build_many`; el
    factory lo contempla.

    Los botones de respuesta rápida, de teléfono y de URL estática no llevan componente — y eso es
    correcto, no un hueco: Meta ya los tiene aprobados tal cual.
    """

    _SUB_TYPES = {"url": ButtonTextParameter, "copy_code": CouponCodeParameter}

    def handles(self) -> Shape:
        return Shape(button_kinds=frozenset({"URL_DINAMICO", "COPY_CODE"}))

    def applies(self, template: WhatsappTemplate, data: FilledTemplateData) -> bool:
        return bool(template.buttons_needing_parameters)

    def build(self, template: WhatsappTemplate, data: FilledTemplateData) -> ComponentForPayload:
        # El factory usa `build_many`; este método existe sólo para cumplir el protocolo.
        componentes = self.build_many(template, data)
        return componentes[0]

    def build_many(self, template: WhatsappTemplate, data: FilledTemplateData) -> list[ComponentForPayload]:
        por_indice = {p.index: p for p in data.button_parameters}
        componentes: list[ComponentForPayload] = []
        for indice, sub_type in template.buttons_needing_parameters:
            valor = por_indice.get(indice)
            if valor is None:
                raise TemplateButtonParameterMissing(
                    f"El botón #{indice + 1} de la plantilla '{template.name}' necesita un valor "
                    f"({sub_type}) y no se completó."
                )
            parametro = self._SUB_TYPES[sub_type]
            campo = "coupon_code" if sub_type == "copy_code" else "text"
            componentes.append(
                ComponentForPayload(
                    type="button", sub_type=sub_type, index=str(indice),
                    parameters=[parametro(**{campo: valor.text})],
                )
            )
        return componentes


class LimitedTimeOfferComponentBuilder:
    """La oferta por tiempo limitado: el reloj que WhatsApp muestra sobre el mensaje.

    Lo único que viaja es cuándo vence. El texto de la oferta ya quedó aprobado en la plantilla.
    """

    def handles(self) -> Shape:
        return Shape(component_types=frozenset({"LIMITED_TIME_OFFER"}))

    def applies(self, template: WhatsappTemplate, data: FilledTemplateData) -> bool:
        return data.offer_expiration_ms is not None and any(
            c.type == ComponentType.LIMITED_TIME_OFFER for c in template.components)

    def build(self, template: WhatsappTemplate, data: FilledTemplateData) -> ComponentForPayload:
        return ComponentForPayload(
            type="limited_time_offer",
            parameters=[LimitedTimeOfferParameter(expiration_time_ms=data.offer_expiration_ms)])


class FlowButtonComponentBuilder:
    """El botón que abre un WhatsApp Flow.

    Lo único que viaja al enviar es el `flow_token`: el id del Flow y la pantalla inicial ya quedaron
    fijados al aprobar la plantilla. El token es lo que permite atar la respuesta del formulario a
    ESTE envío puntual — sin él, llega el `nfm_reply` y no se sabe de quién es.
    """

    def handles(self) -> Shape:
        return Shape(button_kinds=frozenset({"FLOW"}))

    def applies(self, template: WhatsappTemplate, data: FilledTemplateData) -> bool:
        return bool(data.flow_token) and any(
            b.type == ButtonType.FLOW
            for c in template.components if c.type == ComponentType.BUTTONS
            for b in (c.buttons or []))

    def build(self, template: WhatsappTemplate, data: FilledTemplateData) -> ComponentForPayload:
        indice = next(
            (i for c in template.components if c.type == ComponentType.BUTTONS
             for i, b in enumerate(c.buttons or []) if b.type == ButtonType.FLOW), 0)
        return ComponentForPayload(
            type="button", sub_type="flow", index=str(indice),
            parameters=[FlowActionParameter(flow_token=data.flow_token)])


class CarouselComponentBuilder:
    """El carrusel.

    Lo bueno del diseño: los componentes de una tarjeta son los MISMOS que los del mensaje principal
    (encabezado, cuerpo, botones), así que se arman con los mismos armadores en vez de con una rama
    aparte. Sumar un formato nuevo lo hereda el carrusel gratis.

    Meta pide uniformidad entre tarjetas —mismos componentes y mismos tipos de botón— y eso lo valida
    la creación, no el envío: acá las tarjetas ya vienen aprobadas.
    """

    def handles(self) -> Shape:
        return Shape(component_types=frozenset({"CAROUSEL"}))

    def applies(self, template: WhatsappTemplate, data: FilledTemplateData) -> bool:
        return bool(data.carousel_cards) and any(
            c.type == ComponentType.CAROUSEL for c in template.components)

    def build(self, template: WhatsappTemplate, data: FilledTemplateData) -> ComponentForPayload:
        tarjetas = []
        for tarjeta in sorted(data.carousel_cards, key=lambda c: c.index):
            componentes = []
            if tarjeta.header_media and tarjeta.header_media.media_id:
                componentes.append(ComponentForPayload(
                    type=ComponentType.HEADER,
                    parameters=[HeaderMediaParameter(
                        type=tarjeta.header_media.kind, media_id=tarjeta.header_media.media_id,
                        filename=tarjeta.header_media.filename)]))
            if tarjeta.parameters:
                componentes.append(ComponentForPayload(
                    type=ComponentType.BODY,
                    parameters=[PositionalParameterForPayload(text=p.text) for p in tarjeta.parameters]))
            for valor in tarjeta.button_parameters:
                parametro = (CouponCodeParameter(coupon_code=valor.text)
                             if valor.sub_type == "copy_code" else ButtonTextParameter(text=valor.text))
                componentes.append(ComponentForPayload(
                    type="button", sub_type=valor.sub_type, index=str(valor.index),
                    parameters=[parametro]))
            tarjetas.append({"card_index": tarjeta.index,
                             "components": [c.model_dump() for c in componentes]})
        return ComponentForPayload(type="carousel", parameters=[], cards=tarjetas)


class OtpComponentBuilder:
    """El código de una plantilla de autenticación.

    Meta lo pide DOS veces: en el cuerpo (el texto del mensaje lo escribe Meta e inserta el código ahí)
    y en el botón (para que el "copiar" o el autocompletado tengan qué copiar). Mandarlo en uno solo
    hace que la plantilla llegue a medias.
    """

    def handles(self) -> Shape:
        return Shape(button_kinds=frozenset({"OTP"}))

    def applies(self, template: WhatsappTemplate, data: FilledTemplateData) -> bool:
        return bool(data.otp_code) and any(
            b.type == ButtonType.OTP
            for c in template.components if c.type == ComponentType.BUTTONS
            for b in (c.buttons or []))

    def build(self, template: WhatsappTemplate, data: FilledTemplateData) -> ComponentForPayload:
        return self.build_many(template, data)[0]

    def build_many(self, template: WhatsappTemplate, data: FilledTemplateData) -> list[ComponentForPayload]:
        indice = next(
            (i for c in template.components if c.type == ComponentType.BUTTONS
             for i, b in enumerate(c.buttons or []) if b.type == ButtonType.OTP), 0)
        return [
            ComponentForPayload(type=ComponentType.BODY,
                                parameters=[PositionalParameterForPayload(text=data.otp_code)]),
            ComponentForPayload(type="button", sub_type="url", index=str(indice),
                                parameters=[ButtonTextParameter(text=data.otp_code)]),
        ]


# El orden importa y es deliberado: encabezado, cuerpo, botones — como se lee el mensaje. Meta no lo
# exige, pero deja el payload determinista y por lo tanto testeable.
DEFAULT_COMPONENT_BUILDERS: list[TemplateComponentBuilder] = [
    HeaderComponentBuilder(),
    HeaderTextComponentBuilder(),
    BodyComponentBuilder(),
    ButtonComponentBuilder(),
    FlowButtonComponentBuilder(),
    LimitedTimeOfferComponentBuilder(),
    CarouselComponentBuilder(),
    OtpComponentBuilder(),
]


# --- La compuerta, derivada de los armadores ------------------------------------------------------

# Formas que no necesitan ningún componente al enviar porque Meta ya las tiene aprobadas tal cual.
# No son un hueco: son inertes. Se declaran explícitas para que la compuerta no las confunda con algo
# que falta armar.
_FORMAS_INERTES = Shape(
    header_formats=frozenset({"TEXT"}),
    # VOICE_CALL va acá y no en un armador: como el botón de teléfono, Meta ya lo tiene aprobado y no
    # espera ningún valor al enviar. Estaba bloqueado por confundir "no tiene armador" con "no se puede".
    button_kinds=frozenset({"QUICK_REPLY", "PHONE_NUMBER", "URL_ESTATICO", "VOICE_CALL"}),
    component_types=frozenset({"BODY", "FOOTER", "BUTTONS"}),
)


def supported_shape(builders: Optional[Iterable[TemplateComponentBuilder]] = None) -> Shape:
    """Todo lo que Chatty sabe enviar: lo que declaran los armadores más lo inerte."""
    forma = _FORMAS_INERTES
    for builder in (builders if builders is not None else DEFAULT_COMPONENT_BUILDERS):
        forma = forma | builder.handles()
    return forma


def _clasificar_boton(boton: dict) -> str:
    """El botón, en el vocabulario de la capacidad. Un URL no es una forma sola: estático e inerte,
    o con sufijo dinámico y con armador."""
    tipo = str(boton.get("type") or "").upper()
    if tipo == "URL":
        return "URL_DINAMICO" if "{{" in (boton.get("url") or "") else "URL_ESTATICO"
    return tipo


def _clasificar_encabezado(componente: dict) -> str:
    formato = str(componente.get("format") or "TEXT").upper()
    if formato == "TEXT":
        return "TEXT_CON_VARIABLE" if "{{" in (componente.get("text") or "") else "TEXT"
    return formato


def unsupported_shapes(components: Iterable[Any], builders=None) -> list[str]:
    """Qué formas de esta plantilla NO sabe enviar Chatty. Vacío = se puede enviar.

    Trabaja sobre los `components` CRUDOS de Meta (dicts), que es lo que guarda la sincronización, para
    poder decidir sobre plantillas que el modelo tipado ni siquiera parsea.

    Es la única fuente de verdad de la enviabilidad. api-chatty la consulta en vez de mantener su
    propia lista: por construcción no puede quedar desincronizada de los armadores.
    """
    forma = supported_shape(builders)
    faltantes: list[str] = []
    for componente in components or []:
        c = componente if isinstance(componente, dict) else getattr(componente, "__dict__", {})
        tipo = str(c.get("type") or "").upper()
        if tipo == "HEADER":
            clase = _clasificar_encabezado(c)
            if clase not in forma.header_formats:
                faltantes.append(f"encabezado {clase.lower()}")
        elif tipo == "BUTTONS":
            for boton in (c.get("buttons") or []):
                b = boton if isinstance(boton, dict) else getattr(boton, "__dict__", {})
                clase = _clasificar_boton(b)
                if clase not in forma.button_kinds:
                    faltantes.append(f"botón {clase.lower()}")
        elif tipo not in forma.component_types:
            faltantes.append(tipo.lower().replace("_", " "))
    return faltantes
