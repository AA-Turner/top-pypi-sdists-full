"""The media library («biblioteca de medios»): the port every media-asset store implements and the rules of a listing
filter.

A library file (`MediaAsset`, unchanged) is its own aggregate, one document of `media_assets`. A read by id is NOT
scoped to a company: the use case checks it (ADR-007 of api-chatty). A deleted file is still returned by id. Only
deliberately-saved files have a row: conversation sends and received WhatsApp media live only in S3.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol, Tuple

from ...models.company.assets import MediaAsset, MediaOrigin, MediaType
from ...models.utils.types import StrObjectId

# Folder names that mean "no folder filter" (the old S3 listing's semantics).
CATCH_ALL_FOLDERS = ("", "all", "starred")
# Avatars and logos (SYSTEM) and the images of the templates (TEMPLATE) are not the user's files: a listing without
# an explicit origin leaves them out (and keeps the old rows without an `origin`).
HIDDEN_BY_DEFAULT = (MediaOrigin.SYSTEM.value, MediaOrigin.TEMPLATE.value)


@dataclass(frozen=True)
class MediaAssetFilter:
    """What a listing asks for, already validated. `origin` None = every origin but `HIDDEN_BY_DEFAULT`."""

    type: Optional[str] = None
    folder: Optional[str] = None
    origin: Optional[str] = None
    starred: bool = False
    uploaded_by: Optional[str] = None
    search: Optional[str] = None

    @classmethod
    def of(cls, *, type: Optional[str] = None, folder: Optional[str] = None, origin: Optional[str] = None,
           starred: Optional[bool] = None, uploaded_by: Optional[str] = None,
           search: Optional[str] = None) -> "MediaAssetFilter":
        """Raises `ValueError` on an unknown type (checked first) or origin."""
        media_type = None
        if type and str(type).lower() != MediaType.ALL.value:
            media_type = MediaType(type).value
        folder_name = None
        if folder is not None and str(folder).strip().lower() not in CATCH_ALL_FOLDERS:
            folder_name = MediaAsset.normalize_folder(folder)
        return cls(type=media_type, folder=folder_name, origin=MediaOrigin(origin).value if origin else None,
                   starred=bool(starred), uploaded_by=uploaded_by or None, search=search or None)


class MediaAssetRepository(Protocol):
    """Raises `NotFoundError` when no file has that id."""

    async def get(self, asset_id: StrObjectId) -> MediaAsset:
        """By id, whatever its company, also a deleted one."""
        ...

    async def page(self, company_id: StrObjectId, filter: MediaAssetFilter, descending: bool,
                   cursor: Optional[str], limit: int) -> Tuple[List[MediaAsset], Optional[str]]:
        """Up to `limit` live files of the company that match, by (`created_at`, id), after the opaque `cursor`; and
        the cursor of the next page (None on the last one). A cursor that cannot be read starts from the first page."""
        ...

    async def find_by_s3_key(self, company_id: StrObjectId, s3_key: str) -> Optional[MediaAsset]:
        """A live file of the company with that key: the first the store finds (not sorted)."""
        ...

    async def find_by_sha256(self, company_id: StrObjectId, sha256: str) -> Optional[MediaAsset]:
        """The oldest live file of the company with that content hash."""
        ...

    async def add(self, asset: MediaAsset) -> MediaAsset: ...

    async def edit(self, company_id: StrObjectId, asset_id: StrObjectId, fields: Dict[str, Any]) -> None:
        """Writes only `fields` (and `updated_at`) on a file of `company_id`; the change shows in its listings. A write
        that must not reach the listings is `record_use`."""
        ...

    async def record_use(self, asset_id: StrObjectId, use_count: int, last_used_at: datetime) -> None:
        """Writes the use counter and the last use (and `updated_at`): a sort hint, which the company's listings show
        when they expire, not before."""
        ...

    async def delete(self, asset_id: StrObjectId) -> MediaAsset:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...
