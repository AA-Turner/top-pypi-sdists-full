"""Encoders for JSON."""

import json
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


class UniversalJSONEncoder(json.JSONEncoder):
    """A JSON encoder that handles custom classes, datetimes, sets, Decimals,
    and falls back to str() for anything else it can't natively encode.
    """

    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()

        if isinstance(o, (set, frozenset)):
            return list(o)

        if hasattr(o, "__dict__") and not callable(o):
            return o.__dict__

        if isinstance(o, (Decimal, UUID)):
            return str(o)

        try:
            return super().default(o)
        except TypeError:
            return str(o)
