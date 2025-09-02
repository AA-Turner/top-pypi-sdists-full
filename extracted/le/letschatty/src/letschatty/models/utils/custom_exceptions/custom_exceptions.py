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

class UnauthorizedOrigin(CustomException):
    def __init__(self, message="Unauthorized origin", status_code=403, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class WhatsAppAPIError(CustomException):
    def __init__(self, message="WhatsApp API error", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class WhatsAppPayloadValidationError(Exception):
    def __init__(self, message="WhatsApp payload validation error", status_code=400, **context_data):
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
    def __init__(self, message="Maximum follow ups reached", status_code=400, area:Area = Area.WITH_AGENT, **context_data):
        self.area = area
        super().__init__(message, status_code=status_code, **context_data)


class PostponeFollowUp(CustomException):
    def __init__(self, time_delta:timedelta,message="Follow up postponed", status_code=400, **context_data):
        self.time_delta = time_delta
        super().__init__(message, status_code=status_code, **context_data)

class SmartFollowUpStrategyNotSet(CustomException):
    def __init__(self, message="Smart follow up strategy not set", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)

class MissingAIAgentForSmartFollowUp(CustomException):
    def __init__(self, message="Missing AI agent for smart follow up", status_code=400, **context_data):
        super().__init__(message, status_code=status_code, **context_data)