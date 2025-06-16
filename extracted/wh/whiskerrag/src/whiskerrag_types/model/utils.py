import hashlib
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from dateutil import parser


class MetadataSerializer:
    @staticmethod
    def deep_sort_dict(data: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
        if isinstance(data, dict):
            return {
                k: MetadataSerializer.deep_sort_dict(data[k])
                for k in sorted(data.keys())
            }
        elif isinstance(data, list):
            return [MetadataSerializer.deep_sort_dict(item) for item in data]
        return data

    @staticmethod
    @lru_cache(maxsize=1024)
    def serialize(metadata: Optional[Dict]) -> Optional[Dict]:
        if metadata is None:
            return None
        sorted_metadata = MetadataSerializer.deep_sort_dict(metadata)
        return sorted_metadata if isinstance(sorted_metadata, dict) else None


def parse_datetime(value: str) -> datetime:
    try:
        dt: datetime = parser.parse(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception as e:
        raise ValueError(f"Invalid datetime format: {value}") from e


def calculate_sha256(text: str) -> str:
    text_bytes = text.encode("utf-8")
    sha256_hash = hashlib.sha256()
    sha256_hash.update(text_bytes)
    return sha256_hash.hexdigest()


__all__ = ["parse_datetime", "calculate_sha256"]
