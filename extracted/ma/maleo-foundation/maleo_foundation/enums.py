import logging
from enum import IntEnum, StrEnum, Enum
from fastapi import responses

class BaseEnums:
    class EnvironmentType(StrEnum):
        LOCAL = "local"
        STAGING = "staging"
        PRODUCTION = "production"

    class ServiceType(StrEnum):
        BACKEND = "backend"
        FRONTEND = "frontend"

    class ServiceCategory(StrEnum):
        CORE = "core"
        AI = "ai"

    class Service(StrEnum):
        MALEO_STUDIO = "maleo-studio"
        MALEO_NEXUS = "maleo-nexus"
        MALEO_TELEMETRY = "maleo-telemetry"
        MALEO_METADATA = "maleo-metadata"
        MALEO_IDENTITY = "maleo-identity"
        MALEO_ACCESS = "maleo-access"
        MALEO_WORKSHOP = "maleo-workshop"
        MALEO_SOAPIE = "maleo-soapie"
        MALEO_MEDIX = "maleo-medix"
        MALEO_DICOM = "maleo-dicom"
        MALEO_SCRIBE = "maleo-scribe"
        MALEO_CDS = "maleo-cds"
        MALEO_IMAGING = "maleo-imaging"
        MALEO_MCU = "maleo-mcu"

    class StatusType(StrEnum):
        DELETED = "deleted"
        INACTIVE = "inactive"
        ACTIVE = "active"

    class UserType(StrEnum):
        REGULAR = "regular"
        PROXY = "proxy"
        SERVICE = "service"

    class SortOrder(StrEnum):
        ASC = "asc"
        DESC = "desc"

    class TokenType(StrEnum):
        REFRESH = "refresh"
        ACCESS = "access"

    class StatusUpdateType(StrEnum):
        ACTIVATE = "activate"
        DEACTIVATE = "deactivate"
        RESTORE = "restore"
        DELETE = "delete"

    class UpdateType(StrEnum):
        STATUS = "status"
        DATA = "data"

    class OperationType(StrEnum):
        CREATE = "create"
        UPDATE = "update"
        RESTORE = "restore"
        DELETE = "delete"

    class IdentifierTypes(StrEnum):
        ID = "id"
        UUID = "uuid"

    class ServiceControllerType(StrEnum):
        REST = "rest"

    class ClientControllerType(StrEnum):
        HTTP = "http"

    class ClientCategory(StrEnum):
        GOOGLE = "google"
        MALEO = "maleo"

    class KeyType(StrEnum):
        PRIVATE = "private"
        PUBLIC = "public"

    class KeyFormatType(Enum):
        BYTES = bytes
        STRING = str

    class RESTControllerResponseType(StrEnum):
        NONE = "none"
        HTML = "html"
        TEXT = "text"
        JSON = "json"
        REDIRECT = "redirect"
        STREAMING = "streaming"
        FILE = "file"

        def get_response_type(self) -> type[responses.Response]:
            """Returns the corresponding FastAPI Response type."""
            return {
                BaseEnums.RESTControllerResponseType.NONE: responses.Response,
                BaseEnums.RESTControllerResponseType.HTML: responses.HTMLResponse,
                BaseEnums.RESTControllerResponseType.TEXT: responses.PlainTextResponse,
                BaseEnums.RESTControllerResponseType.JSON: responses.JSONResponse,
                BaseEnums.RESTControllerResponseType.REDIRECT: responses.RedirectResponse,
                BaseEnums.RESTControllerResponseType.STREAMING: responses.StreamingResponse,
                BaseEnums.RESTControllerResponseType.FILE: responses.FileResponse,
            }.get(self, responses.Response)

    class MiddlewareLoggerType(StrEnum):
        BASE = "base"
        AUTHENTICATION = "authentication"

    class ServiceLoggerType(StrEnum):
        REPOSITORY = "repository"
        DATABASE = "database"
        APPLICATION = "application"

    class LoggerType(StrEnum):
        MIDDLEWARE = "middleware"
        REPOSITORY = "repository"
        DATABASE = "database"
        APPLICATION = "application"
        CLIENT = "client"

    class LoggerLevel(IntEnum):
        CRITICAL = logging.CRITICAL
        FATAL = logging.FATAL
        ERROR = logging.ERROR
        WARNING = logging.WARNING
        WARN = logging.WARN
        INFO = logging.INFO
        DEBUG = logging.DEBUG
        NOTSET = logging.NOTSET

    class CacheType(StrEnum):
        REPOSITORY = "repository"
        ROUTER = "router"
        CLIENT = "client"

    class CacheTTL(IntEnum):
        TTL_15SC = int(15)
        TTL_30SC = int(30)
        TTL_1MN = int(1*60)
        TTL_5MN = int(5*60)
        TTL_10MN = int(10*60)
        TTL_30MN = int(30*60)
        TTL_1HR = int(1*60*60)
        TTL_6HR = int(6*60*60)
        TTL_12HR = int(12*60*60)
        TTL_1DY = int(1*24*60*60)
        TTL_3DY = int(3*24*60*60)
        TTL_1WK = int(1*7*24*60*60)
        TTL_2WK = int(2*7*24*60*60)
        TTL_1MO = int(1*30*24*60*60)

    class Expiration(IntEnum):
        EXP_15SC = int(15)
        EXP_30SC = int(30)
        EXP_1MN = int(1*60)
        EXP_5MN = int(5*60)
        EXP_10MN = int(10*60)
        EXP_15MN = int(15*60)
        EXP_30MN = int(30*60)
        EXP_1HR = int(1*60*60)
        EXP_6HR = int(6*60*60)
        EXP_12HR = int(12*60*60)
        EXP_1DY = int(1*24*60*60)
        EXP_3DY = int(3*24*60*60)
        EXP_1WK = int(1*7*24*60*60)
        EXP_2WK = int(2*7*24*60*60)
        EXP_1MO = int(1*30*24*60*60)