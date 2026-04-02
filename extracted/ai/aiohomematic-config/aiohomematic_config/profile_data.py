"""Pydantic data models for easymode profile definitions."""

from typing import Literal

from pydantic import BaseModel


class ProfileParamConstraint(BaseModel):
    """Constraint for a single parameter within a profile definition."""

    constraint_type: Literal["fixed", "list", "range"]
    value: float | None = None
    values: list[float] | None = None
    default: float | None = None
    min_value: float | None = None
    max_value: float | None = None


class ProfileDef(BaseModel):
    """Raw profile definition from parsed TCL data."""

    id: int
    name: dict[str, str]
    description: dict[str, str]
    params: dict[str, ProfileParamConstraint] = {}


class ChannelProfileSet(BaseModel):
    """All profile definitions for a receiver/sender channel type pair."""

    profiles: list[ProfileDef]


class ResolvedProfile(BaseModel):
    """Profile resolved for a specific locale, ready for API response."""

    id: int
    name: str
    description: str
    editable_params: list[str]
    fixed_params: dict[str, float]
    default_values: dict[str, float]
