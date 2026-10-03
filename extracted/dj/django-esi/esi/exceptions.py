import dataclasses

from aiopenapi3.errors import (
    HTTPClientError as base_HTTPClientError, HTTPError, HTTPServerError as base_HTTPServerError,
)


class ESIErrorLimitException(Exception):
    """ESI Global Error Limit Exceeded
    https://developers.eveonline.com/docs/services/esi/best-practices/#error-limit
    """

    def __init__(self, reset: float | None = None, message: str | None = None) -> None:
        super().__init__(reset, message)
        self.reset = reset
        self.message = message or (
            f"ESI Error limited. Reset in {reset} seconds." if reset else "ESI Error limited."
        )

    def __str__(self) -> str:
        return self.message


class ESIBucketLimitException(Exception):
    """Endpoint (Bucket) Specific Rate Limit Exceeded"""

    def __init__(self, bucket, reset: float = 0, message: str | None = None) -> None:
        super().__init__(bucket, reset, message)
        self.bucket = bucket
        self.reset = reset if reset else self.bucket.window
        self.message = message or f"ESI bucket limit reached for {bucket}."

    def __str__(self) -> str:
        return self.message


@dataclasses.dataclass(repr=False)
class HTTPNotModified(HTTPError):
    """The HTTP Status is 304"""

    status_code: int
    headers: dict[str, str]

    def __str__(self):
        return f"""<{self.__class__.__name__} {self.status_code} {self.headers}>"""


@dataclasses.dataclass(repr=False)
class HTTPClientError(base_HTTPClientError):
    """HTTP Response Code 4xx"""
    pass


@dataclasses.dataclass(repr=False)
class HTTPServerError(base_HTTPServerError):
    """HTTP Response Code 5xx"""
    pass


class TaskBucketLimitException(Exception):
    def __init__(self, bucket, reset) -> None:
        super().__init__(bucket, reset)
        self.bucket = bucket
        self.reset = reset

    def __str__(self) -> str:
        return f"Task Bucket Limit Exceeded: {self.bucket} - Retry after {self.reset} seconds"
