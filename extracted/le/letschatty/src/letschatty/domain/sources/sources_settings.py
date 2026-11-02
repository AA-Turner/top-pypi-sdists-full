"""Sources settings of a company («ajustes de fuentes»): the port every store of them implements.

One document per company (collection `sources_settings`, `_id` = the company id as text). It holds the settings
(today one, `fuentes_web_copian_smart_message`), who saved them last (`updated_by`) and when (`updated_at`). Not a
catalog (ADR-010 of api-chatty): the document is read and upserted by its natural key, the company, never listed nor
created by id, and nothing is cached.

The settings travel as a plain dict: their model, defaults and validation live in api-chatty
(`application/sources/sources_settings.py`), so a new setting needs no letschatty release.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional, Protocol


class SourcesSettingsRepository(Protocol):
    async def stored(self, company_id: str) -> Optional[Dict[str, Any]]:
        """What the company's document stores, without `_id`, `updated_by` nor `updated_at` (fields the settings do not
        know included); None when it has no document."""
        ...

    async def save(self, company_id: str, settings: Dict[str, Any], *, updated_by: Optional[str],
                   updated_at: datetime) -> None:
        """Upserts the company's document setting `settings`, `updated_by` and `updated_at`; any other field it has
        stays."""
        ...
