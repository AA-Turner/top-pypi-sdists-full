"""Provide a base response model."""

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class BaseResponse(DataClassJSONMixin):
    """Represent a base response."""

    disclaimer: str
    license: str


@dataclass
class BaseRatesResponse(BaseResponse):
    """Represent a base rates response."""

    timestamp: int
    base: str
    rates: dict[str, float]
