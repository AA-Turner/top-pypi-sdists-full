from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from ....meta_message_model.meta_message_json import MetaReferral

class ChattyReferral(BaseModel):
    source_url: str
    source_id: Optional[str] = None
    source_type: Optional[str] = None
    headline: Optional[str] = None
    body: Optional[str] = None
    media_type: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    ctwa_clid: Optional[str] = None

    @property
    def is_default(self) -> bool:
        return self.source_url == "" and self.source_id == "" and self.source_type == ""
    
    @classmethod
    def from_meta(cls, meta_referral: MetaReferral | None) -> ChattyReferral:
        if meta_referral is None:
            return cls.default()
        meta_referral.source_url = meta_referral.source_url.strip() # remove trailing spaces
        return cls(**meta_referral.model_dump())

    @classmethod
    def default(cls) -> ChattyReferral:
        return cls(
            source_url="",
            source_id="",
            source_type=""
        )