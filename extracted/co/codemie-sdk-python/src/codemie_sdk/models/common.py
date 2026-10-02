from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TokensUsage(BaseModel):
    input_tokens: int | None = None
    output_tokens: int | None = None
    money_spent: float | None = None

    model_config = ConfigDict(extra="ignore")


class User(BaseModel):
    """Model representing the User."""

    def __getitem__(self, key):
        return getattr(self, key)

    model_config = ConfigDict(extra="ignore")

    user_id: str = Field(None)
    username: str = ""
    name: str = ""

    @model_validator(mode="before")
    def before_init(cls, values):
        # Check if 'id' is present, then set 'id' field for correct deserialization
        if "id" in values:
            values["user_id"] = values.pop("id")
        return values


class PaginationParams(BaseModel):
    """Pagination parameters with validation."""

    page: int = Field(..., ge=0, description="Page number (0-based)")
    per_page: int = Field(..., gt=0, description="Number of items per page")

    def to_dict(self) -> dict[str, Any]:
        """Convert pagination parameters to dictionary."""
        return self.model_dump(exclude_none=True)
