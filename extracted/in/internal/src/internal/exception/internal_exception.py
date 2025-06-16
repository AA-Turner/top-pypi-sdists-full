from fastapi import status
from .base_exception import InternalBaseException


class BadGatewayException(InternalBaseException):
    code = "error_bad_gateway"
    message = "Bad gateway"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_502_BAD_GATEWAY, self.code, _message, **kwargs)


class GatewayTimeoutException(InternalBaseException):
    code = "error_gateway_timeout"
    message = "Gateway timeout"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_504_GATEWAY_TIMEOUT, self.code, _message, **kwargs)


class DatabaseInitializeFailureException(InternalBaseException):
    code = "error_database_initialize"
    message = "Database initialize failure"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, self.code, _message, **kwargs)


class DatabaseConnectFailureException(InternalBaseException):
    code = "error_database_connect"
    message = "Database connect failure"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, self.code, _message, **kwargs)


class NoChangeException(InternalBaseException):
    code = "error_no_change"
    message = "Document no change"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_200_OK, self.code, _message, **kwargs)


class PermissionDeniedException(InternalBaseException):
    code = "error_permission_denied"
    message = "Permission denied"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_403_FORBIDDEN, self.code, _message, **kwargs)


class ParamValidationException(InternalBaseException):
    code = "error_validation"
    message = "Invalid parameter or incorrect format"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, self.code, _message, **kwargs)


class RedisInitializeFailureException(InternalBaseException):
    code = "error_redis_initialize"
    message = "Redis initialize failure"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, self.code, _message, **kwargs)


class RedisConnectFailureException(InternalBaseException):
    code = "error_redis_connect"
    message = "Redis connect failure"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, self.code, _message, **kwargs)
