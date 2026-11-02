from typing import Literal, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ToolsetInput(BaseModel):
    """Input model that specifies a toolset, for example a connector."""

    # Strict on purpose: a request model the control plane validates. Clients read
    # sessions through forward-compatible models (``_internal.wire_models``) instead.
    model_config = ConfigDict(extra="forbid")

    type: Literal["connector"]
    id: UUID | None = Field(default=None)
    name: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def _validate_id_xor_name_given(self) -> Self:
        if not (self.id or self.name):
            raise ValueError("Toolset id or name is required.")
        if self.id and self.name:
            raise ValueError("Toolset id and name are mutually exclusive.")
        return self

    @classmethod
    def from_connector_id_or_name(cls, ref: str) -> Self:
        try:
            id = UUID(ref)
            return cls(type="connector", id=id)
        except ValueError:
            return cls(type="connector", name=ref)
