from ..base_models.chatty_asset_model import ChattyAssetModel
from ..utils.types import StrObjectId
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from ..utils.types import MessageSubtype

class Highlight(ChattyAssetModel):
    creator_id: StrObjectId
    title: str
    description: str
    starred: bool
    subtype : MessageSubtype
    in_chat: bool = Field(default=False, description="La nota se muestra en la conversación, en la posición de su created_at. Las notas viejas y las de sistema quedan en False: nunca aparecen en el hilo")
    edited_at: Optional[datetime] = Field(default=None, description="Última vez que cambió el título o el texto (la «editada» de la nota). Sumarla o sacarla del chat, o destacarla, no la marca")

class HighlightRequestData(BaseModel):
    title: str
    description: str
    starred: bool = Field(default=False)
    subtype : MessageSubtype = Field(frozen=True, default=MessageSubtype.USER_NOTE)
    in_chat: bool = Field(default=False)

class HighlightUpdateData(BaseModel):
    """Edición de una nota: sólo cambia lo que viene. Lo ausente (o null) se conserva.

    `ChatService.update_highlight` acepta también un `HighlightRequestData` (los llamadores de siempre
    mandan título y texto); de ese también se aplica sólo lo que se informó."""
    title: Optional[str] = None
    description: Optional[str] = None
    starred: Optional[bool] = None
    in_chat: Optional[bool] = None
