from json import JSONEncoder
from typing import Any

from pydantic import BaseModel


class PydanticJsonEncoder(JSONEncoder):
    def __init__(
        self,
        *args: Any,
        exclude_none: bool = True,
        exclude_unset: bool = True,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._exclude_none = exclude_none
        self._exclude_unset = exclude_unset

    def default(self, obj: Any) -> Any:
        if isinstance(obj, BaseModel):
            return obj.model_dump(mode="json", exclude_none=self._exclude_none, exclude_unset=self._exclude_unset)
        return super().default(obj)
