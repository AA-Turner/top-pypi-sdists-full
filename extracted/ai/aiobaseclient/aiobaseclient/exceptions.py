from izihawa_utils.exceptions import BaseError


class ClientError(BaseError):
    code = "client_error"


class PermanentError(ClientError):
    code = "permanent_error"


class TemporaryError(ClientError):
    code = "temporary_error"


class BadRequestError(PermanentError):
    code = "bad_request_error"


class ExternalServiceError(ClientError):
    code = "external_service_error"

    def __init__(self, url: str, status_code: int, text: str) -> None:
        self.info = {
            "url": url,
            "status_code": status_code,
            "text": text,
        }


class AuthorizationRequiredError(ClientError):
    code = "authorization_error"


class NotFoundError(PermanentError):
    code = "not_found_error"


class MethodNotAllowedError(PermanentError):
    code = "method_not_allowed_error"


class ServiceUnavailableError(TemporaryError):
    code = "service_unavailable_error"


class TooManyRequestsError(TemporaryError):
    code = "too_many_requests_error"


class WrongContentTypeError(PermanentError):
    code = "wrong_content_type_error"
