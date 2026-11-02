from __future__ import annotations
from enum import StrEnum
import re
from datetime import datetime, timezone
from typing import List, Optional, Any, Dict, Union
from pydantic import BaseModel, Field, field_validator, model_validator

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
    # += (G2 read-model widening): approved templates using these components used to fail this strict
    # enum and vanish from Chatty with no error. They now parse so they can be DISPLAYED. The send path
    # is unchanged (C6) — sendability is decided separately by MetaTemplate.to_whatsapp_template().
    CAROUSEL = "CAROUSEL"
    LIMITED_TIME_OFFER = "LIMITED_TIME_OFFER"

class ButtonType(StrEnum):
    QUICK_REPLY = "QUICK_REPLY"
    URL = "URL"
    PHONE_NUMBER = "PHONE_NUMBER"
    COPY_CODE = "COPY_CODE"
    # += (G2 read-model widening) — display-only; see ComponentType note above.
    FLOW = "FLOW"
    CATALOG = "CATALOG"
    MPM = "MPM"
    OTP = "OTP"
    VOICE_CALL = "VOICE_CALL"


class CarouselCard(BaseModel):
    """Una tarjeta del carrusel.

    Meta exige uniformidad: todas las tarjetas tienen que traer los MISMOS componentes y los mismos
    tipos de botón. Se guarda como venga (los componentes son dicts crudos) porque el carrusel se lee
    para mostrarlo mucho antes de poder enviarlo.
    """

    card_index: Optional[int] = None
    components: List[Dict[str, Any]] = Field(default_factory=list)


class Button(BaseModel):
    type: ButtonType
    # Opcional a propósito: un botón OTP puede venir sin texto y Meta le pone "Copy code" solo.
    # Exigirlo rechazaba la forma MÁS COMÚN de las plantillas de autenticación, que es de las pocas
    # que Meta permite crear sin escribir el cuerpo.
    text: Optional[str] = None
    url: Optional[str] = None
    phone_number: Optional[str] = None
    example: Optional[List[str]] = None
    # --- FLOW ---
    flow_id: Optional[str] = None
    flow_name: Optional[str] = None
    flow_action: Optional[str] = None
    navigate_screen: Optional[str] = None
    # --- OTP (plantillas de autenticación) ---
    # `otp_type` decide si el código se copia a mano, se autocompleta con un toque o entra solo.
    otp_type: Optional[str] = None
    autofill_text: Optional[str] = None

    @field_validator("example", mode="before")
    @classmethod
    def _example_de_copy_code_es_un_texto(cls, valor: Any) -> Any:
        """Meta manda el `example` de un botón COPY_CODE como UN texto (`"example": "250FF"`) y el de
        un botón URL como lista (`["https://…/abc"]`). Con el tipo sólo-lista, crear una plantilla con
        botón de copiar código desde Chatty daba 400 («Input should be a valid list»), y leer una ya
        creada tiraba la sincronización de toda la WABA. Se guarda siempre como lista de un elemento,
        así `example[0]` es el código entero en todos los lectores (y no su primera letra)."""
        return [valor] if isinstance(valor, str) else valor
    package_name: Optional[str] = None
    signature_hash: Optional[str] = None

class HeaderExample(BaseModel):
    """El ejemplo del encabezado, tal como lo devuelve Meta.

    `header_handle` es el archivo (imagen, video, documento). Los otros dos son el ejemplo de un
    encabezado de TEXTO con variable — y faltaban: sin ellos, el `example` de un encabezado de texto
    caía en esta rama de la unión, no matcheaba ningún campo y se parseaba a un objeto vacío. La
    variable del encabezado quedaba invisible para todo lo que viene después, que es exactamente por
    qué esas plantillas se ofrecían y fallaban.
    """

    header_handle: Optional[List[str]] = None
    header_text: Optional[List[str]] = None
    header_text_named_params: Optional[List[NamedParameter]] = None

