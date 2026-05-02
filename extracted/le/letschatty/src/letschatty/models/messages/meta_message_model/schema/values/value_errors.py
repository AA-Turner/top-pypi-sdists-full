from typing import Optional, Dict
from pydantic import BaseModel, Field
from enum import Enum

# -------------------------
# Notas de la Documentación
# -------------------------
# https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes/#otros-errores
# entry.changes.value.errors
# entry.changes.value.messages.errors

# -------------------------
# Modelos de Pydantic
# -------------------------

class ErrorData(BaseModel):
    messaging_product: Optional[str] = Field(default="")
    details: str

class Error(BaseModel):
    message: str
    type: Optional[str] = Field(default="")
    code: int
    error_data: ErrorData
    error_subcode: Optional[int] = Field(default=None)  # Obsoleto en versiones 16.0+
    fbtrace_id: Optional[str] = Field(default=None)

class ErrorResponse(BaseModel):
    error: Error

# -------------------------
# Funciones Utilitarias
# -------------------------

def get_error_details(code: int) -> Optional[Dict[str, str]]:
    """
    Obtiene los detalles del error basándose en el código de error.
    
    :param code: Código de error entero.
    :return: Diccionario con 'description', 'solution' y 'http_status' si el código existe, de lo contrario None.
    """
    return ERROR_CODE_DETAILS.get(code)




# -------------------------
# Enumeraciones de Errores
# -------------------------

class ErrorCode(Enum):
    # Errores de autorización
    EXCEPTION_AUTH = 0
    NOT_AUTHORIZED = 401
    METHOD_API = 3
    INTERNAL_SERVER_ERROR = 500
    PERMISSION_DENIED = 10
    TOKEN_EXPIRED = 190
    API_PERMISSION = range(200, 300) 

    # Errores de limitación
    TOO_MANY_API_CALLS = 4
    INVALID_REQUEST = 400
    FREQUENCY_LIMIT_PROBLEMS = 80007
    WHATSAPP_BUSINESS_FREQUENCY_LIMIT = 80007
    RATE_LIMIT_HIT = 130429
    FREQUENCY_LIMIT = 131048
    SPAM_FREQUENCY_LIMIT = 131056
    BUSINESS_ACCOUNT_CLIENT_FREQUENCY_LIMIT = 133016

    # Errores de integración
    TEMPORARILY_BLOCKED_POLICY_VIOLATION = 368
    BUSINESS_ACCOUNT_COUNTRY_RESTRICTION = 130497
    ACCOUNT_BLOCKED = 131031
    ACCESS_DENIED = 131005
    MISSING_REQUIRED_PARAMETER = 131008
    INVALID_PARAMETER_VALUE = 131009
    SERVICE_UNAVAILABLE_TEMPORARILY = 131016
    RECIPIENT_CANNOT_BE_SENDER = 131021
    MESSAGE_CANNOT_BE_SENT = 131026
    BUSINESS_PAYMENT_ISSUE = 131042
    INCORRECT_CERTIFICATE = 131045
    MEDIA_DOWNLOAD_ERROR = 131052
    MEDIA_UPLOAD_ERROR = 131053
    MAINTENANCE_MODE = 131057
    TEMPLATE_PARAMETER_COUNT_MISMATCH = 132000
    TEMPLATE_DOES_NOT_EXIST = 132001
    TEMPLATE_TEXT_TOO_LONG = 132005
    TEMPLATE_FORMAT_POLICY_VIOLATION = 132007
    TEMPLATE_PARAMETER_FORMAT_MISMATCH = 132012
    TEMPLATE_PAUSED = 132015
    TEMPLATE_DEACTIVATED = 132016
    PROCESS_LOCKED = 132068
    PROCESS_LIMITED = 132069
    INCOMPLETE_REGISTRATION_REVOCATION = 133000
    TEMPORARILY_UNAVAILABLE_SERVER = 133004
    API_SERVICE_UNAVAILABLE = 133005
    PIN_MISMATCH = 133006
    PHONE_VERIFICATION_REQUIRED = 133008
    TOO_MANY_PIN_ATTEMPTS = 133009
    PIN_ENTRY_TOO_FAST = 133010
    PHONE_NOT_REGISTERED = 133015
    GENERIC_USAGE_ERROR = 135000

    # Otros errores
    UNKNOWN_API = 1
    API_SERVICE = 2
    INVALID_PHONE_NUMBER_DELETED = 33
    INVALID_PHONE_NUMBER = 100
    USER_EXPERIMENT = 130472
    UNKNOWN_ERROR = 131000

# -------------------------
# Mapeo de Códigos de Error
# -------------------------

