"""JSON Serializers."""

import json
from datetime import datetime
from typing import Any


class JsonDateTimeEncoder(json.JSONEncoder):
    """Add ability to encode datetime to JSON encoder"""

    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)
