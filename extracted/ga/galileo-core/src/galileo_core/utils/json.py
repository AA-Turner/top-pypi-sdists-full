from json import JSONEncoder
from typing import Any

from pydantic import BaseModel


class PydanticJsonEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, BaseModel):
            return obj.model_dump(mode="json", exclude_none=True, exclude_unset=True)
        return super().default(obj)
