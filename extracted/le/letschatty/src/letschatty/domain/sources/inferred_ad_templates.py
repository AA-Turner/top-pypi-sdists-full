"""Learned ad templates («atribución inferida»): the ports every store of them implements.

A template is its own aggregate: one document per (company, account, normalized text) in `inferred_ad_templates`,
with the ads that text was seen arriving from (`linked_ads`, counted per day), its sightings without an ad
(`orphan_msgs`), its status (`learning` | `active` | `excluded`) and the human decisions over its suggestions. The
distinct persons behind each template are a second store, `TemplatePersonCounter` (HyperLogLogs in Redis today).

Not a catalog (ADR-010 of api-chatty): a template is found by its natural key, never by id, listed nor deleted. The
account is part of the key only when there is one: «no account» means «this company has no accounts», and a lookup
without account matches the text of any account. Every write is atomic on one document, and none creates a document
except the labeled sighting (an upsert). Documents travel as the dicts Mongo answers (datetimes naive, in UTC).
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional, Protocol, Sequence


def day_key(when: datetime) -> str:
    """The name of the day bucket a sighting counts in (`linked_ads.<ad>.days.<key>`)."""
    return when.strftime("%Y%m%d")


class InferredAdTemplateRepository(Protocol):
    async def record_labeled(self, company_id: str, account_id: Optional[str], normalized_body: str, *,
                             body_sample: str, template_hash: str, hll_base: Optional[str], ad_source_id: str,
                             ad_id: str, at: datetime, stale_days: Sequence[datetime]) -> Optional[dict]:
        """One sighting of the text arriving from the ad `ad_source_id`, in one atomic upsert. A new document is
        inserted with the text, its sample, its hash, `learning`, `created_at` = `at` and, with an account, the account
        and `hll_base`. The ad's bucket of the day of `at` and its total go up by one, its `ad_id`, `last_seen_at` and the
        document's `updated_at` are `at`, and the ad's buckets of `stale_days` are taken off. Answers the document
        after the write."""
        ...

    async def drop_linked_ad(self, company_id: str, account_id: Optional[str], normalized_body: str,
                             ad_source_id: str) -> None:
        """Takes the ad off the template's `linked_ads`."""
        ...

    async def record_orphan(self, company_id: str, account_id: Optional[str], normalized_body: str) -> Optional[dict]:
        """One sighting without an ad: `orphan_msgs` up by one, only on a document that exists. Answers the document
        after the write, or None when there is none."""
        ...

    async def set_status(self, company_id: str, account_id: Optional[str], normalized_body: str, status: str, *,
                         updated_at: datetime, activated_at: Optional[datetime]) -> None:
        """Sets the status and `updated_at` (and `activated_at` when given) of an existing document."""
        ...

    async def record_decision(self, company_id: str, account_id: Optional[str], template_hash: str, kind: str) -> None:
        """Counts a human decision of `kind` (and the total) on the template with that hash: the first one Mongo finds
        when there is no account."""
        ...


class TemplatePersonCounter(Protocol):
    """Distinct persons per template, approximately (HyperLogLog), by the template's counter base: its `hll_base`, or
    its hash for a template without one."""

    async def add_labeled(self, company_id: str, base: str, person: str) -> None:
        ...

    async def add_orphan(self, company_id: str, base: str, person: str) -> None:
        ...

    async def labeled(self, company_id: str, base: str) -> int:
        ...

    async def orphans(self, company_id: str, base: str) -> int:
        ...
