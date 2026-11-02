"""Meta templates saved per company («plantillas de Meta guardadas»): the port every store of them implements.

One row per (company_id, meta_template_id), written by the template sync from what Meta returns. The entity is
`letschatty.models.messages.message_templates.meta_template.MetaTemplate`, unchanged: the lambdas read the
`meta_templates` collection directly. The natural key carries the company, so a read by Meta's id is scoped to it.
A read by the row's own id (`get`, and so `update` and `delete`) is not: whoever calls it already read the row from the
company's list.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol

from ...models.messages.message_templates.meta_template import MetaTemplate
from ...models.utils.types import StrObjectId


class MetaTemplateKeyTaken(Exception):
    """The store refused a second row for the same (company, Meta's template id): the unique index the code was written
    for (prod has none, ENG-94). The store's own error is the cause (`__cause__`)."""

    def __init__(self, company_id: StrObjectId, meta_template_id: str):
        self.company_id, self.meta_template_id = company_id, meta_template_id
        super().__init__(f"Meta template {meta_template_id} of company {company_id} is already stored")


class MetaTemplateRepository(Protocol):
    """Raises `NotFoundError` when no row has that id."""

    async def get(self, company_id: StrObjectId, template_id: StrObjectId) -> MetaTemplate:
        """By the row's id, whatever its company, also a deleted one."""
        ...

    async def get_live(self, company_id: StrObjectId, meta_template_id: str) -> Optional[MetaTemplate]:
        """The company's live row for Meta's template id, or None. Always read from the store, never from a cache."""
        ...

    async def get_any(self, company_id: StrObjectId, meta_template_id: str) -> Optional[MetaTemplate]:
        """The company's row for Meta's template id, also a deleted one, or None. Always read from the store."""
        ...

    async def list_live(self, company_id: StrObjectId) -> List[MetaTemplate]:
        """Live rows of the company, whole."""
        ...

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """Live rows of the company, newest first, as JSON-ready preview dicts."""
        ...

    async def add(self, template: MetaTemplate) -> MetaTemplate:
        """Raises `MetaTemplateKeyTaken` when the store refuses a second row for the same key."""
        ...

    async def update(self, company_id: StrObjectId, template_id: StrObjectId, changes: MetaTemplate) -> MetaTemplate:
        """Writes only the fields `changes` was built with, merged onto what is in the store now. The frozen ones
        (`company_id`, `waba_id`, `meta_template_id`) are never rewritten."""
        ...

    async def delete(self, company_id: StrObjectId, template_id: StrObjectId) -> MetaTemplate:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...

    async def restore(self, template_id: StrObjectId) -> MetaTemplate:
        """Clears `deleted_at` of a deleted row and writes the whole row back."""
        ...

    async def move_to_waba(self, template_id: StrObjectId, waba_id: str) -> None:
        """Writes only `waba_id` (frozen for `update`). Leaves the cache as it is: an `update` always follows."""
        ...
