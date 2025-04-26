from dataclasses import asdict, is_dataclass
from decimal import Decimal
from enum import Enum
from json import JSONEncoder
from datetime import date, datetime


class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, Enum):
            return obj.name
        elif is_dataclass(obj):
            return asdict(obj)
        return super().default(obj)