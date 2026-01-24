import json
from typing import Any, Union
from uuid import UUID


class PayloadEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that serializes UUID objects as strings.

    This encoder extends the default `json.JSONEncoder` and overrides the `default` method
    to handle `UUID` instances by converting them to their string representation. For all
    other types, it falls back to the standard encoding behavior.

    Attributes:
        Inherits all attributes from `json.JSONEncoder`.

    Methods:
        default(o): Returns a string representation for UUID objects, otherwise delegates
        to the superclass implementation.
    """

    def default(self, o) -> Union[str, Any]:
        if isinstance(o, UUID):
            return str(o)

        return super().default(o)
