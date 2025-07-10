"""Module for pidname definitions"""

from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from aind_data_schema_models.registries import Registry


class BaseName(BaseModel):
    """A simple model associating a name with an abbreviation"""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    name: str = Field(..., title="Name")
    abbreviation: Optional[str] = Field(default=None, title="Abbreviation")


class PIDName(BaseName):
    """
    Model for associate a name with a persistent identifier (PID),
    the registry for that PID, and abbreviation for that registry
    """

    registry: Optional[Union[Registry, str]] = Field(default=None, title="Registry")
    registry_identifier: Optional[str] = Field(default=None, title="Registry identifier")
