from typing import Any

import fastapi

from arpakitlib.ar_json_util import transfer_data_to_json_str_to_data
from project.api.schema.common import BaseSO


class APIJSONResponse(fastapi.responses.JSONResponse):
    def __init__(
            self, *,
            content: dict[str, Any] | list[Any] | BaseSO | None, status_code: int = fastapi.status.HTTP_200_OK
    ):
        if isinstance(content, dict):
            content = transfer_data_to_json_str_to_data(content)
        elif isinstance(content, list):
            content = transfer_data_to_json_str_to_data(content)
        elif isinstance(content, BaseSO):
            content = transfer_data_to_json_str_to_data(content.model_dump())
        elif content is None:
            content = None
        else:
            raise ValueError(f"unknown content type, type(content)={type(content)}")

        self.content_ = content
        self.status_code_ = status_code

        super().__init__(
            content=content,
            status_code=status_code
        )
