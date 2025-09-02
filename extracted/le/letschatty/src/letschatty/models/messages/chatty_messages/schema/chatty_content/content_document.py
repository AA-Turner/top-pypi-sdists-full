from pydantic import BaseModel, Field, model_validator, ValidationInfo
from typing import Optional
from .content_media import ChattyContentMedia

class ChattyContentDocument(ChattyContentMedia):
    filename: str = Field(default=None, description="Name of the document")

    @model_validator(mode='before')
    def validate_filename(cls, data: dict, info: ValidationInfo):
        if not data.get("filename") and data.get("url"):
            data["filename"] = data["url"].split("/")[-1]
        return data