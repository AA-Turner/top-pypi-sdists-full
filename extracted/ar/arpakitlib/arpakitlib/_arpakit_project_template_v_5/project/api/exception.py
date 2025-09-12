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
            kwargs_create_story_log: bool = True,
            kwargs_logging_full_error: bool = True,
    ):
        self.status_code = status_code

        if error_common_so is None:
            self.error_code = error_code
            self.error_specification_code = error_specification_code
            self.error_description = error_description
            if error_description_data is None:
                error_description_data = {}
            self.error_description_data = error_description_data
            if error_data is None:
                error_data = {}
            self.error_data = error_data
            self.error_common_so = ErrorCommonSO(
                has_error=True,
                error_code=self.error_code,
                error_specification_code=self.error_specification_code,
                error_description=self.error_description,
                error_description_data=self.error_description_data,
                error_data=self.error_data
            )
        else:
            self.error_common_so = error_common_so
            self.error_code = error_common_so.error_code
            self.error_specification_code = error_common_so.error_specification_code
            self.error_description = error_common_so.error_description
            self.error_description_data = error_common_so.error_description_data
            self.error_data = error_common_so.error_data

        if kwargs_ is None:
            kwargs_ = {}
        if "create_story_log" not in kwargs_:
            kwargs_["create_story_log"] = kwargs_create_story_log
        if "logging" not in kwargs_:
            kwargs_["logging_full_error"] = kwargs_logging_full_error
        self.kwargs_ = kwargs_

        super().__init__(
            status_code=self.status_code,
            detail=self.error_common_so.model_dump(mode="json")
        )
