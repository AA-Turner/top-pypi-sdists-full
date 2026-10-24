"""Typed receipts for data-fetch tool outcomes."""

from __future__ import annotations

from typing import Literal

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "data_fetch_not_started",
    disposition="envelope",
    label="Data Fetch Not Started",
    family="data_fetch",
    example={"status": "not_started", "message": "This request is not started in chat."},
    maturity="placeholder",
)
class DataFetchNotStarted(KindModel):
    status: Literal["not_started"]
    message: str


__all__ = ["DataFetchNotStarted"]
