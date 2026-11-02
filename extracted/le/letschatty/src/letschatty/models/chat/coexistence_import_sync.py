"""
Tracks the progress of a one-time WhatsApp Coexistence *history import* for a
company. When a coexistence number connects, Meta backfills the owner's prior
WhatsApp Business App conversations as a stream of ordered, idempotent chunks
(the `history` webhook) plus a contacts sync (`smb_app_state_sync`). This record
is the durable bookmark for that backfill: which chunks have already been applied
(``seen_chunks``, for idempotency), the furthest reported ``max_progress``, the
running import counts, and whether the backfill is still ``in_progress`` or has
``completed``. One record per company (keyed by ``company_id``), stored in its
own collection — NOT inside the Chat.
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import List, Optional

from pydantic import Field

from letschatty.models.utils.types import StrObjectId
from ..base_models.chatty_asset_model import ChattyAssetModel


class ImportSyncStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class CoexistenceImportSync(ChattyAssetModel):
    company_id: StrObjectId = Field(frozen=True, description="Company whose WhatsApp Business App history is being imported")
    phone_number_id: Optional[str] = Field(default=None, description="The coexistence phone_number_id this import belongs to")
    status: ImportSyncStatus = Field(default=ImportSyncStatus.IN_PROGRESS)
    seen_chunks: List[str] = Field(default_factory=list, description="Chunk keys already applied, for idempotent re-delivery handling")
    max_progress: float = Field(default=0.0, description="Furthest 0-100 progress percentage reported by any processed chunk")
    messages_imported: int = Field(default=0, description="Total historical messages imported so far")
    contacts_imported: int = Field(default=0, description="Total contacts imported from the state sync so far")
    threads_imported: int = Field(default=0, description="Total distinct customer threads imported so far")
    last_chunk_at: Optional[datetime] = Field(default=None, description="UTC time of the most recent processed chunk; quiescence clock for the finalizer sweep")
    notification_id: Optional[str] = Field(default=None, description="Id of the INFO Notification tracking this import's progress")
