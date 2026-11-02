from pydantic import BaseModel, Field
from typing import Optional
import logging
import json
from datetime import timedelta

from letschatty.models.utils.definitions import Area
logger = logging.getLogger("logger")

class Context(BaseModel):
    company_id: Optional[str] = Field(default=None)
    agent_email: Optional[str] = Field(default=None)
    chat_id: Optional[str] = Field(default=None)
    details: Optional[str] = Field(default=None)
    json_data: Optional[str] = Field(default=None, exclude=True)

    def model_dump_json(self, *args, **kwargs) -> str:
        #exclude none values
        kwargs['exclude_none'] = True
        return super().model_dump_json(*args, **kwargs)

    def model_dump(self, **kwargs):
        return json.loads(self.model_dump_json(**kwargs, exclude_none=True))

class CustomException(Exception):
    def __init__(self, message="Custom exception", status_code=400, company_id:str=None, agent_email:str=None, chat_id:str=None, details:str=None, json_data:str=None):
        self.status_code = status_code
        self.context = Context(company_id=company_id, agent_email=agent_email, chat_id=chat_id, details=details, json_data=json_data)
        super().__init__(f"{self.__class__.__name__}: {message}")

    @property
    def message(self):
        return super().__str__()

    def __str__(self):
        return super().__str__() + f" - Context: {self.context.model_dump_json(indent=4)}"

    def log_error(self):
        logger.error(f"{str(self)} - Context: {self.context}")


