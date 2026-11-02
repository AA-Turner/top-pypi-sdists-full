from pydantic import BaseModel, Field, model_validator, ValidationInfo
from typing import Optional
from urllib.parse import urlparse, unquote
from .content_media import ChattyContentMedia

class ChattyContentDocument(ChattyContentMedia):
    filename: str = Field(default=None, description="Name of the document")

    @model_validator(mode='before')
    def validate_filename(cls, data, info: ValidationInfo):
        # `data` isn't always a dict: ChattyContent is a plain (non-discriminated) Union,
        # so pydantic's smart-union resolution can offer this validator an already-built
        # instance of a SIBLING member (e.g. a ChattyContentSticker) while checking whether
        # it could also fit here — before this guard, that crashed with AttributeError
        # (no .get on a BaseModel) any time a non-Document union member was validated.
        if not isinstance(data, dict):
            return data
        if not data.get("filename") and data.get("url"):
            parsed = urlparse(data["url"])
            data["filename"] = unquote(parsed.path.split("/")[-1])
        return data
