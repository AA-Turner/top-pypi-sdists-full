from pydantic import BaseModel, Field


class MetaBaseModel(BaseModel):
    """Base model with metadata support for all shop system models."""

    metadata: dict = Field(default_factory=dict, exclude=True)
