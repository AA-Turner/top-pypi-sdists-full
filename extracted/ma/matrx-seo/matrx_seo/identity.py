from __future__ import annotations

import hashlib
import json
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any


def _json_default(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    raise TypeError(f"Unsupported identity value: {type(value).__name__}")


def stable_hash(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=_json_default,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


#: Separator for :func:`daily_fact_key` parts (ASCII unit separator — never in a URL,
#: query text or id). The SQL twin in the dedupe migration joins with ``chr(31)``.
DAILY_FACT_KEY_SEPARATOR = "\x1f"


def daily_fact_key(*parts: object) -> str:
    """Identity of one provider-reported daily fact (a GSC or GA4 day row).

    A day's numbers are ONE fact however many collection runs fetch it: the
    daily schedules re-fetch a trailing window on purpose because providers
    revise recent days, so a run-scoped key stored the same day up to seven
    times and every sum over it overcounted. ``None`` and ``""`` collapse.
    Deliberately reproducible in SQL as
    ``encode(sha256(convert_to(concat_ws(chr(31), coalesce(p, '')...), 'UTF8')), 'hex')``.
    """
    joined = DAILY_FACT_KEY_SEPARATOR.join("" if part is None else str(part) for part in parts)
    return hashlib.sha256(joined.encode()).hexdigest()


def collection_identity(
    organization_id: str,
    provider: str,
    capability: str,
    operation: str,
    target_ref: str,
    settings_hash: str,
    observation_period: str,
    *,
    site_id: str | None = None,
    page_id: str | None = None,
    source_crawl_session_id: str | None = None,
) -> str:
    return stable_hash(
        {
            "organization_id": organization_id,
            "provider": provider,
            "capability": capability,
            "operation": operation,
            "target_ref": target_ref,
            "site_id": site_id,
            "page_id": page_id,
            "source_crawl_session_id": source_crawl_session_id,
            "settings_hash": settings_hash,
            "observation_period": observation_period,
        }
    )
