from pydantic import BaseModel
from typing import Optional

class MetaMultimediaContent(BaseModel):
    caption: Optional[str] = None
    mime_type: str
    sha256: str
    id: str

class MetaImageContent(MetaMultimediaContent):
    pass

class MetaStickerContent(MetaMultimediaContent):
    animated: bool

class MetaAudioContent(MetaMultimediaContent):
    voice: bool

class MetaVideoContent(MetaMultimediaContent):
    pass

class MetaDocumentContent(MetaMultimediaContent):
    filename: str