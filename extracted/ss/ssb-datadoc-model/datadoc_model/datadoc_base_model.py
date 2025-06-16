from pydantic import BaseModel, ConfigDict


class DatadocBaseModel(BaseModel):
    """Defines configuration which applies to all Models in this package."""

    model_config = ConfigDict(
        validate_assignment=True, use_enum_values=True, extra="forbid"
    )