class HeaderFormat(StrEnum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    # += (G2 read-model widening) — display-only; a media header no longer drops the whole template.
    VIDEO = "VIDEO"
    DOCUMENT = "DOCUMENT"
    LOCATION = "LOCATION"


class TemplateComponent(BaseModel):
    type: ComponentType
    text: Optional[str] = None
    format: Optional[HeaderFormat] = None
    example: Optional[Union[TemplateExample, HeaderExample]] = None
    buttons: Optional[List[Button]] = None
    # --- CAROUSEL ---
    cards: Optional[List[CarouselCard]] = None
    # --- LIMITED_TIME_OFFER ---
    limited_time_offer: Optional[Dict[str, Any]] = None
    # --- AUTHENTICATION ---
    add_security_recommendation: Optional[bool] = None
    code_expiration_minutes: Optional[int] = None

    @model_validator(mode='before')
    def validate_component(cls, values):
        comp_type = values.get('type')
        if comp_type == ComponentType.BUTTONS and not values.get('buttons'):
            raise ValueError("Buttons component must have buttons field")
        # Este modelo lo comparten LEER y CREAR, y sus requisitos son opuestos: al leer, Meta a veces
        # devuelve un encabezado multimedia sin ejemplo y la plantilla igual tiene que poder mostrarse
        # (ese fue el punto de la ampliación G2). Exigir el ejemplo acá haría desaparecer plantillas
        # reales del listado. La exigencia vive en el validador de CREACIÓN, que es donde tiene sentido.
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
        # G10: null-guard the BODY component and its example. An approved template can have an IMAGE header
        # + a param-less BODY (or no BODY at all after the widened read model), leaving body_component None
        # or example None while parameter_format is still POSITIONAL/NAMED. Deref without a guard raised
        # AttributeError and 500'd /required_fields. Missing example -> no parameters.
        body = self.body_component
        if body is None or body.example is None:
            return []
        if self.parameter_format == ParameterFormat.NAMED:
            return body.example.body_text_named_params or []
        elif self.parameter_format == ParameterFormat.POSITIONAL:
            return (body.example.body_text or [[]])[0]
        else:
            return []

    @property
    def body_component(self) -> TemplateComponent:
        return next((component for component in self.components if component.type == ComponentType.BODY), None)

    @property
    def header_component(self) -> TemplateComponent:
        return next((component for component in self.components if component.type == ComponentType.HEADER), None)

    @property
    def requires_header_media(self) -> bool:
        """True si para enviarla hay que adjuntar un archivo (encabezado de imagen, video o documento).

        Delega en `TemplateHeaderKind` para no duplicar qué formatos son multimedia: ahí está la única
        fuente de verdad, y un formato que no manejamos (TEXT, LOCATION) devuelve False.
        """
        from .header_media import TemplateHeaderKind
        header = self.header_component
        if header is None:
            return False
        return TemplateHeaderKind.from_header_format(header.format) is not None

    @property
    def header_has_variable(self) -> bool:
        """El encabezado es de TEXTO y lleva una variable, así que necesita su componente al enviar."""
        header = self.header_component
        if header is None or (header.format or HeaderFormat.TEXT) != HeaderFormat.TEXT:
            return False
        return "{{" in (header.text or "")

    @property
    def header_parameters(self) -> List[str]:
        """Las variables del encabezado, en orden. Meta admite una sola, pero se devuelve lista para
        que el consumidor no tenga que asumirlo."""
        header = self.header_component
        if header is None:
            return []
        return re.findall(r"\{\{(.*?)\}\}", header.text or "")

    @property
    def buttons_needing_parameters(self) -> List[tuple]:
        """`(índice, sub_type)` de cada botón que necesita un valor al enviar.

        El índice es la POSICIÓN en el array BUTTONS: así los identifica Meta. Los de respuesta rápida,
        teléfono y URL estática no aparecen acá porque no llevan componente, que es lo correcto.
        """
        componente = next((c for c in self.components if c.type == ComponentType.BUTTONS), None)
        if componente is None or not componente.buttons:
            return []
        necesitan = []
        for indice, boton in enumerate(componente.buttons):
            if boton.type == ButtonType.URL and "{{" in (boton.url or ""):
                necesitan.append((indice, "url"))
            elif boton.type == ButtonType.COPY_CODE:
                necesitan.append((indice, "copy_code"))
        return necesitan

    @property
    def header_media_example_url(self) -> Optional[str]:
        """La URL del archivo que la empresa cargó en la plantilla al crearla, en el CDN de Meta.

        Meta la devuelve al LEER la plantilla (`example.header_handle`), firmada y descargable sin
        autenticación. Es la imagen que el negocio aprobó y espera mandar, así que sirve de default.

        ⚠️ Caduca (~30 días, ver `header_media_example_expires_at`). No guardar esta URL como si fuera
        estable: hay que bajar el archivo una vez y quedárselo.
        """
        header = self.header_component
        if header is None or header.example is None:
            return None
        handles = getattr(header.example, "header_handle", None)
        return handles[0] if handles else None

    @property
    def header_media_file_id(self) -> Optional[str]:
        """Identidad del archivo del encabezado: el PATH de la URL, sin la firma.

        La URL tiene dos partes: el path (`/v/t61.../698013623_..._n.jpg`), que identifica al archivo y
        NO cambia entre sincronizaciones, y la query (`oh`, `oe`, `_nc_gid`), que es la firma y se
        renueva cada vez. Comparando el path sabemos si la imagen es la misma sin bajar nada — y si
        cambió, sabemos que la reemplazaron en Meta.

        Es identidad de contenido, no una fecha: más confiable que `last_updated_time`, que puede no
        moverse al cambiar la imagen (o moverse por una edición que no la tocó).
        """
        url = self.header_media_example_url
        if not url:
            return None
        from urllib.parse import urlparse
        return urlparse(url).path or None

    @property
    def header_media_example_expires_at(self) -> Optional[datetime]:
        """Cuándo caduca la URL firmada, leído del parámetro `oe` (epoch en hexadecimal).

        Se puede saber SIN tocar la red, así que conviene mirarlo antes de intentar la descarga en vez
        de enterarse por un 403.
        """
        url = self.header_media_example_url
        if not url:
            return None
        from urllib.parse import parse_qs, urlparse
        oe = parse_qs(urlparse(url).query).get("oe", [None])[0]
        if not oe:
            return None
        try:
            return datetime.fromtimestamp(int(oe, 16), tz=timezone.utc)
        except (ValueError, OverflowError, OSError):
            return None

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