class NotFoundError(CustomException):
    def __init__(self, message="Not found", status_code=404, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class MessageNotFoundError(NotFoundError):
    def __init__(self, message="Message not found", status_code=404, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class ChatAlreadyExists(CustomException):
    """The person already has a live chat in that account (`uniq_live_chat_per_account`). The
    caller continues with that chat (`chat_id`) instead of a new one."""
    def __init__(self, chat_id: str, message="The person already has a live chat in this account", status_code=409, **context_data):
        super().__init__(message, status_code=status_code, **context_data)
        self.chat_id = chat_id

class UnauthorizedOrigin(CustomException):
    def __init__(self, message="Unauthorized origin", status_code=403, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class WhatsAppAPIError(CustomException):
    def __init__(self, message="WhatsApp API error", status_code=400, meta_code: Optional[int] = None, transient: bool = False, media_upload: bool = False, meta_message: Optional[str] = None, **context_data):
        super().__init__(message, status_code=status_code, **context_data)
        # meta_code: Meta's numeric error code parsed from the response body (when present).
        # transient: True for retryable transport failures (clean 5xx). Both default-safe so
        # existing call sites that don't pass them keep working.
        self.meta_code = meta_code
        self.transient = transient
        # media_upload: the failure came from POST /media (the file itself was refused),
        # not from POST /messages. Meta answers those with generic codes (100 "Invalid
        # parameter") much more often than the 131052/131053 the async webhook uses, so
        # the code alone cannot tell an agent the FILE was the problem — this flag can.
        self.media_upload = media_upload
        # meta_message: Meta's own explanation, kept verbatim. friendly_failure_reason
        # only maps known codes, so without this the specific text was always discarded.
        self.meta_message = meta_message

class WhatsAppPayloadValidationError(Exception):
    def __init__(self, message="WhatsApp payload validation error", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class ChatWithActiveContinuousConversation(CustomException):
    """
    Raised when an AI agent is triggered on a chat that has an active Continuous Conversation.
    """
    def __init__(self, message="Chat has an active continuous conversation", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class ChattyAIModeOff(CustomException):
    """
    Raised when an AI agent is in OFF mode and cannot be triggered.
    """
    def __init__(self, message="Chatty AI agent is OFF", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class MissingAIAgentInChat(CustomException):
    """
    Raised when a chat has no AI agent assigned but one is required for the operation.
    """
    def __init__(self, message="AI agent not assigned to chat", status_code=404, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class UnsuportedChannel(CustomException):
    def __init__(self, message="Channel not supported", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class ChatNotFoundError(NotFoundError):
    def __init__(self, message="Chat not found", status_code=404, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class MetaReceiverError(CustomException):
    def __init__(self, message="There's been an exception while processing the meta json", status_code=500, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class ImpossibleError(CustomException):
    def __init__(self, message="It's virtually impossible to happen, so if it did, it means the logic is flawed", status_code=500, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class TestException(CustomException):
    def __init__(self, message="Exception produced in testing environment", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class CompanyNotFound(NotFoundError):
    def __init__(self, message="Company not found", status_code=404, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class UnknownMetaNotificationType(CustomException):
    def __init__(self, message="Received a meta notification we don't know how to process", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class InvalidSourceChecker(CustomException):
    def __init__(self, message="Invalid source checker", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class TopicNotFound(NotFoundError):
    def __init__(self, message="Topic not found", status_code=404, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class TopicWithLockedMessages(CustomException):
    def __init__(self, message="Topic with locked messages", status_code=409, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class DuplicatedMessage(CustomException):
    def __init__(self, message="Duplicated message trigger", status_code=406, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class ConflictedSource(CustomException):
    def __init__(self, message="Conflicted source", status_code=409, conflicting_source_id:str=None, **context_data):
        super().__init__(message, status_code=status_code, **context_data)
        self.conflicting_source_id = conflicting_source_id

class SourceNotFound(NotFoundError):
    def __init__(self, message="Source not found", status_code=404, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class FriendlyCodeNotFound(NotFoundError):
    def __init__(self, message="Friendly code not found", status_code=404, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class TemplateNotFound(NotFoundError):
    def __init__(self, message="Template not found", status_code=404, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class MetaBusinessRegistrationError(CustomException):
    def __init__(self, message="Error registering meta business", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class ErrorSendingMessageToWhatsapp(CustomException):
    def __init__(self, message="Error sending message to whatsapp", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class MetaErrorNotification(CustomException):
    def __init__(self, message, status_code, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class AssetAlreadyAssigned(CustomException):
    def __init__(self, message="Asset already assigned", status_code=208, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class MessageAlreadyInChat(CustomException):
    def __init__(self, message="Message already in chat", status_code=409, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class ChatAlreadyAssigned(CustomException):
    def __init__(self, message="Chat already assigned", status_code=208, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class ChatNotAssignedToAgentError(CustomException):
    def __init__(self, message="Chat not assigned to agent", status_code=409, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class InvalidApiKey(CustomException):
    def __init__(self, message="Invalid API key", status_code=401, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class AlreadyCompleted(CustomException):
    def __init__(self, message="Operation already completed", status_code=208, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class ErrorToMantainSafety(CustomException):
    def __init__(self, message="Raised to mantain safety", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class ResetAIAgentMessage(CustomException):
    def __init__(self, message="Raised to reset the agent and not answer the user", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class DatasetIDConversionsAPINotFound(NotFoundError):
    def __init__(self, message="Dataset ID conversions API not found", status_code=404, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class HumanInterventionRequired(CustomException):
    def __init__(self, message="Human intervention required", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class MaximumFollowUpsReached(CustomException):
    def __init__(self, message="Maximum follow ups reached", status_code=400, area: Optional[Area] = Area.WITH_AGENT, **context_data):
        self.area = area
        super().__init__(message, status_code=status_code, **context_data)

class MaximumConsecutiveFollowUpsReached(CustomException):
    def __init__(self, message="Maximum consecutive follow ups reached", status_code=400, area: Optional[Area] = Area.WITH_AGENT, **context_data):
        self.area = area
        super().__init__(message, status_code=status_code, **context_data)

class MaximumTotalFollowUpsReached(CustomException):
    def __init__(self, message="Maximum total follow ups reached", status_code=400, area: Optional[Area] = Area.WITH_AGENT, **context_data):
        self.area = area
        super().__init__(message, status_code=status_code, **context_data)

class PostponeFollowUp(CustomException):
    def __init__(self, time_delta:timedelta,message="Follow up postponed", status_code=400, **context_data):
        self.time_delta = time_delta
        super().__init__(message, status_code=status_code, **context_data)

class PostponeFollowUpTillChatUpdate(CustomException):
    def __init__(self, message="Follow up postponed till chat update", status_code=400, area: Optional[Area] = Area.WITH_AGENT, **context_data):
        self.area = area
        super().__init__(message, status_code=status_code, **context_data)

class ChatStillHasSuggestedMessages(CustomException):
    def __init__(self, message="Chat still has suggested messages", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class SmartFollowUpStrategyNotSet(CustomException):
    def __init__(self, message="Smart follow up strategy not set", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class MissingAIAgentForSmartFollowUp(CustomException):
    def __init__(self, message="Missing AI agent for smart follow up", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class OpenAIError(CustomException):
    def __init__(self, message="OpenAI error", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class NewerAvailableMessageToBeProcessedByAiAgent(CustomException):
    def __init__(self, message="Duplicated incoming message call for ai agent", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


# --- Encabezado multimedia de una plantilla -------------------------------------------------------
# 422 y no 400: el pedido está bien formado, lo que falla es que no cumple lo que la plantilla exige.
# api-chatty ya traduce cualquier CustomException a su `status_code`, así que estas viajan solas como
# 422 hasta quien llama (el chat, una campaña, la API pública) con el motivo en castellano.

class TemplateHeaderMediaMissing(CustomException):
    """La plantilla lleva multimedia en el encabezado y el envío no lo adjuntó."""
    def __init__(self, message="La plantilla necesita un archivo en el encabezado y no se adjuntó", status_code=422, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class TemplateHeaderMediaMismatch(CustomException):
    """El archivo adjuntado no es del tipo que pide el encabezado (p. ej. una imagen donde va un video)."""
    def __init__(self, message="El archivo adjuntado no es del tipo que pide la plantilla", status_code=422, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class TemplateHeaderMediaUnresolved(CustomException):
    """Llegó el archivo pero sin `media_id` de Meta.

    Es un error de programación, no del usuario: significa que se llamó a armar el payload sin haber
    resuelto la media contra Meta. Se corta acá para no mandarle a Meta un encabezado vacío.
    """
    def __init__(self, message="El archivo del encabezado no se resolvió contra Meta antes de armar el envío", status_code=500, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class TemplateHeaderParameterMissing(CustomException):
    """La plantilla tiene una variable en el encabezado y el envío no la completó."""

    def __init__(self, message: str):
        super().__init__(message, status_code=422)


class TemplateButtonParameterMissing(CustomException):
    """Un botón de la plantilla necesita un valor (sufijo de URL o código) y no vino."""

    def __init__(self, message: str):
        super().__init__(message, status_code=422)


class MessagesNotLoaded(CustomException):
    """Se le preguntó por sus mensajes a un chat que no los cargó.

    Desde que los mensajes viven en `chat_messages`, un `Chat` llega sin ellos salvo que el
    cargador los pida. Antes de esta excepción, una propiedad que recorre mensajes sobre una
    lista vacía devolvía vacío o verdadero en silencio (`is_first_message` daba verdadero para
    todos los chats). Falla fuerte para que quien la necesite cargue los mensajes a propósito.
    """
    def __init__(self, message="El chat no tiene los mensajes cargados: pedirlos al cargador", status_code=500, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class FlowStatesNotLoaded(CustomException):
    """Se le preguntó por sus workflows a un chat que no los cargó (viven en `chat_flow_states`)."""
    def __init__(self, message="El chat no tiene los estados de workflow cargados: pedirlos al cargador", status_code=500, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class IdentityAlreadyTaken(CustomException):
    """El teléfono o el BSUID que se quiere escribir en una persona ya es de OTRA persona de la
    empresa (índices únicos de `clients`). Es un caso de fusión, no un error del pedido: quien
    llama decide (loguear y seguir, o fusionar con `ClientCollection.merge`)."""
    def __init__(self, message="La identidad ya es de otra persona de la empresa", status_code=409, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class PersonNotLoaded(CustomException):
    """Se pidió la persona completa (`clients`) y el chat sólo trae la preview."""
    def __init__(self, message="La persona completa no se cargó: pedirla al cargador", status_code=500, **context_data):
        super().__init__(message, status_code=status_code, **context_data)
