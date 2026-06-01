from typing import Any, Dict

from pydantic import BaseModel, Field


class SignalDefinition(BaseModel):
    name: str = Field(description="Name of the signal")
    description: str | None = Field(default=None, description="Description of the signal")
    input_schema: Dict[str, Any] = Field(
        description="Input JSON schema of the signal's model",
        json_schema_extra={"additionalProperties": True},
    )
    # Signals don't have an output schema from the sender's perspective


class QueryDefinition(BaseModel):
    name: str = Field(description="Name of the query")
    description: str | None = Field(default=None, description="Description of the query")
    input_schema: Dict[str, Any] = Field(
        description="Input JSON schema of the query's model",
        json_schema_extra={"additionalProperties": True},
    )
    output_schema: Dict[str, Any] | None = Field(
        default=None,
        description="Output JSON schema of the query's model",
        json_schema_extra={"additionalProperties": True},
    )


class UpdateDefinition(BaseModel):
    name: str = Field(description="Name of the update")
    description: str | None = Field(default=None, description="Description of the update")
    input_schema: Dict[str, Any] = Field(
        description="Input JSON schema of the update's model",
        json_schema_extra={"additionalProperties": True},
    )
    output_schema: Dict[str, Any] | None = Field(
        default=None,
        description="Output JSON schema of the update's model",
        json_schema_extra={"additionalProperties": True},
    )
