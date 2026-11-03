"""Sources («fuentes de origen»): the port every source store implements.

A source is its own aggregate, polymorphic by `type` (`SourceFactory` builds the subclass). It includes the motivos it
declares (`motivo_ids`, its mirror `motivo_id` and `mapeo_motivo`, who put them) and the entrada it belongs to
(`entrada_id`). The entity is `letschatty.models.analytics.sources.SourceBase` and its subclasses, unchanged. A read by
id is NOT scoped to a company: the use case checks the company (ADR-007). A deleted source is still returned by id.

Besides the whole source, some reads and writes are targeted, on purpose: the attention flow writes `entrada_id` and
the motivos with a `$set` on `_id` + `company_id` (never rebuilding the source, which would undo what another save
changed), and reads them with a projection. Those methods return or take plain documents.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol

from ...models.analytics.sources import SourceBase
from ...models.utils.types import StrObjectId


#: The conditions a targeted write of the motivos can be made under (the repository knows their query).
#: Not decided by a person (never over what a person chose) and still without motivos: «Sugerir con IA».
UNDECIDED_WITHOUT_REASONS = "undecided_without_reasons"
#: Not decided by a person and without any mapping yet: a source just created.
UNDECIDED_WITHOUT_MAPPING = "undecided_without_mapping"
#: Still pending for the AI and without motivos: the lambda's answer.
PENDING_FOR_THE_AI = "pending_for_the_ai"


class SourceRepository(Protocol):
    """Raises `NotFoundError` when no source has that id."""

    async def get(self, source_id: StrObjectId) -> SourceBase:
        """By id, whatever its company, also a deleted one."""
        ...

    async def list_live(self, company_id: StrObjectId, fresh: bool = False) -> List[SourceBase]:
        """Live sources of the company, whole. `fresh`: never from a cache (after losing a race on a unique index)."""
        ...

    async def list_for_validation(self, company_id: StrObjectId) -> List[SourceBase]:
        """Live sources of the company with only what the uniqueness checks read (name, type, checker, trigger, ad,
        topic, template, url, utm campaign, ads ids, post, entrada, account), read fresh."""
        ...

    async def add(self, source: SourceBase) -> SourceBase:
        """Raises `pymongo.errors.DuplicateKeyError` when a unique index of one-per-account sources refuses it."""
        ...

    async def update(self, source_id: StrObjectId, changes: SourceBase) -> SourceBase:
        """Writes only the fields `changes` was built with, merged onto what is in the store now."""
        ...

    async def delete(self, source_id: StrObjectId) -> SourceBase:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...

    async def patch(self, company_id: StrObjectId, source_id: StrObjectId, fields: Dict[str, Any]) -> None:
        """`$set` of `fields` (and `updated_at`) by id, without reading it: maintenance that is not a person's edit (the
        ad's creative mirror). Raises `NotFoundError` when no source has that id."""
        ...

    # ── entradas (`entrada_id`) ──

    async def entries_of_sources(self, company_id: StrObjectId) -> Dict[str, Optional[str]]:
        """`{source_id: entrada_id | None}` of the company's live sources, read fresh."""
        ...

    async def accounts_of_sources(self, company_id: StrObjectId) -> Dict[str, Optional[str]]:
        """`{source_id: account_id | None}` of the company's live sources as stored, read fresh."""
        ...

    async def set_entry(self, company_id: StrObjectId, source_ids: List[str], entry_id: Optional[str],
                        now: datetime) -> int:
        """`entrada_id` (and `updated_at`) on those sources of the company; how many changed."""
        ...

    async def clear_entry(self, company_id: StrObjectId, entry_id: str, source_ids: Optional[List[str]],
                          now: datetime) -> List[str]:
        """`entrada_id` → None on the company's sources in that entrada (all, or only `source_ids`), live or deleted;
        the released ids."""
        ...

    # ── targeted fields: the motivos (`motivo_ids`, `motivo_id`, `mapeo_motivo`) and the attention migration ──

    async def find_for_mapping(self, company_id: StrObjectId, source_id: StrObjectId) -> Optional[Dict[str, Any]]:
        """The live source of the company with what the mapping reads (a projection), or None."""
        ...

    async def mapping_candidates(self, company_id: StrObjectId, ad_types: List[str]) -> List[Dict[str, Any]]:
        """The company's live sources of those types, or with a mapping the AI put, with what the mapping reads."""
        ...

    async def set_fields(self, company_id: StrObjectId, source_id: StrObjectId, fields: Dict[str, Any],
                          when: Optional[str] = None) -> bool:
        """`$set` of `fields` on the source of the company, and only if it is live and meets `when` (one of the
        conditions above) when given; whether it matched. The motivos' mapping and the attention migration write with
        it."""
        ...

    async def put_back_fields(self, company_id: StrObjectId, source_id: StrObjectId, fields: Dict[str, Any],
                               absent: List[str]) -> None:
        """Fields exactly as in a snapshot: `fields` set, `absent` removed (undoing the motivos' assistant or the
        attention migration)."""
        ...

    # ── cache ──

    async def forget(self, company_id: StrObjectId, source_ids: List[str]) -> None:
        """Drops the cached copies of those sources and of the company's lists, after a targeted write. Never raises:
        the write is already in the store (a failure is logged at ERROR and the copies expire with their TTL)."""
        ...

    async def all_ids(self, company_id: StrObjectId) -> List[str]:
        """The ids of every source of the company, deleted ones included, read fresh."""
        ...

    async def drop_cache(self, company_id: StrObjectId, source_ids: List[str]) -> None:
        """Drops the cached copies of those sources and of the company's lists, on request (sources written outside
        the API). Unlike `forget`, a cache failure raises."""
        ...
