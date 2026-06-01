"""Reusable base models for csrd-utils schemas."""

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict


class BaseModel(_BaseModel):
    """Baseline model with strict unknown-field handling."""

    model_config = ConfigDict(extra="forbid")
