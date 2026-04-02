"""JSON related utilities."""

# Standard Library
import datetime as dt
import json
from typing import Any
from zoneinfo import ZoneInfo

# Third Party
from redis import Redis

# Django
from django.core.cache import caches

try:
    # Third Party
    import django_redis
except ImportError:
    django_redis = None


def get_redis_client() -> Redis:
    """
    Return configured redis client used for Django caching in Alliance Auth.

    Taken from the `allianceauth-app-utils` package.
    Credits to: Erik Kalkoken
    """
    try:
        return django_redis.get_redis_connection("default")
    except AttributeError:
        default_cache = caches["default"]
        return default_cache.get_master_client()


class JSONDateTimeDecoder(json.JSONDecoder):
    """Decoder for the standard json library to decode JSON into datetime.
    To be used together with ``JSONDateTimeEncoder``.

    Example:

        .. code-block:: python

            message = json.loads(message_json, cls=JSONDateTimeDecoder)

    Taken from the `allianceauth-app-utils` package.
    Credits to: Erik Kalkoken
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        :meta private:
        """
        json.JSONDecoder.__init__(
            self, object_hook=self._dict_to_object, *args, **kwargs
        )

    def _dict_to_object(self, dct: dict) -> object:
        if "__type__" not in dct:
            return dct

        type_str = dct.pop("__type__")
        zone, _ = dct.pop("tz")
        if zone:
            dct["tzinfo"] = ZoneInfo(zone)
        try:
            date_obj = dt.datetime(**dct)
            return date_obj
        except (ValueError, TypeError):
            dct["__type__"] = type_str
            return dct


class JSONDateTimeEncoder(json.JSONEncoder):
    """Encoder for the standard json library to encode datetime into JSON.
    To be used together with ``JSONDateTimeDecoder``.

    Works with naive and aware datetimes, but only with UTC timezone.

    Example:

        .. code-block:: python

            message_json = json.dumps(message, cls=JSONDateTimeEncoder)

    Taken from the `allianceauth-app-utils` package.
    Credits to: Erik Kalkoken
    """

    def default(self, o: Any) -> Any:
        """
        :meta private:
        """
        if isinstance(o, dt.datetime):
            tz_name = o.tzinfo.tzname(o) if o.tzinfo else None
            if tz_offset := o.utcoffset():
                tz_total_seconds = tz_offset.total_seconds()
            else:
                tz_total_seconds = None
            timezone_info = tz_name, tz_total_seconds
            return {
                "__type__": "datetime",
                "year": o.year,
                "month": o.month,
                "day": o.day,
                "hour": o.hour,
                "minute": o.minute,
                "second": o.second,
                "microsecond": o.microsecond,
                "tz": timezone_info,
            }

        return json.JSONEncoder.default(self, o)