ERROR_CODE_DETAILS: Dict[int, Dict[str, str]] = {
    0: {
        "description": "Excepción de autenticación",
        "solution": "Obtener un nuevo token de acceso.",
        "http_status": "401 Unauthorized"
    },
    401: {
        "description": "No autorizado",
        "solution": "Obtener un nuevo token de acceso.",
        "http_status": "401 Unauthorized"
    },
    3: {
        "description": "Método de la API",
        "solution": "Usar el depurador de token de acceso para comprobar permisos.",
        "http_status": "500 Internal Server Error"
    },
    500: {
        "description": "Error de servidor interno",
        "solution": "Intentar nuevamente más tarde.",
        "http_status": "500 Internal Server Error"
    },
    10: {
        "description": "Permiso denegado",
        "solution": "Verificar permisos y número de teléfono autorizado.",
        "http_status": "403 Forbidden"
    },
    190: {
        "description": "El token de acceso caducó",
        "solution": "Obtener un nuevo token de acceso.",
        "http_status": "401 Unauthorized"
    },

    4: {
        "description": "Demasiadas llamadas a la API",
        "solution": "Reducir la frecuencia de las consultas o esperar antes de reintentar.",
        "http_status": "400 Bad Request"
    },
    400: {
        "description": "Solicitud incorrecta",
        "solution": "Verificar la sintaxis y los parámetros de la solicitud.",
        "http_status": "400 Bad Request"
    },
    80007: {
        "description": "Problemas de límite de frecuencia",
        "solution": "Reducir la frecuencia de las consultas a la API.",
        "http_status": "400 Bad Request"
    },
    130429: {
        "description": "Se alcanzó el límite de frecuencia",
        "solution": "Esperar antes de reintentar o reducir la frecuencia de envío de mensajes.",
        "http_status": "400 Bad Request"
    },
    131048: {
        "description": "Se alcanzó el límite de frecuencia de spam",
        "solution": "Mejorar la calidad de los mensajes y reducir la frecuencia.",
        "http_status": "400 Bad Request"
    },
    131056: {
        "description": "Se alcanzó el límite de frecuencia de la combinación de cuenta de empresa y cuenta de cliente",
        "solution": "Esperar antes de reintentar enviar mensajes al mismo número de teléfono.",
        "http_status": "400 Bad Request"
    },
    133016: {
        "description": "Se excedió el límite de frecuencia de anulación del registro del registro de cuenta",
        "solution": "Esperar a que el número de teléfono se desbloquee antes de intentar nuevamente.",
        "http_status": "400 Bad Request"
    },
    368: {
        "description": "Bloqueado temporalmente por infracción de las políticas",
        "solution": "Revisar y cumplir con las políticas de la plataforma.",
        "http_status": "403 Forbidden"
    },
    130497: {
        "description": "La cuenta de empresa no puede enviar mensajes a los usuarios de este país",
        "solution": "Consultar la política de mensajes para países permitidos.",
        "http_status": "403 Forbidden"
    },
    131031: {
        "description": "Se bloqueó la cuenta",
        "solution": "Revisar el documento de políticas y resolver las infracciones.",
        "http_status": "403 Forbidden"
    },
    131005: {
        "description": "Acceso denegado",
        "solution": "Verificar permisos y usar el depurador de tokens de acceso.",
        "http_status": "403 Forbidden"
    },
    131008: {
        "description": "Falta un parámetro obligatorio",
        "solution": "Incluir todos los parámetros obligatorios en la solicitud.",
        "http_status": "400 Bad Request"
    },
    131009: {
        "description": "El valor del parámetro no es válido",
        "solution": "Verificar los valores de los parámetros y su formato.",
        "http_status": "400 Bad Request"
    },
    131016: {
        "description": "Servicio no disponible",
        "solution": "Esperar y reintentar más tarde.",
        "http_status": "500 Internal Server Error"
    },
    131021: {
        "description": "El destinatario no puede ser el emisor",
        "solution": "Enviar mensajes a números de teléfono diferentes al emisor.",
        "http_status": "400 Bad Request"
    },
    131026: {
        "description": "El mensaje no se puede enviar",
        "solution": "Verificar el número de teléfono del destinatario y la versión de WhatsApp.",
        "http_status": "400 Bad Request"
    },
    131042: {
        "description": "Elegibilidad de la empresa: problema de pago",
        "solution": "Revisar la configuración de facturación y métodos de pago.",
        "http_status": "400 Bad Request"
    },
    131045: {
        "description": "Certificado incorrecto",
        "solution": "Registrar el número de teléfono correctamente.",
        "http_status": "500 Internal Server Error"
    },
    131052: {
        "description": "Error de descarga del archivo multimedia",
        "solution": "Pedir al usuario que envíe el archivo por otro canal.",
        "http_status": "400 Bad Request"
    },
    131053: {
        "description": "Error al subir el archivo multimedia",
        "solution": "Inspeccionar y confirmar que el tipo de MIME es compatible.",
        "http_status": "400 Bad Request"
    },
    131057: {
        "description": "Cuenta en modo de mantenimiento",
        "solution": "Esperar a que termine el mantenimiento.",
        "http_status": "500 Internal Server Error"
    },
    132000: {
        "description": "No coincide el conteo de parámetros de plantilla",
        "solution": "Asegurar que el número de parámetros en la solicitud coincida con la plantilla.",
        "http_status": "400 Bad Request"
    },
    132001: {
        "description": "La plantilla no existe",
        "solution": "Verificar que la plantilla esté aprobada y que el nombre y el idioma sean correctos.",
        "http_status": "404 Not Found"
    },
    132005: {
        "description": "Texto de plantilla traducido demasiado largo",
        "solution": "Revisar la traducción de la plantilla en el administrador de WhatsApp.",
        "http_status": "400 Bad Request"
    },
    132007: {
        "description": "Se infringió la política de caracteres de formato de plantilla",
        "solution": "Revisar y corregir el contenido de la plantilla según las políticas de WhatsApp.",
        "http_status": "400 Bad Request"
    },
    132012: {
        "description": "No coincide el formato de parámetro de plantilla",
        "solution": "Asegurar que los parámetros cumplen con el formato especificado en la plantilla.",
        "http_status": "400 Bad Request"
    },
    132015: {
        "description": "La plantilla está en pausa",
        "solution": "Editar y mejorar la calidad de la plantilla para reactivarla.",
        "http_status": "400 Bad Request"
    },
    132016: {
        "description": "La plantilla está desactivada",
        "solution": "Crear una nueva plantilla con otro contenido.",
        "http_status": "400 Bad Request"
    },
    132068: {
        "description": "Proceso bloqueado",
        "solution": "Corregir el proceso que está bloqueado.",
        "http_status": "400 Bad Request"
    },
    132069: {
        "description": "Proceso limitado",
        "solution": "Corregir el proceso que ha excedido el límite de mensajes.",
        "http_status": "400 Bad Request"
    },
    133000: {
        "description": "Anulación del registro incompleta",
        "solution": "Anular el registro del número nuevamente.",
        "http_status": "500 Internal Server Error"
    },
    133004: {
        "description": "Servidor no disponible temporalmente",
        "solution": "Revisar el estado de la plataforma y reintentar más tarde.",
        "http_status": "503 Service Unavailable"
    },
    133005: {
        "description": "No coincide el PIN de verificación en dos pasos",
        "solution": "Verificar el PIN o restablecerlo siguiendo las instrucciones.",
        "http_status": "400 Bad Request"
    },
    133006: {
        "description": "Es necesario volver a verificar el número de teléfono",
        "solution": "Verificar el número de teléfono antes de registrarlo.",
        "http_status": "400 Bad Request"
    },
    133008: {
        "description": "Demasiados intentos incorrectos de ingreso del PIN de verificación en dos pasos",
        "solution": "Esperar el tiempo especificado antes de reintentar.",
        "http_status": "400 Bad Request"
    },
    133009: {
        "description": "Intento de ingreso del PIN de verificación en dos pasos demasiado rápido",
        "solution": "Esperar antes de reintentar ingresar el PIN.",
        "http_status": "400 Bad Request"
    },
    133010: {
        "description": "Número de teléfono no registrado",
        "solution": "Registrar el número de teléfono en la Plataforma de WhatsApp Business.",
        "http_status": "400 Bad Request"
    },
    133015: {
        "description": "Espera unos minutos antes de volver a intentar registrar este número de teléfono",
        "solution": "Esperar 5 minutos antes de reenviar la solicitud.",
        "http_status": "400 Bad Request"
    },
    135000: {
        "description": "Error de uso genérico",
        "solution": "Verificar la sintaxis de la solicitud y contactar al soporte si el error persiste.",
        "http_status": "400 Bad Request"
    },
    1: {
        "description": "API desconocida",
        "solution": "Verificar la referencia del punto de conexión y la sintaxis de la solicitud.",
        "http_status": "400 Bad Request"
    },
    2: {
        "description": "Servicio de API",
        "solution": "Revisar el estado de la plataforma y reintentar más tarde.",
        "http_status": "503 Service Unavailable"
    },
    33: {
        "description": "Valor no válido del parámetro",
        "solution": "Verificar que el número de teléfono de la empresa sea correcto.",
        "http_status": "400 Bad Request"
    },
    100: {
        "description": "Parámetro inválido",
        "solution": "Corregir los parámetros de la solicitud según la referencia del punto de conexión.",
        "http_status": "400 Bad Request"
    },
    130472: {
        "description": "El número del usuario es parte de un experimento",
        "solution": "Consultar Experimento con mensaje de marketing.",
        "http_status": "400 Bad Request"
    },
    131000: {
        "description": "Se produjo un error",
        "solution": "Reintentar o contactar al soporte si el error persiste.",
        "http_status": "500 Internal Server Error"
    }
}
