from pydantic import BaseModel, field_validator
from typing import Dict, Any, List, Optional
from ...base_models.chatty_asset_model import CompanyAssetModel
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import Field
import logging
from letschatty.models.utils import StrObjectId
from .account_scope import applies_to_account, normalize_account_ids
logger = logging.getLogger("logger")

class FlowPreview(CompanyAssetModel):
    """This class is only used to preview the workflow. It is not used to create or update the flow."""
    title: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("UTC")))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("UTC")))
    company_id: StrObjectId = Field(alias="companyId")
    visible: bool = Field(default=True)
    es_seguimiento: bool = Field(default=False, description="El switch «Es un seguimiento» del editor de workflows. Lo escribe copilot (dueño del documento); api-chatty lo LEE sin caché en cada envío con workflow_id para registrar el seguimiento con origen `workflow`.")

    # Plain strings (not StrObjectId): api-chatty builds the previews of ALL the company's workflows in one
    # list, and one stored value that is not an ObjectId must not make the whole list unreadable.
    account_ids: List[str] = Field(
        default_factory=list,
        description="Which WhatsApp accounts (numbers) the workflow is limited to. Empty = every account, the ones connected later included. Written by copilot (owner of the document).",
    )

    @field_validator("account_ids", mode="before")
    @classmethod
    def _normalize_account_ids(cls, value: Any) -> List[str]:
        return normalize_account_ids(value)

    def applies_to(self, account_id: Optional[str], default_account_id: Optional[str] = None) -> bool:
        """Can the workflow be linked to a chat of that account? Empty scope = yes. A chat without account is
        the default account's; if that cannot be resolved, a scoped workflow does not apply."""
        return applies_to_account(self.account_ids, account_id, default_account_id)

    @property
    def is_smart_follow_up(self) -> bool:
        """Check if the flow is a smart follow up"""
        return self.title.lower() == "smart follow up"

    @classmethod
    def default_create_instance_method(cls, dict_data: Dict[str, Any]) -> 'FlowPreview':

        return cls(created_at=dict_data.get("created_at", datetime.now(tz=ZoneInfo("UTC"))), updated_at=dict_data.get("updated_at", datetime.now(tz=ZoneInfo("UTC"))), **dict_data)

    def embedding_chunks(self) -> list[dict[str, str]]:
        from .embeddable import build_chunks
        # FlowPreview uses `title` instead of `name`, but keep the chunk key
        # consistent with other assets so retrieval callers don't need to
        # branch per-type.
        return build_chunks("workflow", {"name": self.title, "description": self.description})