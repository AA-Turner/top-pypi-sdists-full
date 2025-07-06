import json
from typing import Any, Union
from uuid import UUID


class PayloadEncoder(json.JSONEncoder):
    def default(self, obj) -> Union[str, Any]:
        if isinstance(obj, UUID):
            return str(obj)

        return super().default(obj)
