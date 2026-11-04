"""Global betas («betas globales», api-chatty `docs/empresa/ajustes-de-la-plataforma.md`): the port every store of them
implements, and how a stored value is read.

One document for the whole platform (collection `platform_settings`, `_id` "global"): the list `betas_globales` and who
switched one last (`updated_by`) and when (`updated_at`). There is no company: a beta in the list is on for every one.
Not a catalog (ADR-010 of api-chatty): one document by its natural key, never listed nor created by id.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional, Protocol


def clean_global_betas(value: Any) -> List[str]:
    """A list of text, without duplicates and in the stored order (the first one stays). Anything else is `[]`."""
    if not isinstance(value, list):
        return []
    betas: List[str] = []
    for beta in value:
        text = str(beta)
        if text not in betas:
            betas.append(text)
    return betas


class GlobalBetasRepository(Protocol):
    async def enabled(self) -> List[str]:
        """The global betas, cleaned (`clean_global_betas`); `[]` without a document."""
        ...

    async def switch(self, beta: str, on: bool, *, updated_by: Optional[str], updated_at: datetime) -> List[str]:
        """Adds (`on`) or removes `beta` from the list without reading nor rewriting it, upserting the document, and
        sets who and when. Returns the resulting list, cleaned."""
        ...
