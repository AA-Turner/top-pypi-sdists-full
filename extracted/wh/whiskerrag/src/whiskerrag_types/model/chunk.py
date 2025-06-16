from datetime import datetime, timezone
from typing import Any, List, Optional, Union
from uuid import UUID, uuid4

import numpy as np
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)

from whiskerrag_types.model.knowledge import EmbeddingModelEnum
from whiskerrag_types.model.utils import parse_datetime


class Chunk(BaseModel):
    chunk_id: str = Field(default_factory=lambda: str(uuid4()), description="chunk id")
    space_id: str = Field(..., description="space id")
    tenant_id: str = Field(..., description="tenant id")
    embedding: Optional[list[float]] = Field(None, description="chunk embedding")
    context: str = Field(..., description="chunk content")
    knowledge_id: str = Field(..., description="file source info")
    enabled: bool = Field(True, description="is chunk enabled")
    embedding_model_name: Union[EmbeddingModelEnum, str] = Field(
        EmbeddingModelEnum.OPENAI, description="name of the embedding model"
    )
    metadata: Optional[dict] = Field(
        None, description="Arbitrary metadata associated with the content."
    )
    # Add specific fields as required by metadata rules
    tags: Optional[List[str]] = Field(
        None, description="Tags from knowledge.metadata._tags"
    )
    f1: Optional[str] = Field(None, description="Field 1 from knowledge.metadata._f1")
    f2: Optional[str] = Field(None, description="Field 2 from knowledge.metadata._f2")
    f3: Optional[str] = Field(None, description="Field 3 from knowledge.metadata._f3")
    f4: Optional[str] = Field(None, description="Field 4 from knowledge.metadata._f4")
    f5: Optional[str] = Field(None, description="Field 5 from knowledge.metadata._f5")
    created_at: Optional[datetime] = Field(
        default=None,
        alias="gmt_create",
        description="creation time",
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        alias="gmt_modified",
        description="update time",
    )

    @field_validator("embedding", mode="before")
    @classmethod
    def parse_embedding(cls, v: Union[str, List[float], None]) -> Optional[List[float]]:
        if v is None:
            return None
        if isinstance(v, np.ndarray):
            return v.tolist()

        if isinstance(v, list):
            return [float(x) for x in v]

        if isinstance(v, str):
            v = v.strip()
            try:
                import json

                return (
                    [float(x) for x in json.loads(v)]
                    if isinstance(json.loads(v), list)
                    else None
                )
            except json.JSONDecodeError:
                try:
                    if v.startswith("[") and v.endswith("]"):
                        v = v[1:-1]
                    return [float(x.strip()) for x in v.split(",") if x.strip()]
                except ValueError:
                    raise ValueError(f"Invalid embedding format: {v}")

        raise ValueError(f"Unsupported embedding type: {type(v)}")

    @field_serializer("embedding_model_name")
    def serialize_embedding_model_name(
        self, embedding_model_name: Union[EmbeddingModelEnum, str]
    ) -> str:
        if isinstance(embedding_model_name, EmbeddingModelEnum):
            return embedding_model_name.value
        return str(embedding_model_name)

    def update(self, **kwargs: Any) -> "Chunk":
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.updated_at = datetime.now(timezone.utc)
        return self

    @field_validator("enabled", mode="before")
    @classmethod
    def convert_tinyint_to_bool(cls, v: Any) -> bool:
        return bool(v)

    @model_validator(mode="before")
    def pre_process_data(cls, data: dict) -> dict:
        for field, value in data.items():
            if isinstance(value, UUID):
                data[field] = str(value)
        field_mappings = {"created_at": "gmt_create", "updated_at": "gmt_modified"}
        for field, alias_name in field_mappings.items():
            val = data.get(field) or data.get(alias_name)
            if val is None:
                continue

            if isinstance(val, str):
                dt = parse_datetime(val)
                data[field] = dt
                data[alias_name] = dt
            else:
                if val and val.tzinfo is None:
                    dt = val.replace(tzinfo=timezone.utc)
                    data[field] = dt
                    data[alias_name] = dt

        return data

    @model_validator(mode="after")
    def set_defaults(self) -> "Chunk":
        now = datetime.now(timezone.utc)
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now
        return self

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
