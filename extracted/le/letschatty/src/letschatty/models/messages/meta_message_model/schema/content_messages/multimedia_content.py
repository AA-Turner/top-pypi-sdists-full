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
    # filename is optional in Meta's WhatsApp Cloud API spec — clients can send
    # documents without a filename. ChildMetaMessageFactory derives the filename
    # from the URL path when it's missing (see child_meta_message_factory.py).
    filename: Optional[str] = None