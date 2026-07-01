# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, TypedDict

__all__ = ["ApplicationVariantPatchParams", "Configuration"]


class ApplicationVariantPatchParams(TypedDict, total=False):
    configuration: Configuration

    description: str

    name: str


class Configuration(TypedDict, total=False):
    metadata: Dict[str, object]
    """The user-defined application variant metadata."""

    params: object
    """Configuration sent to agent service."""

    raw_configuration: str
    """The raw configuration string for the application variant."""

    type: Literal["WORKFLOW", "PLAN", "STATE_MACHINE"]
