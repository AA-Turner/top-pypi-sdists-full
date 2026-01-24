from typing import Any, Dict, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator

ChunkMetaDataValueType = Union[bool, str, int, float]


class Document(BaseModel):
    content: str = Field(description="Content of the document.", validation_alias="page_content")
    metadata: Dict[str, ChunkMetaDataValueType] = Field(default_factory=dict, validate_default=True)

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    @field_validator("metadata", mode="before")
    def filter_metadata(cls, metadata: Any) -> Dict[str, ChunkMetaDataValueType]:
        # We don't want to throw an error due to unexpected metadata, so we filter it out.
        if not isinstance(metadata, Dict):
            return dict()
        return {key: val for key, val in metadata.items() if isinstance(val, (bool, str, int, float))}
