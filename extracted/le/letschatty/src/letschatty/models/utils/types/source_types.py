from enum import StrEnum

class SourceType(StrEnum):
    OTHER_SOURCE = "other_source"
    PURE_AD = "pure_ad"
    DEFAULT_SOURCE = "default_source"
    WHATSAPP_DEFAULT_SOURCE = "whatsapp_default_source"
    TOPIC_DEFAULT_SOURCE = "topic_default_source"
    UTM_SOURCE = "utm_source"
    PURE_AD_UTM_SOURCE = "pure_ad_utm_source"
    GOOGLE_AD_UTM_SOURCE = "google_ad_utm_source"
    TEMPLATE_SOURCE = "template_source"
    @classmethod
    def list(cls):
        return [member.value for member in cls]

class SourceCheckerType(StrEnum):
    SMART_MESSAGES = "smart_messages"
    SIMILARITY = "similarity"
    FIRST_CONTACT = "first_contact"
    REFERRAL = "referral"
    LITERAL = "literal"
    AD_ID_IN_UTM_PARAMS = "ad_id_in_utm_params"
    CHATTY_PIXEL = "chatty_pixel"
    TEMPLATE = "template"

source_checker_types_schema = {
    SourceCheckerType.SMART_MESSAGES: {
        "label": "Smart Messages de Chatty (recomendado)",
        "description": "Chatty administra y asigna mensajes de forma inteligente para hacer el seguimiento de la fuente de origen del contacto."
    },
    SourceCheckerType.SIMILARITY: {
        "label": "Coincidencia por significado con IA",
        "description": "Existirá match cuando el texto disparador sea similar en significado (evaluado con técnicas de IA) al mensaje que envíe el usuario."
    },
    SourceCheckerType.LITERAL: {
        "label": "Coincidencia exacta dentro del mensaje",
        "description": "Existirá match sólo cuando el texto disparador esté literalmente incluido en el mensaje que envíe el usuario."
    },
    SourceCheckerType.FIRST_CONTACT: {
        "label": "Primer contacto (nuevo chat) sin fuente de origen",
        "description": "Método interno de Chatty utilizado para asignar la fuente de origen predeterminada de WhatsApp a nuevos contactos que no tienen una fuente de origen específica."
    },
    SourceCheckerType.REFERRAL: {
        "label": "Anuncios Click to WhatsApp (META)",
        "description": "Chatty reconoce directamente los anuncios de Click to WhatsApp de META como fuentes de origen, identificando el ID del anuncio."
    },
    SourceCheckerType.AD_ID_IN_UTM_PARAMS: {
        "label": "ID del anuncio en parámetros UTM",
        "description": "El ID del anuncio está en los parámetros UTM, aplica a campañas de Google Ads y Meta Ads con objetivos de redirección a la web"
    },
    SourceCheckerType.CHATTY_PIXEL: {
        "label": "Botón WhatsApp con Chatty Pixel",
        "description": "ChattyPixel es una herramienta de Chatty que te permite identificar la fuente de origen de los usuarios que visitan tu website."
    },
    SourceCheckerType.TEMPLATE: {
        "label": "Plantilla de mensaje",
        "description": "Chatty reconoce directamente las plantillas de mensaje como fuentes de origen, identificando el nombre de la plantilla."
    }
}

source_types_schema = {
    SourceType.OTHER_SOURCE: {
        "label": "Fuentes personalizadas con links a WhatsApp",
        "description": "Crea la fuente de origen que desees identificar, selecciona un método de identificación y Chatty te dará un link para compartir con tus clientes."
    },
    SourceType.PURE_AD: {
        "label": "Anuncios Click to WhatsApp (META)",
        "description": "Chatty reconoce directamente los anuncios de Click to WhatsApp de META como fuentes de origen, identificando el ID del anuncio."
    },
    SourceType.UTM_SOURCE: {
        "label": "Website con UTM y ChattyPixel",
        "description": "Instala el ChattyPixel en tu website y Chatty capturará los datos de UTM para identificar la fuente de origen o crearla automáticamente."
    },
    SourceType.GOOGLE_AD_UTM_SOURCE: {
        "label": "Google ADS con destino web (search, display, etc.)",
        "description": "Crea una fuente de origen para cada anuncio de Google Ads con destino web, y Chatty lo identificará automáticamente vía parámetros UTM."
    },
    SourceType.PURE_AD_UTM_SOURCE: {
        "label": "META Ads con destino web (tráfico, ventas, etc.)",
        "description": "Crea una fuente de origen para cada anuncio de Meta Ads con destino web, y Chatty lo identificará automáticamente vía parámetros UTM."
    },
    SourceType.WHATSAPP_DEFAULT_SOURCE: {
        "label": "Primer contacto (nuevo chat) sin fuente de origen",
        "description": "Método interno de Chatty utilizado para asignar la fuente de origen predeterminada de WhatsApp a nuevos contactos que no tienen una fuente de origen específica."
    },
    SourceType.TOPIC_DEFAULT_SOURCE: {
        "label": "Fuente para mensajes de topics sin fuente de origen",
        "description": "Fuente predeterminada de Chatty para usuarios que envían un smart message de un topic, sin que tengan una fuente de origen específica."
    }
}

def get_label(source_checker_type: SourceCheckerType | SourceType) -> str:
    if isinstance(source_checker_type, SourceCheckerType):
        return source_checker_types_schema[source_checker_type]["label"]
    return source_types_schema[source_checker_type]["label"] if source_checker_type in source_types_schema else "No se encontró el label"

def get_description(source_checker_type: SourceCheckerType | SourceType) -> str:
    if isinstance(source_checker_type, SourceCheckerType):
        return source_checker_types_schema[source_checker_type]["description"]
    return source_types_schema[source_checker_type]["description"] if source_checker_type in source_types_schema else "No se encontró la descripción"
