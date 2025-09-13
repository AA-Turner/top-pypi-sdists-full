from typing import Any

from project.api.schema.out.common.error import ErrorCommonSO


class BaseBusinessServiceException(Exception):
    def __init__(
            self,
            message: str,
            *,
            data: dict[str, Any] | None = None,
            data_api_error_status_code: int | None = None,
            data_api_error_error_common_so: ErrorCommonSO | None = None,
    ):
        self.message = message
        if data is None:
            data = {}
        self.data = data
        if data_api_error_status_code is not None:
            self.data["data_api_error_status_code"] = data_api_error_status_code
        if data_api_error_error_common_so is not None:
            self.data["data_api_error_error_common_so"] = data_api_error_error_common_so

    @property
    def data_api_error_status_code(self) -> int | None:
        return self.data.get("data_api_error_status_code")

    @property
    def data_api_error_common_so(self) -> ErrorCommonSO | None:
        return self.data.get("data_api_error_common_so")

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
