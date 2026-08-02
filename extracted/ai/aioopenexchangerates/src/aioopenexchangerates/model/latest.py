"""Provide a model for endpoint latest.json."""

from dataclasses import dataclass

from .response import BaseRatesResponse


@dataclass
class Latest(BaseRatesResponse):
    """Represent the model for endpoint latest.json."""
