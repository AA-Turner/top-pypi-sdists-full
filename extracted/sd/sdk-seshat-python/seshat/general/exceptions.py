import typing


class ColDoesNotExistError(Exception):
    def __init__(self, cols: typing.Iterable):
        message = f"columns {' - '.join(cols)} does not exist in dataframe"
        super().__init__(message)


class OnlyGroupRequiredError(Exception):
    def __init__(self):
        messages = "Group SFrame is required for data"
        super().__init__(messages)


class ColIdNotSpecifiedError(Exception):
    def __init__(self):
        message = "Column ID must be specified in schema"
        super().__init__(message)


class SFrameDoesNotExistError(Exception):
    def __init__(self, group_name, key):
        message = "key %s not exists in %s" % (key, group_name)
        super().__init__(message)


class UnknownDataClassError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidModeError(Exception):
    def __init__(self):
        from seshat.data_class import SF_MAP

        message = "Invalid mode. Mode can only be of these items: %s" % " - ".join(
            SF_MAP
        )
        super().__init__(message)


class InvalidArgumentsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class EmptyDataError(Exception):
    def __init__(self, message=None):
        message = message or "Empty data cannot be processed"
        super().__init__(message)


class SchemaNeededForTableCreationError(Exception):
    def __init__(self):
        message = "Schema needed for table creation"
        super().__init__(message)


class DataBaseNotSupportedError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NoConfigSetError(Exception):
    def __init__(self, message: typing.Optional[str] = None):
        message = (
            message
            if message
            else "Config must be set for this to work. Use `seshat configure` to set necessary settings"
        )
        super().__init__(message)


class InvalidJobIgnore(Exception):
    def __init__(self, message=None):
        message = message or ".jobignore file is invalid"
        super().__init__(message)


class EncryptionError(Exception):
    def __init__(self, message=None):
        super().__init__(message)


class EnvFileNotFound(Exception):
    def __init__(self, message=None):
        super().__init__(message)


class RestClientException(Exception):
    """Base exception for REST client errors"""

    def __init__(self, message):
        super().__init__(message)


class BadRequestError(RestClientException):
    """400 Bad Request"""

    pass


class UnauthorizedError(RestClientException):
    """401 Unauthorized"""

    pass


class ForbiddenError(RestClientException):
    """403 Forbidden"""

    pass


class NotFoundError(RestClientException):
    """404 Not Found"""

    pass


class ServerError(RestClientException):
    """5xx Server Error"""

    pass
