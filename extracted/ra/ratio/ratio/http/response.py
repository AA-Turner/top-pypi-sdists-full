from ratio.http.headers import Headers
from http import HTTPStatus
from typing import TypedDict, NotRequired, Set


class ResponseData(TypedDict):
    code: int
    message: NotRequired[str]
    headers: NotRequired[dict[str, Set[str]]]


STATUS_CODE_LOWER_BOUND = 100
STATUS_CODE_UPPER_BOUND = 600
STATUS_CODE_SUCCESS_LOWER_BOUND = 200
STATUS_CODE_SUCCESS_UPPER_BOUND = 299


class Response:
    """Generic response class for all default responses"""

    code: int
    message: str
    headers: Headers
    __success: bool

    def __init__(self, data: ResponseData) -> None:
        code = data["code"]

        self.code = (
            code
            if STATUS_CODE_LOWER_BOUND < code < STATUS_CODE_UPPER_BOUND
            else HTTPStatus.INTERNAL_SERVER_ERROR.value
        )

        self.message = data.get("message", "")
        self.headers = Headers(data.get("headers", None))

    @classmethod
    def from_http_status(cls, status: HTTPStatus) -> "Response":
        return cls({"code": status.value, "message": status.phrase})

    @property
    def success(self) -> bool:
        return (
            STATUS_CODE_SUCCESS_LOWER_BOUND
            <= self.code
            <= STATUS_CODE_SUCCESS_UPPER_BOUND
        )
