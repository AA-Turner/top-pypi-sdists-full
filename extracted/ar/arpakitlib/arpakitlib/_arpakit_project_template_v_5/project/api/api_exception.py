from typing import Any

import fastapi.security

from project.api.api_error_codes import APIErrorCodes
from project.api.schema.out.common.error import ErrorCommonSO


class APIException(fastapi.exceptions.HTTPException):
    def __init__(
            self,
            *,
            status_code: int = fastapi.status.HTTP_400_BAD_REQUEST,
            error_common_so: ErrorCommonSO | None = None,
            error_code: str | None = APIErrorCodes.unknown_error,
            error_specification_code: str | None = None,
            error_description: str | None = None,
            error_description_data: dict[str, Any] | None = None,
            error_data: dict[str, Any] | None = None,
            kwargs_: dict[str, Any] | None = None,
            kwargs_create_story_log: bool | None = True,
            kwargs_logging_full_error: bool | None = True,
            kwargs_in_own_exception: dict[str, Any] = None,
    ):
        if error_description_data is None:
            error_description_data = {}
        if error_data is None:
            error_data = {}
        if kwargs_in_own_exception is None:
            kwargs_in_own_exception = {}

        self.status_code = status_code

        if error_common_so is None:
            error_common_so = ErrorCommonSO(
                has_error=True,
                error_code=error_code,
                error_specification_code=error_specification_code,
                error_description=error_description,
                error_description_data=error_description_data,
                error_data=error_data
            )
            self.error_common_so = error_common_so
        else:
            self.error_common_so = error_common_so

        if kwargs_in_own_exception.get("raise_own_exception_if_exception_in_api_router") is True:
            self.error_common_so.error_data["raise_own_exception_if_exception_in_api_router"] = True
            self.error_common_so.error_data["caught_exception_type"] = kwargs_in_own_exception.get(
                "caught_exception_type"
            )
            self.error_common_so.error_data["caught_exception_str"] = kwargs_in_own_exception.get(
                "caught_exception_str"
            )

        if kwargs_ is None:
            kwargs_ = {}
        if "create_story_log" not in kwargs_ and kwargs_create_story_log is not None:
            kwargs_["create_story_log"] = kwargs_create_story_log
            self.error_common_so.error_data["create_story_log"] = kwargs_create_story_log
        if "logging" not in kwargs_ and kwargs_logging_full_error is not None:
            kwargs_["logging_full_error"] = kwargs_logging_full_error
            self.error_common_so.error_data["logging_full_error"] = kwargs_logging_full_error
        self.kwargs_ = kwargs_

        super().__init__(
            status_code=self.status_code,
            detail=self.error_common_so.model_dump(mode="json")
        )

    def __str__(self) -> str:
        return f"{self.status_code=}, {self.error_common_so.error_code=}, {self.error_common_so.error_specification_code=}"

    def __repr__(self) -> str:
        return f"{self.status_code=}, {self.error_common_so.error_code=}, {self.error_common_so.error_specification_code=}"
