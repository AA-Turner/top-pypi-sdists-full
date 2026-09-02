"""Structured-information block models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class StructuredInfoItem(BaseModel):
    text: str
    label: str | None = None


class StructuredInfoSection(BaseModel):
    heading: str
    body: str | None = None
    items: list[StructuredInfoItem] = Field(default_factory=list)


class StructuredInfoBlockData(BaseModel):
    title: str
    description: str | None = None
    sections: list[StructuredInfoSection] = Field(default_factory=list)
