from typing import Any


class BaseBusinessServiceException(Exception):
    def __init__(
            self,
            message: str,
            *,
            data: dict[str, Any] | None = None
    ):
        self.message = message
        if data is None:
            data = None
        self.data = data

    def __str__(self):
        parts = [
            f"{self.__class__.__name__}"
        ]
        if self.message is not None:
            parts.append(f"{str(self.message)}")
        return ', '.join(parts)

    def __repr__(self):
        return str(self)


class SimpleBSException(BaseBusinessServiceException):
    pass
