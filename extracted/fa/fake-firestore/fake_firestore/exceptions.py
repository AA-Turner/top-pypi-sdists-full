from typing import Any, Optional


class ClientError(Exception):
    code: Optional[int] = None

    def __init__(self, message: str, *args: Any) -> None:
        self.message = message
        super().__init__(message, *args)

    def __str__(self) -> str:
        return "{} {}".format(self.code, self.message)


class Conflict(ClientError):
    code: Optional[int] = 409


class NotFound(ClientError):
    code: Optional[int] = 404


class AlreadyExists(Conflict):
    pass
