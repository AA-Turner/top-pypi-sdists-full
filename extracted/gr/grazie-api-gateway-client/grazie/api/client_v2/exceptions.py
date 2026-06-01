from typing import Optional

from httpx import HTTPStatusError


class ApiError(Exception):
    pass


class ApiStatusError(ApiError):
    def __init__(self, message: Optional[str] = None, *, exc: HTTPStatusError):
        super().__init__(message or str(exc))
        self.request = exc.request
        self.response = exc.response


class SSEResponseParseError(ApiError):
    pass


class SSERequestFailedError(ApiError):
    pass


# TODO (s): this if for backwards compatibility and remove this eventually
GatewayApiError = ApiError
GatewayApiStatusError = ApiStatusError
