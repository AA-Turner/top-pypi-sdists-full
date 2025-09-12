from typing import Any

from pydantic import Field

from project.api.schema.common import BaseSO


class ErrorCommonSO(BaseSO):
    has_error: bool = True
    error_code: str | None = None
    error_specification_code: str | None = None
    error_description: str | None = None
    error_description_data: dict[str, Any] = Field(default_factory=dict)
    error_data: dict[str, Any] = Field(default_factory=dict)
