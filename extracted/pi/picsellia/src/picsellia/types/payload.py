from typing import Any
from uuid import UUID

from pydantic import BaseModel


class RectangleFormat(BaseModel):
    x: int
    y: int
    w: int
    h: int
    label_id: UUID
    score: float | int
    text: str | None = None


class PolygonFormat(BaseModel):
    polygon: list[list[int]]
    label_id: UUID
    score: float | int
    text: str | None = None


class ClassificationFormat(BaseModel):
    label_id: UUID
    score: float | int
    text: str | None = None


class KeypointFormat(BaseModel):
    keypoints: list[list[int]]
    label_id: UUID
    score: float | int
    text: str | None = None


class LineFormat(BaseModel):
    line: list[list[int]]
    label_id: UUID
    score: float | int
    text: str | None = None


class PointFormat(BaseModel):
    point: tuple[int, int]
    label_id: UUID
    score: float | int
    text: str | None = None


class EvaluationFormat(BaseModel):
    classifications: list[ClassificationFormat] | None = None
    keypoints: list[KeypointFormat] | None = None
    lines: list[LineFormat] | None = None
    points: list[PointFormat] | None = None
    polygons: list[PolygonFormat] | None = None
    rectangles: list[RectangleFormat] | None = None
    custom_metrics: dict[str, Any] | None = None
