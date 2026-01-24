import hashlib
import json
from typing import Any

from pydantic import BaseModel


def request_fingerprint(obj: BaseModel | dict[str, Any]) -> str:
    """
    Generate a stable SHA256 fingerprint of a request object
    to deduplicate requests, track operation history, and correlate
    related operations. It should be stable for the same input parameters.

    Uses canonical JSON serialization (sorted keys, compact format)
    to ensure the same input always produces the same hash.

    If the model has fields marked with x-unique (via AnnotatedField(unique=True)),
    only those fields are included in the hash. Otherwise, all fields are hashed.

    Args:
        obj: A Pydantic model or dictionary to fingerprint.

    Returns:
        A SHA256 hex digest string that uniquely identifies the request.

    Example:
        >>> from connector_sdk_types import request_fingerprint, ListAccounts
        >>> req = ListAccounts(custom_attributes=["email"])
        >>> fingerprint = request_fingerprint(req)
        >>> # fingerprint = "a3f2b8c1d4e5..." (64 char hex string)
    """
    if isinstance(obj, BaseModel):
        unique_fields = [
            name
            for name, field_info in obj.model_fields.items()
            if isinstance(field_info.json_schema_extra, dict)
            and field_info.json_schema_extra.get("x-unique")
        ]

        all_data = obj.model_dump(mode="json", exclude_none=True)

        if unique_fields:
            data = {k: v for k, v in all_data.items() if k in unique_fields}
        else:
            data = all_data
    else:
        data = obj

    # Canonical JSON: sorted keys, no whitespace, ensure_ascii for portability
    canonical_json = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
