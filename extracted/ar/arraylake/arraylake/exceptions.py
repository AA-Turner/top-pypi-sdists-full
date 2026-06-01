class ArraylakeHttpError(ValueError):
    """Base exception for HTTP-related errors from Arraylake API"""

    def __init__(self, message: str, request_id: str | None = None, status_code: int | None = None):
        super().__init__(message)
        self.request_id = request_id
        self.status_code = status_code

    def __str__(self) -> str:
        msg = super().__str__()
        if self.request_id:
            msg = f"{msg} [request-id: {self.request_id}]"
        return msg


class ArraylakeValidationError(ArraylakeHttpError):
    """422 validation errors from the API"""

    pass


class ArraylakeClientError(ArraylakeHttpError):
    """4xx client errors from the API"""

    pass


class ArraylakeServerError(ArraylakeHttpError):
    """5xx server errors from the API"""

    pass


class BucketNotFoundError(KeyError):
    pass


class AuthException(ValueError):
    pass
